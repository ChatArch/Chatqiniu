# 命令树

本页只列出已经实现的 `chatqiniu` 命令。命令树来自当前 CLI help 面；新增命令时应同步更新本页、测试和可复用 Python API。

## 顶层命令

```text
chatqiniu
├── --version                    # 输出当前包版本
├── auth                         # 七牛凭证登录、清理和只读身份校验
├── profile                      # ChatEnv 命名 profile 管理
├── config                       # 默认 bucket / URL / CDN 配置
├── bucket                       # 查看 Kodo bucket
├── object                       # 管理 Kodo 对象
├── url                          # 生成对象 URL
├── cdn                          # CDN 刷新、预取和任务查询
├── cert                         # CDN 证书查看、上传、部署和删除
├── domain                       # CDN 域名查看和 HTTPS 配置
├── doctor                       # 本地诊断
├── docs                         # 官方文档链接和示例
└── hello                        # 兼容模板 smoke 的问候命令
```

## 鉴权与 profile {#auth-profile}

```text
chatqiniu auth
├── login                        # 写入 ChatEnv 管理的七牛凭证
├── logout                       # 清理 active 或命名 profile
└── whoami                       # 通过只读 bucket listing 验证当前凭证

chatqiniu profile
├── create                       # 创建命名 profile
├── delete                       # 删除命名 profile
├── list                         # 列出命名 profile
├── show                         # 查看 active 或命名 profile，敏感值会被脱敏
└── use                          # 激活命名 profile

chatqiniu config
├── get                          # 读取一个非敏感配置值
├── list                         # 列出非敏感配置值
├── set                          # 写入一个配置值
└── unset                        # 删除一个配置值
```

## 对象存储 {#object-storage}

```text
chatqiniu bucket
├── list                         # 列出可访问 bucket
└── show                         # 查看 bucket 基础信息

chatqiniu object
├── list                         # 列出 bucket 内对象
├── stat                         # 查看对象元信息
├── upload                       # 上传一个本地文件
├── upload-dir                   # 递归上传目录
├── download                     # 通过生成 URL 下载对象
├── delete                       # 删除一个对象，默认 dry-run
├── batch-delete                 # 按 prefix 批量删除，默认 dry-run
├── copy                         # 复制对象，默认 dry-run
└── move                         # 移动对象，默认 dry-run

chatqiniu url
├── public                       # 生成公开对象 URL
└── private                      # 生成私有签名对象 URL
```

## CDN 与域名 {#cdn-domain}

```text
chatqiniu cdn
├── refresh                      # 刷新 CDN 缓存，默认 dry-run
├── prefetch                     # 预取 CDN 资源，默认 dry-run
└── task                         # 查询 CDN 任务状态

chatqiniu domain
├── list                         # 列出 CDN 域名
├── show                         # 查看一个 CDN 域名
└── https
    └── set                      # 设置域名 HTTPS 证书，默认 dry-run
```

## 证书

```text
chatqiniu cert
├── list                         # 列出 CDN 证书
├── show                         # 查看一张证书
├── upload                       # 上传 PEM 证书，默认 dry-run
├── deploy                       # 上传证书并绑定多个 CDN 域名，默认 dry-run
└── delete                       # 删除一张证书，默认 dry-run
```

`cert deploy` 的真实执行需要 `--execute --yes`，并且不会在输出中打印证书正文或私钥内容。完整流程见 [证书部署](certificate-workflow.md)。

## 诊断与文档

```text
chatqiniu doctor
└── check                        # 检查本地配置和只读 API 健康

chatqiniu docs
├── links                        # 输出官方文档链接
├── open                         # 输出指定主题的官方文档链接
└── examples                     # 输出常用示例
```
