from pathlib import Path

import click

from papass import (
    PassphraseGenerator,
    PasswordGenerator,
    WordList,
)
from papass.alphabet import (
    alphabet_from_preset,
    alphabet_preset_base,
    alphabet_preset_shortcuts,
)
from papass.random_source import (
    available_randomness_sources_str,
    default_randomness_source,
    get_rng,
)

RESULT_BG_COLOR = (0, 44, 77)


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "--length",
    "-l",
    type=int,
    required=True,
    help="Number of words to generate.",
)
@click.option(
    "--randomness-source",
    "-r",
    default=f"{default_randomness_source()}",
    help=f"Source of randomness (default: '{default_randomness_source()}',"
    f" available: {available_randomness_sources_str()}).",
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
    "-s",
    type=int,
    default=6,
    help="Number of sides of dice (default: 6).",
)
@click.option(
    "--remove-leading-digits",
    "--rld",
    is_flag=True,
    help="If wordlist contains entries like `123 foo` normalizes it to `foo`.",
)
def pp(
    length: int,
    randomness_source: str,
    wordlist_file: str,
    delimiter: str,
    min_word_size: int,
    max_word_size: int,
    dice_sides: int,
    remove_leading_digits: bool,
) -> None:
    """Create a passphrase.

    \b
    Example:
    \b
    $ papass pp -l 4 -w wordlist.txt
    Passphrase: gents backed marvelous mounting
    Entropy: 51.6993
    """

    try:
        rng = get_rng(randomness_source, dice_sides=dice_sides)

        wordlist = WordList.from_file(
            Path(wordlist_file),
            min_word_size=min_word_size,
            max_word_size=max_word_size,
            remove_leading_digits=remove_leading_digits,
        )

        passphrase_generator = PassphraseGenerator(
            wordlist=wordlist, rng=rng, delimiter=delimiter
        )
        result = passphrase_generator.generate(length)
    except AssertionError as error:
        click.secho(f"ERROR: {error}", fg="red")
        click.echo("Try again!")
        return

    passphrase = click.style(result.passphrase, bg=RESULT_BG_COLOR)

    click.echo(f"Passphrase: {passphrase}")
    click.echo(f"Entropy: {result.entropy:.6}")

    if not result.entropy_is_guaranteed:
        click.secho(
            "WARNING: Entropy might be slightly lower than estimated. "
            "See https://papass.readthedocs.io/en/stable/usage_cli.html#entropy-guarantee.",
            fg="yellow",
        )


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "--length",
    "-l",
    type=int,
    help="Number of characters the password should contain.",
)
@click.option(
    "--randomness-source",
    "-r",
    default=f"{default_randomness_source()}",
    help=f"Source of randomness (default: '{default_randomness_source()}',"
    f" available: {available_randomness_sources_str()}).",
)
@click.option(
    "--dice-sides",
    "-s",
    type=int,
    default=6,
    help="Number of sides of dice (default: 6).",
)
@click.option(
    "--alpha-include", "-i", help="Include these characters for password generation."
)
@click.option(
    "--alpha-preset",
    "-p",
    help="Comma separated list of pre-defined character sets. See also --help-alpha-preset.",
)
@click.option(
    "--alpha-exclude", "-e", help="Exclude these characters for password generation."
)
@click.option(
    "--help-alpha-preset",
    is_flag=True,
    help="Show available --alpha-preset names and exit.",
)
def pw(
    length: int,
    randomness_source: str,
    dice_sides: int,
    alpha_include: str,
    alpha_preset: str,
    alpha_exclude: str,
    help_alpha_preset: bool,
) -> None:
    """Create a password.

    \b
    Example:
    \b
    $ papass pw -l 20 -p letters,digits
    Password: UOytQY57pcUldprI7LYL
    Entropy: 119.084

    NOTE: You can use all --alpha-* options simultaneously.
    """

    if help_alpha_preset:
        print_alpha_preset()
        return

    try:
        assert length is not None, "Missing option --length."
        alpha: str = alpha_include or ""

        if alpha_preset:
            alpha += alphabet_from_preset(alpha_preset.split(","))

        if alpha_exclude:
            alpha = "".join(c for c in alpha if c not in alpha_exclude)

        assert alpha, "No alphabet given. Did you forget --alphabet or alphabet-names?"

        rng = get_rng(randomness_source, dice_sides=dice_sides)
        password_generator = PasswordGenerator(rng=rng, alphabet=alpha)
        result = password_generator.generate(length)
    except AssertionError as error:
        click.secho(f"ERROR: {error}", fg="red")
        click.echo("Try again!")
        return

    password = click.style(result.password, bg=RESULT_BG_COLOR)

    click.echo(f"Password: {password}")
    click.echo(f"Entropy: {result.entropy:.6}")


def print_alpha_preset() -> None:
    base = {
        k: click.style(v, bg=RESULT_BG_COLOR) for k, v in alphabet_preset_base().items()
    }
    shortcuts = {k: ",".join(v) for k, v in alphabet_preset_shortcuts().items()}

    click.echo("The following names can be used with -p, --alpha-preset:")
    click.echo("\n".join(f"{name:9}: {alpha}" for name, alpha in base.items()))

    click.echo("\nIn addition the following shortcuts can be used:")
    click.echo("\n".join(f"{short:9}: {names}" for short, names in shortcuts.items()))

    click.echo("\nExample: -p letters,digits")
