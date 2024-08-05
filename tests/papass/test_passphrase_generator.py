import string

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from papass import PassphraseGenerator, WordList

from tests.utils.cycle_rng import CycleRng


@st.composite
def st_ordered_pair(draw, min: int, max: int) -> tuple[int, int]:
    """Strategy returning (i, j) with min <= i < j <= max."""
    j = draw(st.integers(min + 1, max))
    i = draw(st.integers(min, j - 1))
    return (i, j)


class TestPassphraseGenerator:
    @given(ij=st_ordered_pair(0, 26**11 - 1))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_randbelow_to_passphrase_1(self, ij):
        """Makes sure that the mapping preserves strict order and hence is bijective."""
        length = 11
        wordlist = WordList(string.ascii_lowercase)

        # Compare with @given:
        assert length == 11, "Assumption of test violated"
        assert len(wordlist) == 26, "Assumption of test violated"

        # Each call to generate calls randbelow exactly once:
        i, j = ij
        ppg = PassphraseGenerator(wordlist=wordlist, rng=CycleRng([i, j]))
        passphrase_1 = ppg.generate(length).passphrase
        passphrase_2 = ppg.generate(length).passphrase

        assert i < j, "This shouldn't fail"
        assert passphrase_1 < passphrase_2

    @pytest.fixture
    def wordlist(self):
        """Eight words. Three bits of entropy per word."""
        return WordList(list("abcdefgh"))

    @pytest.mark.parametrize(
        "cycle, passphrase",
        [
            # NOTE: choice and hence randbelow should only be called once.
            ([0], "aaaa"),
            ([1], "aaab"),
            ([2], "aaac"),
            # Checks that the second value in cycle is irrelevant:
            ([0, 1], "aaaa"),
            # Each coefficient corresponds to a letter in order:
            ([4 * 8**3 + 0 * 8**2 + 2 * 8 + 7], "each"),
            ([2 * 8**3 + 0 * 8**2 + 5 * 8 + 4], "cafe"),
            ([8**4 - 1], "hhhh"),
        ],
    )
    def test_randbelow_to_passphrase_2(self, wordlist, cycle, passphrase):
        """Similar purpose as the other test of the same name but from a different angle."""
        ppg = PassphraseGenerator(wordlist=wordlist, rng=CycleRng(cycle), delimiter="")
        result = ppg.generate(4)

        assert result.passphrase == passphrase
        assert result.entropy == pytest.approx(12.0)

    @pytest.mark.parametrize("length", range(4))
    def test_entropy(self, wordlist, length):
        ppg = PassphraseGenerator(wordlist=wordlist, rng=CycleRng(range(4)), delimiter=" ")

        # wordlist has 4 words, so 2 bits of entropy per word.
        assert ppg.generate(length).entropy == pytest.approx(3 * length)

    @pytest.mark.parametrize("delimiter", list(" @-*"))
    def test_delimiter(self, wordlist, delimiter: str):
        ppg = PassphraseGenerator(wordlist=wordlist, rng=CycleRng([0]), delimiter=delimiter)

        assert ppg.generate(3).passphrase == delimiter.join("aaa")


class TestEntropyGuarantee:
    """Test correctness of entropy guarantee.

    We only test the following:

    - Guarantee MUST be True if current implementation SHOULD be able to prove it true.
    - Guarantee MUST be False if entropy IS indeed lower.

    For all other cases we do not test it because the implementation might become smarter.
    """

    @pytest.fixture
    def wordlist(self):
        """Wordlist with the following properties

        - Words do not contain `x` or `y`.
        - Using e.g. `a` as delimiter decreases the number of possible passphrases as compared to
          using ` `. For example `aaab` can occur in mulitple ways (from chosing `aa` and `b` as
          well as from chosing `a` and `ab`).
        """
        return WordList(["aa", "bb", "ab", "b", "a"])

    @pytest.mark.parametrize(
        "delimiter",
        [
            # If the delimiter is not from the alphabet of the words the entropy is guaranteed:
            " ",
            "#",
            "-",
            "x",
            "y",
        ],
    )
    def test_is_guaranteed(self, wordlist, delimiter):
        ppg = PassphraseGenerator(wordlist=wordlist, delimiter=delimiter, rng=CycleRng([0, 1]))
        result = ppg.generate(2)
        assert result.entropy_is_guaranteed

    @pytest.mark.parametrize(
        "delimiter",
        [
            "",
            "a",
            "b",
        ],
    )
    def test_is_not_guaranteed(self, wordlist, delimiter):
        # With the chosen wordlist these delimiters decrease the number of possible passphrases.
        # Hence check must return False.
        ppg = PassphraseGenerator(wordlist=wordlist, delimiter=delimiter, rng=CycleRng([0, 1]))

        # Edge case: If only one word is generated the guarantee naturally holds.
        result_1 = ppg.generate(1)
        result_2 = ppg.generate(2)

        assert result_1.entropy_is_guaranteed
        assert not result_2.entropy_is_guaranteed
