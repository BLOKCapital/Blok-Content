// "Anyone" (1602 -> 2026): a pop-up paper story in four dioramas laid out left to right on one printed sheet.
// A: Amsterdam 1602 (canal houses, a ship, a queue of ordinary people at the subscription desk)
// B: the world map today (a walled US skyline, people on every other continent outside the gate)
// C: a phone lying on the page (an exchange, share cards and a growth chart fold up out of it)
// D: the world map again, people everywhere popping up with a phone, a small garden in the middle
// The camera dollies between them on the narration's timeline (timeline.js), captions are DOM overlays.
//
// PAPER SPEC
// BRIEF    history to today, money access; warm, editorial, a little playful; must: no logos, no text printed on cards
// SUBJECT  "anyone" growing from one canal city to the whole map; the reader looks at the people first
// STOCK    cream cardstock, quiet fibre
// PALETTE  ground linen #e4dcc4 / #d6cbb0, lead indigo #3d63a8, accents coral #d4594f + lime #93bf45, ink #2e1f18,
//          shadow tint warm umber #8a5a3a, water #6f9fb4
// LIGHT    warm key #ffe0b8 from upper left (-0.8, 0.95, 0.55), fill 1/4, shadow tint umber
// LENS     fov 26, pitch 47, dist 40-58, band ~40 %, blur 16 px
// FORMAT   1920x1080 X video, 30 fps, ~55 s
// MOTION   hinge rise per diorama on its line, stagger 0.05-0.1 s, camera dolly with ease
// LIFE     gulls over the canal, cloud shadows
import * as P2 from 'papercraft/lib/paperkit-2d.js';
import { createLife } from 'papercraft/lib/paper-life.js';
import { createHarness } from './harness.js';

const TL = window.TIMELINE || [];
const ls = (i, d) => (TL[i] ? TL[i].start : d);   // line start (s)
const le = (i, d) => (TL[i] ? TL[i].end : d);
const END = TL.length ? TL[TL.length - 1].end + 4.5 : 56;

const C = {
  ground: '#ddd3b8', wash: '#d3c8aa', washB: '#e2d9bf', quay: '#cdb48c', cobble: '#b89c74', water: '#6f9fb4', waterD: '#4f7f98', foam: '#eef0e6',
  sea: '#a9c4c9', seaD: '#8fb0b8', land: '#e9dcb6', landD: '#d2bf8e',
  indigo: '#3d63a8', indigoD: '#2c4a82', coral: '#d4594f', lime: '#93bf45', limeD: '#6f9a32', ochre: '#d6a24a', brick: '#a5553e', brickD: '#7e3f2f',
  slate: '#4e5f63', cream: '#f4ead2', ink: '#2e1f18', wood: '#9a6338', woodD: '#6e4426', skin: '#efcfaa', skinB: '#c99068', skinC: '#8d5a3b',
  glass: '#f2d27a', phone: '#2f2a30', screen: '#eef2ea',
};
const AX = -75, BX = -25, CX = 25, DX = 75;   // diorama centres (x); all near z = -6

const H = createHarness({ ground: C.ground, bounds: { x0: -118, x1: 118, z0: -48, z1: 34 }, view: { pitch: 47, dist: 52, target: [AX, 1.5, -5] },
  focus: [AX, 2, -5] });
const { flags } = H;
let rnd = P2.rng(11);
const D = P2.draw2, between = (a, b) => a + rnd() * (b - a);

// rise scheduling: the harness opens hinge k at 0.1 + order * 0.09 s
const ALLUP = new URLSearchParams(location.search).has('allup');
const orderAt = (t) => ALLUP ? 1 : Math.max(0, (t - 0.1) / 0.09);
let RISE = 0.3, STAG = 0;
const popup = (pts, paint, o = {}) => H.popup(pts, paint, { order: orderAt(RISE + STAG * (o.k ?? 0)), effects: 1, ...o });

// ---------------------------------------------------------------- shapes
const blob = (cx, cz, rx, rz, seed, n = 36, amp = 0.22) => { const r = P2.rng(seed), ph = [r() * 6, r() * 6, r() * 6]; return Array.from({ length: n }, (_, i) => { const a = i / n * Math.PI * 2, k = 1 + amp * (0.5 * Math.sin(a * 2 + ph[0]) + 0.3 * Math.sin(a * 3 + ph[1]) + 0.2 * Math.sin(a * 5 + ph[2])); return [cx + Math.cos(a) * rx * k, cz + Math.sin(a) * rz * k]; }); };
// continents in a map frame of width W centred on (mx, mz): rough, friendly, recognisable at a glance
const CONT = [
  ['na', -0.33, -0.2, 0.17, 0.2, 3], ['sa', -0.22, 0.2, 0.08, 0.2, 5], ['eu', -0.02, -0.25, 0.09, 0.1, 7], ['af', 0.0, 0.06, 0.1, 0.2, 9],
  ['as', 0.22, -0.2, 0.2, 0.18, 11], ['au', 0.33, 0.25, 0.08, 0.07, 13],
];
const mapPts = (mx, mz, W, Dd) => CONT.map(([id, u, v, ru, rv, s]) => [id, blob(mx + u * W, mz + v * Dd * 1.6, ru * W, rv * Dd * 1.6, s)]);
const contAt = (mx, mz, W, Dd, id) => { const c = CONT.find((q) => q[0] === id); return [mx + c[1] * W, mz + c[2] * Dd * 1.6]; };

