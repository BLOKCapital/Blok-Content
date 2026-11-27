// BLOK papercraft reel 1: Grandma's garden. Own subject (a cottage allotment) on the fixed 2D harness.
import * as P2 from 'papercraft/lib/paperkit-2d.js';
import * as EX from 'papercraft/examples/countryside.js';
import { createHarness2D } from './harness-2d.js';
const C = { ground: '#d8c9a0', wash: '#b4b27e', washWarm: '#dcbf86', soil: '#8a5a36', soilDark: '#6e4426', path: '#f1e4c4',
  leaf: '#4f8a46', leafLight: '#7fae4f', pine: '#5f7f3e', trunk: '#74452a', wall: '#f1e2c2', roof: '#b9503a', window: '#ffc45a', wood: '#a8683a',
  ink: '#3a2412', shadow: '#6a3414', kraft: '#c9a77c', petal: ['#f2b81d', '#e0752c', '#c94a5a', '#f3e6c8', '#7a5ab0'] };
const GMA_AT = [0, 2];
const H = createHarness2D({ ground: C.ground, shadow: C.shadow, kraft: C.kraft, view: { pitch: 46, dist: 26, across: 19 }, light: [-0.7, 1.1, 0.4], play: true, subject: GMA_AT });
const D = P2.draw2;
// plots: [x0, x1, z0, z1, rows]
const PLOTS = [[-9, -2, -5, 1, 5], [2, 9, -5, 1, 5], [-9, -2, 4, 9, 4], [2, 9, 4, 9, 4], [-9, -2, 12, 17, 4], [2, 9, 12, 17, 4]];
const NB = [-17, -11, -6, 6];   // the neighbor's bare plot (left edge)
H.printGround(({ x, GQ, X, Z, rnd, washes, drifts }) => {
  washes([C.wash, C.wash, C.washWarm, C.washWarm, C.wash]);
  const rect = (x0, x1, z0, z1, col, a = 1) => { x.fillStyle = P2.rgba(col, a); x.beginPath(); x.moveTo(X(x0), Z(z0)); x.lineTo(X(x1), Z(z0)); x.lineTo(X(x1), Z(z1)); x.lineTo(X(x0), Z(z1)); x.closePath(); x.fill(); };
  rect(-1.3, 1.3, -40, 40, C.path, 0.9); rect(-30, 30, 2, 3.2, C.path, 0.85); rect(-30, 30, 10, 11.2, C.path, 0.85);
  for (const [x0, x1, z0, z1, n] of PLOTS) { rect(x0, x1, z0, z1, C.soil, 0.95);
    for (let k = 0; k < n; k++) { const zz = z0 + (k + 0.5) * (z1 - z0) / n; rect(x0 + 0.3, x1 - 0.3, zz - 0.25, zz + 0.25, C.soilDark, 0.8); } }
  rect(NB[0], NB[1], NB[2], NB[3], '#b8a27a', 0.9);
  for (let k = 0; k < 300; k++) { const px = X(-30 + rnd() * 60), pz = Z(-30 + rnd() * 60); x.fillStyle = P2.rgba(rnd() < 0.5 ? '#6c7c4a' : '#8d9a58', 0.5); x.fillRect(px, pz, 0.08 * GQ, 0.25 * GQ); }
  drifts((px, py) => { if (rnd() < 0.8) { x.strokeStyle = P2.rgba('#7d8c50', 0.7); x.lineWidth = 0.07 * GQ; x.beginPath(); x.moveTo(px, py); x.lineTo(px + (rnd() - 0.5) * 0.15 * GQ, py - 0.35 * GQ); x.stroke(); } });
});
let rnd = P2.rng(77);
const G = { g0: [], g1: [], g2: [], g3: [], g4: [] };
const put = (grp, pp, x, z, o = {}) => { const p = H.piece(pp[0], pp[1], { x, z, ...o }); G[grp].push(p); return p; };
const between = (a, b) => a + rnd() * (b - a);
const mound = (w, h, lobes = 7, depth = 0.18) => P2.roughen(P2.shape.mound(rnd, { w, h, lobes, depth }), rnd);
// pieces
const sprout = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#5f9a45'); D.rect(g, -0.04, 0, 0.08, 0.5); D.ell(g, -0.18, 0.5, 0.18, 0.09, -0.4); D.ell(g, 0.18, 0.55, 0.18, 0.09, 0.4); }, { w: 0.8, h: 0.75, name: 'sprout' });
const cabbage = () => [mound(between(1.3, 1.7), 1.0, 6, 0.25), EX.paintBush({ leaf: '#6f9e55' }, { bands: 2, flowers: false, motifs: false })];
const sunflower = (h) => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#4f8a3a'); D.rect(g, -0.07, 0, 0.14, h - 0.4); D.ell(g, -0.3, h * 0.4, 0.3, 0.12, -0.5); D.ell(g, 0.3, h * 0.55, 0.3, 0.12, 0.5);
  g.fillStyle = ink('#f2b81d'); for (let k = 0; k < 12; k++) { const a = k / 12 * 6.283; D.ell(g, Math.cos(a) * 0.38, h - 0.3 + Math.sin(a) * 0.38, 0.2, 0.09, a); }
  g.fillStyle = ink('#6a3a1a'); D.ell(g, 0, h - 0.3, 0.26, 0.26); }, { w: 1.4, h: h + 0.5, name: 'sunflower' });
