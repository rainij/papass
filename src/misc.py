import random
from collections.abc import Sequence
from pathlib import Path
from dataclasses import dataclass
import math


class WordList(Sequence[str]):
    """TODO"""

    _words: list[str]

    def __init__(self, words: list[str], config):
        # TODO: validation, transformation
        self._words = words

    def __getitem__(self, index):
        return self._words[index]

    def __len__(self):
        return len(self._words)

    @staticmethod
    def from_file(path: Path, config):
        with open(path, "r") as f:
            words = f.readlines()
            return WordList(words, config)


class RandomNumberGenerator:
    """TODO."""

    def __init__(self, config): ...

    def randint(self, end: int) -> int:
        """Return a random integer between 0 (inclusive) and end (exclusive)."""
        return random.randint(0, end - 1)

    # TODO: more generic typing
    def choice(self, items: Sequence[str]) -> str:
        assert items, "Empty items!"
        index = self.randint(len(items))
        return items[index]


@dataclass
class Result:
    phrase: str
    entropy: float


class RandomPhraseGenerator:
    """TODO."""

    _wordlist: WordList
    _rng: RandomNumberGenerator
    _delim: str

    def __init__(self, wordlist: WordList, rng: RandomNumberGenerator):
        self._wordlist = wordlist
        self._rng = rng
        self._delim = " "

    def get(self, count: int) -> Result:
        """TODO."""
        return Result(
            phrase = self._delim.join([self._rng.choice(self._wordlist) for _ in range(count)]),
            entropy = count * self._entropy_per_word(),
        )

    def _entropy_per_word(self) -> float:
        return math.log2(len(self._wordlist))
