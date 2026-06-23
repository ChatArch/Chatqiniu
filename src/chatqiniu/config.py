"Typed environment configuration for Chatqiniu."

from chatenv import BaseEnvConfig, EnvField


class ChatqiniuConfig(BaseEnvConfig):
    "Chatqiniu ChatEnv configuration."

    _title = "Chatqiniu Configuration"
    _aliases = ["qiniu", "chatqiniu"]
    _storage_dir = "Qiniu"

    QINIU_ACCESS_KEY = EnvField(
        "QINIU_ACCESS_KEY",
        desc="Qiniu access key",
        is_sensitive=True,
    )
    QINIU_SECRET_KEY = EnvField(
        "QINIU_SECRET_KEY",
        desc="Qiniu secret key",
        is_sensitive=True,
    )
    QINIU_API_BASE = EnvField(
        "QINIU_API_BASE",
        desc="Qiniu API base URL",
    )
    CHATQINIU_REGISTRY = EnvField(
        "CHATQINIU_REGISTRY",
        desc="Path to the Chatqiniu lightweight app registry JSON file",
    )

    @classmethod
    def test(cls) -> None:
        """Validate provider wiring without calling Qiniu or printing secrets."""

        print(f"Testing {cls._title}...")
        fields = cls.get_fields()
        expected = {
            "QINIU_ACCESS_KEY",
            "QINIU_SECRET_KEY",
            "QINIU_API_BASE",
            "CHATQINIU_REGISTRY",
        }
        missing = expected.difference(fields)
        if missing:
            raise RuntimeError(f"Missing config fields: {', '.join(sorted(missing))}")
        sensitive = [name for name, field in fields.items() if field.is_sensitive]
        print(
            "Provider schema OK: "
            f"{len(fields)} fields, {len(sensitive)} sensitive fields masked."
        )


__all__ = ["ChatqiniuConfig"]