const tomato = () => P2.drawnPiece((g, ink) => { g.fillStyle = ink('#a8683a'); D.rect(g, -0.04, 0, 0.08, 2.0); g.fillStyle = ink('#4f8a3a'); D.ell(g, 0, 1.2, 0.5, 0.7);
  g.fillStyle = ink('#d8452d'); for (const [a, b] of [[-0.2, 1.0], [0.25, 1.3], [-0.05, 1.6], [0.2, 0.85]]) D.ell(g, a, b, 0.11, 0.11); }, { w: 1.2, h: 2.2, name: 'tomato' });
const flowerBed = (col) => [mound(between(2.2, 3), 1.1, 9, 0.3), EX.paintBush({ leaf: '#6f8f5a' }, { bands: 0, flowers: true, motifs: false })];
const tree = () => { const h = between(6.5, 8); return [P2.roughen(EX.shape.tree(rnd, { w: h * 0.8, h, lobes: 8, canopy: 0.7 }), rnd), EX.paintTree({ leaf: rnd() < 0.5 ? '#d9a03a' : '#5f8f45', trunk: C.trunk }, { trunkTop: 0.3, leaves: 20, berries: '#c8452d' })]; };
const fence = (w) => [EX.shape.fence({ w, h: 1.4, pickets: Math.round(w * 1.3) }), EX.paintWood({ wood: '#b07a48' }, { planks: 1 })];
const house = [EX.shape.house({ w: 6, wallH: 3.7, roofH: 3 }), EX.paintHouse({ wall: C.wall, roof: C.roof, window: C.window, ink: C.ink }, { wallH: 3.7 })];
// g0: cottage + Grandma
put('g0', house, 5.5, -12, { yaw: -0.15 });
const gma = put('g0', P2.drawnPiece((g, ink) => { g.save(); g.scale(1.6, 1.6);
  g.fillStyle = ink('#8a4f7d'); D.rect(g, -0.4, 0.7, 0.8, 1.35, 0.24);                     // cardigan
  g.fillStyle = ink('#f3e6c8'); D.rect(g, -0.28, 0.7, 0.56, 0.9, 0.1);                       // apron
  g.fillStyle = ink('#c9845a', 'print'); D.rect(g, -0.18, 1.0, 0.36, 0.2, 0.04);             // apron pocket
  g.fillStyle = ink('#8a4f7d'); D.rect(g, 0.32, 1.25, 0.22, 0.62, 0.1);
  g.fillStyle = ink('#e8b48c'); D.ell(g, 0.43, 1.22, 0.1, 0.09); D.ell(g, 0, 2.32, 0.36, 0.38);
  g.fillStyle = ink('#dcdcdc'); D.ell(g, 0, 2.58, 0.36, 0.17); D.ell(g, 0, 2.82, 0.2, 0.17); // hair + bun
  g.fillStyle = ink('#3a2a1a', 'print'); D.ell(g, -0.13, 2.3, 0.04, 0.05); D.ell(g, 0.13, 2.3, 0.04, 0.05);
  g.strokeStyle = '#3a2a1a'; g.lineWidth = 0.035; g.beginPath(); g.arc(-0.13, 2.3, 0.11, 0, 6.3); g.stroke(); g.beginPath(); g.arc(0.13, 2.3, 0.11, 0, 6.3); g.stroke();
  g.fillStyle = ink('#a33a2a', 'print'); D.rect(g, -0.08, 2.12, 0.16, 0.03, 0.015); g.restore();
}, { w: 2.1, h: 4.9, name: 'grandma' }), GMA_AT[0], GMA_AT[1], { sway: 0.15, sharp: true });
const can = put('g0', P2.drawnPiece((g, ink) => { g.fillStyle = ink('#9fb0b0'); D.rect(g, -0.25, 0, 0.5, 0.45, 0.06); D.poly(g, [[0.2, 0.15], [0.3, 0.2], [0.6, 0.55], [0.55, 0.6]]); g.fillStyle = ink('#7c8c8c'); D.rect(g, -0.15, 0.43, 0.3, 0.12, 0.05); }, { w: 1.2, h: 0.7, name: 'can' }), GMA_AT[0] + 1.4, GMA_AT[1] + 0.1, { sharp: true });
H.setHero(gma, { parts: [], step: 0.9 });
// g1: first sprouts in the near-left plot row
for (let k = 0; k < 6; k++) put('g1', sprout(), -8.3 + k * 1.2, -4.4 + (k % 2) * 0.2, { yaw: (rnd() - 0.5) * 0.5 });
// g2: the neighbor's bare plot behind a fence, waiting
put('g2', fence(6), (NB[0] + NB[1]) / 2, NB[2] - 0.3); put('g2', [EX.props.signpost(2.6), EX.paintWood({ wood: '#b9844f' }, { planks: 1 })], NB[1] - 0.8, NB[3] - 0.6, { yaw: 0.3 });
// g3: she keeps planting: cabbages, tomatoes, more sprouts in every plot
for (const [x0, x1, z0, z1, n] of PLOTS) for (let r = 0; r < n; r++) { const zz = z0 + (r + 0.5) * (z1 - z0) / n; if (x0 < 0 && z0 < 0 && r === 0) continue;
  for (let xx = x0 + 0.9; xx < x1 - 0.5; xx += between(1.6, 2.2)) put('g3', r % 2 ? cabbage() : rnd() < 0.5 ? tomato() : sprout(), xx, zz, { yaw: (rnd() - 0.5) * 0.4, sway: 0.3 }); }
