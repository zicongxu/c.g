# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs


project_root = Path(SPECPATH).parents[1]
package_root = project_root / "src" / "congguo_depth_studio"
cgcli_source_root = project_root.parents[1] / "cli" / "cgcli" / "src"

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

exe = EXE(
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
    argv_emulation=False,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="CongGuoDepthStudio",
)

app = BUNDLE(
    coll,
    name="葱果深度工坊.app",
    icon=str(package_root / "resources" / "brand" / "CongGuo.icns"),
    bundle_identifier="com.congguo.depthstudio",
    info_plist={
        "CFBundleDisplayName": "葱果深度工坊",
        "CFBundleName": "葱果深度工坊",
        "CFBundleShortVersionString": "2.3.0",
        "CFBundleVersion": "6",
        "LSMinimumSystemVersion": "13.0",
        "NSHighResolutionCapable": True,
        "NSPrincipalClass": "NSApplication",
    },
)
