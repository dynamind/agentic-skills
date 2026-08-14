#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Synchronize the repository's dm-* skills with global Codex and Claude Code skills.

Usage: ./install-skills.sh [--dry-run] [--codex-only | --claude-only]

Environment overrides:
  CODEX_SKILLS_DIR    Default: ~/.codex/skills
  CODEX_SKILLS_DIR    Default: ~/.codex/skills
  CLAUDE_SKILLS_DIR   Default: ~/.claude/skills
EOF
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
agents_dir="${CODEX_SKILLS_DIR:-$HOME/.agents/skills}"
codex_dir="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
claude_dir="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
dry_run=false
install_agents=true
install_codex=true
install_claude=true

for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=true ;;
    --agents-only) install_agents=true; install_codex=false; install_claude=false ;;
    --codex-only) install_agents=false; install_codex=true; install_claude=false ;;
    --claude-only) install_agents=false; install_codex=false; install_claude=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

if ! command -v rsync >/dev/null 2>&1; then
  echo "Error: rsync is required to synchronize skills." >&2
  exit 1
fi

skill_count=0
for skill_dir in "$repo_root"/dm-*; do
  [[ -d "$skill_dir" && -f "$skill_dir/SKILL.md" ]] || continue
  skill_name="$(basename "$skill_dir")"
  skill_count=$((skill_count + 1))

  for target_dir in "$codex_dir" "$claude_dir"; do
    [[ "$target_dir" == "$codex_dir" && "$install_codex" == true ]] || \
    [[ "$target_dir" == "$claude_dir" && "$install_claude" == true ]] || continue

    destination="$target_dir/$skill_name"
    [[ "$dry_run" == true ]] || mkdir -p "$destination"

    rsync_args=(-a --delete)
    [[ "$dry_run" == true ]] && rsync_args+=(--dry-run --itemize-changes)
    rsync "${rsync_args[@]}" "$skill_dir/" "$destination/"
    echo "Synchronized $skill_name -> $destination"
  done
done

if [[ "$skill_count" -eq 0 ]]; then
  echo "Error: no root dm-* skill directories containing SKILL.md were found." >&2
  exit 1
fi

echo "Synchronized $skill_count skill(s)."