// ---------------------------------------------------------------- the printed ground
const CANAL = { x0: AX - 32, x1: AX + 30, z: -2.2, w: 3.6 };
const canalPoly = (half) => { const top = [], bot = []; for (let x = CANAL.x0; x <= CANAL.x1; x += 1) { const wv = Math.sin(x * 0.21) * 0.25 + Math.sin(x * 0.07) * 0.4; top.push([x, CANAL.z - half + wv]); bot.push([x, CANAL.z + half + wv]); } return top.concat(bot.reverse()); };
const PHONE = { x: CX, z: -6, w: 15, d: 24 };
H.printGround(({ g, ppu, X, Z, rnd: r, washes, torn, drifts }) => {
  washes([C.wash, C.wash, C.washB, C.washB, C.wash]);
  // A: the quay, cobbles and the canal
  torn([[AX - 34, -14], [AX + 32, -14], [AX + 32, 14], [AX - 34, 14]], P2.rgba(C.quay, 0.55));
  for (let k = 0; k < 900; k++) { const x = AX - 32 + r() * 62, z = -12 + r() * 25; if (Math.abs(z - CANAL.z) < CANAL.w * 0.75) continue; g.fillStyle = P2.rgba(r() < 0.5 ? C.cobble : P2.shade(C.quay, 0.25), 0.45); D.rect(g, X(x), Z(z), (0.55 + r() * 0.3) * ppu, (0.35 + r() * 0.2) * ppu, 0.12 * ppu); }
  torn(canalPoly(CANAL.w * 0.7), '#efe5cc');
  torn(canalPoly(CANAL.w * 0.55), C.water, 'rgba(250,244,228,0.45)');
  for (let k = 0; k < 160; k++) { const x = CANAL.x0 + 1 + r() * (CANAL.x1 - CANAL.x0 - 2), z = CANAL.z + (r() - 0.5) * CANAL.w * 0.8, l = (0.5 + r() * 0.9) * ppu; g.strokeStyle = k % 3 ? P2.rgba(C.foam, 0.8) : P2.rgba(C.waterD, 0.7); g.lineWidth = 0.1 * ppu; g.beginPath(); g.moveTo(X(x) - l / 2, Z(z)); g.quadraticCurveTo(X(x), Z(z) - 0.1 * ppu, X(x) + l / 2, Z(z)); g.stroke(); }
  // B and D: two world maps printed on pale sea paper
  for (const mx of [BX, DX]) {
    const W = 44, Dd = 15, mz = -6;
    torn([[mx - W / 2 - 3, mz - 20], [mx + W / 2 + 3, mz - 20], [mx + W / 2 + 3, mz + 17], [mx - W / 2 - 3, mz + 17]], C.sea, 'rgba(250,246,232,0.8)');
    for (let k = 0; k < 140; k++) { const x = mx - W / 2 + r() * W, z = mz - 18 + r() * 33, l = (0.5 + r() * 0.8) * ppu; g.strokeStyle = P2.rgba(k % 2 ? '#e8f0ec' : C.seaD, 0.7); g.lineWidth = 0.09 * ppu; g.beginPath(); g.moveTo(X(x) - l / 2, Z(z)); g.quadraticCurveTo(X(x), Z(z) - 0.09 * ppu, X(x) + l / 2, Z(z)); g.stroke(); }
    for (const [id, pts] of mapPts(mx, mz, W, Dd)) {
      torn(pts, id === 'na' && mx === BX ? P2.mix(C.land, C.indigo, 0.18) : C.land, 'rgba(255,250,236,0.85)');
      g.fillStyle = P2.rgba(C.landD, 0.5); for (let q = 0; q < 26; q++) { const [px, pz] = pts[Math.floor(r() * pts.length)], c = contAt(mx, mz, W, Dd, id), t = 0.2 + r() * 0.6; D.ell(g, X(px + (c[0] - px) * t), Z(pz + (c[1] - pz) * t), 0.25 * ppu, 0.18 * ppu); }
    }
    g.strokeStyle = P2.rgba('#f7f2e2', 0.55); g.lineWidth = 0.08 * ppu;   // a faint graticule
    for (let x = mx - W / 2; x <= mx + W / 2; x += 7.3) { g.beginPath(); g.moveTo(X(x), Z(mz - 19)); g.lineTo(X(x), Z(mz + 16)); g.stroke(); }
    for (let z = mz - 17; z <= mz + 16; z += 6.5) { g.beginPath(); g.moveTo(X(mx - W / 2 - 2), Z(z)); g.lineTo(X(mx + W / 2 + 2), Z(z)); g.stroke(); }
  }
  // C: a phone lying on the page, screen up
  const { x, z, w, d } = PHONE;
  g.fillStyle = 'rgba(70,40,20,0.25)'; D.rect(g, X(x - w / 2 + 0.5), Z(z - d / 2 + 0.7), w * ppu, d * ppu, 2.2 * ppu);
  g.fillStyle = C.phone; D.rect(g, X(x - w / 2), Z(z - d / 2), w * ppu, d * ppu, 2.2 * ppu);
  g.fillStyle = '#4a434c'; D.rect(g, X(x - w / 2 + 0.15), Z(z - d / 2 + 0.15), (w - 0.3) * ppu, 0.5 * ppu, 0.25 * ppu);
  g.fillStyle = C.screen; D.rect(g, X(x - w / 2 + 0.9), Z(z - d / 2 + 1.4), (w - 1.8) * ppu, (d - 2.8) * ppu, 1.2 * ppu);
  g.fillStyle = P2.rgba(C.lime, 0.35); D.rect(g, X(x - w / 2 + 1.6), Z(z + d / 2 - 5.2), (w - 3.2) * ppu, 3.2 * ppu, 0.8 * ppu);
  g.fillStyle = P2.rgba(C.indigo, 0.22); for (let i = 0; i < 4; i++) D.rect(g, X(x - w / 2 + 1.6), Z(z + d / 2 - 8.6 + i * 0.85), (w - 3.2 - (i % 2) * 3) * ppu, 0.42 * ppu, 0.2 * ppu);
  g.fillStyle = '#1b171c'; D.rect(g, X(x - 1.6), Z(z - d / 2 + 0.55), 3.2 * ppu, 0.55 * ppu, 0.27 * ppu);
  drifts((px, py) => { if (r() < 0.8) { g.strokeStyle = P2.rgba(r() < 0.5 ? '#a99a70' : '#8f8a5a', 0.55); g.lineWidth = 1.4; g.beginPath(); g.moveTo(px, py); g.lineTo(px + (r() - 0.5) * 3, py - 4 - r() * 4); g.stroke(); } });
});

