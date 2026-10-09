#!/usr/bin/env node
// Render an on-brand BLOK Capital carousel from a slides.json file into PNGs.
//
//   node scripts/render-carousel.mjs content/carousels/<slug>/slides.json
//
// Output: <slug>/export/slide-01.png ..., publish-ready <slug>/export/jpg/slide-01.jpg ...,
// plus <slug>/export/preview.html.
// Slide schema: see templates/carousel/README.md.

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { stickerPages } from './lib/sticker.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const W = 1080;
const H = 1350;

const THEMES = {
  linen: { bg: '#F6F3E8', fg: '#0B1B2B', head: '#004EBA', accent: '#7ED116', muted: '#844947', logo: 'logo-wordmark.png' },
  indigo: { bg: '#004EBA', fg: '#F6F3E8', head: '#FFFFFF', accent: '#7DD2FD', muted: '#CFE6FF', logo: 'logo-mark-white-bg.png' },
  night: { bg: '#0B1B2B', fg: '#F6F3E8', head: '#7DD2FD', accent: '#7ED116', muted: '#9FB3C8', logo: 'logo-mark-black-bg.png' },
  lime: { bg: '#7ED116', fg: '#0B1B2B', head: '#0B1B2B', accent: '#004EBA', muted: '#2B4A0B', logo: 'logo-wordmark.png' },
};

const esc = (s = '') =>
  String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

// **word** → accent highlight, __word__ → coral underline. Everything else escaped.
const rich = (s = '') =>
  esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<span class="hl">$1</span>')
    .replace(/__(.+?)__/g, '<span class="ul">$1</span>')
    .replace(/\n/g, '<br>');

async function dataUri(file) {
  const buf = await readFile(path.join(ROOT, 'brand/assets', file));
  return `data:image/png;base64,${buf.toString('base64')}`;
}

function slideBody(s) {
  switch (s.type) {
    case 'cover':
      return `
        ${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}
        <h1 class="cover-title">${rich(s.title)}</h1>
        ${s.subtitle ? `<p class="sub">${rich(s.subtitle)}</p>` : ''}
        <div class="swipe">Swipe →</div>`;
    case 'list':
      return `
        ${s.title ? `<h2>${rich(s.title)}</h2>` : ''}
        <ol class="list">${(s.items || []).map((i) => `<li><span>${rich(i)}</span></li>`).join('')}</ol>`;
    case 'compare':
      return `
        ${s.title ? `<h2>${rich(s.title)}</h2>` : ''}
        <div class="compare">
          <div class="col old"><div class="col-h">${esc(s.left?.label || 'Old way')}</div>
            ${(s.left?.items || []).map((i) => `<p>✕ ${rich(i)}</p>`).join('')}</div>
          <div class="col new"><div class="col-h">${esc(s.right?.label || 'BLOK')}</div>
            ${(s.right?.items || []).map((i) => `<p>✓ ${rich(i)}</p>`).join('')}</div>
        </div>`;
    case 'stat':
      return `
        <div class="stat">${rich(s.value)}</div>
        <h2>${rich(s.title || '')}</h2>
        ${s.body ? `<p class="body">${rich(s.body)}</p>` : ''}`;
    case 'quote':
      return `
        <blockquote>“${rich(s.quote)}”</blockquote>
        ${s.by ? `<div class="by">${esc(s.by)}</div>` : ''}`;
    case 'cta':
      return `
        <h1 class="cta-title">${rich(s.title)}</h1>
        ${s.body ? `<p class="body">${rich(s.body)}</p>` : ''}
        ${s.button ? `<div class="button">${esc(s.button)}</div>` : ''}
        ${s.handle ? `<div class="handle">${esc(s.handle)}</div>` : ''}`;
    case 'text':
    default:
      return `
        ${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}
        ${s.title ? `<h2>${rich(s.title)}</h2>` : ''}
        ${s.body ? `<p class="body">${rich(s.body)}</p>` : ''}`;
  }
}

