from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class RandomNumberGeneratorBase(ABC):
    """Base for all random number generators."""

    @abstractmethod
    def randbelow(self, upper: int) -> int:
        """Return a random integer from [0, upper).

        The output is uniformly distributed.
        """

    def choice(self, items: Sequence[T]) -> T:
        """Return a random item from items (uniform distribution)."""
        assert items, "Empty items!"
        index = self.randbelow(len(items))
        return items[index]
