import secrets

from .base import RngBase


class SystemRng(RngBase):
    """Random number generator using the most secure rng of the operating system."""

    def randbelow(self, upper: int) -> int:
        """Get a random integer ``i`` with ``0 <= i < upper``.

        ``i`` is uniformly distributed.
        """
        return secrets.randbelow(upper)
