// node cover.mjs <t> <out.jpg> : renders scene.built.html at time t without captions -> 1080x1920 JPEG
import path from 'node:path'; import { pathToFileURL, fileURLToPath } from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const [t, out] = process.argv.slice(2);
const { chromium } = await import('playwright');
const b = await chromium.launch().catch(() => chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }));
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(pathToFileURL(path.join(dir, 'scene.built.html')).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.evaluate((t) => { window.draw(t); document.getElementById('cap').style.display = 'none'; document.getElementById('flash').style.opacity = 0; }, +t);
await p.screenshot({ path: out, type: 'jpeg', quality: 92 });
await b.close();
