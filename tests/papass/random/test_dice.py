from collections.abc import Callable, Iterable, Iterator
from typing import Any

import pytest
from papass.random.dice import DiceFrame, DiceRng, compute_dice_frame
from papass.utils import rolls_to_value


def make_patched_input(rolls: Iterable[Iterable[int]]) -> Callable[[Any], str]:
    """Make a patched version of the builtin `input`."""

    def make_iterator() -> Iterator[str]:
        for r in rolls:
            yield " ".join(map(str, r))

        raise AssertionError("Unexpectedly many requests to roll.")

    iterator = make_iterator()
    return lambda _: next(iterator)


def patch_input(monkeypatch, rolls: Iterable[Iterable[int]]):
    patched_input = make_patched_input(rolls)
    monkeypatch.setattr("builtins.input", patched_input)


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
            6,
            6**3,
            [[6, 6, 6]],
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
            [[6, 6, 6, 6, 6], [2, 3, 2, 3, 1]],
        ),
    ],
)
def test_randbelow(monkeypatch, num_sides, upper, rolls):
    patch_input(monkeypatch, rolls)

    # Only the last roll should be used (others are rejected).
    expected = rolls_to_value(num_sides, rolls[-1]) % upper

    rng = DiceRng(num_sides=num_sides, required_success_probability=0.99)
    assert rng.randbelow(upper) == expected


@pytest.mark.parametrize(
    "upper, req_prob, expected",
    [
        (
            10,
            0.999,
            DiceFrame(
                upper_multiple=10,
                required_num_rolls=1,
            ),
        ),
        (
            5,
            0.999,
            DiceFrame(
                upper_multiple=10,
                required_num_rolls=1,
            ),
        ),
        (
            4,
            0.999,
            DiceFrame(
                upper_multiple=100,
                required_num_rolls=2,
            ),
        ),
        (
            20,
            0.999,
            DiceFrame(
                upper_multiple=100,
                required_num_rolls=2,
            ),
        ),
        (
            3,
            0.8,
            DiceFrame(
                upper_multiple=9,
                required_num_rolls=1,
            ),
        ),
        (
            3,
            0.95,
            DiceFrame(
                upper_multiple=99,
                required_num_rolls=2,
            ),
        ),
        (
            3,
            0.998,
            DiceFrame(
                upper_multiple=999,
                required_num_rolls=3,
            ),
        ),
        (
            17,
            0.8,
            DiceFrame(
                upper_multiple=85,
                required_num_rolls=2,
            ),
        ),
        (
            17,
            0.98,
            DiceFrame(
                upper_multiple=986,
                required_num_rolls=3,
            ),
        ),
        (
            17,
            0.9995,
            DiceFrame(
                upper_multiple=9996,
                required_num_rolls=4,
            ),
        ),
    ],
)
def test_compute_frame(upper, req_prob, expected):
    result = compute_dice_frame(
        num_sides=10, upper=upper, required_success_probability=req_prob
    )
    assert result == expected
