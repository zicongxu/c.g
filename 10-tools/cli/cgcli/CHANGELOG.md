# Changelog

Versions follow semantic versioning. Dates use `YYYY-MM-DD`.

## [Unreleased]

### Documentation

- Added the complete macOS installation order, App dependency, PATH recovery, uninstall steps, and
  the distinction between the production launcher and `make dev-install`.

## [0.2.0] - 2026-09-19

### Changed

- Production `cgcli` is now a lightweight launcher for the installed Congguo Depth Studio App Bundle.
- The App Bundle owns the Python runtime, processing libraries, model, and embedded cgcli command code.
- Moved the dependency-heavy editable environment to the explicit `make dev-install` workflow.

### Added

- App discovery through `CGCLI_APP_PATH`, `~/Applications`, and `/Applications`.
- Launcher delegation tests and a macOS launcher installer.

## [0.1.0] - 2026-09-19

### Added

- Extensible `cgcli <domain> <capability>` command hierarchy.
- `cgcli video depth` backed by Congguo Depth Studio's public API.
- Text and JSON result modes, stable error codes, progress routing, and cancellation.
