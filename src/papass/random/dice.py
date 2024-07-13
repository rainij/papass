from papass.utils import rolls_to_value

from .base import RandomNumberGeneratorBase


class DiceRng(RandomNumberGeneratorBase):
    """Random number generator relying on the user to throw physical dice."""

    _num_sides: int

    def __init__(self, *, num_sides: int = 6):
        assert num_sides > 1
        self._num_sides = num_sides

    def randbelow(self, upper: int) -> int:
        # TODO:
        # - improve this
        # - introduce option for success probability
        # - better error handling and user feedback
        num_sides = self._num_sides

        required_num_rolls = 1
        upper_dice = num_sides

        while upper_dice < upper:
            required_num_rolls += 1
            upper_dice *= num_sides

        upper_multiple = (upper_dice // upper) * upper

        result = None
        while result is None:
            user_input = input(f"Roll at least {required_num_rolls} dice: ")
            rolls = self._parse_user_input(user_input, required_num_rolls)

            if rolls is None:
                continue

            result = rolls_to_value(self._num_sides, rolls)

            if result >= upper_multiple:
                print("Rejected")
                result = None
                continue

            result = result % upper

        return result

    def _parse_user_input(
        self, user_input: str, required_num_rolls: int
    ) -> list[int] | None:
        """Returns None if user input could not be parsed."""
        try:
            rolls = [int(r) for r in user_input.split()]
        except ValueError:
            print(
                "Invalid. Require a space-separated list of integers (like: 1 3 2). Roll again!"
            )
            return None

        if len(rolls) < required_num_rolls:
            print(f"Got only {len(rolls)} rolls, need {required_num_rolls}. Roll again!")
            return None

        if not all(1 <= r <= self._num_sides for r in rolls):
            print(f"Some rolls are not between 1 and {self._num_sides}. Roll again!")
            return None

        return rolls
