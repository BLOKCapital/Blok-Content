// node kit-render.mjs <s 1-6> <v 0|1> <out.mp4|out.png> [t for png]
import { spawn } from 'node:child_process'; import path from 'node:path'; import { pathToFileURL } from 'node:url'; import fs from 'node:fs';
const [s, v, out, tArg] = process.argv.slice(2); const V = v === '1', W = V ? 1080 : 1920, H = V ? 1920 : 1080, fps = 30;
const { chromium } = await import('playwright');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: W, height: H } });
await page.goto(pathToFileURL(path.resolve(path.dirname(new URL(import.meta.url).pathname), 'kit.html')).href + `?s=${s}&v=${v}${process.env.Q ? '&q=1' : ''}`, { waitUntil: 'load' });
await page.evaluate(async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 300)); window.draw(0); });
const grab = async (t, type = 'jpeg') => { await page.evaluate(t => window.draw(t), t); return page.locator('canvas').screenshot(type === 'png' ? { type } : { type, quality: 93 }); };
if (out.endsWith('.png')) fs.writeFileSync(out, await grab(Number(tArg || 7.9), 'png'));
else {
  const n = 8 * fps, ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) { const b = await grab(i / fps); if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
