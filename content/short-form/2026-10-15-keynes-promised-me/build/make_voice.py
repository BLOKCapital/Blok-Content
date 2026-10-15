import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
T = sys.argv[1]  # tts model dir
k = Kokoro(f"{T}/kokoro.onnx", f"{T}/voices.bin")
VOICE = {"M": ("am_michael", 1.05), "B": ("bm_george", 0.95)}
lines = [l.rstrip("\n").split("\t") for l in open("script.tsv") if l.strip()]
sr = 24000; out = []; tl = []; t = 0.35
out.append(np.zeros(int(sr*0.35), dtype=np.float32))
for i, (who, text) in enumerate(lines):
    v, sp = VOICE[who]
    a, sr = k.create(text.replace("...", ""), voice=v, speed=sp, lang="en-us" if who=="M" else "en-gb")
    a = a.astype(np.float32)
    # trim silence
    idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0]-240): idx[-1]+480]
    a = a / max(1e-6, np.abs(a).max()) * 0.85
    d = len(a)/sr
    tl.append({"who": who, "text": text, "start": round(t, 3), "end": round(t+d, 3)})
    out.append(a); t += d
    gap = 0.28 if who == "M" else 0.42
    if text.startswith("...") or (i+1 < len(lines) and lines[i+1][1].startswith("...")): gap += 0.45
    out.append(np.zeros(int(sr*gap), dtype=np.float32)); t += gap
out.append(np.zeros(int(sr*1.2), dtype=np.float32))
sf.write("vo.wav", np.concatenate(out), sr)
json.dump(tl, open("timeline.json", "w"), indent=1)
print("total", round(t+1.2, 2))
