# Chatqiniu 文档

Chatqiniu 是 ChatArch 的七牛云命令行工具。它把七牛云 Kodo、CDN、SSL 证书和 CDN 域名 HTTPS 配置收敛到一个可脚本化、可交互、默认安全的命令面。

## 入口选择

<div class="grid cards" markdown>

-   **先配置鉴权**

    ---

    使用 ChatEnv profile 保存七牛凭证，日常命令通过 `--profile` 选择账号，不在输出中打印密钥。

    [`auth` / `profile` 命令](cli-tree.md#auth-profile)

-   **查看对象存储**

    ---

    查看 bucket、列对象、上传下载文件，并生成公开或私有对象 URL。

    [`bucket` / `object` / `url` 命令](cli-tree.md#object-storage)

-   **维护 CDN**

    ---

    刷新、预取、查询任务，并查看 CDN 域名当前状态。

    [`cdn` / `domain` 命令](cli-tree.md#cdn-domain)

-   **部署 HTTPS 证书**

    ---

    上传本地 PEM 证书并绑定到一个或多个 CDN 域名；真实写操作必须显式确认。

    [证书部署流程](certificate-workflow.md)

</div>

## 当前安全默认值

| 能力 | 默认行为 | 真实写操作 |
| --- | --- | --- |
| 删除对象 | dry-run | 需要 `--execute` |
| 批量删除对象 | dry-run | 需要 `--execute` |
| CDN 刷新/预取 | dry-run | 需要 `--execute` |
| 上传证书 | dry-run | 需要 `--execute` |
| 部署证书 | dry-run | 需要 `--execute --yes` |
| 切换域名 HTTPS 证书 | dry-run | 需要 `--execute` |

## 常用命令

```bash
chatqiniu --version
chatqiniu auth whoami --profile wzh
chatqiniu bucket list --profile wzh
chatqiniu cert list --profile wzh
chatqiniu domain list --profile wzh
```

更多命令见 [命令树](cli-tree.md)，能力边界见 [能力地图](capability-map.md)。
