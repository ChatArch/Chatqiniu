# Chatqiniu

Chatqiniu is the ChatArch command-line tool for Qiniu Cloud workflows, covering ChatEnv-backed credentials, Kodo object storage, CDN operations, SSL certificates, and CDN domain HTTPS configuration.

- Documentation: https://arch.gh.wzhecnu.cn/Chatqiniu/
- Source repository: https://github.com/ChatArch/Chatqiniu
- Chinese README: [README.md](README.md)

## Quick Start

```bash
pip install -e ".[dev,docs]"
chatqiniu --version
chatqiniu --tree
chatqiniu auth whoami --profile wzh
chatqiniu bucket list --profile wzh
python -m pytest -q
```

## Current Capabilities

| Scenario | Command entry | Notes |
| --- | --- | --- |
| Authentication and profiles | `auth`, `profile`, `config` | Read and write Qiniu credentials and default bucket / CDN domain settings through ChatEnv. |
| Kodo object storage | `bucket`, `object`, `url` | Inspect buckets, list objects, upload/download files, and generate public or private URLs. |
| CDN operations | `cdn` | Refresh, prefetch, and query CDN tasks. |
| Certificates and HTTPS | `cert`, `domain https` | List/upload certificates and bind certificates to CDN domains. High-impact writes default to dry-run. |
| Diagnostics and docs | `doctor`, `docs` | Check local configuration, run read-only API health checks, and print curated official links. |

## Certificate Deployment

`cert deploy` uploads a local PEM certificate to Qiniu and binds the returned certificate ID to one or more CDN domains. It previews by default; real writes require both `--execute` and `--yes`.

```bash
chatqiniu cert deploy \
  --profile wzh \
  --name chatdns-wzhecnu-default-20261028 \
  --cert-chain ~/.chatarch/certs/wzhecnu.cn/default/fullchain.pem \
  --private-key ~/.chatarch/certs/wzhecnu.cn/default/privkey.pem \
  --domain qiniu.wzhecnu.cn \
  --domain qiniu-cdn.wzhecnu.cn \
  --force-https \
  --execute --yes
```

Safety contract: command output does not print certificate bodies, private keys, AccessKeys, or SecretKeys.

## Documentation

- CLI tree: https://arch.gh.wzhecnu.cn/Chatqiniu/cli-tree/
- Capability map: https://arch.gh.wzhecnu.cn/Chatqiniu/capability-map/
- Certificate deployment workflow: https://arch.gh.wzhecnu.cn/Chatqiniu/certificate-workflow/

## Development Checks

```bash
python -m pytest -q
mkdocs build --strict
python -m build
python -m twine check dist/*
```
