from functools import reduce

from random_number_generator.base import RandomNumberGeneratorBase


class DiceRng(RandomNumberGeneratorBase):
    """Random number generator relying on the user to throw physical dice."""

    _num_sides: int

    def __init__(self, *, num_sides: int = 6):
        assert num_sides > 1
        self._num_sides = num_sides

    def randbelow(self, upper: int) -> int:
        # TODO:
        # - improve this
        # - testing (also success probability)
        num_sides = self._num_sides

        num_rolls = 1
        upper_dice = num_sides

        while upper_dice - 1 < upper:
            num_rolls += 1
            upper_dice *= num_sides

        upper_dice -= 1
        upper_multiple = (upper_dice % upper) * upper

        result = None
        while result is None:
            user_input = input(f"Roll {num_rolls} dice: ")
            rolls = [int(r) for r in user_input.split()]
            assert all(1 <= r <= num_sides for r in rolls), "Invalid input"

            result = reduce(lambda acc, r: num_sides * acc + r - 1, rolls, 0)

            if result >= upper_multiple:
                print("Rejected")
                result = None
                continue

            result = result % upper

        return result
