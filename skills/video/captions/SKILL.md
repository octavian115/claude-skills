---
name: captions
description: Add word-by-word burned-in captions in a fixed personal style (Montserrat SemiBold, translucent box, spoken word highlighted, big yellow emphasis words popping beside the speaker), timed to the final cut. Use when the user says "add captions", "subtitles in my style", "word-by-word captions", "make key words pop".
---

# Step 6 — Captions

Shown in the video ("STEP 6 — CAPTIONS"):

```
> add captions in my style: Montserrat SemiBold, translucent box,…   (prompt truncated on screen)
● Skill(captions)
● Bash(python scripts/transcribe.py .)
    2,406 words, each with a start and end
● Write(fx/captions.ass)
    155 lines · word-timed
● Captions in. Emphasis pops beside you.
```
Look: small lower-centre caption on a translucent dark box, 2–3 words at a time, the word being spoken in white and the rest grey (e.g. **my** video). Key words also appear large in yellow uppercase beside her (e.g. **EMPHASIS**), Montserrat ExtraBold with a soft shadow.

## Commands (this pack)
```bash
# fonts once: download Montserrat (OFL, Google Fonts) into ~/Movies/edits/_assets/fonts/

# 1. word timings ON THE CUT — reuse rough-cut verify output, or transcribe the render
python3 scripts/captions.py --words cuts/verify_v4_words.json --video renders/v4.mp4 \
        --out fx/captions.ass --emphasis "emphasis,captions,music" --max-words 3
#   or: --transcribe renders/v4.mp4   (uses mlx-whisper on Apple Silicon, else faster-whisper)

# 2. burn in
ffmpeg -i renders/v4.mp4 -vf "ass=fx/captions.ass:fontsdir=$HOME/Movies/edits/_assets/fonts" \
       -c:v libx264 -crf 18 -c:a copy renders/v5.mp4
```
Flags: `--vertical` (9:16 layout), `--font`, `--pop-font`, `--max-gap 0.6` (new line after a pause).

## Rules
- Caption **after** the cut is locked (pacing + graphics done) — timings come from the final timeline, not the raw.
- Spell-check proper nouns in the words file before generating (Whisper mishears names/brands).
- Emphasis: 1 pop per ~15–20 s max, on the word that carries the point. Never pop during a graphic.
- Keep captions out of the bottom ~8% (platform UI) and away from on-screen graphics.
- Proof the `.ass` lines for the first 30 s on a preview before burning the full-res version.

## Template
```
add captions in my style: Montserrat SemiBold, translucent box, word-by-word, emphasis pops beside me on "<word1>", "<word2>"
```
