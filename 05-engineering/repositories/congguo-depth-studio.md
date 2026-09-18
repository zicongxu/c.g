---
title: Congguo Depth Studio Repository Index
summary: Code location, ownership, build entry points, and asset boundaries for Congguo Depth Studio
status: draft
owner: Congguo Product Team
updated: 2026-09-18
review_cycle: quarterly
source_of_truth: true
confidentiality: internal
tags: [repository, desktop-app, video-ai]
related: [../../10-tools/software/congguo-depth-studio/README.md]
---

# Congguo Depth Studio repository index

| Field | Value |
|---|---|
| Code | [`10-tools/software/congguo-depth-studio/`](../../10-tools/software/congguo-depth-studio/README.md) |
| Product definition | [`02-products/congguo-depth-studio/README.md`](../../02-products/congguo-depth-studio/README.md) |
| Git remote | `https://github.com/zicongxu/c.g` |
| Default branch | `main` |
| Owner | Congguo Product Team; named human owner pending |
| Stack | Python, PySide6, OpenCV, ONNX Runtime, FFmpeg, PyInstaller |
| Runtime | Offline desktop application |
| Current release | 2.3.0 / macOS arm64 |

## Engineering entry points

- Handoff: [`AGENTS.md`](../../10-tools/software/congguo-depth-studio/AGENTS.md)
- Architecture: [`docs/architecture.md`](../../10-tools/software/congguo-depth-studio/docs/architecture.md)
- Development: [`docs/development.md`](../../10-tools/software/congguo-depth-studio/docs/development.md)
- Build/release: [`docs/build-and-release.md`](../../10-tools/software/congguo-depth-studio/docs/build-and-release.md)
- Operations: [`docs/operations.md`](../../10-tools/software/congguo-depth-studio/docs/operations.md)

Git stores source, tests, documentation, build configuration, and small brand assets. Model weights,
applications, ZIPs, regression videos, and user videos remain outside Git. Source setup downloads a
revision-pinned public ONNX artifact and enforces its recorded SHA-256. No public GitHub Release App
asset exists yet; its artifact location and checksum must be added here when available.
