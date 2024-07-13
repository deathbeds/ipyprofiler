"""Verify notebook behaviors."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    import nbconvert
    import nbformat


def test_a_notebook(
    a_notebook: nbformat.NotebookNode, a_notebook_exporter: nbconvert.NotebookExporter
) -> NoReturn:
    """Verify notebooks run without error."""
    (body, resources) = a_notebook_exporter.from_filename(str(a_notebook))

    assert '"output_type": "error"' not in body
