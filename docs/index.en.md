# Chatqiniu Docs

`Chatqiniu` is a ChatArch Python CLI package for managing Qiniu lightweight app entries. This version focuses on a local registry: app name, endpoint, title, and description are stored in a JSON file, leaving room for future Qiniu API integration.

## Install

```bash
pip install Chatqiniu
```

Local development install:

```bash
pip install -e ".[dev,docs]"
```

## Manage Apps

```bash
chatqiniu add demo --endpoint https://demo.example.com --title "Demo App"
chatqiniu list
chatqiniu show demo
chatqiniu remove demo
```

The default registry is `~/.chatqiniu/apps.json`. Override it with an environment variable or command option:

```bash
export CHATQINIU_REGISTRY=/path/to/apps.json
chatqiniu list
chatqiniu list --registry /path/to/apps.json
```

## ChatEnv

`Chatqiniu` registers the `qiniu` config type:

```bash
chatenv init -t qiniu
chatenv cat -t qiniu
```

Fields:

- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`
- `QINIU_API_BASE`
- `CHATQINIU_REGISTRY`

## Local Preview

```bash
mkdocs serve
```

Chinese version: [index.md](index.md).
