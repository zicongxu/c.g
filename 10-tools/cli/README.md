# CLI Catalog

Each internal CLI lives at `cli/<cli-name>/` and documents:

- installation, upgrade, and removal;
- common commands and real examples;
- input/output contract, exit codes, and non-interactive mode;
- permissions, credential reference, and data impact;
- tests, version, owner, and troubleshooting.

Register every CLI in `registry.yaml`. Production-mutating commands should support dry-run or explicit confirmation and produce an audit record.
