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

Chatqiniu is a ChatArch CLI package for managing Qiniu lightweight apps. This release starts with a local app registry and exposes a `chatenv` provider for Qiniu access key, secret key, API base, and registry path settings.

## Quick Start

```bash
pip install Chatqiniu
chatqiniu add demo --endpoint https://demo.example.com --title "Demo App"
chatqiniu list
chatqiniu show demo
```

For local development:

```bash
pip install -e ".[dev]"
python -m pytest -q
python -m build
```

## CLI

- `chatqiniu add [NAME] --endpoint URL`: add or update a lightweight app.
- `chatqiniu list`: list configured lightweight apps.
- `chatqiniu show [NAME]`: show one app entry.
- `chatqiniu remove [NAME]`: remove one app entry.
- `chatqiniu path`: print the active registry path.

Commands with recoverable missing input follow the ChatStyle contract: `-i` forces interactive mode and `-I` disables prompting and fails fast.

## Configuration

`Chatqiniu` registers a `chatenv.configs` provider:

```bash
chatenv init -t qiniu
chatenv cat -t qiniu
```

Fields:

- `QINIU_ACCESS_KEY`: Qiniu access key, sensitive.
- `QINIU_SECRET_KEY`: Qiniu secret key, sensitive.
- `QINIU_API_BASE`: Qiniu API base URL.
- `CHATQINIU_REGISTRY`: lightweight app registry JSON path.

When `CHATQINIU_REGISTRY` is unset, Chatqiniu uses `~/.chatqiniu/apps.json`.

## Layout

- `src/`: package source code.
- `tests/code-tests/`: code tests and migrated historical tests.
- `tests/cli-tests/`: real CLI tests, doc-first.
- `tests/mock-cli-tests/`: mock/fake CLI tests, doc-first.
- `docs/`: long-lived project docs built by mkdocs.

## Release

Official releases use `vX.Y.Z` tags. PyPI already has `0.0.1` and `0.1.0`; this local package is prepared as `0.1.1`.
