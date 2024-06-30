from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


# TODO: rename to NumberGeneratorBase?
class RandomNumberGeneratorBase(ABC):
    """Base for all random number generators."""

    # TODO: make the texts a bit more generic. Move the statement about uniform
    # distribution into derived classes and make it possible for an rng to claim that it
    # is uniform.

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
