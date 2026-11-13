---
name: brand-kit-graphics
description: Pull a company's real brand (colours, font files, logo, card shapes) from its live website into a reusable kit, then restyle motion graphics to match — same graphic, the brand's exact fonts and colours. Use before any sponsored or client graphic, or when the user says "make it on-brand for <company>", "match their brand", "use <company>'s colours/fonts".
---

# Step 5b — Brand kit for graphics

Shown in the video: the same ROUGH CUT 3:54 graphic re-rendered next to a **BRAND KIT** panel for "Northwind" (northwind.com): five colour swatches (deep green → mint → cream → near-black), typeface **Avenir Next** (Regular · Medium · Demi Bold), footer "3 font files · 3 stylesheets · pulled from the live site". Caption: **"Same graphic, the brand's exact fonts and colours."** She described it as matching a sponsor's "design system".

## Option A — author's skill (simcraft `brand-kit`)
```bash
ln -s ~/simcraft/skills/design/brand-kit ~/.claude/skills/brand-kit
cd ~/simcraft && npm i
node   ~/simcraft/skills/design/brand-kit/scripts/extract.mjs https://<brand>.com ~/.local/share/simcraft/brands/<slug> [https://<brand>.com/product]
python3 ~/simcraft/skills/design/brand-kit/scripts/propose.py ~/.local/share/simcraft/brands/<slug> --name "<Brand>"
python3 ~/simcraft/skills/design/brand-kit/scripts/board.py   ~/.local/share/simcraft/brands/<slug>    # → board.png, check it
```
Then add `"brand": "<slug>"` to a vox-explainer scene.

## Option B — apply to this pack's HTML scenes
1. Open the brand's site in a browser (or read its press kit / brand guidelines — official files beat scraped CSS).
2. Record in `~/Movies/edits/_assets/brands/<slug>/brand.json`:
   `{"bg","card","ink","muted","accent","rule","display_font","body_font","font_files":[…],"radius"}`
3. Put the font files next to it and add `@font-face` rules to the scene.
4. Override the CSS variables at the top of the scene (`--bg --card --ink --muted --accent --rule --display --body`) — the stat template is built so only these change.
5. Re-render with the same `render_html.mjs` command; show the user the board/still side by side with the brand's site before final.

## Rules
- Run this **before** making anything for a brand; never guess brand colours.
- Brand fonts/logos are licensed to that company: use them only for work with or about that brand, never commit or redistribute the files.
- Monochrome brands have a black accent — that's correct, don't invent a colour.

## Template
```
make the rough-cut graphic on-brand for <company> (<url>) — pull their colours and fonts from the live site
```
