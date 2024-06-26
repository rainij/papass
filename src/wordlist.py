import re
from collections.abc import Iterable, Sequence
from pathlib import Path


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
