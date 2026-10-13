#!/usr/bin/env node
// Render an animated carousel scene (window.draw(t, staticSlide), window.TOTAL, 5 slides) to:
//   export/png/slide-NN.png (resting frames), export/jpg/, export/frames → export/full.mp4 (with music),
//   export/mp4/slide-NN.mp4 (per-slide video with the matching music segment, for Instagram video slides).
// node scripts/render-animated-carousel.mjs <scene.html> [music.m4a] [fps]
import { chromium } from 'playwright';
import { readFile, mkdir, rm } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
const [,, scene, music='assets/music/blok-morning-soil.m4a', fpsArg='30'] = process.argv;
const fps = +fpsArg, dir = path.dirname(path.resolve(scene)), out = path.join(dir, 'export');
for (const d of ['png','jpg','mp4','frames']) await mkdir(path.join(out,d), { recursive: true });
const logo = `data:image/png;base64,${(await readFile('brand/assets/logo-wordmark.png')).toString('base64')}`;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1440 } });
await p.goto('file://' + path.resolve(scene)); await p.waitForLoadState('networkidle');
await p.evaluate(async (l) => { window.setLogo(l); await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(()=>{}))); }, logo);
const total = await p.evaluate(() => window.TOTAL); const N = 5, per = total / N;
for (let i = 0; i < N; i++) {
  await p.evaluate((i) => window.draw(0, i), i);
  const f = path.join(out, 'png', `slide-0${i+1}.png`); await p.screenshot({ path: f });
  execFileSync('ffmpeg', ['-v','error','-y','-i',f,'-q:v','2',path.join(out,'jpg',`slide-0${i+1}.jpg`)]);
}
const frames = Math.round(total * fps);
for (let k = 0; k < frames; k++) {
  await p.evaluate((t) => window.draw(t), k / fps);
  await p.screenshot({ path: path.join(out, 'frames', `f${String(k).padStart(5,'0')}.jpg`), type: 'jpeg', quality: 92 });
}
await b.close();
execFileSync('ffmpeg', ['-v','error','-y','-framerate',String(fps),'-i',path.join(out,'frames','f%05d.jpg'),'-i',music,
  '-filter_complex',`[1:a]atrim=0:${total},afade=t=in:d=0.5,afade=t=out:st=${total-1.2}:d=1.2[a]`,'-map','0:v','-map','[a]',
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',path.join(out,'full.mp4')]);
for (let i = 0; i < N; i++) execFileSync('ffmpeg', ['-v','error','-y','-ss',String(i*per),'-t',String(per),'-i',path.join(out,'full.mp4'),
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',path.join(out,'mp4',`slide-0${i+1}.mp4`)]);
await rm(path.join(out,'frames'), { recursive: true });
console.log('done', total + 's');
