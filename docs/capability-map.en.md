# Capability Map

## What Chatqiniu Owns

| Capability | Status | Notes |
| --- | --- | --- |
| Qiniu authentication | Implemented | Reads AccessKey / SecretKey from ChatEnv active or named profiles and masks sensitive output. |
| Kodo bucket inspection | Implemented | Reads accessible buckets and basic bucket information. |
| Kodo object operations | Implemented | Supports list, stat, upload, download, copy, move, and delete; delete/copy/move default to dry-run. |
| URL generation | Implemented | Supports public URLs and private signed URLs. |
| CDN refresh/prefetch | Implemented | Supports URL and directory refresh/prefetch, dry-run by default. |
| CDN task lookup | Implemented | Reads Qiniu CDN task status. |
| Certificate inspection/upload | Implemented | Lists, shows, and uploads CDN certificates; upload defaults to dry-run. |
| Certificate deployment | Implemented | `cert deploy` uploads a certificate and binds multiple CDN domains, dry-run by default; real writes require `--execute --yes`. |
| Domain HTTPS switching | Implemented | `domain https set` binds an existing certificate, dry-run by default. |
| Local diagnostics | Implemented | Checks config source, credential presence, and read-only API health. |

## Boundaries

- Chatqiniu does not issue certificates; certificate material comes from ChatDNS, an ACME client, or another certificate system.
- Chatqiniu does not persist certificate bodies or private keys; commands read paths supplied by the caller and send the material to Qiniu APIs.
- Chatqiniu does not manage DNS records; DNS remains owned by ChatDNS or DNS provider tooling.
- Chatqiniu does not export ChatEnv profiles as shell environment variables; the package reads them through its configuration loader.

## Safety Contract

| Risk | Handling |
| --- | --- |
| AccessKey / SecretKey leakage | Profile and diagnostic output shows masked values or booleans only. |
| Private key leakage | Dry-run and real execution results do not print PEM bodies. |
| Accidental object deletion | Delete commands default to dry-run and require `--execute` for writes. |
| Accidental CDN certificate switch | `cert deploy` defaults to dry-run and requires `--execute --yes` for real writes. |
| Automation parsing | Primary list/show/deploy commands support JSON output. |

## Reusable Interface

`chatqiniu.operations.deploy_certificate(...)` is the reusable Python API behind `cert deploy`. Other ChatArch packages can call it directly instead of shelling out to `chatqiniu cert deploy`.