// ---------------------------------------------------------------- pieces
const plain = (c) => (P) => { P.gradient(P2.shade(c, 0.1), P2.shade(c, -0.1), 0.5); P.innerShade(P2.shade(c, -0.5), { alpha: 0.3, blurPx: 8 }); };
// a person: hat / cap variants, a coat or dress, arms, feet; opts.phone holds a lit phone
function person({ coat = C.indigo, trim = C.cream, skin = C.skin, hat = 'none', hatC = C.ink, apron = false, ruff = false, stripes = false, phone = false, dress = false } = {}) {
  return P2.drawnPiece((g, ink) => {
    g.fillStyle = ink('#3a2a1e'); D.rect(g, -0.26, 0, 0.22, 0.16, 0.06); D.rect(g, 0.04, 0, 0.22, 0.16, 0.06);
    if (!dress) { g.fillStyle = ink(P2.shade(coat, -0.35)); D.rect(g, -0.22, 0.1, 0.18, 0.7, 0.05); D.rect(g, 0.04, 0.1, 0.18, 0.7, 0.05); }
    g.fillStyle = ink(coat); dress ? D.poly(g, [[-0.5, 0.12], [0.5, 0.12], [0.28, 1.55], [-0.28, 1.55]]) : D.rect(g, -0.34, 0.7, 0.68, 0.9, 0.16);
    if (apron) { g.fillStyle = ink(C.cream); D.rect(g, -0.24, 0.25, 0.48, 1.0, 0.08); }
    if (stripes) { g.fillStyle = ink(C.cream, 'print'); for (let k = 0; k < 4; k++) D.rect(g, -0.34, 0.82 + k * 0.18, 0.68, 0.07); }
    g.fillStyle = ink(P2.shade(coat, -0.12)); D.rect(g, -0.48, 0.78, 0.16, 0.75, 0.08);
    if (phone) { g.fillStyle = ink(P2.shade(coat, -0.12)); D.poly(g, [[0.3, 1.45], [0.46, 1.45], [0.62, 1.05], [0.48, 1.0]]); g.fillStyle = ink(skin); D.ell(g, 0.58, 1.08, 0.09, 0.09); g.fillStyle = ink(C.phone); D.rect(g, 0.5, 1.1, 0.2, 0.32, 0.04); g.fillStyle = ink('#bfe6ff', 'print'); D.rect(g, 0.53, 1.15, 0.14, 0.22, 0.02); }
    else { D.rect(g, 0.32, 0.78, 0.16, 0.75, 0.08); g.fillStyle = ink(skin); D.ell(g, 0.4, 0.78, 0.08, 0.08); }
    g.fillStyle = ink(skin); D.ell(g, -0.4, 0.78, 0.08, 0.08);
    if (ruff) { g.fillStyle = ink(C.cream); D.ell(g, 0, 1.6, 0.36, 0.11); } else { g.fillStyle = ink(trim); D.poly(g, [[-0.2, 1.6], [0.2, 1.6], [0.08, 1.42], [-0.08, 1.42]]); }
    g.fillStyle = ink(skin); D.ell(g, 0, 1.84, 0.26, 0.29);
    g.fillStyle = ink('#2a1608', 'print'); D.ell(g, -0.09, 1.92, 0.03, 0.04); D.ell(g, 0.09, 1.92, 0.03, 0.04);
    g.fillStyle = ink('#c9845a', 'print'); D.ell(g, -0.15, 1.82, 0.04, 0.025); D.ell(g, 0.15, 1.82, 0.04, 0.025);
    if (hat === 'brim') { g.fillStyle = ink(hatC); D.rect(g, -0.46, 2.08, 0.92, 0.1, 0.05); D.rect(g, -0.26, 2.12, 0.52, 0.36, 0.08); g.fillStyle = ink(C.coral, 'print'); D.rect(g, -0.26, 2.16, 0.52, 0.06); }
    if (hat === 'cap') { g.fillStyle = ink(C.cream); D.ell(g, 0, 2.12, 0.3, 0.18); D.rect(g, -0.3, 1.86, 0.08, 0.26, 0.04); D.rect(g, 0.22, 1.86, 0.08, 0.26, 0.04); }
    if (hat === 'beret') { g.fillStyle = ink(hatC); D.ell(g, 0.05, 2.14, 0.32, 0.13); }
    if (hat === 'hair') { g.fillStyle = ink(hatC); D.ell(g, 0, 2.08, 0.28, 0.16); D.rect(g, -0.29, 1.8, 0.12, 0.3, 0.06); D.rect(g, 0.17, 1.8, 0.12, 0.3, 0.06); }
  }, { w: 1.4, h: 2.6, name: 'person' });
}
// an Amsterdam canal house facade: tall, narrow, a stepped / neck / bell gable, rows of white-framed windows, a hoist beam
function canalHouse(w, h, kind, wall) {
  return P2.drawnPiece((g, ink) => {
    const body = h * 0.72;
    g.fillStyle = ink(wall); D.rect(g, -w / 2, 0, w, body);
    if (kind === 'step') { const st = 4; for (let i = 0; i < st; i++) { const sw = w * (1 - i / st) * 0.98, y = body + i * (h - body) / st; D.rect(g, -sw / 2, y - 0.05, sw, (h - body) / st + 0.06); } }
    else if (kind === 'neck') { D.rect(g, -w * 0.3, body - 0.05, w * 0.6, h - body); D.poly(g, [[-w / 2, body], [-w * 0.3, body + (h - body) * 0.55], [-w * 0.3, body]]); D.poly(g, [[w / 2, body], [w * 0.3, body + (h - body) * 0.55], [w * 0.3, body]]); D.poly(g, [[-w * 0.36, h - 0.05], [w * 0.36, h - 0.05], [0, h + 0.5]]); }
    else { D.poly(g, [[-w / 2, body], [w / 2, body], [w * 0.38, body + (h - body) * 0.5], [w * 0.22, h], [-w * 0.22, h], [-w * 0.38, body + (h - body) * 0.5]]); D.ell(g, 0, h, w * 0.22, 0.35); }
    g.fillStyle = ink(P2.shade(wall, -0.22), 'print'); for (let y = 0.6; y < body; y += 0.55) D.rect(g, -w / 2, y, w, 0.05);   // brick courses
    const cols = w > 4 ? 3 : 2, ww = w / (cols * 1.9);
    for (let row = 0; row < 4; row++) for (let c = 0; c < cols; c++) {
      const x = -w / 2 + (c + 0.5) * w / cols - ww / 2, y = 1.9 + row * (body - 2.1) / 4; if (y + ww * 1.4 > body + (h - body) * 0.4) continue;
      g.fillStyle = ink(C.cream); D.rect(g, x - 0.1, y - 0.1, ww + 0.2, ww * 1.45 + 0.2, 0.06);
      g.fillStyle = ink(row ? '#3b4a55' : C.glass, 'print'); D.rect(g, x, y, ww, ww * 1.45, 0.04);
      g.fillStyle = ink(C.cream, 'print'); D.rect(g, x + ww / 2 - 0.04, y, 0.08, ww * 1.45); D.rect(g, x, y + ww * 0.7, ww, 0.07);
    }
    g.fillStyle = ink(C.cream); D.rect(g, -0.08, body + (h - body) * 0.3, 0.16, 0.5);   // gable window
    g.fillStyle = ink(C.woodD); D.rect(g, -0.6, 0, 1.2, 1.65, 0.5); g.fillStyle = ink(C.ochre, 'print'); D.ell(g, 0.3, 0.8, 0.07, 0.07);
    g.fillStyle = ink(C.woodD); D.rect(g, -0.07, h - 0.6, 0.14, 0.7);   // hoist beam
  }, { w: w + 0.4, h: h + 0.6, name: 'canal house' });
}
// a merchant ship (a fluyt), side on: hull, three masts, cream sails, coral pennants
const ship = () => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.woodD); D.poly(g, [[-4.4, 1.6], [4.6, 1.6], [3.6, 0], [-3.6, 0]]); D.poly(g, [[2.6, 1.5], [4.6, 1.5], [4.4, 2.7], [2.8, 2.7]]);
  g.fillStyle = ink(C.ochre, 'print'); D.rect(g, -3.9, 1.15, 8.2, 0.16); g.fillStyle = ink('#2a1a10', 'print'); for (let i = 0; i < 6; i++) D.ell(g, -2.8 + i * 1.1, 0.75, 0.12, 0.12);
  g.fillStyle = ink(C.wood); for (const [mx, mh] of [[-2.4, 6.2], [0.2, 7.4], [2.6, 5.6]]) D.rect(g, mx - 0.08, 1.5, 0.16, mh);
  g.fillStyle = ink(C.cream); for (const [mx, mh, sw] of [[-2.4, 6.2, 2.4], [0.2, 7.4, 2.8], [2.6, 5.6, 2.1]]) { D.poly(g, [[mx - sw / 2, 2.7], [mx + sw / 2, 2.7], [mx + sw / 2 - 0.15, 4.4], [mx - sw / 2 + 0.15, 4.4]]); D.poly(g, [[mx - sw / 2 + 0.2, 4.6], [mx + sw / 2 - 0.2, 4.6], [mx + sw / 2 - 0.35, mh + 0.9], [mx - sw / 2 + 0.35, mh + 0.9]]); }
  g.fillStyle = ink(P2.shade(C.cream, -0.12), 'print'); for (const mx of [-2.4, 0.2, 2.6]) { D.rect(g, mx - 1.1, 3.5, 2.2, 0.06); D.rect(g, mx - 1, 5.6, 2.0, 0.06); }
  g.fillStyle = ink(C.coral); for (const [mx, mh] of [[-2.4, 6.2], [0.2, 7.4], [2.6, 5.6]]) D.poly(g, [[mx, mh + 1.45], [mx, mh + 1.75], [mx + 0.9, mh + 1.6]]);
  g.fillStyle = ink(C.wood); D.rect(g, -2.48, 6.6, 0.16, 1.6); D.rect(g, 0.12, 7.7, 0.16, 1.6); D.rect(g, 2.52, 6.1, 0.16, 1.4);
}, { w: 9.6, h: 9.6, name: 'ship' });
const desk = () => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.wood); D.rect(g, -1.6, 0, 0.22, 1.2); D.rect(g, 1.38, 0, 0.22, 1.2); D.rect(g, -1.8, 1.1, 3.6, 0.28, 0.06);
  g.fillStyle = ink(P2.shade(C.coral, -0.2)); D.rect(g, -1.8, 0.62, 3.6, 0.5, 0.04); g.fillStyle = ink(C.ochre, 'print'); D.rect(g, -1.8, 0.82, 3.6, 0.08);
  g.fillStyle = ink(C.cream); D.poly(g, [[-1.1, 1.36], [0.4, 1.36], [0.3, 1.66], [-1.0, 1.66]]); g.fillStyle = ink(C.ink, 'print'); for (let i = 0; i < 3; i++) D.rect(g, -0.9, 1.43 + i * 0.07, 1.1, 0.025);
  g.fillStyle = ink(C.cream); D.poly(g, [[0.8, 1.36], [0.88, 1.36], [1.3, 2.2], [1.18, 2.22]]); g.fillStyle = ink(C.ink); D.rect(g, 0.62, 1.36, 0.3, 0.2, 0.05);
}, { w: 4, h: 2.4, name: 'desk' });
const barrel = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink(C.wood); D.rect(g, -0.55, 0, 1.1, 1.4, 0.35); g.fillStyle = ink(C.woodD, 'print'); D.rect(g, -0.55, 0.3, 1.1, 0.1); D.rect(g, -0.55, 1.0, 1.1, 0.1); }, { w: 1.3, h: 1.5, name: 'barrel' });
const crate = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#b9844f'); D.rect(g, -0.7, 0, 1.4, 1.2, 0.06); g.fillStyle = ink(C.woodD, 'print'); D.rect(g, -0.7, 0.55, 1.4, 0.08); D.poly(g, [[-0.6, 0.1], [-0.5, 0.1], [0.6, 1.05], [0.5, 1.1]]); }, { w: 1.6, h: 1.3, name: 'crate' });
const lampPost = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#3a3030'); D.rect(g, -0.08, 0, 0.16, 3); D.rect(g, -0.3, 2.9, 0.6, 0.6, 0.08); D.poly(g, [[-0.4, 3.45], [0, 3.8], [0.4, 3.45]]); g.fillStyle = ink(C.glass, 'print'); D.rect(g, -0.2, 3.0, 0.4, 0.4); }, { w: 1, h: 3.9, name: 'lamp' });
const elm = (h) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.woodD); D.rect(g, -0.22, 0, 0.44, h * 0.45); D.poly(g, [[-0.1, h * 0.4], [0.1, h * 0.4], [-0.8, h * 0.6], [-1, h * 0.58]]);
  g.fillStyle = ink('#5f8a46'); D.ell(g, 0, h * 0.66, h * 0.42, h * 0.34); D.ell(g, -h * 0.22, h * 0.56, h * 0.2, h * 0.16); D.ell(g, h * 0.24, h * 0.58, h * 0.2, h * 0.16);
  g.fillStyle = ink('#7fae55'); D.ell(g, -h * 0.08, h * 0.76, h * 0.22, h * 0.15);
  const r = P2.rng(Math.round(h * 100)); g.fillStyle = ink(C.cream, 'print'); for (let i = 0; i < 9; i++) D.ell(g, (r() - 0.5) * h * 0.6, h * (0.5 + r() * 0.35), 0.13, 0.13);
  g.fillStyle = ink(C.coral, 'print'); for (let i = 0; i < 6; i++) D.ell(g, (r() - 0.5) * h * 0.55, h * (0.52 + r() * 0.3), 0.11, 0.11);
}, { w: h * 0.9, h: h * 1.0, name: 'elm' });
const tower = (w, h, col, top) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(col); D.rect(g, -w / 2, 0, w, h);
  if (top === 'spire') { D.rect(g, -w * 0.3, h - 0.05, w * 0.6, 0.9); D.poly(g, [[-w * 0.18, h + 0.8], [w * 0.18, h + 0.8], [0, h + 2.6]]); }
  if (top === 'step') { D.rect(g, -w * 0.38, h - 0.05, w * 0.76, 0.8); D.rect(g, -w * 0.22, h + 0.7, w * 0.44, 0.7); }
  const cols = Math.max(2, Math.round(w / 0.7)); g.fillStyle = ink(C.glass, 'print');
  for (let y = 0.6; y < h - 0.5; y += 0.7) for (let c = 0; c < cols; c++) { if ((c * 7 + Math.round(y * 3)) % 5 === 0) continue; D.rect(g, -w / 2 + 0.2 + c * (w - 0.4) / cols, y, (w - 0.4) / cols * 0.55, 0.38); }
  g.fillStyle = ink(P2.shade(col, 0.25), 'print'); D.rect(g, -w / 2, h - 0.25, w, 0.12);
}, { w: w + 0.2, h: h + 2.8, name: 'tower' });
const fence = (w) => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#6b5a4c'); D.rect(g, -w / 2, 1.1, w, 0.18); D.rect(g, -w / 2, 0.45, w, 0.18); const n = Math.round(w / 0.55); for (let i = 0; i <= n; i++) D.poly(g, [[-w / 2 + i * w / n - 0.08, 0], [-w / 2 + i * w / n + 0.08, 0], [-w / 2 + i * w / n + 0.08, 1.6], [-w / 2 + i * w / n, 1.8], [-w / 2 + i * w / n - 0.08, 1.6]]); }, { w: w + 0.3, h: 2, name: 'fence' });
const gate = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#5a4a40'); D.rect(g, -1.6, 0, 0.3, 2.6); D.rect(g, 1.3, 0, 0.3, 2.6); D.rect(g, -1.3, 0.3, 2.6, 0.16); D.rect(g, -1.3, 1.9, 2.6, 0.16); for (let i = 0; i < 6; i++) D.rect(g, -1.2 + i * 0.47, 0.3, 0.1, 1.7); g.fillStyle = ink(C.ochre); D.rect(g, -0.28, 0.9, 0.56, 0.5, 0.08); g.fillStyle = ink(C.ochre); D.ell(g, 0, 1.45, 0.2, 0.2); g.fillStyle = ink('#5a4a40', 'print'); D.ell(g, 0, 1.12, 0.07, 0.07); }, { w: 3.4, h: 2.8, name: 'gate' });
const exchange = () => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.cream); D.rect(g, -3.6, 0, 7.2, 0.5); D.rect(g, -3.3, 0.45, 6.6, 0.35); D.poly(g, [[-3.6, 4.4], [3.6, 4.4], [0, 5.9]]); D.rect(g, -3.6, 3.9, 7.2, 0.55);
  for (let i = 0; i < 6; i++) { g.fillStyle = ink(P2.shade(C.cream, -0.05)); D.rect(g, -3.0 + i * 1.18, 0.75, 0.55, 3.2, 0.1); g.fillStyle = ink(P2.shade(C.cream, -0.25), 'print'); D.rect(g, -2.86 + i * 1.18, 0.9, 0.06, 2.9); D.rect(g, -2.66 + i * 1.18, 0.9, 0.06, 2.9); }
  g.fillStyle = ink(C.indigo, 'print'); D.poly(g, [[-2.2, 4.55], [2.2, 4.55], [0, 5.5]]); g.fillStyle = ink(C.ochre, 'print'); D.ell(g, 0, 4.85, 0.25, 0.25);
}, { w: 7.6, h: 6.1, name: 'exchange' });
const shareCard = (col) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.cream); D.rect(g, -1.4, 0, 2.8, 3.6, 0.12); g.fillStyle = ink(col, 'print'); D.rect(g, -1.2, 3.0, 2.4, 0.32); D.rect(g, -1.2, 0.2, 2.4, 0.12);
  g.fillStyle = ink(C.ink, 'print'); for (let i = 0; i < 5; i++) D.rect(g, -1.0, 1.0 + i * 0.32, 1.6 - (i % 2) * 0.5, 0.08);
  g.fillStyle = ink(C.coral); D.ell(g, 0.8, 0.75, 0.38, 0.38); g.fillStyle = ink(C.ochre, 'print'); D.ell(g, 0.8, 0.75, 0.18, 0.18);
}, { w: 3, h: 3.8, name: 'share' });
const bar = (h, col) => P2.drawnPiece((g, ink) => { g.fillStyle = ink(col); D.rect(g, -1.1, 0, 2.2, h, 0.12); g.fillStyle = ink(P2.shade(col, 0.25), 'print'); for (let y = 0.5; y < h - 0.3; y += 0.8) D.rect(g, -0.9, y, 1.8, 0.12); g.fillStyle = ink(P2.shade(col, -0.25)); D.rect(g, -1.1, h - 0.4, 2.2, 0.4, 0.1); }, { w: 2.4, h: h + 0.1, name: 'bar' });
const arrow = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink(C.coral); D.poly(g, [[-2.4, 0], [-1.9, 0], [1.2, 2.5], [1.0, 1.5], [2.2, 3.2], [0.4, 3.0], [1.0, 2.8], [-2.2, 0.4]]); }, { w: 4.8, h: 3.4, name: 'arrow' });
const sprout = (h, col, bloom) => P2.drawnPiece((g, ink) => { g.fillStyle = ink(C.limeD); D.rect(g, -0.06, 0, 0.12, h); D.ell(g, -0.35, h * 0.5, 0.38, 0.17, 0.5); D.ell(g, 0.35, h * 0.7, 0.38, 0.17, -0.5); g.fillStyle = ink(col); D.ell(g, 0, h, bloom, bloom); g.fillStyle = ink(C.ochre, 'print'); D.ell(g, 0, h, bloom * 0.4, bloom * 0.4); }, { w: 1.4, h: h + 0.6, name: 'sprout' });
const bed = (w) => P2.drawnPiece((g, ink) => { g.fillStyle = ink(C.wood); D.rect(g, -w / 2, 0, w, 0.7, 0.1); g.fillStyle = ink(C.woodD, 'print'); D.rect(g, -w / 2, 0.32, w, 0.06); g.fillStyle = ink('#5e3f2a'); D.rect(g, -w / 2 + 0.2, 0.66, w - 0.4, 0.2, 0.08); }, { w: w + 0.2, h: 0.95, name: 'bed' });

