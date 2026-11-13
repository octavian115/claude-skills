---
name: edit-with-claude
description: Full 10-step talking-head edit driven from Claude Code — project folder, rough cut, clean audio, pacing, motion graphics, captions, music, colour, final mix, export. Use when the user says "edit this video", "edit my video with claude", "run the full edit", or drops raw talking footage and wants a finished video.
---

# Edit with Claude — the full pass

This is the workflow from simran sachdeva's "how I edit my videos with Claude (beginner edition)" (X, Nov 2026). Every step is one plain-English prompt typed into Claude Code, run from inside the project folder. Each step has its own skill; this one runs them in order and keeps the user in the loop between steps.

## Order (never reorder 2 and 3 after 4)

| # | Step | Skill | Prompt used in the video |
|---|------|-------|--------------------------|
| 1 | Project folder | `project-folder` | *(Finder: one dated folder per video)* |
| 2 | Rough cut | `rough-cut-pass` | `rough cut raw/DJI_0048.MP4, keep my last good take of every line` |
| 3 | Clean audio | `clean-audio-pass` | `clean up the audio, social loudness` |
| 4 | Pacing | `pacing-punch-in` | `tighten the pacing: cut pauses over 0.3 s, punch in on "zoom-in" …` |
| 5 | Motion graphics | `motion-graphic` (+ `brand-kit-graphics` for sponsors) | `make a motion graphic for the rough-cut stat: 17:48 to 3:54, …` |
| 6 | Captions | `captions` | `add captions in my style: Montserrat SemiBold, translucent box, …` |
| 7 | Music | `music-bed` | `music: calm lo-fi under the voice, it should never overpower me` |
| 8 | Colour | `color-grade` | `fix the basics: white balance, blacks, exposure` then `[Image #1] match this warm film look, keep my skin natural` |
| 9 | Final mix | `final-mix` | `final mix: -14 LUFS, true peak -1 dB` |
| 10 | Export | `export-master` | `export at source settings` |

Note: step 3 cleans the **raw clips** (noise is learned from pauses), so run it right after the transcript exists and before the final render of step 2/4.

## How to run it

1. Confirm the workspace (`~/Movies/edits/YYYY-MM-DD-<slug>/`). If it doesn't exist, run `project-folder`.
2. Run each step's skill. After steps 2, 4, 5, 6 and 8, show the user a **preview** (480p) and wait for notes before moving on. Bump the version number (`v1`, `v2`…) each round; never overwrite an earlier render.
3. Keep a running `EDIT_LOG.md` in the workspace: step, prompt, command, result (e.g. `17:48 → 3:54, 53 pieces, verified 99.1% of words`).
4. Only render full resolution at step 10.

## Template — paste into Claude Code for a new video

```
cd ~/Movies/edits/<YYYY-MM-DD-slug>
claude
> rough cut raw/<CLIP>.MP4, keep my last good take of every line
> clean up the audio, social loudness
> tighten the pacing: cut pauses over 0.3 s, punch in on "<phrase 1>", "<phrase 2>"
> make a motion graphic for <stat or idea>: <numbers>, keep it on brand
> add captions in my style: Montserrat SemiBold, translucent box, word-by-word, emphasis pops beside me
> music: <mood> under the voice, it should never overpower me   (put the track in music/)
> fix the basics: white balance, blacks, exposure
> [paste inspo still] match this look, keep my skin natural
> final mix: -14 LUFS, true peak -1 dB
> export at source settings
```

## Rules (from the video)
- One folder per video, raw files copied in and never modified.
- Edit the words, not the waveform: cut from the transcript, then verify by re-listening.
- Music sits under the voice; voice always wins.
- -14 LUFS / -1 dBTP is the target for YouTube, Instagram and TikTok.
- Export matches the source (e.g. 4K, 29.97 fps, HEVC 10-bit).
