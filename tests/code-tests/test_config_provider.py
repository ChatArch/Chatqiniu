from chatqiniu.config import ChatqiniuConfig


def test_config_provider_schema_test_is_safe(capsys):
    ChatqiniuConfig.test()

    output = capsys.readouterr().out
    assert "Provider schema OK" in output
    assert "QINIU_SECRET_KEY=" not in output
