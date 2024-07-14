"""documentation for ``ipyprofiler``."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from sphinx.application import Sphinx

RTD = "READTHEDOCS"
CONF_PY = Path(__file__)
HERE = CONF_PY.parent
ROOT = HERE.parent
PYPROJ = ROOT / "pyproject.toml"
PIXI = ROOT / "pixi.toml"
REPORTS = ROOT / "build/reports"

if os.getenv(RTD) == "True":
    # provide a fake root doc
    root_doc = "rtd"

    def setup(app: Sphinx) -> None:
        """Customize the sphinx build lifecycle."""

        def _run_pixi(*_args: Any) -> None:
            args = ["pixi", "run", "-e", "rtd", "-v", "rtd"]
            env = {k: v for k, v in os.environ.items() if k != RTD}
            subprocess.check_call(args, env=env, cwd=str(ROOT))  # noqa: S603

        app.connect("build-finished", _run_pixi)
else:
    import tomllib
    from jinja2 import Template

    __import__("ipyprofiler")
    _intersphinx_mapping: Dict[str, tuple[str, None]] = {}

    PPT_DATA: dict[str, Any] = tomllib.loads(PYPROJ.read_text(encoding="utf-8"))
    PT_DATA: dict[str, Any] = tomllib.loads(PIXI.read_text(encoding="utf-8"))

    locals().update(
        json.loads(
            Template(json.dumps(PT_DATA["tool"]["sphinx"], indent=2)).render(
                ppt=PPT_DATA,
                pt=PT_DATA
            )
        )
    )

    intersphinx_mapping = {k: (v, None) for k, v in _intersphinx_mapping.items()}
    REPORTS.mkdir(parents=True, exist_ok=True)


# RTD will inject more config below here
