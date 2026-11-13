---
name: clean-audio-pass
description: Clean voice audio for social video — cut rumble, tame boxiness, add clarity, soften harsh S's, compress, and normalise to -14 LUFS — measuring before and after. Use when the user says "clean up the audio", "social loudness", "fix the sound", "remove hum/noise", or right after a rough cut transcript exists.
---

# Step 3 — Clean audio

Shown in the video (before/after waveform panel, `DJI_0048.wav`):

```
> clean up the audio, social loudness
● Skill(clean-audio)
● Bash(ffmpeg -i audio/DJI_0048_D.wav -af ebur128)
    -21.9 LUFS · 50 Hz hum · rumble under 80 Hz
● Done. Saved audio/DJI_0048_D.clean.wav
    Rumble cut below 80 Hz
    Boxiness -2 dB at 250 Hz
    Clarity +1.5 dB at 4.5 kHz
    Harsh S's softened, 3:1 compression
    Loudness -21.9 → -14 LUFS, peaks -1 dBTP
```
On-screen caption: "Hum, rumble and harsh S's out → -14 LUFS for social".

## Option A — author's skill (best: has a Whisper clarity check)
```bash
ln -s ~/simcraft/skills/video/clean-audio ~/.claude/skills/clean-audio
PY=~/simcraft/skills/video/rough-cut/.venv/bin/python
$PY ~/simcraft/skills/video/clean-audio/scripts/clean_audio.py raw/<CLIP> --sample   # 10 s before/after to listen to
$PY ~/simcraft/skills/video/clean-audio/scripts/clean_audio.py .                    # cleans every raw clip → audio/<clip>.clean.wav
```
rough-cut's `render.py` picks up `audio/<clip>.clean.wav` automatically.

## Option B — standalone (this pack)
```bash
sh scripts/clean_voice.sh raw/<CLIP> audio/<clip>.clean.wav [hum_hz=50|60|0] [target=-14]
```
1. Measures: `ffmpeg -i in -af ebur128 -f null -` (integrated loudness, true peak).
2. Chain: `highpass=f=80` → hum notches at 50/100/150/200 Hz → `afftdn` light denoise → `equalizer=f=250:g=-2` → `equalizer=f=4500:g=1.5` → `deesser` → `acompressor` 3:1.
3. Two-pass `loudnorm=I=-14:TP=-1:LRA=11` (measure, then apply with measured values — one-pass pumps).
4. Re-measures and prints before → after.

## Rules
- Clean the **raw** clips before the final cut render — the noise profile comes from pauses that the cut removes.
- Never trade clarity for quiet; if words get smeared, drop denoise strength.
- Leave a little room tone; don't gate to digital silence.
- -14 LUFS for YouTube/Instagram/TikTok, -16 for podcasts.

## Template
```
clean up the audio, social loudness
[variants] … podcast loudness (-16) | … no EQ, I like my voice as is | … my hum is 60 Hz
```
