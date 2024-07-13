"""Test configuration for ``ipyprofiler``."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    import nbconvert

HERE = Path(__file__).parent
ROOT = HERE.parent
EXAMPLES = ROOT / "examples/files"
NOTEBOOKS = [
    p.relative_to(EXAMPLES)
    for p in EXAMPLES.rglob("*.ipynb")
    if "ipynb_checkpoints" not in str(p)
]


@pytest.fixture(params=[n.name for n in NOTEBOOKS])
def a_notebook(request: pytest.FixtureRequest) -> Path:
    """Provide a notebook."""
    return EXAMPLES / f"{request.param}"


@pytest.fixture()
def a_notebook_exporter() -> Generator[nbconvert.NotebookExporter, None, None]:
    """Provide an executing notebook exporter."""
    env_patch = {
        "JUPYTER_PLATFORM_DIRS": "1",
    }
    old_values = {os.environ[k]: v for k, v in env_patch.items() if k in os.environ}
    os.environ.update(env_patch)
    from nbconvert import NotebookExporter
    from nbconvert.preprocessors import ExecutePreprocessor

    nbe = NotebookExporter()
    nbe.preprocessors += [ExecutePreprocessor(timeout=600, kernel_name="python3")]
    yield nbe
    [os.environ.pop(k) for k in env_patch]
    os.environ.update(old_values)
