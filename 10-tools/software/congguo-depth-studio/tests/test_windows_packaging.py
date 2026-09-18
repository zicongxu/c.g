import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]


def test_windows_spec_is_valid_python_and_collects_shared_runtime() -> None:
    spec_path = PROJECT_ROOT / "packaging/windows/DepthMotionStudio.spec"
    source = spec_path.read_text(encoding="utf-8")

    ast.parse(source)
    assert "BUNDLE(" not in source
    assert 'name="CongGuoDepthStudio"' in source
    assert 'name="CongGuoCliHost"' in source
    assert 'console=False' in source
    assert 'console=True' in source
    assert '"cgcli.cli"' in source
    assert "depth_anything_v2_vits.onnx" in source


def test_windows_build_script_verifies_both_hosts() -> None:
    source = (PROJECT_ROOT / "scripts/build-windows.ps1").read_text(encoding="utf-8")

    assert "DepthMotionStudio.spec" in source
    assert "CongGuoDepthStudio.exe" in source
    assert "CongGuoCliHost.exe" in source
    assert "--cgcli --version" in source
    assert "ready=True" in source


def test_windows_download_uses_pinned_model_and_expected_hash() -> None:
    source = (PROJECT_ROOT / "scripts/download-model.ps1").read_text(encoding="utf-8")

    assert "daec18e762798acb835d3cda7542d9ecee0dc16b" in source
    assert "d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be" in source
    assert "Get-FileHash -Algorithm SHA256" in source
