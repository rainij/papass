import click


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
    print(f"Got: count={count}, random_source={random_source}, delimiter='{delimiter}', wordlist={wordlist}.")


if __name__ == "__main__":
    main()
