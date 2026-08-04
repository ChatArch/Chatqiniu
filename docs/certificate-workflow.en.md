# Certificate Deployment

`chatqiniu cert deploy` uploads an existing PEM certificate to Qiniu and binds the returned certificate ID to one or more CDN domains. It is designed for synchronizing certificates issued by ChatDNS or another ACME workflow into Qiniu CDN.

## When to Use It

<div class="grid cards" markdown>

-   **A certificate already exists**

    ---

    You have local `fullchain.pem` and `privkey.pem` files and need to sync them to Qiniu.

-   **Multiple CDN domains share one certificate**

    ---

    One matching wildcard certificate can be bound to multiple CDN domains.

-   **Preview before writing**

    ---

    The command defaults to dry-run; real writes require `--execute --yes`.

</div>

## Preflight Checks

```bash
chatqiniu doctor check --profile wzh --format json
chatqiniu cert list --profile wzh --format json
chatqiniu domain list --profile wzh --format json
```

Check the following:

| Item | Expected state |
| --- | --- |
| `has_credentials` | `true` |
| read-only bucket check | succeeds |
| CDN domains | target domains exist |
| certificate material | local PEM files cover the target domains |

## Preview Deployment

```bash
chatqiniu cert deploy \
  --profile wzh \
  --name chatdns-wzhecnu-default-20261028 \
  --cert-chain ~/.chatarch/certs/wzhecnu.cn/default/fullchain.pem \
  --private-key ~/.chatarch/certs/wzhecnu.cn/default/privkey.pem \
  --domain qiniu.wzhecnu.cn \
  --domain qiniu-cdn.wzhecnu.cn \
  --force-https
```

The preview output shows action summaries only. It does not print certificate bodies or private keys.

## Execute Deployment

After confirming the target domains and certificate name, run the write path:

```bash
chatqiniu cert deploy \
  --profile wzh \
  --name chatdns-wzhecnu-default-20261028 \
  --cert-chain ~/.chatarch/certs/wzhecnu.cn/default/fullchain.pem \
  --private-key ~/.chatarch/certs/wzhecnu.cn/default/privkey.pem \
  --domain qiniu.wzhecnu.cn \
  --domain qiniu-cdn.wzhecnu.cn \
  --force-https \
  --execute --yes \
  --format json
```

The result includes the new certificate ID and a response summary for each domain.

## Readback Verification

```bash
chatqiniu domain show qiniu.wzhecnu.cn --profile wzh --format json
chatqiniu domain show qiniu-cdn.wzhecnu.cn --profile wzh --format json
```

Also verify the public TLS certificate after CDN propagation. Chatqiniu owns the Qiniu API update path; certificate fingerprint, SAN, and expiration readback can be verified with system `openssl` or browser network inspection.

## Failure Handling

| Symptom | Handling |
| --- | --- |
| Missing credentials | Configure ChatEnv or select the correct `--profile` first. |
| Upload response has no certificate ID | Stop before binding and keep the upload response for debugging. |
| Some domain bindings fail | Identify failed domains from the result; do not delete old certificates before fixing or retrying failed items. |
| Public TLS still shows the old certificate | Check Qiniu management state first, then allow CDN propagation; do not repeatedly upload the same certificate. |

## Safety Requirements

- Do not write AccessKeys, SecretKeys, private keys, or certificate bodies into logs, reports, PR descriptions, or docs.
- Use `--profile` to make the target account explicit instead of relying on the active profile.
- For production CDN domains, dry-run first and add `--execute --yes` only after confirming the domain list.
