import re
from collections.abc import Iterable, Sequence
from pathlib import Path


class WordList(Sequence[str]):
    """Represents an sorted sequence of unique words.

    Internally the list of words is sorted alphabetically (via `sorted`).

    # Example

    >>> wordlist = WordList(["c", "b", "a"])
    >>> wordlist
    WordList(['a', 'b', 'c'])
    >>> assert wordlist[0] == "a"
    >>> assert list(wordlist) == ["a", "b", "c"]
    >>> assert wordlist == WordList(["a", "b", "c"])
    """

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
        :param max_word_size: Filter out words which are longer than this. None means no
            filtering.
        """
        words = sorted(list(words))
        self._validate(words)
        self._words = words

        # TODO: Better error handling
        assert min_word_size > 0
        assert max_word_size is None or max_word_size >= min_word_size

        self._filter_min_word_size(min_word_size)
        self._filter_max_word_size(max_word_size)

    def __getitem__(self, index) -> str:
        return self._words[index]

    def __len__(self) -> int:
        return len(self._words)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WordList):
            return False
        return self._words == other._words

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return f"{WordList.__name__}({self._words})"

    @staticmethod
    def from_file(file_path: Path, **options):
        """Construct a wordlist from a file of words (newline separated).

        The options are the same as the kwargs for the __init__ function.
        """
        with open(file_path, "r") as f:
            words = [w.strip() for w in f.readlines()]
            return WordList(words, **options)

    @staticmethod
    def _validate(words: list[str]) -> None:
        # TODO: really test for a pattern? Should we validate at all?
        allowed_pattern = re.compile("[a-z]+")

        # TODO: Would empty list be OK
        assert len(words) != 0, "Empty wordlist."
        assert all(
            allowed_pattern.match(w) for w in words
        ), f"Words should match pattern '{allowed_pattern}'."
        # TODO: maybe just deduplicate?
        assert len(set(words)) == len(words), "All words must be different."

    def _filter_min_word_size(self, min_word_size: int) -> None:
        self._words = [w for w in self._words if len(w) >= min_word_size]

    def _filter_max_word_size(self, max_word_size: int | None) -> None:
        if max_word_size is None:
            return

        self._words = [w for w in self._words if len(w) <= max_word_size]
