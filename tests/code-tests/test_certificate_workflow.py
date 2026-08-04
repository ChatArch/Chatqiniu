from chatqiniu.client import DryRunResult
from chatqiniu.operations import deploy_certificate


class RecordingFusionClient:
    def __init__(self):
        self.uploads = []
        self.binds = []

    def cert_upload(self, **kwargs):
        self.uploads.append(kwargs)
        return {"certid": "new-cert-123"}

    def domain_https_set(self, **kwargs):
        self.binds.append(kwargs)
        return {"code": 200, "domain": kwargs["domain"]}


def test_deploy_certificate_dry_run_hides_certificate_material():
    result = deploy_certificate(
        None,
        name="demo-cert",
        cert_chain="CERTIFICATE MATERIAL WITH HIDDEN CONTENT",
        private_key="PRIVATE KEY MATERIAL WITH HIDDEN CONTENT",
        domains=["cdn.example.com", "assets.example.com"],
        force_https=True,
        dry_run=True,
    )

    assert isinstance(result, DryRunResult)
    rendered = "\n".join(result.steps)
    assert "demo-cert" in rendered
    assert "cdn.example.com" in rendered
    assert "assets.example.com" in rendered
    assert "SECRET CERT" not in rendered
    assert "SECRET KEY" not in rendered


def test_deploy_certificate_uploads_then_binds_every_domain():
    client = RecordingFusionClient()

    result = deploy_certificate(
        client,
        name="demo-cert",
        cert_chain="CERT BODY",
        private_key="KEY BODY",
        domains=["cdn.example.com", "assets.example.com"],
        force_https=True,
        http2=False,
        dry_run=False,
    )

    assert client.uploads == [
        {"name": "demo-cert", "cert_chain": "CERT BODY", "private_key": "KEY BODY", "dry_run": False}
    ]
    assert client.binds == [
        {"domain": "cdn.example.com", "cert_id": "new-cert-123", "force_https": True, "http2": False, "dry_run": False},
        {"domain": "assets.example.com", "cert_id": "new-cert-123", "force_https": True, "http2": False, "dry_run": False},
    ]
    assert result["cert_id"] == "new-cert-123"
    assert result["domains"] == [
        {"domain": "cdn.example.com", "code": 200},
        {"domain": "assets.example.com", "code": 200},
    ]
