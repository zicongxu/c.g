from __future__ import annotations

import argparse

from .video_depth import run_video_depth


def register_video_commands(root_subparsers: argparse._SubParsersAction) -> None:
    video = root_subparsers.add_parser("video", help="Video processing capabilities")
    capabilities = video.add_subparsers(
        dest="video_capability", title="capabilities", required=True
    )

    depth = capabilities.add_parser(
        "depth", help="Convert a monocular video into a relative-depth MP4"
    )
    depth.add_argument("input", help="Input video path")
    depth.add_argument("-o", "--output", help="Output MP4; defaults to INPUT_depth.mp4")
    depth.add_argument("--model", help="Depth Anything V2 Small ONNX model path")
    depth.add_argument("--fps", type=int, choices=(24, 30, 60), default=30)
    depth.add_argument(
        "--keep-audio",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Preserve source audio when present (default: true)",
    )
    depth.add_argument(
        "--overwrite", action="store_true", help="Replace an existing output file"
    )
    depth.set_defaults(command_handler=run_video_depth)
