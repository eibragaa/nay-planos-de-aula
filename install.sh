#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
install_target="${1:---codex}"

if [[ "$install_target" != "--codex" && "$install_target" != "--hermes" && "$install_target" != "--both" ]]; then
  echo "Uso: ./install.sh [--codex|--hermes|--both]"
  exit 2
fi

python3 -m venv "$repo_dir/.venv"
"$repo_dir/.venv/bin/python" -m pip install --upgrade pip
"$repo_dir/.venv/bin/python" -m pip install -r "$repo_dir/requirements.txt"

skill_source="$repo_dir/skill/gerar-planos-pre-maternal"

install_skill_link() {
  local agent_root="$1"
  local skill_target="$agent_root/skills/gerar-planos-pre-maternal"

  mkdir -p "$agent_root/skills"
  if [[ -e "$skill_target" && ! -L "$skill_target" ]]; then
    echo "Já existe uma pasta em $skill_target; remova-a ou mova-a antes de instalar."
    exit 1
  fi

  ln -sfn "$skill_source" "$skill_target"
  echo "Skill instalada em $skill_target"
}

if [[ "$install_target" == "--codex" || "$install_target" == "--both" ]]; then
  codex_root="${CODEX_HOME:-$HOME/.codex}"
  install_skill_link "$codex_root"
fi

if [[ "$install_target" == "--hermes" || "$install_target" == "--both" ]]; then
  hermes_root="${HERMES_HOME:-$HOME/.hermes}"
  install_skill_link "$hermes_root"
fi

mkdir -p "$repo_dir/outputs"
echo "Ambiente Python criado em $repo_dir/.venv"
