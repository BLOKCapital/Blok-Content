import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/overlays.html'); await p.evaluate(()=>document.fonts.ready);
for (const id of ['hook','notif','aside','end']) {
  await p.evaluate(id=>{document.querySelectorAll('.layer').forEach(e=>e.classList.toggle('on',e.id===id))},id);
  await p.waitForTimeout(150);
  await p.screenshot({path:`ov-${id}.png`, omitBackground:true});
}
await b.close();
