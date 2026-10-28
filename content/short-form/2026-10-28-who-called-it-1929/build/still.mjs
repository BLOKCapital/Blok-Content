import { chromium } from 'playwright'; import path from 'node:path';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + path.resolve('scene.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
await p.evaluate(() => { window.draw(17.0); ['qA','qB','qC'].forEach(i => document.getElementById(i).style.borderColor = 'transparent'); document.getElementById('cap').style.display = 'none'; document.getElementById('guess').style.display = 'none'; });
await p.screenshot({ path: '../x-image-abc.png', clip: { x: 0, y: 180, width: 1080, height: 1180 } }); await b.close();
