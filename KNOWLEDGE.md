# Knowledge Governance

## Lifecycle

```text
capture -> draft -> reviewed -> active -> deprecated -> archived
```

- `capture`: raw material waiting for human classification in `00-inbox/`.
- `draft`: being developed; not authoritative.
- `reviewed`: checked by an owner but not yet active.
- `active`: current and safe to use as company guidance.
- `deprecated`: no longer recommended but may be referenced by older work.
- `archived`: retained only for historical traceability.

## Required Metadata

Long-lived Markdown documents use this YAML front matter:

```yaml
---
title: Document title
summary: One sentence explaining the purpose
status: draft
owner: unassigned
updated: YYYY-MM-DD
review_cycle: monthly | quarterly | yearly | event-driven
source_of_truth: false
confidentiality: public | internal | restricted
tags: []
related: []
---
```

`updated` means the last content verification date, not a formatting change. An `active` document must have a real owner.

## Knowledge Classes

| Class | Examples | Storage | Update model |
|---|---|---|---|
| Fact | Product definition, metric definition, software catalog | Owning domain | Update canonical source and retain history |
| Decision | Architecture, model, vendor, or process choice | ADR or project decision log | Add a new decision; preserve old record |
| Procedure | SOP, runbook, production workflow, Skill | Playbooks, `09-ai/`, engineering | Promote only after validation |
| Evidence | Interview, paper, transcript, experiment data | Research or references | Preserve source, date, license, provenance |

## Minimum Content Standard

Every durable document should answer:

1. What is the conclusion or operational instruction?
2. What is in scope and out of scope?
3. What evidence supports it?
4. Who owns it and when is it reviewed?
5. What downstream artifact, action, or decision depends on it?

## AI-native Rules

- Context packs in `09-ai/context/` must be short, stable, scoped, and linked to canonical sources.
- Prompts, Skills, and workflows require versions, input/output contracts, examples, and evaluation links.
- Evaluations record model, parameters, dataset version, date, latency, quality, safety, and cost.
- AI-generated reports identify the generation method and human reviewer.
- A repeated written procedure should become an executable Skill or workflow when practical.
- An AI-generated claim is not a company fact until a named human owner verifies it.

## Naming and Linking

- Use lowercase `kebab-case` for file and directory names.
- Use `YYYY-MM-DD` for dates.
- Decisions: `adr-NNN-short-title.md`.
- Experiments: `exp-YYYYMMDD-short-title.md`.
- Each project has a directory with `README.md` as its status page.
- Use relative links inside the repository.
- Update the relevant registry whenever a typed artifact is created, renamed, moved, or archived.

## Content That Must Not Enter Git

- Credentials, cookies, tokens, `.env` values, or recovery codes.
- Personal data, customer raw data, or restricted signed documents.
- Large video/audio files, model weights, datasets, or reproducible build outputs.
- Unreviewed chat output presented as authoritative knowledge.
