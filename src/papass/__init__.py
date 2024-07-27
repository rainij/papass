"""papass is a simple library to generate passphrases.

Everything from the ``papass`` module is considered public. Everything else is considered
private.

Usage
=====

First we create two word lists:

>>> wordlist_1 = WordList(["bear", "dog", "duck"])
>>> wordlist_2 = WordList(["duck", "cat"])

Word lists implement ``Sequence``, are sorted, can be written to disk, and read from disk.

>>> wordlist = wordlist_1 + wordlist_2
>>> assert wordlist == WordList(["bear", "dog", "duck", "cat"]), "It deduplicates"
>>> assert list(wordlist) == ["bear", "cat", "dog", "duck"], "It is sorted"
>>>
>>> file_path = "/tmp/my_wordlist.txt"
>>> wordlist.to_file(file_path)
>>> assert wordlist == WordList.from_file(file_path)

Next we create a phrase generator. To do that we need a random source. Here we take the
systems most secure random source for simplicity but you can also take the one which
requires physical dice to be thrown.

>>> rng = SystemRng()
>>> rpg = PhraseGenerator(wordlist=wordlist, rng=rng, delimiter=" ")

This can now be used to create a random phrase:

>>> num_words = 5
>>> rpg.get_phrase(num_words)
RpgResult(phrase=..., entropy=10.0, entropy_is_guaranteed=True)

The actual ``phrase`` is random of course. It could be something like ``'dog duck cat duck
duck'``. The ``entropy`` is ``10.0`` in this example because there are ``2**10==4**5``
possible phrases made up from ``5`` words with ``4`` possibilities each.

The ``entropy_is_guaranteed=True`` tells us that the entropy is indeed not lower than
expected. Note that in principle it might be possible that there are less possible phrases
if e.g. you choose ``''`` (empty string) as the delimiter and some words contain some of
the other words.

Consider for example the wordlist ``foo bar foobar barfoo`` with ``num_words=5``. Then
``foobarfoo`` can come from ``foobar, foo`` or from ``foo, barfoo``.

If ``entropy_is_guaranteed=False`` this doesn't necessarily mean that the entropy is lower
(and even `if`, it is probably not much lower). The check relies on a simple heuristic
which has the property that ``True`` is always correct and ``False`` basically means
`don't know`.
"""

from .phrase_generator import PhraseGenerator, RpgResult
from .random import DiceRng, RandomNumberGeneratorBase, SystemRng
from .wordlist import WordList

__version__ = "0.0.4"

__all__ = [
    DiceRng.__name__,
    PhraseGenerator.__name__,
    RandomNumberGeneratorBase.__name__,
    RpgResult.__name__,
    SystemRng.__name__,
    WordList.__name__,
]
