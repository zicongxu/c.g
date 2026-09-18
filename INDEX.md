# Workspace Knowledge Index

This is the canonical discovery entrypoint for humans and AI agents. Use it to select one domain, then load only that domain's README and registry.

## Canonical Entry Points

| Need | Read first | Structured registry |
|---|---|---|
| Company identity and strategy | `01-company/README.md` | Canonical items in `08-knowledge/index/README.md` |
| Products and product requirements | `02-products/README.md` | `02-products/registry.yaml` |
| Video projects and media assets | `03-studio/README.md` | `03-studio/projects/registry.yaml` |
| Market, users, models, papers, experiments | `04-research/README.md` | `04-research/models/registry.yaml` for models |
| Engineering architecture and operations | `05-engineering/README.md` | `05-engineering/repositories/registry.yaml` |
| Growth, sales, and distribution | `06-growth/README.md` | Domain-local indexes |
| People, finance, legal, administration | `07-operations/README.md` | Restricted external systems |
| Cross-domain canonical knowledge | `08-knowledge/README.md` | `08-knowledge/index/README.md` |
| Agents | `09-ai/agents/README.md` | `09-ai/agents/registry.yaml` |
| Skills | `09-ai/skills/README.md` | `09-ai/skills/registry.yaml` |
| Prompts | `09-ai/prompts/README.md` | `09-ai/prompts/registry.yaml` |
| AI workflows | `09-ai/workflows/README.md` | `09-ai/workflows/registry.yaml` |
| Evaluations and context packs | `09-ai/README.md` | Consumer artifact links |
| CLIs | `10-tools/cli/README.md` | `10-tools/cli/registry.yaml` |
| Integrations | `10-tools/integrations/README.md` | `10-tools/integrations/registry.yaml` |
| Software | `10-tools/software/README.md` | `10-tools/software/registry.yaml` |
| Historical material | `99-archive/README.md` | Search by original path or topic |

## Current Canonical Knowledge

The detailed owner and review table lives in [`08-knowledge/index/README.md`](08-knowledge/index/README.md).

- Company profile: [`01-company/brief/company-profile.md`](01-company/brief/company-profile.md) — draft, requires human verification.
- Workspace operating contract: [`AGENTS.md`](AGENTS.md) — active.
- Knowledge governance: [`KNOWLEDGE.md`](KNOWLEDGE.md) — active.
- Storage boundaries: [`STORAGE.md`](STORAGE.md) — active.

## Search Protocol

After selecting a domain:

```bash
# Discover files in the domain
rg --files 09-ai/skills

# Search names, aliases, owners, tags, and content
rg -n -i 'query|alias' 09-ai/skills
```

Search the entire repository only when the domain index and local search do not resolve the request.
