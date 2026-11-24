#!/usr/bin/env python3
"""Original score for "Anyone, 1602": a small storybook piece, all synthesized here (no licensing questions).

    python3 music.py out.wav TOTAL tB tC tD

Sections follow the story: A (0..tB) Amsterdam 1602, a music box and plucked harpsichord over pizzicato bass in D major;
B (tB..tC) the locked-out world, the same melody thinned out over B minor pads; C (tC..tD) "another way in", a lift with
a warm bass pulse and soft brushes; D (tD..end) everyone, the full theme, ending on a long ringing chord.
Soft paper whooshes mark each move between dioramas.
"""
import sys, wave
import numpy as np

SR = 44100
out = sys.argv[1]; TOTAL = float(sys.argv[2]); tB, tC, tD = map(float, sys.argv[3:6])
N = int(SR * (TOTAL + 1)); mix = np.zeros((N, 2)); rng = np.random.default_rng(3)
BPM = 92; BEAT = 60 / BPM; BAR = 4 * BEAT
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:j, 0] += sig[:j - i] * gain * l; mix[i:j, 1] += sig[:j - i] * gain * r

def env(n, a=0.005, d=0.4, s=0.0, r=0.2, dur=None):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4))
    e *= s + (1 - s) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4))
    if dur is not None: e *= np.clip(1 - (t - dur) / r, 0, 1)
    return e

def musicbox(m, dur=1.6):
    n = int(SR * dur); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 6) + 0.18 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 14)
    return s * env(n, 0.002, 0.55)

from functools import lru_cache
@lru_cache(None)
def pluck(m, dur=1.0, bright=0.6):   # Karplus-Strong: harpsichord / pizzicato
    f = hz(m); p = int(SR / f); n = int(SR * dur)
    buf = np.convolve(rng.uniform(-1, 1, p + 4), np.ones(5) / 5, 'valid')[:p] * 1.8; out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.994
    out = out * env(n, 0.001, dur * 0.5); out.flags.writeable = False; return out

def pad(ms, dur, bright=0.3):
    n = int(SR * dur); t = np.arange(n) / SR; s = np.zeros(n)
    for m in ms:
        for det in (-0.07, 0.0, 0.08):
            f = hz(m + det); s += np.sin(2 * np.pi * f * t) + bright * 0.4 * np.sin(2 * np.pi * 2 * f * t)
    a = np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 0.9)
    return s / (3 * len(ms)) * np.clip(a, 0, 1)

def bass(m, dur):
    n = int(SR * dur); t = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * env(n, 0.01, 0.6, 0.3, 0.1, dur - 0.1)

def brush(dur=0.18):
    n = int(SR * dur); x = rng.normal(0, 1, n); x = np.diff(np.concatenate([[0], x]))
    return x * env(n, 0.003, 0.05)

def whoosh(dur=1.2):
    n = int(SR * dur); x = rng.normal(0, 1, n); k = int(SR * 0.004)
    x = np.convolve(x, np.ones(k) / k, 'same'); t = np.arange(n) / n
    return x * np.sin(np.pi * t) ** 2

# harmony: D major I-vi-IV-V (A, C, D), B minor pads (B)
PROG_A = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 55, 59, 62], [45, 52, 57, 61]]   # D Bm G A
PROG_B = [[47, 54, 59, 62], [43, 55, 59, 62], [50, 57, 62, 66], [45, 52, 57, 61]]   # Bm G D A
THEME = [(74, 1), (76, .5), (78, .5), (81, 1.5), (78, .5), (76, 1), (74, 1), (73, 1), (71, 1), (73, 1), (76, 1), (74, 3)]

def theme(t0, end, voice, gain, octave=0):
    t = t0
    while t < end - 0.5:
        for m, d in THEME:
            if t >= end - 0.3: break
            add(voice(m + octave), t, gain, pan=0.25 * np.sin(t)); t += d * BEAT

def chords(t0, end, prog, fn):
    t, i = t0, 0
    while t < end - 0.05:
        fn(prog[i % 4], t, min(BAR, end - t)); t += BAR; i += 1

# A: music box theme + harpsichord broken chords + pizzicato bass
theme(0.4, tB, musicbox, 0.22)
def harps(ch, t, d):
    for k in range(8):
        if t + k * BEAT / 2 < t + d: add(pluck(ch[1 + k % 3] + 12, 0.7), t + k * BEAT / 2, 0.10, pan=-0.3)
    add(pluck(ch[0], 1.0), t, 0.25); add(pluck(ch[0], 1.0), t + 2 * BEAT, 0.18)
chords(0.4, tB, PROG_A, harps)
# B: thinned melody (every other note), long minor pads, slow bass
def padB(ch, t, d): add(pad(ch[1:], d + 0.8, 0.2), t, 0.22); add(bass(ch[0] - 12, d), t, 0.22)
chords(tB, tC, PROG_B, padB)
t = tB + BAR
for j, (m, dd) in enumerate(THEME * 3):
    if t > tC - 1: break
    if j % 2 == 0: add(musicbox(m - 12, 2.2), t, 0.13, pan=0.3)
    t += dd * BEAT * 1.3
# C: the lift: pulse bass, brushes, bright plucks, pad
def lift(ch, t, d):
    add(pad(ch, d + 0.6, 0.5), t, 0.16)
    for k in range(8):
        tk = t + k * BEAT / 2
        if tk < t + d: add(bass(ch[0] - 12 if k % 2 == 0 else ch[0], BEAT / 2), tk, 0.2); add(brush(), tk, 0.025 if k % 2 else 0.04, pan=0.4)
        if tk < t + d and k % 2: add(pluck(ch[2] + 12, 0.5), tk, 0.08, pan=-0.4)
chords(tC, tD, PROG_A, lift)
# D: full theme, octave doubled, then the final ringing chord
def full(ch, t, d): lift(ch, t, d); harps(ch, t, d)
end_music = TOTAL - 3.2
chords(tD, end_music, PROG_A, full)
theme(tD + 0.05, end_music, musicbox, 0.2); theme(tD + 0.05, end_music, lambda m: pluck(m, 0.9), 0.1, -12)
for m in [50, 57, 62, 66, 69, 74]: add(musicbox(m + 12, 3.2), end_music, 0.08); add(pad([m], 3.4, 0.2), end_music, 0.1)
add(bass(38, 3.0), end_music, 0.3)
# paper whooshes at each move between dioramas
for tw in (tB, tC, tD): add(whoosh(1.1), tw - 0.2, 0.05, pan=-0.5)

mix /= max(1e-6, np.abs(mix).max()) / 0.8
fade = np.minimum(1, np.arange(N) / (SR * 0.3)); mix *= fade[:, None]
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', out, TOTAL)
