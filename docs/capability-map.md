# 能力地图

## Chatqiniu 负责什么

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 七牛鉴权 | 已实现 | 通过 ChatEnv active 或命名 profile 读取 AccessKey / SecretKey，输出敏感值脱敏。 |
| Kodo bucket 查看 | 已实现 | 读取可访问 bucket 和基础信息。 |
| Kodo 对象操作 | 已实现 | 支持列出、查看、上传、下载、复制、移动和删除；删除/复制/移动默认 dry-run。 |
| URL 生成 | 已实现 | 支持公开 URL 和私有签名 URL。 |
| CDN 刷新/预取 | 已实现 | 支持 URL 或目录刷新/预取，默认 dry-run。 |
| CDN 任务查询 | 已实现 | 查询七牛 CDN 任务状态。 |
| 证书查看/上传 | 已实现 | 支持列出、查看和上传 CDN 证书，上传默认 dry-run。 |
| 证书部署 | 已实现 | `cert deploy` 上传证书后绑定多个 CDN 域名，默认 dry-run，真实执行需要 `--execute --yes`。 |
| 域名 HTTPS 切换 | 已实现 | `domain https set` 绑定已有证书，默认 dry-run。 |
| 本地诊断 | 已实现 | 检查配置来源、凭证存在性和只读 API 健康。 |

## 边界

- Chatqiniu 不签发证书；证书材料来自 ChatDNS、ACME 客户端或其他证书系统。
- Chatqiniu 不保存证书正文或私钥；命令只从用户指定路径读取并传给七牛接口。
- Chatqiniu 不管理 DNS 解析；DNS 记录归 ChatDNS 或 DNS provider 工具管理。
- Chatqiniu 不把 ChatEnv profile 自动导出成 shell 环境变量；它由包内配置加载逻辑读取。

## 安全契约

| 风险点 | 处理方式 |
| --- | --- |
| AccessKey / SecretKey 泄露 | profile 展示和诊断输出只显示脱敏值或布尔状态。 |
| 证书私钥泄露 | dry-run 和真实执行结果不打印 PEM 正文。 |
| 意外删除对象 | 删除类命令默认 dry-run，真实执行需 `--execute`。 |
| 意外切换 CDN 域名证书 | `cert deploy` 默认 dry-run，真实执行需 `--execute --yes`。 |
| 自动化调用难以解析 | 主要列表/查看/部署命令支持 JSON 输出。 |

## 可复用接口

`chatqiniu.operations.deploy_certificate(...)` 是 `cert deploy` 背后的可复用 Python API。其他 ChatArch 包可以直接调用该函数，而不是 shell 出 `chatqiniu cert deploy`。
