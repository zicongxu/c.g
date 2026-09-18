from pathlib import Path

import numpy as np

from congguo_depth_studio.app import MainWindow, resource_path
from congguo_depth_studio.depth_processor import DepthProcessor


def test_preprocess_shape_and_dtype() -> None:
    frame = np.zeros((32, 48, 3), dtype=np.uint8)
    tensor = DepthProcessor._preprocess(frame)

    assert tensor.shape == (1, 3, 518, 518)
    assert tensor.dtype == np.float32
    assert tensor.flags.c_contiguous


def test_eta_formatting() -> None:
    assert MainWindow._format_eta(12.9) == "约 12 秒"
    assert MainWindow._format_eta(125) == "约 2 分 5 秒"


def test_brand_asset_is_versioned() -> None:
    assert resource_path("brand/cong-guo-app-icon.png").is_file()


def test_model_is_deliberately_external() -> None:
    model = (
        Path(__file__).parents[1]
        / "src/congguo_depth_studio/resources/depth_anything_v2_vits.onnx"
    )
    assert not model.is_file() or model.stat().st_size > 90_000_000
