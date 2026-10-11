#!/usr/bin/env python3
"""Original score + sound design for 'Receipts beat reports' (everything synthesised here, no samples).

    python3 score.py            (run from this build/ folder after vo.wav, timeline.js and cues.json exist)

Writes music.wav (solo piano + soft string pad), sfx.wav (paper, seal, clicks, ticks, chime...) and
mix.wav (voice + ducked music + sfx, 48 kHz stereo, loudness-normalised for social).
The piano turns from B minor to D major at the split screen ("Now, the books.") and resolves on "beat reports".
"""
import json, re, subprocess

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
rng = np.random.default_rng(7)
TL = json.loads(re.sub(r"^window\.TIMELINE = |;$", "", open("timeline.js").read().strip()))
CUES = json.load(open("cues.json"))
S = lambda i: TL[i]["start"]
LAST = TL[-1]["end"]
DUR = np.ceil((LAST + 2.6) * 10) / 10
N = int(DUR * SR) + SR
word = lambda i, w: next(x["s"] for x in TL[i]["words"] if re.sub(r"[^a-z]", "", x["w"].lower()).startswith(w))

def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x)

def lp(x, f, order=2):
    return sosfilt(butter(order, f, "lowpass", fs=SR, output="sos"), x)

def hp(x, f, order=2):
    return sosfilt(butter(order, f, "highpass", fs=SR, output="sos"), x)

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def place(buf, x, t, g=1.0):
    i = int(t * SR)
    if i < 0: x, i = x[-i:], 0
    x = x[: max(0, len(buf) - i)]
    buf[i:i + len(x)] += g * x

def reverb(x, secs=2.4, wet=0.28, damp=5000):
    n = int(secs * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 6.9 / secs)
    ir = lp(ir, damp); ir /= np.sqrt(np.sum(ir ** 2))
    return (1 - wet) * x + wet * fftconvolve(x, ir)[: len(x)]

# ---------------- piano ----------------
def piano(m, dur, vel=0.6):
    f = 440 * 2 ** ((m - 69) / 12)
    n = int((dur + 2.5) * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(1, 11):
        fk = k * f * np.sqrt(1 + 0.00035 * k * k)
        if fk > 12000: break
        dec = 3.2 * (220 / f) ** 0.45 / k ** 0.6
        amp = (1 / k ** 1.25) * (0.6 + 0.4 * vel) ** (k * 0.4)
        y += amp * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.28)) * np.exp(-t / dec)
    y *= np.minimum(1, t / 0.004)
    rel = int(dur * SR)
    if rel < n:  # damper
        y[rel:] *= np.exp(-np.arange(n - rel) / SR / 0.25)
    ham = lp(rng.standard_normal(int(0.02 * SR)), 2500) * np.exp(-np.arange(int(0.02 * SR)) / SR / 0.004) * 0.15
    y[: len(ham)] += ham
    return y * vel * 0.18

