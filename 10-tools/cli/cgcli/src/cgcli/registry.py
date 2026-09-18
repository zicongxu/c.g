from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Callable, List

from .output import OutputWriter

CommandHandler = Callable[[argparse.Namespace, OutputWriter], int]
CommandRegistrar = Callable[[argparse._SubParsersAction], None]


@dataclass(frozen=True)
class CommandDefinition:
    domain: str
    register: CommandRegistrar


def command_definitions() -> List[CommandDefinition]:
    """Return built-in domains; future plugins can extend this boundary."""

    from .commands.video import register_video_commands

    return [CommandDefinition(domain="video", register=register_video_commands)]


def register_commands(subparsers: argparse._SubParsersAction) -> None:
    for definition in command_definitions():
        definition.register(subparsers)
