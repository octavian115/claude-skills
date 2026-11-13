---
name: final-mix
description: Final loudness pass on the finished edit — two-pass EBU R128 normalisation to -14 LUFS integrated, -1 dBTP true peak, LRA 11 — so it plays at the right level on YouTube, Instagram and TikTok. Use when the user says "final mix", "-14 LUFS", "normalise loudness", "make it broadcast-safe", or before export.
---

# Step 9 — Final mix

Shown in the video ("STEP 9 — FINAL MIX", loudness meter reading **-14.0 LUFS**, "Ready for YouTube · Instagram · TikTok"):

```
> final mix: -14 LUFS, true peak -1 dB
● Bash(ffmpeg … loudnorm=I=-14:TP=-1:LRA=11)
    -14.0 LUFS · -1.0 dBTP · LRA 6.2
● Broadcast-safe for YouTube and Instagram.
```

## Command (this pack)
```bash
sh scripts/final_mix.sh renders/v7.mp4 renders/v8.mp4 [target=-14] [tp=-1]
```
Two-pass: pass 1 measures (`loudnorm … print_format=json`), pass 2 applies with the measured values and `linear=true` (one-pass loudnorm "pumps" the level). Video is stream-copied. It prints before → after and re-measures the output with `ebur128`.

## Targets
| Where | Integrated | True peak |
|---|---|---|
| YouTube / Instagram / TikTok | -14 LUFS | -1 dBTP |
| Podcasts / Spotify video | -16 LUFS | -1 dBTP |
| Broadcast (EBU R128) | -23 LUFS | -1 dBTP |

## Rules
- Run on the full mix (voice + music + any SFX), after step 7, before export.
- If the result reports LRA > 11 or the voice sounds squashed, the problem is upstream (music too loud or no compression on voice) — fix there, not here.
- Report: `<before> → <after> LUFS · <tp> dBTP · LRA <x>`.

## Template
```
final mix: -14 LUFS, true peak -1 dB
```