// ---------------------------------------------------------------- A: Amsterdam, 1602
const WALLS = [C.brick, '#6d4a3c', '#b88a5a', C.slate, '#8a4436', '#c9a46c', '#5d6b55'];
const KINDS = ['step', 'bell', 'neck', 'step', 'bell', 'neck', 'step'];
RISE = 0.25; STAG = 0.06;
{
  let x = AX - 25;
  for (let i = 0; i < 9; i++) { const w = between(3.6, 4.6), h = between(9, 11.5); popup(...canalHouse(w, h, KINDS[i % 7], WALLS[(i * 3) % 7]), { x: x + w / 2, z: -7.5 - (i % 2) * 0.5, yaw: 0, k: i }); x += w + 0.35; }
  popup(...ship(), { x: AX + 10, z: CANAL.z - 0.3, yaw: 0, k: 10, sway: 0.2 });
  for (const [ex, ez, eh] of [[AX - 28, -4.5, 7], [AX + 25, -4.8, 6.5], [AX - 20, 6.5, 6], [AX + 22, 7.5, 6.8]]) popup(...elm(eh), { x: ex, z: ez, cross: true, k: 6, sway: 0.5 });
  popup(...desk(), { x: AX - 8, z: 3.2, yaw: 0.1, k: 12, scale: 1.5 });
  popup(...person({ coat: '#2a2a30', ruff: true, hat: 'brim', hatC: '#1e1e22' }), { x: AX - 8.2, z: 2.2, yaw: 0.1, scale: 1.7, k: 11 });   // the clerk
  // the queue: anyone. a maid, a baker, a sailor, a merchant, a carpenter, a widow, a boy
  const Q = [
    { coat: '#5a6f8a', hat: 'cap', apron: true, dress: true },                         // maid (the hero)
    { coat: '#c9a46c', apron: true, hat: 'beret', hatC: C.cream },                      // baker
    { coat: C.indigo, stripes: true, hat: 'beret', hatC: '#22304a', skin: C.skinB },    // sailor
    { coat: '#2a2a30', ruff: true, hat: 'brim' },                                       // merchant
    { coat: '#7e5a3a', hat: 'beret', hatC: '#4a3020', skin: C.skinC },                  // carpenter
    { coat: '#3e3a40', hat: 'cap', dress: true },                                      // widow
    { coat: C.coral, hat: 'hair', hatC: '#6a3a20' },                                    // boy
  ];
  Q.forEach((o, i) => {
    const h = popup(...person(o), { x: AX - 4.4 + i * 2.5, z: 3.6 + (i % 2) * 0.5, yaw: -0.05, scale: i === 6 ? 1.35 : 1.75, k: 13 + i, sway: 0.05 });
    if (i === 0) H.setHero(h, { turn: 'flip' });
  });
  for (const [bx, bz, kind] of [[AX + 15, 3.5, barrel], [AX + 16.3, 4.3, barrel], [AX + 17.8, 3.6, crate], [AX - 17, 4.5, crate], [AX - 15.6, 5.2, barrel], [AX + 4, 9.5, crate]]) popup(...kind(), { x: bx, z: bz, k: 8 });
  for (const lx of [AX - 20, AX + 2, AX + 17]) popup(...lampPost(), { x: lx, z: 1.2, k: 7 });
  // passers-by on the far quay and near edge
  for (const [px, pz, o] of [[AX - 22, -5, { coat: '#8a4436', hat: 'brim' }], [AX + 6, -5.2, { coat: '#5d6b55', dress: true, hat: 'cap' }], [AX - 26, 9, { coat: C.ochre, hat: 'beret', hatC: '#5a3a20' }], [AX + 14, 10, { coat: '#4e5f63', hat: 'brim', hatC: '#2a2a30' }]]) popup(...person(o), { x: px, z: pz, k: 9, scale: 1.6 });
}

