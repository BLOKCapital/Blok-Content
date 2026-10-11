import { chromium } from 'playwright';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
const [scene, outdir, ...ts] = process.argv.slice(2);
let b; try { b = await chromium.launch(); } catch { b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.log('ERR', e.message));
await p.goto(pathToFileURL(path.resolve(scene)).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
console.log('DURATION', await p.evaluate(() => window.DURATION));
if (ts[0] === 'cues') { console.log(JSON.stringify(await p.evaluate(() => window.CUES))); }
else for (const t of ts) { await p.evaluate(t => window.draw(t), +t); await p.screenshot({ path: `${outdir}/f-${t}.png` }); }
await b.close();
