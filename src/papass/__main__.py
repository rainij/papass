import click

from papass.commands import pp


@click.group()
def cli():
    "Create passphrases and passwords."
    pass


cli.add_command(pp, "pp")

if __name__ == "__main__":
    cli()
