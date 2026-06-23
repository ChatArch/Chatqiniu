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

Chatqiniu 是 ChatArch 体系下的七牛轻应用管理 CLI。当前版本先提供本地轻应用清单管理，并通过 `chatenv` 预留七牛 Access Key、Secret Key、API Base 与 registry 路径配置。

## 快速开始

```bash
pip install Chatqiniu
chatqiniu add demo --endpoint https://demo.example.com --title "Demo App"
chatqiniu list
chatqiniu show demo
```

本地开发：

```bash
pip install -e ".[dev]"
python -m pytest -q
python -m build
```

## CLI

- `chatqiniu add [NAME] --endpoint URL`：新增或更新轻应用。
- `chatqiniu list`：列出当前 registry 中的轻应用。
- `chatqiniu show [NAME]`：查看单个轻应用。
- `chatqiniu remove [NAME]`：删除单个轻应用。
- `chatqiniu path`：输出当前 registry 路径。

需要补齐参数的命令支持 ChatStyle 交互规范：`-i` 强制进入交互，`-I` 禁止交互并快速失败。

## 配置

`Chatqiniu` 注册了 `chatenv.configs` provider：

```bash
chatenv init -t qiniu
chatenv cat -t qiniu
```

配置项：

- `QINIU_ACCESS_KEY`：七牛 Access Key，敏感字段。
- `QINIU_SECRET_KEY`：七牛 Secret Key，敏感字段。
- `QINIU_API_BASE`：七牛 API Base URL。
- `CHATQINIU_REGISTRY`：轻应用 registry JSON 文件路径。

如果未设置 `CHATQINIU_REGISTRY`，默认使用 `~/.chatqiniu/apps.json`。

## 目录结构

- `src/`：包源码。
- `tests/code-tests/`：代码测试和历史测试迁移。
- `tests/cli-tests/`：真实 CLI 测试，doc-first。
- `tests/mock-cli-tests/`：mock/fake CLI 测试，doc-first。
- `docs/`：长期维护文档，由 mkdocs 构建。

## 发版

正式发版使用 `vX.Y.Z` tag。PyPI 已存在 `0.0.1` 和 `0.1.0`，当前本地准备版本是 `0.1.1`。
