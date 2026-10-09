#!/usr/bin/env node
// Render a 1080x1920 reel from an HTML scene file that exposes window.draw(t) (t in seconds).
//
//   node scripts/render-reel.mjs <scene.html> <audio> <out.mp4> [fps=30]
//
// The scene page must define window.DURATION and window.draw(t). Frames are captured with
// Playwright and piped to ffmpeg, then muxed with the audio track (padded with silence if the
// scene runs longer than the audio).

import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [scene, audio, out, fpsArg] = process.argv.slice(2);
if (!scene || !audio || !out) {
  console.error('Usage: node scripts/render-reel.mjs <scene.html> <audio> <out.mp4> [fps]');
  process.exit(1);
}
const fps = Number(fpsArg || 30);

const { chromium } = await import('playwright');
let browser;
try {
  browser = await chromium.launch();
} catch (e) {
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
  '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
  '-i', audio,
  '-map', '0:v', '-map', '1:a',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(fps),
  '-af', 'apad', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
  out,
], { stdio: ['pipe', 'inherit', 'inherit'] });

for (let i = 0; i < frames; i++) {
  await page.evaluate((t) => window.draw(t), i / fps);
  const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  if (i % (fps * 5) === 0) console.log(`frame ${i}/${frames}`);
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
console.log(`Wrote ${out} (${frames} frames @ ${fps}fps)`);
