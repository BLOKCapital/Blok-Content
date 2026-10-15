// "They called it un-American" (Bogle's folly, 1976). Collage reel spec; see ../../_engine/collage.js
const I = (n) => `../../img/${n}.png`;
const usd = (v) => '$' + Math.round(v).toLocaleString('en-US');
window.REEL = {
  boards: [
    { line: 0, items: [
      { type: 'scrap', font: 'head', text: '1976', size: 170, x: 80, y: 330, at: { l: 0, w: '1976' }, rot: -3 },
      { type: 'tile', icon: 'target', bg: '#16181D', x: 760, y: 360, at: { l: 0, w: 'beat' } },
      { type: 'tile', icon: 'cross', bg: '#EC464D', size: 96, x: 870, y: 470, at: { l: 0, w: 'market' }, rot: 8 },
      { type: 'head', text: "a fund that didn't even try to <span class=hl>beat the market</span>", size: 86, x: 80, y: 640, w: 920, at: { l: 0, w: 'fund' }, rot: 0 },
      { type: 'img', src: I('trader'), x: 470, y: 960, w: 560, at: { l: 0, w: 'beat' } },
      { type: 'scrap', text: 'everyone else<br>was trying to', size: 32, x: 80, y: 1120, at: { l: 0, w: 'market', o: 0.25 }, rot: -4 },
    ] },
    { line: 1, items: [
      { type: 'img', src: I('laughing'), x: 160, y: 350, w: 760, at: { l: 1, w: 'laughed' }, rot: -2 },
      { type: 'scrap', font: 'serif', text: '“bogle’s folly”', size: 96, x: 120, y: 1100, at: { l: 1, w: 'folly' }, rot: 3 },
      { type: 'stamp', text: 'un-american', size: 88, x: 230, y: 1410, at: { l: 2, w: 'un' }, rot: -8 },
    ] },
    { line: 3, items: [
      { type: 'html', html: '<div class="ticket">the goal<span class="n">$150,000,000</span></div>', x: 80, y: 360, w: 920, at: { l: 3, w: 'hundred' }, rot: -2 },
      { type: 'html', html: '<div class="ticket" style="background:#7ED116">what came in<span class="n">$0</span></div>', x: 80, y: 700, w: 920, at: { l: 3, w: 'got' }, rot: 2, count: { from: 0, to: 11300000, dur: 0.8, fmt: usd } },
      { type: 'html', html: '<svg width="900" height="430"><rect x="120" y="20" width="250" height="360" fill="#004EBA"/><rect x="530" y="353" width="250" height="27" fill="#7ED116" stroke="#111" stroke-width="2"/><text x="245" y="420" text-anchor="middle" font-family="Space Mono" font-size="28">goal</text><text x="655" y="420" text-anchor="middle" font-family="Space Mono" font-size="28">raised</text></svg>', x: 90, y: 1030, w: 900, at: { l: 3, w: 'eleven' }, rot: 0, noShadow: true },
      { type: 'scrap', text: 'source: jason zweig, “bogle’s folly turns 40”', size: 20, x: 80, y: 1500, at: { l: 3, w: 'eleven' }, rot: 0 },
    ] },
    { line: 4, items: [
      { type: 'head', text: 'the idea was <i>boring.</i>', size: 112, x: 80, y: 360, w: 940, at: { l: 4, w: 'boring' }, rot: -1 },
      { type: 'tile', icon: 'basket', bg: '#7DD2FD', label: 'buy the whole market', x: 110, y: 640, at: { l: 4, w: 'whole' } },
      { type: 'tile', icon: 'pct', bg: '#16181D', label: 'keep costs low', x: 465, y: 640, at: { l: 4, w: 'costs' } },
      { type: 'tile', icon: 'hourglass', bg: '#F6F3E8', label: 'wait', x: 820, y: 640, at: { l: 4, w: 'wait' } },
      { type: 'img', src: I('calm'), x: 290, y: 900, w: 500, at: { l: 4, w: 'wait', o: 0.25 } },
    ] },
    { line: 5, items: [
      { type: 'scrap', text: 'end of 2023 · money in US funds', size: 40, x: 80, y: 340, at: { l: 5, w: 'end' }, rot: -2 },
      { type: 'html', html: '<div class="card" style="background:#7ED116;width:860px"><b>index funds</b> · ~$13.3 trillion</div>', x: 80, y: 470, at: { l: 5, w: 'index' }, rot: 0 },
      { type: 'html', html: '<div class="card" style="width:850px"><b>stock pickers</b> · ~$13.2 trillion</div>', x: 80, y: 600, at: { l: 5, w: 'stock' }, rot: 0 },
      { type: 'img', src: I('trader'), x: 600, y: 760, w: 430, at: { l: 5, w: 'pickers' }, rot: 4 },
      { type: 'head', text: '<span class=hl>boring</span><br>won.', size: 170, x: 80, y: 820, at: { l: 6, w: 'boring' }, rot: -2 },
      { type: 'scrap', text: 'source: morningstar, via hargreaves lansdown, 19 jan 2024', size: 20, x: 80, y: 1500, at: { l: 5, w: 'pickers' }, rot: 0 },
    ] },
    { line: 7, items: [
      { type: 'scrap', text: 'the next step?', size: 40, x: 600, y: 470, at: { l: 7 }, rot: 4 },
      { type: 'head', text: 'same boring playbook.<br><i>new home.</i>', size: 84, x: 80, y: 330, w: 940, at: { l: 7, w: 'same' }, rot: 0 },
      { type: 'img', src: I('phone'), x: 520, y: 560, w: 520, at: { l: 7, w: 'account' }, rot: 3 },
      { type: 'tile', icon: 'lock', bg: '#7ED116', x: 90, y: 600, at: { l: 7, w: 'control' }, rot: -6 },
      { type: 'html', html: '<div class="card" style="width:600px;font-size:28px"><div class="src" style="display:inline-block;margin-bottom:10px">public ledger · illustrative</div><br><b>your account</b><br>only you control it<br><br>07:02 · bought the basket ✓<br>07:03 · rebalanced ✓<br>now · every holding visible</div>', x: 70, y: 820, at: { l: 7, w: 'control' }, rot: -3 },
      { type: 'tile', icon: 'eye', bg: '#16181D', label: 'anyone can check', x: 160, y: 1330, at: { l: 7, w: 'check' }, rot: 5 },
    ] },
    { line: 8, items: [
      { type: 'head', text: 'what are we laughing at <i>today?</i>', size: 98, x: 80, y: 340, w: 920, at: { l: 8, w: 'laughing' }, rot: -1 },
      { type: 'scrap', text: 'that we’ll all be doing in 2076', size: 36, x: 80, y: 760, at: { l: 8, w: 'fifty' }, rot: 2 },
      { type: 'img', src: I('laughing'), x: 470, y: 900, w: 560, at: { l: 8, w: 'laughing' }, rot: 4 },
      { type: 'scrap', text: 'comment ↓', bg: '#7ED116', size: 52, x: 90, y: 1160, at: { l: 8, w: 'years', o: 0.3 }, rot: -5 },
    ] },
  ],
  endHtml: '<div class="h">boring is a feature.<br>now it can be <i style="font-family:Instrument Serif;font-weight:400">yours.</i></div><div class="f">follow @blok.capital</div><div class="d">educational content only, not financial or investment advice. investing involves risk and you can lose money; on-chain assets can be volatile. images and voice are AI-generated.</div>',
};
