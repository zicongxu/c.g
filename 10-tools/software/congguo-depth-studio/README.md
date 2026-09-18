---
title: Congguo Depth Studio
summary: Offline desktop software that converts monocular video into a stabilized relative-depth video
status: draft
owner: Congguo Product Team
updated: 2026-09-18
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [software, desktop-app, video-ai, depth-estimation]
related: [docs/architecture.md, docs/development.md, docs/build-and-release.md]
---

# Congguo Depth Studio (葱果深度工坊)

Congguo Depth Studio is an offline desktop application that turns a monocular video into a stabilized grayscale relative-depth MP4. It runs Depth Anything V2 Small through ONNX Runtime, preserves the source audio when requested, and presents the workflow through the Congguo character and brand system.

## Current status

- Version: `2.1.0`
- Lifecycle: usable prototype; remains `draft` until a named human owner accepts it
- Verified baseline: macOS 15.7 on Apple Silicon, including packaged end-to-end processing
- Delivered artifact: macOS arm64 `.app` and ZIP, stored outside Git
- Main limitation: the output is monocular relative depth, not metric distance, skeletal motion capture, or reconstructed 3D geometry

## Supported workflow

- Input: MP4, MOV, M4V, AVI, MKV, and WebM.
- Output frame rate: 24, 30, or 60 FPS.
- Audio: optionally remux the original audio into the depth video.
- Privacy: no cloud model, API key, Codex, ChatGPT, telemetry, or runtime network request.
- Results: retain up to eight valid recent outputs with Play and Reveal actions.
- Layout: usable at `680x600`; the page scrolls when the screen or Dock reduces available height.

## Five-minute setup

Prerequisites: Python 3.9-3.13. Reproducing the current macOS build requires Apple Silicon and macOS 13 or later.

```bash
cd 10-tools/software/congguo-depth-studio
make install
make install-model MODEL=/absolute/path/depth_anything_v2_vits.onnx
make run
```

The model is intentionally excluded from Git. The installer validates its SHA-256 before copying it into the runtime resource directory. See [`MODEL.md`](src/congguo_depth_studio/resources/MODEL.md).

## Validation

```bash
make lint
make test
make smoke
```

For a packaged macOS application:

```bash
make build-macos
```

The result is `dist/葱果深度工坊.app`. Follow [`docs/build-and-release.md`](docs/build-and-release.md) before distributing any artifact.

## Repository map

```text
congguo-depth-studio/
├── AGENTS.md                     mandatory handoff and change constraints
├── README.md                    current status and quick start
├── CHANGELOG.md                 version history
├── THIRD_PARTY_NOTICES.md       dependency and release-license checklist
├── docs/
│   ├── architecture.md              modules, threads, state, and data flow
│   ├── development.md               setup, tests, debugging, conventions
│   ├── build-and-release.md         macOS release and Windows porting
│   ├── operations.md                runtime behavior and troubleshooting
│   └── user-guide.zh-CN.md          localized end-user guide
├── packaging/macos/             PyInstaller macOS specification
├── scripts/                     model installation and build automation
├── src/congguo_depth_studio/    Python/PySide6 source and brand assets
├── tests/                       fast regression tests
└── pyproject.toml               dependencies, version, and tool settings
```

## Handoff routes

- New agent or maintainer: start with [`AGENTS.md`](AGENTS.md).
- Processing or model changes: read [`docs/architecture.md`](docs/architecture.md) and [`docs/development.md`](docs/development.md).
- Packaging or release: read [`docs/build-and-release.md`](docs/build-and-release.md).
- User-environment failures: read [`docs/operations.md`](docs/operations.md).
- Dependency review: read [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Data boundary

The application reads the selected source locally. Intermediate files live in a system temporary directory and are removed by `TemporaryDirectory` on success, cancellation, or handled failure. Do not add uploads, telemetry, or user tracking without an approved product decision and explicit user consent.
