"""PyInstaller entry point; kept outside the package for reliable absolute imports."""

from congguo_depth_studio.app import main


if __name__ == "__main__":
    raise SystemExit(main())
