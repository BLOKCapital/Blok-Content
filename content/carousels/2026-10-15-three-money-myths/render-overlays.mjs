// Renders the 5 text overlays (transparent PNG, 1080x1440). With --preview <photo>, also a preview over that photo.
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const HERE = dirname(fileURLToPath(import.meta.url));
const { chromium } = await import(pathToFileURL(join(HERE, "../../../node_modules/playwright/index.mjs")).href);
const prev = process.argv.indexOf("--preview");
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const pg = await b.newPage({ viewport: { width: 1080, height: 1440 } });
await pg.goto(pathToFileURL(join(HERE, "overlays.html")).href);
await pg.evaluate(() => document.fonts.ready);
for (let i = 0; i < 5; i++) {
  await pg.evaluate(([i]) => window.show(i), [i]);
  await pg.screenshot({ path: join(HERE, "overlays", `o${i + 1}.png`), omitBackground: true });
  if (prev > 0) { await pg.evaluate(([i, bg]) => window.show(i, bg), [i, pathToFileURL(process.argv[prev + 1]).href]); await pg.screenshot({ path: join(process.argv[prev + 2], `p${i + 1}.jpg`), type: "jpeg", quality: 80 }); }
}
await b.close();
