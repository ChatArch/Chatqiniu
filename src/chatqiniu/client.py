"""HTTP clients for Qiniu Kodo, CDN, and certificate APIs."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode, urlparse

import requests

from .config import QiniuSettings

ApiPayload = dict[str, Any] | list[Any]


class QiniuApiError(RuntimeError):
    """Raised when a Qiniu API request fails."""

    def __init__(self, message: str, *, status_code: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


@dataclass(frozen=True)
class DryRunResult:
    """Description of a write operation that was not executed."""

    action: str
    steps: tuple[str, ...]


def urlsafe_base64(data: bytes | str) -> str:
    """Return Qiniu URL-safe base64 without padding."""

    raw = data.encode("utf-8") if isinstance(data, str) else data
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def entry_uri(bucket: str, key: str) -> str:
    """Return EncodedEntryURI for object management APIs."""

    return urlsafe_base64(f"{bucket}:{key}")


class QiniuClient:
    """Small Qiniu API wrapper used by the CLI."""

    def __init__(self, settings: QiniuSettings, *, timeout: int = 30):
        settings.require_credentials()
        self.settings = settings
        self.timeout = timeout

    @property
    def access_key(self) -> str:
        return self.settings.access_key

    @property
    def secret_key(self) -> str:
        return self.settings.secret_key

    def bucket_list(self) -> list[str]:
        data = self._request("GET", "https://uc.qiniuapi.com/buckets")
        if isinstance(data, list):
            return [str(item) for item in data]
        buckets = data.get("buckets") or data.get("items") or []
        return [str(item) for item in buckets]

    def object_list(
        self,
        *,
        bucket: str,
        prefix: str | None = None,
        limit: int = 100,
        marker: str | None = None,
        delimiter: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"bucket": bucket, "limit": limit}
        if prefix:
            params["prefix"] = prefix
        if marker:
            params["marker"] = marker
        if delimiter:
            params["delimiter"] = delimiter
        return self._request_dict("GET", "https://rsf.qiniuapi.com/list", params=params)

    def object_stat(self, *, bucket: str, key: str) -> dict[str, Any]:
        return self._request_dict("GET", f"https://rs.qiniuapi.com/stat/{entry_uri(bucket, key)}")

    def object_delete(self, *, bucket: str, key: str, dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        path = f"/delete/{entry_uri(bucket, key)}"
        if dry_run:
            return DryRunResult("object delete", (f"POST https://rs.qiniuapi.com{path}", f"bucket={bucket}", f"key={key}"))
        return self._request_dict("POST", f"https://rs.qiniuapi.com{path}")

    def object_copy(self, *, bucket: str, src_key: str, dst_key: str, dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        path = f"/copy/{entry_uri(bucket, src_key)}/{entry_uri(bucket, dst_key)}"
        if dry_run:
            return DryRunResult("object copy", (f"POST https://rs.qiniuapi.com{path}", f"{src_key} -> {dst_key}"))
        return self._request_dict("POST", f"https://rs.qiniuapi.com{path}")

    def object_move(self, *, bucket: str, src_key: str, dst_key: str, dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        path = f"/move/{entry_uri(bucket, src_key)}/{entry_uri(bucket, dst_key)}"
        if dry_run:
            return DryRunResult("object move", (f"POST https://rs.qiniuapi.com{path}", f"{src_key} -> {dst_key}"))
        return self._request_dict("POST", f"https://rs.qiniuapi.com{path}")

    def object_batch_delete(self, *, bucket: str, keys: list[str], dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        ops = [f"/delete/{entry_uri(bucket, key)}" for key in keys]
        if dry_run:
            sample = tuple(f"delete {key}" for key in keys[:10])
            return DryRunResult("object batch-delete", (f"bucket={bucket}", f"items={len(keys)}", *sample))
        body = urlencode([("op", op) for op in ops]).encode("utf-8")
        return self._request_dict("POST", "https://rs.qiniuapi.com/batch", body=body)

    def upload_token(self, *, bucket: str, key: str | None = None, expires: int = 3600) -> str:
        scope = f"{bucket}:{key}" if key else bucket
        policy = {"scope": scope, "deadline": int(time.time()) + expires}
        encoded_policy = urlsafe_base64(json.dumps(policy, separators=(",", ":")))
        sign = self._sign(encoded_policy.encode("ascii"))
        return f"{self.access_key}:{sign}:{encoded_policy}"

    def object_upload(
        self,
        *,
        local_file: Path,
        bucket: str,
        key: str,
        overwrite: bool = False,
        skip_existing: bool = False,
        dry_run: bool = False,
        up_host: str | None = None,
    ) -> dict[str, Any] | DryRunResult:
        if dry_run:
            return DryRunResult(
                "object upload",
                (f"file={local_file}", f"bucket={bucket}", f"key={key}", f"up_host={up_host or self.settings.up_host}"),
            )
        if skip_existing:
            try:
                self.object_stat(bucket=bucket, key=key)
                return {"skipped": True, "reason": "exists", "key": key}
            except QiniuApiError as exc:
                if exc.status_code not in {404, 612}:
                    raise
        token_key = key if overwrite else None
        token = self.upload_token(bucket=bucket, key=token_key)
        mime = mimetypes.guess_type(local_file.name)[0] or "application/octet-stream"
        with local_file.open("rb") as fh:
            response = requests.post(
                (up_host or self.settings.up_host).rstrip("/") + "/",
                data={"token": token, "key": key},
                files={"file": (local_file.name, fh, mime)},
                timeout=self.timeout,
            )
        return self._decode_response_dict(response)

    def public_url(self, *, key: str, url_prefix: str) -> str:
        return f"{url_prefix.rstrip('/')}/{quote(key)}"

    def private_url(self, *, key: str, url_prefix: str, expires: int = 3600) -> str:
        base = self.public_url(key=key, url_prefix=url_prefix)
        deadline = int(time.time()) + expires
        url = f"{base}?e={deadline}"
        token = f"{self.access_key}:{self._sign(url.encode('utf-8'))}"
        return f"{url}&token={token}"

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        body: bytes | None = None,
        json_body: dict[str, Any] | None = None,
        auth_scheme: str = "qiniu",
    ) -> ApiPayload:
        request_body = body
        headers: dict[str, str] = {}
        if json_body is not None:
            request_body = json.dumps(json_body, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif request_body is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            request_body = b""
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers.update(
            self._auth_headers(
                method,
                url,
                params=params,
                body=request_body,
                content_type=headers["Content-Type"],
                scheme=auth_scheme,
            )
        )
        response = requests.request(
            method,
            url,
            params=params,
            data=request_body if method.upper() != "GET" else None,
            headers=headers,
            timeout=self.timeout,
        )
        return self._decode_response(response)

    def _request_dict(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        payload = self._request(method, url, **kwargs)
        if isinstance(payload, dict):
            return payload
        return {"items": payload}

    def _decode_response(self, response: requests.Response) -> ApiPayload:
        try:
            payload: Any = response.json() if response.text else {}
        except ValueError:
            payload = {"text": response.text}
        if response.status_code >= 400:
            message = payload.get("error") if isinstance(payload, dict) else None
            raise QiniuApiError(message or f"Qiniu API failed with HTTP {response.status_code}", status_code=response.status_code, payload=payload)
        return payload

    def _decode_response_dict(self, response: requests.Response) -> dict[str, Any]:
        payload = self._decode_response(response)
        if isinstance(payload, dict):
            return payload
        return {"items": payload}

    def _auth_headers(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None,
        body: bytes,
        content_type: str,
        scheme: str,
    ) -> dict[str, str]:
        parsed = urlparse(url)
        query = parsed.query
        if params:
            query = urlencode(params)
        path_query = parsed.path or "/"
        if query:
            path_query += f"?{query}"
        if scheme.lower() == "qbox":
            data = path_query.encode("utf-8") + b"\n" + body
            return {"Authorization": f"QBox {self.access_key}:{self._sign(data)}"}
        qiniu_date = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        signing_text = (
            f"{method.upper()} {path_query}\n"
            f"Host: {parsed.netloc}\n"
            f"Content-Type: {content_type}\n"
            f"X-Qiniu-Date: {qiniu_date}\n\n"
        ).encode("utf-8") + body
        return {
            "Authorization": f"Qiniu {self.access_key}:{self._sign(signing_text)}",
            "X-Qiniu-Date": qiniu_date,
        }

    def _sign(self, data: bytes) -> str:
        return urlsafe_base64(hmac.new(self.secret_key.encode("utf-8"), data, hashlib.sha1).digest())


class FusionClient(QiniuClient):
    """Qiniu CDN/Fusion API wrapper."""

    def cert_list(self, *, marker: str | None = None, limit: int = 100) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit}
        if marker:
            params["marker"] = marker
        return self._request_dict("GET", "https://fusion.qiniuapi.com/sslcert", params=params, auth_scheme="qbox")

    def cert_show(self, cert_id: str) -> dict[str, Any]:
        return self._request_dict("GET", f"https://fusion.qiniuapi.com/sslcert/{quote(cert_id)}", auth_scheme="qbox")

    def cert_upload(self, *, name: str, private_key: str, cert_chain: str, dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        if dry_run:
            return DryRunResult("cert upload", (f"name={name}", "POST https://fusion.qiniuapi.com/sslcert", "private key and certificate body hidden"))
        return self._request_dict(
            "POST",
            "https://fusion.qiniuapi.com/sslcert",
            json_body={"name": name, "pri": private_key, "ca": cert_chain},
            auth_scheme="qbox",
        )

    def cert_delete(self, cert_id: str, *, dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        if dry_run:
            return DryRunResult("cert delete", (f"DELETE https://fusion.qiniuapi.com/sslcert/{cert_id}",))
        return self._request_dict("DELETE", f"https://fusion.qiniuapi.com/sslcert/{quote(cert_id)}", auth_scheme="qbox")

    def domain_list(self, *, marker: str | None = None, limit: int = 100) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit}
        if marker:
            params["marker"] = marker
        return self._request_dict("GET", "https://api.qiniu.com/domain", params=params)

    def domain_show(self, domain: str) -> dict[str, Any]:
        return self._request_dict("GET", f"https://api.qiniu.com/domain/{quote(domain)}")

    def domain_https_set(
        self,
        *,
        domain: str,
        cert_id: str,
        force_https: bool = False,
        http2: bool = True,
        dry_run: bool = True,
    ) -> dict[str, Any] | DryRunResult:
        body = {"certId": cert_id, "forceHttps": force_https, "http2Enable": http2}
        path = f"https://api.qiniu.com/domain/{quote(domain)}/httpsconf"
        if dry_run:
            return DryRunResult("domain https set", (f"PUT {path}", f"certId={cert_id}", f"forceHttps={force_https}", f"http2Enable={http2}"))
        return self._request_dict("PUT", path, json_body=body)

    def cdn_refresh(self, *, urls: list[str], dirs: list[str] | None = None, dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        body = {"urls": urls, "dirs": dirs or []}
        if dry_run:
            return DryRunResult("cdn refresh", (f"urls={len(urls)}", f"dirs={len(dirs or [])}", "POST https://fusion.qiniuapi.com/v2/tune/refresh"))
        return self._request_dict("POST", "https://fusion.qiniuapi.com/v2/tune/refresh", json_body=body, auth_scheme="qbox")

    def cdn_prefetch(self, *, urls: list[str], dry_run: bool = True) -> dict[str, Any] | DryRunResult:
        body = {"urls": urls}
        if dry_run:
            return DryRunResult("cdn prefetch", (f"urls={len(urls)}", "POST https://fusion.qiniuapi.com/v2/tune/prefetch"))
        return self._request_dict("POST", "https://fusion.qiniuapi.com/v2/tune/prefetch", json_body=body, auth_scheme="qbox")

    def cdn_task(self, *, task_id: str, kind: str = "refresh") -> dict[str, Any]:
        endpoint = "refresh" if kind == "refresh" else "prefetch"
        return self._request_dict(
            "POST",
            f"https://fusion.qiniuapi.com/v2/tune/{endpoint}/list",
            json_body={"taskId": task_id},
            auth_scheme="qbox",
        )
