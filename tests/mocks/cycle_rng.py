from collections.abc import Iterable, Iterator

from rspass.random.base import RandomNumberGeneratorBase


class MockCycleRng(RandomNumberGeneratorBase):
    _cycle: Iterator[int]

    def __init__(self, cycle: Iterable[int]):
        cycle = list(cycle)
        assert cycle, "Cycle must not be empty."

        def _cycler() -> Iterator[int]:
            i = 0
            while True:
                yield cycle[i]
                i += 1
                i = 0 if i >= len(cycle) else i

        self._cycle = _cycler()

    def randbelow(self, upper: int) -> int:
        """Return a random integer from [0, upper).

        The output is uniformly distributed.
        """
        return next(self._cycle) % upper
