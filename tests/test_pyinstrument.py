"""Tests of speedscope."""

from __future__ import annotations

import re
from typing import Any, NoReturn

import pytest


def fib(n: int) -> int:
    """Nnaively calculate the nth Fibonacci number with recursion."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


@pytest.mark.parametrize(
    ("init_kwargs", "profile_kwargs", "expect"),
    [
        ({}, {}, r'"name": "untitled"'),
        ({}, {"name": "foobarbaz"}, r'"name": "foobarbaz"'),
        ({"name": None}, {}, r'"name": "CPU profile for'),
        ({}, {"interval": 0.01}, r".*"),
    ],
)
def test_pyinstrument_flamgegraph(
    init_kwargs: dict[str, Any], profile_kwargs: dict[str, Any], expect: str
) -> NoReturn:
    """Verify some flamgraph outputs."""
    from ipyprofiler import Pyinstrument

    ps = Pyinstrument(**init_kwargs)

    old_profile = ps.flamegraph.profile.value

    with ps.profile(**profile_kwargs):
        fib(10)

    new_profile = ps.flamegraph.profile.value
    assert old_profile != new_profile
    print("new_profile")
    print(new_profile)
    assert re.findall(expect, new_profile), f"pattern not found: '{expect}' "


@pytest.mark.parametrize(
    ("init_kwargs", "profile_kwargs", "expect"),
    [
        ({}, {"interval": 0.0001, "use_elk": True}, r'"elk"'),
    ],
)
def test_pyinstrument_callgraph(
    init_kwargs: dict[str, Any],
    profile_kwargs: dict[str, Any],
    expect: str,
) -> NoReturn:
    """Verify some mermaid outputs."""
    from ipyprofiler import Pyinstrument

    ps = Pyinstrument(**init_kwargs)
    tabs = ps.tabs()
    assert len(tabs.children) == 2

    old_mmd = ps.callgraph._mermaid()
    old_profile = ps.callgraph.profile.value

    with ps.profile(**profile_kwargs):
        fib(10)

    new_mmd = ps.callgraph._mermaid()
    new_profile = ps.callgraph.profile.value
    assert old_mmd != new_mmd
    assert old_profile != new_profile
    print("new profile")
    print(new_profile)
    print("new mermaid")
    print(new_mmd)
    assert re.findall(expect, new_mmd), f"pattern not found: '{expect}' "
