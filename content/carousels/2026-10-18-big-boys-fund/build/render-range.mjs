// node render-range.mjs <dir> <fps> <from> <to>   (frame indices, to exclusive)
import { chromium } from 'playwright';
import path from 'node:path'; import fs from 'node:fs';
const [dir, fps, from, to] = process.argv.slice(2).map((v,i)=>i?Number(v):v);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 5400, height: 1440 } });
await page.goto('file://' + path.resolve(path.dirname(new URL(import.meta.url).pathname), 'scene.html'));
await page.evaluate(() => window.ready);
await page.waitForTimeout(300);
fs.mkdirSync(dir, { recursive: true });
for (let i = from; i < to; i++) {
  const f = path.join(dir, `f${String(i).padStart(4, '0')}.jpg`);
  if (fs.existsSync(f)) continue;
  await page.evaluate(t => window.draw(t), i / fps);
  await page.screenshot({ path: f, type: 'jpeg', quality: 92 });
}
await browser.close();
