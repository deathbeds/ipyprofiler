"""Convenience wrapper widget for ``pyinstrument``."""

from __future__ import annotations

import re
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, NoReturn

import ipywidgets as W
import jinja2
import traitlets as T

from .constants import SPEEDSCOPE_SIMPLE_JSON, UTF8, AsyncMode, DOMClasses
from .widget_callgraph import Callgraph
from .widget_flamegraph import Flamegraph
from .widget_profile import ProfileJSON

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyinstrument import Profiler
    from pyinstrument.renderers import SpeedscopeRenderer


@dataclass
class HistoryItem:
    """Lightweight history for files."""

    name: str
    value: str
    path: Path


@W.register
class Pyinstrument(W.Widget):
    """Display a speedscope profile."""

    flamegraph: Flamegraph = T.Instance(Flamegraph, help="a flamegraph visualizer")
    callgraph: Callgraph = T.Instance(Callgraph, help="a callgraph visualizer")
    _profile: ProfileJSON = T.Instance(ProfileJSON, help="a shared profile")

    interval: float = T.Float(0.001, help="the sampling interval in seconds")
    async_mode: AsyncMode = T.UseEnum(AsyncMode, help="behavior with async code")
    name: str | None = T.Unicode("untitled", help="name to display", allow_none=True)
    output_folder: Path | None = T.Instance(Path, allow_none=True)
    output_template: str = T.Unicode("{{ now_ts }}-{{ name }}.json")
    filename: str | None = T.Unicode(allow_none=True)
    processor_options: Dict[str, Any] = T.Dict(
        help="additional options to pass to post-processors"
    )
    profiling: bool = T.Bool(default_value=False)

    _profiler: Profiler = T.Instance("pyinstrument.Profiler")
    _flamegraph_renderer: SpeedscopeRenderer = T.Instance(
        "pyinstrument.renderers.SpeedscopeRenderer"
    )
    _history: tuple[HistoryItem, ...] = T.Tuple()

    def ui(self, **kwargs: Any) -> W.VBox:
        """Provide a tab-based UI."""
        tab = W.Tab(
            children=[self.flamegraph, self.callgraph],
            titles=["🔥 flame graph", "📞 call graph"],
            layout={"flex": "1"},
        )
        meta = W.HBox(
            [self.history()],
            layout={"flex": "0", "min_height": "2.5em", "overflow": "hidden"},
        )

        kwargs["children"] = [tab, meta]

        box = W.VBox(**kwargs)
        box.add_class(DOMClasses.pyinstrument.value)
        T.dlink(
            (self, "_history"),
            (meta.layout, "display"),
            lambda h: "flex" if len(h) > 1 else "none",
        )
        return box

    def history(self) -> W.Select:
        """Build and link a history navigator."""
        dropdown = W.Select(description="profiles", rows=1)

        T.dlink(
            (self, "_history"),
            (dropdown, "options"),
            lambda h: {hi.name: hi for hi in h},
        )
        T.dlink(
            (dropdown, "value"),
            (self._profile, "value"),
            lambda hi: self._profile.value if hi is None else hi.value,
        )

        return dropdown

    @contextmanager
    def profile(  # noqa: PLR0913
        self,
        name: str | None = None,
        interval: float | None = None,
        async_mode: AsyncMode | None = None,
        processor_options: Dict[str, Any] | None = None,
        mermaid_options: Dict[str, Any] | None = None,
        use_elk: bool | None = None,
        group_by_file: bool | None = None,
        filename: str | None = None,
    ) -> Generator[None, Any, None]:
        """Profile some Python code and update the speedscope display."""
        self.interval = interval if interval is not None else self.interval
        self.async_mode = async_mode if interval is not None else self.async_mode
        self.name = name if name is not None else self.name
        self.filename = filename if filename else self.filename
        self.callgraph.mermaid_options = (
            mermaid_options
            if mermaid_options is not None
            else self.callgraph.mermaid_options
        )
        self.callgraph.use_elk = (
            use_elk if use_elk is not None else self.callgraph.use_elk
        )
        self.callgraph.group_by_file = (
            group_by_file if group_by_file is not None else self.callgraph.group_by_file
        )
        self.processor_options = (
            processor_options
            if self.processor_options is None
            else self.processor_options
        )

        self.profiling = False
        try:
            self.profiling = True
            yield
        finally:
            self.profiling = False

    @T.observe("profiling")
    def _on_profiling(self, *_: Any) -> NoReturn:
        """Handle a change to ``profiling``."""
        if self._profiler.is_running:
            self._profiler.stop()

        if self.profiling:
            self._profiler = self._default_profiler()
            self._profiler.start()
            return

        self._speedscope_renderer = self._default_speedscope_renderer()
        new_json = self._profiler.output(self._speedscope_renderer)
        new_json = self._profile.rewrite_speedscope_json(new_json, name=self.name)

        if self.output_folder is not None:
            self.archive(new_json)
        self._profile.value = new_json
        self.callgraph.render()

    def archive(self, new_json: str) -> None:
        """Write out the file."""
        filename = self.filename
        if not filename:
            tmpl = jinja2.Template(self.output_template)
            now_ts = round(datetime.timestamp(datetime.now(tz=timezone.utc)), 2)
            filename = tmpl.render(now_ts=now_ts, name=self.name)
        filename = re.sub(r"[^a-z_\d\.\-]+", "_", filename, flags=re.IGNORECASE)
        path = self.output_folder / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_json, **UTF8)
        self._history += (HistoryItem(path=path, name=self.name, value=new_json),)

    @T.default("_profiler")
    def _default_profiler(self) -> Profiler:
        """Provide a default profiler."""
        from pyinstrument import Profiler

        return Profiler(
            interval=self.interval,
            async_mode=self.async_mode,
        )

    @T.default("_speedscope_renderer")
    def _default_speedscope_renderer(self) -> SpeedscopeRenderer:
        """Provide a speedscope renderer."""
        from pyinstrument.renderers import SpeedscopeRenderer

        return SpeedscopeRenderer(processor_options=self.processor_options)

    @T.default("_profile")
    def _default_profile(self) -> ProfileJSON:
        return ProfileJSON(value=SPEEDSCOPE_SIMPLE_JSON)

    @T.default("flamegraph")
    def _default_speedscope(self) -> Flamegraph:
        """Provide a default ``Flamegraph``."""
        return Flamegraph(profile=self._profile)

    @T.default("callgraph")
    def _default_callgraph(self) -> Callgraph:
        """Provide a default ``Callgraph``."""
        return Callgraph(profile=self._profile)

    @T.default("processor_options")
    def _default_processor_options(self) -> Dict[str, Any]:
        """Provide default profile postprocessor options."""
        return {}
