// Overlay renderer: draws scene.html (transparent) on top of bg.mp4, muxes audio.
//   node render.mjs cuts            -> prints CUTS + DURATION as JSON
//   node render.mjs render bg.mp4 audio.m4a out.mp4 [fps]
//   node render.mjs still t out.png
import { spawn } from 'node:child_process';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [mode, a1, a2, a3, fpsArg] = process.argv.slice(2);
const { chromium } = await import('playwright');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--headless=new','--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(pathToFileURL(path.resolve('scene.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const info = await page.evaluate(() => ({ cuts: window.CUTS, duration: window.DURATION }));
if (mode === 'cuts') console.log(JSON.stringify(info));
if (mode === 'still') { await page.evaluate((t) => window.draw(t), Number(a1)); await page.screenshot({ path: a2, omitBackground: true }); }
if (mode === 'render') {
  const fps = Number(fpsArg || 30), frames = Math.ceil(info.duration * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', a1,
    '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-', '-i', a2,
    '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]', '-map', '[v]', '-map', '2:a',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', String(fps), '-c:a', 'aac', '-b:a', '192k',
    '-t', String(info.duration), '-movflags', '+faststart', a3], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < frames; i++) {
    await page.evaluate((t) => window.draw(t), i / fps);
    const buf = await page.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${frames}`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
}
await browser.close();
