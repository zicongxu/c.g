# cgcli Agent Contract

The repository-root `AGENTS.md` remains authoritative. This file defines the handoff contract for
the company-wide CLI.

## Mandatory reading order

1. Read [`README.md`](README.md) for scope, setup, and operational boundaries.
2. Read [`docs/command-contract.md`](docs/command-contract.md) before changing arguments, JSON,
   error codes, exit codes, or stdout/stderr behavior.
3. Read [`docs/adding-a-capability.md`](docs/adding-a-capability.md) before adding a domain or command.
4. Read the providing product's public API contract; for depth video this is
   [`congguo_depth_studio/api.py`](../../software/congguo-depth-studio/src/congguo_depth_studio/api.py).
5. Check `git status`, `CHANGELOG.md`, tests, and registry entries before editing.

## Invariants

- `cgcli` is a company-wide entry point, not a depth-only application.
- Command paths use `cgcli <domain> <capability>`; do not add product-specific top-level flags.
- Global flags configure rendering and automation only. Capability flags stay on that capability.
- Final data uses stdout. Progress and human diagnostics use stderr.
- `--output-format json` returns exactly one final JSON object on stdout.
- Heavy or product-specific dependencies are imported only inside their capability handler.
- Production installation is a lightweight launcher into the App Bundle. Do not create a second
  Python runtime or copy model weights for cgcli.
- On Windows, `cgcli.cmd` delegates to `CongGuoCliHost.exe` in the portable App. Keep the separate
  console host so stdout, stderr, pipes, and exit codes remain reliable; it must share `_internal`.
- The packaged executable accepts the private transport marker `--cgcli`; users continue to use the
  public `cgcli <domain> <capability>` contract.
- Non-interactive calls never prompt. Destructive replacement requires an explicit flag.
- Exit codes and JSON fields are compatibility contracts; change them additively or release a major
  version with a migration note.
- Local video processing must remain offline and cancellable.

## Required validation

```bash
make lint
make test
make smoke
```

For changes to `video depth`, also run the depth studio checks and a sanitized short-video test when
the model is available. Never commit models, media, build output, virtual environments, or secrets.

## Definition of done

Code, tests, README, command contract, changelog, CLI registry, and any provider API documentation
are consistent. Record validations that could not be run and why.
