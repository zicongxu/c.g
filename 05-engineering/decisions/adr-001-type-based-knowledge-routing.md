---
title: ADR-001 Type-based knowledge routing and layered indexes
summary: Route artifacts by artifact type and discover knowledge through deterministic layered indexes
status: accepted
owner: workspace maintainers
updated: 2026-09-18
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [decision, knowledge, agents]
related: [AGENTS.md, INDEX.md, knowledge-map.yaml]
---

# ADR-001: Type-based Knowledge Routing and Layered Indexes

## Context

The initial workspace described domains but did not give agents a deterministic lookup or write protocol. An agent could treat `00-inbox/` as a safe fallback and place a well-defined artifact, such as a Skill, outside its canonical location. The workspace also lacked one explicit discovery entrypoint and machine-readable routing.

## Decision

Use artifact type as the primary routing key.

- `AGENTS.md` is the mandatory agent operating contract.
- `INDEX.md` is the human-readable discovery entrypoint.
- `knowledge-map.yaml` is the machine-readable routing source.
- Domain READMEs define local scope.
- Typed registries enumerate concrete artifacts.
- Scoped full-text search follows registry lookup.
- Agents cannot use the inbox as a default destination.
- Creating a typed artifact and updating its registry are one atomic change.

## Alternatives Considered

### Topic-only folders

- Benefit: simple for humans at small scale.
- Cost: an artifact can match several topics, producing inconsistent storage.
- Rejected because artifact identity is more stable than topic wording.

### One global flat index

- Benefit: one file to search.
- Cost: merge conflicts, duplicated metadata, and excessive context as the company grows.
- Rejected in favor of a small root map linked to domain registries.

### Inbox as the universal fallback

- Benefit: agents never need to stop for ambiguity.
- Cost: canonical artifacts become invisible to typed discovery and remain ungoverned.
- Rejected. Undefined routing requires clarification, not silent dumping.

## Consequences

- Agents have a short and deterministic startup sequence.
- Skills, prompts, agents, workflows, tools, products, projects, models, and repositories have stable registries.
- Artifact creation requires a small additional registry update.
- Registry drift is possible, so workspace validation is required.
- Future artifact types must be added to both `AGENTS.md` and `knowledge-map.yaml`.

## Review Triggers

Revisit this decision if registry maintenance becomes a bottleneck, the workspace moves to a database-backed knowledge graph, or agents cannot reliably load repository-level instructions.