def pad(ms, dur):
    n = int((dur + 1.5) * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for m in ms:
        f = 440 * 2 ** ((m - 69) / 12)
        for det in (-0.12, 0.0, 0.12):
            ph = 2 * np.pi * f * 2 ** (det / 12) * t
            y += sum(np.sin(k * ph) / k for k in range(1, 7))
    y = lp(y, 1100, 2)
    a = np.minimum(1, t / 1.2) * np.clip((dur + 1.2 - t) / 1.2, 0, 1)
    return y * a * 0.006

T_TURN = S(7) - 0.3
T_END = word(13, "beat")
L1, L2 = T_TURN / 6, (T_END - T_TURN) / 8
bars = []
pre = [  # bass, mid arpeggio, melody (beat 1, beat 3)
    (47, [54, 57, 62], [74, 73]), (43, [54, 59, 62], [71, 74]), (40, [55, 59, 62], [66, 67]),
    (42, [52, 59, 61], [71, 70]), (47, [54, 57, 62], [74, 76]), (43, [54, 59, 62], [71, 69])]
post = [
    (38, [57, 62, 66], [78, 76]), (49, [57, 61, 64], [76, 73]), (47, [54, 57, 62], [74, 71]),
    (43, [54, 59, 62], [71, 74]), (42, [57, 62, 66], [78, 81]), (40, [55, 59, 62], [79, 76]),
    (43, [54, 59, 62], [74, 71]), (45, [55, 61, 64], [73, 76])]
for i, b in enumerate(pre): bars.append((i * L1, L1, b))
for i, b in enumerate(post): bars.append((T_TURN + i * L2, L2, b))

mus = np.zeros(N)
padbuf = np.zeros(N)
for start, L, (bass, mid, mel) in bars:
    beat = L / 4
    place(mus, piano(bass, L * 0.95, 0.55), start)
    place(mus, piano(bass + 12, L * 0.9, 0.3), start + 0.01)
    for j, pos in enumerate([1, 1.5, 2, 2.5, 3, 3.5]):
        place(mus, piano(mid[j % 3] if j < 3 else mid[(5 - j) % 3], beat * 0.9, 0.32 + 0.04 * (j % 2 == 0)), start + pos * beat + rng.uniform(-0.01, 0.01))
    place(mus, piano(mel[0], beat * 1.9, 0.5), start + 0.02)
    place(mus, piano(mel[1], beat * 1.9, 0.42), start + 2 * beat + 0.02)
    place(padbuf, pad([bass + 12] + mid, L), start)
# final chord, rolled, rings out under the end card
for j, m in enumerate([38, 50, 57, 62, 64, 66, 69, 74]):
    place(mus, piano(m, DUR - T_END + 1, 0.5 if m > 45 else 0.6), T_END + j * 0.045)
place(padbuf, pad([50, 57, 62, 66], DUR - T_END), T_END)
music = reverb(mus + padbuf, 2.6, 0.32)
music[: int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
fade = int(1.2 * SR); e = int(DUR * SR)
music[e - fade:e] *= np.linspace(1, 0, fade); music[e:] = 0

# ---------------- sound effects ----------------
def noise(sec): return rng.standard_normal(int(sec * SR))

def sfx(kind):
    if kind == "whoosh":
        n = noise(0.6); t = np.arange(len(n)) / SR
        x = t / t[-1]
        sweep = bp(n, 250, 1200) * (1 - x) + bp(n, 1200, 6000) * x
        return sweep * np.sin(np.pi * x) ** 2 * 0.55
    if kind == "slide":  # paper sliding on a desk
        n = noise(0.7); t = np.arange(len(n)) / SR
        g = 1 + 0.5 * lp(rng.standard_normal(len(n)), 30)
        return bp(n, 1500, 7000) * g * np.sin(np.pi * t / t[-1]) ** 1.5 * 0.35
    if kind == "thud":  # wax seal / heavy paper
        n = int(0.35 * SR); t = np.arange(n) / SR
        body = np.sin(2 * np.pi * (95 * np.exp(-t * 6) + 45) * t) * np.exp(-t / 0.08)
        return (body * 0.9 + lp(noise(0.35), 900) * env(n, 0.001, 0.02) * 0.6) * 0.7
    if kind == "stamp":
        a = sfx("thud") * 1.1
        b = bp(noise(0.12), 800, 5000) * env(int(0.12 * SR), 0.0005, 0.025) * 0.6
        a[: len(b)] += b
        return a
    if kind == "flip":  # page turn
        out = np.zeros(int(0.45 * SR))
        for k, at in enumerate([0.0, 0.11, 0.2]):
            seg = bp(noise(0.16), 2000 + k * 800, 9000) * env(int(0.16 * SR), 0.01, 0.04)
            place(out, seg, at, 0.45 - 0.1 * k)
        return out
    if kind == "tick":
        n = int(0.03 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 2600 * t) + 0.5 * hp(noise(0.03), 3000)) * np.exp(-t / 0.004) * 0.35
    if kind == "tap":
        n = int(0.06 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 900 * t) * 0.6 + bp(noise(0.06), 1500, 6000)) * np.exp(-t / 0.008) * 0.35
    if kind == "click":  # mouse click: press + release
        out = np.zeros(int(0.1 * SR))
        for at, g in ((0, 0.5), (0.055, 0.32)):
            n = int(0.02 * SR); t = np.arange(n) / SR
            place(out, (hp(noise(0.02), 2500) + np.sin(2 * np.pi * 4200 * t)) * np.exp(-t / 0.0025), at, g)
        return out
    if kind == "key":  # typewriter-ish key
        n = int(0.05 * SR); t = np.arange(n) / SR
        return (bp(noise(0.05), 1800, 7000) * np.exp(-t / 0.006) + np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.015) * 0.4) * (0.3 + 0.1 * rng.random())
    if kind == "type":  # a ledger row landing
        a = sfx("key") * 1.3
        b = sfx("tick") * 0.6
        out = np.zeros(int(0.12 * SR)); place(out, a, 0); place(out, b, 0.04)
        return out
    if kind == "deny":  # soft, low 'locked'
        n = int(0.3 * SR); t = np.arange(n) / SR
        y = (np.sin(2 * np.pi * 220 * t) + 0.6 * np.sin(2 * np.pi * 165 * t)) * np.exp(-t / 0.07)
        y[int(0.12 * SR):] += ((np.sin(2 * np.pi * 220 * t) + 0.6 * np.sin(2 * np.pi * 165 * t)) * np.exp(-t / 0.07))[: n - int(0.12 * SR)]
        return y * 0.18
    if kind == "pen":  # nib scratch for underlines
        n = noise(0.45); t = np.arange(len(n)) / SR
        am = 0.6 + 0.4 * np.sin(2 * np.pi * 14 * t) ** 2
        return bp(n, 3000, 9000) * am * np.sin(np.pi * t / t[-1]) * 0.12
    if kind == "print":  # receipt printer
        n = int(0.85 * SR); t = np.arange(n) / SR
        buzz = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.3 + bp(noise(0.85), 2000, 6000) * 0.5
        gate = (np.sin(2 * np.pi * 24 * t) > -0.2).astype(float)
        return lp(buzz * gate, 5000) * np.sin(np.pi * t / t[-1]) ** 0.5 * 0.22
    if kind in ("ding", "chime"):
        notes = [1318.5] if kind == "ding" else [587.3, 880.0, 1174.7, 1760.0]
        n = int((1.2 if kind == "ding" else 3.0) * SR); t = np.arange(n) / SR
        y = np.zeros(n)
        for j, f in enumerate(notes):
            d = int(j * 0.06 * SR)
            for k, (r, a) in enumerate(((1, 1), (2.76, 0.35), (5.4, 0.15))):
                y[d:] += a * np.sin(2 * np.pi * f * r * t[: n - d]) * np.exp(-t[: n - d] / (0.9 / (k + 1) * (1 if kind == "ding" else 2)))
        return y * (0.12 if kind == "ding" else 0.09) * np.minimum(1, t / 0.003)
    raise ValueError(kind)

