"""Jupyter Widgets for visualizing profiler data."""

from pathlib import Path
from typing import Any, Dict, List

from .constants import __ext__, __ns__, __prefix__, __version__
from .widget_callgraph import Callgraph
from .widget_flamegraph import Flamegraph
from .widget_profile import ProfileJSON
from .widget_pyinstrument import Pyinstrument

__all__ = [
    "_jupyter_labextension_paths",
    "__version__",
    "__js__",
    "Flamegraph",
    "Pyinstrument",
    "Callgraph",
    "ProfileJSON",
]


def _jupyter_labextension_paths(
    prefix: Path = __prefix__, extensions: List[str] = __ext__
) -> List[Dict[str, Any]]:
    return [{"src": str(prefix / e), "dest": f"{__ns__}/{e}"} for e in extensions]
