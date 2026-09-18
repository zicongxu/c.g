from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional, TextIO

from .errors import CliError


@dataclass(frozen=True)
class OutputOptions:
    output_format: str
    quiet: bool
    progress: str


class OutputWriter:
    """Keep result data on stdout and human progress on stderr."""

    def __init__(
        self,
        options: OutputOptions,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
    ) -> None:
        self.options = options
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    def success(self, payload: Dict[str, Any], message: str = "Completed") -> None:
        envelope = {"ok": True, **payload}
        if self.options.output_format == "json":
            print(json.dumps(envelope, ensure_ascii=False, sort_keys=True), file=self.stdout)
        elif not self.options.quiet:
            print(message, file=self.stdout)

    def error(self, error: CliError) -> None:
        if self.options.output_format == "json":
            envelope = {
                "ok": False,
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "details": error.details,
                },
            }
            print(json.dumps(envelope, ensure_ascii=False, sort_keys=True), file=self.stdout)
        else:
            print(f"Error [{error.code}]: {error.message}", file=self.stderr)

    def progress(self, percent: int, message: str, eta: Optional[float]) -> None:
        if self.options.quiet or self.options.progress == "none":
            return
        if self.options.progress == "auto" and not self.stderr.isatty():
            return
        eta_text = "" if eta is None else f" · ETA {max(0, round(eta))}s"
        print(f"{percent:3d}% · {message}{eta_text}", file=self.stderr)
