import secrets

from random_number_generator.base import RandomNumberGeneratorBase


class SystemRng(RandomNumberGeneratorBase):
    """Random number generator using the operating system."""

    def __init__(self, config):
        pass

    def randbelow(self, end: int) -> int:
        return secrets.randbelow(end)
