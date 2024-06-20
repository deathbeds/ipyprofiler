"""Widgets for describing profiles."""

from __future__ import annotations

import json
import re
import site
from pathlib import Path
from typing import Any, Dict

import ipywidgets as W
import traitlets as T

from .base import IPyProfilerBase


@W.register
class ProfileJSON(IPyProfilerBase):
    """A widget containing speedscope-compatible JSON."""

    value = T.Unicode(allow_none=True).tag(sync=True)
    json_rewrites: dict[str, Any] = T.Dict(
        help="regular expressions to replace in raw JSON"
    )

    _model_name: str = T.Unicode("ProfileJSONModel").tag(sync=True)
    _view_name: str = T.Unicode("ProfileJSONView").tag(sync=True)

    def to_callgraph(self) -> Dict[str, Any]:
        """Generate a callgraph from a speedscope profile."""
        fp = json.loads(self.value)
        nodes = []
        groups = {}
        edges = []
        if "profiles" in fp:
            fp0 = fp["profiles"][0]

            for i, frame in enumerate(fp["shared"]["frames"]):
                nodes += [{"id": f"n-{i}", **frame}]
                frame_file = frame.get("file")
                if frame_file is not None:
                    if frame_file not in groups:
                        groups[frame_file] = {
                            "id": f"g-{len(groups)}",
                            "file": frame_file,
                            "nodes": [],
                        }
                    groups[frame_file]["nodes"].append(f"n-{i}")

            stack = []
            observed = []
            for e in fp0["events"]:
                if e["type"] == "O":
                    edge = {
                        "opened": e,
                        "closed": None,
                        "parent": stack[0] if stack else None,
                    }
                    observed += [edge]
                    stack.insert(0, edge)
                elif e["type"] == "C":  # pragma: no cover
                    stack[0]["closed"] = e
                    stack.remove(stack[0])

            for o in observed:
                parent = o["parent"]
                if parent is None:
                    continue
                opened = o["opened"]
                closed = o["closed"]
                edge = {
                    "id": f"e-{len(edges)}",
                    "source": f"""n-{parent["opened"]["frame"]}""",
                    "target": f"""n-{closed["frame"]}""",
                    "time": closed["at"] - opened["at"],
                }
                edges += [edge]
        return {"nodes": nodes, "edges": edges, "groups": [*groups.values()]}

    def rewrite_speedscope_json(self, raw: str, name: str | None = None) -> str:
        """Replace strings in JSON."""
        for pattern, replacement in self.json_rewrites.items():
            raw = re.sub(pattern, replacement, raw)
        if name is not None:
            profile_data = json.loads(raw)
            profile_data["name"] = name
            for profile in profile_data["profiles"]:
                profile["name"] = name
            raw = json.dumps(profile_data, indent=2, sort_keys=True)
        return raw

    @T.default("json_rewrites")
    def _default_json_rewrites(self) -> Dict[str, str]:
        """Provide default rewrite patterns for profile JSON."""
        return {
            str(Path.cwd()): ".",
            r'"[^"]+?ipykernel_[\d]+.[\d]+\.py"': '"__main__"',
            site.getsitepackages()[0]: "",
            str(Path(site.getsitepackages()[0]).parent): "",
            r"ipython-input-\d+-\d+": "__main__",
        }
