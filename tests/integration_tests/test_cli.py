import re

import pytest
from click.testing import CliRunner
from papass.__main__ import cli

from tests.utils.mock import patch_input

WORDLIST_NAME = "wordlist.txt"


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.parametrize("opt_help", ["--help", "-h"])
def test_help(opt_help):
    runner = CliRunner()
    result = runner.invoke(cli, [opt_help])

    assert result.exit_code == 0
    assert "Usage" in result.output


@pytest.mark.parametrize("opt_count", ["-c", "--count"])
@pytest.mark.parametrize("opt_wordlist_file", ["-w", "--wordlist-file"])
@pytest.mark.parametrize("opt_random_source", [None, "-r", "--random-source"])
def test_system_rng_simple(tmp_path, opt_count, opt_wordlist_file, opt_random_source):
    runner = CliRunner()
    wordlist_content = "foo\nbar"
    count = 4
    output_pattern = re.compile(r"^Phrase: (foo|bar)( foo| bar){3}\nEntropy: 4\.0$")

    random_source = [] if opt_random_source is None else [opt_random_source, "system"]

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(WORDLIST_NAME, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli, [opt_count, str(count), opt_wordlist_file, WORDLIST_NAME] + random_source
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt_count", ["-c", "--count"])
@pytest.mark.parametrize("opt_wordlist_file", ["-w", "--wordlist-file"])
@pytest.mark.parametrize("opt_random_source", ["-r", "--random-source"])
def test_dice_rng_simple(
    monkeypatch, tmp_path, opt_count, opt_wordlist_file, opt_random_source
):
    runner = CliRunner()
    wordlist_content = "muh\nmae\nwau\nnak"
    count = 3
    output_pattern = re.compile(r"^Phrase: \w\w\w \w\w\w \w\w\w\nEntropy: 6\.0$")

    random_source = [opt_random_source, "dice"]

    patch_input(monkeypatch, [[1, 1], [1, 6], [6, 6]])

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(WORDLIST_NAME, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli,
            [opt_count, str(count), opt_wordlist_file, WORDLIST_NAME] + random_source,
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt_delimiter", ["-d", "--delimiter"])
@pytest.mark.parametrize("delimiter", ["@", "#"])
def test_delimiter(tmp_path, opt_delimiter, delimiter):
    runner = CliRunner()
    # whitespace intentional:
    wordlist_content = " foo\n bar"
    count = 2
    output_pattern = re.compile(
        rf"^Phrase: ( foo| bar){delimiter}( foo| bar)\nEntropy: 2\.0\n"
    )

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(WORDLIST_NAME, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli, ["-c", str(count), "-w", WORDLIST_NAME, opt_delimiter, delimiter]
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt_min_word_size", ["--minw", "--min-word-size"])
def test_min_word_size(tmp_path, opt_min_word_size):
    runner = CliRunner()
    wordlist_content = "fo\nfoo"
    count = 2
    output_pattern = re.compile(r"^Phrase: foo foo\nEntropy: 0\.0$")

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(WORDLIST_NAME, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli, ["-c", str(count), "-w", WORDLIST_NAME, opt_min_word_size, "3"]
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt_max_word_size", ["--maxw", "--max-word-size"])
def test_max_word_size(tmp_path, opt_max_word_size):
    runner = CliRunner()
    wordlist_content = "fooo\nfoo"
    count = 2
    output_pattern = re.compile(r"^Phrase: foo foo\nEntropy: 0\.0$")

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(WORDLIST_NAME, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli, ["-c", str(count), "-w", WORDLIST_NAME, opt_max_word_size, "3"]
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt_remove", ["--remove-leading-digits"])
def test_remove_leading_digits(tmp_path, opt_remove):
    runner = CliRunner()
    wordlist_content = "123 foo\nbar"
    count = 1
    output_pattern = re.compile(r"^Phrase: (foo|bar)\nEntropy: 1\.0$")

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(WORDLIST_NAME, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(cli, ["-c", str(count), "-w", WORDLIST_NAME, opt_remove])

        assert result.exit_code == 0
        assert output_pattern.match(result.output)
