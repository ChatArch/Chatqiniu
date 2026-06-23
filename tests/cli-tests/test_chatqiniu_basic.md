# Chatqiniu CLI Basic Test

## 目标

验证 `chatqiniu` 的轻应用 registry 基础链路：新增、列表、查看、删除，以及 `-I` 非交互缺参快速失败。

## 初始环境准备

- 使用 pytest `tmp_path` 创建独立 registry JSON 文件。
- 所有命令通过 `--registry` 指向临时文件，避免污染用户默认 `~/.chatqiniu/apps.json`。

## 预期过程和结果

1. 执行 `chatqiniu add demo --endpoint https://demo.example.com --title "Demo App" --registry <tmp>`，命令成功并输出 `Saved demo`。
2. 执行 `chatqiniu list --registry <tmp>`，命令成功并输出 `demo (Demo App): https://demo.example.com`。
3. 执行 `chatqiniu show demo --registry <tmp>`，命令成功并输出 endpoint。
4. 执行 `chatqiniu remove demo --registry <tmp>`，命令成功并输出 `Removed demo`。
5. 再次执行 `chatqiniu list --registry <tmp>`，命令成功并输出 `No apps configured.`。
6. 执行 `chatqiniu add demo --registry <tmp> -I`，缺少 endpoint 时必须非零退出，且错误信息包含 endpoint。

## 参考执行脚本

```sh
registry="$(mktemp)"
chatqiniu add demo --endpoint https://demo.example.com --title "Demo App" --registry "$registry"
chatqiniu list --registry "$registry"
chatqiniu show demo --registry "$registry"
chatqiniu remove demo --registry "$registry"
chatqiniu add demo --registry "$registry" -I
```
