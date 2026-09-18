# Tools

| Directory | Content | Registry |
|---|---|---|
| `cli/` | Internal command-line tools | `cli/registry.yaml` |
| `scripts/` | Small single-purpose automation | Documented by parent tool/workflow |
| `integrations/` | APIs, webhooks, bots, account connections | `integrations/registry.yaml` |
| `software/` | SaaS and desktop software catalog | `software/registry.yaml` |

If a script becomes shared, versioned, tested, or multi-purpose, promote it to a CLI or separate code repository. Store credentials only in a secret manager.
