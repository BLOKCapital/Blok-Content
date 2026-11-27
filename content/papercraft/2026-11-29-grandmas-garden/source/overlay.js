const $=id=>document.getElementById(id);
const T=window.TIMELINE;window.DURATION=T[T.length-1].end+0.6+2.4;
const S=i=>T[i].start,E=i=>T[i].end;
const ease=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const back=x=>{x=Math.max(0,Math.min(1,x));const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const HOT=/^(grandma's|30|thirty|planting|start|blok|\$10|fund|7|grow|look)/i,RED=/^(waiting|bigger|isn't|promised)/i,BIGWORD=/^FUND$/;
const CH=[];T.forEach((L,i)=>{let cur=[];const push=()=>{if(cur.length){CH.push({line:i,ws:cur,s:cur[0].s-0.05});cur=[]}};
 L.words.forEach((w,k)=>{cur.push(w);const end=/[.,?!]$/.test(w.w);const left=L.words.length-k-1;if((end&&left!==1)||(cur.length>=3&&left>1&&!/^(a|the|of|to|in|for|and|who|so|her|his|on|at|with|from|was)$/i.test(w.w)))push()});push()});
CH.forEach((c,i)=>{const n=CH[i+1];c.e=n?n.s:window.DURATION;if(n&&n.line!==c.line)c.e=Math.min(c.e,E(c.line)+0.15)});
let ck=null,hk=false;
function drawText(t){const box=$('txt');
 if(t<E(0)+0.1){if(!hk){box.innerHTML='';T[0].text.split(' ').forEach(w=>{const sp=document.createElement('span');sp.className='w';const r=w.replace(/[.,?!:]$/,'');
   if(RED.test(r))sp.classList.add('red');else if(HOT.test(r))sp.classList.add('hot');sp.textContent=w.replace(/,$/,'');sp.style.fontSize='104px';box.appendChild(sp)});hk=true}
  return}
 if(hk){hk=false;box.innerHTML='';ck=null}
 const i=CH.findIndex(c=>t>=c.s&&t<c.e);if(i<0){box.innerHTML='';ck=null;return}
 const c=CH[i];if(i!==ck){box.innerHTML='';c.ws.forEach(w=>{const sp=document.createElement('span');sp.className='w';const r=w.w.replace(/[.,?!]$/,'');
  if(RED.test(r))sp.classList.add('red');else if(HOT.test(r))sp.classList.add('hot');if(c.line===T.length-1&&BIGWORD.test(r))sp.style.fontSize='130px';sp.textContent=w.w.replace(/[,]$/,'');sp.dataset.s=w.s;box.appendChild(sp)});ck=i}
 for(const sp of box.children){const p=cl((t-(+sp.dataset.s-0.04))/0.16);sp.style.opacity=p>0?1:0;sp.style.transform=`scale(${0.6+0.4*back(p)})`}}
// paper cards fold up like a hinge from their base
function card(id,t0,t1){const e=$(id);const p=cl((t-0)/1);}
function fold(id,t,t0,t1){const e=$(id);if(t<t0||t>t1){e.style.opacity=0;return}const p=cl((t-t0)/0.45),q=cl((t1-t)/0.3);const a=(1-back(p))*85+(1-q)*85;e.style.opacity=1;e.style.transform=`translateX(-50%) perspective(900px) rotateX(${a}deg)`}
// papercraft driver: step the fixed clock to t, raising each group at its beat
let pcT=0,sched=null;
function buildSched(){const G=window.REEL_GROUPS,out=[];const add=(arr,t0,spread)=>{const zs=arr.map(p=>p.z),z0=Math.min(...zs),z1=Math.max(...zs);arr.forEach(p=>out.push({p,t:t0+(z1>z0?(p.z-z0)/(z1-z0):0)*spread+p.jit*2}))};
 add(G.g0,0.05,0.3);add(G.g1,0.6,0.8);add(G.g3,S(2)-0.1,4.5);add(G.g2,S(3)+0.2,0.4);add(G.g4,S(5)-0.2,1.8);return out}
window.reelReset=function(){__papercraft.restart();for(const p of Object.values(window.REEL_GROUPS).flat()){p.pending=false;p.spring.reset(0)}
 // pieces not in any group (none) stay flat; sched
 sched=buildSched();sched.forEach(s=>s.done=false);pcT=0;window._fell=0;window._rose=0};
window.draw=function(t){
 if(!sched)reelReset();
 if(t<pcT){reelReset()}
 while(pcT<t-1e-6){const dt=Math.min(1/60,t-pcT);for(const s of sched)if(!s.done&&s.t<=pcT){s.p.spring.set(1);s.done=true}
   const all=Object.values(window.REEL_GROUPS).flat();if(!window._fell&&pcT>=S(6)-0.15){all.forEach(p=>{if(!window.REEL_GROUPS.g0.includes(p))p.spring.set(0)});window._fell=1}
   if(!window._rose&&pcT>=S(8)){all.forEach(p=>p.spring.set(1));window._rose=1}
   __papercraft.step(dt,1/dt);pcT+=dt}
 if(pcT===0)__papercraft.step(0);
 const li=Math.max(0,T.findIndex((L,i)=>t<(T[i+1]?T[i+1].start-0.3:1e9)));
 $('pill').textContent=li>=8?'TELL ME BELOW':"GRANDMA'S GARDEN";
 fold('c30',t,S(5)+0.2,E(5)+0.3);fold('cfund',t,S(7)+0.3,E(7)+0.2);fold('cq',t,S(8),E(8)+0.2);fold('cf',t,S(9),window.DURATION);
 $('logo').style.opacity=t>S(7)?1:0;
 drawText(t)};
