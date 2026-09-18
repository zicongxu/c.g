# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs


project_root = Path(SPECPATH).parents[1]
package_root = project_root / "src" / "congguo_depth_studio"
cgcli_source_root = project_root.parents[1] / "cli" / "cgcli" / "src"
windows_root = project_root / "packaging" / "windows"

datas = [
    (str(package_root / "resources" / "depth_anything_v2_vits.onnx"), "resources"),
    (str(package_root / "resources" / "brand"), "resources/brand"),
]
datas += collect_data_files("imageio_ffmpeg")

binaries = collect_dynamic_libs("onnxruntime")

a = Analysis(
    [str(project_root / "packaging" / "pyinstaller_entry.py")],
    pathex=[str(project_root / "src"), str(cgcli_source_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        "cv2",
        "imageio_ffmpeg",
        "onnxruntime",
        "cgcli.cli",
        "cgcli.commands.video",
        "cgcli.commands.video_depth",
        "congguo_depth_studio.api",
        "congguo_depth_studio.contracts",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtQml"],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

# Windows needs separate GUI and console-subsystem hosts so cgcli keeps working in pipes and agents.
# Both hosts share the same COLLECT directory, libraries, model, and Python implementation.
gui_exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CongGuoDepthStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon=str(package_root / "resources" / "brand" / "CongGuo.ico"),
    version=str(windows_root / "version_info.txt"),
)

cli_exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CongGuoCliHost",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    icon=str(package_root / "resources" / "brand" / "CongGuo.ico"),
    version=str(windows_root / "version_info.txt"),
)

coll = COLLECT(
    gui_exe,
    cli_exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="CongGuoDepthStudio",
)
