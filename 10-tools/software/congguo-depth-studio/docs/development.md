---
title: Congguo Depth Studio Development Guide
summary: Local setup, commands, test layers, debugging hooks, and code conventions
status: draft
owner: Congguo Product Team
updated: 2026-09-18
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [development, testing, python]
related: [../README.md, architecture.md, build-and-release.md]
---

# Development guide

## Prerequisites

- Python 3.9-3.13. The macOS 2.1.0 baseline was built with Python 3.9.6.
- Apple Silicon Mac for reproducing the current macOS artifact.
- Approximately 2 GB of temporary space for dependencies and PyInstaller.
- The accepted ONNX model, stored outside Git.

## Setup

```bash
cd 10-tools/software/congguo-depth-studio
make install
make install-model MODEL=/absolute/path/depth_anything_v2_vits.onnx
```

`make install` creates `.venv` and installs the runtime, test, lint, and build dependencies in editable mode.

## Commands

| Command | Purpose |
|---|---|
| `make run` | Launch the source UI |
| `make lint` | Run Ruff checks |
| `make test` | Run fast tests on Qt's minimal platform |
| `make smoke` | Construct the application and verify model readiness without entering the event loop |
| `make build-macos` | Validate the model, package, and verify the macOS app |
| `make clean` | Remove reproducible build output and caches |

## Test hooks

| Environment variable | Behavior |
|---|---|
| `DEPTH_STUDIO_SMOKE_TEST=1` | Print model readiness and exit |
| `DEPTH_STUDIO_PROCESS_TEST_INPUT=/path/in.mp4` | Select an input for headless end-to-end processing |
| `DEPTH_STUDIO_PROCESS_TEST_OUTPUT=/path/out.mp4` | Select the matching headless output |
| `QT_QPA_PLATFORM=minimal` | Construct Qt widgets without a desktop session |

Example:

```bash
QT_QPA_PLATFORM=minimal \
DEPTH_STUDIO_PROCESS_TEST_INPUT=/tmp/sample.mp4 \
DEPTH_STUDIO_PROCESS_TEST_OUTPUT=/tmp/sample-depth.mp4 \
.venv/bin/python -m congguo_depth_studio
```

## Validation layers

Fast tests cover preprocessing shape/dtype, ETA formatting, and packaged brand-resource resolution. Processing changes also require a sanitized 0.5-2 second clip with audio. Verify successful exit, decodable output, expected streams, cancellation cleanup, depth polarity, temporal stability, and edge quality.

UI validation must cover at least `680x600`, `768x760`, and `1440x900`. Qt's minimal platform is suitable for layout/state smoke tests but not final typography, Retina, Dock, file-drop, or visual acceptance; use a real macOS graphical session for those checks.

## Code conventions

- Use type annotations and keep source lines at or below 100 characters.
- Keep page composition, reusable widgets, visual styles, and processing logic separated.
- Treat all five brand states (`idle`, `selected`, `processing`, `completed`, `error`) as one copy contract.
- Use native Qt controls and maintain accessible names; never communicate state by color alone.
- Pass subprocess arguments as lists and never use `shell=True`.
- Never log, commit, or transmit a user's selected path or source video.

## Common changes

- Input format: update `VIDEO_EXTENSIONS`, the picker filter, user documentation, and a decode test.
- Frame rate: update the combo, then validate FPS conversion and output duration.
- Color or spacing: change the semantic QSS system in `styles.py`, not inline widget styles.
- Inference provider: capability-detect it, test it separately, and retain CPU fallback.
- Version: update `pyproject.toml`, `__init__.py`, the PyInstaller spec, and `CHANGELOG.md`.
