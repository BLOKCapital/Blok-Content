const { chromium } = require('playwright');
const fs=require('fs');
const helpers = fs.readFileSync('annotate.cjs','utf8').split('const helpers = `')[1].split('`;')[0].replace(/\\`/g,'`').replace(/\\\$/g,'$');
const css = `.annbox{outline:5px solid #E01E2B;outline-offset:2px;margin:0 8px;font-weight:700;color:#111!important}
.annul{text-decoration:underline;text-decoration-color:#E01E2B;text-decoration-thickness:5px;text-underline-offset:7px;font-weight:700;color:#111!important}`;
(async()=>{
 const b = await chromium.launch();
 const which=process.argv[2];
 const p = await b.newPage({viewport:{width:1000,height:1400},deviceScaleFactor:2});
 if(which==='pr'){
  await p.goto('https://protos.com/llm-crypto-trading-contest-finds-llms-cant-trade-crypto',{waitUntil:'domcontentloaded',timeout:60000});
  await p.waitForTimeout(6000);
  await p.addStyleTag({content:css+` p{line-height:1.9!important} .annbox,.annul{color:#fff!important}`});
  await p.evaluate(()=>{ [...document.querySelectorAll('div,section,aside')].filter(x=>/We use cookies/.test(x.innerText||'') && x.innerText.length<400).forEach(x=>x.style.display='none'); });
  await p.addScriptTag({content:helpers});
  const r=await p.evaluate(()=>{
   const g=e=>{const b=e.getBoundingClientRect();return {top:b.top+scrollY,bottom:b.bottom+scrollY,left:b.left,right:b.right}};
   const h=[...document.querySelectorAll('h1')].find(x=>x.innerText.includes('LLMs can'));
   const a=wrap('losing 63% of its funds','annbox'); wrap('less than the $10,000 they started with','annul'); wrap('$2,232','annbox');
   const c=wrap('Gemini made a total of 238 trades','annul');
   const d=wrap('ranged between 25 and 30%','annbox');
   const e=wrap('managed to double their money','annul');
   const f=wrap('PnL (profit and loss) was dominated by trading costs','annul');
   // remove "Read more" paragraph(s) between
   [...document.querySelectorAll('p')].filter(x=>x.innerText.startsWith('Read more')).forEach(x=>x.style.display='none');
   const ch=[...document.querySelectorAll('img')].find(x=>x.getBoundingClientRect().top+scrollY>a.getBoundingClientRect().top+scrollY && x.getBoundingClientRect().width>400);
   const cr=ch.getBoundingClientRect();
   const ns='http://www.w3.org/2000/svg'; const svg=document.createElementNS(ns,'svg'); svg.style.cssText='position:absolute;left:0;top:0;pointer-events:none;z-index:99999;overflow:visible'; svg.setAttribute('width',document.documentElement.scrollWidth); svg.setAttribute('height',document.documentElement.scrollHeight); document.body.appendChild(svg);
   const rx=cr.left+cr.width*0.805, ry=cr.top+scrollY+cr.height*0.50, rw=cr.width*0.165, rh=cr.height*0.37;
   const rc=document.createElementNS(ns,'rect'); rc.setAttribute('x',rx);rc.setAttribute('y',ry);rc.setAttribute('width',rw);rc.setAttribute('height',rh);rc.setAttribute('fill','none');rc.setAttribute('stroke','#E01E2B');rc.setAttribute('stroke-width','6'); svg.appendChild(rc);
   const x2=rx+rw+14, y=ry+rh*0.75, x1=x2+150;
   const pth=document.createElementNS(ns,'path'); pth.setAttribute('d',`M${x1},${y+30} Q${x1-50},${y} ${x2},${y} M${x2+26},${y-16} L${x2},${y} L${x2+26},${y+16}`); pth.setAttribute('stroke','#E01E2B');pth.setAttribute('stroke-width','7');pth.setAttribute('fill','none');pth.setAttribute('stroke-linecap','round');pth.setAttribute('stroke-linejoin','round'); svg.appendChild(pth);
   const cap=[...document.querySelectorAll('figcaption,p,div')].find(x=>(x.innerText||'').startsWith('Grok, ChatGPT, and Gemini were') && x.children.length<4);
   const lost=[...document.querySelectorAll('p')].find(x=>x.innerText.startsWith('ChatGPT lost $6,267'));
   const date=[...document.querySelectorAll('*')].find(x=>x.children.length==0 && /NOV 4, 2025/i.test(x.innerText||''));
   const last=[...document.querySelectorAll('p')].find(x=>x.innerText.startsWith('ChatGPT and Gemini, however'));
   return {cap:g(cap),lost:g(lost),h:g(h),date:date?g(date):null,last:g(last),col:g(a.closest('p'))};
  });
  console.log(JSON.stringify(r)); fs.writeFileSync('pr_res.json',JSON.stringify(r));
  await p.screenshot({path:'pr_ann.png',fullPage:true});
 } else {
  await p.goto('https://www.nof1.ai/',{waitUntil:'domcontentloaded',timeout:60000});
  await p.waitForTimeout(5000);
  await p.addStyleTag({content:css});
  await p.addScriptTag({content:helpers});
  const r=await p.evaluate(()=>{
   const g=e=>{const b=e.getBoundingClientRect();return {top:b.top+scrollY,bottom:b.bottom+scrollY,left:b.left,right:b.right}};
   const a=wrap('shockingly bad at navigating financial markets','annbox');
   const b2=wrap('showing minimal signs of improvement between releases','annul');
   const h=[...document.querySelectorAll('*')].find(x=>x.children.length==0 && (x.innerText||'').trim()==='Why markets');
   return {a:g(a),b:g(b2),h:h?g(h):null,par:g(a.closest('p')||a.parentElement)};
  });
  console.log(JSON.stringify(r)); fs.writeFileSync('nh_res.json',JSON.stringify(r));
  await p.screenshot({path:'nh_ann.png',fullPage:true});
 }
 await b.close();
})();
