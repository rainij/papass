# rspass

**This is a work in progress**

*rspass* generates passphrases following the
[diceware](https://theworld.com/~reinhold/diceware.html) approach as proposed by Arnold
G. Reinhold.

# Usage

```bash
$ rspass --count 7 --wordlist-file /path/to/eff_large.wordlist
Phrase: material occultist vibes departed enchanted udder occultist
Entropy: 90.47368752524046
```

# Development
Create a virtual environment and do

```bash
$ pip install -r requirements.txt -e .
$ pip install ".[dev]"
```

To run unit tests do

```bash
$ pytest
```
