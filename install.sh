#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -m venv "$repo_dir/.venv"
"$repo_dir/.venv/bin/python" -m pip install --upgrade pip
"$repo_dir/.venv/bin/python" -m pip install -r "$repo_dir/requirements.txt"

codex_dir="${CODEX_HOME:-$HOME/.codex}"
skill_source="$repo_dir/skill/gerar-planos-pre-maternal"
skill_target="$codex_dir/skills/gerar-planos-pre-maternal"

mkdir -p "$codex_dir/skills"
if [[ -e "$skill_target" && ! -L "$skill_target" ]]; then
  echo "Já existe uma pasta em $skill_target; remova-a ou mova-a antes de instalar."
  exit 1
fi

ln -sfn "$skill_source" "$skill_target"
echo "Skill instalada em $skill_target"
echo "Ambiente Python criado em $repo_dir/.venv"
