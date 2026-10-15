// node cover.mjs <out.jpg>: presenter frame (shot A) with the title card, no caption
import path from 'node:path'; import { pathToFileURL, fileURLToPath } from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const { chromium } = await import('playwright');
const b = await chromium.launch().catch(() => chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }));
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(pathToFileURL(path.join(dir, 'scene.built.html')).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.evaluate(() => { window.draw(0.9); const t = document.getElementById('title'); t.style.opacity = 1; t.style.transform = ''; t.style.top = '1180px'; document.getElementById('cap').textContent = ''; document.getElementById('flash').style.opacity = 0; });
await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 });
await b.close();
