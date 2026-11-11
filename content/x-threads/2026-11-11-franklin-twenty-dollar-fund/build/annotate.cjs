const { chromium } = require('playwright');
const fs=require('fs');
// in-page helpers
const helpers = `
window.wrap = (phrase, cls) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while ((n = w.nextNode())) {
    const i = n.nodeValue.indexOf(phrase);
    if (i >= 0 && n.parentElement.offsetParent !== null) {
      const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + phrase.length);
      const s = document.createElement('span'); s.className = cls; r.surroundContents(s); return s;
    }
  }
  throw new Error('not found: ' + phrase);
};
window.arrow = (el, side, len=110) => {
  const r = el.getBoundingClientRect(); const sx = scrollX, sy = scrollY;
  let x2, y2, x1, y1;
  if (side==='left'){ x2=r.left+sx-14; y2=r.top+sy+r.height/2; x1=x2-len; y1=y2+len*0.55; }
  if (side==='hright'){ x2=r.right+sx+16; y2=r.top+sy+r.height/2; x1=x2+len; y1=y2-8; }
  if (side==='right'){ x2=r.right+sx+14; y2=r.top+sy+r.height/2; x1=x2+len; y1=y2+len*0.5; }
  if (side==='below'){ x2=r.left+sx+r.width*0.5; y2=r.bottom+sy+12; x1=x2+len*0.35; y1=y2+len; }
  if (side==='above'){ x2=r.left+sx+r.width*0.5; y2=r.top+sy-12; x1=x2-len*0.35; y1=y2-len; }
  const ns='http://www.w3.org/2000/svg';
  let svg=document.getElementById('annsvg');
  if(!svg){svg=document.createElementNS(ns,'svg');svg.id='annsvg';svg.style.cssText='position:absolute;left:0;top:0;pointer-events:none;z-index:99999;overflow:visible';svg.setAttribute('width',document.documentElement.scrollWidth);svg.setAttribute('height',document.documentElement.scrollHeight);document.body.appendChild(svg);}
  const ang=Math.atan2(y2-y1,x2-x1), h=30;
  const p=document.createElementNS(ns,'path');
  p.setAttribute('d',\`M\${x1},\${y1} L\${x2},\${y2} M\${x2-h*Math.cos(ang-0.5)},\${y2-h*Math.sin(ang-0.5)} L\${x2},\${y2} L\${x2-h*Math.cos(ang+0.5)},\${y2-h*Math.sin(ang+0.5)}\`);
  p.setAttribute('stroke','#E01E2B');p.setAttribute('stroke-width','7');p.setAttribute('fill','none');p.setAttribute('stroke-linecap','round');p.setAttribute('stroke-linejoin','round');
  svg.appendChild(p);
};
`;
const css = `.annbox{outline:5px solid #E01E2B;outline-offset:2px;margin:0 9px;font-weight:700;color:#111!important}
.annul{text-decoration:underline;text-decoration-color:#E01E2B;text-decoration-thickness:5px;text-underline-offset:7px;font-weight:700;color:#111!important}`;

