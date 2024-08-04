from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class RngBase(ABC):
    """Base for all random number generators."""

    @abstractmethod
    def randbelow(self, upper: int) -> int:
        """Return a random integer ``i`` with ``0 <= i < upper``."""

    def choice(self, items: Sequence[T]) -> T:
        """Return a random item from ``items``.

        The choices are determined by consecutive calls to ``randbelow`` which determines
        the index of the item to be chosen.
        """
        assert items, "Items must not be empty."
        index = self.randbelow(len(items))
        return items[index]
