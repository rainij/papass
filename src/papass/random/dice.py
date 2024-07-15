from dataclasses import dataclass

import click

from papass.utils import rolls_to_value

from .base import RandomNumberGeneratorBase


@dataclass
class DiceFrame:
    upper_multiple: int
    required_num_rolls: int


class DiceRng(RandomNumberGeneratorBase):
    """Random number generator relying on the user to throw physical dice."""

    def __init__(self, *, num_sides: int = 6, required_success_probability: float = 0.99):
        assert num_sides > 1, f"num_sides must be at least 1, got {num_sides}"
        assert (
            0 <= required_success_probability < 1.0
        ), f"required_success_probability must be >= 0 and < 1.0. Got {required_success_probability}."

        self._num_sides = num_sides
        self._required_success_probability = required_success_probability

    def randbelow(self, upper: int) -> int:
        """TODO: docstring"""
        # TODO:
        # - improve this
        # - introduce option for success probability
        frame = self._compute_frame(upper)
        required_num_rolls = frame.required_num_rolls
        upper_multiple = frame.upper_multiple

        result = None
        while result is None:
            user_input = input(f"Roll at least {required_num_rolls} dice: ")
            rolls = self._parse_user_input(user_input, required_num_rolls)

            if rolls is None:
                continue

            result = rolls_to_value(self._num_sides, rolls)

            if result >= upper_multiple:
                click.echo("Rejected. Try again!")
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

    def _parse_user_input(
        self, user_input: str, required_num_rolls: int
    ) -> list[int] | None:
        """Returns None if user input could not be parsed."""
        try:
            rolls = [int(r) for r in user_input.split()]
        except ValueError:
            click.echo(
                "Invalid. Require a space-separated list of integers (like: 1 3 2). Roll again!"
            )
            return None

        if len(rolls) < required_num_rolls:
            click.echo(
                f"Got only {len(rolls)} rolls, need {required_num_rolls}. Roll again!"
            )
            return None

        if not all(1 <= r <= self._num_sides for r in rolls):
            click.echo(f"Some rolls are not between 1 and {self._num_sides}. Roll again!")
            return None

        return rolls


def compute_dice_frame(
    *, num_sides: int, upper: int, required_success_probability: float
) -> DiceFrame:
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
