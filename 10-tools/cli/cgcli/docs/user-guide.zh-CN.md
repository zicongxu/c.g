---
title: cgcli 中文使用指南
summary: 安装和调用葱果统一 CLI 的最短路径
status: draft
owner: Congguo Engineering
updated: 2026-09-19
review_cycle: event-driven
source_of_truth: false
confidentiality: internal
tags: [cli, user-guide, zh-CN]
related: [../README.md, command-contract.md]
---

# cgcli 中文使用指南

`cgcli` 是葱果统一命令行入口。深度视频只是第一个能力，命令为：

```bash
cgcli video depth /path/input.mp4
```

## 安装（macOS）

生产版 `cgcli` 不会重新安装 Python、推理库或模型，而是调用已经安装的“葱果深度工坊.app”。
所以顺序必须是“先装 App，再装几 KB 的命令行启动器”。

1. 按[软件使用说明](../../../software/congguo-depth-studio/docs/user-guide.zh-CN.md)安装
   “葱果深度工坊.app”。仓库不含 App；当前也没有公开的 GitHub Release 安装包，需要向发布
   负责人获取带版本号的 ZIP。
2. 在仓库根目录执行：

```bash
cd 10-tools/cli/cgcli
make install
cgcli --version
cgcli video depth --help
```

如果 App 没有放在 `~/Applications` 或 `/Applications`：

```bash
make install APP=/绝对路径/葱果深度工坊.app
```

安装脚本会打印 `cgcli` 的实际位置。如果随后提示 `command not found`，把打印出的目录加入
`PATH` 并重新打开终端。普通用户不要执行 `make dev-install`；那是源码开发环境，会额外安装
一套 Python 依赖。

## 使用

默认在原视频旁生成 `input_depth.mp4`，输出 30 FPS，并尽量保留原音频。常用示例：

```bash
cgcli video depth input.mov --fps 60 --no-keep-audio -o result.mp4
cgcli --output-format json --progress none video depth input.mp4
CGCLI_DEPTH_MODEL=/models/depth_anything_v2_vits.onnx cgcli video depth input.mp4
```

已有同名输出时命令会拒绝覆盖；确认需要替换后再增加 `--overwrite`。按 `Ctrl+C` 会请求安全取消。
本能力完全本地运行，不需要 Codex、ChatGPT 或云端 API。

## 卸载与排查

- 卸载：删除安装脚本打印出的 `cgcli` 文件，以及
  `~/Library/Application Support/Congguo/cgcli-app-path`；不会删除 App、模型或视频。
- `葱果深度工坊.app not found`：先安装 App，或设置 `CGCLI_APP_PATH`。
- `app runtime is missing or not executable`：App 不完整，请重新解压并安装完整 App Bundle。
- 查看完整参数：`cgcli --help` 和 `cgcli video depth --help`。
