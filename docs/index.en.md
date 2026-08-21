# Chatqiniu Documentation

Chatqiniu is the ChatArch command-line tool for Qiniu Cloud. It brings Kodo, CDN, SSL certificates, and CDN domain HTTPS configuration into one scriptable, interactive, and safety-first command surface.

## Choose an Entry Point

<div class="grid cards" markdown>

-   **Configure credentials first**

    ---

    Store Qiniu credentials in ChatEnv profiles, select accounts with `--profile`, and keep secrets out of command output.

    [`auth` / `profile` commands](cli-tree.md#authentication-and-profiles)

-   **Inspect object storage**

    ---

    View buckets, list objects, upload/download files, and generate public or private object URLs.

    [`bucket` / `object` / `url` commands](cli-tree.md#object-storage)

-   **Operate CDN**

    ---

    Refresh, prefetch, query tasks, and inspect CDN domain state.

    [`cdn` / `domain` commands](cli-tree.md#cdn-and-domains)

-   **Deploy HTTPS certificates**

    ---

    Upload local PEM certificates and bind them to one or more CDN domains; real writes require explicit confirmation.

    [Certificate deployment workflow](certificate-workflow.md)

</div>

## Safety Defaults

| Capability | Default behavior | Real write requirement |
| --- | --- | --- |
| Delete one object | dry-run | `--execute` |
| Batch delete objects | dry-run | `--execute` |
| CDN refresh/prefetch | dry-run | `--execute` |
| Upload certificate | dry-run | `--execute` |
| Deploy certificate | dry-run | `--execute --yes` |
| Switch domain HTTPS certificate | dry-run | `--execute` |

## Common Commands

```bash
chatqiniu --version
chatqiniu --tree
chatqiniu --tree-brief
chatqiniu auth whoami --profile wzh
chatqiniu bucket list --profile wzh
chatqiniu cert list --profile wzh
chatqiniu domain list --profile wzh
```

See the [CLI tree](cli-tree.md) for command topology and the [capability map](capability-map.md) for package boundaries.
