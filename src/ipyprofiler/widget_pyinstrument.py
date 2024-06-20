"""Convenience wrapper widget for ``pyinstrument``."""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, NoReturn

import ipywidgets as W
import traitlets as T

from .constants import SPEEDSCOPE_SIMPLE_JSON, AsyncMode
from .widget_callgraph import Callgraph
from .widget_flamegraph import Flamegraph
from .widget_profile import ProfileJSON

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyinstrument import Profiler
    from pyinstrument.renderers import SpeedscopeRenderer


@W.register
class Pyinstrument(W.Widget):
    """Display a speedscope profile."""

    flamegraph: Flamegraph = T.Instance(Flamegraph, help="a flamegraph visualizer")
    callgraph: Callgraph = T.Instance(Callgraph, help="a callgraph visualizer")
    _profile: ProfileJSON = T.Instance(ProfileJSON, help="a shared profile")

    interval: float = T.Float(0.001, help="the sampling interval in seconds")
    async_mode: AsyncMode = T.UseEnum(AsyncMode, help="behavior with async code")
    name: str | None = T.Unicode("untitled", help="name to display", allow_none=True)
    processor_options: Dict[str, Any] = T.Dict(
        help="additional options to pass to post-processors"
    )
    profiling: bool = T.Bool(default_value=False)

    _profiler: Profiler = T.Instance("pyinstrument.Profiler")
    _flamegraph_renderer: SpeedscopeRenderer = T.Instance(
        "pyinstrument.renderers.SpeedscopeRenderer"
    )

    def tabs(self, **kwargs: Any) -> W.Tab:
        """Provide a tab-based UI."""
        kwargs.update(
            children=[self.flamegraph, self.callgraph],
            titles=["🔥 flame graph", "📞 call graph"],
        )
        tab = W.Tab(**kwargs)
        tab.add_class("jprf-Pyinstrument-Tab")
        return tab

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
    ) -> Generator[None, Any, None]:
        """Profile some Python code and update the speedscope display."""
        self.interval = interval if interval is not None else self.interval
        self.async_mode = async_mode if interval is not None else self.async_mode
        self.name = name if name is not None else self.name
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
        else:
            self._speedscope_renderer = self._default_speedscope_renderer()
            self._profile.value = self._profile.rewrite_speedscope_json(
                self._profiler.output(self._speedscope_renderer), name=self.name
            )
            self.callgraph.render()

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
