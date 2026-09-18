# Information and Asset Storage Boundaries

An AI-native company should not store every artifact in one drive. Choose the system by versioning needs, size, sensitivity, and query pattern. Keep a stable index link in this workspace.

| Content | Primary system | Store in this repository |
|---|---|---|
| Strategy, standards, product definitions, ADRs, playbooks | This Git workspace | Full Markdown and version history |
| Tasks, assignees, deadlines, live status | Project management system | Project entrypoint, milestones, board link |
| Raw footage, audio, project files, rendered video | Object storage, NAS, or media asset manager | Asset ID, version, rights, checksum, stable link |
| Model weights and large datasets | Model/data registry or object storage | Model card, dataset card, version, license, evaluation link |
| Metrics, events, and logs | Data warehouse or observability platform | Metric definition, query entrypoint, dashboard link |
| Secrets, tokens, recovery codes | Secret or password manager | Secret name, owner, request process; never the value |
| Signed contracts, compensation, identity records | Audited restricted system | Redacted summary, owner, restricted link |
| Chat, email, meeting recording | Original collaboration system | Reviewed conclusion, actions, source link |

## Link Requirements

- Use stable asset IDs and explicit versions; never rely on labels such as `final` or `latest` alone.
- Record owner, access class, verification date, and expected retention.
- Core business knowledge must not depend on a single employee's personal account.
- Preserve enough citation metadata that a broken external link does not erase the rationale for a decision.
