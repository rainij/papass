import math
from dataclasses import dataclass

from random_number_generator.base import RandomNumberGeneratorBase
from wordlist import WordList


@dataclass
class Result:
    phrase: str
    entropy: float


class RandomPhraseGenerator:
    """Generate phrases from a wordlist using a random number generator."""

    _wordlist: WordList
    _rng: RandomNumberGeneratorBase
    _delim: str

    def __init__(self, wordlist: WordList, rng: RandomNumberGeneratorBase):
        self._wordlist = wordlist
        self._rng = rng
        self._delim = " "

    def get_phrase(self, count: int) -> Result:
        """Generate a random phrase."""
        return Result(
            phrase=self._delim.join(
                [self._rng.choice(self._wordlist) for _ in range(count)]
            ),
            entropy=count * self._entropy_per_word(),
        )

    def _entropy_per_word(self) -> float:
        return math.log2(len(self._wordlist))
