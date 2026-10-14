// node preview.mjs t1 t2 ...  -> prev-<t>.png (overlay with alpha)
import { chromium } from '/home/claude/Blok-Content/node_modules/playwright/index.mjs';
import path from 'node:path';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + path.resolve('notes.html'));
await p.evaluate(() => window.ready);
for (const t of process.argv.slice(2)) {
  await p.evaluate((t) => window.draw(t), Number(t));
  await p.screenshot({ path: `prev-${t}.png`, omitBackground: true });
}
await b.close();
