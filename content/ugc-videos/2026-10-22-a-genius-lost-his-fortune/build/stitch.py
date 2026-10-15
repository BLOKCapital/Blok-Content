# Stitch the Gemini TTS takes (takes/t*.wav, 24 kHz mono) into vo.wav and map the Whisper word
# timings (takes/words.json, per take) onto the stitched timeline -> vo.json.
# Pauses between words are tightened using the word timings (sentence end -> SENT, comma -> COMMA,
# otherwise WORD); takes are joined with the script pause of their last line; then the whole
# track is sped up by TEMPO (ffmpeg atempo keeps pitch).   python3 stitch.py [tempo]
import json, wave, subprocess, sys, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.08
SENT, COMMA, WORD = 0.42, 0.26, 0.2
SR = 24000
TAKES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10], [11], [12, 13], [14, 15], [16, 17]]
# words dropped from a take after recording (take: [first, last] word index): cut 'This is the man who ran the Royal Mint.' for length
DROP = {4: (0, 8)}
pauses = [float(l.split('|')[1]) for l in open(f'{D}/script.txt') if l.strip()]
words = json.load(open(f'{D}/takes/words.json'))
FADE = int(0.006 * SR)
def fade(c):
    c = c.copy()
    if len(c) > 2 * FADE:
        c[:FADE] *= np.linspace(0, 1, FADE); c[-FADE:] *= np.linspace(1, 0, FADE)
    return c
out, omap, pos = [], [], 0
for ti, lines in enumerate(TAKES):
    w = wave.open(f'{D}/takes/t{ti}.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    ws = words[str(ti)]
    if ti in DROP: a, b = DROP[ti]; ws = ws[:a] + ws[b + 1:]
    # cut points: list of (src_start, src_end) segments to keep
    segs = []; s0 = max(0, ws[0]['s'] - 0.08)
    for a, b in zip(ws, ws[1:]):
        gap = b['s'] - a['e']
        tgt = SENT if a['w'][-1:] in '.?!' else COMMA if a['w'][-1:] in ',;:' else WORD
        if gap > tgt:
            segs.append((s0, a['e'] + tgt * 0.6)); s0 = b['s'] - tgt * 0.4
    segs.append((s0, min(len(x) / SR, ws[-1]['e'] + 0.35)))
    for a0, a1 in segs:
        chunk = fade(x[int(a0 * SR):int(a1 * SR)])
        omap.append((ti, a0, a1, pos / SR)); out.append(chunk); pos += len(chunk)
    gap = pauses[lines[-1]] if ti < len(TAKES) - 1 else 0.3
    out.append(np.zeros(int(gap * SR), np.float32)); pos += int(gap * SR)
y = np.concatenate(out)
with wave.open(f'{D}/vo_raw.wav', 'wb') as o:
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/vo_raw.wav', '-af', f'atempo={TEMPO}', '-ar', '48000', f'{D}/vo.wav'], check=True)
def m(ti, t):
    last = None
    for (tk, a0, a1, d0) in omap:
        if tk != ti: continue
        if t < a0: return d0 / TEMPO if last is None else last
        if t <= a1: return (d0 + t - a0) / TEMPO
        last = (d0 + a1 - a0) / TEMPO
    return last
keep = lambda ti: (lambda ws: ws[:DROP[ti][0]] + ws[DROP[ti][1] + 1:] if ti in DROP else ws)(words[str(ti)])
vj = [{'w': wd['w'], 's': round(m(ti, wd['s']), 3), 'e': round(m(ti, wd['e']), 3)} for ti in range(len(TAKES)) for wd in keep(ti)]
json.dump(vj, open(f'{D}/vo.json', 'w'))
print('vo.wav', round(len(y) / SR / TEMPO, 2), 's;', len(vj), 'words')
