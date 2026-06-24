"""CLI entrypoint for chatqiniu."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import quote

import click
from chatstyle import (
    CommandField,
    CommandSchema,
    add_interactive_option,
    render_dry_run,
    render_error,
    render_info,
    render_key_values,
    render_success,
    render_warning,
    resolve_command_inputs,
)

from .client import DryRunResult, FusionClient, QiniuApiError, QiniuClient
from .config import delete_profile, list_profiles, load_settings, masked_settings, save_settings, use_profile
from .formatting import render_data

DOC_LINKS = {
    "developer-center": "https://developer.qiniu.com/",
    "kodo": "https://developer.qiniu.com/kodo",
    "kodo-api": "https://developer.qiniu.com/kodo/3939/overview-of-the-api",
    "python-sdk": "https://developer.qiniu.com/kodo/1242/python",
    "cdn": "https://developer.qiniu.com/fusion",
    "cdn-api": "https://developer.qiniu.com/fusion/13353/fusion-api-overview",
    "cdn-cert": "https://developer.qiniu.com/fusion/13368/fusion-api-cert-management",
    "ssl": "https://developer.qiniu.com/ssl",
}

CONFIG_KEY_MAP = {
    "bucket": "QINIU_BUCKET_NAME",
    "url-prefix": "QINIU_URL_PREFIX",
    "cdn-domain": "QINIU_CDN_DOMAIN",
    "region": "QINIU_REGION",
    "up-host": "QINIU_UP_HOST",
}

HELLO_SCHEMA = CommandSchema(
    name="hello",
    fields=(CommandField("name", prompt="name", required=True),),
)

LOGIN_SCHEMA = CommandSchema(
    name="auth-login",
    fields=(
        CommandField("access_key", prompt="Qiniu AccessKey", required=True, sensitive=True),
        CommandField("secret_key", prompt="Qiniu SecretKey", required=True, sensitive=True),
        CommandField("profile", prompt="profile name", required=False, default=""),
    ),
)

UPLOAD_SCHEMA = CommandSchema(
    name="object-upload",
    fields=(
        CommandField("local_file", prompt="local file", required=True),
        CommandField("key", prompt="object key", required=True),
    ),
)

UPLOAD_DIR_SCHEMA = CommandSchema(
    name="object-upload-dir",
    fields=(
        CommandField("local_dir", prompt="local directory", required=True),
        CommandField("prefix", prompt="object prefix", required=False, default=""),
    ),
)

DELETE_SCHEMA = CommandSchema(
    name="object-delete",
    fields=(CommandField("key", prompt="object key", required=True),),
)

COPY_SCHEMA = CommandSchema(
    name="object-copy",
    fields=(
        CommandField("src_key", prompt="source key", required=True),
        CommandField("dst_key", prompt="destination key", required=True),
    ),
)

URL_SCHEMA = CommandSchema(
    name="object-url",
    fields=(CommandField("key", prompt="object key", required=True),),
)

CERT_UPLOAD_SCHEMA = CommandSchema(
    name="cert-upload",
    fields=(
        CommandField("name", prompt="certificate name", required=True),
        CommandField("cert_chain", prompt="certificate chain path", required=True),
        CommandField("private_key", prompt="private key path", required=True),
    ),
)

DOMAIN_HTTPS_SCHEMA = CommandSchema(
    name="domain-https-set",
    fields=(
        CommandField("domain", prompt="cdn domain", required=True),
        CommandField("cert_id", prompt="certificate id", required=True),
    ),
)


@click.group()
def main() -> None:
    """chatqiniu command line interface."""


@main.command()
@click.argument("name", required=False)
@add_interactive_option
def hello(name: str | None, interactive: bool | None) -> None:
    """Backward-compatible greeting command from the template."""

    values = _resolve_inputs(
        schema=HELLO_SCHEMA,
        provided={"name": name},
        interactive=interactive,
        usage="Usage: chatqiniu hello [NAME]",
    )
    render_success(f"Hello, {values['name']}!")


def _resolve_inputs(
    *,
    schema: CommandSchema,
    provided: dict[str, Any],
    interactive: bool | None,
    usage: str,
) -> dict[str, Any]:
    return resolve_command_inputs(
        schema=schema,
        provided=provided,
        interactive=interactive,
        usage=usage,
    )


def _get_settings(profile: str | None = None):
    return load_settings(profile=profile or None)


def _client(profile: str | None = None) -> QiniuClient:
    return QiniuClient(_get_settings(profile))


def _fusion_client(profile: str | None = None) -> FusionClient:
    return FusionClient(_get_settings(profile))


def _config_env_key(key: str) -> str:
    normalized = key.strip().lower()
    if normalized in CONFIG_KEY_MAP:
        return CONFIG_KEY_MAP[normalized]
    raise click.ClickException(f"Unsupported config key: {key}")


def _maybe_render_dry_run(result: Any) -> None:
    if isinstance(result, DryRunResult):
        render_dry_run(result.steps, heading=f"Dry run: {result.action}")
        return
    render_data(result, output_format="table")


def _collect_keys_from_list_result(data: dict[str, Any]) -> list[str]:
    items = data.get("items") or []
    keys: list[str] = []
    for item in items:
        if isinstance(item, dict) and item.get("key"):
            keys.append(str(item["key"]))
    return keys


@main.group()
def auth() -> None:
    """Credential bootstrap and identity checks."""


@auth.command("login")
@click.option("--access-key", help="Qiniu AccessKey")
@click.option("--secret-key", help="Qiniu SecretKey")
@click.option("--profile", help="Named ChatEnv profile to save")
@add_interactive_option
def auth_login(access_key: str | None, secret_key: str | None, profile: str | None, interactive: bool | None) -> None:
    """Save credentials into ChatEnv-managed Qiniu config."""

    values = _resolve_inputs(
        schema=LOGIN_SCHEMA,
        provided={"access_key": access_key, "secret_key": secret_key, "profile": profile},
        interactive=interactive,
        usage="Usage: chatqiniu auth login [--access-key AK --secret-key SK] [--profile NAME]",
    )
    target_profile = values.get("profile") or None
    path = save_settings(
        {"QINIU_ACCESS_KEY": values["access_key"], "QINIU_SECRET_KEY": values["secret_key"]},
        profile=target_profile,
    )
    render_success(f"Saved Qiniu credentials to {path}")


@auth.command("logout")
@click.option("--profile", help="Named ChatEnv profile to clear instead of active")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def auth_logout(profile: str | None, yes: bool) -> None:
    """Clear active credentials or remove a named profile."""

    if not yes:
        raise click.ClickException("Refusing to clear credentials without --yes.")
    path = save_settings({"QINIU_ACCESS_KEY": "", "QINIU_SECRET_KEY": ""}, profile=profile or None)
    render_success(f"Cleared Qiniu credentials in {path}")


@auth.command("whoami")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def auth_whoami(profile: str | None, output_format: str) -> None:
    """Validate current credentials with a read-only bucket listing."""

    settings = _get_settings(profile)
    client = _client(profile)
    buckets = client.bucket_list()
    payload = {
        "profile": settings.profile,
        "env_path": str(settings.env_path or ""),
        "bucket_count": len(buckets),
        "buckets": buckets,
        "QINIU_ACCESS_KEY": masked_settings(settings)["QINIU_ACCESS_KEY"],
    }
    render_data(payload, output_format=output_format)


@main.group()
def profile() -> None:
    """Manage named ChatEnv profiles."""


@profile.command("list")
def profile_list() -> None:
    """List named Qiniu profiles."""

    rows = [{"profile": name} for name in list_profiles()]
    render_data(rows or [{"profile": "<none>"}], columns=["profile"])


@profile.command("show")
@click.argument("name", required=False)
def profile_show(name: str | None) -> None:
    """Show the active or named profile."""

    render_key_values(masked_settings(_get_settings(name)))


@profile.command("use")
@click.argument("name")
def profile_use(name: str) -> None:
    """Activate a named profile."""

    source = use_profile(name)
    render_success(f"Activated Qiniu profile from {source}")


@profile.command("create")
@click.argument("name")
@click.option("--copy-active/--empty", default=True, help="Copy current active values by default")
def profile_create(name: str, copy_active: bool) -> None:
    """Create a named profile."""

    values = {}
    if copy_active:
        current = _get_settings()
        values = {
            "QINIU_ACCESS_KEY": current.access_key,
            "QINIU_SECRET_KEY": current.secret_key,
            "QINIU_BUCKET_NAME": current.bucket_name,
            "QINIU_URL_PREFIX": current.url_prefix,
            "QINIU_CDN_DOMAIN": current.cdn_domain,
            "QINIU_REGION": current.region,
            "QINIU_UP_HOST": current.up_host,
        }
    path = save_settings(values, profile=name)
    render_success(f"Created Qiniu profile at {path}")


@profile.command("delete")
@click.argument("name")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def profile_delete(name: str, yes: bool) -> None:
    """Delete a named profile."""

    if not yes:
        raise click.ClickException("Refusing to delete a profile without --yes.")
    target = delete_profile(name)
    render_success(f"Deleted Qiniu profile {target}")


@main.group()
def config() -> None:
    """Manage default Qiniu settings in ChatEnv."""


@config.command("list")
@click.option("--profile", help="Named ChatEnv profile")
def config_list(profile: str | None) -> None:
    """List non-sensitive config values."""

    render_key_values(masked_settings(_get_settings(profile)))


@config.command("get")
@click.argument("key")
@click.option("--profile", help="Named ChatEnv profile")
def config_get(key: str, profile: str | None) -> None:
    """Get one config value."""

    env_key = _config_env_key(key)
    render_key_values({env_key: masked_settings(_get_settings(profile)).get(env_key, "<unset>")})


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.option("--profile", help="Named ChatEnv profile")
def config_set(key: str, value: str, profile: str | None) -> None:
    """Set one config value."""

    env_key = _config_env_key(key)
    path = save_settings({env_key: value}, profile=profile or None)
    render_success(f"Updated {env_key} in {path}")


@config.command("unset")
@click.argument("key")
@click.option("--profile", help="Named ChatEnv profile")
def config_unset(key: str, profile: str | None) -> None:
    """Unset one config value."""

    env_key = _config_env_key(key)
    path = save_settings({env_key: ""}, profile=profile or None)
    render_success(f"Cleared {env_key} in {path}")


@main.group()
def bucket() -> None:
    """Inspect Kodo buckets."""


@bucket.command("list")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def bucket_list(profile: str | None, output_format: str) -> None:
    """List accessible buckets."""

    buckets = _client(profile).bucket_list()
    render_data([{"bucket": item} for item in buckets], output_format=output_format, columns=["bucket"])


@bucket.command("show")
@click.argument("name", required=False)
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def bucket_show(name: str | None, profile: str | None, output_format: str) -> None:
    """Show simple bucket information."""

    settings = _get_settings(profile)
    selected = name or settings.bucket_name
    if not selected:
        raise click.ClickException("Bucket is required. Pass a name or configure QINIU_BUCKET_NAME.")
    buckets = _client(profile).bucket_list()
    payload = {
        "bucket": selected,
        "configured_default": settings.bucket_name,
        "accessible": selected in buckets,
        "profile": settings.profile,
    }
    render_data(payload, output_format=output_format)


@main.group()
def object() -> None:
    """Manage Kodo objects."""


@object.command("upload")
@click.argument("local_file", required=False)
@click.option("--key", help="Object key")
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--overwrite", is_flag=True, help="Generate overwrite token")
@click.option("--skip-existing", is_flag=True, help="Skip upload when key already exists")
@click.option("--dry-run", is_flag=True, help="Preview upload request")
@add_interactive_option
def object_upload(local_file: str | None, key: str | None, bucket: str | None, profile: str | None, overwrite: bool, skip_existing: bool, dry_run: bool, interactive: bool | None) -> None:
    """Upload one local file."""

    values = _resolve_inputs(
        schema=UPLOAD_SCHEMA,
        provided={"local_file": local_file, "key": key},
        interactive=interactive,
        usage="Usage: chatqiniu object upload LOCAL_FILE --key KEY",
    )
    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    result = _client(profile).object_upload(
        local_file=Path(values["local_file"]),
        bucket=selected_bucket,
        key=values["key"],
        overwrite=overwrite,
        skip_existing=skip_existing,
        dry_run=dry_run,
    )
    _maybe_render_dry_run(result)


@object.command("upload-dir")
@click.argument("local_dir", required=False)
@click.option("--prefix", default="", help="Remote prefix")
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--overwrite", is_flag=True, help="Generate overwrite token")
@click.option("--skip-existing", is_flag=True, help="Skip upload when key already exists")
@click.option("--dry-run", is_flag=True, help="Preview upload requests")
@add_interactive_option
def object_upload_dir(local_dir: str | None, prefix: str, bucket: str | None, profile: str | None, overwrite: bool, skip_existing: bool, dry_run: bool, interactive: bool | None) -> None:
    """Upload a directory recursively."""

    values = _resolve_inputs(
        schema=UPLOAD_DIR_SCHEMA,
        provided={"local_dir": local_dir, "prefix": prefix},
        interactive=interactive,
        usage="Usage: chatqiniu object upload-dir LOCAL_DIR [--prefix PREFIX]",
    )
    base_dir = Path(values["local_dir"])
    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    client = _client(profile)
    rows: list[dict[str, Any]] = []
    for path in sorted(item for item in base_dir.rglob("*") if item.is_file()):
        rel = path.relative_to(base_dir).as_posix()
        key_name = f"{values['prefix'].strip('/')}/{rel}".strip("/") if values["prefix"] else rel
        result = client.object_upload(
            local_file=path,
            bucket=selected_bucket,
            key=key_name,
            overwrite=overwrite,
            skip_existing=skip_existing,
            dry_run=dry_run,
        )
        if isinstance(result, DryRunResult):
            rows.append({"file": str(path), "key": key_name, "mode": "dry-run"})
        else:
            rows.append({"file": str(path), "key": key_name, "result": result.get("key", result.get("skipped", True))})
    render_data(rows, columns=["file", "key", "mode", "result"])


@object.command("download")
@click.argument("key")
@click.option("--out", "output_path", required=True, help="Write target path")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--bucket", help="Bucket override")
@click.option("--private", "private_link", is_flag=True, help="Use signed private URL")
@click.option("--expires", default=3600, type=int, show_default=True, help="Private URL ttl")
def object_download(key: str, output_path: str, profile: str | None, bucket: str | None, private_link: bool, expires: int) -> None:
    """Download an object via generated URL."""

    settings = _get_settings(profile)
    client = _client(profile)
    url_prefix = settings.require_url_prefix()
    if private_link:
        url = client.private_url(key=key, url_prefix=url_prefix, expires=expires)
    else:
        url = client.public_url(key=key, url_prefix=url_prefix)
    response = __import__("requests").get(url, timeout=30)
    response.raise_for_status()
    Path(output_path).write_bytes(response.content)
    render_success(f"Downloaded {key} to {output_path}")


@object.command("list")
@click.option("--prefix", default=None, help="Prefix filter")
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--limit", default=100, type=int, show_default=True)
@click.option("--marker", default=None)
@click.option("--delimiter", default=None)
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def object_list(prefix: str | None, bucket: str | None, profile: str | None, limit: int, marker: str | None, delimiter: str | None, output_format: str) -> None:
    """List objects in one bucket."""

    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    result = _client(profile).object_list(bucket=selected_bucket, prefix=prefix, limit=limit, marker=marker, delimiter=delimiter)
    render_data(result.get("items", []), output_format=output_format)


@object.command("stat")
@click.argument("key")
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def object_stat(key: str, bucket: str | None, profile: str | None, output_format: str) -> None:
    """Show object metadata."""

    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    render_data(_client(profile).object_stat(bucket=selected_bucket, key=key), output_format=output_format)


@object.command("delete")
@click.argument("key", required=False)
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@click.option("--yes", is_flag=True, help="Required with --execute")
@add_interactive_option
def object_delete(key: str | None, bucket: str | None, profile: str | None, dry_run: bool, yes: bool, interactive: bool | None) -> None:
    """Delete one object, dry-run by default."""

    values = _resolve_inputs(
        schema=DELETE_SCHEMA,
        provided={"key": key},
        interactive=interactive,
        usage="Usage: chatqiniu object delete KEY [--execute --yes]",
    )
    if not dry_run and not yes:
        raise click.ClickException("Use --yes together with --execute for destructive operations.")
    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    result = _client(profile).object_delete(bucket=selected_bucket, key=values["key"], dry_run=dry_run)
    _maybe_render_dry_run(result)


@object.command("copy")
@click.argument("src_key", required=False)
@click.argument("dst_key", required=False)
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@add_interactive_option
def object_copy(src_key: str | None, dst_key: str | None, bucket: str | None, profile: str | None, dry_run: bool, interactive: bool | None) -> None:
    """Copy one object, dry-run by default."""

    values = _resolve_inputs(
        schema=COPY_SCHEMA,
        provided={"src_key": src_key, "dst_key": dst_key},
        interactive=interactive,
        usage="Usage: chatqiniu object copy SRC_KEY DST_KEY [--execute]",
    )
    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    result = _client(profile).object_copy(bucket=selected_bucket, src_key=values["src_key"], dst_key=values["dst_key"], dry_run=dry_run)
    _maybe_render_dry_run(result)


@object.command("move")
@click.argument("src_key", required=False)
@click.argument("dst_key", required=False)
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@add_interactive_option
def object_move(src_key: str | None, dst_key: str | None, bucket: str | None, profile: str | None, dry_run: bool, interactive: bool | None) -> None:
    """Move one object, dry-run by default."""

    values = _resolve_inputs(
        schema=COPY_SCHEMA,
        provided={"src_key": src_key, "dst_key": dst_key},
        interactive=interactive,
        usage="Usage: chatqiniu object move SRC_KEY DST_KEY [--execute]",
    )
    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    result = _client(profile).object_move(bucket=selected_bucket, src_key=values["src_key"], dst_key=values["dst_key"], dry_run=dry_run)
    _maybe_render_dry_run(result)


@object.command("batch-delete")
@click.option("--prefix", required=True, help="Prefix selector")
@click.option("--bucket", help="Bucket override")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@click.option("--yes", is_flag=True, help="Required with --execute")
def object_batch_delete(prefix: str, bucket: str | None, profile: str | None, dry_run: bool, yes: bool) -> None:
    """Batch delete keys by prefix, dry-run by default."""

    if not dry_run and not yes:
        raise click.ClickException("Use --yes together with --execute for destructive operations.")
    settings = _get_settings(profile)
    selected_bucket = settings.require_bucket(bucket)
    listing = _client(profile).object_list(bucket=selected_bucket, prefix=prefix, limit=1000)
    keys = _collect_keys_from_list_result(listing)
    result = _client(profile).object_batch_delete(bucket=selected_bucket, keys=keys, dry_run=dry_run)
    _maybe_render_dry_run(result)


@main.group()
def url() -> None:
    """Generate object URLs."""


@url.command("public")
@click.argument("key", required=False)
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--url-prefix", default=None)
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
@add_interactive_option
def url_public(key: str | None, profile: str | None, url_prefix: str | None, output_format: str, interactive: bool | None) -> None:
    """Generate a public object URL."""

    values = _resolve_inputs(schema=URL_SCHEMA, provided={"key": key}, interactive=interactive, usage="Usage: chatqiniu url public KEY")
    settings = _get_settings(profile)
    prefix = settings.require_url_prefix(url_prefix)
    payload = {"key": values["key"], "url": _client(profile).public_url(key=values["key"], url_prefix=prefix)}
    render_data(payload, output_format=output_format)


@url.command("private")
@click.argument("key", required=False)
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--url-prefix", default=None)
@click.option("--expires", default=3600, type=int, show_default=True)
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
@add_interactive_option
def url_private(key: str | None, profile: str | None, url_prefix: str | None, expires: int, output_format: str, interactive: bool | None) -> None:
    """Generate a private signed object URL."""

    values = _resolve_inputs(schema=URL_SCHEMA, provided={"key": key}, interactive=interactive, usage="Usage: chatqiniu url private KEY")
    settings = _get_settings(profile)
    prefix = settings.require_url_prefix(url_prefix)
    payload = {"key": values["key"], "url": _client(profile).private_url(key=values["key"], url_prefix=prefix, expires=expires), "expires": expires}
    render_data(payload, output_format=output_format)


@main.group()
def cdn() -> None:
    """CDN refresh and prefetch."""


@cdn.command("refresh")
@click.option("--url", "urls", multiple=True, help="One or more URLs")
@click.option("--dir", "dirs", multiple=True, help="One or more directory URLs")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
def cdn_refresh(urls: tuple[str, ...], dirs: tuple[str, ...], profile: str | None, dry_run: bool) -> None:
    """Refresh CDN cache entries."""

    if not urls and not dirs:
        raise click.ClickException("At least one --url or --dir is required.")
    result = _fusion_client(profile).cdn_refresh(urls=list(urls), dirs=list(dirs), dry_run=dry_run)
    _maybe_render_dry_run(result)


@cdn.command("prefetch")
@click.option("--url", "urls", multiple=True, help="One or more URLs")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
def cdn_prefetch(urls: tuple[str, ...], profile: str | None, dry_run: bool) -> None:
    """Prefetch CDN resources."""

    if not urls:
        raise click.ClickException("At least one --url is required.")
    result = _fusion_client(profile).cdn_prefetch(urls=list(urls), dry_run=dry_run)
    _maybe_render_dry_run(result)


@cdn.command("task")
@click.argument("task_id")
@click.option("--kind", type=click.Choice(["refresh", "prefetch"]), default="refresh")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def cdn_task(task_id: str, kind: str, profile: str | None, output_format: str) -> None:
    """Query CDN task status."""

    render_data(_fusion_client(profile).cdn_task(task_id=task_id, kind=kind), output_format=output_format)


@main.group()
def cert() -> None:
    """Inspect and manage CDN certificates."""


@cert.command("upload")
@click.option("--name", required=False)
@click.option("--cert-chain", required=False, help="PEM chain path")
@click.option("--private-key", required=False, help="PEM private key path")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@add_interactive_option
def cert_upload(name: str | None, cert_chain: str | None, private_key: str | None, profile: str | None, dry_run: bool, interactive: bool | None) -> None:
    """Upload a certificate, dry-run by default."""

    values = _resolve_inputs(
        schema=CERT_UPLOAD_SCHEMA,
        provided={"name": name, "cert_chain": cert_chain, "private_key": private_key},
        interactive=interactive,
        usage="Usage: chatqiniu cert upload --name NAME --cert-chain CHAIN.pem --private-key KEY.pem",
    )
    chain = Path(values["cert_chain"]).read_text(encoding="utf-8")
    key_text = Path(values["private_key"]).read_text(encoding="utf-8")
    result = _fusion_client(profile).cert_upload(name=values["name"], cert_chain=chain, private_key=key_text, dry_run=dry_run)
    _maybe_render_dry_run(result)


@cert.command("list")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--marker", default=None)
@click.option("--limit", default=100, type=int, show_default=True)
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def cert_list(profile: str | None, marker: str | None, limit: int, output_format: str) -> None:
    """List CDN certificates."""

    data = _fusion_client(profile).cert_list(marker=marker, limit=limit)
    rows = data.get("certs") or data.get("items") or []
    render_data(rows, output_format=output_format)


@cert.command("show")
@click.argument("cert_id")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def cert_show(cert_id: str, profile: str | None, output_format: str) -> None:
    """Show one certificate."""

    render_data(_fusion_client(profile).cert_show(cert_id), output_format=output_format)


@cert.command("delete")
@click.argument("cert_id")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@click.option("--yes", is_flag=True, help="Required with --execute")
def cert_delete(cert_id: str, profile: str | None, dry_run: bool, yes: bool) -> None:
    """Delete one certificate, dry-run by default."""

    if not dry_run and not yes:
        raise click.ClickException("Use --yes together with --execute for destructive operations.")
    result = _fusion_client(profile).cert_delete(cert_id, dry_run=dry_run)
    _maybe_render_dry_run(result)


@main.group()
def domain() -> None:
    """Inspect CDN domains and HTTPS config."""


@domain.command("list")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--marker", default=None)
@click.option("--limit", default=100, type=int, show_default=True)
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def domain_list(profile: str | None, marker: str | None, limit: int, output_format: str) -> None:
    """List CDN domains."""

    data = _fusion_client(profile).domain_list(marker=marker, limit=limit)
    rows = data.get("domains") or data.get("items") or []
    render_data(rows, output_format=output_format)


@domain.command("show")
@click.argument("name")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def domain_show(name: str, profile: str | None, output_format: str) -> None:
    """Show one CDN domain."""

    render_data(_fusion_client(profile).domain_show(name), output_format=output_format)


@domain.group("https")
def domain_https() -> None:
    """Manage domain HTTPS configuration."""


@domain_https.command("set")
@click.argument("domain", required=False)
@click.option("--cert-id", required=False)
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--force-https", is_flag=True, help="Enable force https")
@click.option("--http2/--no-http2", default=True, help="Toggle http2")
@click.option("--dry-run/--execute", default=True, help="Preview by default")
@click.option("--yes", is_flag=True, help="Required with --execute")
@add_interactive_option
def domain_https_set(domain: str | None, cert_id: str | None, profile: str | None, force_https: bool, http2: bool, dry_run: bool, yes: bool, interactive: bool | None) -> None:
    """Set the HTTPS certificate for one domain, dry-run by default."""

    values = _resolve_inputs(
        schema=DOMAIN_HTTPS_SCHEMA,
        provided={"domain": domain, "cert_id": cert_id},
        interactive=interactive,
        usage="Usage: chatqiniu domain https set DOMAIN --cert-id CERT_ID [--execute --yes]",
    )
    if not dry_run and not yes:
        raise click.ClickException("Use --yes together with --execute for destructive operations.")
    result = _fusion_client(profile).domain_https_set(
        domain=values["domain"],
        cert_id=values["cert_id"],
        force_https=force_https,
        http2=http2,
        dry_run=dry_run,
    )
    _maybe_render_dry_run(result)


@main.group()
def doctor() -> None:
    """Run local diagnostics."""


@doctor.command("check")
@click.option("--profile", help="Named ChatEnv profile")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "markdown"]), default="table")
def doctor_check(profile: str | None, output_format: str) -> None:
    """Check local config and read-only API health."""

    settings = _get_settings(profile)
    payload: dict[str, Any] = {
        "profile": settings.profile,
        "env_path": str(settings.env_path or ""),
        "has_credentials": settings.has_credentials,
        "bucket": settings.bucket_name,
        "url_prefix": settings.url_prefix,
        "cdn_domain": settings.cdn_domain,
        "up_host": settings.up_host,
    }
    if settings.has_credentials:
        try:
            payload["bucket_count"] = len(_client(profile).bucket_list())
            payload["api_readonly"] = "ok"
        except Exception as exc:  # pragma: no cover - network depends on environment
            payload["api_readonly"] = f"failed: {exc}"
    render_data(payload, output_format=output_format)


@main.group()
def docs() -> None:
    """Show doc links and examples."""


@docs.command("links")
def docs_links() -> None:
    """Print curated official documentation links."""

    render_key_values(DOC_LINKS)


@docs.command("examples")
def docs_examples() -> None:
    """Print common examples."""

    render_info("chatqiniu auth whoami")
    render_info("chatqiniu bucket list")
    render_info("chatqiniu object list --prefix assets/")
    render_info("chatqiniu cert list")
    render_info("chatqiniu domain show cdn.example.com")


@docs.command("open")
@click.argument("topic")
def docs_open(topic: str) -> None:
    """Print one official document link by topic."""

    url = DOC_LINKS.get(topic)
    if not url:
        raise click.ClickException(f"Unknown topic: {topic}")
    click.echo(url)


def _handle_error(exc: Exception) -> None:
    if isinstance(exc, click.ClickException):
        raise exc
    if isinstance(exc, QiniuApiError):
        render_error(str(exc))
        raise SystemExit(1)
    render_error(str(exc))
    raise SystemExit(1)


if __name__ == "__main__":
    main()
