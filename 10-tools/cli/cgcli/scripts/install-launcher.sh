#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/.." && pwd)"
launcher="$project_root/launcher/cgcli"
requested_app="${1:-}"
requested_bin_dir="${2:-}"

if [[ -n "$requested_app" ]]; then
  app_path="$requested_app"
elif [[ -d "$HOME/Applications/葱果深度工坊.app" ]]; then
  app_path="$HOME/Applications/葱果深度工坊.app"
elif [[ -d "/Applications/葱果深度工坊.app" ]]; then
  app_path="/Applications/葱果深度工坊.app"
else
  echo "葱果深度工坊.app was not found." >&2
  echo "Install the app first, or run: make install APP=/absolute/path/葱果深度工坊.app" >&2
  exit 3
fi

app_executable="$app_path/Contents/MacOS/CongGuoDepthStudio"
if [[ ! -x "$app_executable" ]]; then
  echo "App runtime is missing or not executable: $app_executable" >&2
  exit 3
fi

if [[ -n "$requested_bin_dir" ]]; then
  bin_dir="$requested_bin_dir"
elif [[ -d "/opt/homebrew/bin" && -w "/opt/homebrew/bin" ]]; then
  bin_dir="/opt/homebrew/bin"
elif [[ -d "/usr/local/bin" && -w "/usr/local/bin" ]]; then
  bin_dir="/usr/local/bin"
else
  bin_dir="$HOME/.local/bin"
fi

mkdir -p "$bin_dir"
install -m 755 "$launcher" "$bin_dir/cgcli"
config_dir="$HOME/Library/Application Support/Congguo"
mkdir -p "$config_dir"
printf '%s\n' "$app_path" > "$config_dir/cgcli-app-path"

echo "Installed cgcli launcher: $bin_dir/cgcli"
echo "Using app runtime: $app_path"
if [[ ":$PATH:" != *":$bin_dir:"* ]]; then
  echo "Add this directory to PATH: $bin_dir" >&2
fi
