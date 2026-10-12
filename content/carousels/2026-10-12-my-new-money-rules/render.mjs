// Renders the photo-dump carousel in slides.json to PNG + Instagram-ready JPG.
//   node content/carousels/2026-10-12-my-new-money-rules/render.mjs
import { readFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const { chromium } = await import('playwright');

const dir = path.dirname(fileURLToPath(import.meta.url));
const spec = JSON.parse(readFileSync(path.join(dir, 'slides.json'), 'utf8'));
mkdirSync(path.join(dir, 'export/jpg'), { recursive: true });

const html = (s, i, n) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Mono:wght@400;700&display=block" rel="stylesheet">
<style>
  html,body{margin:0;width:1080px;height:1440px;overflow:hidden;background:#0B1B2B}
  .ph{position:absolute;inset:0;background:url('${pathToFileURL(path.join(dir, s.photo)).href}') center/cover}
  .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,12,20,.62) 0%,rgba(5,12,20,.28) 34%,rgba(5,12,20,0) 52%,rgba(5,12,20,0) 78%,rgba(5,12,20,.55) 100%)}
  .txt{position:absolute;left:64px;right:64px;top:92px}
  h1{margin:0;font-family:Anton,sans-serif;font-weight:400;font-size:${s.headline.length > 12 ? 168 : 200}px;line-height:.98;color:#7DD2FD;letter-spacing:-.005em;text-transform:lowercase;text-shadow:0 4px 28px rgba(0,0,0,.35)}
  .sub{margin-top:26px;font-family:'Space Mono',monospace;font-size:36px;line-height:1.38;color:#fff;max-width:900px;text-shadow:0 2px 14px rgba(0,0,0,.7)}
  .foot{position:absolute;left:64px;right:260px;bottom:58px;font-family:'Space Mono',monospace;font-size:20px;line-height:1.45;color:rgba(255,255,255,.88);text-shadow:0 1px 8px rgba(0,0,0,.8)}
  .mark{position:absolute;right:64px;bottom:58px;font-family:'Space Mono',monospace;font-weight:700;font-size:24px;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.8)}
</style></head><body>
<div class="ph"></div><div class="shade"></div>
<div class="txt"><h1>${s.headline}</h1><div class="sub">${s.sub}</div></div>
${s.foot ? `<div class="foot">${s.foot}</div>` : ''}
<div class="mark">${i < n - 1 ? `${i + 1}/${n} &rarr;` : '@blok.capital'}</div>
</body></html>`;

const browser = await chromium.launch().catch(() => chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }));
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
for (const [i, s] of spec.slides.entries()) {
  const tmp = path.join(dir, `.slide-${i}.html`);
  (await import('node:fs')).writeFileSync(tmp, html(s, i, spec.slides.length));
  await page.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const png = path.join(dir, `slide-${String(i + 1).padStart(2, '0')}.png`);
  await page.screenshot({ path: png });
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', png, '-q:v', '2', path.join(dir, 'export/jpg', path.basename(png, '.png') + '.jpg')]);
  (await import('node:fs')).unlinkSync(tmp);
  console.log('wrote', png);
}
await browser.close();
