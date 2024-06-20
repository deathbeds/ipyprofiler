"""Profile visualizer widgets."""

from __future__ import annotations

from typing import Dict

import ipywidgets as W
import traitlets as T

from .base import IPyProfilerBase
from .constants import SPEEDSCOPE_HELP_MARKDOWN, SPEEDSCOPE_SIMPLE_JSON
from .widget_profile import ProfileJSON


@W.register
class Flamegraph(IPyProfilerBase, W.Box):
    """Display a speedscope profile."""

    profile: ProfileJSON = T.Instance(ProfileJSON, allow_none=True).tag(
        sync=True, **W.widget_serialization
    )
    view: str = T.Unicode("time-ordered").tag(sync=True)

    _model_name: str = T.Unicode("FlamegraphModel").tag(sync=True)
    _view_name: str = T.Unicode("FlamegraphView").tag(sync=True)

    @T.default("profile")
    def _default_profile(self) -> ProfileJSON:
        """Provide a reasonable speedscope file."""
        return ProfileJSON(value=SPEEDSCOPE_SIMPLE_JSON)

    @T.default("layout")
    def _default_layout(self) -> Dict[str, str]:
        """Provide a reasonable minimum height."""
        return {"min_height": "60vh", "height": "100%", "flex": "1"}

    def help(self) -> W.Output:
        """Display help for a speedscope widget."""
        from IPython.display import Markdown, display

        out = W.Output()
        with out:
            display(Markdown(SPEEDSCOPE_HELP_MARKDOWN))
        return out