# per-sound balance, set by measuring peaks against the voice
MIXGAIN = {"pen": 2.5, "whoosh": 1.4, "key": 1.5, "click": 0.8, "thud": 1.5, "stamp": 1.3, "deny": 1.3}
fx = np.zeros(N)
for c in CUES:
    place(fx, sfx(c["s"]), c["t"], c["g"] * MIXGAIN.get(c["s"], 1))
fx = reverb(fx, 1.2, 0.18, 7000)

# ---------------- mix ----------------
def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)

vo = np.zeros(N); v = load("vo.wav"); vo[: len(v)] = v[:N]
vo = hp(vo, 70)
vo *= 0.7 / np.max(np.abs(vo))
# duck music under the voice
e = np.sqrt(lp(vo ** 2, 6, 1).clip(0))
duck = 1 - 0.55 * np.clip(e / (np.max(e) * 0.25), 0, 1)
duck = lp(duck, 3, 1)
music_n = music / np.max(np.abs(music)) * 0.22
fx_n = fx / np.max(np.abs(fx)) * 0.32

def stereo(x, width=0.0, delay_ms=0):
    d = int(delay_ms * SR / 1000)
    r = np.concatenate([np.zeros(d), x])[: len(x)]
    return np.stack([x, (1 - width) * x + width * r])

mix = stereo(vo) + stereo(music_n * duck, 1.0, 11) + stereo(fx_n, 0.6, 4)
mix = mix[:, : int(DUR * SR)]

def write(path, x):
    x = np.atleast_2d(x)
    pcm = (np.clip(x.T, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", str(x.shape[0]), "-i", "-", path], input=pcm, check=True)

write("music.wav", music_n[: int(DUR * SR)])
write("sfx.wav", fx_n[: int(DUR * SR)])
write("mix-raw.wav", mix / np.max(np.abs(mix)) * 0.9)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "mix-raw.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "mix.wav"], check=True)
print(f"music turn {T_TURN:.2f}s, resolve {T_END:.2f}s, duration {DUR}s, {len(CUES)} cues")
