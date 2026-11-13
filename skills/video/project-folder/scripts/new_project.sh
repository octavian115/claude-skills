#!/bin/sh
# Usage: new_project.sh <slug> [raw files...]
# Makes $EDIT_ROOT/YYYY-MM-DD-<slug>/ with the standard subfolders and copies raw files in.
set -e
[ -n "$1" ] || { echo "usage: new_project.sh <slug> [raw files...]"; exit 1; }
slug=$(printf '%s' "$1" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-'); shift
root="${EDIT_ROOT:-$HOME/Movies/edits}"
ws="$root/$(date +%F)-$slug"
mkdir -p "$ws/raw" "$ws/audio" "$ws/cuts" "$ws/fx/scenes" "$ws/music" "$ws/renders"
for f in "$@"; do
  [ -e "$ws/raw/$(basename "$f")" ] || cp "$f" "$ws/raw/"
  chmod a-w "$ws/raw/$(basename "$f")"
done
[ -f "$ws/EDIT_LOG.md" ] || printf '# Edit log — %s\n\n| step | prompt | result |\n|---|---|---|\n' "$slug" > "$ws/EDIT_LOG.md"
echo "$ws"
ls -la "$ws/raw"
