#!/usr/bin/env python3
"""Add punch-in zooms to a video at given time ranges.

Usage:
  punch_in.py in.mp4 out.mp4 --at 95.0-98.6,141.2-143.0 [--zoom 1.08] [--center 0.5,0.45] [--ease 0]

--zoom    scale factor while punched in (1.08 = 8%)
--center  crop centre as fractions of width,height (bias toward the face)
--ease    seconds to ease into the zoom (0 = hard jump-cut punch, the default)
Audio is copied untouched, so sync can't drift.
"""
import argparse, json, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--at", required=True)
ap.add_argument("--zoom", type=float, default=1.08)
ap.add_argument("--center", default="0.5,0.45")
ap.add_argument("--ease", type=float, default=0.0)
ap.add_argument("--crf", default="18")
a = ap.parse_args()

ranges = []
for r in a.at.split(","):
    s, e = (float(x) for x in r.split("-"))
    if e <= s: sys.exit(f"bad range {r}")
    ranges.append((s, e))
cx, cy = (float(v) for v in a.center.split(","))

probe = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
     "-of", "json", a.inp], capture_output=True, text=True, check=True).stdout)
W, H = probe["streams"][0]["width"], probe["streams"][0]["height"]

# z(t): zoom factor as an expression of time; 1 outside ranges
def zexpr():
    parts = []
    for s, e in ranges:
        if a.ease > 0:
            ramp = f"min(1,(t-{s})/{a.ease})"
            parts.append(f"between(t,{s},{e})*({a.zoom}-1)*{ramp}")
        else:
            parts.append(f"between(t,{s},{e})*({a.zoom}-1)")
    return "1+" + "+".join(parts)

z = zexpr()
# upscale each frame by z(t) (scale re-evaluates per frame), then crop back to the source size around the centre bias
vf = (f"scale=w='trunc(iw*({z})/2)*2':h='trunc(ih*({z})/2)*2':eval=frame:flags=lanczos,"
      f"crop={W}:{H}:x='max(0,min(in_w-{W},{cx}*in_w-{W}/2))':y='max(0,min(in_h-{H},{cy}*in_h-{H}/2))',setsar=1")
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.inp,
       "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "0:a?",
       "-c:v", "libx264", "-crf", a.crf, "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", a.out]
subprocess.run(cmd, check=True)
print(f"wrote {a.out}  punch-ins: " + ", ".join(f"{s:.2f}-{e:.2f}s" for s, e in ranges) + f" @ {round((a.zoom-1)*100)}%")
