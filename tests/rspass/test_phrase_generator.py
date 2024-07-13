import pytest
from papass.phrase_generator import PhraseGenerator
from papass.wordlist import WordList

from tests.utils.cycle_rng import CycleRng

# TODO: test error handling


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
        rpg = PhraseGenerator(wordlist=wordlist, rng=CycleRng(cycle), delimiter="")

        assert rpg.get_phrase(4).phrase == phrase

    @pytest.mark.parametrize("count", range(4))
    def test_entropy(self, wordlist, count):
        rpg = PhraseGenerator(wordlist=wordlist, rng=CycleRng(range(4)), delimiter=" ")

        # wordlist has 4 words, so 2 bits of entropy per word.
        assert rpg.get_phrase(count).entropy == pytest.approx(2 * count)

    @pytest.mark.parametrize("delimiter", list(" @-*"))
    def test_delimiter(self, wordlist, delimiter: str):
        rpg = PhraseGenerator(
            wordlist=wordlist, rng=CycleRng(range(4)), delimiter=delimiter
        )

        assert rpg.get_phrase(3).phrase == delimiter.join(wordlist[:3])
