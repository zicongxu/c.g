# Changelog

Versions follow semantic versioning. Dates use `YYYY-MM-DD`.

## [Unreleased]

### Documentation

- Separated packaged-user installation from source development and documented the current release
  artifact and model-access prerequisites for clean-machine onboarding.
- Updated release examples and repository indexes to version 2.3.0.

### Added

- Revision-pinned public ONNX download with mandatory SHA-256 verification through
  `make download-model`.
- Recorded the distinction between the official Apache-2.0 Small checkpoint and the third-party
  ONNX conversion mirror.

## [2.3.0] - 2026-09-19

### Added

- Embedded cgcli runtime mode in the packaged macOS executable.
- One-bundle architecture so GUI and CLI share the same Python runtime, processing libraries, model,
  and `DepthProcessor` implementation.

### Changed

- The macOS build script can reuse an explicitly selected Python environment through
  `DEPTH_STUDIO_PYTHON`, avoiding a second build environment.

## [2.2.0] - 2026-09-19

### Added

- Public, UI-independent `extract_depth_video` API for CLI and automation callers.
- Typed request/result objects, stable validation errors, and default model discovery.

### Fixed

- Upgrade pip before editable development installs so the documented setup works with macOS Python 3.9.

## [2.1.0] - 2026-09-18

### Added

- Full-page responsive scrolling for small screens and macOS Dock constraints.
- Congguo brand header, app icon, processing animation, and visual system.
- Immediate file-name, dimensions, and duration feedback after selection.
- Persistent Recent Outputs with Play and Reveal actions.
- Standard source layout, handoff documentation, build scripts, and regression tests.

### Fixed

- Prevented header clipping, text-on-border collisions, and button overlap when vertical space is limited.

## [2.0.0] - 2026-09-18

- First Congguo-branded release.
- Offline Depth Anything V2 Small ONNX inference.
- PySide6 UI, FFmpeg encoding, optional audio preservation, and cancellable processing.
