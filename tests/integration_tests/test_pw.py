import re

import pytest
from click.testing import CliRunner
from papass.__main__ import cli


@pytest.mark.parametrize("opt_help", ["--help", "-h"])
def test_help(opt_help):
    runner = CliRunner()
    result = runner.invoke(cli, ["pp", opt_help])

    assert result.exit_code == 0
    assert "Usage" in result.output


@pytest.mark.parametrize("opt_length", ["-l", "--length"])
@pytest.mark.parametrize("opt_alphabet", ["-a", "--alphabet"])
@pytest.mark.parametrize("opt_random_source", [None, "-r", "--randomness-source"])
def test_system_rng_simple(tmp_path, opt_length, opt_alphabet, opt_random_source):
    runner = CliRunner()
    alphabet = "abcd"
    length = 13
    output_pattern = re.compile(r"^Password: [abcd]{13}\nEntropy: 26\.0$")

    random_source = [] if opt_random_source is None else [opt_random_source, "system"]

    result = runner.invoke(
        cli,
        ["pw", opt_length, str(length), opt_alphabet, alphabet] + random_source,
    )

    assert result.exit_code == 0
    assert output_pattern.match(result.output)
