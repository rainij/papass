"""A CLI to generate passphrases."""

from .phrase_generator import PhraseGenerator
from .wordlist import WordList

__version__ = "0.0.1"

__all__ = [
    PhraseGenerator.__name__,
    WordList.__name__,
]
