# Original score + SFX synthesised from cues.json, mixed under vo.wav -> mix.wav (no samples, no licences)
import json, wave, subprocess, numpy as np
from scipy.signal import butter, sosfilt
D = __import__('os').path.dirname(__file__) or '.'
SR = 48000
cues = json.load(open(f'{D}/cues.json'))
dur = cues['duration']; L = cues['lines']; N = int(dur * SR) + SR
rng = np.random.default_rng(7)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def env(n, a, r): e = np.ones(n); ai = int(a * SR); ri = int(r * SR); e[:ai] = np.linspace(0, 1, ai) if ai else 1; e[-ri:] *= np.exp(-np.linspace(0, 5, ri)) if ri else 1; return e
def put(buf, t, x, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x));
    if i < len(buf): buf[i:j] += x[:j - i] * g
t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

# --- music bed: slow detuned pad, D minor -> warmer D major at "here's the idea" ---
pad = np.zeros(N); idea = L[cues['idea']] - 0.3
def chord(notes, s, e, g):
    n = int((e - s) * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for m in notes:
        for d in (-0.08, 0.0, 0.07):
            x += np.sin(2 * np.pi * hz(m + d) * tt + rng.uniform(0, 6)) * (0.6 if m < 50 else 0.35)
    x *= env(n, 2.5, 2.5) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.12 * tt))
    put(pad, s, x, g)
prog1 = [[38, 50, 53, 57], [34, 50, 53, 58], [36, 48, 52, 55], [33, 49, 52, 57]]  # Dm Bb C A
s = 0.0; k = 0
while s < idea:
    e = min(s + 8, idea + 2); chord(prog1[k % 4], s, e, 0.05); s += 7; k += 1
prog2 = [[38, 50, 54, 57], [43, 50, 55, 59], [45, 52, 57, 61], [38, 50, 54, 57, 62]]  # D G A D
s = idea; k = 0
while s < dur:
    e = min(s + 8, dur); chord(prog2[k % 4], s, e, 0.05); s += 7; k += 1
pad = lp(pad, 1400)
# soft felt-piano plucks on the idea section (one per chord)
def pluck(m, g=0.12):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * hz(m) * h * tt) / h ** 1.6 for h in (1, 2, 3, 4)) * np.exp(-tt * 2.2)
    return lp(x, 2500) * g
for k, s0 in enumerate(np.arange(idea, dur - 3, 3.5)):
    put(pad, s0, pluck([62, 66, 69, 74, 69, 66][k % 6]))
put(pad, cues['end'] + 0.1, pluck(62, .16)); put(pad, cues['end'] + 0.1, pluck(69, .12)); put(pad, cues['end'] + 0.1, pluck(74, .1))

# --- room tone ---
room = lp(rng.standard_normal(N), 300) * 0.012

# --- tension pulse while the book fills up ---
fx = np.zeros(N)
def thump(g=0.5):
    n = int(0.35 * SR); tt = np.arange(n) / SR; f = 55 * np.exp(-tt * 6) + 38
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * g
ta, tb = cues['tension']
for s0 in np.arange(L[ta], L[tb], 1.0): put(fx, s0, thump(0.22))

def whoosh(g):
    n = int(0.45 * SR); x = rng.standard_normal(n); tt = np.linspace(0, 1, n)
    y = np.zeros(n)
    for a in range(0, n, 2400):
        seg = x[a:a + 2400]; fc = 300 + 3500 * np.sin(np.pi * tt[a]) ** 2
        y[a:a + len(seg)] = bp(seg, max(80, fc * .6), fc * 1.4)
    return y * np.sin(np.pi * tt) ** 2 * g
def buzz(g):
    out = np.zeros(int(1.1 * SR))
    for a in (0, 0.5):
        n = int(0.32 * SR); tt = np.arange(n) / SR
        x = np.sign(np.sin(2 * np.pi * 165 * tt)) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * tt))
        put(out, a, lp(x, 900) * env(n, .01, .05) * g)
    return out
def quill(g):
    n = int(0.9 * SR); out = np.zeros(n)
    for a in np.arange(0, 0.8, 0.13) + rng.uniform(0, .03, 7)[:len(np.arange(0, 0.8, 0.13))]:
        m = int(rng.uniform(.06, .11) * SR); tt = np.linspace(0, 1, m)
        put(out, a, bp(rng.standard_normal(m), 2500, 7000) * np.sin(np.pi * tt) ** 2 * g)
    return out
def blip(f0, f1, g, d=0.09):
    n = int(d * SR); tt = np.arange(n) / SR; f = np.linspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30) * g
def boom(g):
    n = int(2.2 * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(48 * np.exp(-tt * 1.5) + 32) / SR) * np.exp(-tt * 1.8)
    return (x + lp(rng.standard_normal(n), 200) * np.exp(-tt * 4) * .4) * g
def rise(g):
    n = int(1.4 * SR); tt = np.linspace(0, 1, n); x = rng.standard_normal(n)
    return hp(lp(x, 4000), 400) * tt ** 3 * g
def bell(f, g):
    n = int(1.6 * SR); tt = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (3 + h)) / h for h in (1, 2.76, 5.4)) * g
def key_click(g):
    n = int(0.03 * SR); return hp(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / SR * 220) * g

for c in cues['cues']:
    k, s0 = c['k'], c['t']
    if k == 'cut': put(fx, s0 - 0.2, whoosh(0.05))
    elif k == 'quill': put(fx, s0, quill(0.10))
    elif k == 'pop': put(fx, s0, blip(700, 1100, 0.09))
    elif k == 'hit': put(fx, s0, boom(0.25)); put(fx, s0, bell(660, .05))
    elif k == 'boom': put(fx, s0, boom(0.32))
    elif k == 'rise': put(fx, s0 - 1.4, rise(0.05))
    elif k == 'tick': put(fx, s0, blip(1500, 1500, 0.05, .05))
    elif k == 'ding': put(fx, s0, bell(1320, .07))
    elif k == 'chime': put(fx, s0, bell(880, .06)); put(fx, s0 + .12, bell(1320, .04))
last = -1
for ty in cues['typing']:
    if ty - last > 0.055: put(fx, ty + rng.uniform(0, .02), key_click(rng.uniform(.10, .16))); last = ty

# --- voice + ducking ---
w = wave.open(f'{D}/vo.wav'); vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
vo = vo / (np.abs(vo).max() + 1e-9) * 0.8
ve = lp(np.abs(vo), 4); ve = ve / (ve.max() + 1e-9)
duck = 1 - 0.55 * np.clip(ve * 6, 0, 1)
mix = vo + (pad * duck + room) + fx
mix = mix[:int(dur * SR)]
mix /= np.abs(mix).max() / 0.95
st = np.stack([mix, mix], 1)
with wave.open(f'{D}/premix.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((st * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/premix.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=11', '-ar', '48000', f'{D}/mix.wav'], check=True)
print('mix.wav', round(dur, 2), 's')
