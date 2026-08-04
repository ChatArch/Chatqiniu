"""Reusable Chatqiniu operation workflows behind CLI commands."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .client import DryRunResult

_CERT_ID_KEYS = ("certid", "certID", "certId", "id")


def deploy_certificate(
    fusion_client: Any,
    *,
    name: str,
    cert_chain: str,
    private_key: str,
    domains: Sequence[str],
    force_https: bool = False,
    http2: bool = True,
    dry_run: bool = True,
) -> dict[str, Any] | DryRunResult:
    """Upload a certificate and bind it to one or more CDN domains.

    Certificate and private-key bodies are intentionally omitted from dry-run
    steps and returned payloads.
    """

    selected_domains = [domain for domain in domains if domain]
    if dry_run:
        return DryRunResult(
            "cert deploy",
            (
                f"name={name}",
                "POST https://fusion.qiniuapi.com/sslcert",
                "private key and certificate body hidden",
                *(f"bind domain={domain} forceHttps={force_https} http2Enable={http2}" for domain in selected_domains),
            ),
        )

    upload_result = fusion_client.cert_upload(
        name=name,
        cert_chain=cert_chain,
        private_key=private_key,
        dry_run=False,
    )
    cert_id = extract_certificate_id(upload_result)
    domain_results: list[dict[str, Any]] = []
    for domain in selected_domains:
        bind_result = fusion_client.domain_https_set(
            domain=domain,
            cert_id=cert_id,
            force_https=force_https,
            http2=http2,
            dry_run=False,
        )
        row = {"domain": domain}
        if isinstance(bind_result, dict):
            row.update({key: value for key, value in bind_result.items() if key not in {"domain"}})
        domain_results.append(row)
    return {"cert_id": cert_id, "domains": domain_results}


def extract_certificate_id(upload_result: Any) -> str:
    """Return the certificate id from Qiniu's upload response."""

    if isinstance(upload_result, dict):
        for key in _CERT_ID_KEYS:
            value = upload_result.get(key)
            if value:
                return str(value)
    raise ValueError("Qiniu certificate upload response did not include a certificate id")
