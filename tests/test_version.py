from click.testing import CliRunner

from chatqiniu import __version__
from chatqiniu.cli import main


def test_version_present():
    assert __version__ == "0.2.1"


def test_cli_version_option_prints_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output
