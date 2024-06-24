import click


@click.command()
@click.option("--count", "-c", type=int, help="Number of words to generate.")
def main(count):
    print(f"Got: count={count}")


if __name__ == "__main__":
    main()
