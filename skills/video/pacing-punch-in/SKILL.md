---
name: pacing-punch-in
description: Tighten the pacing of a rough cut — cut every pause over a threshold (default 0.3 s) with edges snapped to the voice — and add subtle punch-in zooms on chosen phrases. Use when the user says "tighten the pacing", "make it snappier", "cut pauses over X s", "punch in on …", "add a zoom-in on …".
---

# Step 4 — Pacing + punch-ins

Shown in the video (timeline at the bottom: `edit-with-claude · Primary storyline · 4K · 29.97 fps`, duration counter dropping 4:29 → 4:08 → 3:54):

```
> tighten the pacing: cut pauses over 0.3 s, punch in on "zoom-in…   (prompt truncated on screen)
● Skill(rough-cut)
● Bash(python scripts/find_cuts.py . --gap 0.3)
    26 pauses cut · every edge snapped to the voice
● Edit(cuts/edl.json)
    punch-in 8% at 1:35
● Timeline tightened: 3:54 → 3:23.
```

## Commands

1. **Re-cut pauses at a tighter gap** (rough-cut skill, keeps your judgement edits if you re-apply them):
   ```bash
   $PY ~/simcraft/skills/video/rough-cut/scripts/find_cuts.py . --gap 0.3
   $PY ~/simcraft/skills/video/rough-cut/scripts/render.py . --w 854 --v 2
   $PY ~/simcraft/skills/video/rough-cut/scripts/verify.py . --v 2
   ```
   If you already hand-edited `cuts/edl.json`, back it up first (`cp cuts/edl.json cuts/edl_v1.json`) and re-apply those edits.

2. **Find the punch-in times** — read `cuts/verify_v2_words.json` (words as heard in the cut) or the transcript, locate each phrase the user named, and note `start-end` in seconds on the **cut** timeline. Hold each punch for the whole phrase (usually 1.5–4 s).

3. **Apply punch-ins** (this pack):
   ```bash
   python3 scripts/punch_in.py renders/v2_854.mp4 renders/v3_854.mp4 --at 95.0-98.6,141.2-143.0 --zoom 1.08
   ```
   Hard-cut zoom (jump-cut style) by default; `--ease 0.25` makes a quick ease-in instead. `--center 0.5,0.4` biases the crop toward the face (x,y as fractions).

## Rules
- 0.3 s is snappy talking-head pace; 0.35 s is the safer default. Go no lower than 0.25 s.
- Punch-ins: 6–10% zoom, on emphasis lines only. Constant alternating zooms read as amateur — max one every ~20 s.
- Never punch in during a cutaway or graphic.
- Report: `<before> → <after>, <N> pauses cut, punch-ins at <times>`.

## Template
```
tighten the pacing: cut pauses over 0.3 s, punch in on "<phrase 1>" and "<phrase 2>"
```
