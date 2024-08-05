from random import Random

import pytest
from hypothesis import given
from hypothesis import strategies as st
from papass.random_source.dice import DiceRng, compute_dice_frame
from papass.utils import rolls_to_value

from tests.utils.mock import MockCallbackQueryForDice, MockIterQueryForDice


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
        (
            9,
            9**2 - 1,
            [[9, 9, 9, 9], [1, 2, 3, 4]],
        ),
    ],
)
def test_randbelow(num_sides, upper, rolls):
    """*Basic* test showing that randbelow behaves as expected."""
    query = MockIterQueryForDice(rolls)
    rng = DiceRng(query_for_dice=query, num_sides=num_sides, required_success_probability=0.99)

    expected = rolls_to_value(num_sides, rolls[-1]) % upper
    assert rng.randbelow(upper) == expected
    assert query.num_rejections == len(rolls) - 1


@given(
    num_sides=st.integers(2, 20),
    upper=st.integers(2, 1000_000),
    req_prob_exponent=st.integers(1, 6),
)
def test_compute_frame(num_sides, upper, req_prob_exponent):
    required_success_probability = 1.0 - 10 ** (-req_prob_exponent)
    # Due to possible floating point issues (not sure if really needed)
    epsilon = 10 ** (-2 * req_prob_exponent)

    result = compute_dice_frame(
        num_sides=num_sides,
        upper=upper,
        required_success_probability=required_success_probability,
    )

    # The success probability is as high as desired
    upper_dice = num_sides**result.required_num_rolls
    upper_multiple = (upper_dice // upper) * upper
    assert upper_multiple == result.upper_multiple
    success_probability = upper_multiple / upper_dice
    assert success_probability > required_success_probability - epsilon

    # Less rolls would not work:
    upper_dice_less = num_sides ** (result.required_num_rolls - 1)
    upper_multiple_less = (upper_dice_less // upper) * upper
    success_probability_less = upper_multiple_less / upper_dice_less
    assert success_probability_less < required_success_probability + epsilon


class TestUniformity:
    """Test that randbelow has a uniform distribution on [0, upper)."""

    @given(rand_rng=st.randoms(use_true_random=True))
    def test_part_1(self, rand_rng):
        """Tests that randbelow maps into [0,upper) and is uniform on its range.

        It does not test that the range of randbelow the full interval.
        """
        num_sides = 6
        upper = 100
        num_calls = upper // 2

        memo: list[int] = []

        def rolls_callback(required_num_rolls: int, memo=memo, **_ignored) -> list[int]:
            # The memo memorizes all outputs
            out = [rand_rng.randint(1, num_sides) for _ in range(required_num_rolls)]
            value = rolls_to_value(num_sides, rolls=out)
            memo.append(value % upper)
            return out

        query = MockCallbackQueryForDice(rolls_callback)
        dice_rng = DiceRng(
            query_for_dice=query, num_sides=num_sides, required_success_probability=0.99
        )

        all_values = []
        raw_values = []
        for _ in range(num_calls):
            value = dice_rng.randbelow(upper)
            assert 0 <= value < upper, "Not inside bounds."
            all_values.append(value)
            # The last entry of memo lead to the observed value:
            raw_values.append(memo[-1])

        assert len(all_values) == num_calls
        # This essentially tests that the map from non-rejected raw values to actual
        # outputs of randbelow is injective. This injectivity makes sure that randbelow is
        # uniform on its range (assuming the dice rolls are uniform).
        assert len(set(all_values)) == len(set(raw_values))

    @given(
        # Taking a seed is faster than taking an rng in case of failures:
        rand_seed=st.integers(0, 2**128),
    )
    def test_part_2(self, rand_seed):
        """Test that all values from [0, upper) are possible."""
        # These values make it *extremely* unlikely that the heuristic check below fails:
        num_sides = 5
        upper = 3
        num_calls = 200

        rand_rng = Random(rand_seed)

        def rolls_callback(required_num_rolls: int, **_ignored) -> list[int]:
            return [rand_rng.randint(1, num_sides) for _ in range(required_num_rolls)]

        query = MockCallbackQueryForDice(rolls_callback)
        dice_rng = DiceRng(
            query_for_dice=query, num_sides=num_sides, required_success_probability=0.99
        )

        obtained_values = [dice_rng.randbelow(upper) for _ in range(num_calls)]
        assert set(obtained_values) == set(range(upper)), "Heuristic surjectivity check."
