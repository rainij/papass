from pathlib import Path

import click
from phrase_generator import RandomPhraseGenerator
from random_number_generator import available_rngs, get_rng
from wordlist import WordList


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
    default="system",
    help=f"Source of randomness ({', '.join(available_rngs())}).",
)
@click.option(
    "--delimiter",
    "-d",
    default=" ",
    help="Separator between the words.",
)
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
@click.option(
    "--dice-sides",
    "--ds",
    type=int,
    default=6,
    help="Number of sides of dice used.",
)
@click.argument("wordlist")
def main(
    count, random_source, delimiter, min_word_size, max_word_size, dice_sides, wordlist
):
    """Create a passphrase"""

    rng = get_rng(random_source, dice_sides=dice_sides)

    wordlist = WordList.from_file(
        Path(__file__).parent.parent.parent / "eff_large.wordlist",  # TODO
        min_word_size=min_word_size,
        max_word_size=max_word_size,
    )

    print(f"Wordlist size: {len(wordlist)}")

    phrase_generator = RandomPhraseGenerator(wordlist, rng, delimiter=delimiter)
    phrase = phrase_generator.get_phrase(count)

    print(phrase)


if __name__ == "__main__":
    main()
