// "Sticker" carousel style: grid-paper background, heavy geometric headline with a marker highlight,
// big outlined sticker visuals (emoji / icons / images), hand-drawn arrows and doodles, Share/Save footer.
// Used by scripts/render-carousel.mjs when slides.json has "style": "sticker".
// Style guide and slide schema: brand/carousel-style.md.

const esc = (s = '') =>
  String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

// **word** → lime marker highlight, __word__ → coral underline, \n → line break.
const rich = (s = '') =>
  esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<span class="mk">$1</span>')
    .replace(/__(.+?)__/g, '<span class="ul">$1</span>')
    .replace(/\n/g, '<br>');

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;800;900&family=Noto+Color+Emoji&display=block');
*{box-sizing:border-box;margin:0;padding:0}
body{background:#222}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;color:#0B1B2B;font-family:Montserrat,sans-serif;
  background-color:#FDFCF7;
  background-image:linear-gradient(#ECE7D8 2px,transparent 2px),linear-gradient(90deg,#ECE7D8 2px,transparent 2px);
  background-size:68px 68px;background-position:-2px -2px}
.slide.dark{background-color:#004EBA;color:#F6F3E8;
  background-image:linear-gradient(rgba(255,255,255,.08) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.08) 2px,transparent 2px)}
.hdr{position:absolute;left:56px;top:46px;display:flex;align-items:center;gap:18px}
.hdr img{width:78px;height:78px;border-radius:50%;background:#fff;object-fit:cover;border:3px solid #0B1B2B}
.hdr b{display:block;font-weight:800;font-size:30px;line-height:1.1}
.hdr span{font-weight:500;font-size:24px}
.hatch{position:absolute;right:-30px;top:-20px;width:300px;height:220px}
.txt{position:absolute;left:60px;right:60px;top:210px}
.kick{font-weight:800;font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:#844947;margin-bottom:18px}
.dark .kick{color:#7DD2FD}
h1{font-weight:900;font-size:96px;line-height:1.02;letter-spacing:-2px}
h2{font-weight:900;font-size:76px;line-height:1.04;letter-spacing:-1.5px}
.sub{font-weight:500;font-size:46px;line-height:1.2;margin-top:18px}
.body{font-weight:500;font-size:40px;line-height:1.3;margin-top:26px;max-width:900px}
.mk{position:relative;z-index:0;white-space:nowrap}
.mk::before{content:'';position:absolute;z-index:-1;left:-10px;right:-14px;top:52%;bottom:-4%;background:#7ED116;
  transform:rotate(-1.5deg) skewX(-8deg);border-radius:6px 22px 8px 18px}
.dark .mk::before{background:#7ED116;opacity:.9}
.ul{text-decoration:underline;text-decoration-color:#EC464D;text-decoration-thickness:9px;text-underline-offset:10px}
.list{list-style:none;margin-top:26px;display:flex;flex-direction:column;gap:20px}
.list li{font-weight:600;font-size:44px;line-height:1.2;display:flex;gap:18px}
.list li::before{content:'•';font-weight:900}
.vis{position:absolute;line-height:1;text-align:center}
.vis .e{font-family:'Noto Color Emoji';display:block}
.vis .e,.vis img,.vis svg{filter:drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 -7px 0 #fff)
  drop-shadow(5px 0 0 #7ED116) drop-shadow(-5px 0 0 #7ED116) drop-shadow(0 5px 0 #7ED116) drop-shadow(0 -5px 0 #7ED116)
  drop-shadow(0 22px 30px rgba(11,27,43,.18))}
.vis img{display:block}
.doodle{position:absolute;left:0;top:0;width:1080px;height:1350px;pointer-events:none;overflow:visible}
.flow{margin-top:34px;display:flex;flex-direction:column;gap:0}
.step{display:flex;align-items:center;gap:26px;background:#fff;border:4px solid #0B1B2B;border-radius:26px;padding:16px 28px;width:max-content;
  box-shadow:8px 8px 0 #0B1B2B}
.step .e{font-family:'Noto Color Emoji';font-size:62px}
.step b{font-weight:800;font-size:40px}
.step small{display:block;font-weight:500;font-size:26px;color:#5B5B5B}
.down{font-size:46px;font-weight:900;margin:6px 0 6px 52px;color:#844947}
.cmp{position:absolute;left:60px;right:60px;top:430px;display:grid;grid-template-columns:1fr 1fr;gap:26px}
.col{border-radius:30px;padding:34px 30px;border:4px solid #0B1B2B;background:#fff;box-shadow:8px 8px 0 #0B1B2B}
.col.new{background:#004EBA;color:#fff}
.col .e{font-family:'Noto Color Emoji';font-size:90px;line-height:1}
.col h3{font-weight:900;font-size:40px;margin:14px 0 18px}
.col p{font-weight:600;font-size:31px;line-height:1.25;margin-bottom:14px}
.btn{display:inline-block;margin-top:40px;background:#EC464D;color:#fff;font-weight:900;font-size:44px;padding:28px 50px;border-radius:999px;
  border:4px solid #0B1B2B;box-shadow:8px 8px 0 #0B1B2B}
.ftr{position:absolute;left:56px;right:56px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:38px}
.ftr span{display:flex;align-items:center;gap:14px}
.disc{position:absolute;left:60px;right:60px;bottom:118px;font-weight:500;font-size:20px;line-height:1.35;color:#844947}
.dark .disc{color:#CFE6FF}
.pg{position:absolute;right:60px;top:70px;font-weight:800;font-size:26px;color:#844947}
.dark .pg{color:#CFE6FF}
`;

const HATCH = `<svg class="hatch" viewBox="0 0 300 220" fill="none" stroke="#7ED116" stroke-width="9" stroke-linecap="round">
  <path d="M40 30 L150 200"/><path d="M110 10 L230 200"/><path d="M180 0 L290 170"/>
  <path d="M30 120 L280 40"/><path d="M60 190 L300 110"/></svg>`;

const SHARE = `<svg width="44" height="40" viewBox="0 0 24 22"><path d="M14 2l9 8-9 8v-5c-6 0-10 2-13 7 1-7 5-12 13-13z" fill="currentColor"/></svg>`;
const SAVE = `<svg width="32" height="40" viewBox="0 0 16 20"><path d="M1 1h14v18l-7-5-7 5z" fill="currentColor"/></svg>`;

// Hand-drawn arrow from [x1,y1] to [x2,y2]; bend pushes the control point sideways; loop adds a curl.
function arrow({ from, to, bend = 120, loop = false, color }, dark) {
  const [x1, y1] = from, [x2, y2] = to;
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
  const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
  const cx = mx - (dy / len) * bend, cy = my + (dx / len) * bend;
  const ang = Math.atan2(y2 - cy, x2 - cx);
  const h = 34, a1 = ang + Math.PI - 0.45, a2 = ang + Math.PI + 0.45;
  const stroke = color || (dark ? '#F6F3E8' : '#0B1B2B');
  let d = `M${x1} ${y1} Q${cx} ${cy} ${x2} ${y2}`;
  if (loop) {
    const lx = cx, ly = cy;
    d = `M${x1} ${y1} Q${x1} ${ly} ${lx} ${ly} q40 -10 30 30 q-20 30 -40 0 Q${lx + 20} ${ly + 60} ${x2} ${y2}`;
  }
  return `<path d="${d}" fill="none" stroke="${stroke}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M${x2 + h * Math.cos(a1)} ${y2 + h * Math.sin(a1)} L${x2} ${y2} L${x2 + h * Math.cos(a2)} ${y2 + h * Math.sin(a2)}"
      fill="none" stroke="${stroke}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
}

// Short "excitement" strokes around a point.
function burst([cx, cy], r = 260, dark) {
  const stroke = dark ? '#F6F3E8' : '#0B1B2B';
  return [-150, -110, -70, -30, 20]
    .map((deg) => {
      const a = (deg * Math.PI) / 180;
      return `<path d="M${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r} L${cx + Math.cos(a) * (r + 60)} ${cy + Math.sin(a) * (r + 60)}"
        stroke="${stroke}" stroke-width="9" stroke-linecap="round"/>`;
    })
    .join('');
}

function visual(v, assets) {
  if (!v) return '';
  const size = v.size || 420;
  const pos = `left:${v.x ?? 1080 - size - 60}px;top:${v.y ?? 1350 - size - 150}px;transform:rotate(${v.rotate || 0}deg)`;
  let inner = '';
  if (v.emoji) inner = `<span class="e" style="font-size:${size}px">${v.emoji}</span>`;
  else if (v.img) inner = `<img src="${assets.image(v.img)}" style="width:${size}px">`;
  return `<div class="vis" style="${pos}">${inner}${v.label ? `<div style="font-weight:800;font-size:34px;margin-top:18px">${esc(v.label)}</div>` : ''}</div>`;
}

function body(s) {
  const kick = s.kicker ? `<div class="kick">${rich(s.kicker)}</div>` : '';
  switch (s.type) {
    case 'hook':
      return `<div class="txt">${kick}<h1>${rich(s.title)}</h1>${s.sub ? `<div class="sub">${rich(s.sub)}</div>` : ''}</div>`;
    case 'list':
      return `<div class="txt">${kick}<h2>${rich(s.title)}</h2><ul class="list">${(s.items || []).map((i) => `<li><span>${rich(i)}</span></li>`).join('')}</ul></div>`;
    case 'flow':
      return `<div class="txt">${kick}<h2>${rich(s.title)}</h2><div class="flow">${(s.steps || [])
        .map((st, i) => `${i ? '<div class="down">↓</div>' : ''}<div class="step"><span class="e">${st.emoji || ''}</span><div><b>${esc(st.label)}</b>${st.note ? `<small>${esc(st.note)}</small>` : ''}</div></div>`)
        .join('')}</div></div>`;
    case 'compare':
      return `<div class="txt">${kick}<h2>${rich(s.title)}</h2></div><div class="cmp">${[['old', s.left], ['new', s.right]]
        .map(([k, c]) => `<div class="col ${k}"><span class="e">${c?.emoji || ''}</span><h3>${esc(c?.label || '')}</h3>${(c?.items || []).map((i) => `<p>${k === 'old' ? '✕' : '✓'} ${rich(i)}</p>`).join('')}</div>`)
        .join('')}</div>`;
    case 'cta':
      return `<div class="txt">${kick}<h2>${rich(s.title)}</h2>${s.body ? `<div class="body">${rich(s.body)}</div>` : ''}${s.button ? `<div class="btn">${esc(s.button)}</div>` : ''}</div>`;
    case 'point':
    default:
      return `<div class="txt">${kick}<h2>${rich(s.title)}</h2>${s.body ? `<div class="body">${rich(s.body)}</div>` : ''}</div>`;
  }
}

export function stickerPages(spec, assets) {
  const slides = spec.slides || [];
  return slides.map((s, i) => {
    const dark = s.theme === 'dark';
    const disclaimer = s.disclaimer === true ? spec.disclaimer : s.disclaimer;
    const doodles = [
      ...(s.arrows || (s.arrow ? [s.arrow] : [])).map((a) => arrow(a, dark)),
      s.visual?.burst ? burst(s.visual.burst, s.visual.burstR, dark) : '',
    ].join('');
    const save = s.type === 'hook' ? '' : `<span>Save it ${SAVE}</span>`;
    return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>
      <div class="slide ${dark ? 'dark' : ''}">
        ${s.type === 'hook' ? HATCH : `<div class="pg">${i + 1}/${slides.length}</div>`}
        <div class="hdr"><img src="${assets.mark}"><div><b>${esc(spec.handle || '@blok.capital')}</b><span>${esc(spec.tagline || 'On-chain investing, explained')}</span></div></div>
        ${body(s)}
        ${visual(s.visual, assets)}
        <svg class="doodle" viewBox="0 0 1080 1350">${doodles}</svg>
        ${disclaimer ? `<div class="disc">${esc(disclaimer)}</div>` : ''}
        <div class="ftr"><span>Share it ${SHARE}</span>${save}</div>
      </div></body></html>`;
  });
}
