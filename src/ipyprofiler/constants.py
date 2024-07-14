"""Constants for ``ipyprofiler``."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path

__all__ = ["__version__", "__ns__", "__ext__", "__prefix__"]
__version__ = "0.1.0"
__ns__ = "@deathbeds"
__ext__ = ["jupyter-profiler"]

HERE = Path(__file__).parent
FRAG = f"share/jupyter/labextensions/{__ns__}"
IN_TREE = (HERE / "../_d").resolve() / FRAG
IN_PREFIX = Path(sys.prefix) / FRAG

__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX


class AsyncMode(Enum):
    """Allowed values for ``pyinstrument``'s ``async_mode``."""

    enabled = "enabled"
    disabled = "disabled"
    strict = "strict"


class MermaidDirection(Enum):
    """Allowed values for mermaid graph directions."""

    top_to_bottom = "TB"
    bottom_to_top = "BT"
    right_to_left = "RL"
    left_to_right = "LR"


class DOMClasses(Enum):
    """Classes added to widgets from the python side."""

    pyinstrument_tab = "jprf-Pyinstrument-Tab"
    callgraph = "jprf-Callgraph"
    callgraph_options = "jprf-Callgraph-Options"


SPEEDSCOPE_SIMPLE_JSON = """
{
  "$schema": "https://www.speedscope.app/file-format-schema.json",
  "version": "0.0.1",
  "shared": {
    "frames": [
      {"name": "a"},
      {"name": "b"},
      {"name": "c"},
      {"name": "d"}
    ]
  },
  "profiles": [
    {
      "endValue": 14,
      "events": [
        {"at": 0, "frame": 0, "type": "O"},
        {"at": 0, "frame": 1, "type": "O"},
        {"at": 0, "frame": 2, "type": "O"},
        {"at": 2, "frame": 2, "type": "C"},
        {"at": 2, "frame": 3, "type": "O"},
        {"at": 6, "frame": 3, "type": "C"},
        {"at": 6, "frame": 2, "type": "O"},
        {"at": 9, "frame": 2, "type": "C"},
        {"at": 14, "frame": 1, "type": "C"},
        {"at": 14, "frame": 0, "type": "C"}
      ],
      "name": "simple.txt",
      "startValue": 0, "type": "evented",
      "unit": "none"
    }
  ]
}
"""

SPEEDSCOPE_HELP_MARKDOWN = """
_Excerpt from the `speedscope` [README]._

[README]: https://github.com/jlfwong/speedscope/blob/v1.20.0/README.md#navigation

> ### Navigation
>
> Once a profile has loaded, the main view is split into two: the top area is the
> "minimap", and the bottom area is the "stack view".
>
> ### Minimap Navigation
>
> * Scroll on either axis to pan around
> * Click and drag to narrow your view to a specific range
>
> ### Stack View Navigation
>
> * Scroll on either axis to pan around
> * Pinch to zoom
> * Hold Cmd+Scroll to zoom
> * Double click on a frame to fit the viewport to it
> * Click on a frame to view summary statistics about it
>
> ### Keyboard Navigation
>
> * `+`: zoom in
> * `-`: zoom out
> * `0`: zoom out to see the entire profile
> * `w`/`a`/`s`/`d` or arrow keys: pan around the profile
> * `1`: Switch to the "Time Order" view
> * `2`: Switch to the "Left Heavy" view
> * `3`: Switch to the "Sandwich" view
> * `r`: Collapse recursion in the flamegraphs
> * `Cmd+S`/`Ctrl+S` to save the current profile
> * `Cmd+O`/`Ctrl+O` to open a new profile
> * `n`: Go to next profile/thread if one is available
> * `p`: Go to previous profile/thread if one is available
> * `t`: Open the profile/thread selector if available
> * `Cmd+F`/`Ctrl+F`: to open search. While open, `Enter` and `Shift+Enter` cycle
>    through results
"""
