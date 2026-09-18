#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/depth_anything_v2_vits.onnx" >&2
  exit 2
fi

project_root="$(cd "$(dirname "$0")/.." && pwd)"
source_model="$1"
target_model="$project_root/src/congguo_depth_studio/resources/depth_anything_v2_vits.onnx"
expected_sha256="d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be"

if [[ ! -f "$source_model" ]]; then
  echo "Model not found: $source_model" >&2
  exit 1
fi

actual_sha256="$(shasum -a 256 "$source_model" | awk '{print $1}')"
if [[ "$actual_sha256" != "$expected_sha256" ]]; then
  echo "Model SHA-256 mismatch." >&2
  echo "Expected: $expected_sha256" >&2
  echo "Actual:   $actual_sha256" >&2
  exit 1
fi

cp "$source_model" "$target_model"
echo "Installed model: $target_model"
