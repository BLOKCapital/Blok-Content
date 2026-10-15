// "The first index fund had one customer" (Wells Fargo for Samsonite's pension, 1971). Collage reel spec; see ../../_engine/collage.js
const I = (n) => `../../img/${n}.png`;
const usd = (v) => '$' + Math.round(v).toLocaleString('en-US');
const NUM = (n,c) => `<span style="font:900 72px Inter;color:${c||"#fff"}">${n}</span>`;
window.REEL = {
  boards: [
    { line: 0, items: [
      { type: 'head', text: 'the first index fund ever built had', size: 92, x: 80, y: 340, w: 940, at: { l: 0, w: 'first' }, rot: 0 },
      { type: 'html', html: '<div class="ticket" style="text-align:center;font-size:40px">customers<span class="n" style="font-size:300px">1</span></div>', x: 270, y: 640, w: 540, at: { l: 0, w: 'one' }, rot: -3 },
      { type: 'scrap', text: 'exactly.', bg: '#7ED116', size: 56, x: 640, y: 1240, at: { l: 0, w: 'customer' }, rot: 5 },
    ] },
    { line: 1, items: [
      { type: 'scrap', font: 'head', text: '1971', size: 170, x: 80, y: 330, at: { l: 1, w: '1971' }, rot: -3 },
      { type: 'img', src: I('banker'), x: 60, y: 580, w: 400, at: { l: 1, w: 'bank' }, rot: -2 },
      { type: 'html', html: '<div class="ticket" style="background:#7ED116">one portfolio<span class="n">$0</span></div>', x: 480, y: 560, w: 540, at: { l: 1, w: 'six' }, rot: 3, count: { from: 0, to: 6000000, dur: 0.8, fmt: usd } },
      { type: 'img', src: I('suitcase'), x: 600, y: 860, w: 360, at: { l: 1, w: 'luggage' }, rot: 6 },
      { type: 'scrap', text: 'one client: a luggage<br>company’s pension fund', size: 34, x: 80, y: 1320, at: { l: 1, w: 'pension' }, rot: -2 },
      { type: 'scrap', text: 'wells fargo for samsonite’s pension fund · source: jason zweig (2016)', size: 20, x: 80, y: 1500, at: { l: 1, w: 'pension' }, rot: 0 },
    ] },
    { line: 2, items: [
      { type: 'head', text: 'regular <i>people?</i>', size: 120, x: 80, y: 340, at: { l: 2, w: 'regular' }, rot: -1 },
      { type: 'img', src: I('crowd'), x: 50, y: 600, w: 980, at: { l: 2, w: 'people' }, rot: 0 },
      { type: 'stamp', text: 'waited 5 years', size: 70, x: 200, y: 1250, at: { l: 2, w: 'five' }, rot: -6 },
    ] },
    { line: 3, items: [
      { type: 'head', text: 'new money ideas start <i>at the top.</i>', size: 86, x: 80, y: 340, w: 940, at: { l: 3, w: 'new' }, rot: 0 },
      { type: 'html', html: '<div class="card" style="background:#16181D;color:#F6F3E8;font-size:40px"><b>big players</b></div>', x: 80, y: 620, at: { l: 3, w: 'big' }, rot: -3 },
      { type: 'arrow', dx: 260, dy: 200, bend: -60, x: 280, y: 700, at: { l: 3, w: 'reach' } },
      { type: 'html', html: '<div class="card" style="background:#7ED116;font-size:40px"><b>everyone else</b></div>', x: 520, y: 900, at: { l: 3, w: 'everyone' }, rot: 3 },
      { type: 'head', text: 'then it’s <span class=hl>normal.</span>', size: 110, x: 80, y: 1160, at: { l: 3, w: 'normal' }, rot: -1 },
    ] },
    { line: 4, items: [
      { type: 'scrap', text: 'buffett’s advice, for everyone else:', size: 34, x: 80, y: 340, at: { l: 4, w: 'buffett' }, rot: -2 },
      { type: 'head', text: 'own a cheap, broad index.', size: 96, x: 80, y: 470, w: 940, at: { l: 4, w: 'own' }, rot: 0 },
      { type: 'head', text: '<i>leave it alone.</i>', size: 120, x: 80, y: 720, at: { l: 4, w: 'leave' }, rot: 0 },
      { type: 'img', src: I('calm'), x: 520, y: 880, w: 460, at: { l: 4, w: 'alone' }, rot: 3 },
      { type: 'scrap', text: 'paraphrased from his berkshire hathaway shareholder letters', size: 20, x: 80, y: 1500, at: { l: 4, w: 'own' }, rot: 0 },
    ] },
    { line: 5, items: [
      { type: 'head', text: 'on-chain portfolios are at their <span class=hl>1971</span> moment.', size: 86, x: 80, y: 340, w: 940, at: { l: 5, w: 'on' }, rot: 0 },
      { type: 'img', src: I('phone'), x: 580, y: 700, w: 440, at: { l: 5, w: 'right' }, rot: 4 },
      { type: 'scrap', text: 'the real test:', size: 34, x: 80, y: 720, at: { l: 6, w: 'real' }, rot: -3 },
      { type: 'html', html: '<div class="card" style="font-size:52px;line-height:1.1">can <b>you</b><br>use it?</div>', x: 80, y: 820, at: { l: 6, w: 'whether' }, rot: 2 },
      { type: 'tile', icon: 'sprout', bg: '#7ED116', label: 'start small', x: 110, y: 1140, at: { l: 6, w: 'small' }, rot: -5 },
      { type: 'tile', icon: 'lock', bg: '#F6F3E8', label: 'only you control it', x: 380, y: 1200, at: { l: 6, w: 'control' }, rot: 4 },
    ] },
    { line: 7, items: [
      { type: 'head', text: 'would you have bought the first index fund in <i>1976?</i>', size: 88, x: 80, y: 340, w: 940, at: { l: 7, w: 'would' }, rot: 0 },
      { type: 'tile', icon: '<span style="font:900 64px Inter;color:#111">yes</span>', bg: '#7ED116', size: 220, x: 160, y: 860, at: { l: 7, w: 'bought' }, rot: -6 },
      { type: 'tile', icon: '<span style="font:900 64px Inter;color:#fff">no</span>', bg: '#EC464D', size: 220, x: 640, y: 880, at: { l: 7, w: '1976' }, rot: 5 },
      { type: 'scrap', text: 'be honest ↓', size: 52, x: 330, y: 1220, at: { l: 7, w: 'honest' }, rot: -3 },
    ] },
  ],
  endHtml: '<div class="h">index investing started<br>with one client.<br>next, it’s <i style="font-family:Instrument Serif;font-weight:400">yours.</i></div><div class="f">follow @blok.capital</div><div class="d">educational content only, not financial or investment advice. investing involves risk and you can lose money; on-chain assets can be volatile. images and voice are AI-generated.</div>',
};
