from collections.abc import Iterable, Iterator, Sequence
from functools import reduce
from typing import Generic, TypeVar, overload

import click


def digits_to_value(base: int, digits: Iterable[int]) -> int:
    """Compute the integer with the given digits in base.

    Example
    =======

    >>> digits_to_value(10, [1, 2, 3])
    123
    """
    assert 1 < base
    assert all(0 <= d < base for d in digits)
    return reduce(lambda acc, r: base * acc + r, digits, 0)


def rolls_to_value(num_sides: int, rolls: Iterable[int]) -> int:
    """Compute the integer corresponding to the given dice rolls.

    Example
    =======

    >>> rolls_to_value(6, [5, 3])  # 6*(5-1) + (3-1)
    26
    """
    digits = [r - 1 for r in rolls]
    return digits_to_value(num_sides, digits)


def value_to_digits(value: int, *, base: int, length: int | None = None) -> list[int]:
    """Return the digits of ``value`` in given base.

    Example
    =======

    >>> value_to_digits(123, base=10, length=4)
    [0, 1, 2, 3]
    """
    assert value >= 0, "Only positive values allowed."

    result: list[int] = []

    while value:
        result.append(value % base)
        value //= base

    if length is not None:
        assert length >= len(result)
        zeros = [0] * (length - len(result))
        result.extend(zeros)

    result.reverse()
    return result


class QueryUserForDice:
    """Asks the user to roll some dice."""

    def __call__(self, *, num_sides: int, required_num_rolls: int) -> list[int]:
        """Ask user for desired number of dice rolls.

        Return ``None`` if user gives invalid input.
        """
        rolls: list[int] = []
        while len(rolls) < required_num_rolls:
            remaining_num_rolls = required_num_rolls - len(rolls)

            if not rolls:
                user_input = input(f"Roll {remaining_num_rolls} dice: ")
            else:
                user_input = input(f"Roll remaining {remaining_num_rolls} dice: ")

            rolls += self._parse_input(
                user_input, num_sides=num_sides, required_num_rolls=required_num_rolls
            )

        return rolls

    def notify_rejection(self) -> None:
        """Print a message on the rejection to stdout.

        Does nothing else.
        """
        click.echo("Rejected. Please try again.")

    @staticmethod
    def _parse_input(
        user_input: str, *, num_sides: int, required_num_rolls: int
    ) -> list[int]:
        """Parse user input as a list of dice rolls.

        Returns ``[]`` if input is invalid.

        Example
        =======

        >>> cls = QueryUserForDice
        >>> cls._parse_input("2 3 5", num_sides=6, required_num_rolls=3)
        [2, 3, 5]

        In case the user provides invalid input:

        >>> cls._parse_input("2 3 7", num_sides=6, required_num_rolls=3)
        Some rolls are not between 1 and 6.
        []
        >>> cls._parse_input("foo 3", num_sides=6, required_num_rolls=3)
        Invalid. Require a space-separated list of integers (like: 1 3 2).
        []
        """
        try:
            rolls = [int(r) for r in user_input.split()]
        except ValueError:
            click.echo(
                "Invalid. Require a space-separated list of integers (like: 1 3 2)."
            )
            return []

        if not all(1 <= r <= num_sides for r in rolls):
            click.echo(f"Some rolls are not between 1 and {num_sides}.")
            return []

        return rolls


T = TypeVar("T")


class PowerSequence(Generic[T]):
    """A sequence representing a cartesian power product.

    Example
    =======

    >>> ps = PowerSequence([0, 1, 2], 2)
    >>> list(ps)
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    It supports huge powers for which the entire sequence would not fit into memory:

    >>> ps = PowerSequence(range(1000), 20)
    >>> ps[1000**19 + 98765432101234567890876543210123456789]
    (1, 0, 0, 0, 0, 0, 0, 98, 765, 432, 101, 234, 567, 890, 876, 543, 210, 123, 456, 789)

    NOTE: In essence this thing is a Sequence. Unfortunately due to a limitation of
    CPython __len__ is not allowed to return large integers (it must be "index-sized").
    """

    def __init__(self, sequence: Sequence[T], power: int):
        """Create a power sequence."""
        assert power >= 0

        self._sequence = sequence
        self._power = power
        self._base_length = len(sequence)

    @property
    def size(self) -> int:
        """Number of elements in the power sequence.

        NOTE: This replaces __len__. See class docstring for the reason.
        """
        return self._base_length**self._power

    def __bool__(self) -> bool:
        """True iff the sequence is non-empty."""
        return self.size != 0

    # TODO: slice not supported.
    @overload
    def __getitem__(self, index: int) -> tuple[T, ...]: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[tuple[T, ...]]: ...
    def __getitem__(self, index: int | slice) -> tuple[T, ...] | Sequence[tuple[T, ...]]:
        """Get item at given index.

        The elements are ordered lexicographically.
        """
        if isinstance(index, slice):
            raise NotImplementedError("Indexing by slices not supported.")

        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        indices = value_to_digits(index, base=self._base_length, length=self._power)
        return tuple(self._sequence[i] for i in indices)

    def __iter__(self) -> Iterator[tuple[T, ...]]:
        for i in range(self.size):
            yield self[i]
