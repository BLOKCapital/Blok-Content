# Stitch the Gemini TTS takes (takes/t0..t7.wav, 24 kHz mono) into vo.wav:
# trim edges, shorten long internal pauses to 0.38s, join with the script's pauses, then tempo 1.1.
import numpy as np, wave, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); SR = 24000
def rd(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def squeeze(x, maxgap=0.38, thr=10 ** (-40 / 20)):
    env = np.convolve(np.abs(x), np.ones(240) / 240, 'same') > thr
    idx = np.where(env)[0]; x = x[max(0, idx[0] - 600): idx[-1] + 1800]
    env = env[max(0, idx[0] - 600): idx[-1] + 1800]
    out, i, n = [], 0, len(x)
    while i < n:
        if not env[i]:
            j = i
            while j < n and not env[j]: j += 1
            g = j - i; keep = min(g, int(maxgap * SR))
            out.append(x[i:i + keep // 2]); out.append(x[j - (keep - keep // 2):j]); i = j
        else:
            j = i
            while j < n and env[j]: j += 1
            out.append(x[i:j]); i = j
    return np.concatenate(out)
gaps = [0.75, 0.5, 0.6, 0.35, 0.85, 0.45, 0.45, 0.0]   # after each take
parts = [np.zeros(int(0.15 * SR))]
for k in range(8):
    parts += [squeeze(rd(f'{D}/takes/t{k}.wav')), np.zeros(int(gaps[k] * SR))]
x = np.concatenate(parts); x = x / np.abs(x).max() * 0.89
with wave.open(f'{D}/vo_raw.wav', 'wb') as o:
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((x * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/vo_raw.wav', '-af', 'atempo=1.1', '-ar', '48000', f'{D}/vo.wav'], check=True)
os.remove(f'{D}/vo_raw.wav')
print('vo.wav', round(len(x) / SR / 1.1, 2), 's')
