# Congguo Media Company Workspace

This is the shared knowledge and operating workspace for Congguo Media (葱果传媒), an AI-native video AI startup.

## Start Here

- AI agents: read [`AGENTS.md`](AGENTS.md), then [`INDEX.md`](INDEX.md).
- Humans looking for knowledge: start at [`INDEX.md`](INDEX.md).
- Machine-readable routing: [`knowledge-map.yaml`](knowledge-map.yaml).
- Knowledge governance: [`KNOWLEDGE.md`](KNOWLEDGE.md).
- Storage boundaries: [`STORAGE.md`](STORAGE.md).
- New documents: use [`90-templates/`](90-templates/README.md).

## Run the depth product

This repository contains the source and handoff documentation for both products, but it deliberately
does not contain the ONNX model or packaged application. Choose the route that matches your goal:

| Goal | Start here | Important prerequisite |
|---|---|---|
| Install and use the macOS App | [`Congguo Depth Studio user guide`](10-tools/software/congguo-depth-studio/docs/user-guide.zh-CN.md) | A release ZIP supplied by the release owner |
| Run or build on Windows x64 | [`Windows clean-machine guide`](10-tools/software/congguo-depth-studio/docs/windows.md) | Python 3.12 x64 and PowerShell |
| Install `cgcli` for normal use | [`cgcli user guide`](10-tools/cli/cgcli/docs/user-guide.zh-CN.md) | Build/install the platform App first |
| Run or change the App from source | [`Depth Studio development guide`](10-tools/software/congguo-depth-studio/docs/development.md) | Python 3.9-3.13; the verified model downloads during setup |
| Extend `cgcli` | [`cgcli maintainer guide`](10-tools/cli/cgcli/README.md) | Python is needed only for development |

Cloning the repository is enough to inspect and change source code. Source execution additionally
downloads Python dependencies and a hash-verified public ONNX artifact. Packaged end-user
installation still requires the App ZIP; see the linked guides for current artifact availability.

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
