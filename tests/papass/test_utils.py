import pytest
from papass.utils import (
    QueryUserForDice,
    digits_to_value,
    rolls_to_value,
    value_to_digits,
)
from tests.utils.mock import patch_input


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
    @pytest.mark.parametrize("user_input, expected", [
        (["1 2 3"], [1, 2, 3]),
        (["1", "4 3"], [1, 4, 3]),
        (["6", "2", "6"], [6, 2, 6]),
        (["", "5 5 4"], [5, 5, 4]),
        # more rolls than required is ok:
        (["1 2 3 4 5 6"], [1, 2, 3, 4, 5, 6]),
        # invalid input in between is ignored
        (["1", "4 asdf", "2 3"], [1, 2, 3]),
        (["1", "5 6 7", "2 2"], [1, 2, 2]),
    ])
    def test_valid(self, monkeypatch, user_input, expected):
        query_user = QueryUserForDice()

        patch_input(monkeypatch, user_input)
        result = query_user(num_sides=6, required_num_rolls=3)
        assert result == expected

    @pytest.mark.parametrize("user_input", [
        (["1 2 a"]),
        (["1 2"]),
        (["1 2", "foo"])
    ])
    def test_invalid(self, monkeypatch, user_input):
        query_user = QueryUserForDice()
        patch_input(monkeypatch, user_input)

        with pytest.raises(StopIteration):
            query_user(num_sides=6, required_num_rolls=3)
