---
name: color-grade
description: Colour-correct and grade talking-head footage with a measured 3D LUT — fix white balance, blacks and exposure, then match the look of a reference/inspo still while protecting skin tones. Use when the user says "fix the colour", "fix the basics: white balance, blacks, exposure", "match this look", "warm film look", "keep my skin natural", or pastes an inspo image.
---

# Step 8 — Colour

Shown in the video (two prompts, with an Adjust panel and a Resolve-style colour page on screen):

```
> fix the basics: white balance, blacks, exposure
● Bash(python scripts/grade.py --wb --blacks --exposure)
    wb neutral · blacks -0.03 · exposure +0.20
✳ Correcting…
        (panel: White Balance 5744 K · Blacks -0.20 · Exposure +0.20)

> [Image #1] match this warm film look, keep my skin natural
● Read(inspo.jpg)
    warm highlights, lifted blacks, soft contrast
● Bash(python scripts/grade.py --match inspo.jpg --protect-skin)
    3 nodes · skin tones held
● Matched: Temp +420 K, blacks lifted, skin held.
```
Caption: "Drop in your inspo, Claude matches the grade".

## Commands (this pack — `pip install numpy pillow`)
```bash
# save the pasted inspo still as fx/inspo.jpg first
# 1. basics only, with before/after stills to check
python3 scripts/grade.py renders/v6.mp4 --wb --blacks --exposure --stills
# 2. basics + look match, skin protected
python3 scripts/grade.py renders/v6.mp4 --wb --blacks --exposure --match fx/inspo.jpg --protect-skin --strength 0.7 --stills
# 3. apply (or pass --apply renders/v7.mp4 above)
ffmpeg -i renders/v6.mp4 -vf "lut3d=file='fx/grade.cube':interp=tetrahedral" -c:v libx264 -crf 18 -c:a copy renders/v7.mp4
```
The `.cube` file also loads in DaVinci Resolve, Final Cut Pro and Premiere if you'd rather finish there.

How it works: samples 8 frames → grey-world white balance gains → exposure to a target median → black point to a target (small moves only, ±0.06) → Reinhard mean/std transfer in CIELAB toward the inspo, with contrast and colour-cast shifts clamped and skin-tone pixels (YCbCr skin range) kept at ~15% of the change.

## Rules
- Always **look** at `fx/grade_before.jpg` vs `fx/grade_after.jpg` before applying; describe the change to the user (warmer/cooler, lifted/crushed blacks, ± stops).
- Correct first, then grade. Never match a look on uncorrected footage.
- Skin must stay natural: if the face shifts orange/green, lower `--strength` (0.5) or tighten protection.
- Mixed lighting (window + lamp) — grade per shot, not one LUT for the whole video.
- Do it after the cut is locked, so you only grade what's kept.

## Template
```
fix the basics: white balance, blacks, exposure
[paste inspo] match this <warm film | clean bright | moody> look, keep my skin natural
```
