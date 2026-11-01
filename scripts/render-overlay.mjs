#!/usr/bin/env node
// Render a transparent HTML overlay (window.draw(t), window.DURATION) on top of a background video, then mux audio.
// Used for the "people in scenes" Reel style (brand/reel-style.md): AI clips/stills as the background, captions,
// scoreboard and end card as the overlay.
//
//   node scripts/render-overlay.mjs <overlay.html> <background.mp4> <audio> <out.mp4> [fps=30]

import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [scene, bg, audio, out, fpsArg] = process.argv.slice(2);
if (!scene || !bg || !audio || !out) {
  console.error('Usage: node scripts/render-overlay.mjs <overlay.html> <background.mp4> <audio> <out.mp4> [fps]');
  process.exit(1);
}
const fps = Number(fpsArg || 30);
const { chromium } = await import('playwright');
let browser;
try { browser = await chromium.launch(); } catch (e) {
  if (!existsSync('/opt/pw-browsers/chromium')) throw e;
  browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
}
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.resolve(scene)).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const duration = await page.evaluate(() => window.DURATION);
const frames = Math.ceil(duration * fps);

const ff = spawn('ffmpeg', [
  '-y', '-loglevel', 'error',
  '-i', bg,
  '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
  '-i', audio,
  '-filter_complex', `[0:v]fps=${fps},scale=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=60[b];[b][1:v]overlay=0:0:shortest=1,format=yuv420p[v]`,
  '-map', '[v]', '-map', '2:a',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', String(fps),
  '-af', 'apad', '-c:a', 'aac', '-b:a', '192k', '-t', String(frames / fps), '-movflags', '+faststart',
  out,
], { stdio: ['pipe', 'inherit', 'inherit'] });

for (let i = 0; i < frames; i++) {
  await page.evaluate((t) => window.draw(t), i / fps);
  const buf = await page.screenshot({ type: 'png', omitBackground: true });
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  if (i % (fps * 5) === 0) console.log(`frame ${i}/${frames}`);
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
console.log(`Wrote ${out} (${frames} frames @ ${fps}fps)`);
