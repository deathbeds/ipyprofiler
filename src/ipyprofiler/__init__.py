"""Jupyter Widgets for visualizing profiler data."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from .constants import __ext__, __ns__, __prefix__, __version__
from .widget_callgraph import Callgraph
from .widget_flamegraph import Flamegraph
from .widget_profile import ProfileJSON
from .widget_pyinstrument import Pyinstrument

if TYPE_CHECKING:
    from pathlib import Path

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
    prefix: Path = __prefix__,
    extensions: List[str] = __ext__,
) -> List[Dict[str, Any]]:
    """Provide the mapping of labextensions at rest to their canonical location."""
    return [{"src": str(prefix / e), "dest": f"{__ns__}/{e}"} for e in extensions]
