// Collage reel engine for BLOK (1080x1920). Same look as the "investing for dummies" carousel:
// grey paper, faint logo watermark, grain, halftone cut-outs with white sticker edges, icon tiles,
// Space Mono body + Inter headings. Pieces slap onto the page one by one with a stop-motion feel,
// and each "board" (page) is built up in sync with the voiceover.
//
// A reel defines window.REEL = { boards: [{ line, items: [...] }], end: {...} } and loads timeline.js.
// Item timing: at: <line index> | { l: <line>, w: '<word>', o: <offset s> }.
// URL flags: ?still=<board index> renders that board fully built, without captions (for X images).

(function () {
  const TL = window.TIMELINE;
  const R = window.REEL;
  const q = new URLSearchParams(location.search);
  const STILL = q.has('still') ? +q.get('still') : null;
  const $ = (s) => document.querySelector(s);
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
  const S = (i) => TL[i].start;

  // word-level timings
  const words = [];
  TL.forEach((s, si) => {
    if (s.words) { s.words.forEach((w) => words.push({ ...w, si })); return; }
    const ws = s.text.split(/\s+/).filter(Boolean);
    const total = ws.reduce((n, w) => n + w.length + 2, 0);
    let acc = s.start;
    ws.forEach((w) => { const d = (s.end - s.start) * (w.length + 2) / total; words.push({ w, s: acc, e: acc + d, si }); acc += d; });
  });
  const W = (l, w) => {
    const hit = words.find((x) => x.si === l && norm(x.w).startsWith(norm(w)));
    if (!hit) { console.warn('word not found', l, w); return S(l); }
    return hit.s;
  };
  const T = (at) => (typeof at === 'number' ? S(at) : (at.w ? W(at.l, at.w) : S(at.l)) + (at.o || 0));

  const last = TL[TL.length - 1];
  const END_AT = last.end + 0.5;
  window.DURATION = Math.ceil((END_AT + (R.endHold || 3.2)) * 10) / 10;

  // board windows
  R.boards.forEach((b, i) => {
    b.t0 = i === 0 ? -1 : S(b.line) - 0.12;
    b.t1 = i < R.boards.length - 1 ? S(R.boards[i + 1].line) - 0.12 : END_AT;
  });

  // ---------- build DOM ----------
  let seed = 11;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const stage = $('#stage');

  function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  function place(e, it) {
    e.style.left = it.x + 'px'; e.style.top = it.y + 'px';
    if (it.w) e.style.width = it.w + 'px';
    if (it.h) e.style.height = it.h + 'px';
    if (it.z) e.style.zIndex = it.z;
  }

  const ICONS = {
    sprout: '<svg viewBox="0 0 70 70"><path d="M35 60V34" stroke="#2F5A06" stroke-width="6" stroke-linecap="round"/><path d="M35 36C35 22 26 14 12 14c0 14 9 22 23 22Z" fill="#2F5A06"/><path d="M35 30c0-12 8-19 22-19 0 12-8 19-22 19Z" fill="#2F5A06" opacity=".75"/></svg>',
    pct: '<svg viewBox="0 0 72 72"><path d="M16 56L56 16" stroke="#fff" stroke-width="7" stroke-linecap="round"/><circle cx="20" cy="20" r="9" fill="none" stroke="#fff" stroke-width="6.5"/><circle cx="52" cy="52" r="9" fill="none" stroke="#fff" stroke-width="6.5"/></svg>',
    pie: '<svg viewBox="0 0 70 70"><circle cx="35" cy="35" r="24" fill="#F6F3E8"/><path d="M35 35V11a24 24 0 0 1 20.8 36Z" fill="#004EBA"/><path d="M35 35L55.8 47A24 24 0 0 1 21 54.4Z" fill="#004EBA" opacity=".55"/></svg>',
    bars: '<svg viewBox="0 0 66 66"><g stroke="#fff" stroke-width="7" stroke-linecap="round"><path d="M12 52V22M25 52V30M38 52V14M51 52V36"/></g></svg>',
    hourglass: '<svg viewBox="0 0 70 70"><path d="M18 10h34M18 60h34M22 10c0 16 26 16 26 25S22 44 22 60M48 10c0 16-26 16-26 25s26 9 26 25" fill="none" stroke="#004EBA" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M28 56h14l-7-8Z" fill="#004EBA"/></svg>',
    lock: '<svg viewBox="0 0 70 70"><rect x="14" y="30" width="42" height="30" rx="7" fill="#111"/><path d="M23 30v-8a12 12 0 0 1 24 0v8" fill="none" stroke="#111" stroke-width="6.5"/><circle cx="35" cy="45" r="5" fill="#7ED116"/></svg>',
    eye: '<svg viewBox="0 0 70 70"><path d="M6 35s10-18 29-18 29 18 29 18-10 18-29 18S6 35 6 35Z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/><circle cx="35" cy="35" r="8" fill="#7ED116"/></svg>',
    basket: '<svg viewBox="0 0 70 70"><path d="M10 28h50l-6 30H16Z" fill="#004EBA"/><path d="M22 28l10-16M48 28L38 12" stroke="#004EBA" stroke-width="6" stroke-linecap="round"/><path d="M26 36v14M35 36v14M44 36v14" stroke="#F6F3E8" stroke-width="4" stroke-linecap="round"/></svg>',
    target: '<svg viewBox="0 0 70 70"><circle cx="35" cy="35" r="24" fill="none" stroke="#fff" stroke-width="6"/><circle cx="35" cy="35" r="12" fill="none" stroke="#fff" stroke-width="6"/><circle cx="35" cy="35" r="3" fill="#fff"/></svg>',
    trophy: '<svg viewBox="0 0 78 78"><path d="M22 12h34v14a17 17 0 0 1-34 0Z" fill="none" stroke="#004EBA" stroke-width="6" stroke-linejoin="round"/><path d="M22 18H12c0 10 5 15 11 16M56 18h10c0 10-5 15-11 16M39 43v12M27 64h24M31 56h16v8H31Z" fill="none" stroke="#004EBA" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    check: '<svg viewBox="0 0 70 70"><path d="M16 37l12 12 26-28" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    cross: '<svg viewBox="0 0 70 70"><path d="M18 18l34 34M52 18L18 52" stroke="#fff" stroke-width="8" stroke-linecap="round"/></svg>',
    person: '<svg viewBox="0 0 70 70"><circle cx="35" cy="22" r="11" fill="currentColor"/><path d="M14 62c0-14 9-24 21-24s21 10 21 24Z" fill="currentColor"/></svg>',
  };

  function makeItem(it) {
    let e;
    switch (it.type) {
      case 'img':
        e = el('img', 'it img'); e.src = it.src; break;
      case 'scrap': // torn paper strip with text
        e = el('div', 'it scrap ' + (it.font || 'mono'), it.text);
        if (it.bg) e.style.background = it.bg;
        if (it.color) e.style.color = it.color;
        if (it.size) e.style.fontSize = it.size + 'px';
        if (it.align) e.style.textAlign = it.align;
        if (it.pad) e.style.padding = it.pad;
        break;
      case 'head': // big heading, no paper
        e = el('div', 'it head', it.text);
        if (it.size) e.style.fontSize = it.size + 'px';
        if (it.align) e.style.textAlign = it.align;
        if (it.color) e.style.color = it.color;
        break;
      case 'stamp':
        e = el('div', 'it stamp', it.text);
        if (it.color) { e.style.color = it.color; e.style.borderColor = it.color; }
        if (it.size) e.style.fontSize = it.size + 'px';
        break;
      case 'tile':
        e = el('div', 'it tile', ICONS[it.icon] || it.icon);
        e.style.background = it.bg || '#16181D';
        if (it.size) { e.style.width = e.style.height = it.size + 'px'; }
        if (it.label) e.appendChild(el('div', 'tlabel', it.label));
        break;
      case 'tape':
        e = el('div', 'it tapebit'); break;
      case 'html':
        e = el('div', 'it', it.html); break;
      case 'arrow': { // hand-drawn arrow, from (0,0) to (dx,dy) inside its box
        const { dx, dy } = it; const w = Math.abs(dx) + 60, h = Math.abs(dy) + 60;
        const x0 = dx < 0 ? w - 30 : 30, y0 = dy < 0 ? h - 30 : 30, x1 = x0 + dx, y1 = y0 + dy;
        const mx = (x0 + x1) / 2 + (it.bend || 40), my = (y0 + y1) / 2 - (it.bend || 40);
        const a = Math.atan2(y1 - my, x1 - mx), L = 26;
        e = el('div', 'it', `<svg width="${w}" height="${h}"><path d="M${x0} ${y0}Q${mx} ${my} ${x1} ${y1}" fill="none" stroke="${it.color || '#111'}" stroke-width="5" stroke-linecap="round"/><path d="M${x1 - L * Math.cos(a - .5)} ${y1 - L * Math.sin(a - .5)}L${x1} ${y1}L${x1 - L * Math.cos(a + .5)} ${y1 - L * Math.sin(a + .5)}" fill="none" stroke="${it.color || '#111'}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`);
        it.noShadow = true; break;
      }
      case 'circle': // hand-drawn circle around something
        e = el('div', 'it', `<svg width="${it.w}" height="${it.h}" viewBox="0 0 ${it.w} ${it.h}"><path d="M${it.w * .52} ${it.h * .04}C${it.w * .95} ${it.h * .02} ${it.w * 1.0} ${it.h * .9} ${it.w * .5} ${it.h * .96}S${it.w * -.02} ${it.h * .55} ${it.w * .2} ${it.h * .15}" fill="none" stroke="${it.color || '#EC464D'}" stroke-width="7" stroke-linecap="round" stroke-dasharray="4000" stroke-dashoffset="4000"/></svg>`);
        it.draw = true; it.noShadow = true; break;
      case 'strike':
        e = el('div', 'it strike'); e.style.background = it.color || '#EC464D'; it.wipe = true; it.noShadow = true; break;
    }
    place(e, it);
    if (it.cls) e.classList.add(...it.cls.split(' '));
    if (it.noShadow) e.classList.add('flat');
    it.rot = it.rot != null ? it.rot : (rnd() - 0.5) * 6;
    it.seedA = rnd() * 10; it.seedB = rnd() * 10;
    it.el = e;
    return e;
  }

  R.boards.forEach((b, bi) => {
    const page = el('div', 'board');
    page.appendChild(el('div', 'paper'));
    b.items.forEach((it) => { page.appendChild(makeItem(it)); it.tAt = T(it.at != null ? it.at : b.line) + (it.d || 0); });
    stage.appendChild(page); b.el = page;
  });

  // end card
  const endB = el('div', 'board');
  endB.appendChild(el('div', 'paper'));
  endB.appendChild(el('div', 'endcard', R.endHtml || ''));
  stage.appendChild(endB);

  // ---------- animation ----------
  const step = (t, fps = 12) => Math.floor(t * fps) / fps; // stop-motion quantise
  const POP = [1.28, 0.9, 1.05, 1.0];

  function drawItem(it, t) {
    const e = it.el; const dt = t - it.tAt;
    if (dt < 0) { e.style.opacity = 0; return; }
    e.style.opacity = 1;
    const f = Math.floor(dt * 12);
    const s = it.wipe || it.draw ? 1 : (f < POP.length ? POP[f] : 1);
    const boil = it.still ? 0 : Math.sin(step(t, 6) * 7.3 + it.seedA) * 0.6;
    const bx = it.still ? 0 : Math.round(Math.sin(step(t, 6) * 5.1 + it.seedB));
    e.style.transform = `translate(${bx}px,0) rotate(${it.rot + boil}deg) scale(${s})`;
    if (it.wipe) e.style.clipPath = `inset(0 ${100 - clamp(step(dt, 24) / 0.35) * 100}% 0 0)`;
    if (it.draw) { const p = e.querySelector('path'); p.style.strokeDashoffset = 4000 - clamp(step(dt, 24) / 0.5) * 4000 * 0.75; }
    if (it.count) { // number ticker: {from,to,dur,fmt}
      const c = it.count; const k = clamp(step(dt, 15) / (c.dur || 1));
      const v = c.from + (c.to - c.from) * (1 - Math.pow(1 - k, 2));
      e.querySelector('.n').textContent = c.fmt ? c.fmt(v) : Math.round(v);
    }
    if (it.type === 'html' && (it.typeOn || it.typeOnLine != null)) {
      if (it.typeOnLine != null && !it.typeOn) it.typeOn = Math.max(0.5, TL[it.typeOnLine].end - TL[it.typeOnLine].start - 0.3); // typewriter text reveal on .tw children
      const tw = e.querySelector('.tw'); const full = tw.dataset.full || (tw.dataset.full = tw.textContent);
      const n = Math.floor(clamp(dt / it.typeOn) * full.length); tw.textContent = full.slice(0, n);
    }
  }

  // captions (label-maker tape)
  const cap = $('#cap');
  function captions(t) {
    if (STILL != null || t > END_AT) { cap.innerHTML = ''; return; }
    const si = TL.findIndex((s, i) => t >= s.start - 0.1 && t < (TL[i + 1] ? TL[i + 1].start - 0.1 : s.end + 0.4));
    if (si < 0) { cap.innerHTML = ''; return; }
    const ws = words.filter((w) => w.si === si);
    let cur = ws.findIndex((w) => t < w.e); if (cur < 0) cur = ws.length - 1;
    const start = Math.floor(cur / 5) * 5;
    cap.innerHTML = ws.slice(start, start + 5).map((w) => `<span class="${t >= w.s && t < w.e ? 'on' : ''}">${w.w.toLowerCase()}</span>`).join(' ');
  }

  window.draw = (t) => {
    let active = R.boards.findIndex((b) => t >= b.t0 && t < b.t1);
    const isEnd = t >= END_AT;
    R.boards.forEach((b, bi) => {
      const on = bi === active && !isEnd;
      b.el.style.display = on ? 'block' : 'none';
      if (!on) return;
      // page slap-in: first 3 frames slide up
      const k = clamp(step(t - b.t0, 12) / 0.25);
      b.el.style.transform = bi === 0 ? 'none' : `translateY(${(1 - k) * 140}px) rotate(${(1 - k) * 1.5}deg)`;
      b.items.forEach((it) => drawItem(it, t));
    });
    endB.style.display = isEnd ? 'block' : 'none';
    if (isEnd) { const k = clamp(step(t - END_AT, 12) / 0.25); endB.style.transform = `translateY(${(1 - k) * 140}px)`; }
    captions(t);
  };

  if (STILL != null) {
    const b = R.boards[STILL];
    b.items.forEach((it) => (it.still = true));
    const tEnd = Math.max(...b.items.map((it) => it.tAt)) + 1.2;
    document.body.classList.add('still');
    window.draw(Math.min(tEnd, b.t1 - 0.01));
  } else {
    window.draw(0);
  }
})();
