// "24 men and a tree" (Buttonwood Agreement 1792 → May Day 1975). Collage reel spec; see ../../_engine/collage.js
const I = (n) => `../../img/${n}.png`;
const NUM = (n,c) => `<span style="font:900 86px Inter;color:${c||"#fff"}">${n}</span>`;
window.REEL = {
  boards: [
    { line: 0, items: [
      { type: 'scrap', font: 'head', text: '1792', size: 170, x: 80, y: 330, at: { l: 0, w: '1792' }, rot: -3 },
      { type: 'html', html: '<div class="ticket">brokers<span class="n">24</span></div>', x: 680, y: 360, w: 320, at: { l: 0, w: 'twenty' }, rot: 4 },
      { type: 'img', src: I('tree'), x: 130, y: 640, w: 820, at: { l: 0, w: 'tree' }, rot: 0 },
      { type: 'scrap', text: 'the buttonwood agreement · wall street', size: 30, x: 80, y: 1390, at: { l: 0, w: 'deal' }, rot: -2 },
    ] },
    { line: 1, items: [
      { type: 'img', src: I('gents'), x: 90, y: 400, w: 900, at: { l: 1, w: 'each' }, rot: -1 },
      { type: 'stamp', text: 'first dibs', size: 60, color: '#004EBA', x: 620, y: 330, at: { l: 1, w: 'dibs' }, rot: 6 },
      { type: 'html', html: '<div class="card" style="font-size:42px;width:520px;text-align:center">minimum fee<br><span style="font:900 120px Inter;letter-spacing:-.04em">0.25%</span><br>nobody charges less</div>', x: 280, y: 1080, at: { l: 1, w: 'fixed' }, rot: -4 },
    ] },
    { line: 2, items: [
      { type: 'html', html: '<div class="ticket">the fee rule lasted<span class="n">0</span>years</div>', x: 80, y: 360, w: 920, at: { l: 2, w: 'hundred' }, rot: -2, count: { from: 0, to: 183, dur: 0.9 } },
      { type: 'head', text: '1792 <i>→</i> 1975', size: 140, x: 80, y: 760, at: { l: 2, w: 'until' }, rot: 0 },
      { type: 'stamp', text: 'ended 1 may 1975', size: 70, x: 150, y: 1050, at: { l: 2, w: '1975' }, rot: -6 },
      { type: 'scrap', text: 'sources: buttonwood agreement (17 may 1792) · SEC “may day” (1 may 1975)', size: 20, x: 80, y: 1500, at: { l: 2, w: 'until' }, rot: 0 },
    ] },
    { line: 3, items: [
      { type: 'head', text: 'fees fell.<br><i>the middlemen stayed.</i>', size: 86, x: 80, y: 330, w: 940, at: { l: 3, w: 'fallen' }, rot: 0 },
      { type: 'html', html: '<div class="card" style="font-size:42px;background:#7ED116"><b>you</b></div>', x: 80, y: 640, at: { l: 3, w: 'middlemen' }, rot: -3 },
      { type: 'html', html: '<div class="card" style="font-size:42px">a broker</div>', x: 300, y: 790, at: { l: 4, w: 'broker' }, rot: 3 },
      { type: 'html', html: '<div class="card" style="font-size:42px">a fund house</div>', x: 110, y: 950, at: { l: 4, w: 'fund' }, rot: -2 },
      { type: 'html', html: '<div class="card" style="font-size:42px">a custodian</div>', x: 340, y: 1110, at: { l: 4, w: 'custodian' }, rot: 2 },
      { type: 'html', html: '<div class="card" style="font-size:42px;background:#EC464D;color:#fff"><b>your money</b></div>', x: 130, y: 1290, at: { l: 4, w: 'holding' }, rot: -3 },
      { type: 'img', src: I('banker'), x: 700, y: 640, w: 330, at: { l: 4, w: 'someone' }, rot: 3 },
    ] },
    { line: 5, items: [
      { type: 'scrap', text: 'warren buffett’s advice for most people:', size: 32, x: 80, y: 340, at: { l: 5, w: 'warren' }, rot: -2 },
      { type: 'head', text: 'skip the <span class=hl>expensive managers.</span>', size: 92, x: 80, y: 460, w: 940, at: { l: 5, w: 'skip' }, rot: 0 },
      { type: 'head', text: 'own a cheap <i>index fund.</i>', size: 92, x: 80, y: 700, w: 940, at: { l: 5, w: 'own' }, rot: 0 },
      { type: 'img', src: I('typewriter'), x: 300, y: 930, w: 600, at: { l: 5, w: 'advice' }, rot: 3 },
      { type: 'scrap', text: 'paraphrased from his berkshire hathaway shareholder letters', size: 20, x: 80, y: 1500, at: { l: 5, w: 'skip' }, rot: 0 },
    ] },
    { line: 6, items: [
      { type: 'head', text: 'now: <span class=hl>nobody</span> in the middle.', size: 92, x: 80, y: 340, w: 940, at: { l: 6 }, rot: 0 },
      { type: 'html', html: '<div class="card" style="font-size:42px;background:#7ED116"><b>you</b></div>', x: 80, y: 640, at: { l: 6, w: 'index' }, rot: -3 },
      { type: 'arrow', dx: 240, dy: 0, bend: 30, x: 230, y: 660, at: { l: 6, w: 'money' } },
      { type: 'html', html: '<div class="card" style="font-size:42px;background:#EC464D;color:#fff"><b>your money</b></div>', x: 540, y: 640, at: { l: 6, w: 'money' }, rot: 2 },
      { type: 'scrap', text: 'the rules are<br>written in code', size: 40, x: 80, y: 880, at: { l: 6, w: 'rules' }, rot: -3 },
      { type: 'img', src: I('phone'), x: 560, y: 820, w: 460, at: { l: 6, w: 'code' }, rot: 4 },
      { type: 'tile', icon: 'eye', bg: '#16181D', label: 'anyone can check', x: 140, y: 1160, at: { l: 6, w: 'check' }, rot: -4 },
    ] },
    { line: 7, items: [
      { type: 'head', text: 'how many middlemen sit between you and <i>your money?</i>', size: 90, x: 80, y: 340, w: 930, at: { l: 7, w: 'how' }, rot: 0 },
      { type: 'tile', icon: NUM(1), bg: '#16181D', x: 80, y: 900, at: { l: 7, w: 'count' }, rot: -5 },
      { type: 'tile', icon: NUM(2), bg: '#004EBA', x: 270, y: 930, at: { l: 7, w: 'count', o: 0.15 }, rot: 4 },
      { type: 'tile', icon: NUM(3), bg: '#16181D', x: 460, y: 890, at: { l: 7, w: 'count', o: 0.3 }, rot: -3 },
      { type: 'tile', icon: NUM(4), bg: '#004EBA', x: 650, y: 935, at: { l: 7, w: 'count', o: 0.45 }, rot: 6 },
      { type: 'tile', icon: NUM('?', '#111'), bg: '#7ED116', x: 840, y: 900, at: { l: 7, w: 'them' }, rot: -4 },
      { type: 'scrap', text: 'count them ↓', bg: '#7ED116', size: 52, x: 90, y: 1180, at: { l: 7, w: 'comments' }, rot: -5 },
    ] },
  ],
  endHtml: '<div class="h">same boring index.<br>no one holding it <i style="font-family:Instrument Serif;font-weight:400">for you.</i></div><div class="f">follow @blok.capital</div><div class="d">educational content only, not financial or investment advice. investing involves risk and you can lose money; on-chain assets can be volatile. images and voice are AI-generated.</div>',
};
