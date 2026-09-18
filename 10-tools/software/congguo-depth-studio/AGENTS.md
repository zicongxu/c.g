# Congguo Depth Studio Agent Contract

The repository-root `AGENTS.md` remains authoritative. This file adds project-specific handoff and safety requirements.

## Mandatory reading order

1. Read this project's [`README.md`](README.md) for scope and current status.
2. Read [`docs/architecture.md`](docs/architecture.md) before changing UI state, threading, inference, or FFmpeg behavior.
3. Read [`docs/development.md`](docs/development.md) and reproduce the local validation commands.
4. Read [`docs/build-and-release.md`](docs/build-and-release.md) for packaging, versioning, signing, or platform work.
5. Read [`docs/windows.md`](docs/windows.md) for Windows setup, package layout, or launcher work.
6. Check `git status`, `CHANGELOG.md`, and the relevant source before editing. Chat history is not a source of truth.

## Product invariants

- Offline by default: no cloud model, API, telemetry, upload, or runtime network dependency.
- Responsive UI: ONNX inference and FFmpeg processing must stay off the Qt main thread.
- Cancellable work: long loops and child processes must continually observe cancellation.
- Safe output: create the complete result in a temporary directory, then move it to the user target only after success.
- Small-screen usability: preserve the full-page `QScrollArea` and the `680x600` minimum-operable layout.
- Brand consistency: keep visual tokens in `styles.py` and stateful brand components in `widgets.py`.
- Discoverable results: a successful output must enter Recent Outputs and keep Play and Reveal actions.

## Repository boundaries

Never commit:

- `depth_anything_v2_vits.onnx` or any other model weight.
- `.venv/`, `build/`, `dist/`, application bundles, installers, or ZIP artifacts.
- User videos, generated depth videos, extracted frames, or machine-specific absolute paths.
- API keys, tokens, cookies, signing identities, certificates, or personal account information.

Commit source, tests, build scripts, documentation, small brand assets, and model metadata/hashes only.

## Change routing

- Page composition and state transitions: `app.py`.
- Reusable UI components and UI-state copy: `widgets.py`.
- Visual tokens and QSS: `styles.py`; do not add ad-hoc inline styling to `app.py`.
- Video, inference, temporal normalization, and FFmpeg behavior: `depth_processor.py`.
- Public automation contract and request validation: `api.py`; shared callback/cancellation types:
  `contracts.py`.
- macOS bundle metadata and collection rules: `packaging/macos/DepthMotionStudio.spec`.
- Windows hosts, metadata, and collection rules: `packaging/windows/DepthMotionStudio.spec`.
- Model changes: update `MODEL.md`, download/install/build scripts, tests, and the visual regression
  baseline together.
- Version changes: update `pyproject.toml`, `__init__.py`, the PyInstaller spec, and `CHANGELOG.md` together.

## Required validation

For every code change:

```bash
make lint
make test
make smoke
```

For processing, model, FFmpeg, or packaging changes, also:

1. Process a 0.5-2 second sanitized clip with an audio stream.
2. Use `ffprobe` to verify output video and, when enabled, audio streams.
3. Launch the packaged app in a real graphical session; verify Chinese text, drag-and-drop, small-window scrolling, and Recent Outputs.
4. Run `codesign --verify --deep --strict dist/葱果深度工坊.app` on macOS.

For Windows packaging or shared-runtime changes, the Windows CI build must also pass. Manually
verify the portable directory on Windows for DPI, Chinese text, drag/drop, Explorer Reveal, cgcli
streams/exit codes, and offline processing before external distribution.

## Definition of done

Source, tests, documentation, and `CHANGELOG.md` are consistent; no large or sensitive file enters Git; required validation passes; the commit message records what was verified and what was not.
