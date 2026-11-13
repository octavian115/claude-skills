---
name: project-folder
description: Create a dated, self-contained project folder for a new video and copy (never move) the raw footage into it. Use when the user starts a new edit, says "set up a project", "new video folder", or hands over raw clips with no workspace yet.
---

# Step 1 — Project folder

From the video: "first things first, I like to make a specific folder for every single video that I'm working on." Her folders live in `~/Movies/edits/` and are named `YYYY-MM-DD-<slug>` (e.g. `2026-11-11-edit-with-claude`), so they sort by date in Finder.

## Command

```bash
sh scripts/new_project.sh "<slug>" <raw files...>
# e.g.
sh scripts/new_project.sh edit-with-claude ~/Downloads/DJI_0048.MP4
```

Creates:

```
~/Movies/edits/2026-11-14-edit-with-claude/
  raw/       originals (copied, read-only)
  audio/     transcripts, cleaned wavs
  cuts/      edl.json, cut sheets, verify reports
  fx/        captions.ass, scenes/*.html, rendered overlays, LUTs
  music/     licensed tracks
  renders/   v1_854.mp4, v2_854.mp4 … final
  EDIT_LOG.md
```

Then `cd` into it and start Claude Code there, so every later prompt can use short relative paths (`raw/DJI_0048.MP4`).

## Rules
- Copy, never move. Make `raw/` read-only after copying.
- One video per folder. Shared assets (fonts, LUTs, logo) go in `~/Movies/edits/_assets/`, not inside a project.
- Use `EDIT_ROOT=/path` to override the default root.
