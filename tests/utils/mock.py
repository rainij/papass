from collections.abc import Callable, Iterable, Iterator
from typing import Any


def patch_input(monkeypatch, rolls: Iterable[Iterable[int]]) -> None:
    """Patch the builtin ``input``."""
    patched_input = _make_patched_input(rolls)
    monkeypatch.setattr("builtins.input", patched_input)


def _make_patched_input(rolls: Iterable[Iterable[int]]) -> Callable[[Any], str]:
    """Make a patched version of the builtin ``input``."""

    def make_iterator() -> Iterator[str]:
        for r in rolls:
            yield " ".join(map(str, r))

        raise AssertionError("Unexpectedly many requests to roll.")

    iterator = make_iterator()
    return lambda _: next(iterator)
