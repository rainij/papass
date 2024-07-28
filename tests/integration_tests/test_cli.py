import pytest
from click.testing import CliRunner
from papass.__main__ import cli


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
