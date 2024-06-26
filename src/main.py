from pathlib import Path

import click
from misc import RandomPhraseGenerator, WordList
from random_number_generator.system import SystemRng


@click.command()
@click.option(
    "--count", "-c", type=int, required=True, help="Number of words to generate."
)
@click.option(
    "--random-source", "-r", default="system", help="Source of randomness (system, dice)."
)
@click.option("--delimiter", "-d", default=" ", help="Separator between the words.")
@click.argument("wordlist")
def main(count, random_source, delimiter, wordlist):
    print(
        f"Got: count={count}, random_source={random_source}, delimiter='{delimiter}', wordlist={wordlist}."
    )

    rng = SystemRng(None)
    wordlist = WordList.from_file(
        Path(__file__).parent.parent.parent / "eff_large.wordlist", None
    )  # TODO

    gen = RandomPhraseGenerator(wordlist, rng)
    phrase = gen.get_phrase(count)

    print(phrase)


if __name__ == "__main__":
    main()
