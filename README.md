<h1 align="center">
  papass
</h1>

[![PyPI](https://img.shields.io/pypi/v/papass.svg)](https://pypi.org/project/papass/)
[![Documentation Status](https://readthedocs.org/projects/papass/badge/?version=latest)](https://papass.readthedocs.io/en/latest)
[![CI](https://github.com/rainij/papass/actions/workflows/ci.yml/badge.svg)](https://github.com/rainij/papass/actions/workflows/ci.yml)

**papass** generates passphrases following the
[diceware](https://theworld.com/~reinhold/diceware.html) approach as proposed by Arnold
G. Reinhold.

# Quickstart

Assuming you have a wordlist file `wordlist.txt` ([where to get
one](https://papass.readthedocs.io/en/stable/usage_cli.html#where-to-get-wordlist)) you
can run the following command to generate a random list of four words:

```{code} console
$ papass pp -l 4 -w wordlist.txt
Passphrase: grimy street acetone overcast
Entropy: 51.6993
```

By default this uses the system's most secure random number generator. To use physical
dice add `-r dice`. The number of dice rolls can become very high so for convenience you
can enter the rolls in groups as in the following example:

```{code} console
$ papass pp -l 4 -w wordlist.txt -r dice
Roll 20 dice: 5 1 3 5 1
Roll remaining 15 dice: 4 6 4 6 2
Roll remaining 10 dice: 5 6 2 3 6
Roll remaining 5 dice: 6 5 2 2 4
Passphrase: renegade reapprove static uphold
Entropy: 51.6993
```

Passwords can be created too (can also be used with `-r dice`):

```{code} console
$ papass pw -l 20 -p letters,digits
Password: rXJndFnML2j3YqVo2WgF
Entropy: 119.084
```

See [papass.readthedocs.io](https://papass.readthedocs.io) for the full documentation.

# Development
Create a virtual environment (e.g. via `python -m venv .myvenv` or
[mamba/micromamba](https://mamba.readthedocs.io)). Install (development) dependencies and
`papass` in editable mode:

```{code} console
$ pip install -r requirements.txt -e .
```

Run tests and type checking via

```{code} console
$ pytest
$ mypy .
```

Formatting and linting is done via [ruff](https://github.com/astral-sh/ruff).

```{code} console
$ ruff format
$ ruff check --fix
```

To build the docs install e.g. [make](https://www.gnu.org/software/make/) and do

```{code} console
$ pip install -r docs/requirements.txt
$ make -C docs/ html
```
