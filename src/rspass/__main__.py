from pathlib import Path

import click

from rspass.phrase_generator import PhraseGenerator
from rspass.random import (
    available_random_sources,
    default_random_source,
    get_rng,
)
from rspass.wordlist import WordList


@click.command()
@click.option(
    "--count",
    "-c",
    type=int,
    required=True,
    help="Number of words to generate.",
)
@click.option(
    "--random-source",
    "-r",
    default=f"{default_random_source()}",
    help=f"Source of randomness (default: '{default_random_source()}',"
    f" available: {', '.join(f'\'{s}\'' for s in available_random_sources())}).",
)
@click.option(
    "--wordlist-file",
    "-w",
    required=True,
    help="A file with a new-line-separated list of words.",
)
@click.option(
    "--delimiter",
    "-d",
    default=" ",
    help="Separator between the words (default: ' ').",
)
@click.option(
    "--min-word-size",
    "--minw",
    type=int,
    default=1,
    help="Filter out words which are shorter than this (default: 1).",
)
@click.option(
    "--max-word-size",
    "--maxw",
    type=int,
    help="Filter out words which are longer than this (default: no limit).",
)
@click.option(
    "--dice-sides",
    "--ds",
    type=int,
    default=6,
    help="Number of sides of dice (default: 6).",
)
def cli(
    count,
    random_source,
    wordlist_file,
    delimiter,
    min_word_size,
    max_word_size,
    dice_sides,
):
    """Create a passphrase."""

    rng = get_rng(random_source, dice_sides=dice_sides)

    wordlist = WordList.from_file(
        Path(wordlist_file),
        min_word_size=min_word_size,
        max_word_size=max_word_size,
    )

    phrase_generator = PhraseGenerator(
        wordlist=wordlist, rng=rng, delimiter=delimiter
    )
    result = phrase_generator.get_phrase(count)

    print(f"Phrase: {result.phrase}")
    print(f"Entropy: {result.entropy}")


if __name__ == "__main__":
    cli()