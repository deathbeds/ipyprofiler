"""Render a profile as directed graph."""

from __future__ import annotations

from typing import Any, Dict, List

import ipywidgets as W
import jinja2
import traitlets as T

from .constants import SPEEDSCOPE_SIMPLE_JSON, DOMClasses, MermaidDirection
from .widget_profile import ProfileJSON

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

DEFAULT_MERMAID_TEMPLATE = """
%%{init: {"flowchart": {{ mermaid_options | tojson }}} }%%

flowchart {{ direction }}

{% for node in nodes -%}
    {{ node.id }}([{{ escape_mmd(node.name) }}])
{% endfor -%}

{%- for edge in edges %}
{{ edge.source }} -->
{%- if show_time %} {{ edge.id }}>{{ edge.time }}] --> {% endif -%}
{{ edge.target }}
{%- endfor -%}

{% if group_by_file %}
{% for group in groups %}
subgraph {{ group.id }} [{{ escape_mmd(group.file or "???") }}]
    {% for node_id in group.nodes %}
    {{ node_id }}
    {% endfor -%}
end
{% endfor %}
{% endif %}
"""

CHECKBOX_TRAITS = ["show_time", "group_by_file", "use_elk"]
SELECT_TRAITS = {"direction": MermaidDirection}
RENDER_ON_TRAITS = [*CHECKBOX_TRAITS, *SELECT_TRAITS, "template"]


@W.register
class Callgraph(W.VBox):
    """Display a call graph from a profile."""

    profile = T.Instance(ProfileJSON)
    output = T.Instance(W.Output)
    options = T.Instance("ipyprofiler.widget_callgraph.CallgraphOptions")

    show_time = T.Bool(default_value=False, help="whether to show times on edges").tag(
        sync=True
    )
    template = T.Unicode().tag(sync=True)
    mermaid_options = T.Dict().tag(sync=True)
    use_elk = T.Bool(default_value=False).tag(sync=True)
    group_by_file = T.Bool(default_value=False).tag(sync=True)
    direction: MermaidDirection = T.UseEnum(MermaidDirection)

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
            "group_by_file": self.group_by_file,
            "direction": self.direction.value,
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
        return [self.options, self.output]

    @T.default("options")
    def _default_options(self) -> List[W.Widget]:
        return CallgraphOptions(self)

    @T.default("output")
    def _default_output(self) -> W.Output:
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
class CallgraphOptions(W.HBox):
    """A minimal UI for callgraph diagram options."""

    parent = T.Instance(Callgraph)

    def __init__(self, parent: Callgraph, **kwargs: Any):
        """Create a new UI for callgraph options."""
        kwargs["parent"] = parent
        super().__init__(**kwargs)
        self.children = self._default_children()
        self.add_class(DOMClasses.callgraph_options.value)

    @T.default("children")
    def _default_children(self) -> List[W.Widget]:
        """Show widgets to control rendering options."""
        children = []
        for trait in CHECKBOX_TRAITS:
            child = W.Checkbox(description=trait.replace("_", " "))
            T.link((self.parent, trait), (child, "value"))
            children += [child]
        for trait, enum in SELECT_TRAITS.items():
            child = W.SelectionSlider(
                description=trait.replace("_", " "),
                options=[(e.name.replace("_", " "), e) for e in enum],
            )
            T.link((self.parent, trait), (child, "value"))
            children += [child]
        return children
