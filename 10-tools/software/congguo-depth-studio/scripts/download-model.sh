#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/.." && pwd)"
target_model="$project_root/src/congguo_depth_studio/resources/depth_anything_v2_vits.onnx"
default_model_url="https://huggingface.co/CyberTimon/RapidRAW-Models/resolve/"
default_model_url+="daec18e762798acb835d3cda7542d9ecee0dc16b/"
default_model_url+="depth_anything_v2_vits.onnx?download=true"
model_url="${DEPTH_STUDIO_MODEL_URL:-$default_model_url}"
expected_sha256="d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be"

if [[ -f "$target_model" ]]; then
  installed_sha256="$(shasum -a 256 "$target_model" | awk '{print $1}')"
  if [[ "$installed_sha256" == "$expected_sha256" ]]; then
    echo "Model already installed and verified: $target_model"
    exit 0
  fi
fi

temporary_model="$(mktemp "$target_model.download.XXXXXX")"
cleanup() {
  rm -f "$temporary_model"
}
trap cleanup EXIT INT TERM

echo "Downloading the pinned Depth Anything V2 Small ONNX artifact..."
curl --fail --location --retry 3 --output "$temporary_model" "$model_url"

actual_sha256="$(shasum -a 256 "$temporary_model" | awk '{print $1}')"
if [[ "$actual_sha256" != "$expected_sha256" ]]; then
  echo "Model SHA-256 mismatch; refusing to install." >&2
  echo "Expected: $expected_sha256" >&2
  echo "Actual:   $actual_sha256" >&2
  exit 1
fi

chmod 644 "$temporary_model"
mv -f "$temporary_model" "$target_model"
trap - EXIT INT TERM
echo "Downloaded and verified model: $target_model"
