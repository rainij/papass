import secrets

from random_number_generator.base import RandomNumberGeneratorBase


class SystemRng(RandomNumberGeneratorBase):
    """Random number generator using the operating system."""

    def randbelow(self, upper: int) -> int:
        return secrets.randbelow(upper)
