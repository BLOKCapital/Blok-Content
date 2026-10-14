const {chromium}=require('playwright');(async()=>{const [,,html,out,dur,fps]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+html);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
const N=Math.round(+dur*+fps);for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/+fps);await p.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.png`});}
await b.close();})();
