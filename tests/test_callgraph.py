"""Tests of ``Callgraph``."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from ipyprofiler import Callgraph

import pytest


@pytest.fixture()
def a_callgraph() -> Callgraph:
    """Provide a callgraph."""
    from ipyprofiler import Callgraph

    return Callgraph()


def test_callgraph_defaults(a_callgraph: Callgraph) -> NoReturn:
    """Verify some invariants in the callgraph defaults."""
    from ipyprofiler.widget_callgraph import ProfileJSON

    cg = a_callgraph
    assert cg.profile.value
    cg.profile = ProfileJSON(value="{}")
    cg.profile = ProfileJSON(value="""{"foo": "bar"}""")
    assert len(cg.options.children) == 3


def test_callgraph_show_options(a_callgraph: Callgraph) -> NoReturn:
    """Verify the linkage of a callgraph."""
    cg = a_callgraph
    assert not cg.show_options
    assert not cg.options.expanded
    cg.show_options = True
    assert cg.options.expanded
    cg.show_options = False
    assert not cg.options.expanded
