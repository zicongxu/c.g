---
title: Congguo Depth Studio Build and Release Guide
summary: Model preparation, macOS and Windows packaging, and release acceptance
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
- Apple Silicon Mac, macOS 13+, and Python 3.9-3.13 for macOS.
- Windows 10/11 x64, PowerShell 5.1+, and Python 3.12 x64 for Windows.
- The accepted `depth_anything_v2_vits.onnx`, verified by SHA-256.
- For external release: Developer ID credentials, notarization credentials, and an approved third-party license manifest.

## macOS build

```bash
cd 10-tools/software/congguo-depth-studio
make install
make download-model
make lint
make test
make build-macos
```

For an offline or controlled release environment, replace `make download-model` with
`make install-model MODEL=/absolute/path/depth_anything_v2_vits.onnx`. Both paths enforce the same
accepted SHA-256.

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
  '葱果深度工坊.app' '葱果深度工坊-v2.4.0-macOS-arm64.zip'
shasum -a 256 '葱果深度工坊-v2.4.0-macOS-arm64.zip'
```

Do not commit the app, ZIP, model, or test video. Store release artifacts in company object
storage/release infrastructure and record version, checksum, build commit, date, and a retrievable
artifact location. Until that location exists, onboarding documentation must explicitly state that
the release owner supplies the ZIP; do not imply that a Git clone contains a runnable App.

## Signing and notarization

The current internal artifact is ad-hoc signed. An external macOS release requires Developer ID Application signing, Apple notarization, and stapling. Credentials belong in CI secret storage, never in Git.

## Windows x64 build

Build on Windows; PyInstaller does not cross-compile from macOS:

```powershell
cd 10-tools\software\congguo-depth-studio
.\scripts\setup-windows.ps1
.\scripts\build-windows.ps1
```

The build uses `packaging\windows\DepthMotionStudio.spec` and produces one portable directory with
two executable hosts. `CongGuoDepthStudio.exe` uses the Windows GUI subsystem;
`CongGuoCliHost.exe` uses the console subsystem so automation receives stdout, stderr, and exit
codes. Both use the same `_internal` directory, model, dependencies, and Python implementation.

The build script verifies the model, runs App and CLI tests, runs PyInstaller, checks both hosts,
smoke-tests `cgcli --version`, smoke-tests model discovery through the console host, and creates
`dist\congguo-depth-studio-v2.4.0-windows-x64.zip`. CI repeats the build but deliberately does not upload
the proprietary portable artifact from this public repository.

Follow [`windows.md`](windows.md) for clean-machine, DPI, Explorer, launcher, and offline acceptance.
If DirectML is added, capability-detect it and keep CPU fallback. Do not fork the processing
algorithm by platform.

## Release checklist

- [ ] Clean build commit recorded.
- [ ] Version matches in `pyproject.toml`, `__init__.py`, spec, and changelog.
- [ ] Lint, unit, smoke, packaged end-to-end, and real-UI checks pass.
- [ ] Model and dependency license review is current.
- [ ] Signing/notarization matches the target audience.
- [ ] Windows CI passes when Windows packaging or shared runtime code changes.
- [ ] Artifact checksum and rollback version are recorded outside Git.
- [ ] `.venv`, `build/`, PyInstaller COLLECT output, and temporary test files are cleaned.
