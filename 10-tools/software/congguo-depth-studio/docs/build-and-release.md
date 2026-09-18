---
title: Congguo Depth Studio Build and Release Guide
summary: Model preparation, macOS packaging, Windows porting, and release acceptance
status: draft
owner: Congguo Product Team
updated: 2026-09-18
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [build, release, macos, windows]
related: [../README.md, development.md, ../THIRD_PARTY_NOTICES.md]
---

# Build and release guide

## Release inputs

- A clean, identified Git commit.
- Apple Silicon Mac, macOS 13+, and Python 3.9-3.13 for the current macOS target.
- The accepted `depth_anything_v2_vits.onnx`, verified by SHA-256.
- For external release: Developer ID credentials, notarization credentials, and an approved third-party license manifest.

## macOS build

```bash
cd 10-tools/software/congguo-depth-studio
make install
make install-model MODEL=/absolute/path/depth_anything_v2_vits.onnx
make lint
make test
make build-macos
```

The build script validates the model, installs/updates build dependencies, runs PyInstaller, and verifies the ad-hoc signed app. Expected output: `dist/葱果深度工坊.app`.

## Packaged acceptance

```bash
codesign --verify --deep --strict --verbose=2 'dist/葱果深度工坊.app'
plutil -p 'dist/葱果深度工坊.app/Contents/Info.plist'
QT_QPA_PLATFORM=minimal DEPTH_STUDIO_SMOKE_TEST=1 \
  'dist/葱果深度工坊.app/Contents/MacOS/CongGuoDepthStudio'
```

Verify bundle identifier `com.congguo.depthstudio`, version consistency, icon, model readiness, and bundle size. Then run the executable inside the app bundle against a short sanitized clip:

```bash
QT_QPA_PLATFORM=minimal \
DEPTH_STUDIO_PROCESS_TEST_INPUT=/tmp/sample.mp4 \
DEPTH_STUDIO_PROCESS_TEST_OUTPUT=/tmp/sample-depth.mp4 \
  'dist/葱果深度工坊.app/Contents/MacOS/CongGuoDepthStudio'
```

Testing source code alone cannot detect omitted bundle resources or libraries.

Verify the embedded CLI before installing the lightweight launcher:

```bash
'dist/葱果深度工坊.app/Contents/MacOS/CongGuoDepthStudio' --cgcli --version
'dist/葱果深度工坊.app/Contents/MacOS/CongGuoDepthStudio' \
  --cgcli --output-format json --progress none video depth \
  /tmp/sample.mp4 --output /tmp/sample-depth.mp4
```

The CLI invocation must use the model and processing libraries inside this same App Bundle.

## Visual acceptance

- First launch stays inside the screen's available geometry.
- `680x600` scrolls instead of overlapping.
- Congguo artwork is not clipped and Chinese text renders correctly.
- Drop feedback immediately shows file name, dimensions, and duration.
- Success adds the file to Recent Outputs; Play and Reveal work.
- Cancellation, overwrite confirmation, and closing during processing behave correctly.

## Archive and checksum

```bash
cd dist
ditto -c -k --sequesterRsrc --keepParent \
  '葱果深度工坊.app' '葱果深度工坊-v2.1-macOS-arm64.zip'
shasum -a 256 '葱果深度工坊-v2.1-macOS-arm64.zip'
```

Do not commit the app, ZIP, model, or test video. Store release artifacts in company object storage/release infrastructure and record version, checksum, build commit, and date.

## Signing and notarization

The current internal artifact is ad-hoc signed. An external macOS release requires Developer ID Application signing, Apple notarization, and stapling. Credentials belong in CI secret storage, never in Git.

## Windows path

The application does not need a rewrite. `app.py`, `widgets.py`, `styles.py`, and `depth_processor.py` are shared, and Reveal already has an `explorer.exe /select,` branch. Windows work is packaging and platform acceptance:

1. Build on Windows x64; PyInstaller does not cross-compile from macOS.
2. Add `packaging/windows/DepthMotionStudio.spec` for a GUI EXE/onedir artifact; do not use macOS `BUNDLE`.
3. Supply an `.ico`, Windows version metadata, and code signing.
4. Verify the Windows ONNX Runtime, OpenCV, and imageio-ffmpeg binaries are collected.
5. Test at 100%, 125%, and 150% DPI, including Chinese fonts, drag-and-drop, playback, and Explorer reveal.
6. Validate the signed artifact on a clean Windows machine.

If DirectML is added, capability-detect it and keep CPU fallback. Do not fork the processing algorithm by platform.

## Release checklist

- [ ] Clean build commit recorded.
- [ ] Version matches in `pyproject.toml`, `__init__.py`, spec, and changelog.
- [ ] Lint, unit, smoke, packaged end-to-end, and real-UI checks pass.
- [ ] Model and dependency license review is current.
- [ ] Signing/notarization matches the target audience.
- [ ] Artifact checksum and rollback version are recorded outside Git.
- [ ] `.venv`, `build/`, PyInstaller COLLECT output, and temporary test files are cleaned.
