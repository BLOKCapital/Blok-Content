#!/usr/bin/env python3
"""Synthesize "Hazel" (variant of Morning Soil, built for the tally-stick carousel): an original, royalty-free lo-fi loop for BLOK carousels.

    python3 scripts/make-music.py assets/music/blok-morning-soil.wav [seconds]

80 BPM (one bar = 3 s, so a 6 s carousel slide = 2 bars). Warm electric piano chords,
soft pad, round bass, brushed drums, a little vinyl. Everything is generated here, so
there are no licensing questions. Master afterwards with ffmpeg (see playbook).
"""
import sys, wave
import numpy as np

SR = 44100
BPM = 80
BEAT = 60 / BPM
BAR = 4 * BEAT
out = sys.argv[1]
LEN = float(sys.argv[2]) if len(sys.argv) > 2 else 32.0
N = int(SR * (LEN + 2))
mix = np.zeros((N, 2))
rng = np.random.default_rng(1834)

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    j = min(N, i + len(sig))
    if i >= N: return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:j, 0] += sig[: j - i] * gain * l
    mix[i:j, 1] += sig[: j - i] * gain * r

def ep(m, dur, vel=1.0):
    """FM electric piano note."""
    t = np.arange(int(SR * (dur + 1.2))) / SR
    f = hz(m)
    idx = 1.8 * vel * np.exp(-t * 3.0)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    s += 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 5)
    env = np.minimum(1, t / 0.004) * np.exp(-t * 1.1)
    rel = np.clip((dur + 1.2 - t) / 1.2, 0, 1)
    return s * env * rel * vel

def pad(m, dur):
    t = np.arange(int(SR * dur)) / SR
    f = hz(m)
    s = sum(np.sin(2 * np.pi * f * k * (1 + d) * t) / k ** 2 for k in (1, 2, 3) for d in (-0.003, 0.003))
    env = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return s * env * 0.5

def bass(m, dur):
    t = np.arange(int(SR * dur)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / 0.01) * np.exp(-t * 1.5) * np.minimum(1, (dur - t) / 0.05)

def kick():
    t = np.arange(int(SR * 0.45)) / SR
    f = 45 + 75 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)

def noise_hit(dur, decay, hp=True):
    n = rng.standard_normal(int(SR * dur))
    if hp: n = np.diff(n, prepend=0)
    # gentle smoothing so it sounds brushed, not harsh
    n = np.convolve(n, np.ones(3) / 3, mode="same")
    t = np.arange(len(n)) / SR
    return n * np.exp(-t * decay)

# Dmaj9 | A/C# | Bm7 | Gmaj7  (key of D, open and woody)
CHORDS = [
    (38, [54, 57, 61, 64]),  # Dmaj9: F# A C# E
    (37, [52, 57, 61, 64]),  # A/C#: E A C# E
    (35, [50, 54, 57, 62]),  # Bm7: D F# A D
    (43, [54, 57, 59, 62]),  # Gmaj7: F# A B D
]
MELODY = [
    [(0.5, 73, 1), (2, 76, 0.5), (2.5, 74, 1.5)],
    [(1, 73, 1), (2.5, 69, 1.5)],
    [(0.5, 71, 1), (1.5, 74, 1), (3, 78, 1)],
    [(1, 76, 2), (3, 74, 1)],
]

def woodblock(m):
    """Short hollow knock: a notch being cut."""
    t = np.arange(int(SR * 0.12)) / SR
    f = hz(m)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t * 55)

bars = int(np.ceil(LEN / BAR))
for b in range(bars):
    root, notes = CHORDS[b % 4]
    t0 = b * BAR
    for k, m in enumerate(notes):  # strum
        add(ep(m, BEAT * 2.2, 0.55), t0 + k * 0.012, 0.22, pan=-0.3 + 0.2 * k)
        add(ep(m, BEAT * 1.2, 0.35), t0 + 2.5 * BEAT + k * 0.01, 0.14, pan=-0.3 + 0.2 * k)
    for m in notes[:3]:
        add(pad(m - 12, BAR + 0.3), t0, 0.05, pan=0)
    add(bass(root, BEAT * 1.8), t0, 0.42)
    add(bass(root + (7 if b % 2 else 12), BEAT * 1.4), t0 + 2.5 * BEAT, 0.3)
    if b >= 2:  # melody enters after the first two bars
        for off, m, ln in MELODY[b % 4]:
            add(ep(m, ln * BEAT, 0.7), t0 + off * BEAT, 0.12, pan=0.35)
    # drums: kick 1 & 3(and), brushed snare 2 & 4, swung hats
    for kb in (0, 2.5):
        add(kick(), t0 + kb * BEAT, 0.55)
    for sb in (1, 3):
        add(noise_hit(0.3, 18, hp=True), t0 + sb * BEAT, 0.07)
    for wb, wm in ((1.5, 84), (3.5, 79)):  # two wood knocks per bar
        add(woodblock(wm), t0 + wb * BEAT, 0.09, pan=0.4)
    for h in range(8):
        sw = 0.08 * BEAT if h % 2 else 0
        add(noise_hit(0.06, 90), t0 + h * BEAT / 2 + sw, 0.035 if h % 2 else 0.05, pan=0.25)

for b in range(bars):
    for q in range(16):
        if q % 4 == 1 or q % 4 == 3 or (q % 8 == 6):
            add(noise_hit(0.018, 260), b * BAR + q * BEAT / 4 + 0.01, 0.05 if q % 2 else 0.03, pan=-0.4)

# vinyl: soft hiss + sparse crackle
hiss = np.convolve(rng.standard_normal(N), np.ones(8) / 8, mode="same") * 0.004
mix += hiss[:, None]
for _ in range(int(LEN * 6)):
    i = rng.integers(0, N - 50)
    mix[i:i + 3] += rng.uniform(-0.05, 0.05)

# fade the very end
fade = int(SR * 1.5)
end = int(SR * LEN)
mix[end - fade:end] *= np.linspace(1, 0, fade)[:, None]
mix[end:] = 0
mix = mix[: end]
mix /= np.max(np.abs(mix)) * 1.12

with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", out, f"{LEN:.1f}s")
