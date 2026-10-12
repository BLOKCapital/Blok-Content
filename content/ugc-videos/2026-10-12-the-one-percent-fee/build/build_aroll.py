import json, cv2, numpy as np
E = json.load(open("edl.json")); fps = E["fps"]; N = int(round(E["dur"] * fps))
cache = {}
def frames(c):
    if c not in cache:
        cap = cv2.VideoCapture(f"clips/{c}.mp4"); L = []
        while True:
            ok, f = cap.read()
            if not ok: break
            L.append(f)
        cache[c] = L
    return cache[c]
vw = cv2.VideoWriter("aroll.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (720, 1280))
segmap = []
for name, t0, t1, c, start, rev, z in E["seg"]:
    F = frames(c); a, b = int(round(t0 * fps)), int(round(t1 * fps))
    for k in range(b - a):
        tt = start - k / fps if rev else start + k / fps
        idx = int(np.clip(round(tt * fps), 0, len(F) - 1))
        vw.write(F[idx]); segmap.append(name)
vw.release(); json.dump(segmap, open("segmap.json", "w")); print(len(segmap), N)
