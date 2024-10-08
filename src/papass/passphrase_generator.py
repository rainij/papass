import math
from dataclasses import dataclass
from functools import cached_property

from .random_source.base import RngBase
from .utils import PowerSequence
from .wordlist import WordList


@dataclass
class PassphraseResult:
    """Represents the result of passphrase generation."""

    passphrase: str
    """The generated passphrase."""

    entropy: float
    """Estimates how secure the passphrase is against brute-force cracking.

    Ideally the number of passphrases which could have been generated with the same
    settings is ``2**entropy``. We use a simple formula to estimate the entropy, hence the
    estimate might not be guaranteed to be exact.
    """

    entropy_is_guaranteed: bool
    """Whether we can guarantee that the entropy is correctly estimated.

    ``True`` means that the entropy estimate is exact. ``False`` means that our heuristic
    could not prove that the estimate is exact (it might be exact though).

    Note that even if the entropy estimate is not exact it probably does not overestimate
    it too much in most cases.

    See also:
    https://papass.readthedocs.io/en/stable/usage_cli.html#entropy-guarantee
    """


class PassphraseGenerator:
    """Generate phrases from a wordlist using a random number generator."""

    _wordlist: WordList
    _rng: RngBase

    _delimiter: str

    def __init__(
        self,
        *,
        wordlist: WordList,
        rng: RngBase,
        delimiter: str = " ",
    ):
        """Create a passphrase generator.

        :param wordlist: The words to draw from.
        :param rng: The randomness source to be used to draw words.
        :param delimiter: At most a single character to be put between the generated words.
        """
        assert len(delimiter) <= 1, "--delimiter must be single character or empty."

        self._wordlist = wordlist
        self._rng = rng
        self._delimiter = delimiter

    def generate(self, length: int) -> PassphraseResult:
        """Generate a random passphrase.

        The passphrase is *essentially* created by a single application of ``rng.choice`` to
        the set of all possible passwords (lazy iterators make this possible even for
        large passphrase spaces).

        :param length: The number of words in the passphrase.
        :return: A result object containing the generated passphrase.
        """
        power_wordlist = PowerSequence(self._wordlist, length)
        index = self._rng.randbelow(power_wordlist.size)
        words = power_wordlist[index]

        return PassphraseResult(
            passphrase=self._delimiter.join(words),
            entropy=length * self._entropy_per_word,
            entropy_is_guaranteed=self._entropy_is_guaranteed(length),
        )

    @property
    def _entropy_per_word(self) -> float:
        return math.log2(len(self._wordlist))

    def _entropy_is_guaranteed(self, count: int) -> bool:
        """Return ``True`` if we can guarantee that the entropy estimate is exact.

        We use a simple heuristic: If the delimiter does not occur in any of the words it
        serves as marker forfor the word boundaries. In that case the number of possible
        passphrases is indeed

        number_of_words_in_wordlist ** number_of_words_in_passphrase

        and the entropy estimate is correct.

        If the heuristic is not satisfied it can in principle still be the case that the
        number of possible passphrases is as desired. But it is hard to check this in
        general so we just return False in that case (we could not prove that it is the
        case).

        But note that in general we entropy is "probably" not too far off.
        """
        assert len(self._delimiter) <= 1

        if count <= 1:
            # In this case delimiter is not even used
            return True
        elif self._delimiter == "" or self._delimiter in self._word_alphabet:
            return False

        return True

    @cached_property
    def _word_alphabet(self) -> set[str]:
        """Set of letters occuring the words."""
        return set().union(*self._wordlist)
