#!/usr/bin/env node
// Render a time-driven HTML scene to video, frame-exact (no screen recording, no dropped frames).
//
// Usage:
//   node render_html.mjs <scene.html> <out.(mov|mp4|webm)> [--dur 5] [--fps 29.97] [--w 3840] [--h 2160] [--alpha]
//
// The scene is driven by time, not by wall clock:
//   * every CSS animation / Web Animation is paused and seeked to t on each frame, and
//   * if the page defines window.renderAt(t) (seconds), it is called on each frame for JS-driven motion.
// --alpha: transparent background → ProRes 4444 .mov with alpha (for overlaying on footage).
// Needs: npm i playwright && npx playwright install chromium ; ffmpeg on PATH.
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { pathToFileURL } from "node:url";
import path from "node:path";

const args = process.argv.slice(2);
if (args.length < 2) { console.error("usage: render_html.mjs scene.html out.mov [--dur 5] [--fps 29.97] [--w 3840] [--h 2160] [--alpha]"); process.exit(1); }
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [scene, out] = args;
const dur = parseFloat(opt("--dur", "5")), fps = parseFloat(opt("--fps", "29.97"));
const W = parseInt(opt("--w", "3840")), H = parseInt(opt("--h", "2160")), alpha = args.includes("--alpha");
const scale = W / 1920; // scenes are authored at 1920x1080 CSS px; deviceScaleFactor maps them to any output size
const frames = Math.round(dur * fps);

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const page = await browser.newPage({ viewport: { width: Math.round(W / scale), height: Math.round(H / scale) }, deviceScaleFactor: scale });
await page.goto(pathToFileURL(path.resolve(scene)).href);
await page.evaluate(() => document.fonts.ready);
if (alpha) await page.addStyleTag({ content: "html,body{background:transparent!important}" });

const ff = ["-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), "-i", "-"];
const enc = out.endsWith(".mov")
  ? (alpha ? ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"] : ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"])
  : out.endsWith(".webm") ? ["-c:v", "libvpx-vp9", "-pix_fmt", alpha ? "yuva420p" : "yuv420p", "-b:v", "0", "-crf", "20"]
  : ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p"];
const proc = spawn("ffmpeg", [...ff, ...enc, out], { stdio: ["pipe", "inherit", "inherit"] });

for (let i = 0; i < frames; i++) {
  const t = i / fps;
  await page.evaluate(async (t) => {
    for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
    if (typeof window.renderAt === "function") await window.renderAt(t);
  }, t);
  const buf = await page.screenshot({ type: "png", omitBackground: alpha });
  if (!proc.stdin.write(buf)) await new Promise(r => proc.stdin.once("drain", r));
  if (i % Math.round(fps) === 0) process.stdout.write(`\r${(t).toFixed(1)}s / ${dur}s`);
}
proc.stdin.end();
await new Promise(r => proc.on("close", r));
await browser.close();
console.log(`\nwrote ${out} (${frames} frames @ ${fps} fps, ${W}x${H}${alpha ? ", alpha" : ""})`);
