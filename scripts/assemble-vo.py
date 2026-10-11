#!/usr/bin/env python3
"""Stitch per-line voiceover clips (from scripts/sandbox/voiceover-lines.py) into one take with hand-set pauses.

    python3 scripts/assemble-vo.py <lines-dir> <out-prefix> [lead=0.15] [gap,gap,...]

Each clip is trimmed to its spoken words (+ a short tail), placed on a timeline with the given pause after
each line (default 0.4s), and written as <out-prefix>.wav (48 kHz mono) and <out-prefix>.json (absolute word
timings, same format as voiceover.py, so scripts/build-timeline.py works unchanged).
"""
import glob, json, subprocess, sys

import numpy as np

SR = 48000
d, out = sys.argv[1], sys.argv[2]
lead = float(sys.argv[3]) if len(sys.argv) > 3 else 0.15
mp3s = sorted(glob.glob(f"{d}/line-*.mp3"))
gaps = [float(g) for g in sys.argv[4].split(",")] if len(sys.argv) > 4 else []
gaps += [0.4] * (len(mp3s) - len(gaps))

def load(p):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

parts, words, t = [np.zeros(int(lead * SR), np.float32)], [], lead
for i, p in enumerate(mp3s):
    a, ws = load(p), json.load(open(p[:-4] + ".json"))
    s0, s1 = max(0, ws[0]["s"] - 0.06), min(len(a) / SR, ws[-1]["e"] + 0.16)
    clip = a[int(s0 * SR):int(s1 * SR)].copy()
    f = int(0.01 * SR); clip[:f] *= np.linspace(0, 1, f); clip[-f:] *= np.linspace(1, 0, f)
    words += [{"w": w["w"], "s": round(t + w["s"] - s0, 3), "e": round(t + w["e"] - s0, 3)} for w in ws]
    parts.append(clip); t += len(clip) / SR
    pad = gaps[i] if i < len(mp3s) - 1 else 0.0
    parts.append(np.zeros(int(pad * SR), np.float32)); t += pad

audio = np.concatenate(parts)
pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", out + ".wav"],
               input=pcm, check=True)
json.dump(words, open(out + ".json", "w"))
print(f"{out}.wav {len(audio)/SR:.2f}s, {len(words)} words")
