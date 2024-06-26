import math
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from random_number_generator.base import RandomNumberGeneratorBase


class WordList(Sequence[str]):
    """Represents a sequence of unique words."""

    _words: list[str]

    def __init__(self, words: Iterable[str], config):
        # TODO: validation, transformation
        self._validate(words)
        self._words = list(words)

    def __getitem__(self, index):
        return self._words[index]

    def __len__(self):
        return len(self._words)

    @staticmethod
    def from_file(path: Path, config):
        with open(path, "r") as f:
            words = [w.strip() for w in f.readlines()]
            return WordList(words, config)

    @staticmethod
    def _validate(words):
        # TODOs:
        # - testing
        # - maybe use something else then assert. Better messages (logging)

        allowed_pattern = re.compile("[a-z]+")

        assert len(words) != 0, "Empty wordlist."
        assert all(
            allowed_pattern.match(w) for w in words
        ), f"Words should match pattern '{allowed_pattern}'."
        assert len(set(words)) == len(words), "All words must be different."


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
