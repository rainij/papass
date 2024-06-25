import click
from misc import RandomNumberGenerator, WordList, RandomPhraseGenerator


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

    rng = RandomNumberGenerator(None)
    wordlist = WordList(["foo", "bar", "baz"], None)

    gen = RandomPhraseGenerator(wordlist, rng)
    phrase = gen.get(count)

    print(phrase)


if __name__ == "__main__":
    main()