// ---------------------------------------------------------------- B: the world today, a walled skyline
RISE = ls(3, 18) + 0.7; STAG = 0.07;
{
  const W = 44, Dd = 15, mz = -6, [nx, nz] = contAt(BX, mz, W, Dd, 'na');
  const T = [[-2.6, -1.2, 1.6, 7, C.indigo, 'spire'], [-0.8, -2.2, 1.9, 10.5, C.indigoD, 'step'], [1.2, -1.4, 1.7, 8.2, '#5b78b2', 'spire'], [2.9, -2.4, 1.5, 6.4, C.slate, null], [0.2, 0.2, 1.4, 5.2, '#6a86b8', null], [-2.0, 0.6, 1.3, 4.2, C.slate, 'step']];
  T.forEach(([dx, dz, w, h, col, top], i) => popup(...tower(w, h, col, top), { x: nx + dx, z: nz + dz, yaw: 0, k: i }));
  popup(...fence(4.2), { x: nx - 3.2, z: nz + 3.2, yaw: 0.35, k: 7 }); popup(...gate(), { x: nx + 0.3, z: nz + 3.6, yaw: 0, k: 8 }); popup(...fence(4.2), { x: nx + 3.9, z: nz + 3.1, yaw: -0.35, k: 9 });
  const crowd = [['eu', -1, 0.4], ['eu', 1.2, -0.3], ['af', -1.2, -1], ['af', 1, 1.2], ['af', 0, 3], ['as', -4, 0.5], ['as', 0, -1], ['as', 3.5, 1], ['as', 6, -1.5], ['as', 1.5, 3], ['sa', 0, 0], ['sa', 0.6, 3], ['au', 0, 0]];
  const COATS = [C.coral, C.ochre, C.lime, '#8a4436', '#5d6b55', C.indigo, '#c9a46c'], SK = [C.skin, C.skinB, C.skinC];
  crowd.forEach(([id, dx, dz], i) => { const [cx, cz] = contAt(BX, mz, W, Dd, id); popup(...person({ coat: COATS[i % 7], skin: SK[i % 3], hat: ['hair', 'cap', 'beret', 'none'][i % 4], hatC: '#4a2a18', dress: i % 3 === 1 }), { x: cx + dx * 1.3, z: cz + dz, k: 10 + i, scale: 1.7 }); });
}

