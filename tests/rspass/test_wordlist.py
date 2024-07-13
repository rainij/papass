import pytest
from papass.wordlist import WordList

# TODOs:
# - test error handling?
# - test logging?


def test_initializes():
    words = ["hallo", "welt"]
    WordList(words)


class TestInterface:
    @pytest.fixture
    def words(self) -> list[str]:
        return ["e", "b", "c", "d", "a"]

    @pytest.fixture()
    def wordlist(self, words) -> WordList:
        return WordList(words)

    def test_test_setup(self, words):
        """We assume that the `words` are *not* sorted."""
        assert len(words) >= 5
        assert words != sorted(words)

    def test_len(self, wordlist, words):
        assert len(wordlist) == len(words)

    @pytest.mark.parametrize("i", range(3))
    def test_getitem(self, i, wordlist, words):
        words = sorted(words)
        assert wordlist[i] == words[i]
        assert wordlist[-i] == words[-i]

    @pytest.mark.parametrize("other", ["abcde", "edcba", "aedbc"])
    def test_eq(self, wordlist, other: str):
        """Two wordlists are equal if they contain the same words (like a set)."""
        assert wordlist == WordList(list(other))

    @pytest.mark.parametrize("other", ["ab", "abcdef"])
    def test_ne_1(self, wordlist, other):
        assert wordlist != WordList(list(other))

    @pytest.mark.parametrize("other", [42, "abcde", list("abcde")])
    def test_ne_2(self, wordlist, other):
        assert wordlist != other

    def test_repr(self, wordlist):
        """There is a canonical __repr__ due to sorting of the words."""
        assert f"{wordlist}" == "WordList(['a', 'b', 'c', 'd', 'e'])"

    def test_from_file(self, tmp_path, words, wordlist):
        file_path = tmp_path / "test.wordlist"

        with open(file_path, "w") as fin:
            for word in words:
                fin.write(f"{word}\n")

        wordlist_from_file = WordList.from_file(file_path)
        assert wordlist_from_file == wordlist


class TestWordSize:
    @pytest.fixture
    def words(self) -> list[str]:
        return ["a", "ab", "abc", "abcd", "abcde"]

    def test_test_setup(self, words):
        """We assume that `words` is sorted and that words[i] has length i+1."""
        assert len(words) >= 5
        assert words == sorted(words)

        for i, w in enumerate(words):
            assert len(w) == i + 1

    @pytest.mark.parametrize(
        "min_word_size,max_word_size",
        [
            (1, None),
            (1, 3),
            (2, None),
            (3, 4),
        ],
    )
    def test_min_max_word_size(self, words, min_word_size, max_word_size):
        options = dict(
            min_word_size=min_word_size,
            max_word_size=max_word_size,
        )

        max_word_size = max_word_size or len(words)

        wordlist = WordList(words, **options)
        assert wordlist == WordList(words[min_word_size - 1 : max_word_size])
