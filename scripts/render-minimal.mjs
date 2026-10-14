#!/usr/bin/env node
// Render a "minimal" carousel (brand/carousel-maker.md rules) from slides.json.
//
//   node scripts/render-minimal.mjs content/carousels/<slug>/slides.json
//
// Output in <slug>/export/: slide-NN.png, jpg/slide-NN.jpg, and (when "music" is set)
// mp4/slide-NN.mp4: each slide as a still video carrying the next segment of the track,
// so the music runs continuously as people swipe.
//
// Layout follows the Z-pattern: kicker top-left → page marker top-right → headline →
// body → brand bottom-left → "Swipe" bottom-right. Left-aligned, brand colours only.

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const specPath = path.resolve(process.argv[2]);
const dir = path.dirname(specPath);
const spec = JSON.parse(await readFile(specPath, 'utf8'));
const [W, H] = spec.size || [1080, 1440];
const N = spec.slides.length;

const C = { linen: '#F6F3E8', indigo: '#004EBA', lime: '#7ED116', sky: '#7DD2FD', coral: '#EC464D', earth: '#844947', ink: '#0B1B2B' };
const THEMES = {
  linen: { bg: C.linen, fg: C.ink, head: C.indigo, kick: C.earth, hl: C.lime, hlText: C.ink, muted: '#5B5A55', rule: C.indigo },
  indigo: { bg: C.indigo, fg: C.linen, head: '#FFFFFF', kick: C.sky, hl: C.lime, hlText: C.ink, muted: '#CFE6FF', rule: C.lime },
};

const esc = (s = '') => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const rich = (s = '') => esc(s).replace(/\*\*(.+?)\*\*/g, '<span class="hl">$1</span>').replace(/\n/g, '<br>');
const logo = `data:image/png;base64,${(await readFile(path.join(ROOT, 'brand/assets/logo-wordmark.png'))).toString('base64')}`;

function slideHtml(s, i) {
  const t = THEMES[s.theme || 'linen'];
  const big = s.big ? `<div class="big" style="color:${s.bigColor ? C[s.bigColor] : t.head}">${esc(s.big)}</div>` : '';
  const steps = s.steps
    ? `<div class="steps">${s.steps.map((x, k) => `<div class="step ${k ? 'on' : ''}"><b>${k + 1}</b>${esc(x)}</div>`).join('<div class="arrow">→</div>')}</div>`
    : '';
  const isHook = s.role === 'hook';
  const isCta = s.role === 'cta';
  return `<section class="slide ${s.role}" style="--bg:${t.bg};--fg:${t.fg};--head:${t.head};--kick:${t.kick};--hl:${t.hl};--hlt:${t.hlText};--muted:${t.muted};--rule:${t.rule}">
  <header><div class="kick">${esc(s.kicker || '')}</div><div class="page">${String(i + 1).padStart(2, '0')} / ${String(N).padStart(2, '0')}</div></header>
  <main>
    ${big}
    <div class="rule"></div>
    <h1>${rich(s.title)}</h1>
    ${s.sub ? `<p class="sub">${rich(s.sub)}</p>` : ''}
    ${s.body ? `<p class="body">${rich(s.body)}</p>` : ''}
    ${steps}
    ${s.button ? `<div class="button">${esc(s.button)}</div>` : ''}
  </main>
  <footer>
    <div class="brand"><span class="pill"><img src="${logo}"></span>${s.source ? `<span class="src">${esc(s.source)}</span>` : ''}</div>
    <div class="next">${isCta ? 'Save it ↓' : isHook ? 'Swipe →' : 'Next →'}</div>
  </footer>
  ${s.disclaimer ? `<p class="disc">${esc(s.disclaimer)}</p>` : ''}
</section>`;
}

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;800;900&family=Inter:wght@400;500;600&display=block');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#888}
.slide{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:var(--bg);color:var(--fg);font-family:Montserrat,sans-serif;
  padding:96px 96px 0 96px;display:flex;flex-direction:column}
