---
name: export-master
description: Export the finished edit at the source's own settings (resolution, frame rate, HEVC 10-bit, AAC 48 kHz) into renders/, plus optional platform versions (9:16, H.264 for upload). Use when the user says "export", "export at source settings", "render the final", "make the upload file".
---

# Step 10 — Export

Shown in the video ("STEP 10 — EXPORT"; export sheet: `edit-with-claude.mov` → `~/Movies/edits/2026-11-11-edit-with-claude/renders`, Video and Audio, **HEVC 10-bit, 3840×2160, 29.97 fps (same as source), AAC 48 kHz**, "Match source" ticked, ~2.4 GB):

```
> export at source settings
● Bash(ffmpeg … 3840x2160 hevc 29.97)
    3:23 · 2.4 GB
● Exported to renders/.
```
Caption: "Export at the source settings: 4K, 29.97 fps".

## Command (this pack)
```bash
sh scripts/export_master.sh renders/v8.mp4 raw/DJI_0048.MP4 renders/<slug>.mov
```
- Reads width, height and frame rate from the **source** clip (`ffprobe`), so nothing gets resampled.
- macOS: `hevc_videotoolbox` 10-bit (fast, hardware); elsewhere `libx265` `yuv420p10le` CRF 16.
- Tags `hvc1` so QuickTime/Finder/iOS play it; AAC 320k 48 kHz; `+faststart`.
- If the edit was rendered at preview size, **re-render the cut at source width first** (rough-cut `render.py --w <source width>`), then re-apply graphics/captions/grade at full res — never upscale a 480p preview.

Optional upload copies:
```bash
# H.264 for platforms that recompress HEVC badly
ffmpeg -i renders/<slug>.mov -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart renders/<slug>_h264.mp4
# 9:16 vertical (centre crop) for Reels/Shorts/TikTok
ffmpeg -i renders/<slug>.mov -vf "crop=ih*9/16:ih,scale=1080:1920" -c:v libx264 -crf 18 -c:a copy renders/<slug>_9x16.mp4
```

## Checks before calling it done
- Duration matches the timeline; audio and video same length (`ffprobe`).
- Scrub 3 points (start/middle/end): captions present, graphics present, grade applied, no black frames.
- Re-measure loudness: -14 LUFS ±0.5.
- Log the final line in `EDIT_LOG.md`: `<duration> · <size> · <codec> · <path>`.

## Template
```
export at source settings
[optional] also make a 9:16 version and an H.264 upload copy
```
