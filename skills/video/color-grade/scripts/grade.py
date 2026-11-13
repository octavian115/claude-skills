#!/usr/bin/env python3
"""Colour grade a talking-head video with a generated 3D LUT.

Two passes, as in the video:
  1. basics  : white balance (grey-world on the footage), blacks, exposure — measured, not guessed
  2. match   : transfer the look of an inspiration still (Reinhard mean/std transfer in CIELAB),
               with skin tones protected so the face stays natural

Usage:
  grade.py <video> --wb --blacks --exposure                      → fx/grade.cube  (basics only)
  grade.py <video> --wb --blacks --exposure --match inspo.jpg --protect-skin [--strength 0.7]
  add --apply out.mp4 to render (otherwise prints the ffmpeg command)
  add --stills to write fx/grade_before.jpg / fx/grade_after.jpg for a side-by-side check

Needs: numpy, Pillow, ffmpeg.
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--wb", action="store_true"); ap.add_argument("--blacks", action="store_true")
ap.add_argument("--exposure", action="store_true")
ap.add_argument("--match"); ap.add_argument("--protect-skin", action="store_true")
ap.add_argument("--strength", type=float, default=0.75)
ap.add_argument("--target-mid", type=float, default=0.45, help="target median luma (0-1) for exposure")
ap.add_argument("--target-black", type=float, default=0.03, help="target 0.5th-percentile luma")
ap.add_argument("--lut", default="fx/grade.cube"); ap.add_argument("--size", type=int, default=33)
ap.add_argument("--apply"); ap.add_argument("--stills", action="store_true")
a = ap.parse_args()

def sample_frames(video, n=8):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True, check=True).stdout.strip())
    out = []
    with tempfile.TemporaryDirectory() as d:
        for i in range(n):
            t = dur * (i + 0.5) / n; f = Path(d) / f"{i}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                            "-vf", "scale=480:-2", str(f)], check=True)
            out.append(np.asarray(Image.open(f).convert("RGB"), dtype=np.float64) / 255)
    return out

# --- colour maths -------------------------------------------------------------------------------
def to_lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def to_srgb(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)
M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
WP = np.array([0.95047, 1.0, 1.08883])
def rgb2lab(rgb):
    xyz = to_lin(rgb) @ M.T / WP
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
def lab2rgb(lab):
    fy = (lab[..., 0] + 16) / 116; fx = fy + lab[..., 1] / 500; fz = fy - lab[..., 2] / 200
    f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f ** 3 > 216 / 24389, f ** 3, (116 * f - 16) / (24389 / 27)) * WP
    return to_srgb(xyz @ np.linalg.inv(M).T)
luma = lambda c: c @ np.array([0.2126, 0.7152, 0.0722])

def skin_weight(rgb):
    """1.0 on skin tones, 0 elsewhere (YCbCr box, softened)."""
    y = luma(rgb); cb = (rgb[..., 2] - y) / 1.8556; cr = (rgb[..., 0] - y) / 1.5748
    w_cb = np.clip(1 - np.abs(cb + 0.07) / 0.09, 0, 1); w_cr = np.clip(1 - np.abs(cr - 0.09) / 0.08, 0, 1)
    return np.clip(w_cb * w_cr * 2, 0, 1) * (y > 0.12)

# --- 1. measure basics -------------------------------------------------------------------------
frames = sample_frames(a.video)
px = np.concatenate([f.reshape(-1, 3) for f in frames])
report = []
gains = np.ones(3); lift = 0.0; stops = 0.0
if a.wb:
    lin = to_lin(px); mask = (luma(px) > 0.15) & (luma(px) < 0.85)
    mean = lin[mask].mean(0); gains = mean.mean() / mean; gains /= gains[1]
    # express as an approximate Kelvin shift for the report (blue/red balance)
    ratio = gains[2] / gains[0]
    report.append(f"WB gains R{gains[0]:.3f} G1.000 B{gains[2]:.3f} ({'warmer' if ratio < 1 else 'cooler'} by ~{abs(np.log2(ratio)) * 1500:.0f} K)")
corrected = lambda c: to_srgb(to_lin(c) * gains * 2 ** stops)
if a.exposure:
    med = np.median(luma(corrected(px)))
    stops = float(np.clip(np.log2(max(a.target_mid, 1e-3) ** 2.2 / max(med, 1e-3) ** 2.2), -1.5, 1.5))
    report.append(f"exposure {stops:+.2f} stops (median luma {med:.2f} → {a.target_mid:.2f})")
if a.blacks:
    b = np.percentile(luma(corrected(px)), 0.5)
    lift = float(np.clip(a.target_black - b, -0.06, 0.06))   # small moves only; big black shifts look wrong
    report.append(f"blacks {lift:+.3f} (0.5% point {b:.3f} → {a.target_black:.3f})")

def basics(c):
    c = corrected(c)
    return np.clip((c + lift * (1 - c)) if lift > 0 else (c + lift) / (1 + lift), 0, 1)  # lift toe or crush

# --- 2. match an inspiration still ----------------------------------------------------------
src_stats = ref_stats = None
if a.match:
    ref = np.asarray(Image.open(a.match).convert("RGB").resize((480, 270)), dtype=np.float64).reshape(-1, 3) / 255
    lab_s = rgb2lab(basics(px)); lab_r = rgb2lab(ref)
    src_stats = (lab_s.mean(0), lab_s.std(0) + 1e-6); ref_stats = (lab_r.mean(0), lab_r.std(0) + 1e-6)
    d = ref_stats[0] - src_stats[0]
    report.append(f"match {Path(a.match).name}: L{d[0]:+.1f} a{d[1]:+.1f} b{d[2]:+.1f}  (b>0 = warmer)  strength {a.strength}"
                  + (" · skin protected" if a.protect_skin else ""))

def grade(c):
    c = basics(c)
    if src_stats is None: return c
    lab = rgb2lab(c)
    sd = np.clip(ref_stats[1] / src_stats[1], 0.6, 1.6)            # limit contrast/saturation swings
    mu = src_stats[0] + np.clip(ref_stats[0] - src_stats[0], [-12, -10, -15], [12, 10, 15])  # limit cast
    t = (lab - src_stats[0]) * sd + mu
    t[..., 0] = lab[..., 0] + (t[..., 0] - lab[..., 0]) * 0.6        # keep contrast changes gentle
    k = np.full(c.shape[:-1], a.strength)
    if a.protect_skin: k = k * (1 - 0.85 * skin_weight(c))
    out = lab + (t - lab) * k[..., None]
    return np.clip(lab2rgb(out), 0, 1)

# --- 3. write .cube ------------------------------------------------------------------------------
N = a.size; g = np.linspace(0, 1, N)
b_, g_, r_ = np.meshgrid(g, g, g, indexing="ij")          # .cube order: red fastest
grid = np.stack([r_, g_, b_], -1).reshape(-1, 3)
out = grade(grid)
Path(a.lut).parent.mkdir(parents=True, exist_ok=True)
with open(a.lut, "w") as f:
    f.write(f'TITLE "grade"\nLUT_3D_SIZE {N}\n')
    f.writelines(f"{x:.6f} {y:.6f} {z:.6f}\n" for x, y, z in out)
print("\n".join(report) or "no changes requested"); print(f"wrote {a.lut}")

vf = f"lut3d=file='{a.lut}':interp=tetrahedral"
if a.stills:
    mid = frames[len(frames) // 2]
    Image.fromarray((mid * 255).astype(np.uint8)).save(Path(a.lut).with_name("grade_before.jpg"))
    Image.fromarray((grade(mid) * 255).astype(np.uint8)).save(Path(a.lut).with_name("grade_after.jpg"))
    print("wrote grade_before.jpg / grade_after.jpg")
if a.apply:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", vf, "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", a.apply], check=True)
    print(f"wrote {a.apply}")
else:
    print(f'apply: ffmpeg -i {a.video} -vf "{vf}" -c:a copy <out>')
