// Render the 5 video slides (1080x1440) from the anatomy figure, plus stills and a full cut.
//   node render.mjs <music.m4a> <outDir> [--only=N] [--stills]
// Needs ../figure/ledger-figure.json (run ../figure/build.mjs first), playwright and ffmpeg.
import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "../../../..");
const { chromium } = await import(pathToFileURL(join(ROOT, "node_modules/playwright/index.mjs")).href);
const [music, outDir] = process.argv.slice(2);
const only = Number((process.argv.find((a) => a.startsWith("--only=")) || "=0").split("=")[1]);
const stillsOnly = process.argv.includes("--stills");
const FPS = 30, SECS = 6;
const fig = JSON.parse(readFileSync(join(HERE, "../figure/ledger-figure.json"), "utf8"));
const script = readFileSync(join(HERE, "dancing-script-latin-700-normal.woff2")).toString("base64");

// Each slide: text, a viewBox crop (from -> to, a slow push in), and the stretch of the model's cycle it plays.
const SLIDES = [
  { kicker: "Anatomy", head: 'How a public ledger <em>actually</em> works', sub: "The record behind on-chain finance, built as a machine you can see. Swipe to open it up.", from: [40, 10, 560, 426], to: [56, 24, 530, 403], t: [0, 6], lines: 2, edited: 1 },
  { kicker: "Part 1 · The box", head: "Every payment is a slip in a <em>box</em>", sub: "Entries are collected into a block: one sealed page of the ledger. When it's full, the press closes the lid.", from: [215, 96, 320, 243], to: [235, 112, 290, 220], t: [0, 6], lines: 2, edited: 1 },
  { kicker: "Part 2 · The seal", head: "Each seal <em>remembers</em> the one before", sub: "The seal is a fingerprint of this page plus the last page's seal. That's what couples the pages into one chain.", from: [60, 30, 400, 304], to: [80, 46, 370, 281], t: [0.2, 6.2], edited: 1, lines: 2 },
  { kicker: "Part 3 · The copies", head: "Change one page, and <em>everything</em> after it breaks", sub: "Edit an old entry and its seal stops matching. Every coupling after it comes loose, and the four other copies say no.", from: [50, -36, 540, 410], to: [64, -22, 512, 389], t: [6.2, 12.2], edited: 1, lines: 2 },
  { kicker: "Why it matters", head: "Receipts beat <em>reports</em>", sub: "Anyone can check the record, any time, instead of waiting for a statement. Newer tech has real trade-offs: learn first, start small.", from: [40, 10, 560, 426], to: [56, 24, 530, 403], t: [12.2, 18.2], edited: 1, cta: true, lines: 1 },
];

const css = `
@font-face{font-family:"Dancing Script";src:url(data:font/woff2;base64,${script}) format("woff2");font-weight:700}
*{box-sizing:border-box;margin:0}
html,body{width:1080px;height:1440px;overflow:hidden;background:#F6F3E8}
body{font-family:Inter,sans-serif;color:#0B1B2B;-webkit-font-smoothing:antialiased}
.frame{position:absolute;inset:0;padding:72px 80px}
.kicker{position:absolute;left:80px;top:72px;font-weight:600;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:#004EBA}
.marker{position:absolute;right:80px;top:72px;font-weight:500;font-size:24px;letter-spacing:.08em;color:#7d8794}
h1{position:absolute;left:80px;top:136px;width:900px;font-weight:800;font-size:76px;line-height:1.04;letter-spacing:-.025em}
h1 em{font-family:"Dancing Script";font-style:normal;font-weight:700;font-size:1.22em;color:#004EBA;letter-spacing:0;line-height:.8}
.sub{position:absolute;left:80px;width:860px;font-size:31px;line-height:1.38;color:#3b4656}
.stage{position:absolute;left:40px;top:500px;width:1000px;height:760px;overflow:hidden}
.iso[data-theme="light"]{--anatomy-weight:.75px;--anatomy-mid:#5d6675;--anatomy-lo:#8a8d88;--anatomy-faint:#c4bfae;--anatomy-shade-0:#d3cdb8;--anatomy-shade-1:#ddd8c6;--anatomy-shade-2:#e8e4d6;--anatomy-shade-3:#f1eee3}
.stage svg{width:1000px!important;height:760px!important;display:block;overflow:hidden}
.readout{position:absolute;left:80px;top:1262px;font:500 22px/1 ui-monospace,Menlo,monospace;color:#4a5563;letter-spacing:.02em}
.readout::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:#7ED116;margin-right:12px;vertical-align:1px}
.handle{position:absolute;left:80px;bottom:72px;font-weight:600;font-size:24px;color:#0B1B2B}
.next{position:absolute;right:80px;bottom:68px;font-weight:600;font-size:26px;color:#0B1B2B}
.next span{display:inline-block;margin-left:10px;color:#EC464D}
.cta{position:absolute;right:80px;bottom:60px;background:#004EBA;color:#fff;font-weight:700;font-size:26px;padding:16px 28px;border-radius:999px}
.disc{position:absolute;left:80px;bottom:132px;width:920px;font-size:18px;line-height:1.4;color:#7d8794}
.iso-plate-corner{display:none}
`;

