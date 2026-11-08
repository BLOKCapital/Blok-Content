# usage: python -I qa_speech.py final.mp4 lines.json timeline.js  -> prints per-line transcript of the FINAL mix vs script
import sys, json, subprocess, difflib, os, numpy as np, sherpa_onnx
sys.path.insert(0, '/mnt/project-files/brand/voice/brooks-chatterbox'); from common import norm
M = os.path.expanduser('~/.cache/blok-models/sherpa-onnx-whisper-small.en')
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{M}/small.en-encoder.int8.onnx', decoder=f'{M}/small.en-decoder.int8.onnx', tokens=f'{M}/small.en-tokens.txt', num_threads=4)
mp4, L, T = sys.argv[1], json.load(open(sys.argv[2])), json.loads(open(sys.argv[3]).read().split('=', 1)[1].rstrip(';\n '))
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
bad = 0
for i, (l, t) in enumerate(zip(L, T)):
    s, e = int(max(0, t['start'] - 0.15) * 16000), int((t['end'] + 0.3) * 16000)
    st = rec.create_stream(); st.accept_waveform(16000, a[s:e]); rec.decode_stream(st); h = st.result.text.strip()
    want = [w for w in norm(l['say']) if w not in ('f', 'b', 'i')]; got = [w for w in norm(h) if w != 'fbi']
    r = difflib.SequenceMatcher(None, want, got).ratio()
    ok = r >= 0.95; bad += not ok
    print(f"{'OK ' if ok else 'CHECK'} {i:2d} {t['start']:5.2f}s match={r:.2f}\n   want: {l['say']}\n   heard: {h}")
print('lines to check:', bad)
