# 命令树

本页列出当前 `chatqiniu --tree` 的运行时输出。命令树由 Click 注册命令面生成，不再手写维护；新增、删除或重命名命令时应同步更新测试、文档和可复用 Python API。

```text
chatqiniu # chatqiniu command line interface
├── --help # Show this message and exit
├── --version # Show the package version
├── --tree # Show the registered CLI command tree
├── auth # Credential bootstrap and identity checks
│   ├── login [--access-key ACCESS-KEY] [--secret-key SECRET-KEY] [--profile PROFILE] [--interactive] # Save credentials into ChatEnv-managed Qiniu config
│   ├── logout [--profile PROFILE] [--yes] # Clear active credentials or remove a named profile
│   └── whoami [--profile PROFILE] [--format OUTPUT-FORMAT] # Validate current credentials with a read-only bucket listing
├── profile # Manage named ChatEnv profiles
│   ├── list # List named Qiniu profiles
│   ├── show [NAME] # Show the active or named profile
│   ├── use NAME # Activate a named profile
│   ├── create NAME [--copy-active] # Create a named profile
│   └── delete NAME [--yes] # Delete a named profile
├── config # Manage default Qiniu settings in ChatEnv
│   ├── list [--profile PROFILE] # List non-sensitive config values
│   ├── get KEY [--profile PROFILE] # Get one config value
│   ├── set KEY VALUE [--profile PROFILE] # Set one config value
│   └── unset KEY [--profile PROFILE] # Unset one config value
├── bucket # Inspect Kodo buckets
│   ├── list [--profile PROFILE] [--format OUTPUT-FORMAT] # List accessible buckets
│   └── show [NAME] [--profile PROFILE] [--format OUTPUT-FORMAT] # Show simple bucket information
├── object # Manage Kodo objects
│   ├── upload [LOCAL-FILE] [--key KEY] [--bucket BUCKET] [--profile PROFILE] [--overwrite] [--skip-existing] [--dry-run] [--interactive] # Upload one local file
│   ├── upload-dir [LOCAL-DIR] [--prefix PREFIX] [--bucket BUCKET] [--profile PROFILE] [--overwrite] [--skip-existing] [--dry-run] [--interactive] # Upload a directory recursively
│   ├── download KEY [--out OUTPUT-PATH] [--profile PROFILE] [--bucket BUCKET] [--private] [--expires EXPIRES] # Download an object via generated URL
│   ├── list [--prefix PREFIX] [--bucket BUCKET] [--profile PROFILE] [--limit LIMIT] [--marker MARKER] [--delimiter DELIMITER] [--format OUTPUT-FORMAT] # List objects in one bucket
│   ├── stat KEY [--bucket BUCKET] [--profile PROFILE] [--format OUTPUT-FORMAT] # Show object metadata
│   ├── delete [KEY] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--yes] [--interactive] # Delete one object, dry-run by default
│   ├── copy [SRC-KEY] [DST-KEY] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--interactive] # Copy one object, dry-run by default
│   ├── move [SRC-KEY] [DST-KEY] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--interactive] # Move one object, dry-run by default
│   └── batch-delete [--prefix PREFIX] [--bucket BUCKET] [--profile PROFILE] [--dry-run] [--yes] # Batch delete keys by prefix, dry-run by default
├── url # Generate object URLs
│   ├── public [KEY] [--profile PROFILE] [--url-prefix URL-PREFIX] [--format OUTPUT-FORMAT] [--interactive] # Generate a public object URL
│   └── private [KEY] [--profile PROFILE] [--url-prefix URL-PREFIX] [--expires EXPIRES] [--format OUTPUT-FORMAT] [--interactive] # Generate a private signed object URL
├── cdn # CDN refresh and prefetch
│   ├── refresh [--url URLS] [--dir DIRS] [--profile PROFILE] [--dry-run] # Refresh CDN cache entries
│   ├── prefetch [--url URLS] [--profile PROFILE] [--dry-run] # Prefetch CDN resources
│   └── task TASK-ID [--kind KIND] [--profile PROFILE] [--format OUTPUT-FORMAT] # Query CDN task status
├── cert # Inspect and manage CDN certificates
│   ├── upload [--name NAME] [--cert-chain CERT-CHAIN] [--private-key PRIVATE-KEY] [--profile PROFILE] [--dry-run] [--interactive] # Upload a certificate, dry-run by default
│   ├── deploy [--name NAME] [--cert-chain CERT-CHAIN] [--private-key PRIVATE-KEY] [--domain DOMAINS] [--profile PROFILE] [--force-https] [--http2] [--dry-run] [--yes] [--format OUTPUT-FORMAT] [--interactive] # Upload a certificate and bind it to one or more CDN domains
│   ├── list [--profile PROFILE] [--marker MARKER] [--limit LIMIT] [--format OUTPUT-FORMAT] # List CDN certificates
│   ├── show CERT-ID [--profile PROFILE] [--format OUTPUT-FORMAT] # Show one certificate
│   └── delete CERT-ID [--profile PROFILE] [--dry-run] [--yes] # Delete one certificate, dry-run by default
├── domain # Inspect CDN domains and HTTPS config
│   ├── list [--profile PROFILE] [--marker MARKER] [--limit LIMIT] [--format OUTPUT-FORMAT] # List CDN domains
│   ├── show NAME [--profile PROFILE] [--format OUTPUT-FORMAT] # Show one CDN domain
│   └── https # Manage domain HTTPS configuration
│       └── set [DOMAIN] [--cert-id CERT-ID] [--profile PROFILE] [--force-https] [--http2] [--dry-run] [--yes] [--interactive] # Set the HTTPS certificate for one domain, dry-run by default
├── doctor # Run local diagnostics
│   └── check [--profile PROFILE] [--format OUTPUT-FORMAT] # Check local config and read-only API health
└── docs # Show doc links and examples
    ├── links # Print curated official documentation links
    ├── examples # Print common examples
    └── open TOPIC # Print one official document link by topic
```

`cert deploy` 的真实执行需要 `--execute --yes`，并且不会在输出中打印证书正文或私钥内容。完整流程见 [证书部署](certificate-workflow.md)。
## 鉴权与 profile {#auth-profile}

见上方 runtime tree 中的 `auth`、`profile` 和 `config` 分支。

## 对象存储 {#object-storage}

见上方 runtime tree 中的 `bucket`、`object` 和 `url` 分支。

## CDN 与域名 {#cdn-domain}

见上方 runtime tree 中的 `cdn`、`cert` 和 `domain https` 分支。