function page(i) {
  const s = SLIDES[i];
  const subTop = 136 + s.lines * 82 + 34;
  const foot = s.cta
    ? `<div class="disc">Educational content only, not financial or investment advice. On-chain assets can be volatile and you can lose money.</div><div class="handle">Follow @blok.capital</div><div class="cta">Follow for plain-English money lessons</div>`
    : `<div class="handle">@blok.capital</div><div class="next">Swipe<span>→</span></div>`;
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fig.iso}${css}</style></head>
<body class="iso" data-theme="light">${fig.style}
<div class="frame"><div class="kicker">${s.kicker}</div><div class="marker">0${i + 1} / 05</div>
<h1>${s.head}</h1><div class="sub" style="top:${subTop}px">${s.sub}</div>
<div class="stage iso-stage">${fig.svg}</div>
<div class="readout" data-readout${s.cta ? ' style="display:none"' : ""}></div>${foot}</div>
<script>window.__recording = true;</script>
<script type="module">${(fig.kit + "\n" + fig.live).replace(/<\/(script)/gi, "<\\/$1")}
const svgEl = document.querySelector(".stage svg");
const S = ${JSON.stringify(s)};
const lerp = (a, b, f) => a + (b - a) * f;
const ease = (f) => f * f * (3 - 2 * f);
window.ledger.setEdited(S.edited);
let at = S.t[0] - 1.5;
window.frameAt = (sec) => {
  const target = S.t[0] + sec;
  while (at < target - 1e-6) { at = Math.min(target, at + 1 / ${FPS}); window.ledger.draw(at, 1 / ${FPS}); }
  const f = ease(Math.min(1, sec / ${SECS}));
  svgEl.setAttribute("viewBox", S.from.map((v, k) => lerp(v, S.to[k], f).toFixed(2)).join(" "));
};
window.ready = true;
</script></body></html>`;
}

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
mkdirSync(join(outDir, "video"), { recursive: true });
const parts = [];
for (let i = 0; i < SLIDES.length; i++) {
  if (only && only !== i + 1) continue;
  const html = join(outDir, `.slide-${i + 1}.html`);
  writeFileSync(html, page(i));
  const pg = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
  pg.on("pageerror", (e) => console.error("page error", e));
  await pg.goto(pathToFileURL(html).href);
  await pg.waitForFunction(() => window.ready);
  await pg.evaluate(() => document.fonts.ready);
  const still = join(outDir, `slide-0${i + 1}.jpg`);
  if (stillsOnly) { await pg.evaluate((s) => window.frameAt(s), SECS * 0.8); await pg.screenshot({ path: still, type: "jpeg", quality: 92 }); await pg.close(); continue; }
  const out = join(outDir, "video", `slide-0${i + 1}.mp4`);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-ss", String(i * SECS), "-t", String(SECS), "-i", music,
    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
    "-af", `afade=t=in:st=0:d=${i === 0 ? 0.6 : 0.25},afade=t=out:st=${SECS - 0.4}:d=0.4`, "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = 0; f < FPS * SECS; f++) {
    await pg.evaluate((s) => window.frameAt(s), f / FPS);
    const buf = await pg.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end();
  await pg.evaluate((s) => window.frameAt(s), SECS * 0.8); // the model only runs forward, so the still comes after the video
  await pg.screenshot({ path: still, type: "jpeg", quality: 92 });
  await new Promise((r) => ff.on("close", r));
  parts.push(out);
  console.log("slide", i + 1, "done");
  await pg.close();
}
await browser.close();

if (!only && !stillsOnly) {
  // one continuous cut for X / Reels, with the music unbroken
  const list = join(outDir, ".concat.txt");
  writeFileSync(list, parts.map((p) => `file '${p}'`).join("\n"));
  await new Promise((r) => spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list, "-an", "-c:v", "copy", join(outDir, ".silent.mp4")], { stdio: "inherit" }).on("close", r));
  await new Promise((r) => spawn("ffmpeg", ["-y", "-loglevel", "error", "-i", join(outDir, ".silent.mp4"), "-t", String(SECS * SLIDES.length), "-i", music, "-map", "0:v", "-map", "1:a",
    "-c:v", "copy", "-af", `afade=t=in:st=0:d=0.6,afade=t=out:st=${SECS * SLIDES.length - 1.5}:d=1.5`, "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", join(outDir, "full.mp4")], { stdio: "inherit" }).on("close", r));
  console.log("full cut done");
}
