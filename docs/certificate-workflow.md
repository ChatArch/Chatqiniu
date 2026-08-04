# 证书部署

`chatqiniu cert deploy` 用于把已有 PEM 证书上传到七牛，并将返回的证书 ID 绑定到一个或多个 CDN 域名。它适合把 ChatDNS 或其他 ACME 工具签发好的证书同步到七牛 CDN。

## 适用场景

<div class="grid cards" markdown>

-   **证书已签发**

    ---

    本地已有 `fullchain.pem` 和 `privkey.pem`，需要同步到七牛。

-   **多个 CDN 域名复用同一张证书**

    ---

    一个 wildcard 证书可以绑定多个匹配的 CDN 域名。

-   **先预览再执行**

    ---

    默认 dry-run；真实写操作必须显式加 `--execute --yes`。

</div>

## 前置检查

```bash
chatqiniu doctor check --profile wzh --format json
chatqiniu cert list --profile wzh --format json
chatqiniu domain list --profile wzh --format json
```

检查目标：

| 项目 | 期望 |
| --- | --- |
| `has_credentials` | `true` |
| bucket 只读检查 | 可读 |
| CDN 域名 | 目标域名存在 |
| 证书材料 | 本地 PEM 文件覆盖目标域名 |

## 预览部署

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

预览输出只展示动作摘要，不展示证书正文或私钥。

## 真实执行

确认目标域名和证书名称后，再执行真实写操作：

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

返回结果包含新证书 ID 和每个域名的接口响应摘要。

## 回读验证

```bash
chatqiniu domain show qiniu.wzhecnu.cn --profile wzh --format json
chatqiniu domain show qiniu-cdn.wzhecnu.cn --profile wzh --format json
```

还应从公网 TLS 回读确认证书已切换。Chatqiniu 负责七牛接口操作；公网证书指纹、SAN 和到期时间可用系统 `openssl` 或浏览器网络检查确认。

## 失败处理

| 现象 | 处理 |
| --- | --- |
| 缺少凭证 | 先通过 ChatEnv 配置或选择正确 `--profile`。 |
| 七牛返回缺少证书 ID | 停止绑定，保留上传响应用于排查。 |
| 部分域名绑定失败 | 使用返回结果确认失败域名；不要删除旧证书，先修复域名配置或重试失败项。 |
| 公网仍显示旧证书 | 先看七牛管理面状态，再等待 CDN 配置传播；不要重复上传同一证书。 |

## 安全要求

- 不把 AccessKey、SecretKey、证书私钥或证书正文写入日志、报告、PR 描述或文档。
- 用 `--profile` 明确账号，避免误用 active profile。
- 对生产 CDN 域名先 dry-run，确认域名列表后再加 `--execute --yes`。
