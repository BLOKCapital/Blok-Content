// Render notes.html to a transparent overlay video: node render-notes.mjs notes.mov [fps=30]
import { chromium } from '/home/claude/Blok-Content/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import path from 'node:path';
const out = process.argv[2] || 'notes.mov', fps = Number(process.argv[3] || 30);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + path.resolve('notes.html'));
await p.evaluate(() => window.ready);
const n = Math.ceil((await p.evaluate(() => window.DURATION)) * fps);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
  '-c:v', 'qtrle', '-pix_fmt', 'argb', out], { stdio: ['pipe', 'inherit', 'inherit'] });
for (let i = 0; i < n; i++) {
  await p.evaluate((t) => window.draw(t), i / fps);
  const buf = await p.screenshot({ type: 'png', omitBackground: true });
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end(); await new Promise((r) => ff.on('close', r)); await b.close();
console.log('wrote', out, n, 'frames');
