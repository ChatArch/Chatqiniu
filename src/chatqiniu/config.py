"""ChatEnv integration for Chatqiniu."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import click
from chatenv import BaseEnvConfig, EnvField, EnvStore, get_paths


class QiniuConfig(BaseEnvConfig):
    """Typed ChatEnv schema for Qiniu/Kodo credentials and defaults."""

    _title = "Qiniu Configuration"
    _aliases = ["qiniu", "kodo"]
    _storage_dir = "Qiniu"

    QINIU_ACCESS_KEY = EnvField("QINIU_ACCESS_KEY", desc="Qiniu AccessKey", is_sensitive=True)
    QINIU_SECRET_KEY = EnvField("QINIU_SECRET_KEY", desc="Qiniu SecretKey", is_sensitive=True)
    QINIU_BUCKET_NAME = EnvField("QINIU_BUCKET_NAME", desc="Default Kodo bucket")
    QINIU_URL_PREFIX = EnvField("QINIU_URL_PREFIX", desc="Default public URL prefix")
    QINIU_CDN_DOMAIN = EnvField("QINIU_CDN_DOMAIN", desc="Default CDN domain")
    QINIU_REGION = EnvField("QINIU_REGION", desc="Default Qiniu region hint")
    QINIU_UP_HOST = EnvField(
        "QINIU_UP_HOST",
        default="https://up.qiniup.com",
        desc="Default Kodo upload host",
    )


@dataclass(frozen=True)
class QiniuSettings:
    """Resolved Qiniu settings loaded from ChatEnv."""

    access_key: str = ""
    secret_key: str = ""
    bucket_name: str = ""
    url_prefix: str = ""
    cdn_domain: str = ""
    region: str = ""
    up_host: str = "https://up.qiniup.com"
    profile: str = "active"
    env_path: Path | None = None

    @property
    def has_credentials(self) -> bool:
        return bool(self.access_key and self.secret_key)

    def require_credentials(self) -> None:
        if not self.has_credentials:
            raise click.ClickException("Qiniu credentials are missing. Run `chatqiniu auth login` first.")

    def require_bucket(self, bucket: str | None = None) -> str:
        selected = bucket or self.bucket_name
        if not selected:
            raise click.ClickException("Qiniu bucket is missing. Pass --bucket or set QINIU_BUCKET_NAME.")
        return selected

    def require_url_prefix(self, url_prefix: str | None = None) -> str:
        selected = url_prefix or self.url_prefix
        if not selected:
            raise click.ClickException("Qiniu url prefix is missing. Pass --url-prefix or set QINIU_URL_PREFIX.")
        return selected.rstrip("/")


def get_store(home: str | Path | None = None) -> EnvStore:
    """Return the ChatEnv store used by Chatqiniu."""

    return EnvStore(get_paths(home).envs_dir)


def _values_to_settings(values: dict[str, Any], *, profile: str, env_path: Path | None) -> QiniuSettings:
    return QiniuSettings(
        access_key=str(values.get("QINIU_ACCESS_KEY") or ""),
        secret_key=str(values.get("QINIU_SECRET_KEY") or ""),
        bucket_name=str(values.get("QINIU_BUCKET_NAME") or ""),
        url_prefix=str(values.get("QINIU_URL_PREFIX") or ""),
        cdn_domain=str(values.get("QINIU_CDN_DOMAIN") or ""),
        region=str(values.get("QINIU_REGION") or ""),
        up_host=str(values.get("QINIU_UP_HOST") or "https://up.qiniup.com"),
        profile=profile,
        env_path=env_path,
    )


def load_settings(profile: str | None = None, home: str | Path | None = None) -> QiniuSettings:
    """Load Qiniu settings from ChatEnv active or named profile."""

    store = get_store(home)
    if profile:
        env_path = store.profile_path(QiniuConfig, profile)
        values = store.load_profile(QiniuConfig, profile)
        return _values_to_settings(values, profile=profile, env_path=env_path)

    env_path = store.active_path(QiniuConfig)
    values = store.load_active(QiniuConfig)
    return _values_to_settings(values, profile="active", env_path=env_path)


def save_settings(values: dict[str, Any], profile: str | None = None, home: str | Path | None = None) -> Path:
    """Merge and save Qiniu settings through ChatEnv."""

    store = get_store(home)
    store.ensure_root()
    current = store.load_profile(QiniuConfig, profile) if profile else store.load_active(QiniuConfig)
    current.update({key: value for key, value in values.items() if value is not None})
    if profile:
        return store.save_profile(QiniuConfig, profile, current)
    return store.save_active(QiniuConfig, current)


def list_profiles(home: str | Path | None = None) -> list[str]:
    """List named Qiniu ChatEnv profiles."""

    return get_store(home).list_profiles(QiniuConfig)


def use_profile(name: str, home: str | Path | None = None) -> Path:
    """Activate a named Qiniu ChatEnv profile."""

    return get_store(home).use_profile(QiniuConfig, name)


def delete_profile(name: str, home: str | Path | None = None) -> Path:
    """Delete a named Qiniu ChatEnv profile."""

    return get_store(home).delete_profile(QiniuConfig, name)


def masked_settings(settings: QiniuSettings) -> dict[str, str]:
    """Return settings safe for terminal output."""

    return {
        "profile": settings.profile,
        "env_path": str(settings.env_path or ""),
        "QINIU_ACCESS_KEY": _mask(settings.access_key),
        "QINIU_SECRET_KEY": _mask(settings.secret_key),
        "QINIU_BUCKET_NAME": settings.bucket_name,
        "QINIU_URL_PREFIX": settings.url_prefix,
        "QINIU_CDN_DOMAIN": settings.cdn_domain,
        "QINIU_REGION": settings.region,
        "QINIU_UP_HOST": settings.up_host,
    }


def _mask(value: str) -> str:
    if not value:
        return "<unset>"
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"
