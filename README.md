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

Chatqiniu 是一个面向七牛云的 ChatArch CLI，统一封装 Kodo 对象存储、CDN、SSL 证书和域名 HTTPS 常见操作。

## 快速开始

```bash
pip install -e ".[dev]"
chatqiniu auth whoami
chatqiniu bucket list
python -m pytest -q
```

## 功能概览

- `auth`：通过 ChatEnv 管理七牛凭证，并做只读身份校验
- `profile` / `config`：管理多环境 profile、默认 bucket、URL 前缀和 CDN 域名
- `bucket` / `object` / `url`：管理对象存储资源、上传目录、查看详情、生成公开或私有 URL
- `cdn` / `cert` / `domain`：管理 CDN 刷新预取、证书列表/上传、域名 HTTPS 配置
- `doctor` / `docs`：本地诊断、官方文档链接和命令示例

## 常用命令

```bash
chatqiniu auth login
chatqiniu auth whoami
chatqiniu config set bucket my-bucket
chatqiniu config set url-prefix https://cdn.example.com
chatqiniu object list --prefix assets/
chatqiniu cert list
chatqiniu domain show cdn.example.com
```

## 配置规范

`Chatqiniu` 遵循当前 ChatArch 约束：

- 凭证和默认配置走 `chatenv>=0.1.1`
- 参数交互走 `chatstyle>=0.1.0`
- 敏感字段必须 masked，不能把真实密钥写进日志、报告或测试快照

默认 Qiniu typed env 路径是：

```text
~/.chatarch/envs/Qiniu/.env
```

## 安全说明

- 删除、证书删除、域名 HTTPS 切换、CDN 刷新/预取等写操作优先支持 dry-run
- 真实执行危险操作时需要显式确认
- 本项目优先实现接口支持，但日常使用尽量先走只读检查和 dry-run

## 目录结构

- `src/`：包源码
- `tests/code-tests/`：代码测试
- `tests/cli-tests/`：真实 CLI 测试
- `tests/mock-cli-tests/`：mock/fake CLI 测试
- `docs/`：长期维护文档，由 mkdocs 构建

## 开发说明

扩展脚手架前，先阅读 `DEVELOP.md` 和 `AGENTS.md`。
