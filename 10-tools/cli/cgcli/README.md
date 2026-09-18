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

- Version: `0.1.0`
- Lifecycle: functional draft pending named human-owner acceptance
- Owner role: Congguo Engineering
- Data impact: reads a local video and model; writes one local MP4
- Credentials: none
- Runtime network: none

## Install for repository development

Prerequisites: Python 3.9-3.13 and the accepted external ONNX model.

```bash
cd 10-tools/cli/cgcli
make install
../../software/congguo-depth-studio/scripts/install-model.sh \
  /absolute/path/depth_anything_v2_vits.onnx
```

`make install` installs the depth provider and cgcli in one local virtual environment. The model is
deliberately excluded from Git. It can instead remain elsewhere and be passed through `--model` or
`CGCLI_DEPTH_MODEL`.

## Commands

```bash
# Human-readable result; defaults to 30 FPS and source audio.
.venv/bin/cgcli video depth /path/source.mp4

# Explicit output and processing options.
.venv/bin/cgcli video depth /path/source.mov \
  --output /path/result.mp4 --fps 60 --no-keep-audio --overwrite

# Agent/automation mode: one JSON result on stdout and no progress.
.venv/bin/cgcli --output-format json --progress none \
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
└── tests/                       fast contract tests with fake providers
```

## Handoff

New maintainers start with [`AGENTS.md`](AGENTS.md), then read the command contract. To add a command,
follow [`docs/adding-a-capability.md`](docs/adding-a-capability.md); business logic belongs behind a
public provider API, not inside cgcli. For depth-video changes, read the provider's
[`AGENTS.md`](../../software/congguo-depth-studio/AGENTS.md) before editing it.
