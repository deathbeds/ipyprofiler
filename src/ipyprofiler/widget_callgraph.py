"""Render a profile as directed graph."""

from __future__ import annotations

from typing import Any, Dict, List

import ipywidgets as W
import jinja2
import traitlets as T

from .constants import SPEEDSCOPE_SIMPLE_JSON, DOMClasses, MermaidDirection
from .widget_profile import ProfileJSON

CSS_COLLAPSED = "jprf-Callgraph-Options-expanded"

#: syntactically-meaningful characters to escape in mermaid labels
MERMAID_ESCAPE = {
    "[": 91,
    "]": 93,
    "<": 8249,
    ">": 8250,
    "(": 40,
    ")": 41,
    "{": 123,
    "}": 125,
    "/": 47,
    "\\": 92,
}

DEFAULT_MERMAID_TEMPLATE = """%%{init: {"flowchart": {{ mermaid_options | tojson }}} }%%
flowchart {{ direction }}

{% set global_indexes = [] %}
{% set edge_styles = {} %}

{% macro draw_edge(edge, i) -%}
    {%- set _ = global_indexes.append(global_indexes.__len__()) -%}
    {%- set indexes = [global_indexes[-1]] -%}
    {%- set hide = i < first_edge or (last_edge != -1 and i > last_edge) -%}
    {%- set edge_style = ["-->", "~~~"][hide] -%}
    {{ edge.source }} {{ edge_style }}
    {%- if show_time -%}
        {{ edge.id }}>
            {%- if time_precision == -1 -%}
            {{ edge.time }}
            {%- else -%}
            {{ edge.time | round(time_precision) }}
            {%- endif -%}
        ] {{ edge_style }}
        {%- set _ = global_indexes.append(global_indexes.__len__()) -%}
        {%- set indexes = [global_indexes[-2], global_indexes[-1]] -%}
    {%- endif %} {{ edge.target }}

    {%- if first_edge != -1 and first_edge == i %}
    {% set _ = edge_styles.__setitem__("stroke:blue;", indexes) %}
    {%- endif %}
    {%- if last_edge != -1 and last_edge == i %}
    {% set _ = edge_styles.__setitem__("stroke:red;", indexes) %}
    {%- endif %}
{% endmacro %}

{% macro add_edge_style(indexes, style) -%}
    linkStyle {{ indexes | join(",") }} {{ style }}
{%- endmacro %}

{% for node in nodes -%}
    {{ node.id }}([{{ escape_mmd(node.name) }}])
{% endfor -%}

{% if group_by_file %}
    {% for group in groups %}
    subgraph {{ group.id }} [{{ escape_mmd(group.file or "???") }}]
        {% for node_id in group.nodes %}
        {{ node_id }}
        {% endfor -%}
    end
    {% endfor %}
{% endif %}

{%- for edge in edges %}
    {{ draw_edge(edge, loop.index) }}
{%- endfor -%}

{% for style, indexes in edge_styles.items() %}
    {{ add_edge_style(indexes, style) }}
{% endfor %}
"""

CHECKBOX_TRAITS = ["show_time", "group_by_file", "use_elk"]
SELECT_TRAITS = {"direction": MermaidDirection}
SLIDER_TRAITS = ["first_edge", "last_edge", "time_precision"]
OPTION_GROUPS = {
    "Layout": ["direction", "use_elk"],
    "Content": ["show_time", "group_by_file", "time_precision"],
    "Playback": ["first_edge", "last_edge"],
}

RENDER_ON_TRAITS = [*CHECKBOX_TRAITS, *SELECT_TRAITS, *SLIDER_TRAITS, "template"]


def no_elk(widgets: dict[str, W.Widget]) -> bool:
    """Handle widget that don't work with elk."""
    return bool(widgets["use_elk"].value)


TRAIT_DISABLED_IF = {
    "first_edge": no_elk,
    "last_edge": no_elk,
}


