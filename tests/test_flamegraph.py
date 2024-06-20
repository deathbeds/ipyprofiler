"""Tests of speedscope."""

from typing import NoReturn

from ipywidgets import Output


def test_flamegraph_defaults() -> NoReturn:
    """Verify some invariants in the speedscope defaults."""
    from ipyprofiler import Flamegraph

    s = Flamegraph()
    assert s.profile.value, "a speedscope should have a default profile"
    assert s.layout.min_height, "a speedscope should have a minimum height"
    assert isinstance(s.help(), Output)
