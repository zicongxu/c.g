---
title: cgcli Command Contract
summary: Stable syntax, output streams, JSON envelopes, errors, and exit codes for automation
status: draft
owner: Congguo Engineering
updated: 2026-09-19
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [cli, api-contract, automation]
related: [../README.md, adding-a-capability.md]
---

# Command contract

## Grammar

```text
cgcli [global options] <domain> <capability> [capability options] [arguments]
```

The initial command is `cgcli video depth INPUT`. Domains describe reusable media or company
surfaces; capabilities are verbs or products inside that domain. Global options must appear before
the domain.

## Global options

| Option | Contract |
|---|---|
| `--output-format text|json` | Final stdout representation; default `text` |
| `--progress auto|plain|none` | Progress on stderr; default `auto` |
| `--quiet` | Suppress human success and progress; JSON results remain available |
| `--version` | Print the cgcli version and exit |

## Stream contract

- stdout contains the final result only.
- stderr contains progress and human-readable errors.
- JSON mode writes exactly one success or error envelope to stdout. Progress may still appear on
  stderr when explicitly requested with `--progress plain`.
- Commands never prompt in non-interactive workflows.

Success envelope:

```json
{"ok":true,"command":"video.depth","input_path":"/in.mov","output_path":"/in_depth.mp4","fps":30,"keep_audio":true,"elapsed_seconds":12.345}
```

Error envelope:

```json
{"ok":false,"error":{"code":"OUTPUT_ALREADY_EXISTS","message":"...","details":{"output_path":"..."}}}
```

## Exit codes

| Exit | Meaning |
|---:|---|
| `0` | Success |
| `2` | Invalid command syntax or option |
| `3` | Missing or invalid input, model, or installed capability |
| `4` | Output conflict; use the capability's explicit replacement flag |
| `5` | Processing failed after validation |
| `130` | Cancelled by SIGINT |

Error string codes are more specific than exit codes and are the preferred automation key.

## Compatibility policy

New commands and optional JSON fields are additive. Renaming commands, changing defaults, removing
fields, changing field types, or reassigning exit meanings requires a cgcli major-version release and
a documented migration path.
