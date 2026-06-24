# Changelog

## 2026-06-24

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
