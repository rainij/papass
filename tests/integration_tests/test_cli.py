import re

import pytest
from click.testing import CliRunner
from papass.__main__ import cli
from tests.utils.mock import patch_input


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert "version" in result.output


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output


@pytest.mark.parametrize("opt_count", ["-c", "--count"])
@pytest.mark.parametrize("opt_wordlist_file", ["-w", "--wordlist-file"])
@pytest.mark.parametrize("opt_random_source", [None, "-r", "--random-source"])
def test_system_rng_simple(tmp_path, opt_count, opt_wordlist_file, opt_random_source):
    runner = CliRunner()
    wordlist_name = "wordlist.txt"
    wordlist_content = "foo\nbar"
    count = 4
    output_pattern = re.compile(r"^Phrase: (foo|bar)( foo| bar){3}\nEntropy: 4\.0$")

    random_source = [] if opt_random_source is None else [opt_random_source, "system"]

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(wordlist_name, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli, [opt_count, str(count), opt_wordlist_file, wordlist_name] + random_source
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)

@pytest.mark.parametrize("opt_count", ["-c", "--count"])
@pytest.mark.parametrize("opt_wordlist_file", ["-w", "--wordlist-file"])
@pytest.mark.parametrize("opt_random_source", ["-r", "--random-source"])
def test_dice_rng_simple(monkeypatch, tmp_path, opt_count, opt_wordlist_file, opt_random_source):
    runner = CliRunner()
    wordlist_name = "wordlist.txt"
    wordlist_content = "muh\nmae\nwau\nnak"
    count = 3
    output_pattern = re.compile(r"^Phrase: \w\w\w \w\w\w \w\w\w\nEntropy: 6\.0$")

    random_source = [opt_random_source, "dice"]

    patch_input(monkeypatch, [[1, 1], [1, 6], [6, 6]])

    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open(wordlist_name, "w") as f:
            f.write(wordlist_content)

        result = runner.invoke(
            cli, [opt_count, str(count), opt_wordlist_file, wordlist_name] + random_source,
        )

        assert result.exit_code == 0
        assert output_pattern.match(result.output)


# TODO: test dice. test all options.
