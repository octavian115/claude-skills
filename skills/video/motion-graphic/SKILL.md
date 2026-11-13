---
name: motion-graphic
description: Build an animated motion graphic (stat counter, title card, sticker pop, explainer beat) as a time-driven HTML scene, render it frame-exact to video (with alpha if needed), and composite it onto the edit at the right word. Use when the user says "make a motion graphic for …", "animate this stat", "add a graphic/sticker when I say …", "explainer graphics".
---

# Step 5 — Motion graphics

Shown in the video ("STEP 5 — MOTION GRAPHICS"):

```
> make a motion graphic for the rough-cut stat: 17:48 to 3:54, ke…   (prompt truncated on screen)
● Skill(vox-explainer)
● Write(fx/scenes/s5_graphic.html)
✳ Animating…
```
Result: a white card on light grey — small-caps label **ROUGH CUT**, a huge number counting down **17:48 → 3:54**, a row of terracotta segment pills, and the line **"53 pieces kept · 99.1% of words present"**. Also seen: a corner timer card ("4:13" with dashed progress) and a cartoon sticker popping in beside her.

Key idea: Claude writes the graphic as **code (HTML/CSS/JS)**, so it's editable by prompt, on-brand, and rendered frame-exact. Nothing in the video used Replit — it was all Claude Code writing HTML scenes. (Replit, or any browser, would work for *previewing* the same HTML.)

## Commands (this pack)
```bash
# one-time
npm i playwright && npx playwright install chromium

# 1. Claude copies & fills the template (or writes a new scene)
cp scripts/stat_template.html fx/scenes/s5_graphic.html     # edit CONFIG: label, from, to, pills, sub

# 2. Render — full-frame cutaway (mp4) or overlay with transparency (mov, ProRes 4444)
node scripts/render_html.mjs fx/scenes/s5_graphic.html fx/s5_graphic.mp4 --dur 4 --fps 29.97 --w 3840 --h 2160
node scripts/render_html.mjs fx/scenes/s5_graphic.html fx/s5_graphic.mov --dur 4 --fps 29.97 --w 3840 --h 2160 --alpha

# 3a. Insert as a full-screen cutaway at 95.2 s (voice keeps playing underneath)
ffmpeg -i renders/v3.mp4 -i fx/s5_graphic.mp4 -filter_complex \
 "[1:v]setpts=PTS-STARTPTS+95.2/TB[g];[0:v][g]overlay=enable='between(t,95.2,99.2)':eof_action=pass[v]" \
 -map "[v]" -map 0:a -c:a copy renders/v4.mp4

# 3b. Overlay an alpha graphic / sticker in a corner (scaled to 30% width, top-right)
ffmpeg -i renders/v3.mp4 -i fx/sticker.mov -filter_complex \
 "[1:v]scale=iw*0.3:-1,setpts=PTS-STARTPTS+100/TB[g];[0:v][g]overlay=W-w-80:80:enable='between(t,100,103)':eof_action=pass[v]" \
 -map "[v]" -map 0:a -c:a copy renders/v4.mp4
```

## How a scene must be written
- Author at **1920×1080 CSS px** (the renderer scales to 4K). For vertical, 1080×1920 and pass `--w 2160 --h 3840`.
- Drive motion from **time**, never wall clock: define `window.renderAt(t)` (seconds) and/or use CSS animations (the renderer pauses and seeks them each frame). No `setTimeout`/`requestAnimationFrame` loops.
- Time the beat to the **word**: get the timestamp from `cuts/verify_vN_words.json` and start the overlay there.
- Nothing freezes: keep a slow push/scale running the whole time.
- One idea per graphic, huge type, max one highlight.

## Template prompts
```
make a motion graphic for <stat>: <from> to <to>, <label>, keep it clean and on-brand
pop a <sticker idea> sticker top-right when I say "<word>"
corner timer showing <value> while I talk about <topic>
```

For a full Vox-style explainer sequence, the author's `vox-explainer` skill (simcraft) builds multi-beat scenes timed word-by-word.
