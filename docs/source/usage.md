# Usage (cli)

## Installation

Install via [pipx](https://pipx.pypa.io/stable/):

```{code-block} shell
$ pipx install papass
$ # Check that it works:
$ papass --help
```

## Usage

Assuming you have a wordlist file `wordlist.txt` you can run the following command to
generate a random list of five words:

```{code-block} shell
$ papass -c 5 -w wordlist.txt
Phrase: anthem hamstring transport doorbell circle
Entropy: 64.62406251802891
```
