const { chromium } = require('/home/claude/Blok-Content/node_modules/playwright');
const fs=require('fs');const S=JSON.parse(fs.readFileSync(__dirname+'/slides.json'));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1440}});
for(const s of S){await p.goto('file://'+__dirname+'/slide.html#'+encodeURIComponent(JSON.stringify(s)));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const tb=await p.evaluate(()=>{const t=document.querySelector('.txt');const r=t.getBoundingClientRect();return r.bottom});
console.log('slide',s.n,'text bottom',Math.round(tb),'panel top',s.panel[0]);
await p.screenshot({path:__dirname+`/layer-0${s.n}.png`,omitBackground:true});}
await b.close();})();
