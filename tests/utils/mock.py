from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Any

from papass.random.dice import QueryForDice


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


class MockQueryForDice(ABC, QueryForDice):
    def __init__(self):
        self._num_rejections = 0

    @abstractmethod
    def __call__(self, *, num_sides: int, required_num_rolls: int) -> list[int]: ...

    def notify_rejection(self) -> None:
        self._num_rejections += 1

    @property
    def num_rejections(self) -> int:
        """Counts how often ``notify_rejection`` was called."""
        return self._num_rejections


class MockIterQueryForDice(MockQueryForDice):
    def __init__(self, rolls: Iterable[Sequence[int]]):
        super().__init__()
        self._rolls: Iterator[Sequence[int]] = iter(rolls)

    def __call__(self, *, num_sides: int, required_num_rolls: int) -> list[int]:
        result = list(next(self._rolls))
        assert (
            len(result) == required_num_rolls
        ), f"Incorrect number of rolls. Require {required_num_rolls}, got {result}."
        assert all(
            1 <= r <= num_sides for r in result
        ), f"Invalid rolls for num_sides={num_sides}: {result}"
        return result


class MockCallbackQueryForDice(MockQueryForDice):
    def __init__(self, rolls_callback: Callable[[int], Sequence[int]]):
        super().__init__()
        self._rolls_callback = rolls_callback

    def __call__(self, *, num_sides: int, required_num_rolls: int) -> list[int]:
        result = self._rolls_callback(required_num_rolls)
        assert (
            len(result) == required_num_rolls
        ), f"Incorrect number of rolls. Require {required_num_rolls}."
        assert all(
            1 <= r <= num_sides for r in result
        ), f"Invalid rolls for num_sides={num_sides}: {result}"
        return list(result)
