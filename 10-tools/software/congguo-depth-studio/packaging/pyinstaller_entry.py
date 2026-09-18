"""Shared packaged entry point for the desktop UI and the embedded cgcli runtime."""

from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--cgcli":
        from cgcli.cli import main as cli_main

        return cli_main(sys.argv[2:])

    from congguo_depth_studio.app import main as app_main

    return app_main()


if __name__ == "__main__":
    raise SystemExit(main())
