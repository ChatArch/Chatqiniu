# Chatqiniu

Chatqiniu 是 ChatArch 的七牛云命令行工具，覆盖 ChatEnv 鉴权、Kodo 对象存储、CDN、SSL 证书和 CDN 域名 HTTPS 配置。

- 文档站：https://arch.gh.wzhecnu.cn/Chatqiniu/
- 源码仓库：https://github.com/ChatArch/Chatqiniu
- 英文版：[README.en.md](README.en.md)

## 快速开始

```bash
pip install -e ".[dev,docs]"
chatqiniu --version
chatqiniu --tree
chatqiniu auth whoami --profile wzh
chatqiniu bucket list --profile wzh
python -m pytest -q
```

## 当前能力

| 场景 | 命令入口 | 说明 |
| --- | --- | --- |
| 鉴权与 profile | `auth`、`profile`、`config` | 通过 ChatEnv 读写七牛凭证和默认 bucket / CDN 域名配置。 |
| Kodo 对象存储 | `bucket`、`object`、`url` | 查看 bucket、列对象、上传/下载、生成公开或私有 URL。 |
| CDN 操作 | `cdn` | 刷新、预取和查询 CDN 任务。 |
| 证书与 HTTPS | `cert`、`domain https` | 列出/上传证书，或把证书绑定到 CDN 域名。高影响写操作默认 dry-run。 |
| 诊断与文档 | `doctor`、`docs` | 本地配置检查、只读 API 健康检查和官方链接索引。 |

## 证书部署

`cert deploy` 会把本地 PEM 证书上传到七牛，再把返回的证书 ID 绑定到一个或多个 CDN 域名。命令默认只预览；真实执行必须显式加 `--execute --yes`。

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

安全约定：命令输出不会打印证书正文、私钥、AccessKey 或 SecretKey。

## 文档入口

- 命令树：https://arch.gh.wzhecnu.cn/Chatqiniu/cli-tree/
- 能力地图：https://arch.gh.wzhecnu.cn/Chatqiniu/capability-map/
- 证书部署流程：https://arch.gh.wzhecnu.cn/Chatqiniu/certificate-workflow/

## 开发验证

```bash
python -m pytest -q
mkdocs build --strict
python -m build
python -m twine check dist/*
```
