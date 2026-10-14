// Anatomy of a public ledger: a ledger press that seals blocks into a chain.
// Built with the anatomy skill (.claude/skills/anatomy). Run: node build.mjs [--dark]
// Writes ledger-press.html (interactive) and ledger-figure.json (svg + live script, for the video slides).
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../../../.claude/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "../../../../.claude/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const theme = process.argv.includes("--dark") ? "dark" : "light";

const WIDTH = 640;
const HEIGHT = 420;

// ---- the model's fixed facts -------------------------------------------------------------
const N = 5; // blocks on the line; the last one is at the press
const PITCH = 64;
const X0 = -150;
const CX = Array.from({ length: N }, (_, i) => X0 + PITCH * i);
const BW = 46, BD = 44, BY = -24; // block plan: x from cx - 23, y from -24 to 20
const SLED_Z = 3, BODY_Z = 7, BODY_H = 26, TOP = BODY_Z + BODY_H, LID_H = 4;
const SEAL_R = 7;
const STATION = CX[N - 1];
const STROKE = 26; // how far the press lifts the lid
const ENTRIES = [
  ["Ana pays Raj 40", "Raj pays Lee 15", "Lee pays Ana 5"],
  ["Mia pays Sam 22", "Sam pays Ana 9", "Ana pays Kai 30"],
  ["Kai pays Mia 12", "Lee pays Raj 7", "Raj pays Sam 18"],
  ["Sam pays Lee 25", "Mia pays Kai 3", "Kai pays Ana 14"],
  ["Ana pays Mia 11", "Raj pays Kai 6", "Lee pays Sam 19"],
];
// FNV-1a, 24 bits shown: a stand-in fingerprint that really depends on the entries and the previous seal.
const fnv = (text) => { let h = 0x811c9dc5; for (const c of text) { h ^= c.charCodeAt(0); h = Math.imul(h, 0x01000193) >>> 0; } return h >>> 0; };
const SEALS = [];
ENTRIES.forEach((list, i) => SEALS.push(fnv((i ? SEALS[i - 1].toString(16) : "genesis") + "|" + list.join(";"))));
const hex = (n) => (n & 0xffffff).toString(16).padStart(6, "0");
const COPIES = 5;

const PLATE = { x: -214, y: -110, w: 428, d: 168, r: 9 };
const PLATE_H = 12, FOOT_H = 5;
const RACK = { x: -176, y: -100, w: 300, d: 26, r: 3 };
const RACK_Z = 0, RACK_H = 20;

const P = k.fitProjection(
  [...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0), [STATION, 0, 128], [RACK.x, RACK.y, 30], [STATION + 12, 40, 110]],
  WIDTH,
  HEIGHT,
  { pad: 26, azimuth: 33 },
);

const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (pts) => [...pts].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));
const blockPlan = (cx) => ({ x: cx - BW / 2, y: BY, w: BW, d: BD, r: 2.4 });

