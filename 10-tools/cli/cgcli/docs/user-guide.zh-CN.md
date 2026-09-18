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

默认在原视频旁生成 `input_depth.mp4`，输出 30 FPS，并尽量保留原音频。常用示例：

```bash
cgcli video depth input.mov --fps 60 --no-keep-audio -o result.mp4
cgcli --output-format json --progress none video depth input.mp4
CGCLI_DEPTH_MODEL=/models/depth_anything_v2_vits.onnx cgcli video depth input.mp4
```

已有同名输出时命令会拒绝覆盖；确认需要替换后再增加 `--overwrite`。按 `Ctrl+C` 会请求安全取消。
本能力完全本地运行，不需要 Codex、ChatGPT 或云端 API。
