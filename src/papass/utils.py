from collections.abc import Iterable
from functools import reduce

import click


def digits_to_value(base: int, digits: Iterable[int]) -> int:
    """Compute the integer with the given digits in base.

    Example:
    >>> digits_to_value(10, [1, 2, 3])
    123
    """
    assert 1 < base
    assert all(0 <= d < base for d in digits)
    return reduce(lambda acc, r: base * acc + r, digits, 0)


def rolls_to_value(num_sides: int, rolls: Iterable[int]) -> int:
    """Compute the integer corresponding to the given dice rolls.

    Example:
    >>> rolls_to_value(6, [5, 3])  # 6*(5-1) + (3-1)
    26
    """
    digits = [r - 1 for r in rolls]
    return digits_to_value(num_sides, digits)


# TODO: testing
class QueryStdinForDice:
    def __call__(self, *, num_sides: int, required_num_rolls: int) -> list[int]:
        """Query stdin for desired number of dice rolls.

        Return ``None`` if user gives invalid input.
        """
        user_input = input(f"Roll at least {required_num_rolls} dice: ")

        rolls = None
        while rolls is None:
            rolls = self._parse_stdin(
                user_input, num_sides=num_sides, required_num_rolls=required_num_rolls
            )

        return rolls

    def notify_rejection(self) -> None:
        click.echo("Rejected. Please try again.")

    @staticmethod
    def _parse_stdin(
        user_input: str, *, num_sides: int, required_num_rolls: int
    ) -> list[int] | None:
        """Parse user input as a list of dice rolls.

        Returns ``None`` if input is invalid.

        TODO: also failing examples
        Example:
        >>> QueryStdinForDice._parse_stdin("2 3 5", num_sides=6, required_num_rolls=3)
        [2, 3, 5]
        """
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

        if not all(1 <= r <= num_sides for r in rolls):
            click.echo(f"Some rolls are not between 1 and {num_sides}. Roll again!")
            return None

        return rolls
