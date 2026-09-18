# Media Asset Catalog

Store metadata here, not large binary files.

| Field | Meaning |
|---|---|
| `asset_id` | Stable unique identifier |
| `type` | video, audio, image, project, character, voice |
| `version` | Explicit version; never only `final` or `latest` |
| `project` | Owning project and deliverable |
| `storage_uri` | Object storage or media system link |
| `checksum` | Integrity and deduplication value |
| `rights` | Copyright, likeness, voice, and permitted use |
| `provenance` | Capture, license, generation model, and input source |
| `owner` | Responsible person or role |
| `retention` | Retention and deletion policy |

AI-generated assets also record model, model version, prompt/workflow version, seed when applicable, and generation date.
