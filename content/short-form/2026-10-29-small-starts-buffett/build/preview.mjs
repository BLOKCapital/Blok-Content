import { chromium } from 'playwright';
import path from 'node:path';
const ts = process.argv.slice(2).map(Number);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + path.resolve('scene.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
for (const t of ts) { await p.evaluate((t) => window.draw(t), t); await p.screenshot({ path: `/tmp/claude-0/pv-${t}.jpg`, type: 'jpeg', quality: 80 }); }
await b.close();
