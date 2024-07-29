import re

import pytest
from click.testing import CliRunner
from papass.__main__ import cli

from tests.utils.mock import patch_input


@pytest.mark.parametrize("opt_help", ["--help", "-h"])
def test_help(opt_help):
    runner = CliRunner()
    result = runner.invoke(cli, ["pp", opt_help])

    assert result.exit_code == 0
    assert "Usage" in result.output


@pytest.mark.parametrize("opt_length", ["-l", "--length"])
@pytest.mark.parametrize("opt_include", ["-i", "--alpha-include"])
@pytest.mark.parametrize("opt_random_source", [None, "-r", "--randomness-source"])
def test_system_rng_simple(opt_length, opt_include, opt_random_source):
    runner = CliRunner()
    alphabet = "abcd"
    length = 13
    output_pattern = re.compile(r"^Password: [abcd]{13}\nEntropy: 26\.0$")

    random_source = [] if opt_random_source is None else [opt_random_source, "system"]

    result = runner.invoke(
        cli,
        ["pw", opt_length, str(length), opt_include, alphabet] + random_source,
    )

    assert result.exit_code == 0
    assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt_dice_sides", ["-s", "--dice-sides"])
def test_dice_rng_simple(monkeypatch, opt_dice_sides):
    runner = CliRunner()
    alphabet = "abcd"
    length = 3
    output_pattern = re.compile(r"^Password: [abcd]{3}\nEntropy: 6\.0$")

    patch_input(monkeypatch, [[1, 1], [1, 6], [6, 6]])

    result = runner.invoke(
        cli,
        ["pw", "-l", str(length), "-i", alphabet]
        + [opt_dice_sides, "6", "-r", "dice", opt_dice_sides, "6"],
    )

    assert result.exit_code == 0
    assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt", ["-e", "--alpha-exclude"])
def test_alpha_exclude(opt):
    runner = CliRunner()
    alphabet = "abcdxy"
    length = 13
    output_pattern = re.compile(r"^Password: [abcd]{13}\nEntropy: 26\.0$")

    result = runner.invoke(cli, ["pw", "-l", str(length), "-i", alphabet, opt, "xyz"])

    assert result.exit_code == 0
    assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt", ["--help-alpha-preset"])
def test_help_alpha_preset(opt):
    runner = CliRunner()
    output_pattern = re.compile(
        r"^The following names can be used with -p, --alpha-preset:"
    )

    result = runner.invoke(cli, ["pw", opt])

    assert result.exit_code == 0
    assert output_pattern.match(result.output)


@pytest.mark.parametrize("opt", ["-p", "--alpha-preset"])
@pytest.mark.parametrize("names", ["digits", "lower,digits", "letters,digits"])
def test_alpha_preset(opt, names):
    runner = CliRunner()
    length = 17
    output_pattern = re.compile(r"^Password: \w{17}\nEntropy: \d+\.\d+$")

    result = runner.invoke(cli, ["pw", "-l", str(length), opt, names])

    assert result.exit_code == 0
    assert output_pattern.match(result.output)
