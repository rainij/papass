from collections.abc import Iterable, Iterator

import pytest
from rspass.phrase_generator import PhraseGenerator
from rspass.random.base import RandomNumberGeneratorBase
from rspass.wordlist import WordList


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


def test_mock_cycle_rng():
    rng = MockCycleRng(range(10, 12))

    assert rng.randbelow(10) == 0
    assert rng.randbelow(10) == 1
    assert rng.randbelow(10) == 0
    assert rng.randbelow(10) == 1


class TestPhraseGenerator:
    @pytest.fixture
    def wordlist(self):
        """Four words. Two bits of entropy per word."""
        return WordList(["a", "b", "c", "d"])

    @pytest.mark.parametrize(
        "cycle,phrase",
        [
            ([2], "cccc"),
            ([0, 1], "abab"),
            ([0, 3, 1, 2], "adbc"),
        ],
    )
    def test_get_phrase_uses_rng_choice_in_order(self, wordlist, cycle, phrase):
        rpg = PhraseGenerator(
            wordlist=wordlist, rng=MockCycleRng(cycle), delimiter=""
        )

        assert rpg.get_phrase(4).phrase == phrase

    @pytest.mark.parametrize("count", range(4))
    def test_entropy(self, wordlist, count):
        rpg = PhraseGenerator(
            wordlist=wordlist, rng=MockCycleRng(range(4)), delimiter=" "
        )

        # wordlist has 4 words, so 2 bits of entropy per word.
        assert rpg.get_phrase(count).entropy == pytest.approx(2 * count)

    @pytest.mark.parametrize("delimiter", list(" @-*"))
    def test_delimiter(self, wordlist, delimiter: str):
        rpg = PhraseGenerator(
            wordlist=wordlist, rng=MockCycleRng(range(4)), delimiter=delimiter
        )

        assert rpg.get_phrase(3).phrase == delimiter.join(wordlist[:3])
