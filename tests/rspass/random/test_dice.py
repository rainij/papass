from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from typing import Any

import pytest
from rspass.random import DiceRng


# TODO: move this into rspass and test it
def digits_to_value(base: int, digits: Iterable[int]):
    assert 1 < base
    assert all(0 <= d < base for d in digits)
    return reduce(lambda acc, r: base * acc + r, digits, 0)


def rolls_to_value(num_sides: int, rolls: Iterable[int]):
    digits = [r - 1 for r in rolls]
    return digits_to_value(num_sides, digits)


def make_patched_input(rolls: Iterable[Iterable[int]]) -> Callable[[Any], str]:
    def make_iterator() -> Iterator[str]:
        for r in rolls:
            yield " ".join(map(str, r))

        raise AssertionError("Unexpectedly many requests to roll.")

    iterator = make_iterator()
    return lambda _: next(iterator)


@pytest.mark.parametrize(
    "num_sides,upper,rolls",
    [
        # upper being a power of num_sides:
        (
            6,
            6**2,
            [[1, 1]],
        ),
        (
            6,
            6,
            [[4]],
        ),
        (
            8,
            8**6,
            [[1, 2, 3, 4, 5, 6]],
        ),
        (
            20,
            20**3,
            [[17, 3, 13]],
        ),
        # upper being no power of num_sides:
        (
            6,
            6**2 - 5,
            [[6, 6], [2, 3]],
        ),
    ],
)
def test_randbelow(monkeypatch, num_sides, upper, rolls):
    patched_input = make_patched_input(rolls)
    monkeypatch.setattr("builtins.input", patched_input)

    # Only the last roll should be used (others were rejected).
    expected = rolls_to_value(num_sides, rolls[-1]) % upper

    rng = DiceRng(num_sides=num_sides)
    assert rng.randbelow(upper) == expected
