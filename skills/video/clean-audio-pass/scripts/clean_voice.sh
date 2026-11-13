#!/bin/sh
# Usage: clean_voice.sh <input video/audio> <output.wav> [hum_hz=50] [target_lufs=-14]
# Voice cleanup chain matching the video: rumble <80 Hz, hum notches, light denoise,
# -2 dB @250 Hz, +1.5 dB @4.5 kHz, de-ess, 3:1 compression, two-pass loudnorm to target / -1 dBTP.
set -e
in="$1"; out="$2"; hum="${3:-50}"; target="${4:--14}"
[ -n "$in" ] && [ -n "$out" ] || { echo "usage: clean_voice.sh in out.wav [hum_hz] [target]"; exit 1; }
FF="${FFMPEG:-ffmpeg}"

measure() { "$FF" -hide_banner -nostats -i "$1" -vn -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{i=$2} f&&/Peak:/{p=$2} END{printf "%s LUFS, true peak %s dBTP", i, p}'; }
echo "before: $(measure "$in")"

chain="highpass=f=80:p=2"
if [ "$hum" != "0" ]; then
  for k in 1 2 3 4; do chain="$chain,bandreject=f=$((hum*k)):width_type=q:w=30"; done
fi
chain="$chain,afftdn=nr=10:nf=-50:tn=1"
chain="$chain,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=4500:t=q:w=1:g=1.5"
chain="$chain,deesser=i=0.4:m=0.5:f=0.5:s=o"
chain="$chain,acompressor=threshold=-21dB:ratio=3:attack=8:release=150:makeup=2:knee=4"

# pass 1: measure after the chain
json=$("$FF" -hide_banner -nostats -i "$in" -vn -af "$chain,loudnorm=I=$target:TP=-1:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { printf '%s' "$json" | sed -n "s/.*\"$1\" : \"\([^\"]*\)\".*/\1/p"; }
ln="loudnorm=I=$target:TP=-1:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true"

# pass 2: apply
"$FF" -hide_banner -loglevel error -y -i "$in" -vn -af "$chain,$ln" -ar 48000 -c:a pcm_s24le "$out"
echo "after:  $(measure "$out")"
echo "wrote $out"
