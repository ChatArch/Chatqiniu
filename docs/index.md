# Chatqiniu 文档

`Chatqiniu` 是一个 ChatArch Python CLI 包，用于管理七牛轻应用清单。当前版本聚焦本地 registry：把轻应用名称、入口地址、标题和描述保存到 JSON 文件，后续可在此基础上接入真实七牛 API。

## 安装

```bash
pip install Chatqiniu
```

本地开发安装：

```bash
pip install -e ".[dev,docs]"
```

## 管理轻应用

```bash
chatqiniu add demo --endpoint https://demo.example.com --title "Demo App"
chatqiniu list
chatqiniu show demo
chatqiniu remove demo
```

默认 registry 是 `~/.chatqiniu/apps.json`。也可以用环境变量或命令参数覆盖：

```bash
export CHATQINIU_REGISTRY=/path/to/apps.json
chatqiniu list
chatqiniu list --registry /path/to/apps.json
```

## ChatEnv

`Chatqiniu` 注册了 `qiniu` 配置类型：

```bash
chatenv init -t qiniu
chatenv cat -t qiniu
```

字段包括：

- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`
- `QINIU_API_BASE`
- `CHATQINIU_REGISTRY`

## 本地预览

```bash
mkdocs serve
```

英文版见：[index.en.md](index.en.md)。
