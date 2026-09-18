---
title: Adding a cgcli Capability
summary: Extension procedure for adding domains and commands without coupling their dependencies
status: draft
owner: Congguo Engineering
updated: 2026-09-19
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [cli, development, extension]
related: [../README.md, command-contract.md]
---

# Adding a capability

1. Choose an existing domain (`video`, later `image`, `agent`, and so on) or justify a new one.
2. Define the callable provider API before the CLI adapter. The provider owns business validation and
   processing; cgcli owns argument parsing, rendering, signal handling, and exit mapping.
3. Put capability options on the capability parser. Add a global option only when every domain can
   honor the same semantics.
4. Import product dependencies lazily inside the handler. `cgcli --help` must work without them.
5. Return a structured result and map expected provider errors to stable cgcli errors.
6. Add parser, success, JSON error, conflict, and cancellation tests.
7. Update the README, command contract when applicable, changelog, and `10-tools/cli/registry.yaml`.

Built-in domains are registered in `src/cgcli/registry.py`. A domain owns one module under
`src/cgcli/commands/`; complex capabilities may use a separate adapter such as `video_depth.py`.
Avoid importing another product's UI module or reaching into a private processor directly.
