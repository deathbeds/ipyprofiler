"""Tests of speedscope."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, NoReturn

import pytest

if TYPE_CHECKING:
    from pathlib import Path


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
def test_pyinstrument_flamegraph(
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
    ui = ps.ui()
    assert len(ui.children) == 2
    tabs, bar = ui.children
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


def test_pyinstrument_history(tmp_path: Path) -> NoReturn:
    """Verify history behavior."""
    from ipyprofiler import Pyinstrument

    output_folder = tmp_path / "_pyinstrument"
    ps = Pyinstrument(output_folder=output_folder)
    ui = ps.ui()
    (tabs, meta) = ui.children
    (history,) = meta.children
    assert not output_folder.exists()
    assert meta.layout.display == "none"

    with ps.profile(name="foo"):
        fib(10)

    assert meta.layout.display == "none"
    assert len(ps._history) == 1
    assert_files(output_folder, 1)

    old_profile = ps._profile.value

    with ps.profile(name="bar", filename="bar.json"):
        fib(11)

    assert ps._profile.value != old_profile
    assert meta.layout.display == "flex"
    assert len(ps._history) == 2
    assert_files(output_folder, 2)


def assert_files(path: Path, count: int, glob: str = "*") -> bool:
    """Check for an expected number of files on disk."""
    files = sorted(path.glob(glob))
    assert (
        len(files) == count
    ), f"expected {count} {path}/{glob} files, not {len(files)}"
    return True
