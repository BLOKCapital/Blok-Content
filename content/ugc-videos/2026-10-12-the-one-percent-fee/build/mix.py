import numpy as np, subprocess, json
from scipy.signal import butter, sosfilt
SR = 44100; VO_DUR = 56.03; TOT = VO_DUR + 2.6; N = int(TOT * SR)
vo = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "vo_7.mp3", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
rng = np.random.default_rng(3)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, "lowpass", fs=SR, output="sos"), x)
def db(x): return 10 ** (x / 20)
t = np.arange(N) / SR
mix = np.zeros(N, np.float32); mix[:len(vo)] += vo[:N] * 1.0
# car interior: low rumble + muffled street
rumble = lp(np.cumsum(rng.standard_normal(N)) * 0.02, 120); rumble /= np.abs(rumble).max()
street = bp(rng.standard_normal(N), 250, 1800); street /= np.abs(street).max()
mod = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9.0 + 1.3)
amb = rumble * db(-34) + street * db(-44) * mod
# passing cars outside (filtered noise swells)
for c in [3.2, 10.5, 16.8, 24.4, 31.0, 39.5, 47.2, 53.0]:
    L = int(3.2 * SR); s = int(c * SR); e = min(N, s + L)
    env = np.hanning(L)[: e - s] ** 2
    amb[s:e] += bp(rng.standard_normal(e - s), 150, 900)[: e - s] * env * db(-36)
# soft pad bed (warm chords), ducked under voice
def chord(fs, a, b):
    seg = np.zeros(N); s, e = int(a * SR), int(b * SR); tt = t[s:e]
    env = np.minimum(1, (tt - a) / 1.5) * np.minimum(1, (b - tt) / 1.5)
    for f in fs:
        seg[s:e] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 0.5)) * env
    return seg
prog = [[220, 277.2, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 293.7]]
pad = np.zeros(N); k = 0; x = 0.0
while x < TOT:
    pad += chord(prog[k % 4], x, min(TOT, x + 4.2)); x += 4.0; k += 1
pad = lp(pad, 1800); pad /= np.abs(pad).max()
venv = np.abs(np.concatenate([vo, np.zeros(max(0, N - len(vo)))]))[:N]
venv = lp(venv, 4) ; venv /= venv.max()
duck = 1 - 0.55 * np.clip(venv * 3, 0, 1)
mix += pad * db(-30) * duck + amb
# pops when card lines appear, whoosh into inserts, chime on end card
def pop(at, f=880, g=-24):
    L = int(0.09 * SR); s = int(at * SR); tt = np.arange(L) / SR
    mix[s:s + L] += np.sin(2 * np.pi * f * tt * (1 + 2 * tt)) * np.exp(-tt * 45) * db(g)
for a, f in [(10.1, 660), (15.5, 880), (21.2, 880), (23.0, 520)]: pop(a, f)
for a in [35.3, 41.1]:
    L = int(0.45 * SR); s = int((a - 0.3) * SR); env = np.hanning(L)
    mix[s:s + L] += bp(rng.standard_normal(L), 600, 5000) * env * db(-30)
for f, d in [(880, 0), (1318.5, 0.12)]:
    L = int(1.8 * SR); s = int((VO_DUR + 0.1 + d) * SR); tt = np.arange(L) / SR
    mix[s:s + L] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3) * db(-26)
fade = int(0.8 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = np.clip(mix, -1, 1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "mix.wav"], input=mix.astype(np.float32).tobytes())
print("ok")
