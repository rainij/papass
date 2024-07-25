<h1 align="center">
  papass
</h1>

[![PyPI](https://img.shields.io/pypi/v/papass.svg)](https://pypi.org/project/papass/)
[![Documentation Status](https://readthedocs.org/projects/papass/badge/?version=latest)](https://papass.readthedocs.io/en/latest)
[![CI](https://github.com/rainij/papass/actions/workflows/ci.yml/badge.svg)](https://github.com/rainij/papass/actions/workflows/ci.yml)

**This is a work in progress**

**papass** generates passphrases following the
[diceware](https://theworld.com/~reinhold/diceware.html) approach as proposed by Arnold
G. Reinhold.

# Quickstart

Assuming you have a wordlist file `wordlist.txt` you can run the following command to
generate a random list of four words:

```shell
$ papass -c 4 -w wordlist.txt
Phrase: grimy street acetone overcast
Entropy: 51.6993
```

By default this uses the system's most secure random number generator. To use physical
dice add `-r dice`. See [papass.readthedocs.io](https://papass.readthedocs.io) for the
full documentation.

# Development
Create a virtual environment (e.g. via `python -m venv` or
[mamba/micromamba](https://mamba.readthedocs.io)). Install (development) dependencies and
`papass` in editable mode:

```shell
$ pip install -r requirements.txt -e .
```

Run unit tests via

```shell
$ pytest
```

Formatting and linting is done via [ruff](https://github.com/astral-sh/ruff).

```shell
$ ruff format
$ ruff check --fix
```

To build the docs install e.g. [make](https://www.gnu.org/software/make/) and do

```shell
$ pip install -r docs/requirements.txt
$ make -C docs/ html
```
