"""Local lightweight app registry for Chatqiniu."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_REGISTRY = Path.home() / ".chatqiniu" / "apps.json"


@dataclass(frozen=True)
class LightApp:
    """A lightweight app entry managed by Chatqiniu."""

    name: str
    endpoint: str
    title: str = ""
    description: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "endpoint": self.endpoint,
            "title": self.title,
            "description": self.description,
        }


def resolve_registry_path(path: str | Path | None = None) -> Path:
    """Resolve the app registry path from an explicit value or env default."""

    if path:
        return Path(path).expanduser()
    env_path = os.environ.get("CHATQINIU_REGISTRY")
    if env_path:
        return Path(env_path).expanduser()
    return DEFAULT_REGISTRY


def load_apps(path: str | Path | None = None) -> list[LightApp]:
    registry_path = resolve_registry_path(path)
    if not registry_path.exists():
        return []
    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid Chatqiniu registry JSON: {registry_path}") from exc
    if not isinstance(payload, list):
        raise ValueError(f"Chatqiniu registry must be a JSON list: {registry_path}")
    return [_app_from_payload(item) for item in payload]


def save_apps(apps: list[LightApp], path: str | Path | None = None) -> Path:
    registry_path = resolve_registry_path(path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [app.to_dict() for app in sorted(apps, key=lambda item: item.name.lower())]
    registry_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return registry_path


def upsert_app(
    *,
    name: str,
    endpoint: str,
    title: str = "",
    description: str = "",
    path: str | Path | None = None,
) -> LightApp:
    normalized = _normalize_name(name)
    app = LightApp(
        name=normalized,
        endpoint=endpoint.strip(),
        title=title.strip(),
        description=description.strip(),
    )
    if not app.endpoint:
        raise ValueError("endpoint is required")

    apps = [item for item in load_apps(path) if item.name != normalized]
    apps.append(app)
    save_apps(apps, path)
    return app


def find_app(name: str, path: str | Path | None = None) -> LightApp | None:
    normalized = _normalize_name(name)
    for app in load_apps(path):
        if app.name == normalized:
            return app
    return None


def remove_app(name: str, path: str | Path | None = None) -> bool:
    normalized = _normalize_name(name)
    apps = load_apps(path)
    kept = [app for app in apps if app.name != normalized]
    if len(kept) == len(apps):
        return False
    save_apps(kept, path)
    return True


def _app_from_payload(payload: Any) -> LightApp:
    if not isinstance(payload, dict):
        raise ValueError("Chatqiniu app entries must be JSON objects")
    name = _normalize_name(str(payload.get("name", "")))
    endpoint = str(payload.get("endpoint", "")).strip()
    if not endpoint:
        raise ValueError(f"endpoint is required for app {name}")
    return LightApp(
        name=name,
        endpoint=endpoint,
        title=str(payload.get("title", "")).strip(),
        description=str(payload.get("description", "")).strip(),
    )


def _normalize_name(name: str) -> str:
    normalized = name.strip()
    if not normalized:
        raise ValueError("name is required")
    return normalized
