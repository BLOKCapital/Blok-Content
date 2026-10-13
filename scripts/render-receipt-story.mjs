#!/usr/bin/env node
// Growth "receipt" Story card (1080x1920): node scripts/render-receipt-story.mjs <n> <followers> <goal> <out.jpg>
import { chromium } from 'playwright';
import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
const [,, n, followers, goal, out] = process.argv;
const logo = `data:image/png;base64,${(await readFile('brand/assets/logo-wordmark.png')).toString('base64')}`;
const pct = Math.min(100, Math.round(followers / goal * 100));
const html = `<html><head><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Inter:wght@500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet"><style>
body{margin:0;width:1080px;height:1920px;background:#004EBA;color:#fff;font-family:Inter,sans-serif;display:flex;flex-direction:column;padding:150px 96px 140px;box-sizing:border-box}
.k{font:800 34px Montserrat;letter-spacing:.16em;color:#7DD2FD;display:flex;justify-content:space-between}
.bar{width:120px;height:12px;background:#7ED116;border-radius:6px;margin:120px 0 50px}
h1{font:900 104px/1.02 Montserrat;margin:0}
.big{font:900 300px/1 Montserrat;color:#7ED116;margin:50px 0 0}
.of{font:800 64px Montserrat;margin-top:10px}
.track{height:28px;background:rgba(255,255,255,.18);border-radius:14px;margin:60px 0 18px;overflow:hidden}.fill{height:100%;width:${pct}%;background:#7ED116}
.m{font:500 34px 'JetBrains Mono',monospace;color:#CFE6FF;display:flex;justify-content:space-between}
p{font:600 46px/1.3 Inter;margin:80px 0 0}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center}.foot img{height:70px;background:#F6F3E8;border-radius:14px;padding:12px 18px}
.foot span{font:800 40px Montserrat}
</style></head><body>
<div class="k"><span>GROWTH RECEIPT #${n}</span><span>${new Date().toISOString().slice(0,10)}</span></div>
<div class="bar"></div>
<h1>We post our numbers in public.</h1>
<div class="big">${followers}</div><div class="of">followers · goal ${goal} by Sunday</div>
<div class="track"><div class="fill"></div></div><div class="m"><span>${pct}% there</span><span>${goal - followers} to go</span></div>
<p>Know someone who invests in funds or ETFs? Send them this. One plain-English money lesson a day.</p>
<div class="foot"><img src="${logo}"><span>@blok.capital</span></div>
</body></html>`;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.setContent(html); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
const png = out.replace(/\.jpg$/, '.png'); await p.screenshot({ path: png }); await b.close();
execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', png, '-q:v', '2', out]);
console.log('wrote', out);
