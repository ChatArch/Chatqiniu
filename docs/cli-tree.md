# 命令树

`chatqiniu --version` 输出包版本。Chatqiniu 使用共享的 `chatstyle.add_tree_option()` 从真实 Click 注册表生成命令树：`chatqiniu --tree` 保留参数签名，`chatqiniu --tree-brief` 保留相同节点和用途说明但省略签名。

## 完整树

```text
chatqiniu
├── --help  # Show this message and exit.
├── --version  # Show the version and exit.
├── --tree  # Print the registered CLI tree and exit.
├── --tree-brief  # Print the registered CLI tree without parameter signatures and exit.
├── auth  # Manage credentials and run masked read-only identity checks.
│   ├── login [--access-key ACCESS-KEY] [--secret-key SECRET-KEY] [--profile PROFILE] [--interactive]  # Write credentials to a ChatEnv profile without printing secret values.
│   ├── logout [--profile PROFILE] [--yes]  # Clear stored credentials after explicit confirmation.
│   └── whoami [--profile PROFILE] [--format OUTPUT-FORMAT]  # Validate credentials with a read-only request and print a masked summary.
├── bucket  # Inspect Qiniu Kodo buckets with read-only requests.
│   ├── list [--profile PROFILE] [--format OUTPUT-FORMAT]  # List accessible buckets with a read-only request.
│   └── show [NAME] [--profile PROFILE] [--format OUTPUT-FORMAT]  # Check one bucket against the read-only accessible-bucket list.
├── cdn  # Refresh, prefetch, and inspect CDN tasks; writes preview by default.
│   ├── prefetch [--url URLS] [--profile PROFILE] [--dry-run]  # Preview CDN prefetch requests; --execute submits remote writes.
│   ├── refresh [--url URLS] [--dir DIRS] [--profile PROFILE] [--dry-run]  # Preview CDN refresh requests; --execute submits remote writes.
│   └── task <TASK-ID> [--kind KIND] [--profile PROFILE] [--format OUTPUT-FORMAT]  # Print CDN task status from a read-only request.
├── cert  # Read and mutate CDN certificates; writes preview by default.
│   ├── delete <CERT-ID> [--profile PROFILE] [--dry-run] [--yes]  # Preview certificate deletion; --execute --yes writes remotely.
│   ├── deploy [--name NAME] [--cert-chain CERT-CHAIN] [--private-key PRIVATE-KEY] [--domain DOMAINS] [--profile PROFILE] [--force-https] [--http2] [--dry-run] [--yes] [--format OUTPUT-FORMAT] [--interactive]  # Preview certificate deployment; --execute --yes writes remotely.
│   ├── list [--profile PROFILE] [--marker MARKER] [--limit LIMIT] [--format OUTPUT-FORMAT]  # List certificate metadata with a read-only request.
│   ├── show <CERT-ID> [--profile PROFILE] [--format OUTPUT-FORMAT]  # Print certificate metadata from a read-only request.
│   └── upload [--name NAME] [--cert-chain CERT-CHAIN] [--private-key PRIVATE-KEY] [--profile PROFILE] [--dry-run] [--interactive]  # Preview certificate upload; --execute sends local PEM data.
├── config  # Read and write non-secret Qiniu defaults in ChatEnv.
│   ├── get <KEY> [--profile PROFILE]  # Print one supported non-secret config value.
│   ├── list [--profile PROFILE]  # Print masked settings for the active or named profile.
│   ├── set <KEY> <VALUE> [--profile PROFILE]  # Write one supported non-secret config value.
│   └── unset <KEY> [--profile PROFILE]  # Clear one supported non-secret config value.
├── docs  # Print bundled documentation links and examples.
│   ├── examples  # Print common command examples without running them.
│   ├── links  # Print curated official links without network requests.
│   └── open <TOPIC>  # Print one official document URL without opening a browser.
├── doctor  # Run local and read-only remote diagnostics.
│   └── check [--profile PROFILE] [--format OUTPUT-FORMAT]  # Print masked config health and optional read-only API status.
├── domain  # Inspect domains and manage HTTPS; writes preview by default.
│   ├── https  # Manage domain HTTPS bindings; writes preview by default.
│   │   └── set [DOMAIN] [--cert-id CERT-ID] [--profile PROFILE] [--force-https] [--http2] [--dry-run] [--yes] [--interactive]  # Preview an HTTPS binding; --execute --yes writes remotely.
│   ├── list [--profile PROFILE] [--marker MARKER] [--limit LIMIT] [--format OUTPUT-FORMAT]  # List CDN domains with a read-only request.
│   └── show <NAME> [--profile PROFILE] [--format OUTPUT-FORMAT]  # Print one CDN domain from a read-only request.
├── object  # Read and mutate Kodo objects; destructive commands preview by default.
│   ├── batch-delete [--prefix PREFIX] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--yes]  # Preview prefix deletion; --execute --yes mutates remote storage.
│   ├── copy [SRC-KEY] [DST-KEY] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--interactive]  # Preview an object copy; --execute mutates remote storage.
│   ├── delete [KEY] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--yes] [--interactive]  # Preview object deletion; --execute --yes mutates remote storage.
│   ├── download <KEY> [--out OUTPUT-PATH] [--profile PROFILE] [--bucket BUCKET] [--private] [--expires EXPIRES]  # Download one object and write it to --out.
│   ├── list [--prefix PREFIX] [--bucket BUCKET] [--profile PROFILE] [--limit LIMIT] [--marker MARKER] [--delimiter DELIMITER] [--format OUTPUT-FORMAT]  # List objects in one bucket with a read-only request.
│   ├── move [SRC-KEY] [DST-KEY] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--interactive]  # Preview an object move; --execute mutates remote storage.
│   ├── stat <KEY> [--bucket BUCKET] [--profile PROFILE] [--format OUTPUT-FORMAT]  # Print object metadata from a read-only request.
│   ├── upload [LOCAL-FILE] [--key KEY] [--bucket BUCKET] [--profile PROFILE] [--overwrite] [--skip-existing] [--dry-run] [--interactive]  # Upload one local file to Kodo; writes remote storage unless --dry-run.
│   └── upload-dir [LOCAL-DIR] [--prefix PREFIX] [--bucket BUCKET] [--profile PROFILE] [--overwrite] [--skip-existing] [--dry-run] [--interactive]  # Upload a directory to Kodo; writes remote storage unless --dry-run.
├── profile  # Read and write named ChatEnv profiles.
│   ├── create <NAME> [--copy-active]  # Create a named profile, optionally copying active settings.
│   ├── delete <NAME> [--yes]  # Delete a named profile after explicit confirmation.
│   ├── list  # List profile names without reading credential values.
│   ├── show [NAME]  # Print masked settings for the active or named profile.
│   └── use <NAME>  # Copy a named profile into active ChatEnv storage.
└── url  # Generate object URLs without mutating remote storage.
    ├── private [KEY] [--profile PROFILE] [--url-prefix URL-PREFIX] [--expires EXPIRES] [--format OUTPUT-FORMAT] [--interactive]  # Print a signed object URL; treat the output as sensitive.
    └── public [KEY] [--profile PROFILE] [--url-prefix URL-PREFIX] [--format OUTPUT-FORMAT] [--interactive]  # Print a public object URL.
```