// small trees on every continent of both maps (density, life)
{
  const W = 44, Dd = 15, mz = -6;
  for (const [mx, r0] of [[BX, ls(3, 17) + 0.9], [DX, ls(10, 45) + 0.5]]) {
    RISE = r0; STAG = 0.04; let k = 0;
    for (const [id, pts] of mapPts(mx, mz, W, Dd)) {
      const [cx, cz] = contAt(mx, mz, W, Dd, id);
      for (let q = 0; q < 2; q++) { if (mx === BX && id === 'na') continue; const [px, pz] = pts[Math.floor(rnd() * pts.length)], t = 0.12 + rnd() * 0.18;
        popup(...elm(between(1.7, 2.3)), { x: px + (cx - px) * t, z: pz + (cz - pz) * t, cross: true, k: k++, sway: 0.4 }); }
    }
  }
}

// ---------------------------------------------------------------- C: the phone
STAG = 0.08;
{
  const { x, z } = PHONE;
  RISE = ls(7, 33) + 0.2;
  popup(...exchange(), { x, z: z - 6, yaw: 0, k: 0 });
  popup(...shareCard(C.indigo), { x: x - 4.4, z: z - 1.5, yaw: 0.3, k: 2 }); popup(...shareCard(C.lime), { x: x - 3.6, z: z + 0.2, yaw: 0.15, k: 3 }); popup(...shareCard(C.coral), { x: x - 2.6, z: z + 1.8, yaw: 0, k: 4 });
  popup(...person({ coat: C.coral, phone: true, hat: 'hair', hatC: '#3a2216', skin: C.skinB }), { x: x - 0.4, z: z + 5.5, yaw: 0, k: 5, scale: 2.0 });
  RISE = ls(8, 37) + 0.3; popup(...bar(2.2, C.coral), { x: x + 2.6, z: z + 1.2, yaw: -0.1, k: 0 });
  RISE = ls(8, 37) + 2.4; popup(...bar(9.5, C.lime), { x: x + 5.0, z: z + 1.0, yaw: -0.1, k: 0 }); popup(...arrow(), { x: x + 3.6, z: z + 3.4, yaw: -0.1, k: 4 });
}