// ---- base ---------------------------------------------------------------------------------
function base() {
  const out = [`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`];
  for (const [x, y] of byDepth(k.corners(PLATE, 24))) {
    out.push(S(k.cylinder(x, y, 7.5, -PLATE_H - FOOT_H, 1.6, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.8, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, P, 28), { tone: "mid" }));
  }
  out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 9, 1.6), { tone: "mid", inner: L(k.sideSeam(PLATE, -5, P, 9), { tone: "faint" }) }));
  out.push(L(k.planOutline(k.insetPlan(PLATE, 5), 0, P, 9), { tone: "lo" }));
  const screws = k.corners(PLATE, 11);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.3, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));
  // ruler strip along the front edge: one tick every 4 units, a major under each block station
  const strip = { x: -196, y: PLATE.y + PLATE.d - 16, w: 330, d: 7, r: 1 };
  out.push(S(k.slabOf(strip, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(strip.x + 4, strip.x + strip.w - 4, 4, 4, strip.y + 0.8, 0.6, [2, 3.8], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  out.push(D([at([strip.x + 2, strip.y + 3.5, 0.6]), at([strip.x + strip.w - 2, strip.y + 3.5, 0.6])], { size: 0.45 }));
  // label plate, front right
  const label = { x: 150, y: PLATE.y + PLATE.d - 26, w: 46, d: 17, r: 1.2 };
  out.push(S(k.slabOf(label, 0, 0.8, P, 4), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(k.insetPlan(label, 1.6), 0.8, P, 3), { tone: "faint" }));
  [[6, 30], [9.5, 22], [13, 26]].forEach(([dy, len]) => out.push(L(k.lineOnTop([label.x + 6, label.y + dy], [label.x + 6 + len, label.y + dy], 0.8, P), { tone: "lo", free: true })));
  out.push(D([at([label.x + 3, label.y + 3, 0.8]), at([label.x + label.w - 3, label.y + label.d - 3, 0.8])], { size: 0.4 }));
  return out.join("");
}

// ---- the copies rack at the back: five copies of the same chain, each with a lamp ------------
const BAY = RACK.w / COPIES;
function rack() {
  const out = [`<path class="iso-halo" d="${k.haloOf(RACK, RACK_Z, RACK_H, P)}" style="opacity:.18"/>`];
  out.push(S(k.slabOf(RACK, RACK_Z, RACK_H, P, 4, 0.8), { tone: "mid", inner: L(k.sideSeam(RACK, 5, P, 4), { tone: "faint" }) }));
  // bay dividers run edge to edge across the top
  for (let b = 1; b < COPIES; b++) out.push(L(k.lineOnTop([RACK.x + BAY * b, RACK.y], [RACK.x + BAY * b, RACK.y + RACK.d], RACK_H, P), { tone: "faint" }));
  const lamps = [];
  for (let b = 0; b < COPIES; b++) {
    const bx = RACK.x + BAY * b;
    // a miniature of the chain: five small blocks on a tray
    const tray = { x: bx + 5, y: RACK.y + 3, w: BAY - 10, d: 10, r: 1 };
    out.push(S(k.slabOf(tray, RACK_H, 1.2, P, 3), { tone: "lo", crease: "none" }));
    for (let m = 0; m < N; m++) {
      const mx = tray.x + 3 + m * ((tray.w - 6) / N);
      out.push(S(k.slabOf({ x: mx, y: tray.y + 2.5, w: (tray.w - 6) / N - 2, d: 6, r: 0.6 }, RACK_H + 1.2, 4.5, P, 2, 0.3), { tone: "hi", crease: "lo" }));
    }
    // lamp in a bezel on the front lip
    const lp = [bx + BAY / 2, RACK.y + RACK.d - 6];
    out.push(S(k.cylinder(lp[0], lp[1], 5, RACK_H, 0.8, P, 24), { tone: "lo" }));
    out.push(`<g data-part="lamp" data-copy="${b}" class="bk-lamp">${S(k.cylinder(lp[0], lp[1], 3.8, RACK_H + 0.8, 2, P, 24), { tone: "mid" })}<path class="bk-lamp-glow" d="${k.ring(lp[0], lp[1], 3.8, RACK_H + 2.8, P, 24)}Z"/></g>`);
    lamps.push(lp);
    out.push(D([at([bx + 4, RACK.y + RACK.d - 3, RACK_H]), at([bx + BAY - 4, RACK.y + RACK.d - 3, RACK_H])], { size: 0.4 }));
  }
  return out.join("");
}

// ---- rails --------------------------------------------------------------------------------
function rails() {
  const out = [];
  for (const y of [-18, 10]) {
    out.push(S(k.slabOf({ x: -198, y, w: 380, d: 5, r: 1 }, 0, 3, P, 3, 0.4), { tone: "mid" }));
    out.push(D([-192, -60, 60, 176].map((x) => at([x, y + 2.5, 3])), { size: 0.4 }));
  }
  for (const x of [-204, 182]) {
    out.push(S(k.slabOf({ x, y: -22, w: 6, d: 41, r: 1.2 }, 0, 8, P, 3, 0.5), { tone: "mid" }));
    out.push(D([at([x + 3, -17, 8]), at([x + 3, 14, 8])], { size: 0.45 }));
  }
  return out.join("");
}

// ---- a block: sled, body with bands, coupling lugs, slot on top; lid and seal separate --------
function sealMarks(cx, z, seal) {
  // the seal's pattern: one notch per set bit of the fingerprint (16 positions round the rim)
  const marks = [];
  for (let b = 0; b < 16; b++) {
    if (!((seal >>> b) & 1)) continue;
    const a = (b / 16) * Math.PI * 2;
    const r0 = SEAL_R - 2.6, r1 = SEAL_R - 0.9;
    marks.push(k.lineOnTop([cx + Math.sin(a) * r0, Math.cos(a) * r0 - 2], [cx + Math.sin(a) * r1, Math.cos(a) * r1 - 2], z, P));
  }
  return marks.join("");
}

function blockBody(i) {
  const cx = CX[i];
  const plan = blockPlan(cx);
  const out = [`<path class="iso-halo" d="${k.haloOf(k.insetPlan(plan, 2), SLED_Z, 0.1, P)}" style="filter:blur(4px)"/>`];
  // sled riding the rails, with four bushings
  out.push(S(k.slabOf(k.insetPlan(plan, -2), SLED_Z, BODY_Z - SLED_Z, P, 4, 0.5), { tone: "mid" }));
  out.push(D([[-22, -20], [22, -20], [22, 18], [-22, 18]].map(([dx, dy]) => at([cx + dx, dy, BODY_Z])), { size: 0.45, tone: "lo" }));
  // body with two bands
  const inner = L(k.sideSeam(plan, BODY_Z + 7, P, 4) + k.sideSeam(plan, TOP - 6, P, 4), { tone: "faint" });
  out.push(S(k.slabOf(plan, BODY_Z, BODY_H, P, 4, 0.7), { tone: "hi", crease: "lo", inner }));
  // index plate on the +y face
  out.push(k.faceTextSvg(k.sideMatrix([cx - 5, BY + BD], BODY_Z + 13, P, "left"), String(i + 1).padStart(2, "0"), { size: 5, tone: "mid", anchor: "middle" }));
  // slot on top where entries go in
  out.push(L(k.planOutline({ x: cx - 15, y: 13.3, w: 30, d: 3.4, r: 1.2 }, TOP, P, 3), { tone: "mid" }));
  // two locating pins for the lid
  out.push(D([at([cx - 18, -19, TOP]), at([cx + 18, -19, TOP])], { size: 0.5 }));
  return out.join("");
}

function lid(i) {
  const cx = CX[i];
  const plan = k.insetPlan(blockPlan(cx), -0.6);
  const out = [];
  out.push(S(k.slabOf(plan, TOP, LID_H, P, 4, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(plan, 3.2), TOP + LID_H, P, 3), { tone: "faint" }));
  out.push(D([[-19, -19], [19, -19], [19, 15], [-19, 15]].map(([dx, dy]) => at([cx + dx, dy, TOP + LID_H])), { size: 0.4 }));
  // the seal: a raised disc, its rim notched with this block's fingerprint
  const sz = TOP + LID_H;
  out.push(`<g class="bk-seal" data-part="seal" data-block="${i}">${S(k.cylinder(cx, -2, SEAL_R, sz, 1.6, P, 40, 0.4), { tone: "hi", lit: true })}<path class="bk-seal-tint" d="${k.ring(cx, -2, SEAL_R - 0.3, sz + 1.6, P, 40)}Z"/>${L(sealMarks(cx, sz + 1.6, SEALS[i]), { tone: "hi" })}${L(k.ring(cx, -2, 1.4, sz + 1.6, P, 16), { tone: "mid" })}</g>`);
  return out.join("");
}

// coupling between block i and i+1, on the front faces: a lug on each block and a bar pinned across
const LUG_Z = 15, LUG_H = 9, FRONT = BY + BD;
const lugAt = (x) => S(k.slabOf({ x: x - 4, y: FRONT, w: 8, d: 4, r: 0.8 }, LUG_Z, LUG_H, P, 2, 0.3), { tone: "mid" });
const lugRight = (i) => lugAt(CX[i] + 16);
const lugLeft = (i) => lugAt(CX[i] - 16);
function couplingBar(i) {
  const a = CX[i] + 16, b = CX[i + 1] - 16;
  const z = LUG_Z + LUG_H;
  const bar = { x: a - 4.5, y: FRONT + 0.2, w: b - a + 9, d: 3.6, r: 1.6 };
  const out = [];
  out.push(S(k.slabOf(bar, z, 3, P, 4, 0.4), { tone: "hi", crease: "lo" }));
  out.push(L(k.lineOnTop([bar.x + 7, FRONT + 2], [bar.x + bar.w - 7, FRONT + 2], z + 3, P), { tone: "faint" }));
  for (const x of [a, b]) {
    out.push(S(k.cylinder(x, FRONT + 2, 1.5, z + 3, 1.4, P, 16), { tone: "mid" }));
    out.push(D([at([x, FRONT + 2, z + 4.4])], { size: 0.4 }));
  }
  return out.join("");
}

// entries (slips) that drop into the station block
function slip(j) {
  const cx = STATION;
  const w = 22 - j * 2;
  return S(k.slabOf({ x: cx - w / 2 + (j - 1) * 2, y: 14.3, w, d: 1.4, r: 0.4 }, 0, 16, P, 2), { tone: "hi", crease: "none", lit: j === 2 });
}

// ---- the press over the station -----------------------------------------------------------
const POST_Y = [-38, 32];
const BEAM_Z = 100, BEAM_H = 10;
function postSvg(y) {
  const out = [];
  out.push(S(k.cylinder(STATION, y, 7, 0, 4, P, 28, 0.4), { tone: "mid" }));
  out.push(D(k.pointsAt([[STATION - 5, y, 4], [STATION + 5, y, 4]], P), { size: 0.4 }));
  out.push(S(k.cylinder(STATION, y, 3.8, 4, BEAM_Z - 4, P, 28), { tone: "mid", crease: "none", inner: L([30, 60].map((z) => k.sideArc(STATION, y, 3.8, z, P, 16)).join(""), { tone: "faint" }) }));
  return out.join("");
}
function beam() {
  const out = [];
  const plan = { x: STATION - 8, y: POST_Y[0] - 7, w: 16, d: POST_Y[1] - POST_Y[0] + 14, r: 3 };
  out.push(S(k.slabOf(plan, BEAM_Z, BEAM_H, P, 4, 0.7), { tone: "mid", inner: L(k.sideSeam(plan, BEAM_Z + 5, P, 4), { tone: "faint" }) }));
  out.push(D(POST_Y.map((y) => at([STATION, y, BEAM_Z + BEAM_H])), { size: 0.5 }));
  // cylinder housing with a knurled cap and a little gauge window
  out.push(S(k.cylinder(STATION, -2, 9.5, BEAM_Z + BEAM_H, 14, P, 40, 0.5), { tone: "mid", inner: L(k.sideArc(STATION, -2, 9.5, BEAM_Z + BEAM_H + 4, P, 30), { tone: "faint" }) }));
  out.push(S(k.cylinder(STATION, -2, 7, BEAM_Z + BEAM_H + 14, 4, P, 32), { tone: "mid" }));
  out.push(L(k.knurl(STATION, -2, 7, BEAM_Z + BEAM_H + 14, BEAM_Z + BEAM_H + 18, 40, P), { tone: "lo" }));
  out.push(L(k.ring(STATION, -2, 4.6, BEAM_Z + BEAM_H + 18, P, 24), { tone: "lo" }));
  out.push(D([at([STATION, -2, BEAM_Z + BEAM_H + 18])], { size: 0.55, tone: "hi" }));
  return out.join("");
}
// lid + stamp head + rod move together; the rod slides up into the beam (drawn before the beam)
function pressMoving() {
  const out = [lid(N - 1)];
  const headZ = TOP + LID_H + 1.6;
  out.push(S(k.cylinder(STATION - 0, -2 - 0, 2.8, headZ + 8, BEAM_Z + 2 - headZ - 8, P, 20), { tone: "hi", crease: "none" }));
  // yoke: two arms from the rod down to the lid's front and back edges
  for (const y of [-24, 20]) {
    const arm = { x: STATION - 2, y: Math.min(y, -2), w: 4, d: Math.abs(y + 2), r: 0.8 };
    out.push(S(k.slabOf(arm, headZ + 6, 2.4, P, 2, 0.3), { tone: "mid" }));
  }
  out.push(S(k.cylinder(STATION, -2, 4.2, headZ + 5, 4, P, 24, 0.3), { tone: "mid" }));
  return out.join("");
}

// ---- assemble in painter's order ----------------------------------------------------------
const body = [base(), rack(), rails()];
const POST_BACK = postSvg(POST_Y[0]);
for (let i = 0; i < N; i++) {
  if (i === N - 1) body.push(POST_BACK);
  body.push(`<g data-part="block" data-block="${i}">${blockBody(i)}</g>`);
  if (i < N - 1) body.push(lugRight(i));
  if (i > 0) body.push(lugLeft(i));
  if (i === N - 1) {
    for (let j = 0; j < 3; j++) body.push(`<g data-part="slip" data-slip="${j}" clip-path="url(#slot-clip)" opacity="0"><g data-move>${slip(j)}</g></g>`);
    body.push(`<g data-part="press">${pressMoving()}</g>`);
  } else {
    body.push(`<g data-part="lid" data-block="${i}">${lid(i)}</g>`);
  }
  if (i > 0) body.push(`<g data-part="bar" data-bar="${i - 1}" class="bk-bar">${couplingBar(i - 1)}</g>`);
}
body.push(postSvg(POST_Y[1]));
body.push(beam());

// slips are clipped to what is above the station's top face, at the slot's line
const slotY = 15;
const clipPts = [at([STATION - 40, slotY, TOP]), at([STATION + 40, slotY, TOP])];
const up = 400;
const clip = `<clipPath id="slot-clip"><path d="M${clipPts[0][0]} ${clipPts[0][1]}L${clipPts[1][0]} ${clipPts[1][1]}L${clipPts[1][0]} ${clipPts[1][1] - up}L${clipPts[0][0]} ${clipPts[0][1] - up}Z"/></clipPath>`;

const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "A ledger press on a bench. Five boxes, called blocks, stand on rails in a row, each coupled to the one before it by a bar. The newest block sits under a press: entries drop through its slot, then the press lowers a lid whose seal is a fingerprint of those entries and of the block before. Behind the line, a rack holds five copies of the same chain, each with a lamp. When an old block is opened and changed, its seal stops matching, the couplings after it come loose, and the other copies reject the changed one.",
  body: [`<defs>${clip}</defs>`, ...body],
});

// ---- live: one pure model of time drives every part ----------------------------------------
const live = `
const P = ${JSON.stringify(P)};
const N = ${N}, STROKE = ${STROKE}, TOP = ${TOP}, COPIES = ${COPIES};
const SEALS = ${JSON.stringify(SEALS.map(hex))};
const ENTRIES = ${JSON.stringify(ENTRIES)};
const fnv = ${fnv.toString()};
const hex = ${hex.toString()};
const root = document.querySelector(".iso-stage");
const svg = root.querySelector("svg");
const readout = document.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");
const q = (sel) => [...svg.querySelectorAll(sel)];
const slips = q('[data-part="slip"]'), press = svg.querySelector('[data-part="press"]');
const lids = q('[data-part="lid"]'), bars = q('[data-part="bar"]'), lamps = q('[data-part="lamp"]');
const seals = q('[data-part="seal"]');
const CYCLE = 16;
const sm = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); };
// The model: what every part should be doing at time t of the cycle, when block T is the one edited.
function model(t, T) {
  const s = {};
  s.slip = [0, 1, 2].map((j) => { const t0 = 0.5 + j * 1.15; const f = sm(t0, t0 + 0.9, t); return { z: 40 - f * 26, o: sm(t0 - 0.05, t0 + 0.25, t) * (1 - sm(t0 + 0.85, t0 + 0.9, t)) }; });
  const down = sm(3.9, 4.9, t) * (1 - sm(14.6, 15.6, t));
  s.lift = STROKE * (1 - down);
  s.sealed = down > 0.98;
  s.entries = t < 0.5 ? 0 : t < 1.65 ? 1 : t < 2.8 ? 2 : 3;
  const open = sm(6.4, 7.2, t) * (1 - sm(12.0, 12.8, t));
  s.lid = Array.from({ length: N - 1 }, (_, i) => (i === T ? open * 7 : 0));
  s.edited = open > 0.5;
  s.bar = Array.from({ length: N - 1 }, (_, i) => {
    const seat = i === N - 2 ? 6 * (1 - sm(4.9, 5.4, t)) + 6 * sm(14.6, 15.2, t) : 0;
    const k0 = 7.4 + (i - T) * 0.45;
    const f = i >= T ? sm(k0, k0 + 0.35, t) * (1 - sm(12.2, 12.9, t)) : 0;
    return { z: Math.max(seat, 6 * f), bad: f > 0.3 };
  });
  const vote = sm(8.9, 9.3, t) * (1 - sm(12.2, 12.8, t));
  s.lamps = Array.from({ length: COPIES }, (_, c) => (vote > 0.5 ? (c === 0 ? "bad" : "ok") : s.sealed ? "ok" : "idle"));
  s.phase = t < 3.9 ? "fill" : t < 6.2 ? "seal" : t < 8.9 ? "edit" : t < 12.2 ? "vote" : t < 14.6 ? "heal" : "next";
  return s;
}
const fp = (i, edited, T) => { let prev = "genesis"; let out = ""; for (let b = 0; b <= i; b++) { const list = ENTRIES[b].slice(); if (edited && b === T) list[0] = list[0].replace(/\\d+$/, (n) => String(Number(n) * 10)); const h = fnv(prev + "|" + list.join(";")); out = hex(h); prev = h.toString(16); } return out; };
function say(s, T) {
  const n = N;
  if (s.phase === "fill") return "block " + n + " · entries in: " + s.entries + " of 3";
  if (s.phase === "seal") return "block " + n + " sealed · " + SEALS[n - 1] + " (carries " + SEALS[n - 2] + ")";
  if (s.phase === "edit") return "block " + (T + 1) + " opened · seal " + SEALS[T] + " → " + fp(T, true, T);
  if (s.phase === "vote") return (N - 1 - T) + " coupling" + (N - 1 - T === 1 ? "" : "s") + " loose · " + (COPIES - 1) + " of " + COPIES + " copies reject it";
  if (s.phase === "heal") return "the honest copy stands · chain intact";
  return "press opens for block " + (n + 1);
}
// displayed values follow the model with calm easing, so changing the edited block never pops
const shown = { lid: new Array(N - 1).fill(0), bar: new Array(N - 1).fill(6), lift: STROKE, slip: [0, 0, 0].map(() => ({ z: 46, o: 0 })) };
const follow = (a, b, dt, tau) => a + (b - a) * (1 - Math.exp(-dt / tau));
let T = 1, clock = 0, last = 0, frame = 0, visible = true, held = false, idleTimer = 0;
function apply(s, dt, calm) {
  const ease = (a, b, tau) => (calm ? b : follow(a, b, dt, tau));
  shown.lift = ease(shown.lift, s.lift, 0.08);
  press.setAttribute("transform", translateAlong(P, [0, 0, shown.lift]));
  s.slip.forEach((v, j) => { slips[j].setAttribute("opacity", v.o.toFixed(3)); slips[j].firstElementChild.setAttribute("transform", translateAlong(P, [0, 0, v.z])); });
  lids.forEach((el, i) => { shown.lid[i] = ease(shown.lid[i], s.lid[i], 0.12); el.setAttribute("transform", translateAlong(P, [0, 0, shown.lid[i]])); el.querySelector('[data-part="seal"]').toggleAttribute("data-bad", s.edited && i === T); });
  bars.forEach((el, i) => { shown.bar[i] = ease(shown.bar[i], s.bar[i].z, 0.1); el.setAttribute("transform", translateAlong(P, [0, 0, shown.bar[i]])); el.toggleAttribute("data-bad", !!s.bar[i].bad); });
  seals[N - 1].toggleAttribute("data-dim", !s.sealed);
  lamps.forEach((el, c) => el.setAttribute("data-state", s.lamps[c]));
  const text = say(s, T);
  if (readout && readout.textContent !== text) readout.textContent = text;
  root.setAttribute("aria-valuetext", text);
}
function draw(t, dt = 1 / 30, calm = false) { apply(model(((t % CYCLE) + CYCLE) % CYCLE, T), dt, calm); }
window.ledger = { draw, model, setEdited: (i) => { T = i; }, CYCLE };
function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  if (!held) clock += dt;
  draw(clock, dt, still.matches);
  frame = visible && !window.__recording ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible && !window.__recording) { last = 0; frame = requestAnimationFrame(tick); } };
const holdOn = (i) => { T = Math.max(0, Math.min(N - 2, i)); held = true; clock = 10; clearTimeout(idleTimer); idleTimer = setTimeout(() => { held = false; run(); }, 3600); run(); };
new IntersectionObserver((e) => { visible = e[e.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(root);
root.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  const x = (event.clientX - box.left) / box.width * ${WIDTH}, y = (event.clientY - box.top) / box.height * ${HEIGHT};
  const centres = ${JSON.stringify(CX.slice(0, N - 1).map((cx) => k.iso([cx, -2, TOP], P)))};
  let best = -1, dist = 60;
  centres.forEach(([cx, cy], i) => { const d = Math.hypot(cx - x, cy - y); if (d < dist) { dist = d; best = i; } });
  if (best >= 0) holdOn(best);
});
root.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft" || event.key === "ArrowUp") { holdOn(T - 1); event.preventDefault(); }
  if (event.key === "ArrowRight" || event.key === "ArrowDown") { holdOn(T + 1); event.preventDefault(); }
});
if (still.matches) { held = true; clock = 10; }
draw(clock, 1, true);
run();
`;

const STYLE = `<style>
.iso[data-theme="light"]{
  --anatomy-page:#F6F3E8;--anatomy-card:#FBF9F2;--anatomy-text:#4a5563;--anatomy-strong:#0B1B2B;--anatomy-muted:#7d8794;
  --anatomy-paper:#FBF9F2;--anatomy-face:#ffffff;--anatomy-top:#fffefb;
  --anatomy-shade-0:#ddd8c8;--anatomy-shade-1:#e6e2d4;--anatomy-shade-2:#eeebdf;--anatomy-shade-3:#f5f3ea;
  --anatomy-lit-top:#ffffff;--anatomy-lit-shade:#eef3fb;
  --anatomy-hi:#0B1B2B;--anatomy-mid:#7a8290;--anatomy-lo:#9c9e98;--anatomy-faint:#cfcbbd;--anatomy-lit:#004EBA;
  --anatomy-halo:#6b6450;--anatomy-dot:#2b3442;
  --bk-ok:#5FAE10;--bk-bad:#EC464D;--bk-idle:#c9c6b8;
}
.iso[data-theme="dark"]{--bk-ok:#7ED116;--bk-bad:#EC464D;--bk-idle:#3a3a3a;--anatomy-lit:#7DD2FD}
.bk-lamp-glow{fill:var(--bk-idle);stroke:none;transition:fill .5s var(--anatomy-ease)}
.bk-lamp[data-state="ok"] .bk-lamp-glow{fill:var(--bk-ok)}
.bk-lamp[data-state="bad"] .bk-lamp-glow{fill:var(--bk-bad)}
.bk-seal-tint{fill:var(--anatomy-lit);opacity:.07;stroke:none;transition:fill .4s,opacity .4s}
.bk-seal[data-bad] .bk-seal-tint{fill:var(--bk-bad);opacity:.85}
.bk-seal[data-bad] .iso-line{stroke:#fff}
.bk-seal[data-dim] .bk-seal-tint{opacity:0}
.bk-pin-tint{fill:none;stroke:none}
.bk-bar[data-bad] .iso-solid .iso-top{fill:color-mix(in srgb,var(--bk-bad) 70%,white)}
.bk-bar[data-bad] .iso-solid .iso-edge{stroke:var(--bk-bad)}
.bk-bar .iso-top{transition:fill .35s}
.iso-plate-corner{font-family:Inter,ui-sans-serif,system-ui,sans-serif}
</style>`;

const plate = k.plateHtml({
  fig: "Fig 1",
  title: "Anatomy of a public ledger",
  hint: "Hover a block to open it",
  readout: "block 5 · entries in: 0 of 3",
  keys: [
    { mark: "lit", label: "Seal: a fingerprint of the entries and of the block before" },
    { mark: "raised", label: "Coupling bar: holds only while both seals match" },
    { mark: "green", label: "Copy lamps: five independent copies of the same chain" },
  ],
  caption:
    "Entries drop into the newest block; the press seals it with a fingerprint that includes the previous block's seal, so each block is locked to the one before. Change an old block and its seal no longer matches: every coupling after it comes loose, and the other copies, which still hold the original, outvote the edited one.",
  body: `${STYLE}<div class="iso-stage" tabindex="0" role="slider" aria-label="Ledger press: arrow keys choose which old block to open" aria-valuemin="1" aria-valuemax="4">${svg}</div>`,
});

const page = k.pageHtml({ title: "Anatomy of a public ledger", theme, body: plate, script: kitScript() + live, width: 720 });
writeFileSync(join(HERE, theme === "dark" ? "ledger-press-dark.html" : "ledger-press.html"), page);
writeFileSync(join(HERE, "ledger-figure.json"), JSON.stringify({ svg, style: STYLE, live, P, CX, STATION, TOP, iso: k.ISO_CSS, kit: kitScript(), seals: SEALS.map(hex) }));
console.log("wrote", theme === "dark" ? "ledger-press-dark.html" : "ledger-press.html", "seals", SEALS.map(hex).join(" "));
