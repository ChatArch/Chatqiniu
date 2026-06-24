# Chatqiniu 文档

这里收纳 `Chatqiniu` 的长期维护文档。

## 当前能力

- `auth`：七牛凭证登录、清理和只读身份校验
- `profile` / `config`：ChatEnv profile 和默认 bucket / url-prefix / cdn-domain 管理
- `bucket` / `object` / `url`：对象存储资源查看、上传、删除 dry-run、URL 生成
- `cdn` / `cert` / `domain`：CDN 刷新预取、证书列表/上传、域名 HTTPS 配置 dry-run
- `doctor` / `docs`：本地诊断和官方文档索引

## 常用示例

```bash
chatqiniu auth whoami
chatqiniu bucket list
chatqiniu object list --prefix assets/
chatqiniu cert list
chatqiniu domain show cdn.example.com
```

## 本地预览

```bash
pip install -e ".[docs]"
mkdocs serve
```

英文版见：[index.en.md](index.en.md)。
