import pytest
from papass.utils import digits_to_value, rolls_to_value, value_to_digits


@pytest.mark.parametrize(
    "base, digits, expected",
    [
        (10, [9, 2, 3], 923),
        (2, [0, 1, 1], 3),
        (7, [3, 1, 6], 3 * 49 + 1 * 7 + 6 * 1),
    ],
)
def test_digits_to_value(base, digits, expected):
    assert expected == digits_to_value(base, digits)


@pytest.mark.parametrize(
    "num_sides, rolls",
    [
        (6, [5, 1, 3, 6]),
        (10, [10, 1, 8]),
        (20, [20, 19, 3, 1, 17]),
    ],
)
def test_rolls_to_value(num_sides, rolls):
    expected = digits_to_value(num_sides, [r - 1 for r in rolls])
    assert expected == rolls_to_value(num_sides, rolls)


@pytest.mark.parametrize(
    "value, base, length, expected",
    [
        (123, 10, 4, [0, 1, 2, 3]),
        (3*6 + 4, 6, 2, [3, 4]),
    ],
)
def test_value_to_digits(value, base, length, expected):
    assert expected == value_to_digits(value, base=base, length=length)


class TestQueryUserForDice:
    def test_valid(self):
        pass
