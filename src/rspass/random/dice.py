from functools import reduce

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

        num_rolls = 1
        upper_dice = num_sides

        while upper_dice < upper:
            num_rolls += 1
            upper_dice *= num_sides

        upper_multiple = (upper_dice // upper) * upper

        result = None
        while result is None:
            user_input = input(f"Roll {num_rolls} dice: ")
            rolls = [int(r) for r in user_input.split()]

            if len(rolls) < num_rolls:
                print(f"Got only {len(rolls)} rolls, need {num_rolls}. Roll again!")
                continue

            if not all(1 <= r <= num_sides for r in rolls):
                print(f"Some rolls are not between 1 and {num_sides}. Roll again!")
                continue

            result = reduce(lambda acc, r: num_sides * acc + r - 1, rolls, 0)

            if result >= upper_multiple:
                print("Rejected")
                result = None
                continue

            result = result % upper

        return result
