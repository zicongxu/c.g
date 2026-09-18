from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .errors import CliError, CliUsageError
from .output import OutputOptions, OutputWriter
from .registry import register_commands


class CGArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


def build_parser() -> argparse.ArgumentParser:
    parser = CGArgumentParser(
        prog="cgcli",
        description="Unified command-line interface for Congguo capabilities",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--output-format",
        choices=("text", "json"),
        default="text",
        help="Final result format written to stdout (default: text)",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress human-facing output")
    parser.add_argument(
        "--progress",
        choices=("auto", "plain", "none"),
        default="auto",
        help="Progress rendering on stderr (default: auto)",
    )
    domains = parser.add_subparsers(dest="domain", title="domains", required=True)
    register_commands(domains)
    return parser


def _requested_output_format(argv: List[str]) -> str:
    for index, value in enumerate(argv):
        if value.startswith("--output-format="):
            return value.split("=", 1)[1]
        if value == "--output-format" and index + 1 < len(argv):
            return argv[index + 1]
    return "text"


def main(argv: Optional[List[str]] = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    fallback_options = OutputOptions(
        output_format=_requested_output_format(arguments), quiet=False, progress="none"
    )
    writer = OutputWriter(fallback_options)
    try:
        args = build_parser().parse_args(arguments)
        writer = OutputWriter(
            OutputOptions(
                output_format=args.output_format,
                quiet=args.quiet,
                progress=args.progress,
            )
        )
        return args.command_handler(args, writer)
    except CliError as exc:
        writer.error(exc)
        return exc.exit_code


def entrypoint() -> None:
    raise SystemExit(main())
