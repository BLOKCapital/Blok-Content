// Screenshot a collage reel at given times, or each board as a finished still.
//   node preview.mjs <scene.html> <outdir> times 1.2 5 9.5     → <outdir>/t-<t>.jpg (1080x1920)
//   node preview.mjs <scene.html> <outdir> cover <board>         → <outdir>/cover.jpg (1080x1920 Reel cover)
//   node preview.mjs <scene.html> <outdir> stills <n>           → <outdir>/still-<i>.jpg (1080x1350 crop for X)
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [scene, out, mode, ...rest] = process.argv.slice(2);
const { chromium } = await import('playwright');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const url = pathToFileURL(path.resolve(scene)).href;
if (mode === 'times') {
  await page.goto(url, { waitUntil: 'networkidle' }); await page.evaluate(() => document.fonts.ready);
  for (const t of rest) { await page.evaluate((t) => window.draw(+t), t); await page.screenshot({ path: `${out}/t-${t}.jpg`, quality: 80 }); }
} else if (mode === 'cover') {
  await page.goto(url + '?still=' + rest[0], { waitUntil: 'networkidle' }); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200);
  await page.screenshot({ path: `${out}/cover.jpg`, quality: 90 });
} else {
  for (let i = 0; i < +rest[0]; i++) {
    await page.goto(url + '?still=' + i, { waitUntil: 'networkidle' }); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200);
    await page.screenshot({ path: `${out}/still-${i + 1}.jpg`, quality: 92, clip: { x: 0, y: 285, width: 1080, height: 1350 } });
  }
}
await browser.close();
