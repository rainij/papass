import math
from collections.abc import Sequence
from dataclasses import dataclass

from papass.random import RngBase


@dataclass
class PassWordResult:
    """Represents the result of password generation."""

    password: str
    entropy: float


class PassWordGenerator:
    """Generate passwords from a list of characters using a random number generator."""

    def __init__(self, *, alphabet: Sequence[str], rng: RngBase):
        """Create a password generator.

        :param alphabet: A sequence of characters to be used in password creation.
        :param rng: The randomness source to be used to draw characters.

        The the alphabet gets deduplicated internally.
        """
        assert all(
            len(c) == 1 for c in alphabet
        ), "Alphabet must be a list of characters (length 1)."

        self._alphabet = list(sorted(set(alphabet)))
        self._rng = rng

    def generate(self, length: int) -> PassWordResult:
        return PassWordResult(
            password="".join(self._choose_char() for _ in range(length)),
            entropy=length * self._entropy_per_char,
        )

    def _choose_char(self) -> str:
        return self._rng.choice(self._alphabet)

    @property
    def _entropy_per_char(self) -> float:
        return math.log2(len(self._alphabet))
