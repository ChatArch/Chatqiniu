import os

import pytest
from click.testing import CliRunner

from chatqiniu.cli import main
from chatqiniu.config import load_settings


pytestmark = pytest.mark.skipif(
    os.getenv("CHATQINIU_RUN_LIVE_TESTS") != "1",
    reason="live Qiniu tests are disabled",
)


@pytest.mark.live
def test_live_auth_whoami_reads_current_account():
    settings = load_settings()
    if not settings.has_credentials:
        pytest.skip("Qiniu credentials are not configured")

    result = CliRunner().invoke(main, ["auth", "whoami", "--format", "json"])

    assert result.exit_code == 0
    assert "bucket_count" in result.output


@pytest.mark.live
def test_live_cert_list_reads_current_certificates():
    settings = load_settings()
    if not settings.has_credentials:
        pytest.skip("Qiniu credentials are not configured")

    result = CliRunner().invoke(main, ["cert", "list", "--format", "json"])

    assert result.exit_code == 0
    assert "certid" in result.output or "certID" in result.output
