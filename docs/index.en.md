# Chatqiniu Docs

Long-lived documentation for `Chatqiniu` lives here.

## Current Capability Surface

- `auth`: credential login, cleanup, and read-only identity checks
- `profile` / `config`: ChatEnv profile management and default bucket / url-prefix / cdn-domain settings
- `bucket` / `object` / `url`: object storage inspection, upload, delete dry-run, and URL generation
- `cdn` / `cert` / `domain`: CDN refresh/prefetch, certificate list/upload, and domain HTTPS dry-run flows
- `doctor` / `docs`: local diagnostics and official documentation index

## Common Examples

```bash
chatqiniu auth whoami
chatqiniu bucket list
chatqiniu object list --prefix assets/
chatqiniu cert list
chatqiniu domain show cdn.example.com
```

## Local Preview

```bash
pip install -e ".[docs]"
mkdocs serve
```

Chinese version: [index.md](index.md).
