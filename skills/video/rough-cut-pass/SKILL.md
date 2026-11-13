---
name: rough-cut-pass
description: Turn raw talking-head footage into a tight first cut by transcribing with word timings and cutting dead air, ums, repeats, false starts and retakes (keeping the last good take), then verifying by re-listening. Use when the user says "rough cut", "first cut", "keep my last good take", "remove the ums", "cut my retakes".
---

# Step 2 — Rough cut

Result shown in the video: **17:48 of rambling → 3:54 first cut, 53 pieces, verified 99.1% of words.** The overlay showed the transcript with struck-through retakes ("First things first, I like to create a folder…" ×3 struck, last take kept) and fillers struck out ("The ums, I have a bad habit of saying um a lot. ~~The filler words.~~").

This step uses the author's open-source `rough-cut` skill from **simcraft** (github.com/dotslashsimran/simcraft, MIT). Install once:

```bash
git clone https://github.com/dotslashsimran/simcraft ~/simcraft
ln -s ~/simcraft/skills/video/rough-cut ~/.claude/skills/rough-cut
sh ~/simcraft/skills/video/rough-cut/setup.sh       # Whisper venv (mlx-whisper on Apple Silicon)
```
Requires ffmpeg on PATH (`brew install ffmpeg`). Review the repo before running its setup script.

## Prompt used in the video
```
rough cut raw/DJI_0048.MP4, keep my last good take of every line
```

## Commands Claude ran
```bash
PY=~/simcraft/skills/video/rough-cut/.venv/bin/python
S=~/simcraft/skills/video/rough-cut/scripts
$PY $S/transcribe.py .  --lang en          # → audio/words.json, audio/transcript.txt  (2,406 words · 193 lines)
$PY $S/find_cuts.py  .  --gap 0.35         # → cuts/edl.json, cuts/cut_sheet.md
# judgement pass: read cut_sheet.md + transcript.txt, fix edl.json by hand
$PY $S/render.py     .  --w 854 --v 1      # → renders/v1_854.mp4 (480p preview)
$PY $S/verify.py     .  --v 1 --lang en    # → cuts/verify_v1.md (missing / leaked words, cuts inside sound)
```

## Judgement pass (never skip)
- Keep the take with the best energy, not automatically the last.
- Keep deliberate pauses before punchlines and fillers that are part of a joke.
- Never auto-cut "like / you know / I mean" — only the pure stalling ones.
- Cut whole sentences that repeat a point in different words.

## Report back to the user
`<before> → <after> · <N> pieces · verified <X>% of words · <judgement calls>`

## Template for a future video
```
rough cut raw/<CLIP>, keep my last good take of every line
[optional] cold open with the line "<strongest line>"
[optional] only the good bits, <N> minutes tops
```
