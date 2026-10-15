// node preview.mjs <times comma> <outdir>  (also writes cues.json + typing.json)
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL, fileURLToPath } from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const html = readFileSync(path.join(dir, 'scene.html'), 'utf8').replace('__TIMING__', readFileSync(path.join(dir, 'timing.json'), 'utf8'));
writeFileSync(path.join(dir, 'scene.built.html'), html);
const [times, out] = process.argv.slice(2);
const { chromium } = await import('playwright');
const b = await chromium.launch().catch(() => chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }));
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(pathToFileURL(path.join(dir, 'scene.built.html')).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
const cues = await p.evaluate(() => window.CUES());
const dur = cues.duration; const typing = [];
for (let t = 0; t < dur; t += 1 / 30) if (await p.evaluate((t) => window.typingActive(t), t)) typing.push(+t.toFixed(3));
writeFileSync(path.join(dir, 'cues.json'), JSON.stringify({ ...cues, typing }));
if (times) for (const t of times.split(',')) { await p.evaluate((t) => window.draw(t), +t); await p.screenshot({ path: `${out}/f_${t}.jpg`, type: 'jpeg', quality: 80 }); }
await b.close(); console.log('duration', dur);
