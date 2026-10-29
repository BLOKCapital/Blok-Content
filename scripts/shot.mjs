// node scripts/shot.mjs <page.html> <out.jpg> <width> <height>
import path from 'node:path'; import { existsSync } from 'node:fs'; import { pathToFileURL } from 'node:url';
const [src,out,w,h]=process.argv.slice(2);
const { chromium } = await import('playwright');
let b; try{b=await chromium.launch();}catch(e){if(!existsSync('/opt/pw-browsers/chromium'))throw e;b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});}
const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto(pathToFileURL(path.resolve(src)).href,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:out,type:'jpeg',quality:92});await b.close();
