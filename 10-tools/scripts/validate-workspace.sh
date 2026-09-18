#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
cd "$repo_root"

errors=0

required_files=(
  "AGENTS.md"
  "CLAUDE.md"
  ".github/copilot-instructions.md"
  ".cursor/rules/00-workspace-routing.mdc"
  "INDEX.md"
  "knowledge-map.yaml"
  "KNOWLEDGE.md"
  "STORAGE.md"
  "02-products/registry.yaml"
  "03-studio/projects/registry.yaml"
  "04-research/models/registry.yaml"
  "05-engineering/repositories/registry.yaml"
  "09-ai/agents/registry.yaml"
  "09-ai/skills/registry.yaml"
  "09-ai/prompts/registry.yaml"
  "09-ai/workflows/registry.yaml"
  "10-tools/cli/registry.yaml"
  "10-tools/integrations/registry.yaml"
  "10-tools/software/registry.yaml"
)

for required_file in "${required_files[@]}"; do
  if [[ ! -f "$required_file" ]]; then
    echo "ERROR missing required file: $required_file"
    errors=$((errors + 1))
  fi
done

while IFS= read -r registry_file; do
  while IFS= read -r registered_path; do
    registered_path="${registered_path#\"}"
    registered_path="${registered_path%\"}"
    registered_path="${registered_path#\'}"
    registered_path="${registered_path%\'}"

    if [[ ! -e "$registered_path" ]]; then
      echo "ERROR registry points to a missing path: $registry_file -> $registered_path"
      errors=$((errors + 1))
    fi
  done < <(sed -n 's/^[[:space:]]*path:[[:space:]]*//p' "$registry_file")
done < <(find . -path "./.git" -prune -o -type f -name "registry.yaml" -print | sort)

while IFS= read -r skill_dir; do
  skill_file="$skill_dir/SKILL.md"
  relative_skill_file="${skill_file#./}"

  if [[ ! -f "$skill_file" ]]; then
    echo "ERROR Skill package is missing SKILL.md: ${skill_dir#./}"
    errors=$((errors + 1))
    continue
  fi

  if ! grep -Fq "path: $relative_skill_file" "09-ai/skills/registry.yaml"; then
    echo "ERROR Skill is not registered: $relative_skill_file"
    errors=$((errors + 1))
  fi
done < <(find "09-ai/skills" -mindepth 1 -maxdepth 1 -type d | sort)

while IFS= read -r misplaced_skill; do
  echo "ERROR SKILL.md exists outside 09-ai/skills/: ${misplaced_skill#./}"
  errors=$((errors + 1))
done < <(find . -path "./.git" -prune -o -type f -name "SKILL.md" -not -path "./09-ai/skills/*" -print | sort)

if [[ $errors -gt 0 ]]; then
  echo "Workspace validation failed with $errors error(s)."
  exit 1
fi

echo "Workspace validation passed."
