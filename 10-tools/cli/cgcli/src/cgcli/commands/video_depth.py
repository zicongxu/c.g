from __future__ import annotations

import argparse
import importlib
import os
import signal
import threading
from pathlib import Path
from types import ModuleType

from ..errors import CliError
from ..output import OutputWriter


def _absolute_path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _load_depth_api() -> ModuleType:
    try:
        return importlib.import_module("congguo_depth_studio.api")
    except ImportError as exc:
        raise CliError(
            "CAPABILITY_UNAVAILABLE",
            "video.depth is not installed; install Congguo Depth Studio first",
            3,
            {"package": "congguo-depth-studio>=2.2,<3"},
        ) from exc


def _resolve_model(args: argparse.Namespace, api: ModuleType) -> Path:
    explicit = args.model or os.environ.get("CGCLI_DEPTH_MODEL")
    return _absolute_path(explicit) if explicit else api.default_model_path().resolve()


def run_video_depth(args: argparse.Namespace, output: OutputWriter) -> int:
    input_path = _absolute_path(args.input)
    output_path = (
        _absolute_path(args.output)
        if args.output
        else input_path.with_name(f"{input_path.stem}_depth.mp4")
    )

    if not input_path.is_file():
        raise CliError(
            "INPUT_VIDEO_NOT_FOUND",
            f"input video does not exist: {input_path}",
            3,
            {"input_path": str(input_path)},
        )
    if output_path.exists() and not args.overwrite:
        raise CliError(
            "OUTPUT_ALREADY_EXISTS",
            f"output already exists: {output_path}; pass --overwrite to replace it",
            4,
            {"output_path": str(output_path)},
        )

    api = _load_depth_api()
    model_path = _resolve_model(args, api)
    cancelled = threading.Event()
    previous_handler = signal.getsignal(signal.SIGINT)

    def request_cancel(_signum: int, _frame: object) -> None:
        cancelled.set()

    signal.signal(signal.SIGINT, request_cancel)
    try:
        request = api.DepthRequest(
            input_path=input_path,
            output_path=output_path,
            model_path=model_path,
            fps=args.fps,
            keep_audio=args.keep_audio,
            overwrite=args.overwrite,
        )
        result = api.extract_depth_video(
            request,
            progress=output.progress,
            cancelled=cancelled.is_set,
        )
    except api.ProcessingCancelled as exc:
        raise CliError("CANCELLED", str(exc) or "operation cancelled", 130) from exc
    except api.OutputAlreadyExists as exc:
        raise CliError(exc.code, str(exc), 4) from exc
    except (
        api.DepthModelNotFound,
        api.InputVideoNotFound,
        api.InvalidDepthRequest,
    ) as exc:
        raise CliError(exc.code, str(exc), 3) from exc
    except CliError:
        raise
    except Exception as exc:
        raise CliError("PROCESSING_FAILED", str(exc), 5) from exc
    finally:
        signal.signal(signal.SIGINT, previous_handler)

    output.success(
        {
            "command": "video.depth",
            "input_path": str(result.input_path),
            "output_path": str(result.output_path),
            "fps": result.fps,
            "keep_audio": result.keep_audio,
            "elapsed_seconds": round(result.elapsed_seconds, 3),
        },
        message=f"Completed: {result.output_path}",
    )
    return 0
