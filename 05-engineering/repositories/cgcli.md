---
title: cgcli Repository Index
summary: Ownership and handoff index for the company-wide Congguo command-line interface
status: draft
owner: Congguo Engineering
updated: 2026-09-19
review_cycle: event-driven
source_of_truth: false
confidentiality: internal
tags: [repository, cli, automation]
related: [../../10-tools/cli/cgcli/README.md]
---

# cgcli repository index

- Canonical source: [`10-tools/cli/cgcli/`](../../10-tools/cli/cgcli/README.md)
- Current version: `0.3.0`
- Production runtime: lightweight macOS/Windows launcher into the platform App; no separate Python
- Development runtime: Python 3.9-3.13
- Owner role: Congguo Engineering
- Provider for `video depth`: [`Congguo Depth Studio`](../../10-tools/software/congguo-depth-studio/README.md)
- Runtime network and credentials: none for the initial depth capability
- Handoff: read the CLI `AGENTS.md` and command contract before changing compatibility surfaces

Production installation is a small launcher into the installed Congguo Depth Studio App Bundle. The
CLI does not own a second Python environment, inference dependency set, or model copy.

The CLI is maintained inside this monorepo. Models, user media, generated outputs, virtual
environments, and release binaries remain outside Git.
