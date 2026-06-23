from click.testing import CliRunner

from chatqiniu.cli import main


def test_add_list_show_and_remove_commands(tmp_path):
    registry = tmp_path / "apps.json"
    runner = CliRunner()

    add_result = runner.invoke(
        main,
        [
            "add",
            "demo",
            "--endpoint",
            "https://demo.example.com",
            "--title",
            "Demo App",
            "--registry",
            str(registry),
        ],
    )
    assert add_result.exit_code == 0, add_result.output
    assert "Saved demo" in add_result.output

    list_result = runner.invoke(main, ["list", "--registry", str(registry)])
    assert list_result.exit_code == 0, list_result.output
    assert "demo (Demo App): https://demo.example.com" in list_result.output

    show_result = runner.invoke(main, ["show", "demo", "--registry", str(registry)])
    assert show_result.exit_code == 0, show_result.output
    assert "endpoint: https://demo.example.com" in show_result.output

    remove_result = runner.invoke(main, ["remove", "demo", "--registry", str(registry)])
    assert remove_result.exit_code == 0, remove_result.output
    assert "Removed demo" in remove_result.output

    empty_result = runner.invoke(main, ["list", "--registry", str(registry)])
    assert empty_result.exit_code == 0, empty_result.output
    assert "No apps configured." in empty_result.output


def test_missing_required_input_fails_fast_with_non_interactive_flag(tmp_path):
    runner = CliRunner()

    result = runner.invoke(main, ["add", "demo", "--registry", str(tmp_path / "apps.json"), "-I"])

    assert result.exit_code != 0
    assert "endpoint" in result.output.lower()
