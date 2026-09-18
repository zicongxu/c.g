from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class CliError(Exception):
    """A stable command failure that can be rendered as text or JSON."""

    code: str
    message: str
    exit_code: int
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.message


class CliUsageError(CliError):
    def __init__(self, message: str):
        super().__init__("INVALID_INVOCATION", message, 2)