(async()=>{
 const b = await chromium.launch();
 const which = process.argv[2];
 const p = await b.newPage({viewport:{width:1100,height:1400},deviceScaleFactor:2});
 if (which==='ft'){
  await p.goto('https://www.franklintempleton.com/press-releases/news-room/2026/franklin-templeton-stellar-development-foundation-mark-five-years-of-benji-the-first-u.s.-registered-tokenized-money-market-fund',{waitUntil:'networkidle',timeout:90000});
  await p.waitForTimeout(3000);
  try{ await p.getByRole('button',{name:'Reject Non-Essential'}).click({timeout:8000}); }catch(e){console.log('no cookie btn')}
  await p.waitForTimeout(1000);
  await p.addStyleTag({content:css+` #onetrust-consent-sdk{display:none!important} p{line-height:1.95!important}`});
  await p.addScriptTag({content:helpers});
  await p.waitForTimeout(800);
  const res = await p.evaluate(()=>{
    const ct=[...document.querySelectorAll('*')].filter(x=>x.children.length<12 && /Contact us/.test(x.innerText||'') && x.innerText.length<200).pop();
    if(ct){ let k=ct; for(let i=0;i<4;i++){ if(k.getBoundingClientRect().height>150) break; k=k.parentElement;} k.style.visibility='hidden'; }
    const a=wrap('first U.S.-registered mutual fund to use a public blockchain','annul');
    const b2=wrap('launched in 2021','annbox');
    const c=wrap('365 days a year, including weekends and holidays','annbox');
    const d=wrap('grew by more than 140%','annbox');
    const e=wrap('$1.98 billion in AUM','annbox');
    const h=[...document.querySelectorAll('h1')].find(x=>x.innerText.includes('Five Years'));
    let hero=h; for(let i=0;i<6;i++){ if(hero.getBoundingClientRect().width>900) break; hero=hero.parentElement; }
    const hb=h.getBoundingClientRect();
    const ar=a.getClientRects()[0]; window.__a={x:ar.right, y:ar.top+scrollY+ar.height/2};
    const er=e.getBoundingClientRect();
    return {ax:window.__a.x, ay:window.__a.y, h1top:hb.top+scrollY, ebottom:er.bottom+scrollY, eright:er.right, ey:er.top+scrollY+er.height/2};
  });
  console.log(res);
  // horizontal arrow from right margin to $1.98B
  await p.evaluate((r)=>{
    const ns='http://www.w3.org/2000/svg'; let svg=document.getElementById('annsvg');
    if(!svg){svg=document.createElementNS(ns,'svg');svg.id='annsvg';svg.style.cssText='position:absolute;left:0;top:0;pointer-events:none;z-index:99999;overflow:visible';svg.setAttribute('width',document.documentElement.scrollWidth);svg.setAttribute('height',document.documentElement.scrollHeight);document.body.appendChild(svg);}
    const x2=r.eright+22, y=r.ey, x1=x2+150;
    const pth=document.createElementNS(ns,'path');
    pth.setAttribute('d',`M${x1},${y+14} Q${x1-60},${y} ${x2},${y} M${x2+26},${y-16} L${x2},${y} L${x2+26},${y+16}`);
    pth.setAttribute('stroke','#E01E2B');pth.setAttribute('stroke-width','7');pth.setAttribute('fill','none');pth.setAttribute('stroke-linecap','round');pth.setAttribute('stroke-linejoin','round');
    svg.appendChild(pth);
    const p2=pth.cloneNode(); const a2=r.ax+18, ay=r.ay, a1=a2+110;
    p2.setAttribute('d',`M${a1},${ay-40} Q${a1-30},${ay} ${a2},${ay} M${a2+26},${ay-16} L${a2},${ay} L${a2+26},${ay+16}`);
    svg.appendChild(p2);
  },res);
  fs.writeFileSync('ft_res.json',JSON.stringify(res));
  await p.screenshot({path:'ft_full_ann.png',fullPage:true});
 } else {
  await p.goto('https://forum.arbitrum.foundation/t/franklin-onchain-u-s-government-money-fund-fobxx-step-application/23655',{waitUntil:'domcontentloaded',timeout:90000});
  await p.waitForTimeout(6000);
  await p.addStyleTag({content:css+` .cooked{font-size:24px!important;line-height:1.7!important} .d-header,.timeline-container,.topic-timeline,#topic-progress-wrapper{display:none!important} .annbox{outline-width:5px} .arbmin{display:inline-block;white-space:nowrap}`});
  await p.addScriptTag({content:helpers});
  await p.waitForTimeout(800);
  const res = await p.evaluate(()=>{
    const t=wrap('Franklin OnChain U.S. Government Money Fund (FOBXX) STEP Application','x0');
    const m=wrap('The minimum initial investment is $20.','annbox arbmin');
    const n=wrap('Franklin Templeton Digital Assets','annul');
    arrow(m,'hright',150);
    const g=r=>{const b=r.getBoundingClientRect();return {top:b.top+scrollY,bottom:b.bottom+scrollY,left:b.left,right:b.right}};
    const ua=wrap('Underlying asset','x1'); const ai=wrap('The AUM of Franklin Templeton is $1.6 Trillion','annul');
    const post=m.closest('.cooked'); 
    return {title:g(t),name:g(n),min:g(m),ua:g(ua),ai:g(ai),post:g(post)};
  });
  console.log(JSON.stringify(res));
  fs.writeFileSync('arb_res.json',JSON.stringify(res));
  await p.screenshot({path:'arb_full_ann.png',fullPage:true,clip:{x:0,y:0,width:1100,height:1800}});
 }
 await b.close();
})();