## 简版树

```text
chatqiniu
├── --help  # Show this message and exit.
├── --version  # Show the version and exit.
├── --tree  # Print the registered CLI tree and exit.
├── --tree-brief  # Print the registered CLI tree without parameter signatures and exit.
├── auth  # Manage credentials and run masked read-only identity checks.
│   ├── login  # Write credentials to a ChatEnv profile without printing secret values.
│   ├── logout  # Clear stored credentials after explicit confirmation.
│   └── whoami  # Validate credentials with a read-only request and print a masked summary.
├── bucket  # Inspect Qiniu Kodo buckets with read-only requests.
│   ├── list  # List accessible buckets with a read-only request.
│   └── show  # Check one bucket against the read-only accessible-bucket list.
├── cdn  # Refresh, prefetch, and inspect CDN tasks; writes preview by default.
│   ├── prefetch  # Preview CDN prefetch requests; --execute submits remote writes.
│   ├── refresh  # Preview CDN refresh requests; --execute submits remote writes.
│   └── task  # Print CDN task status from a read-only request.
├── cert  # Read and mutate CDN certificates; writes preview by default.
│   ├── delete  # Preview certificate deletion; --execute --yes writes remotely.
│   ├── deploy  # Preview certificate deployment; --execute --yes writes remotely.
│   ├── list  # List certificate metadata with a read-only request.
│   ├── show  # Print certificate metadata from a read-only request.
│   └── upload  # Preview certificate upload; --execute sends local PEM data.
├── config  # Read and write non-secret Qiniu defaults in ChatEnv.
│   ├── get  # Print one supported non-secret config value.
│   ├── list  # Print masked settings for the active or named profile.
│   ├── set  # Write one supported non-secret config value.
│   └── unset  # Clear one supported non-secret config value.
├── docs  # Print bundled documentation links and examples.
│   ├── examples  # Print common command examples without running them.
│   ├── links  # Print curated official links without network requests.
│   └── open  # Print one official document URL without opening a browser.
├── doctor  # Run local and read-only remote diagnostics.
│   └── check  # Print masked config health and optional read-only API status.
├── domain  # Inspect domains and manage HTTPS; writes preview by default.
│   ├── https  # Manage domain HTTPS bindings; writes preview by default.
│   │   └── set  # Preview an HTTPS binding; --execute --yes writes remotely.
│   ├── list  # List CDN domains with a read-only request.
│   └── show  # Print one CDN domain from a read-only request.
├── object  # Read and mutate Kodo objects; destructive commands preview by default.
│   ├── batch-delete  # Preview prefix deletion; --execute --yes mutates remote storage.
│   ├── copy  # Preview an object copy; --execute mutates remote storage.
│   ├── delete  # Preview object deletion; --execute --yes mutates remote storage.
│   ├── download  # Download one object and write it to --out.
│   ├── list  # List objects in one bucket with a read-only request.
│   ├── move  # Preview an object move; --execute mutates remote storage.
│   ├── stat  # Print object metadata from a read-only request.
│   ├── upload  # Upload one local file to Kodo; writes remote storage unless --dry-run.
│   └── upload-dir  # Upload a directory to Kodo; writes remote storage unless --dry-run.
├── profile  # Read and write named ChatEnv profiles.
│   ├── create  # Create a named profile, optionally copying active settings.
│   ├── delete  # Delete a named profile after explicit confirmation.
│   ├── list  # List profile names without reading credential values.
│   ├── show  # Print masked settings for the active or named profile.
│   └── use  # Copy a named profile into active ChatEnv storage.
└── url  # Generate object URLs without mutating remote storage.
    ├── private  # Print a signed object URL; treat the output as sensitive.
    └── public  # Print a public object URL.
```

运行时验收命令：

```bash
chatqiniu --version
chatqiniu --tree
chatqiniu --tree-brief
```

`cert deploy` 的真实执行需要 `--execute --yes`，并且不会在输出中打印证书正文或私钥内容。完整流程见 [证书部署](certificate-workflow.md)。
## 鉴权与 profile {#auth-profile}

见上方 runtime tree 中的 `auth`、`profile` 和 `config` 分支。

## 对象存储 {#object-storage}

见上方 runtime tree 中的 `bucket`、`object` 和 `url` 分支。

## CDN 与域名 {#cdn-domain}

见上方 runtime tree 中的 `cdn`、`cert` 和 `domain https` 分支。
