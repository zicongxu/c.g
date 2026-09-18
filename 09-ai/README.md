# AI System

This domain contains executable intelligence and the knowledge required to operate it.

| Directory | Content | Registry |
|---|---|---|
| `agents/` | Agent roles, permissions, tools, handoff contracts | `agents/registry.yaml` |
| `skills/` | Installed reusable capabilities with a `SKILL.md` entrypoint | `skills/registry.yaml` |
| `skill-packages/` | Raw, unreviewed bundles containing one or more Skills | `skill-packages/registry.yaml` |
| `prompts/` | Versioned prompts and input/output examples | `prompts/registry.yaml` |
| `workflows/` | Multi-step human/agent/tool processes | `workflows/registry.yaml` |
| `evals/` | Test sets, rubrics, baselines, results | Linked by evaluated artifact |
| `context/` | Small, stable, task-scoped context packs | Linked by consumer |
| `policies/` | Safety, permissions, model use, human review | Canonical knowledge index when company-wide |

An AI capability is not production-ready until its owner, version, permission boundary, failure behavior, and evaluation are documented.
