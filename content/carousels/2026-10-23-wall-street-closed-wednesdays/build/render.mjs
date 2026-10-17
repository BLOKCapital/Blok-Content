// node render.mjs still <t> <out.png>   |   node render.mjs frames <dir> <fps> <seconds>
import { chromium } from 'playwright';
import path from 'node:path'; import fs from 'node:fs';
const [mode, a, b, c] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 5400, height: 1440 } });
await page.goto('file://' + path.resolve(path.dirname(new URL(import.meta.url).pathname), 'scene.html'));
await page.evaluate(() => window.ready);
await page.waitForTimeout(300);
if (mode === 'still') {
  await page.evaluate(t => window.draw(t), Number(a));
  await page.screenshot({ path: b });
} else {
  fs.mkdirSync(a, { recursive: true });
  const fps = Number(b), n = Math.round(fps * Number(c));
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.draw(t), i / fps);
    await page.screenshot({ path: path.join(a, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
}
await browser.close();
