import random
from collections.abc import Sequence


class WordList(Sequence[str]):
    """TODO"""

    _words: list[str]

    def __init__(self, words: list[str], config):
        self._words = words

    def __getitem__(self, index):
        return self._words[index]

    def __len__(self):
        return len(self._words)

    def __iter__(self):
        return iter(self._words)


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


class RandomPhraseGenerator:
    """TODO."""

    _wordlist: WordList
    _rng: RandomNumberGenerator
    _delim: str

    def __init__(self, wordlist: WordList, rng: RandomNumberGenerator):
        self._wordlist = wordlist
        self._rng = rng
        self._delim = " "

    def get(self, count: int) -> str:
        """TODO."""
        return self._delim.join([self._rng.choice(self._wordlist) for _ in range(count)])
