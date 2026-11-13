#!/usr/bin/env python3
"""Word-by-word captions as an .ass file, in the style from the video:
Montserrat SemiBold, translucent dark box, short lower-centre chunks, the spoken word bright and
the rest dimmed, plus optional big yellow "pop" words beside the speaker for emphasis.

Usage:
  captions.py --words cuts/verify_v3_words.json --out fx/captions.ass [--video renders/v3.mp4]
              [--emphasis "emphasis,captions,music"] [--max-words 3] [--font "Montserrat SemiBold"]
              [--pop-font "Montserrat ExtraBold"] [--vertical]
  captions.py --transcribe renders/v3.mp4 --out fx/captions.ass ...   (needs faster-whisper or mlx-whisper)

Burn in:
  ffmpeg -i renders/v3.mp4 -vf "ass=fx/captions.ass:fontsdir=$HOME/Movies/edits/_assets/fonts" -c:a copy renders/v4.mp4

Accepted --words formats: simcraft {"clip": [[start,end,word,prob],...]}, a list of [start,end,word,...],
or a list of {"start","end","word"|"text"}.
"""
import argparse, json, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--words"); ap.add_argument("--transcribe"); ap.add_argument("--out", required=True)
ap.add_argument("--video"); ap.add_argument("--emphasis", default="")
ap.add_argument("--max-words", type=int, default=3); ap.add_argument("--max-gap", type=float, default=0.6)
ap.add_argument("--font", default="Montserrat SemiBold"); ap.add_argument("--pop-font", default="Montserrat ExtraBold")
ap.add_argument("--vertical", action="store_true"); ap.add_argument("--lang", default=None)
a = ap.parse_args()

def load_words():
    if a.words:
        d = json.load(open(a.words))
        if isinstance(d, dict):  # simcraft: {clip: [[s,e,w,p],...]} — concatenate in order
            d = [w for k in d for w in d[k]]
        out = []
        for w in d:
            if isinstance(w, dict):
                out.append((float(w["start"]), float(w["end"]), str(w.get("word", w.get("text", "")))))
            else:
                out.append((float(w[0]), float(w[1]), str(w[2])))
        return out
    if a.transcribe:
        try:
            import mlx_whisper
            r = mlx_whisper.transcribe(a.transcribe, word_timestamps=True, language=a.lang,
                                       path_or_hf_repo="mlx-community/whisper-large-v3-turbo")
            return [(w["start"], w["end"], w["word"]) for s in r["segments"] for w in s.get("words", [])]
        except ImportError:
            from faster_whisper import WhisperModel
            m = WhisperModel("large-v3", compute_type="auto")
            segs, _ = m.transcribe(a.transcribe, word_timestamps=True, language=a.lang)
            return [(w.start, w.end, w.word) for s in segs for w in s.words]
    sys.exit("give --words or --transcribe")

words = [(s, e, t.strip()) for s, e, t in load_words() if t.strip()]
words.sort()
if not words: sys.exit("no words")

W, H = (1080, 1920) if a.vertical else (1920, 1080)
if a.video:
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "json", a.video], capture_output=True, text=True).stdout)
    W, H = p["streams"][0]["width"], p["streams"][0]["height"]
u = H / 1080  # scale styles to resolution

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

emph = {x.strip().lower() for x in a.emphasis.split(",") if x.strip()}
norm = lambda w: re.sub(r"[^\w']", "", w.lower())

# chunk: up to max-words, break on punctuation or gaps
chunks, cur = [], []
for w in words:
    if cur and (len(cur) >= a.max_words or w[0] - cur[-1][1] > a.max_gap or re.search(r"[.!?,;:]$", cur[-1][2])):
        chunks.append(cur); cur = []
    cur.append(w)
if cur: chunks.append(cur)

BRIGHT, DIM = "&H00FFFFFF&", "&H00A8A8A8&"
fs, mv = round(46 * u), round(110 * u)
head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{a.font},{fs},&H00FFFFFF,&H00FFFFFF,&H70000000,&H70000000,0,0,0,0,100,100,1,0,3,{round(10*u)},0,2,60,60,{mv},1
Style: Pop,{a.pop_font},{round(120*u)},&H0024C8FF,&H0024C8FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,0,{round(4*u)},6,60,{round(150*u)},{round(300*u)},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for ch in chunks:
    for i, (s, e, _) in enumerate(ch):
        end = ch[i + 1][0] if i + 1 < len(ch) else e + 0.15
        txt = " ".join((f"{{\\c{BRIGHT}}}" if j == i else f"{{\\c{DIM}}}") + w.replace("{", "").replace("}", "")
                       for j, (_, _, w) in enumerate(ch))
        lines.append(f"Dialogue: 0,{ts(s)},{ts(end)},Cap,,0,0,0,,{txt}")
    for s, e, w in ch:
        if norm(w) in emph:
            pop = "{\\fad(60,120)\\t(0,140,\\fscx112\\fscy112)\\t(140,260,\\fscx100\\fscy100)}" + norm(w).upper()
            lines.append(f"Dialogue: 1,{ts(s)},{ts(max(e, s + 0.9))},Pop,,0,0,0,,{pop}")

open(a.out, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
print(f"wrote {a.out}: {len(words)} words, {len(chunks)} lines, {sum(1 for l in lines if ',Pop,' in l)} emphasis pops, {W}x{H}")
