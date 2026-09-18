#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_root"

model_path="src/congguo_depth_studio/resources/depth_anything_v2_vits.onnx"
expected_sha256="d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be"

if [[ ! -f "$model_path" ]]; then
  echo "Missing model. Run: ./scripts/install-model.sh /path/to/depth_anything_v2_vits.onnx" >&2
  exit 1
fi

actual_sha256="$(shasum -a 256 "$model_path" | awk '{print $1}')"
if [[ "$actual_sha256" != "$expected_sha256" ]]; then
  echo "Model SHA-256 mismatch; refusing to build." >&2
  exit 1
fi

if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -e '.[build]'
cache_dir="${TMPDIR:-/tmp}/congguo-depth-studio-pyinstaller"
PYINSTALLER_CONFIG_DIR="$cache_dir" .venv/bin/pyinstaller \
  --noconfirm \
  --clean \
  packaging/macos/DepthMotionStudio.spec

codesign --verify --deep --strict "dist/葱果深度工坊.app"
echo "Built: $project_root/dist/葱果深度工坊.app"
