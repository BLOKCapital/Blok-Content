"""Original score for the Ambassador quote-post video (30 Oct 2026). 120 BPM, no samples. Usage: python3 music.py music.wav"""
import sys, numpy as np, soundfile as sf
SR = 44100; DUR = 15.5; N = int(SR * DUR); BEAT = .5; OFF = 0.0
L = np.zeros(N); Rr = np.zeros(N)
rng = np.random.default_rng(7)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if j <= i: return
    L[i:j] += sig[:j - i] * g * (1 - max(0, pan)); Rr[i:j] += sig[:j - i] * g * (1 + min(0, pan))
def env(n, a=.005, d=.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def kick(g=1):
    n = int(.45 * SR); t = np.arange(n) / SR; f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * g
def hat(d=.04):
    n = int(.12 * SR); x = rng.standard_normal(n); x = np.diff(np.concatenate([[0], x])); return x * env(n, .001, d) * .25
def snare():
    n = int(.3 * SR); t = np.arange(n) / SR
    return (rng.standard_normal(n) * .5 * np.exp(-t * 18) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)) * .6
def tone(f, d, wave='saw', a=.01, rel=.15):
    n = int(d * SR); t = np.arange(n) / SR
    if wave == 'saw': x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9))
    elif wave == 'sq': x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9, 2))
    else: x = np.sin(2 * np.pi * f * t)
    e = np.minimum(1, t / a) * np.minimum(1, (d - t) / rel).clip(0); return x * e
def lp(x, a=.08):
    y = np.zeros_like(x); s = 0.
    for i in range(0, len(x), 1): s += a * (x[i] - s); y[i] = s
    return y
def pad(freqs, d, g=.12):
    n = int(d * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (-.004, .004): x += np.sin(2 * np.pi * f * (1 + det) * t + np.sin(2 * np.pi * .3 * t))
    e = np.minimum(1, t / .8) * np.minimum(1, (d - t) / 1.0).clip(0); return x * e * g / len(freqs)
def riser(d, g=.5):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.standard_normal(n); y = np.zeros(n); s = 0.
    a = .01 + .5 * (t / d) ** 2
    for i in range(n): s += a[i] * (x[i] - s); y[i] = s
    sw = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (t / d) ** 2) / SR) * .25
    return (y + sw) * (t / d) ** 2 * g
def impact(g=1):
    n = int(2.5 * SR); t = np.arange(n) / SR; f = 30 + 70 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    crash = rng.standard_normal(n) * np.exp(-t * 2.2) * .35
    return (boom + crash) * g
def beats(t0, t1, step=BEAT):
    k = np.ceil((t0 - OFF) / step - 1e-9); out = []
    while OFF + k * step < t1 - 1e-9: out.append(OFF + k * step); k += 1
    return out


A, F, Cc, G = 55.0, 43.65, 65.41, 49.0
PROG = [A, F, Cc, G]
CH = {A: [220, 261.6, 329.6], F: [174.6, 220, 261.6], Cc: [196, 261.6, 329.6], G: [196, 246.9, 293.7]}

# act 1 (0 - 4.75): dry ticks, low drone, a hit on every cross-out
add(pad([55, 82.4, 110], 4.9, .45), 0)
for b in beats(0, 1.5): add(kick(.5), b)
for b in beats(0, 4.75, .25): add(hat(.02), b, .5, .3 if int(b * 4) % 2 else -.3)
for x in (1.5, 2.0, 2.5, 3.0): add(kick(1.0), x); add(snare(), x + .2, .55)
add(riser(1.25, .8), 3.5)
add(impact(1.0), 4.75)

# act 2 (4.75 - 11.25): full groove
for b in beats(4.75, 11.25): add(kick(.95), b)
for i, b in enumerate(beats(4.75, 11.25)):
    if i % 2: add(snare(), b, .55)
for b in beats(4.75, 11.25, .25): add(hat(.03), b, .55, .25)
for i, b in enumerate(beats(4.75, 11.25, 2.0)):
    r = PROG[i % 4]; add(pad(CH[r], 2.1, .25), b)
    for k in range(16):
        f = CH[r][k % 3] * (2 if k % 4 == 3 else 1)
        add(lp(tone(f, .12, 'sq'), .2) * .2, b + k * .125, 1, .4 if k % 2 else -.4)
        if k % 2 == 0: add(lp(tone(r * 2, .12, 'saw'), .1) * .55, b + k * .125)
for x in (6.25, 7.75): add(impact(.45), x)
add(riser(1.0, .5), 10.25)

# act 3 (11.25 - end): lift and end card
add(impact(1.1), 11.25)
add(pad([220, 277.2, 329.6, 440], 2.0, .35), 11.25)
for b in beats(11.25, 13.0, 1.0): add(kick(.7), b)
add(impact(.9), 13.0)
add(pad([110, 220, 277.2, 329.6, 440, 554.4], 2.5, .4), 13.0)

m = np.stack([L, Rr], 1)
fade = np.ones(N); fo = int(.8 * SR); fade[-fo:] = np.linspace(1, 0, fo); m *= fade[:, None]
m /= np.abs(m).max() * 1.12
sf.write(sys.argv[1] if len(sys.argv) > 1 else 'music.wav', m.astype(np.float32), SR)
print('ok', DUR)
