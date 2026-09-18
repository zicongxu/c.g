from __future__ import annotations

import os
import subprocess
from pathlib import Path

LAUNCHER = Path(__file__).parents[1] / "launcher" / "cgcli"


def test_launcher_delegates_arguments_to_app_bundle(tmp_path) -> None:
    app = tmp_path / "葱果深度工坊.app"
    executable = app / "Contents" / "MacOS" / "CongGuoDepthStudio"
    executable.parent.mkdir(parents=True)
    executable.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\"\n", encoding="utf-8")
    executable.chmod(0o755)
    environment = {**os.environ, "CGCLI_APP_PATH": str(app)}

    result = subprocess.run(
        [str(LAUNCHER), "--output-format", "json", "video", "depth", "input.mp4"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "--cgcli",
        "--output-format",
        "json",
        "video",
        "depth",
        "input.mp4",
    ]


def test_launcher_reports_missing_app(tmp_path) -> None:
    environment = {
        **os.environ,
        "CGCLI_APP_PATH": str(tmp_path / "missing.app"),
    }

    result = subprocess.run(
        [str(LAUNCHER), "--version"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 3
    assert "app runtime is missing" in result.stderr
