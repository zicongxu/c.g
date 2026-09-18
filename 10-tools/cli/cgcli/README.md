---
title: cgcli
summary: Extensible company-wide CLI for invoking Congguo capabilities from humans, agents, and automation
status: draft
owner: Congguo Engineering
updated: 2026-09-19
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [cli, ai-native, automation, video-ai]
related: [docs/command-contract.md, docs/adding-a-capability.md]
---

# cgcli

`cgcli` is Congguo's unified command-line entry point. Its stable hierarchy is
`cgcli <domain> <capability>` so one install can grow across video, image, agent, asset, and future
company workflows without turning product-specific options into global flags.

The first capability is `cgcli video depth`, which wraps the same public processing API used by
Congguo Depth Studio. It does not duplicate the model pipeline and does not require Codex, ChatGPT,
an API key, or a network connection at runtime.

## Status and ownership

- Version: `0.2.0`
- Lifecycle: functional draft pending named human-owner acceptance
- Owner role: Congguo Engineering
- Data impact: reads a local video and model; writes one local MP4
- Credentials: none
- Runtime network: none

## Runtime architecture

Production cgcli does not install Python, Qt, OpenCV, ONNX Runtime, FFmpeg, or a second model. The
installed launcher delegates to the executable inside `葱果深度工坊.app`, which contains the shared
cgcli command implementation and the same `DepthProcessor` used by the GUI.

```text
cgcli launcher (a few KB)
  -> 葱果深度工坊.app/Contents/MacOS/CongGuoDepthStudio --cgcli
  -> embedded cgcli parser
  -> congguo_depth_studio.api
  -> shared DepthProcessor and bundled model
```

## Install

Production installation currently supports macOS. First install the packaged Congguo Depth Studio
in `~/Applications` or `/Applications`; the App already contains Python, FFmpeg, inference
libraries, and the model. A Git clone does not contain that App, and there is currently no public
GitHub Release asset. Obtain the versioned App ZIP from the release owner by following the
[`Depth Studio user guide`](../../software/congguo-depth-studio/docs/user-guide.zh-CN.md).

Then, from the repository root, install only the launcher:

```bash
cd 10-tools/cli/cgcli
make install
cgcli --version
cgcli video depth --help
```

If the app lives elsewhere:

```bash
make install APP=/absolute/path/葱果深度工坊.app
```

The installer selects `/opt/homebrew/bin`, `/usr/local/bin`, or `~/.local/bin` in that order when the
directory is writable. It stores the selected App path in
`~/Library/Application Support/Congguo/cgcli-app-path`; `CGCLI_APP_PATH` can override it at runtime.

If `cgcli` is not found after installation, add the directory printed by the installer to `PATH`,
then open a new terminal. To uninstall, remove the exact launcher path printed by the installer and
`~/Library/Application Support/Congguo/cgcli-app-path`; the App Bundle and its model remain
untouched.

Do not run `make dev-install` for normal installation. That command intentionally creates a second
Python environment for contributors and is not how production `cgcli` operates.

## Repository development

Prerequisites: Python 3.9-3.13 and network access to the provider's pinned public ONNX mirror, or an
already downloaded accepted model for offline setup.

```bash
cd 10-tools/cli/cgcli
make dev-install
make -C ../../software/congguo-depth-studio download-model
```

`make dev-install` is only for contributors running source tests. It intentionally creates a local
dependency environment; production users should never need it. The model remains excluded from Git.
Offline contributors can install an already downloaded model with the provider's
`make install-model MODEL=/absolute/path/depth_anything_v2_vits.onnx` command.

## Commands

```bash
# Human-readable result; defaults to 30 FPS and source audio.
cgcli video depth /path/source.mp4

# Explicit output and processing options.
cgcli video depth /path/source.mov \
  --output /path/result.mp4 --fps 60 --no-keep-audio --overwrite

# Agent/automation mode: one JSON result on stdout and no progress.
cgcli --output-format json --progress none \
  video depth /path/source.mp4 --model /path/depth_anything_v2_vits.onnx
```

Default output is `<input-stem>_depth.mp4` beside the input. Model resolution order is:

1. `--model PATH`
2. `CGCLI_DEPTH_MODEL`
3. the model resource installed with Congguo Depth Studio

Existing outputs are never replaced unless `--overwrite` is present. `Ctrl+C` requests cooperative
cancellation; temporary files are owned and cleaned by the provider.

## Automation contract

Global options must precede the domain:

```text
cgcli [--output-format text|json] [--progress auto|plain|none] [--quiet]
      video depth INPUT [--output PATH] [--model PATH] [--fps 24|30|60]
                         [--keep-audio|--no-keep-audio] [--overwrite]
```

Exit codes are `0` success, `2` invalid invocation, `3` invalid/missing input or capability,
`4` output conflict, `5` processing failure, and `130` cancellation. The complete stdout/stderr and
JSON compatibility rules are in [`docs/command-contract.md`](docs/command-contract.md).

## Validation

```bash
make lint
make test
make smoke
```

When the model is available, also run a sanitized 0.5-2 second input through both text and JSON modes,
then verify video/audio streams with `ffprobe`. Do not commit the input, model, output, `.venv`, or
other generated files.

## Repository map

```text
cgcli/
├── AGENTS.md                    maintainer and agent invariants
├── README.md                    setup, examples, ownership, and boundaries
├── CHANGELOG.md                 version history
├── docs/
│   ├── command-contract.md      stable CLI/JSON/exit-code contract
│   ├── adding-a-capability.md   extension procedure
│   └── user-guide.zh-CN.md      Chinese end-user guide
├── src/cgcli/
│   ├── cli.py                   root parser and lifecycle
│   ├── registry.py              built-in domain registration
│   ├── output.py                stdout/stderr and JSON rendering
│   ├── errors.py                stable command failures
│   └── commands/                domain parsers and provider adapters
├── launcher/cgcli               dependency-free App Bundle launcher
├── scripts/install-launcher.sh  macOS launcher installer
└── tests/                       command and launcher contract tests
```

## Handoff

New maintainers start with [`AGENTS.md`](AGENTS.md), then read the command contract. To add a command,
follow [`docs/adding-a-capability.md`](docs/adding-a-capability.md); business logic belongs behind a
public provider API, not inside cgcli. For depth-video changes, read the provider's
[`AGENTS.md`](../../software/congguo-depth-studio/AGENTS.md) before editing it.
