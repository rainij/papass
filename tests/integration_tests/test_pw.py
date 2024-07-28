import pytest
from click.testing import CliRunner
from papass.__main__ import cli


@pytest.mark.parametrize("opt_help", ["--help", "-h"])
def test_help(opt_help):
    runner = CliRunner()
    result = runner.invoke(cli, ["pp", opt_help])

    assert result.exit_code == 0
    assert "Usage" in result.output
