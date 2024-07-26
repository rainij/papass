# User Guide

`papass` primarily is a command line tool. For usage as a library or from within an
interactive python or [ipython](https://ipython.org/) session look into the [API
Reference](./api.rst).

## Installation

Install via [pipx](https://pipx.pypa.io/stable/):

```{code-block} console
$ pipx install papass
```

Check that it works:

```{code-block} console
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

```{code} console
$ papass -c 4 -w wordlist.txt
Phrase: grimy street acetone overcast
Entropy: 51.6993
```

You can use several wordlists in which case the wordlists are merged and deduplicated. To
use **physical dice** use the ``-r dice`` option.

In the following example you have to roll five dice four times:

```{code} console
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

```{code} console
$ papass -c 4 -w wordlist.txt -r dice
Roll at least 5 dice: 6 6 6 6 6
Rejected. Try again!
Roll at least 5 dice: ...
```

This never happens if the number of words is actually a power of six. In all other cases
the tool chooses the number of rolls in a way so that this does not happen too often.

## Where to get wordlists from

You can download a wordlist designed for passphrases from the
[EFF](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases). You might
need to use the flag `--remove-leading-digits` in order to ignore the leading digits in
the file

```
11111   abacus
11112   abdomen
11113   abdominal
11114   abide
...
```

## On the entropy

The entropy is a measure on how save your passphrase is. In our case the entropy {math}`H`
can be computed as

```{math}
H = \log_2(N^k)
```

were {math}`N` is the size of the word list and {math}`k` is the number of generated
words. Note that {math}`N^k` is the number of possible passphrases and hence a cracker
would need to try around {math}`N^k/2` passphrases to find your passphrase by a
brute-force approach (assuming they know which wordlist you used).

{#entropy-guarantee}
Note that in general the above formula can overestimate the real entropy which should be
more precisely defined as

```{math}
H = \log_2(M)
```

where {math}`M` is the number of possible passphrases. To see why {math}`M<N^k` can happen
consider the case of an empty delimiter and a wordlist containing the words

```
foo
bar
foobar
barfoo
```

A possible 2-word phrase would be `foobarfoo`. But this one can be obtained in two ways:
Either from `foobar` and `foo` or else from `foo` and `barfoo`. `papass` warns you if
something like this *could* happen:

```{code} console
$ papass -c 2 -w wordlist.txt -r system -d ""
Phrase: foobarfoo
Entropy: ...
WARNING: Entropy might be slightly lower than estimated. See https://papass.readthedocs.io/en/stable/usage_cli.html#entropy-guarantee.
```

Note that this uses just a simple heuristic which is biased in the following sense

- If the warning does not appear the entropy estimate is correct.
- If the warning appears the entropy can still be correct. The tool just wasn't able to prove that.

In practice however the entropy decrease should be small. The warning exists for the paranoid 😉.
