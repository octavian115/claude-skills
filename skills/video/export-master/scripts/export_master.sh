#!/bin/sh
# Usage: export_master.sh <edit> <source clip> <out.mov>
# Exports at the source's resolution and frame rate, HEVC 10-bit + AAC 48 kHz.
set -e
in="$1"; src="$2"; out="$3"
[ -n "$out" ] || { echo "usage: export_master.sh edit source out.mov"; exit 1; }
FF="${FFMPEG:-ffmpeg}"
info=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$src" | head -1)
W=$(echo "$info" | cut -d, -f1); H=$(echo "$info" | cut -d, -f2); R=$(echo "$info" | cut -d, -f3)
[ -n "$R" ] || { echo "could not read source video info from $src"; exit 1; }
echo "source: ${W}x${H} @ $R fps"
if "$FF" -hide_banner -encoders 2>/dev/null | grep -q hevc_videotoolbox; then
  venc="-c:v hevc_videotoolbox -profile:v main10 -pix_fmt p010le -q:v 65"
else
  venc="-c:v libx265 -preset slow -crf 16 -pix_fmt yuv420p10le"
fi
"$FF" -hide_banner -loglevel error -stats -y -i "$in" \
  -vf "scale=${W}:${H}:flags=lanczos,fps=${R},setsar=1" $venc -tag:v hvc1 \
  -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$out"
d=$(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$out")
echo "exported $out  (duration,size bytes: $d)"
