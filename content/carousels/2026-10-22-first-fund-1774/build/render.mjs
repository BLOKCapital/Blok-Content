// node build/render.mjs [stills|video]   (run from the carousel folder)
// stills: export/png + export/jpg per slide. video: export/mp4/slide-NN.mp4, 6 s each,
// each carrying the next 6 s of build/track.m4a so the music runs on across swipes.
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const mode = process.argv[2] || 'stills';
const fps = 30;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
await page.goto(pathToFileURL(path.resolve('scene.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const { N, SLIDE } = await page.evaluate(() => ({ N: window.N, SLIDE: window.SLIDE }));
const nn = (i) => String(i + 1).padStart(2, '0');

if (mode === 'stills') {
  mkdirSync('export/png', { recursive: true }); mkdirSync('export/jpg', { recursive: true });
  for (let i = 0; i < N; i++) {
    await page.evaluate((i) => window.draw(0, i), i);
    await page.screenshot({ path: `export/png/slide-${nn(i)}.png` });
    await page.screenshot({ path: `export/jpg/slide-${nn(i)}.jpg`, type: 'jpeg', quality: 92 });
  }
} else {
  mkdirSync('export/mp4', { recursive: true });
  for (let i = 0; i < N; i++) {
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-ss', String(i * SLIDE), '-t', String(SLIDE), '-i', 'build/track.m4a',
      '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', String(fps),
      '-af', `afade=t=in:d=${i === 0 ? 0.3 : 0.05},afade=t=out:st=${SLIDE - 0.25}:d=0.25`, '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
      `export/mp4/slide-${nn(i)}.mp4`], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < SLIDE * fps; f++) {
      await page.evaluate((t) => window.draw(t), i * SLIDE + f / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise((r) => ff.on('close', r));
    console.log(`slide ${nn(i)} done`);
  }
}
await browser.close();
