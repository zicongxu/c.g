---
title: Congguo Depth Studio Windows Guide
summary: Clean-machine source setup, portable build, cgcli installation, and Windows acceptance
status: draft
owner: Congguo Product Team
updated: 2026-09-19
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [windows, installation, build, cgcli]
related: [../README.md, development.md, build-and-release.md]
---

# Windows setup and packaging

This is the canonical clean-machine path for Windows 10/11 x64. It uses the same Python, PySide6,
ONNX Runtime, OpenCV, FFmpeg, model, processing API, and cgcli command implementation as macOS.
Windows adds packaging and launcher files; it does not fork the depth algorithm.

## Prerequisites

- Windows 10 or 11 x64.
- Python 3.12 x64 from python.org, with the `py` launcher enabled. Python 3.9-3.13 is supported, but
  3.12 is the build baseline.
- PowerShell 5.1 or newer.
- Git and at least 5 GB of free temporary disk space.
- Network access for Python packages and the revision-pinned ONNX model on first setup.

No Codex, ChatGPT, API key, Visual Studio compiler, CUDA, or administrator permission is required.

## Run from source

Open PowerShell at the repository root:

```powershell
cd 10-tools\software\congguo-depth-studio
.\scripts\setup-windows.ps1
.\.venv\Scripts\python.exe -m congguo_depth_studio
```

The setup script creates `.venv`, installs App and cgcli development dependencies, downloads the
pinned public ONNX artifact, and verifies its SHA-256. If script execution is blocked, use a
process-scoped policy without changing the machine policy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

If Python was installed without the `py` launcher:

```powershell
.\scripts\setup-windows.ps1 -PythonCommand python
```

The development CLI is immediately available inside the same environment:

```powershell
.\.venv\Scripts\cgcli.exe --version
.\.venv\Scripts\cgcli.exe video depth C:\path\input.mp4
```

## Build the portable App

PyInstaller must run on Windows; a macOS machine cannot cross-compile the Windows executable.

```powershell
.\scripts\build-windows.ps1
```

The script runs Ruff and both projects' tests, builds the package, then smoke-tests the GUI runtime
and embedded CLI. Outputs:

```text
dist\CongGuoDepthStudio\
  CongGuoDepthStudio.exe    GUI host; no console window
  CongGuoCliHost.exe        console host used by cgcli and automation
  _internal\...             one shared runtime, libraries, model, and application code

dist\congguo-depth-studio-v2.4.0-windows-x64.zip
```

The two small hosts intentionally share one `_internal` directory. This preserves CLI stdout,
stderr, pipes, and exit codes on Windows without installing a second inference runtime or model.

## Install production cgcli

The portable App directory may live anywhere and must remain intact. From the repository root:

```powershell
cd 10-tools\cli\cgcli
.\scripts\install-launcher-windows.ps1 `
  -AppPath ..\..\software\congguo-depth-studio\dist\CongGuoDepthStudio
```

The installer copies only `cgcli.cmd` to `%LOCALAPPDATA%\Congguo\bin`, records the CLI Host path in
`%LOCALAPPDATA%\Congguo\cgcli-app-path.txt`, and adds the launcher directory to the user PATH. Open
a new PowerShell window, then verify:

```powershell
cgcli --version
cgcli video depth --help
```

`CGCLI_APP_PATH` can override the recorded host with either the portable App directory or the full
path to `CongGuoCliHost.exe`.

## Clean-machine acceptance

Before distributing the ZIP, validate on a Windows account that has no project virtual environment:

1. Extract the complete `CongGuoDepthStudio` directory; do not copy only the EXE.
2. Launch `CongGuoDepthStudio.exe`; verify Chinese text, drag/drop, and 100%, 125%, and 150% DPI.
3. Process a sanitized 0.5-2 second video with audio.
4. Verify Recent Outputs, Play, and Explorer Reveal.
5. Install the launcher and verify text mode, JSON mode, errors, cancellation, and exit codes.
6. Confirm processing works after disconnecting the network.

The current internal build is unsigned, so Windows SmartScreen may warn. External distribution
requires an approved code-signing certificate and a clean-machine malware/signing review.

## Uninstall

Delete the portable App directory, `%LOCALAPPDATA%\Congguo\bin\cgcli.cmd`, and
`%LOCALAPPDATA%\Congguo\cgcli-app-path.txt`. Optionally remove the launcher directory from the user
PATH. Input videos and generated outputs are never removed by uninstalling.
