import click

from papass.commands import pp, pw


@click.group()
@click.help_option("--help", "-h")
@click.version_option()
def cli() -> None:
    """Create passphrases and passwords."""


cli.add_command(pp, "pp")
cli.add_command(pw, "pw")

if __name__ == "__main__":
    cli()