@W.register
class Callgraph(W.HBox):
    """Display a call graph from a profile."""

    profile: ProfileJSON = T.Instance(ProfileJSON)
    output: W.Output = T.Instance(W.Output)
    options: CallgraphOptions = T.Instance(
        "ipyprofiler.widget_callgraph.CallgraphOptions"
    )

    show_options = T.Bool(default_value=False).tag(sync=True)

    show_time: bool = T.Bool(
        default_value=False, help="whether to show times on edges"
    ).tag(sync=True)
    time_precision: int = T.Int(min=-1, max=10).tag(sync=True)
    template: str = T.Unicode().tag(sync=True)
    mermaid_options: dict[str, Any] = T.Dict().tag(sync=True)
    use_elk: bool = T.Bool(default_value=False).tag(sync=True)
    group_by_file: bool = T.Bool(default_value=False).tag(sync=True)
    direction: MermaidDirection = T.UseEnum(MermaidDirection)
    first_edge: int = T.Int(-1).tag(sync=True)
    last_edge: int = T.Int(-1).tag(sync=True)

    def __init__(self, **kwargs: Any):
        """Create a new callgraph widget."""
        super().__init__(**kwargs)
        self.children = self._default_children()
        self.add_class(DOMClasses.callgraph.value)

    @T.observe(*RENDER_ON_TRAITS)
    def render(self, *_change: T.Bunch) -> None:
        """Update the output."""
        self.output.outputs = (
            {
                "output_type": "display_data",
                "data": {"text/vnd.mermaid": self._mermaid()},
                "metadata": {},
            },
        )

    def _mermaid(self) -> str:
        """Get a mermaid string."""
        template = jinja2.Template(self.template)
        context = self._context()
        return template.render(context)

    def _context(self) -> dict[str, Any]:
        """Get a rendering context."""
        context = {
            **self.profile.to_callgraph(),
            "show_time": self.show_time,
            "time_precision": self.time_precision,
            "group_by_file": self.group_by_file,
            "direction": self.direction.value,
            "first_edge": self.first_edge,
            "last_edge": self.last_edge,
        }
        self._add_mermaid_options(context)
        self._add_mermaid_escape(context)

        return context

    def _add_mermaid_options(self, context: Dict[str, Any]) -> None:
        """Add mermaid options to rendering context."""
        options = {}
        options.update(self.mermaid_options)
        if self.use_elk:
            options.update({"defaultRenderer": "elk"})
        context["mermaid_options"] = options

    def _add_mermaid_escape(self, context: Dict[str, Any]) -> None:
        """Add mermaid escape utility to rendering context."""
        use_elk = context.get("mermaid_options", {}).get("defaultRenderer") == "elk"
        prefix = "&#" if use_elk else "#"

        def mermaid_escape(text: str) -> str:
            for pattern, code in MERMAID_ESCAPE.items():
                text = text.replace(pattern, f"{prefix}{code};")

            return text.strip()

        context["escape_mmd"] = mermaid_escape

    @T.observe("profile")
    def _on_profile_change(self, change: T.Bunch) -> None:
        """Handle a change of profile."""
        if isinstance(change.old, ProfileJSON):
            change.old.unobserve(self.render, "value")
        self.profile.observe(self.render, "value")
        self.render()

    @T.default("children")
    def _default_children(self) -> List[W.Widget]:
        """Provide (and link) the default children."""
        expand = W.ToggleButton(icon="bars", tooltip="hide/show options")

        children = [self.output, self.options, expand]

        T.link((self, "show_options"), (expand, "value"))
        T.link((self, "show_options"), (self.options, "expanded"))

        return children

    @T.default("options")
    def _default_options(self) -> List[W.Widget]:
        """Provide a default options widget."""
        return CallgraphOptions(self)

    @T.default("output")
    def _default_output(self) -> W.Output:
        """Provide a default output widget."""
        return W.Output()

    @T.default("profile")
    def _default_profile(self) -> ProfileJSON:
        """Provide a default profile."""
        return ProfileJSON(value=SPEEDSCOPE_SIMPLE_JSON)

    @T.default("template")
    def _default_template(self) -> str:
        """Provide a default template string."""
        return DEFAULT_MERMAID_TEMPLATE


@W.register
class CallgraphOptions(W.VBox):
    """A minimal UI for callgraph diagram options."""

    parent = T.Instance(Callgraph)
    expanded = T.Bool(default_value=True).tag(sync=True)

    def __init__(self, parent: Callgraph, **kwargs: Any):
        """Create a new UI for callgraph options."""
        kwargs["parent"] = parent
        super().__init__(**kwargs)
        self.children = self._default_children()
        self.add_class(DOMClasses.callgraph_options.value)

    @T.observe("expanded")
    def _on_expanded(self, *_change: Any) -> None:
        self.layout.display = "block" if self.expanded else "none"

    @T.default("children")
    def _default_children(self) -> List[W.Widget]:
        """Show widgets to control rendering options."""
        groups = []
        widgets_by_name = {}
        for group_name, traits in OPTION_GROUPS.items():
            children = []
            child = None
            for trait in traits:
                if trait in CHECKBOX_TRAITS:
                    child = W.Checkbox(description=trait.replace("_", " "))
                    T.link((self.parent, trait), (child, "value"))
                    children += [child]
                elif trait in SELECT_TRAITS:
                    child = W.SelectionSlider(
                        description=trait.replace("_", " "),
                        options=[
                            (e.name.replace("_", " "), e) for e in SELECT_TRAITS[trait]
                        ],
                    )
                    T.link((self.parent, trait), (child, "value"))
                    children += [child]
                elif trait in SLIDER_TRAITS:
                    child = W.IntSlider(
                        description=trait.replace("_", " "), min=-1, max=10000
                    )
                    T.link((self.parent, trait), (child, "value"))
                    children += [child]
                else:  # pragma: no cover
                    continue
                widgets_by_name[trait] = child
            group = W.VBox([W.Label(group_name), *children])
            groups.append(group)

        def _on_change(*_change: Any) -> None:
            for name, disable_fn in TRAIT_DISABLED_IF.items():
                widget = widgets_by_name[name]
                widget.disabled = disable_fn(widgets_by_name)

        self.parent.observe(_on_change)

        return groups
