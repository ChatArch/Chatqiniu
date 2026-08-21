# Changelog

## 0.2.3 - 2026-08-22

### Added

- Add registered `chatqiniu --tree-brief` output, tests, and installed console-script CI readbacks.
- Add exact runtime-to-documentation checks for the full and brief CLI trees.

### Changed

- Replace the package-local Click tree renderer with ChatStyle `add_tree_option()` on the explicit `chatqiniu` root.
- Raise the shared runtime bounds to `chatstyle>=0.2.0,<0.3.0` and `chatenv>=0.2.10,<0.3.0`.
- Clarify command-tree descriptions for read-only output, local/remote writes, dry-run behavior, and secret boundaries.
- Guard tag publishing so the release commit must be contained in the default branch.

## 0.2.2 - 2026-08-11

### Added

- Add runtime `chatqiniu --tree` generated from the registered Click command surface for release/readback acceptance.

### Changed

- Remove the leftover template `hello` command from the public CLI surface.
- Update the CLI tree documentation from the live runtime renderer instead of maintaining a hand-written tree.
- Raise the ChatEnv dependency floor to `>=0.2.4,<0.3.0` and keep MkDocs Material in the strict-build-safe `<9.7` window.

## 0.2.1 - 2026-08-05

### Added

- 增加 `chatqiniu cert deploy`：上传本地 PEM 证书后绑定一个或多个 CDN 域名；默认 dry-run，真实执行需要 `--execute --yes`。
- 增加 `chatqiniu.operations.deploy_certificate(...)` 可复用 Python API，供其他 ChatArch 包直接调用证书部署流程。
- 增加 `chatqiniu --version`。
- 增加标准 MkDocs 文档页：CLI 树、能力地图、证书部署流程，并启用中英文 i18n。

### Changed

- 将文档 URL 对齐到 ChatArch 标准公共域名路径 `https://arch.gh.wzhecnu.cn/Chatqiniu/`。
- 为 ChatArch 内部依赖和 MkDocs 文档依赖增加上界。
- 将发布 workflow 收紧为 tag-only，并与 PyPI Trusted Publisher `(Any)` 环境匹配。

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
