# Claude video-editing skills

Reusable Claude Code skills reverse-engineered from simran sachdeva's "here's how i edit my videos with Claude (beginner edition)" (X, 12 Nov 2026, 3:19). One skill per step shown in the video, plus `edit-with-claude`, which runs all ten in order.

| # | Skill | What it does | Prompt from the video |
|---|---|---|---|
| — | `edit-with-claude` | Runs the full 10-step pipeline | — |
| 1 | `project-folder` | Dated folder per video, raw files copied in as read-only | *(Finder)* |
| 2 | `rough-cut-pass` | Transcript-based cut: pauses, ums, retakes (17:48 → 3:54) | `rough cut raw/DJI_0048.MP4, keep my last good take of every line` |
| 3 | `clean-audio-pass` | Rumble/hum/EQ/de-ess/3:1 comp → -14 LUFS | `clean up the audio, social loudness` |
| 4 | `pacing-punch-in` | Cuts pauses over 0.3 s and adds 8% punch-ins (3:54 → 3:23) | `tighten the pacing: cut pauses over 0.3 s, punch in on "…"` |
| 5 | `motion-graphic` | HTML scene rendered frame-exact to video, then composited | `make a motion graphic for the rough-cut stat: 17:48 to 3:54, …` |
| 5b | `brand-kit-graphics` | Same graphic in a sponsor's real fonts and colours | *(shown, prompt not on screen)* |
| 6 | `captions` | Word-by-word .ass captions with yellow emphasis pops | `add captions in my style: Montserrat SemiBold, translucent box, …` |
| 7 | `music-bed` | Normalise the bed to -18 LUFS and sidechain-duck it ~8 dB under the voice | `music: calm lo-fi under the voice, it should never overpower me` |
| 8 | `color-grade` | WB, blacks and exposure, then an inspo-match LUT with skin protected | `fix the basics: white balance, blacks, exposure` / `[Image #1] match this warm film look, keep my skin natural` |
| 9 | `final-mix` | Two-pass loudnorm: -14 LUFS, -1 dBTP | `final mix: -14 LUFS, true peak -1 dB` |
| 10 | `export-master` | HEVC 10-bit at the source's resolution and frame rate | `export at source settings` |

## Install (Mac)

```bash
brew install ffmpeg
git clone https://github.com/octavian115/claude-skills ~/claude-skills
mkdir -p ~/.claude/skills
sh ~/claude-skills/install.sh video
pip3 install numpy pillow                     # color-grade
npm i -g playwright && npx playwright install chromium   # motion-graphic

# Steps 2, 3 and 5b build on the author's open-source skills (MIT). Read them before you run their setup:
git clone https://github.com/dotslashsimran/simcraft ~/simcraft
ln -sfn ~/simcraft/skills/video/rough-cut   ~/.claude/skills/rough-cut
ln -sfn ~/simcraft/skills/video/clean-audio ~/.claude/skills/clean-audio
ln -sfn ~/simcraft/skills/design/brand-kit  ~/.claude/skills/brand-kit
sh ~/simcraft/skills/video/rough-cut/setup.sh
```

Then run `cd ~/Movies/edits/<project> && claude` and type the prompts. Claude Code picks the skill whose description matches what you asked for. You can also name a skill directly, for example "use the captions skill".

Script paths in each SKILL.md (`scripts/…`) are relative to that skill's folder: `~/.claude/skills/<skill>/scripts/…`.

## What's tested
I ran every script in this pack on synthetic test clips: punch-in, the HTML→video renderer (with and without alpha), captions burned in, the music duck, voice clean (-21.8 → -14.0 LUFS), the grade LUT, final mix and HEVC 10-bit export. Run them on a short real clip before you trust them on a full video.

## Sources
- Video: https://x.com/simranrambles/status/2120917774315008240
- Author's skills: https://github.com/dotslashsimran/simcraft
