# Congguo Media Company Workspace

This is the shared knowledge and operating workspace for Congguo Media (葱果传媒), an AI-native video AI startup.

## Start Here

- AI agents: read [`AGENTS.md`](AGENTS.md), then [`INDEX.md`](INDEX.md).
- Humans looking for knowledge: start at [`INDEX.md`](INDEX.md).
- Machine-readable routing: [`knowledge-map.yaml`](knowledge-map.yaml).
- Knowledge governance: [`KNOWLEDGE.md`](KNOWLEDGE.md).
- Storage boundaries: [`STORAGE.md`](STORAGE.md).
- New documents: use [`90-templates/`](90-templates/README.md).

## Workspace Layers

```text
00-inbox/        Human-only raw capture queue; never an agent default
01-company/      Company facts, strategy, brand, and organization
02-products/     Product portfolio, roadmaps, specifications, and feedback
03-studio/       Video projects, creative systems, pipelines, and asset metadata
04-research/     Market, user, model, paper, and experiment research
05-engineering/  Architecture, ADRs, standards, runbooks, incidents, repositories
06-growth/       Content, marketing, sales, partnerships, and metrics
07-operations/   People, finance, legal, and administration
08-knowledge/    Cross-domain canonical index, glossary, playbooks, meetings, sources
09-ai/           Agents, Skills, prompts, workflows, evaluations, context, policies
10-tools/        CLIs, scripts, integrations, and software catalog
90-templates/    Standard artifact templates
99-archive/      Read-only historical material
```

The folder number indicates navigation order, not importance. Artifact routing is defined by type in `AGENTS.md` and `knowledge-map.yaml`.

## Operating Principle

The repository is not a dumping ground. Raw evidence becomes a reviewed conclusion; a conclusion becomes a decision or reusable procedure; repeated procedures become executable Skills or workflows; production AI capabilities are measured by evaluations.

```text
evidence -> conclusion -> decision -> workflow/skill -> evaluation -> canonical knowledge
```
