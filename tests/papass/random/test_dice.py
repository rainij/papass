from collections.abc import Callable, Iterable, Iterator
from typing import Any

import pytest
from papass.random.dice import DiceRng
from papass.utils import rolls_to_value


def make_patched_input(rolls: Iterable[Iterable[int]]) -> Callable[[Any], str]:
    """Make a patched version of the builtin `input`."""

    def make_iterator() -> Iterator[str]:
        for r in rolls:
            yield " ".join(map(str, r))

        raise AssertionError("Unexpectedly many requests to roll.")

    iterator = make_iterator()
    return lambda _: next(iterator)


@pytest.mark.parametrize(
    "num_sides,upper,rolls",
    [
        # `upper` is a power of `num_sides`:
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
        # `upper` no power of `num_sides`:
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

    # Only the last roll should be used (others are rejected).
    expected = rolls_to_value(num_sides, rolls[-1]) % upper

    rng = DiceRng(num_sides=num_sides)
    assert rng.randbelow(upper) == expected
