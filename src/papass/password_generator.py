import math
from collections.abc import Sequence
from dataclasses import dataclass

from papass.random_source import RngBase
from papass.utils import PowerSequence


@dataclass
class PasswordResult:
    """Represents the result of password generation."""

    password: str
    """The generated password."""

    entropy: float
    """Estimates how secure the password is against brute-force cracking.

    The number of possible passwords which could have been generated with the same
    settings is ``2**entropy``.
    """


class PasswordGenerator:
    """Generate passwords from a list of characters using a random number generator."""

    def __init__(self, *, alphabet: Sequence[str], rng: RngBase):
        """Create a password generator.

        :param alphabet: A sequence of characters to be used in password creation.
        :param rng: The randomness source to be used to draw characters.

        The the alphabet gets deduplicated internally.
        """
        assert len(alphabet) > 0, "Alphabet must not be empty."
        assert all(
            len(c) == 1 for c in alphabet
        ), "Alphabet must be a list of characters (length 1)."

        self._alphabet = list(sorted(set(alphabet)))
        self._rng = rng

    def generate(self, length: int) -> PasswordResult:
        """Generate a random password.

        The password is *essentially* created by a single application of ``rng.choice`` to
        the set of all possible passwords (lazy iterators make this possible even for
        large password spaces).

        :param length: The length of the password.
        :return: A result object containing the generated password.
        """
        power_alphabet = PowerSequence(self._alphabet, length)
        index = self._rng.randbelow(power_alphabet.size)
        characters = power_alphabet[index]

        return PasswordResult(
            password="".join(characters),
            entropy=length * self._entropy_per_char,
        )

    @property
    def _base(self) -> int:
        return len(self._alphabet)

    @property
    def _entropy_per_char(self) -> float:
        return math.log2(self._base)
