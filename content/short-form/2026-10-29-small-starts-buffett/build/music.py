"""Original cinematic piano bed for this Reel (no licensing): python3 music.py <seconds> <hit_time> out.wav
Piano arpeggios over Am-F-C-G with a soft pad, a riser into the name reveal and a low boom on it."""
import sys, wave, numpy as np
SR = 44100; LEN = float(sys.argv[1]); HIT = float(sys.argv[2]); out = sys.argv[3]
N = int(SR * LEN); mix = np.zeros((N, 2)); rng = np.random.default_rng(11)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if i >= N or j <= i: return
    mix[i:j, 0] += sig[:j - i] * g * np.cos((pan + 1) * np.pi / 4); mix[i:j, 1] += sig[:j - i] * g * np.sin((pan + 1) * np.pi / 4)
def piano(m, dur=2.5, v=1.0):
    t = np.arange(int(SR * dur)) / SR; f = hz(m)
    s = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.6 + k * 0.9)) for k, a in ((1, 1), (2, .45), (3, .2), (4, .08)))
    return s * np.minimum(1, t / 0.003) * np.minimum(1, (dur - t) / 0.3) * v
def pad(m, dur):
    t = np.arange(int(SR * dur)) / SR; f = hz(m)
    s = sum(np.sin(2 * np.pi * f * (1 + d) * t + d * 300) for d in (-0.004, 0, 0.004)) / 3
    s += 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return s * np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
BPM = 84; B = 60 / BPM; BAR = 4 * B
CH = [(45, [57, 60, 64, 69]), (41, [57, 60, 65, 69]), (48, [55, 60, 64, 67]), (43, [55, 59, 62, 67])]
bar = 0; t0 = 0.0
while t0 < LEN:
    root, ns = CH[bar % 4]
    pat = [ns[0], ns[1], ns[2], ns[3], ns[2], ns[1], ns[2], ns[3]]
    for k, m in enumerate(pat):
        add(piano(m + 12, 2.2, 0.8 if k == 0 else 0.55), t0 + k * B / 2 + rng.uniform(0, .01), 0.10, pan=-0.3 + 0.08 * k)
    add(piano(root, 3.5, 1.0), t0, 0.16)
    if t0 > HIT - 0.5:  # after the reveal, add a pad and bass pulse to lift it
        for m in ns[:3]: add(pad(m, BAR + 1.2), t0, 0.035, pan=0)
        add(piano(root - 12, 3, 0.9), t0 + 2 * B, 0.10)
    bar += 1; t0 += BAR
# riser into the reveal, then a boom
rl = 1.6; t = np.arange(int(SR * rl)) / SR
riser = np.convolve(rng.standard_normal(len(t)), np.ones(6) / 6, 'same') * (t / rl) ** 2.5
add(riser, HIT - rl, 0.18)
t = np.arange(int(SR * 2.5)) / SR
boom = np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-t * 12)) / SR) * np.exp(-t * 1.8)
add(boom, HIT, 0.9)
fade = int(SR * 2.0); mix[N - fade:] *= np.linspace(1, 0, fade)[:, None]
mix[:int(SR * .3)] *= np.linspace(0, 1, int(SR * .3))[:, None]
mix /= np.max(np.abs(mix)) * 1.1
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', out)