function css(t) {
  return `
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;700&family=JetBrains+Mono:wght@500&display=block');
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#222}
  .slide{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:${t.bg};color:${t.fg};
    font-family:Inter,system-ui,sans-serif;padding:110px 90px 150px;display:flex;flex-direction:column;justify-content:center;gap:36px}
  .slide.cover{justify-content:flex-end;padding-bottom:220px}
  h1,h2{font-family:Fraunces,Georgia,serif;color:${t.head};letter-spacing:-0.02em;line-height:1.02}
  .cover-title{font-size:112px;font-weight:800}
  .cta-title{font-size:96px;font-weight:800}
  h2{font-size:76px;font-weight:700}
  .kicker{font-family:'JetBrains Mono',monospace;font-size:28px;text-transform:uppercase;letter-spacing:.12em;color:${t.muted}}
  .sub,.body{font-size:40px;line-height:1.35;max-width:880px}
  .hl{color:${t.accent === '#7ED116' && t.bg === '#F6F3E8' ? t.head : t.accent};background:${t.bg === '#F6F3E8' ? 'linear-gradient(transparent 58%, #7ED11699 58%)' : 'none'}}
  .ul{text-decoration:underline;text-decoration-color:#EC464D;text-decoration-thickness:8px;text-underline-offset:10px}
  .list{list-style:none;counter-reset:n;display:flex;flex-direction:column;gap:28px}
  .list li{counter-increment:n;display:flex;gap:28px;align-items:flex-start;font-size:40px;line-height:1.3}
  .list li::before{content:counter(n);flex:none;width:64px;height:64px;border-radius:16px;background:${t.accent};color:${t.bg === '#7ED116' ? '#F6F3E8' : '#0B1B2B'};
    font-family:'JetBrains Mono',monospace;font-size:32px;display:flex;align-items:center;justify-content:center;margin-top:-4px}
  .compare{display:grid;grid-template-columns:1fr 1fr;gap:28px}
  .col{border-radius:28px;padding:40px 34px;display:flex;flex-direction:column;gap:20px;font-size:32px;line-height:1.3}
  .col.old{border:3px dashed #844947;opacity:.85}
  .col.new{background:${t.bg === '#F6F3E8' ? '#004EBA' : '#F6F3E8'};color:${t.bg === '#F6F3E8' ? '#F6F3E8' : '#0B1B2B'}}
  .col-h{font-family:'JetBrains Mono',monospace;font-size:26px;text-transform:uppercase;letter-spacing:.1em}
  .stat{font-family:Fraunces,serif;font-weight:800;font-size:260px;line-height:.9;color:${t.accent}}
  blockquote{font-family:Fraunces,serif;font-size:72px;line-height:1.15;color:${t.head}}
  .by{font-size:32px;color:${t.muted}}
  .button{align-self:flex-start;background:#EC464D;color:#fff;font-weight:700;font-size:38px;padding:26px 48px;border-radius:999px}
  .handle{font-family:'JetBrains Mono',monospace;font-size:30px;color:${t.muted}}
  .swipe{font-family:'JetBrains Mono',monospace;font-size:28px;color:${t.muted}}
  .footer{position:absolute;left:90px;right:90px;bottom:60px;display:flex;align-items:center;justify-content:space-between;
    font-family:'JetBrains Mono',monospace;font-size:24px;color:${t.muted}}
  .footer img{height:44px}
  .footer img.mark{height:64px;border-radius:12px}
  .disclaimer{position:absolute;left:90px;right:90px;bottom:120px;font-size:20px;line-height:1.35;color:${t.muted};opacity:.9}
  .sprout{position:absolute;right:-60px;top:-60px;width:360px;height:360px;border-radius:50%;background:${t.accent};opacity:.18}
  .page{position:absolute;top:60px;right:90px;font-family:'JetBrains Mono',monospace;font-size:24px;color:${t.muted}}`;
}

// Assets for the sticker style: the round logo mark plus any images slides reference (paths relative to slides.json).
async function stickerAssets(spec, input, logos) {
  const imgs = {};
  for (const s of spec.slides || []) {
    const src = s.visual?.img;
    if (src && !imgs[src]) {
      const buf = await readFile(path.resolve(path.dirname(input), src));
      const ext = path.extname(src).slice(1).toLowerCase().replace('jpg', 'jpeg');
      imgs[src] = `data:image/${ext === 'svg' ? 'svg+xml' : ext};base64,${buf.toString('base64')}`;
    }
  }
  return { mark: logos['logo-mark-white-bg.png'], image: (src) => imgs[src] };
}

async function main() {
  const input = process.argv[2];
  if (!input) {
    console.error('Usage: node scripts/render-carousel.mjs <path/to/slides.json>');
    process.exit(1);
  }
  const spec = JSON.parse(await readFile(input, 'utf8'));
  const outDir = path.join(path.dirname(input), 'export');
  await mkdir(path.join(outDir, 'jpg'), { recursive: true });

  const slides = spec.slides || [];
  const logos = {};
  for (const t of Object.values(THEMES)) logos[t.logo] ??= await dataUri(t.logo);

  const pages = spec.style === 'sticker' ? stickerPages(spec, await stickerAssets(spec, input, logos)) : slides.map((s, i) => {
    const t = THEMES[s.theme || spec.theme || 'linen'] || THEMES.linen;
    const markClass = t.logo.startsWith('logo-mark') ? 'mark' : '';
    const disclaimer = s.disclaimer === true ? spec.disclaimer : s.disclaimer;
    return `<!doctype html><html><head><meta charset="utf-8"><style>${css(t)}</style></head><body>
      <div class="slide ${s.type === 'cover' ? 'cover' : ''}">
        ${s.type === 'cover' ? '<div class="sprout"></div>' : ''}
        ${spec.showPageNumbers !== false && s.type !== 'cover' ? `<div class="page">${i + 1}/${slides.length}</div>` : ''}
        ${slideBody(s)}
        ${disclaimer ? `<div class="disclaimer">${esc(disclaimer)}</div>` : ''}
        <div class="footer"><img class="${markClass}" src="${logos[t.logo]}"><span>${esc(spec.handle || '@blok_cap')}</span></div>
      </div></body></html>`;
  });

  const { chromium } = await import('playwright');
  const exe = '/opt/pw-browsers/chromium';
  let browser;
  try {
    browser = await chromium.launch();
  } catch (e) {
    if (!existsSync(exe)) throw e;
    browser = await chromium.launch({ executablePath: exe });
  }
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const files = [];
  for (let i = 0; i < pages.length; i++) {
    await page.setContent(pages[i], { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const file = path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`);
    await page.locator('.slide').screenshot({ path: file });
    // Instagram only accepts JPEG, so write a publish-ready copy alongside the PNG.
    await page.locator('.slide').screenshot({ path: path.join(outDir, 'jpg', path.basename(file, '.png') + '.jpg'), type: 'jpeg', quality: 95 });
    files.push(path.basename(file));
  }
  await browser.close();

  const preview = `<!doctype html><meta charset="utf-8"><title>${esc(spec.title || 'Carousel')}</title>
    <body style="margin:0;background:#111;display:flex;gap:16px;overflow-x:auto;padding:16px">
    ${files.map((f) => `<img src="${f}" style="height:80vh;border-radius:8px">`).join('')}</body>`;
  await writeFile(path.join(outDir, 'preview.html'), preview);
  console.log(`Rendered ${files.length} slides → ${path.relative(process.cwd(), outDir)}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
