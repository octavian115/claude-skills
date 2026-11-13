#!/bin/sh
# Usage: music_bed.sh <video> <music> <out> [bed_lufs=-18] [duck_db=8]
# Loops/trims music to the video, normalises it, ducks it under the voice with a sidechain compressor, mixes.
set -e
v="$1"; m="$2"; out="$3"; bed="${4:--18}"; duck="${5:-8}"
[ -n "$out" ] || { echo "usage: music_bed.sh video music out [bed_lufs] [duck_db]"; exit 1; }
FF="${FFMPEG:-ffmpeg}"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
fo=$(awk "BEGIN{d=$dur-3; print (d>0?d:0)}")
tmp="${TMPDIR:-/tmp}/musicbed.$$.wav"

# 1) loop, trim, fade, normalise the bed (two-pass loudnorm)
pre="atrim=0:$dur,asetpts=N/SR/TB,afade=t=in:d=1.5,afade=t=out:st=$fo:d=3"
json=$("$FF" -hide_banner -nostats -stream_loop -1 -i "$m" -af "$pre,loudnorm=I=$bed:TP=-3:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { printf '%s' "$json" | sed -n "s/.*\"$1\" : \"\([^\"]*\)\".*/\1/p"; }
"$FF" -hide_banner -loglevel error -y -stream_loop -1 -i "$m" \
  -af "$pre,loudnorm=I=$bed:TP=-3:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" \
  -ar 48000 -ac 2 "$tmp"
echo "bed normalised to $bed LUFS"

# 2) duck under the voice and mix. ratio chosen so speech pushes the bed down ~duck_db.
ratio=$(awk "BEGIN{r=1+$duck/4; print (r>20?20:r)}")
case "$out" in *.mov|*.mkv) acodec="-c:a pcm_s24le" ;; *) acodec="-c:a aac -b:a 320k" ;; esac
"$FF" -hide_banner -loglevel error -y -i "$v" -i "$tmp" -filter_complex \
  "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[voice][key];\
   [1:a][key]sidechaincompress=threshold=0.02:ratio=$ratio:attack=20:release=400:makeup=1[bed];\
   [voice][bed]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy $acodec "$out"
rm -f "$tmp"
echo "ducks ~${duck} dB whenever you speak -> $out"
