from chatqiniu.config import delete_profile, list_profiles, load_settings, masked_settings, save_settings, use_profile


def test_save_and_load_active_settings(monkeypatch, tmp_path):
    monkeypatch.setenv("CHATARCH_HOME", str(tmp_path / ".chatarch"))

    save_settings(
        {
            "QINIU_ACCESS_KEY": "AK1234567890",
            "QINIU_SECRET_KEY": "SK1234567890",
            "QINIU_BUCKET_NAME": "demo-bucket",
            "QINIU_URL_PREFIX": "https://cdn.example.com",
        }
    )

    settings = load_settings()
    assert settings.access_key == "AK1234567890"
    assert settings.secret_key == "SK1234567890"
    assert settings.bucket_name == "demo-bucket"
    assert settings.url_prefix == "https://cdn.example.com"
    assert settings.env_path is not None
    assert settings.env_path.name == ".env"


def test_profile_create_use_delete(monkeypatch, tmp_path):
    monkeypatch.setenv("CHATARCH_HOME", str(tmp_path / ".chatarch"))

    save_settings({"QINIU_ACCESS_KEY": "ACTIVE_AK", "QINIU_SECRET_KEY": "ACTIVE_SK"})
    save_settings({"QINIU_ACCESS_KEY": "P_AK", "QINIU_SECRET_KEY": "P_SK"}, profile="work")

    assert list_profiles() == ["work"]

    source = use_profile("work")
    assert source.name == "work.env"
    active = load_settings()
    assert active.access_key == "P_AK"

    target = delete_profile("work")
    assert target.name == "work.env"
    assert list_profiles() == []


def test_masked_settings_hides_secret(monkeypatch, tmp_path):
    monkeypatch.setenv("CHATARCH_HOME", str(tmp_path / ".chatarch"))
    save_settings({"QINIU_ACCESS_KEY": "ABCDEFGHIJKL", "QINIU_SECRET_KEY": "1234567890SECRET"})

    masked = masked_settings(load_settings())
    assert masked["QINIU_ACCESS_KEY"].startswith("ABCD")
    assert masked["QINIU_SECRET_KEY"].startswith("1234")
    assert "SECRET" not in masked["QINIU_SECRET_KEY"]
