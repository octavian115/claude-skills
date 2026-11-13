#!/bin/sh
# Usage: final_mix.sh <in> <out> [target_lufs=-14] [true_peak=-1]
# Two-pass loudnorm on the whole mix; video stream copied.
set -e
in="$1"; out="$2"; I="${3:--14}"; TP="${4:--1}"
[ -n "$out" ] || { echo "usage: final_mix.sh in out [lufs] [tp]"; exit 1; }
FF="${FFMPEG:-ffmpeg}"
measure() { "$FF" -hide_banner -nostats -i "$1" -vn -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/ I:/{i=$2} f&&/LRA:/{l=$2} f&&/Peak:/{p=$2} END{printf "%s LUFS · %s dBTP · LRA %s", i, p, l}'; }
echo "before: $(measure "$in")"
json=$("$FF" -hide_banner -nostats -i "$in" -vn -af "loudnorm=I=$I:TP=$TP:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { printf '%s' "$json" | sed -n "s/.*\"$1\" : \"\([^\"]*\)\".*/\1/p"; }
ln="loudnorm=I=$I:TP=$TP:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true"
case "$out" in *.mov|*.mkv) ac="-c:a pcm_s24le" ;; *) ac="-c:a aac -b:a 320k" ;; esac
"$FF" -hide_banner -loglevel error -y -i "$in" -map 0:v? -map 0:a -c:v copy -af "$ln" -ar 48000 $ac "$out"
echo "after:  $(measure "$out")"
