// node render.mjs <scene.html> <out.mp4|preview.jpg> [v=0|1] [fps=30] [times...]
// Renders the canvas scene to a silent MP4, or (with .jpg + times) a preview contact sheet.
import { spawn, execFileSync } from 'node:child_process';
import path from 'node:path'; import { pathToFileURL } from 'node:url'; import fs from 'node:fs';
const [scene, out, v = '0', fpsArg = '30', ...times] = process.argv.slice(2);
const V = v === '1', W = V ? 1080 : 1920, H = V ? 1920 : 1080, fps = Number(fpsArg);
const { chromium } = await import('playwright');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: W, height: H } });
await page.goto(pathToFileURL(path.resolve(scene)).href + (V ? '?v=1' : ''), { waitUntil: 'load' });
await page.evaluate(async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 300)); });
const grab = async t => { await page.evaluate(t => window.draw(t), t); return page.locator('canvas').screenshot({ type: 'jpeg', quality: 92 }); };
if (out.endsWith('.jpg')) {
  const dir = fs.mkdtempSync('/tmp/prev'); let i = 0;
  for (const t of times) fs.writeFileSync(`${dir}/${String(i++).padStart(3, '0')}.jpg`, await grab(Number(t)));
  const cols = V ? 8 : 6;
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-pattern_type', 'glob', '-i', `${dir}/*.jpg`, '-vf', `scale=${V ? 240 : 400}:-1,tile=${cols}x${Math.ceil(times.length / cols)}`, '-frames:v', '1', out]);
} else {
  const dur = await page.evaluate(() => window.DURATION), n = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) { const b = await grab(i / fps); if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 300 == 0) console.log(i, '/', n); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
