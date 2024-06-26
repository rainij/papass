from pathlib import Path

import click
from phrase_generator import RandomPhraseGenerator
from random_number_generator.system import SystemRng
from wordlist import WordList


@click.command()
@click.option(
    "--count", "-c", type=int, required=True, help="Number of words to generate."
)
@click.option(
    "--random-source", "-r", default="system", help="Source of randomness (system, dice)."
)
@click.option("--delimiter", "-d", default=" ", help="Separator between the words.")
@click.option(
    "--min-word-size",
    "--minw",
    type=int,
    default=1,
    help="Filter out words which are shorter than this.",
)
@click.option(
    "--max-word-size",
    "--maxw",
    type=int,
    help="Filter out words which are longer than this.",
)
@click.argument("wordlist")
def main(count, random_source, delimiter, min_word_size, max_word_size, wordlist):
    """Create a passphrase"""

    rng = SystemRng(None)

    wordlist = WordList.from_file(
        Path(__file__).parent.parent.parent / "eff_large.wordlist",  # TODO
        min_word_size=min_word_size,
        max_word_size=max_word_size,
    )

    print(f"Wordlist size: {len(wordlist)}")

    gen = RandomPhraseGenerator(wordlist, rng)
    phrase = gen.get_phrase(count)

    print(phrase)


if __name__ == "__main__":
    main()
