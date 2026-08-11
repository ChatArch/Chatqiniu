from click.testing import CliRunner

from chatqiniu.cli import main


def test_help_lists_tree_and_real_groups_without_template_hello():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "--tree" in result.output
    assert "auth" in result.output
    assert "object" in result.output
    assert "cert" in result.output
    assert "domain" in result.output
    assert "hello" not in result.output.lower()


def test_tree_option_renders_registered_command_surface_without_template_hello():
    result = CliRunner().invoke(main, ["--tree"])

    assert result.exit_code == 0, result.output
    assert "chatqiniu #" in result.output
    assert "--help" in result.output
    assert "--version" in result.output
    assert "--tree" in result.output
    assert "auth # Credential bootstrap" in result.output
    assert "login" in result.output
    assert "object # Manage Kodo objects" in result.output
    assert "upload-dir" in result.output
    assert "cert # Inspect and manage CDN certificates" in result.output
    assert "deploy" in result.output
    assert "domain # Inspect CDN domains and HTTPS config" in result.output
    assert "https # Manage domain HTTPS configuration" in result.output
    assert "set" in result.output
    assert "hello" not in result.output.lower()
