from dataclasses import dataclass
from typing import Protocol

from papass.utils import QueryUserForDice, rolls_to_value

from .base import RngBase


class QueryForDice(Protocol):
    """Interface for the ``query_for_dice`` option of ``DiceRng``."""

    def __call__(self, *, num_sides: int, required_num_rolls: int) -> list[int]:
        """Return dice rolls to be turned into the output of ``DiceRng.randbelow``.

        Called within ``DiceRng.randbelow`` until its output is not rejected.

        :param num_sides: Number of sides of the dice.
        :param require_num_rolls: The number of rolls.
        :return: A list of rolls of the required length.
        """

    def notify_rejection(self) -> None:
        """React to rejected dice rolls.

        Called by ``DiceRng`` if output of ``__call__`` got rejected.
        """


@dataclass
class DiceFrame:
    """Metadata required to convert dice rolls into integers.

    The dice frame contains information on how to turn dice rolls into numbers from an
    interval ``[0, upper)`` with a uniform distribution.

    We assume that the dice rolls themselves is (at least approximately) uniform and
    independent.
    """

    upper_multiple: int
    required_num_rolls: int


class DiceRng(RngBase):
    """Random number generator relying on the user to throw physical dice."""

    def __init__(
        self,
        *,
        query_for_dice: QueryForDice | None = None,
        num_sides: int = 6,
        required_success_probability: float = 0.999,
    ):
        """Create a `DiceRng`.

        :param query_for_dice: A callback to query for dice rolls. ``None`` means *use default*.
        :param num_sides: Number of sides of the dice.
        :param required_success_probability: The minimal required probability that
            ``randbelow`` does not reject a roll. If ``upper`` is a power of ``num_sides``
            this probability is always 100%. But in general the number of required rolls
            increases with this probability.
        """
        assert num_sides > 1, f"num_sides must be at least 1, got {num_sides}"
        assert 0 <= required_success_probability < 1.0, (
            "required_success_probability must be >= 0 and < 1.0. "
            f"Got {required_success_probability}."
        )

        self._query_for_dice = query_for_dice or QueryUserForDice()
        self._num_sides = num_sides
        self._required_success_probability = required_success_probability

    def randbelow(self, upper: int) -> int:
        """Generate random integers ``i`` with ``0 <= i < upper``.

        If the dice are fair (all sides occur with the same probability) and the rolls are
        independent the distribution of ``i`` is uniform.
        """
        frame = self._compute_frame(upper)
        required_num_rolls = frame.required_num_rolls
        upper_multiple = frame.upper_multiple

        result = None
        num_rejections = 0
        while result is None:
            rolls = self._query_for_dice(
                num_sides=self._num_sides, required_num_rolls=required_num_rolls
            )
            result = rolls_to_value(self._num_sides, rolls)

            if result >= upper_multiple:
                # To avoid infinite loops (note that rejection probability should be low
                # under "normal" conditions):
                num_rejections += 1
                assert num_rejections < 100, "Absurdly many rejections!"

                self._query_for_dice.notify_rejection()
                result = None
                continue

            result = result % upper

        return result

    def _compute_frame(self, upper: int) -> DiceFrame:
        return compute_dice_frame(
            upper=upper,
            num_sides=self._num_sides,
            required_success_probability=self._required_success_probability,
        )

    def _next_rolls(self, required_num_rolls: int) -> list[int] | None:
        """Get rolls from user."""
        return self._query_for_dice(
            num_sides=self._num_sides, required_num_rolls=required_num_rolls
        )


def compute_dice_frame(
    *, num_sides: int, upper: int, required_success_probability: float
) -> DiceFrame:
    """Return the dice frame."""
    required_num_rolls = 1
    upper_dice = num_sides
    upper_multiple = (upper_dice // upper) * upper

    def success_probability_to_low() -> bool:
        prob = upper_multiple / upper_dice
        return prob < required_success_probability

    while upper_dice < upper or success_probability_to_low():
        required_num_rolls += 1
        upper_dice *= num_sides
        upper_multiple = (upper_dice // upper) * upper

    return DiceFrame(
        upper_multiple=upper_multiple,
        required_num_rolls=required_num_rolls,
    )
