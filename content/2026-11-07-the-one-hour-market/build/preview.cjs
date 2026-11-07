const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/scene.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const ts=process.argv.slice(2).map(Number);
for(const t of ts){await p.evaluate(t=>draw(t),t);await p.screenshot({path:`/tmp/claude-0/-home-user-Blok-Content/0d4b4adc-9ccd-5363-a510-19eee17e5681/scratchpad/pv_${t}.png`});}
await b.close();})();
