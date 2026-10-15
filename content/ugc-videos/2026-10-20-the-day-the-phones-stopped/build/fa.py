# Forced alignment of vo.wav to script.txt with pocketsphinx (pip install pocketsphinx; model bundled) -> vo.json
# Used instead of Whisper because the sandbox lost the takes and HF downloads are blocked here.
import json, os, re, subprocess, numpy as np
from pocketsphinx import Decoder
D = os.path.dirname(os.path.abspath(__file__))
SPOKEN = {'1987,': 'nineteen eighty seven', '1987.': 'nineteen eighty seven', '1987': 'nineteen eighty seven'}
toks = []  # (display word, [spoken words])
for line in open(f'{D}/script.txt'):
    line = line.split('|')[0].strip()
    if not line: continue
    for w in line.split():
        sp = SPOKEN.get(w) or re.sub(r"[^a-z' -]", '', w.lower().replace('-', ' ')).strip()
        toks.append((w, sp.split()))
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f'{D}/vo.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
d = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
words = [s for _, sp in toks for s in sp]
d.set_align_text(' '.join(words))
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
segs = [(s.word, s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg() if s.word not in ('<s>', '</s>', '<sil>', '[NOISE]') and not s.word.startswith('+')]
segs = [(re.sub(r'\(\d+\)$', '', w), a, b) for w, a, b in segs]
assert len(segs) == len(words), (len(segs), len(words))
out, k = [], 0
for disp, sp in toks:
    a, b = segs[k][1], segs[k + len(sp) - 1][2]; k += len(sp)
    out.append({'w': disp, 's': round(a, 2), 'e': round(b, 2)})
json.dump(out, open(f'{D}/vo.json', 'w'))
print(len(out), 'words; last ends', out[-1]['e'])
