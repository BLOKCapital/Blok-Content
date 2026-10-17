import { chromium } from 'playwright'; import path from 'node:path';
const [scene,out]=process.argv.slice(2);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(scene)); await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>{window.draw(window.LINES[8].end+0.2);const st=document.getElementById('story');st.style.opacity=.22;st.style.filter='blur(3px)';
 const h=document.getElementById('hook');h.style.opacity=1;h.style.transform='none';});
await p.screenshot({path:out,type:'jpeg',quality:90}); await b.close();
