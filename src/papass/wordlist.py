import math
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, overload


@dataclass
class FrequencyEntry:
    """Represents a line a word frequency file."""

    word: str
    frequency: int

    pattern: re.Pattern[str] = field(default=re.compile(r"^\d+\t[^\t]+\t\d+$"), init=False)

    @classmethod
    def from_line(cls, line: str, line_number: int) -> "FrequencyEntry":
        """Convert a single line into a `FrequencyEntry`.

        The line number is only required for error messages.
        """
        assert cls.pattern.match(
            line
        ), f"Line {line_number} `{line}` does not match pattern {cls.pattern}."
        entries = line.split("\t")

        return FrequencyEntry(word=entries[1], frequency=int(entries[2]))


class WordList(Sequence[str]):
    """Represents an sorted sequence of unique words.

    Internally the list of words is deduplicated and sorted (via ``sorted``).

    Example
    -------
    >>> wordlist = WordList(["c", "b", "a"])
    >>> wordlist
    WordList(['a', 'b', 'c'])
    >>> assert wordlist[0] == "a"
    >>> assert list(wordlist) == ["a", "b", "c"]
    >>> assert wordlist == WordList(["a", "b", "c"])

    """

    def __init__(
        self,
        words: Iterable[str] = [],
        *,
        min_word_size: int = 1,
        max_word_size: int | None = None,
        remove_leading_digits: bool = False,
    ):
        """Construct a wordlist from ``words``.

        :param words: Words to construct wordlist from.
        :param min_word_size: Filter out words which are shorter than this.
        :param max_word_size: Filter out words which are longer than this. ``None`` means
            no filtering.
        :param trim_leading_digits: Some word lists contain lines like
            ``12345  someword``. If ``True`` we just read ``someword``.
        """
        if remove_leading_digits:
            words = _remove_leading_digits(words)

        words = sorted(set(words))
        self._words: list[str] = words

        assert min_word_size > 0, "--min-word-size must be at least 1."
        assert (
            max_word_size is None or max_word_size >= min_word_size
        ), "--max-word-size must be greater or equal to --min-word-size"

        self._filter_min_word_size(min_word_size)
        self._filter_max_word_size(max_word_size)

    @overload
    def __getitem__(self, index: int) -> str: ...
    @overload
    def __getitem__(self, index: slice) -> "WordList": ...

    def __getitem__(self, index: Any) -> Any:
        """Get a word at an index or a new word list from a slice."""
        if isinstance(index, int):
            return self._words[index]
        else:
            return WordList(self._words[index])

    def __len__(self) -> int:
        """Return the number of words."""
        return len(self._words)

    def __eq__(self, other: object) -> bool:
        """Two word lists are equal if they contain the same words."""
        if not isinstance(other, WordList):
            return False
        return self._words == other._words

    @overload
    def __add__(self, other: "WordList") -> "WordList": ...
    @overload
    def __add__(self, other: list[str]) -> "WordList": ...

    def __add__(self, other: Any) -> "WordList":
        """Combine two word lists to a new word list made of the union of their words.

        If the second summand is a list of words it behaves as if this list was converted
        to a word list first.
        """
        if isinstance(other, WordList):
            return WordList(self._words + other._words)
        elif isinstance(other, list):
            return WordList(self._words + other)
        raise ValueError(f"Unsupported type {type(other)}")

    def __repr__(self) -> str:
        """Exact representation of wordlist."""
        return f"{WordList.__name__}({self._words})"

    def to_file(self, file_path: Path | str) -> None:
        """Write this wordlist to a file (overwrites if file exists)."""
        with open(file_path, mode="w") as fout:
            fout.write("\n".join(self))

    @staticmethod
    def from_file(file_path: Path | str, **options: Any) -> "WordList":
        """Create a wordlist from a file of words (newline separated).

        The ``options`` are the same as those for ``__init__``.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        assert file_path.exists(), f"Wordfile does not exist: {file_path}"

        with open(file_path) as fin:
            words = [w.strip("\n") for w in fin.readlines()]
            return WordList(words, **options)

    @staticmethod
    def from_frequency_file(
        file_path: Path | str,
        *,
        min_frequency: int = 1,
        max_frequency: int | None = None,
        **options: Any,
    ) -> "WordList":
        """Create a wordlist from a frequency file.

        We assume the following format for each line:

        LINENO TAB WORD TAB FREQUENCY

        We ignore the LINENO (digits). We are only interested in WORD (str) and FREQUENCY
        (int). Example::

            1	der	1000
            2	haus	120
            3	felsen	100
            4	foo bar-baz	100
            5	rareword	1

        Note that the three columns must be separated by tabs and that no tabs appear elsewhere.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        assert file_path.exists(), f"Frequency file does not exist: {file_path}"

        with open(file_path) as fin:
            lines = [w.strip("\n") for w in fin.readlines()]

        max_frequency_or_inf = max_frequency if max_frequency is not None else math.inf

        def filter_fn(entry: FrequencyEntry) -> bool:
            return min_frequency <= entry.frequency <= max_frequency_or_inf

        entries = [FrequencyEntry.from_line(w, i) for i, w in enumerate(lines)]
        entries = [e for e in entries if filter_fn(e)]

        return WordList([e.word for e in entries], **options)

    def _filter_min_word_size(self, min_word_size: int) -> None:
        self._words = [w for w in self._words if len(w) >= min_word_size]

    def _filter_max_word_size(self, max_word_size: int | None) -> None:
        if max_word_size is None:
            return

        self._words = [w for w in self._words if len(w) <= max_word_size]


def _remove_leading_digits(words: Iterable[str]) -> list[str]:
    return [re.sub(r"\d+\s+", "", w) for w in words]
