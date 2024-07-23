# Usage

`papass` primarily is a command line tool. For usage as a library look into the [API
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

Assuming you have a wordlist file `wordlist.txt` you can run the following command to
generate a random list of five words:

```{code-block} console
$ papass -c 5 -w wordlist.txt
Phrase: anthem hamstring transport doorbell circle
Entropy: 64.62406251802891
```

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
