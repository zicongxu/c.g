"""Public, UI-independent API for Congguo depth-video extraction."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .contracts import CancelCallback, ProcessingCancelled, ProgressCallback

SUPPORTED_VIDEO_EXTENSIONS = frozenset({".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"})
SUPPORTED_OUTPUT_FPS = frozenset({24, 30, 60})


class DepthCapabilityError(RuntimeError):
    """Base class for stable public capability errors."""

    code = "DEPTH_CAPABILITY_ERROR"


class InvalidDepthRequest(DepthCapabilityError):
    code = "INVALID_DEPTH_REQUEST"


class InputVideoNotFound(DepthCapabilityError):
    code = "INPUT_VIDEO_NOT_FOUND"


class DepthModelNotFound(DepthCapabilityError):
    code = "DEPTH_MODEL_NOT_FOUND"


class OutputAlreadyExists(DepthCapabilityError):
    code = "OUTPUT_ALREADY_EXISTS"


@dataclass(frozen=True)
class DepthRequest:
    """Validated inputs for one local depth-video extraction job."""

    input_path: Path
    output_path: Path
    model_path: Path
    fps: int = 30
    keep_audio: bool = True
    overwrite: bool = False


@dataclass(frozen=True)
class DepthResult:
    """Stable result returned after a completed extraction job."""

    input_path: Path
    output_path: Path
    model_path: Path
    fps: int
    keep_audio: bool
    elapsed_seconds: float


def default_model_path() -> Path:
    """Return the model location used by source and PyInstaller builds."""

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "resources" / "depth_anything_v2_vits.onnx"
    return Path(__file__).resolve().parent / "resources" / "depth_anything_v2_vits.onnx"


def _load_processor_type():
    # Keep the public contract importable for help, validation, and orchestration
    # without loading OpenCV, ONNX Runtime, or FFmpeg until work actually starts.
    from .depth_processor import DepthProcessor

    return DepthProcessor


def _validate_request(request: DepthRequest) -> None:
    if request.fps not in SUPPORTED_OUTPUT_FPS:
        raise InvalidDepthRequest("fps must be one of: 24, 30, 60")
    if not request.input_path.is_file():
        raise InputVideoNotFound(f"input video does not exist: {request.input_path}")
    if request.input_path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_VIDEO_EXTENSIONS))
        raise InvalidDepthRequest(f"unsupported input extension; expected one of: {supported}")
    if not request.model_path.is_file():
        raise DepthModelNotFound(f"depth model does not exist: {request.model_path}")
    if request.output_path.suffix.lower() != ".mp4":
        raise InvalidDepthRequest("output path must end in .mp4")
    if request.input_path.resolve() == request.output_path.resolve():
        raise InvalidDepthRequest("input and output paths must be different")
    if request.output_path.exists() and not request.overwrite:
        raise OutputAlreadyExists(f"output already exists: {request.output_path}")


def extract_depth_video(
    request: DepthRequest,
    progress: Optional[ProgressCallback] = None,
    cancelled: Optional[CancelCallback] = None,
) -> DepthResult:
    """Extract a relative-depth MP4 locally using the packaged ONNX pipeline.

    This is the supported automation boundary shared by ``cgcli`` and future
    non-Qt integrations. It performs no network requests.
    """

    _validate_request(request)
    progress_callback = progress or (lambda _value, _message, _eta: None)
    cancel_callback = cancelled or (lambda: False)
    started = time.monotonic()

    processor_type = _load_processor_type()
    processor = processor_type(request.model_path, progress_callback, cancel_callback)
    processor.run(request.input_path, request.output_path, request.fps, request.keep_audio)

    return DepthResult(
        input_path=request.input_path,
        output_path=request.output_path,
        model_path=request.model_path,
        fps=request.fps,
        keep_audio=request.keep_audio,
        elapsed_seconds=time.monotonic() - started,
    )


__all__ = [
    "DepthCapabilityError",
    "DepthModelNotFound",
    "DepthRequest",
    "DepthResult",
    "InputVideoNotFound",
    "InvalidDepthRequest",
    "OutputAlreadyExists",
    "ProcessingCancelled",
    "default_model_path",
    "extract_depth_video",
]
