from click.testing import CliRunner
from chatstyle import render_click_tree

from chatqiniu.cli import main


def test_help_lists_shared_tree_options_and_real_groups():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "--tree" in result.output
    assert "--tree-brief" in result.output
    assert "auth" in result.output
    assert "object" in result.output
    assert "cert" in result.output
    assert "domain" in result.output
    assert "hello" not in result.output.lower()


def test_tree_option_renders_registered_command_surface_with_signatures():
    result = CliRunner().invoke(main, ["--tree"])

    assert result.exit_code == 0, result.output
    assert result.output == render_click_tree(main, root_name="chatqiniu") + "\n"
    assert result.output.splitlines().count("chatqiniu") == 1
    assert "├── --tree-brief" in result.output
    assert "login [--access-key ACCESS-KEY]" in result.output
    assert "upload-dir [LOCAL-DIR]" in result.output
    assert "deploy [--name NAME]" in result.output
    assert "https  # Manage domain HTTPS bindings" in result.output
    assert "set [DOMAIN]" in result.output
    assert "writes remote storage" in result.output
    assert "treat the output as sensitive" in result.output
    assert "hello" not in result.output.lower()


def test_tree_brief_keeps_nodes_and_descriptions_but_omits_signatures():
    full = CliRunner().invoke(main, ["--tree"])
    brief = CliRunner().invoke(main, ["--tree-brief"])

    assert full.exit_code == 0, full.output
    assert brief.exit_code == 0, brief.output
    assert brief.output == render_click_tree(main, root_name="chatqiniu", brief=True) + "\n"
    assert brief.output.splitlines().count("chatqiniu") == 1
    for description in (
        "Manage credentials and run masked read-only identity checks.",
        "Read and mutate Kodo objects; destructive commands preview by default.",
        "Read and mutate CDN certificates; writes preview by default.",
        "Inspect domains and manage HTTPS; writes preview by default.",
    ):
        assert description in full.output
        assert description in brief.output
    assert "[--access-key ACCESS-KEY]" in full.output
    assert "[LOCAL-DIR]" in full.output
    assert "[DOMAIN]" in full.output
    assert "[--access-key ACCESS-KEY]" not in brief.output
    assert "[LOCAL-DIR]" not in brief.output
    assert "[DOMAIN]" not in brief.output


def test_tree_root_uses_public_console_command_in_module_mode():
    result = CliRunner().invoke(main, ["--tree"], prog_name="python -m chatqiniu.cli")

    assert result.exit_code == 0, result.output
    assert result.output.splitlines()[0] == "chatqiniu"
    assert "python -m chatqiniu.cli" not in result.output
