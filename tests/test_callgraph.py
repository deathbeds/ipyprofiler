"""Tests of ``Callgraph``."""

from typing import NoReturn


def test_callgraph_defaults() -> NoReturn:
    """Verify some invariants in the callgraph defaults."""
    from ipyprofiler import Callgraph
    from ipyprofiler.widget_callgraph import ProfileJSON

    cg = Callgraph()
    assert cg.profile.value
    cg.profile = ProfileJSON(value="{}")
    cg.profile = ProfileJSON(value="""{"foo": "bar"}""")
    options = cg.show_options()
    assert len(options.children) == 4
