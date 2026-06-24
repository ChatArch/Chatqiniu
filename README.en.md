<div align="center">
    <a href="https://pypi.python.org/pypi/Chatqiniu">
        <img src="https://img.shields.io/pypi/v/Chatqiniu.svg" alt="PyPI version" />
    </a>
    <a href="https://github.com/ChatArch/Chatqiniu/actions/workflows/ci.yml">
        <img src="https://github.com/ChatArch/Chatqiniu/actions/workflows/ci.yml/badge.svg" alt="Tests" />
    </a>
    <a href="https://ChatArch.github.io/Chatqiniu">
        <img src="https://img.shields.io/badge/docs-mkdocs-blue.svg" alt="Documentation" />
    </a>
</div>

<div align="center">

[English](README.en.md) | [简体中文](README.md)
</div>

# Chatqiniu

Chatqiniu is a ChatArch CLI for Qiniu Cloud workflows, covering Kodo object storage, CDN, SSL certificates, and domain HTTPS operations behind one command surface.

## Quick Start

```bash
pip install -e ".[dev]"
chatqiniu auth whoami
chatqiniu bucket list
python -m pytest -q
```

## What It Covers

- `auth`: manage Qiniu credentials through ChatEnv and validate them with read-only calls
- `profile` / `config`: manage named profiles, default bucket, public URL prefix, and CDN domain
- `bucket` / `object` / `url`: inspect buckets, upload files, list objects, inspect metadata, and generate public/private URLs
- `cdn` / `cert` / `domain`: CDN refresh/prefetch, certificate list/upload, and domain HTTPS configuration
- `doctor` / `docs`: local diagnostics, official doc links, and command examples

## Common Commands

```bash
chatqiniu auth login
chatqiniu auth whoami
chatqiniu config set bucket my-bucket
chatqiniu config set url-prefix https://cdn.example.com
chatqiniu object list --prefix assets/
chatqiniu cert list
chatqiniu domain show cdn.example.com
```

## Runtime Contract

`Chatqiniu` follows the current ChatArch rules:

- configuration and secrets go through `chatenv>=0.1.1`
- CLI prompting and input resolution go through `chatstyle>=0.1.0`
- sensitive values must stay masked in logs, reports, and test snapshots

The default Qiniu typed env path is:

```text
~/.chatarch/envs/Qiniu/.env
```

## Safety Notes

- delete, certificate delete, domain HTTPS switching, and CDN refresh/prefetch are designed to prefer dry-run-style usage
- high-impact writes should require explicit confirmation
- day-to-day usage should favor read-only inspection and dry-run previews first

## Layout

- `src/`: package source code
- `tests/code-tests/`: code tests
- `tests/cli-tests/`: real CLI tests
- `tests/mock-cli-tests/`: mock/fake CLI tests
- `docs/`: long-lived docs built by mkdocs

## Development Notes

See `DEVELOP.md` and `AGENTS.md` before expanding the scaffold.
