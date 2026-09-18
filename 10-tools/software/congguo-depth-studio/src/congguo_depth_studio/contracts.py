"""Lightweight shared types for depth-processing callers and providers."""

from typing import Callable, Optional

ProgressCallback = Callable[[int, str, Optional[float]], None]
CancelCallback = Callable[[], bool]


class ProcessingCancelled(RuntimeError):
    """Raised when a caller requests cooperative processing cancellation."""
