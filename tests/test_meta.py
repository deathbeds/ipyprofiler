"""Tests of basic metadata."""

from typing import NoReturn


def test_version() -> NoReturn:
    """Verify the ``ipyprofiler`` version."""
    import ipyprofiler

    assert ipyprofiler.__version__


def test_extensions() -> NoReturn:
    """Verify the ``ipyprofiler`` labextensions."""
    import ipyprofiler

    exts = ipyprofiler._jupyter_labextension_paths()
    assert len(exts) == 1