// g4: thirty springs later: sunflowers, flower beds, trees, fence round her garden
for (let k = 0; k < 6; k++) put('g4', sunflower(between(2.6, 3.4)), -8.6 + k * 1.1, 9.4 + (k % 2) * 0.3, { sway: 0.6 });
for (let k = 0; k < 6; k++) put('g4', sunflower(between(2.6, 3.4)), 2.6 + k * 1.1, 9.5 + (k % 2) * 0.3, { sway: 0.6 });
for (const [x, z] of [[-10.5, 14], [10.5, 14], [-10.5, -7], [10.5, 2.5], [-10.5, 6], [10.5, 7]]) put('g4', flowerBed(), x, z, { sway: 0.4 });
for (const [x, z] of [[-12, -14], [12, -10], [-5, -15], [13, 7], [-13, 12]]) put('g4', tree(), x, z, { sway: 0.6, slotted: true });
put('g4', fence(7), -5.5, -6.2); put('g4', fence(7), 5.5, -6.2);
// big blurred near pieces sell the scale
for (const [f, dz] of [[-0.85, 3.5], [0.85, 3]]) { const z = H.zBot + dz, x = H.frame.cx + f * H.frame.half(z); put('g4', flowerBed(), x, z, { sway: 0.5 }); }
window.REEL_GROUPS = G;
H.start();
