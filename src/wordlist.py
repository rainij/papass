import re
from collections.abc import Iterable, Sequence
from pathlib import Path


class WordList(Sequence[str]):
    """Represents a sequence of unique words."""

    _words: list[str]

    def __init__(
        self,
        words: Iterable[str],
        *,
        min_word_size: int = 1,
        max_word_size: int | None = None,
    ):
        """Construct a wordlist from words.

        :param words: Words to construct wordlist from.
        :param min_word_size: Filter out words which are shorter than this.
        :param max_word_size: Filter out words which are longer than this. None means no filtering.
        """
        words = list(words)
        self._validate(words)
        self._words = words

        # TODO: Better error handling
        assert min_word_size > 0
        assert max_word_size is None or max_word_size >= min_word_size

        self._filter_min_word_size(min_word_size)
        self._filter_max_word_size(max_word_size)

    def __getitem__(self, index):
        return self._words[index]

    def __len__(self):
        return len(self._words)

    @staticmethod
    def from_file(file_path: Path, **options):
        """Construct a wordlist from a file of words (newline separated).

        The options are the same as the kwargs for the __init__ function.
        """
        with open(file_path, "r") as f:
            words = [w.strip() for w in f.readlines()]
            return WordList(words, **options)

    @staticmethod
    def _validate(words: list[str]):
        # TODOs:
        # - testing
        # - Better error handling. Better messages (logging).

        allowed_pattern = re.compile("[a-z]+")

        assert len(words) != 0, "Empty wordlist."
        assert all(
            allowed_pattern.match(w) for w in words
        ), f"Words should match pattern '{allowed_pattern}'."
        assert len(set(words)) == len(words), "All words must be different."

    def _filter_min_word_size(self, min_word_size: int) -> None:
        self._words = [w for w in self._words if len(w) >= min_word_size]

    def _filter_max_word_size(self, max_word_size: int | None) -> None:
        if max_word_size is None:
            return

        self._words = [w for w in self._words if len(w) <= max_word_size]
