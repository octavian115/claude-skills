# claude-skills

Skills that teach [Claude Code](https://claude.com/claude-code) to do real work end to end, each with tested scripts rather than just prompts.

Each skill is a folder with a `SKILL.md` covering the method, the commands and the rules, plus the scripts it runs. You don't call skills by name. You ask for the task ("rough cut this clip", "add captions in my style") and Claude Code loads the skill that matches.

## Skills

### 🎬 Video — [skills/video](skills/video)

A full talking-head edit run from the terminal: one prompt per step, from raw footage to a 4K export.

| Skill | What it does |
|:--|:--|
| [**edit-with-claude**](skills/video/edit-with-claude/SKILL.md) | Runs all ten steps in order, with a preview after each one |
| [**project-folder**](skills/video/project-folder/SKILL.md) | Creates a dated workspace; raw footage is copied in and never modified |
| [**rough-cut-pass**](skills/video/rough-cut-pass/SKILL.md) | Cuts from the transcript: dead air, ums and retakes out, then checks the result by re-listening |
| [**clean-audio-pass**](skills/video/clean-audio-pass/SKILL.md) | Removes rumble, hum and harsh S's, adds clarity and sets loudness to -14 LUFS |
| [**pacing-punch-in**](skills/video/pacing-punch-in/SKILL.md) | Cuts pauses over 0.3 s and adds 8% punch-in zooms on key lines |
| [**motion-graphic**](skills/video/motion-graphic/SKILL.md) | Graphics written as HTML and rendered frame-exact to video (alpha supported) |
| [**brand-kit-graphics**](skills/video/brand-kit-graphics/SKILL.md) | Remakes the same graphic in a sponsor's real fonts and colours |
| [**captions**](skills/video/captions/SKILL.md) | Word-by-word burned-in captions, with emphasis words popping beside the speaker |
| [**music-bed**](skills/video/music-bed/SKILL.md) | Puts music under the voice and lowers it automatically whenever you speak |
| [**color-grade**](skills/video/color-grade/SKILL.md) | Corrects white balance, blacks and exposure, then matches an inspiration still without shifting skin tones |
| [**final-mix**](skills/video/final-mix/SKILL.md) | Two-pass loudness normalisation to -14 LUFS and -1 dBTP |
| [**export-master**](skills/video/export-master/SKILL.md) | Exports HEVC 10-bit at the source's resolution and frame rate |

More categories will be added over time.

## Install

```bash
git clone https://github.com/octavian115/claude-skills ~/claude-skills
sh ~/claude-skills/install.sh          # every skill
sh ~/claude-skills/install.sh video    # or one category
```

`install.sh` links each skill into `~/.claude/skills/`. Claude Code only finds skills one folder deep, so the category folders are for browsing only. Because the skills are linked rather than copied, `git pull` updates them everywhere.

Requirements for the video skills: `ffmpeg`, Python 3.9+ (`pip install numpy pillow`), Node 18+ with Playwright for motion graphics. The rough-cut, clean-audio and brand-kit steps build on simcraft (credited below). Full setup is in [skills/video/README.md](skills/video/README.md).

## Credits

The video workflow is adapted from simran sachdeva's [how I edit my videos with Claude](https://x.com/simranrambles/status/2120917774315008240). Three of its steps call her MIT-licensed [simcraft](https://github.com/dotslashsimran/simcraft) skills, which are installed separately and not copied here.

## License

[MIT](LICENSE)
