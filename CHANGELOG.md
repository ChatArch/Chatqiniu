# Changelog

## 未发布

### Added

- 增加 `chatqiniu cert deploy`：上传本地 PEM 证书后绑定一个或多个 CDN 域名；默认 dry-run，真实执行需要 `--execute --yes`。
- 增加 `chatqiniu.operations.deploy_certificate(...)` 可复用 Python API，供其他 ChatArch 包直接调用证书部署流程。
- 增加 `chatqiniu --version`。
- 增加标准 MkDocs 文档页：CLI 树、能力地图、证书部署流程，并启用中英文 i18n。

### Changed

- 将文档 URL 对齐到 ChatArch 标准公共域名路径 `https://arch.gh.wzhecnu.cn/Chatqiniu/`。
- 为 ChatArch 内部依赖和 MkDocs 文档依赖增加上界。

## 0.2.0 - 2026-06-24

### Added

- Add a ChatEnv-backed `QiniuConfig` schema and config helpers so Qiniu credentials and defaults live under `~/.chatarch/envs/Qiniu/.env`.
- Add Kodo, Fusion CDN, certificate, and domain API client wrappers with dry-run support for high-impact write operations.
- Add a multi-group `chatqiniu` CLI covering `auth`, `profile`, `config`, `bucket`, `object`, `url`, `cdn`, `cert`, `domain`, `doctor`, and `docs`.
- Add code tests for ChatEnv profile/config behavior and mock CLI tests for representative command flows.

### Changed

- Update `README.md`, `README.en.md`, and `docs/` to describe the real Qiniu CLI surface instead of the template-only `hello` example.
- Register `chatqiniu.config` as a `chatenv.configs` provider and add `requests` as a runtime dependency.
- Keep a backward-compatible `hello` command so the template smoke test still passes.

### Fixed

- N/A

## 2026-06-23

### Added

- Prepare the patch Chatqiniu release, version `0.1.1`, for tokenless PyPI publishing through the ChatArch GitHub workflow.

### Changed

- Keep this patch release on the plain ChatArch template; real Qiniu cloud/light-app API integration is intentionally not included yet.

### Fixed

- N/A
