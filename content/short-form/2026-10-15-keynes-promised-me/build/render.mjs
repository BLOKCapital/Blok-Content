// node render.mjs preview t1,t2,...   |   node render.mjs full out.mp4 [fps]
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process';
const ROOT = path.resolve('../../../..'); const REL = path.relative(ROOT, process.cwd());
const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png' };
const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); });
await new Promise(r => srv.listen(8765, r));
const { chromium } = await import(path.join(ROOT, 'node_modules/playwright/index.mjs'));
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on('console', m => console.log('page:', m.text())); page.on('pageerror', e => console.log('ERR', e.message));
await page.goto(`http://localhost:8765/${REL}/scene.html`);
await page.waitForFunction(() => window.READY, null, { timeout: 60000 }); await page.evaluate(() => document.fonts.ready);
const [mode, arg, fpsA] = process.argv.slice(2);
if (mode === 'preview') {
  fs.mkdirSync('prev', { recursive: true });
  for (const t of arg.split(',').map(Number)) { await page.evaluate(t => window.draw(t), t); await page.screenshot({ path: `prev/t${t}.jpg`, type: 'jpeg', quality: 85 }); }
} else {
  const fps = Number(fpsA || 30); const dur = await page.evaluate(() => window.DURATION); const n = Math.ceil(dur * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-i', 'vo.m4a',
    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-af', 'apad', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', arg], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) { await page.evaluate(t => window.draw(t), i / fps); const b = await page.screenshot({ type: 'jpeg', quality: 90 });
    if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 150 === 0) console.log(`frame ${i}/${n} ${((Date.now() - t0) / 1000).toFixed(0)}s`); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close(); srv.close();
