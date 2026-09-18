from __future__ import annotations

import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace

from cgcli.cli import build_parser, main
from cgcli.commands import video_depth


class FakeDepthError(RuntimeError):
    code = "FAKE_DEPTH_ERROR"


class FakeCancelled(RuntimeError):
    pass


def fake_api(elapsed_seconds: float = 1.25) -> SimpleNamespace:
    def request(**kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(**kwargs)

    def extract(job: SimpleNamespace, progress, cancelled) -> SimpleNamespace:
        assert not cancelled()
        progress(50, "halfway", 2.0)
        return SimpleNamespace(
            input_path=job.input_path,
            output_path=job.output_path,
            fps=job.fps,
            keep_audio=job.keep_audio,
            elapsed_seconds=elapsed_seconds,
        )

    return SimpleNamespace(
        DepthRequest=request,
        extract_depth_video=extract,
        default_model_path=lambda: Path("/unused/default.onnx"),
        ProcessingCancelled=FakeCancelled,
        OutputAlreadyExists=FakeDepthError,
        DepthModelNotFound=FakeDepthError,
        InputVideoNotFound=FakeDepthError,
        InvalidDepthRequest=FakeDepthError,
    )


def test_parser_keeps_global_and_capability_options_separate() -> None:
    args = build_parser().parse_args(
        [
            "--output-format",
            "json",
            "--progress",
            "none",
            "video",
            "depth",
            "input.mov",
            "--fps",
            "60",
            "--no-keep-audio",
        ]
    )

    assert args.domain == "video"
    assert args.video_capability == "depth"
    assert args.output_format == "json"
    assert args.progress == "none"
    assert args.fps == 60
    assert args.keep_audio is False


def test_video_depth_emits_machine_readable_success(tmp_path, monkeypatch) -> None:
    source = tmp_path / "source.mov"
    model = tmp_path / "depth.onnx"
    source.touch()
    model.touch()
    monkeypatch.setattr(video_depth, "_load_depth_api", fake_api)
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(
            [
                "--output-format",
                "json",
                "--progress",
                "none",
                "video",
                "depth",
                str(source),
                "--model",
                str(model),
            ]
        )

    assert exit_code == 0
    result = json.loads(stdout.getvalue())
    assert result["command"] == "video.depth"
    assert result["output_path"] == str(tmp_path / "source_depth.mp4")
    assert result["ok"] is True


def test_existing_output_is_rejected_before_loading_capability(tmp_path, monkeypatch) -> None:
    source = tmp_path / "source.mp4"
    output = tmp_path / "result.mp4"
    source.touch()
    output.touch()

    def should_not_load():
        raise AssertionError("capability should not load for an output conflict")

    monkeypatch.setattr(video_depth, "_load_depth_api", should_not_load)
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(
            [
                "--output-format",
                "json",
                "video",
                "depth",
                str(source),
                "--output",
                str(output),
            ]
        )

    assert exit_code == 4
    assert '"code": "OUTPUT_ALREADY_EXISTS"' in stdout.getvalue()
    assert '"ok": false' in stdout.getvalue()


def test_missing_input_uses_stable_exit_code(tmp_path) -> None:
    stderr = io.StringIO()

    with redirect_stderr(stderr):
        exit_code = main(["video", "depth", str(tmp_path / "missing.mp4")])

    assert exit_code == 3
    assert "INPUT_VIDEO_NOT_FOUND" in stderr.getvalue()


def test_missing_provider_uses_capability_error(tmp_path, monkeypatch) -> None:
    source = tmp_path / "source.mp4"
    source.touch()

    def missing_provider(_name):
        raise ModuleNotFoundError("provider missing")

    monkeypatch.setattr(video_depth.importlib, "import_module", missing_provider)
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(
            ["--output-format", "json", "video", "depth", str(source)]
        )

    assert exit_code == 3
    assert '"code": "CAPABILITY_UNAVAILABLE"' in stdout.getvalue()


def test_cancellation_uses_exit_130(tmp_path, monkeypatch) -> None:
    source = tmp_path / "source.mp4"
    model = tmp_path / "depth.onnx"
    source.touch()
    model.touch()
    api = fake_api()

    def cancel(_job, progress, cancelled):
        raise FakeCancelled("operation cancelled")

    api.extract_depth_video = cancel
    monkeypatch.setattr(video_depth, "_load_depth_api", lambda: api)
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(
            [
                "--output-format",
                "json",
                "video",
                "depth",
                str(source),
                "--model",
                str(model),
            ]
        )

    assert exit_code == 130
    assert '"code": "CANCELLED"' in stdout.getvalue()


def test_invalid_invocation_can_be_json() -> None:
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(["--output-format", "json", "video", "depth"])

    assert exit_code == 2
    assert '"code": "INVALID_INVOCATION"' in stdout.getvalue()
    assert '"ok": false' in stdout.getvalue()
