// "The know-nothing investor" (Buffett, 1993 letter). Collage reel spec; see ../../_engine/collage.js
const I = (n) => `../../img/${n}.png`;
const dots = (n, on) => '<div style="display:grid;grid-template-columns:repeat(5,150px);gap:20px">' + Array.from({ length: n }, (_, i) => `<div style="width:150px;height:150px;border-radius:30px;background:${i < on ? '#EC464D' : '#16181D'};display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 70 70" width="90" height="90"><circle cx="35" cy="22" r="11" fill="#fff"/><path d="M14 62c0-14 9-24 21-24s21 10 21 24Z" fill="#fff"/></svg></div>`).join('') + '</div>';
window.REEL = {
  boards: [
    { line: 0, items: [
      { type: 'scrap', font: 'head', text: '1993', size: 170, x: 80, y: 330, at: { l: 0, w: '1993' }, rot: -3 },
      { type: 'scrap', text: 'warren buffett’s<br>letter to shareholders', size: 30, x: 560, y: 380, at: { l: 0, w: 'buffett' }, rot: 3 },
      { type: 'img', src: I('typewriter'), x: 170, y: 560, w: 740, at: { l: 0, w: 'wrote' }, rot: -2 },
      { type: 'html', html: '<div class="card" style="font-size:40px;line-height:1.35;width:920px;min-height:330px"><span class="tw">“by periodically investing in an index fund, the know-nothing investor can actually out-perform most investment professionals.”</span></div>', x: 80, y: 1050, at: { l: 1 }, typeOnLine: 1, rot: 1 },
      { type: 'scrap', text: 'source: berkshire hathaway shareholder letter, 1993', size: 20, x: 80, y: 1500, at: { l: 1 }, rot: 0 },
    ] },
    { line: 2, items: [
      { type: 'head', text: 'the <span class=hl>know-nothing</span> investor.', size: 98, x: 80, y: 340, w: 940, at: { l: 2, w: 'know' }, rot: 0 },
      { type: 'img', src: I('calm'), x: 70, y: 660, w: 450, at: { l: 2, w: 'investor' }, rot: -3 },
      { type: 'img', src: I('stressed'), x: 560, y: 720, w: 470, at: { l: 2, w: 'genius' }, rot: 4 },
      { type: 'scrap', text: 'not the genius', size: 34, x: 600, y: 640, at: { l: 2, w: 'genius' }, rot: -3 },
      { type: 'tile', icon: 'cross', bg: '#EC464D', size: 110, x: 900, y: 1180, at: { l: 2, w: 'screens' }, rot: 8 },
      { type: 'scrap', text: 'six screens', size: 34, x: 620, y: 1320, at: { l: 2, w: 'screens' }, rot: 2 },
    ] },
    { line: 3, items: [
      { type: 'scrap', text: 'the data kept agreeing.', size: 40, x: 520, y: 1220, at: { l: 3 }, rot: 3 },
      { type: 'head', text: '<span class=hl>9 in 10</span>', size: 190, x: 80, y: 330, at: { l: 3, w: 'nine' }, rot: -2 },
      { type: 'html', html: dots(10, 9), x: 80, y: 640, at: { l: 3, w: 'nine' }, rot: 0, noShadow: true },
      { type: 'scrap', text: 'actively managed US large-company funds<br>that trailed the S&amp;P 500 over 15 years', size: 30, x: 80, y: 1050, at: { l: 3, w: 'trailed' }, rot: -1 },
      { type: 'scrap', text: 'source: S&amp;P SPIVA U.S. scorecard, year-end 2024 (89.5%)', size: 20, x: 80, y: 1500, at: { l: 3, w: 'trailed' }, rot: 0 },
    ] },
    { line: 4, items: [
      { type: 'head', text: 'nobody wants <i>complexity.</i>', size: 100, x: 80, y: 340, w: 940, at: { l: 4, w: 'people' }, rot: 0 },
      { type: 'html', html: '<svg id="tangle" width="900" height="300"></svg>', x: 90, y: 600, at: { l: 4, w: 'complexity' }, rot: 0, noShadow: true },
      { type: 'scrap', text: 'what most people want:', size: 34, x: 80, y: 940, at: { l: 4, w: 'want', o: 0.0 }, rot: -2 },
      { type: 'tile', icon: 'pie', bg: '#7DD2FD', label: 'diversified', size: 190, x: 90, y: 1060, at: { l: 4, w: 'diversified' } },
      { type: 'tile', icon: 'pct', bg: '#16181D', label: 'low cost', size: 190, x: 445, y: 1060, at: { l: 4, w: 'low' } },
      { type: 'tile', icon: 'hourglass', bg: '#F6F3E8', label: 'set &amp; forget', size: 190, x: 800, y: 1060, at: { l: 4, w: 'forget' } },
    ] },
    { line: 5, items: [
      { type: 'head', text: 'ready-made baskets that <span class=hl>rebalance themselves</span>', size: 86, x: 80, y: 340, w: 940, at: { l: 5 }, rot: 0 },
      { type: 'img', src: I('phone'), x: 540, y: 720, w: 480, at: { l: 5, w: 'baskets' }, rot: 3 },
      { type: 'tile', icon: 'basket', bg: '#7DD2FD', x: 110, y: 760, at: { l: 5, w: 'baskets' }, rot: -6 },
      { type: 'stamp', text: 'coming soon', size: 64, color: '#004EBA', x: 80, y: 1000, at: { l: 5, w: 'coming' }, rot: -7 },
      { type: 'tile', icon: 'lock', bg: '#7ED116', label: 'only you control it', x: 190, y: 1220, at: { l: 5, w: 'control' }, rot: 4 },
    ] },
    { line: 6, items: [
      { type: 'head', text: 'be <i>honest.</i>', size: 120, x: 80, y: 330, at: { l: 6 }, rot: -2 },
      { type: 'img', src: I('stressed'), x: 60, y: 620, w: 470, at: { l: 6, w: 'genius' }, rot: -4 },
      { type: 'scrap', text: 'the genius', size: 40, x: 120, y: 1240, at: { l: 6, w: 'genius' }, rot: 3 },
      { type: 'img', src: I('calm'), x: 570, y: 600, w: 440, at: { l: 6, w: 'know' }, rot: 3 },
      { type: 'scrap', text: 'the know-nothing', size: 40, bg: '#7ED116', x: 600, y: 1240, at: { l: 6, w: 'know' }, rot: -3 },
      { type: 'scrap', text: 'comment ↓', size: 48, x: 380, y: 1390, at: { l: 6, w: 'know', o: 0.4 }, rot: 2 },
    ] },
  ],
  endHtml: '<div class="h">the know-nothing investor<br>deserves better <i style="font-family:Instrument Serif;font-weight:400">plumbing.</i></div><div class="f">follow @blok.capital</div><div class="d">educational content only, not financial or investment advice. past performance doesn’t guarantee future results; investing involves risk and you can lose money. ready-made baskets are planned, not live yet. images and voice are AI-generated.</div>',
};
// tangle → circle doodle (from the "investing for dummies" carousel)
document.addEventListener('DOMContentLoaded', () => {
  const svg = document.getElementById('tangle'); if (!svg) return;
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const pts = []; const cx = 250, cy = 150;
  for (let i = 0; i < 90; i++) { const a = rnd() * Math.PI * 2, r = 30 + rnd() * 120, ry = r * (0.75 + rnd() * 0.3); pts.push([cx + Math.cos(a) * r + (rnd() - .5) * 30, cy + Math.sin(a) * ry * .9 + (rnd() - .5) * 30]); }
  pts.push([400, 200]); pts.push([520, 120]);
  for (let i = 0; i <= 4 * 48; i++) { const a = Math.PI * 1.05 + i / 48 * Math.PI * 2, r = 120 + Math.sin(i * .09) * 5; pts.push([700 + Math.cos(a) * r, 150 + Math.sin(a) * r]); }
  const cat = (p) => { let d = `M${p[0][0]} ${p[0][1]}`; for (let i = 0; i < p.length - 1; i++) { const p0 = p[i - 1] || p[i], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2] || p2, t = .5; d += ` C${p1[0] + (p2[0] - p0[0]) * t / 3} ${p1[1] + (p2[1] - p0[1]) * t / 3} ${p2[0] - (p3[0] - p1[0]) * t / 3} ${p2[1] - (p3[1] - p1[1]) * t / 3} ${p2[0]} ${p2[1]}`; } return d; };
  svg.innerHTML = `<path d="${cat(pts)}" fill="none" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`;
});
