from pathlib import Path

from click.testing import CliRunner

import chatqiniu.cli as cli_module
from chatqiniu.client import DryRunResult
from chatqiniu.cli import main
from chatqiniu.config import QiniuSettings


class FakeObjectClient:
    def object_delete(self, **kwargs):
        return DryRunResult("object delete", (f"key={kwargs['key']}",))


class FakeFusionClient:
    def cert_list(self, **kwargs):
        return {"certs": [{"certID": "cert-1", "name": "demo-cert"}]}

    def domain_https_set(self, **kwargs):
        return DryRunResult("domain https set", (f"certId={kwargs['cert_id']}",))


def test_main_help_lists_expected_groups():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "auth" in result.output
    assert "object" in result.output
    assert "cert" in result.output
    assert "domain" in result.output


def test_docs_links_prints_official_links():
    result = CliRunner().invoke(main, ["docs", "links"])

    assert result.exit_code == 0
    assert "developer-center" in result.output
    assert "developer.qiniu.com" in result.output


def test_auth_login_saves_credentials(monkeypatch, tmp_path):
    saved = {}

    def fake_save(values, profile=None, home=None):
        saved["values"] = values
        saved["profile"] = profile
        return tmp_path / ".chatarch" / "envs" / "Qiniu" / ".env"

    monkeypatch.setattr(cli_module, "save_settings", fake_save)
    result = CliRunner().invoke(
        main,
        [
            "auth",
            "login",
            "--access-key",
            "AK_TEST",
            "--secret-key",
            "SK_TEST",
            "--profile",
            "work",
            "-I",
        ],
    )

    assert result.exit_code == 0
    assert saved["profile"] == "work"
    assert saved["values"]["QINIU_ACCESS_KEY"] == "AK_TEST"
    assert saved["values"]["QINIU_SECRET_KEY"] == "SK_TEST"


def test_object_delete_defaults_to_dry_run(monkeypatch):
    monkeypatch.setattr(cli_module, "_get_settings", lambda profile=None: QiniuSettings(bucket_name="demo"))
    monkeypatch.setattr(cli_module, "_client", lambda profile=None: FakeObjectClient())

    result = CliRunner().invoke(main, ["object", "delete", "demo.txt", "-I"])

    assert result.exit_code == 0
    assert "Dry run" in result.output
    assert "demo.txt" in result.output


def test_cert_list_renders_fake_response(monkeypatch):
    monkeypatch.setattr(cli_module, "_fusion_client", lambda profile=None: FakeFusionClient())

    result = CliRunner().invoke(main, ["cert", "list"])

    assert result.exit_code == 0
    assert "demo-cert" in result.output


def test_domain_https_set_defaults_to_dry_run(monkeypatch):
    monkeypatch.setattr(cli_module, "_fusion_client", lambda profile=None: FakeFusionClient())

    result = CliRunner().invoke(main, ["domain", "https", "set", "cdn.example.com", "--cert-id", "cert-1", "-I"])

    assert result.exit_code == 0
    assert "Dry run" in result.output
    assert "cert-1" in result.output


def test_doctor_check_without_credentials(monkeypatch):
    monkeypatch.setattr(
        cli_module,
        "_get_settings",
        lambda profile=None: QiniuSettings(profile="active", env_path=Path("/tmp/.env")),
    )

    result = CliRunner().invoke(main, ["doctor", "check"])

    assert result.exit_code == 0
    assert "has_credentials" in result.output
