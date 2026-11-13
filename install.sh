#!/bin/sh
# Link every skill (skills/<category>/<skill>/) into ~/.claude/skills so Claude Code finds it.
# Usage: sh install.sh [category]     e.g. sh install.sh video
set -e
here="$(cd "$(dirname "$0")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest"
n=0
for s in "$here"/skills/${1:-*}/*/; do
  [ -f "$s/SKILL.md" ] || continue
  ln -sfn "${s%/}" "$dest/$(basename "$s")"; n=$((n+1))
done
echo "linked $n skills into $dest"