// ---------------------------------------------------------------- D: anyone with a phone, everywhere
{
  const W = 44, Dd = 15, mz = -6;
  RISE = ls(11, 47) + 0.15; STAG = 0.05;
  const spots = [['na', -3, -2], ['na', 2, 1], ['na', -1, 3], ['sa', 0, -2], ['sa', 0.8, 2], ['eu', -1, 0], ['eu', 1.5, -1], ['af', -1.5, -2], ['af', 1, 0.5], ['af', -0.5, 3.5], ['as', -5, -1], ['as', -1, 1], ['as', 3, -2], ['as', 6, 1], ['as', 1, 4], ['au', -0.5, 0], ['au', 1.4, 0.6]];
  const COATS = [C.coral, C.ochre, C.lime, C.indigo, '#8a4436', '#5d6b55', '#c9a46c'], SK = [C.skin, C.skinB, C.skinC];
  spots.forEach(([id, dx, dz], i) => { const [cx, cz] = contAt(DX, mz, W, Dd, id); popup(...person({ coat: COATS[(i * 3) % 7], skin: SK[i % 3], phone: true, hat: ['hair', 'cap', 'beret', 'none', 'brim'][i % 5], hatC: i % 5 === 4 ? '#2a2a30' : '#4a2a18', dress: i % 4 === 2 }), { x: cx + dx * 1.2, z: cz + dz, k: i, scale: 1.75, yaw: (i % 3 - 1) * 0.12 }); });
  // the garden on the sea, bottom middle: a planter bed and sprouts in brand colours
  RISE = ls(12, 51) + 0.5; STAG = 0.07;
  const gx = DX + 1, gz = 6.5, GS = 2.1;
  popup(...bed(7), { x: gx, z: gz + 0.6 * GS, yaw: 0, k: 0, scale: GS });
  [[-2.6, 2.2, C.coral, 0.32], [-1.4, 3.0, C.lime, 0.36], [-0.2, 2.5, C.cream, 0.3], [1.0, 3.3, C.ochre, 0.38], [2.3, 2.4, C.coral, 0.3], [-2.0, 1.6, C.cream, 0.26], [1.7, 1.8, C.lime, 0.28]]
    .forEach(([dx, h, col, b], i) => popup(...sprout(h, col, b), { x: gx + dx * GS, z: gz + (i % 2) * 0.35 * GS, yaw: 0, k: 1 + i, sway: 0.5, scale: GS }));
}

