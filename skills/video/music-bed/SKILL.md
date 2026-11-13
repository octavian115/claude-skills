---
name: music-bed
description: Lay a licensed music track under the voice so it never overpowers it — normalise the bed, sidechain-duck it whenever the speaker talks, loop/trim to length, and fade in/out. Use when the user says "add music", "lo-fi under my voice", "duck the music when I talk", "it should never overpower me".
---

# Step 7 — Music

Shown in the video ("STEP 7 — MUSIC", caption: "Pick the mood, keep it under your voice"). She browsed a royalty-free music library filtered by mood (Calm / Cinematic / Upbeat / Lo-fi), picked a calm track, then:

```
> music: calm lo-fi under the voice, it should never overpower me
● Bash(ffmpeg … loudnorm=I=-18)
    bed normalised to -18 LUFS
● Bash(ffmpeg … sidechaincompress)
    ducks 8 dB whenever you speak
● Bed sits under the voice. Switches moods on your cue.

> put this under my voice, duck it to -20 LUFS when I talk
● Skill(clean-audio)
    Music ducked under voice · -20 LUFS bed
```

## Commands (this pack)
```bash
# put the licensed track in music/ first (YouTube Audio Library, Pixabay Music, Epidemic, Artlist…)
sh scripts/music_bed.sh renders/v5.mp4 music/<track>.mp3 renders/v6.mp4 [bed_lufs=-18] [duck_db=8]
```
What it does:
1. Loops/trims the track to the video length; 1.5 s fade in, 3 s fade out.
2. Two-pass `loudnorm` on the bed to `-18 LUFS` (or `-20` for quieter).
3. `sidechaincompress` keyed by the voice — the bed drops ~8 dB while you speak and recovers in the gaps (attack 20 ms, release 400 ms).
4. `amix` voice + ducked bed (voice untouched), video stream copied.

Mood changes ("switches moods on your cue"): render separate beds per section and crossfade at the cue word with `acrossfade=d=1.5`, or run the script per section and join.

## Rules
- Only use tracks you have a licence for; keep the licence file/URL in `music/LICENSE.txt`.
- The voice always wins: if any word gets hard to hear on phone speakers, lower `bed_lufs` by 2 and re-render.
- No music under a punchline or a deliberate silence beat — cut the bed there.
- Do this **before** step 9; the final mix normalises the whole thing.

## Template
```
music: <calm lo-fi | upbeat | cinematic> under the voice, it should never overpower me
switch to <mood> when I say "<cue>"
```