header{display:flex;justify-content:space-between;align-items:center}
.kick{font-weight:800;font-size:26px;letter-spacing:.16em;text-transform:uppercase;color:var(--kick)}
.page{font-family:Inter;font-weight:600;font-size:24px;letter-spacing:.08em;color:var(--muted)}
main{flex:1;display:flex;flex-direction:column;justify-content:center;max-width:860px;padding-bottom:40px}
.rule{width:120px;height:10px;background:var(--rule);border-radius:5px;margin-bottom:44px}
h1{font-weight:900;font-size:88px;line-height:1.04;letter-spacing:-2px;color:var(--head)}
.hook h1{font-size:112px;letter-spacing:-3px}
.cta h1{font-size:100px}
.hl{background:linear-gradient(transparent 58%, var(--hl) 58%, var(--hl) 92%, transparent 92%);padding:0 6px;margin:0 -6px}
.hook .hl,.cta .hl{color:var(--hl);background:none;padding:0;margin:0}
.sub{font-family:Inter;font-weight:500;font-size:44px;line-height:1.3;margin-top:40px;color:var(--muted)}
.body{font-family:Inter;font-weight:400;font-size:40px;line-height:1.42;margin-top:40px;color:var(--fg)}
.body .hl{font-weight:600}
.big{font-weight:900;font-size:200px;line-height:.9;letter-spacing:-8px;margin-bottom:48px}
.steps{display:flex;align-items:center;gap:24px;margin-top:56px}
.step{font-weight:800;font-size:34px;padding:22px 30px;border-radius:18px;border:3px solid ${C.indigo};color:${C.indigo};display:flex;gap:16px;align-items:center}
.step b{font-size:26px;width:44px;height:44px;border-radius:50%;background:${C.indigo};color:#fff;display:grid;place-items:center}
.step.on{background:${C.lime};border-color:${C.lime};color:${C.ink}}
.step.on b{background:${C.ink}}
.arrow{font-size:44px;color:${C.earth};font-weight:800}
.button{align-self:flex-start;margin-top:56px;background:${C.coral};color:#fff;font-weight:800;font-size:40px;padding:28px 48px;border-radius:999px}
footer{height:150px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid color-mix(in srgb, var(--fg) 14%, transparent)}
.brand{display:flex;align-items:center;gap:24px}
.pill{background:${C.linen};border-radius:14px;padding:10px 16px;display:flex}
.pill img{height:40px}
.src{font-family:Inter;font-size:20px;color:var(--muted);max-width:520px;line-height:1.3}
.next{font-weight:800;font-size:30px;color:var(--head);white-space:nowrap}
.disc{position:absolute;left:96px;right:96px;bottom:166px;font-family:Inter;font-size:21px;line-height:1.35;color:var(--muted)}
.cta main{padding-bottom:120px}
</style></head><body>${spec.slides.map(slideHtml).join('\n')}</body></html>`;

const out = path.join(dir, 'export');
await mkdir(path.join(out, 'jpg'), { recursive: true });
await writeFile(path.join(out, 'preview.html'), html);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.setContent(html, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const els = await page.$$('section.slide');
for (let i = 0; i < els.length; i++) {
  const nn = String(i + 1).padStart(2, '0');
  const png = path.join(out, `slide-${nn}.png`);
  await els[i].screenshot({ path: png });
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', png, '-q:v', '2', path.join(out, 'jpg', `slide-${nn}.jpg`)]);
}
await browser.close();

// Video slides with a continuous music track.
if (spec.music) {
  const music = path.resolve(dir, spec.music);
  const d = spec.secondsPerSlide || 6;
  await mkdir(path.join(out, 'mp4'), { recursive: true });
  for (let i = 0; i < N; i++) {
    const nn = String(i + 1).padStart(2, '0');
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error',
      '-loop', '1', '-framerate', '30', '-t', String(d), '-i', path.join(out, `slide-${nn}.png`),
      '-ss', String(i * d), '-t', String(d), '-i', music,
      '-filter_complex', `[1:a]afade=t=in:d=0.15,afade=t=out:st=${d - 0.4}:d=0.4[a]`,
      '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
      '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-shortest', '-movflags', '+faststart',
      path.join(out, 'mp4', `slide-${nn}.mp4`)]);
  }
}
console.log(`Rendered ${N} slides to ${path.relative(ROOT, out)}`);