// ---------------------------------------------------------------- life
const life = createLife({ scene: H.scene, camera: H.camera, heroHeight: H.heroHeight, seed: 7, wind: [0.94, 0.34] });
life.flock({ size: 4, every: 12, height: 3.6, colors: ['#f6f1e6', '#ece4d4'] });
life.cloudShadows({ count: 3, alpha: 0.12 });
life.reset(H.target);
H.onRestart(() => life.reset(H.target));

// ---------------------------------------------------------------- camera: dolly between the dioramas on the narration
const ease = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
const KEYS = [   // [time, x, z, dist]
  [0, AX - 1, 0, 52], [ls(2, 10), AX - 1, 2.2, 42], [ls(3, 17) - 0.2, AX, 2.6, 40],
  [ls(3, 17) + 1.6, BX - 9, -7, 46], [ls(5, 26) - 0.2, BX - 6, -6, 42],
  [ls(6, 31) + 0.1, BX - 5, -6, 42], [ls(6, 31) + 1.8, CX + 1, -6.5, 41], [ls(10, 45) - 0.3, CX + 1, -6.8, 39],
  [ls(10, 45) + 1.4, DX, -4, 50], [ls(12, 50), DX, -1, 48], [ls(12, 50) + 2.5, DX + 1, 4.5, 40], [END, DX + 1, 5, 38],
];
function camAt(t) {
  let i = 0; while (i < KEYS.length - 2 && t > KEYS[i + 1][0]) i++;
  const [t0, x0, z0, d0] = KEYS[i], [t1, x1, z1, d1] = KEYS[i + 1], u = ease((t - t0) / Math.max(0.01, t1 - t0));
  return [x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, d0 + (d1 - d0) * u];
}
H.onStep((t, dt) => {
  const [x, z, d] = camAt(t);
  if (!ALLUP) window.__papercraft?.look(x, z, d, 1.5);
  life.update(dt, H.target);
  window.__overlay?.(t);
});
H.start(); window.__H = H;
window.__END = END;
