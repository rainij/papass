# Usage

`papass` primarily is a command line tool. For usage as a library or from within an
interactive python or [ipython](https://ipython.org/) session look into the [API
documentation](./api.rst).

## Installation

Install via [pipx](https://pipx.pypa.io/stable/):

```{code-block} console
$ pipx install papass
$ # Check that it works:
$ papass --help
...
```

## Usage

Assuming you have a wordlist file `wordlist.txt` like this one

```
abacus
abdomen
abdominal
abide
...
```

you can run the following command to quickly generate a random list of four words:

```{code-block} console
$ papass -c 4 -w ../eff_large.wordlist
Phrase: grimy street acetone overcast
Entropy: 51.6993
```

You can use several wordlist in which case the wordlists are merged and deduplicated. To
use **physical dice** use the ``-r dice`` option. In this example you have to roll five
dice four times:

```{code-block} console
$ papass -c 4 -w wordlist.txt -r dice
Roll at least 5 dice: 1 6 3 4 4
Roll at least 5 dice: 4 1 1 2 5
Roll at least 5 dice: 3 1 2 1 4
Roll at least 5 dice: 4 4 1 3 6
Phrase: colossal math fleshed payday
Entropy: 51.6993
```

In contrast to some other similar tools the number of words in the wordlist does not need
to be a power of six (or the number of sides of the dice). Some tools also allow this but
at the cost of truncating the word list and hence loosing entropy. ``papass`` on the other
hand uses all the words, but at the cost of rejecting some of the rolls (**rejection
sampling**). This is necessary to obtain a uniform distribution on the words. This looks
like this:

```{code-block} console
$ papass -c 4 -w wordlist.txt -r dice
Roll at least 5 dice: 6 6 6 6 6
Rejected. Try again!
Roll at least 5 dice: ...
```

This never happens if the number of words is actually a power of six. In all other cases
the tool chooses the number of rolls in a way so that this does not happen too often.

## Where to get wordlists

You can download a wordlist designed for passphrases from the
[EFF](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases). You might
need to remove the dice numbers, that is, change a line like this

```
11114     abide
```

into

```
abide
```
