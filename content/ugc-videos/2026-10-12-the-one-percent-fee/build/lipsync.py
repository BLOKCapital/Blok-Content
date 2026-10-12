import sys, os, cv2, numpy as np, torch, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "Wav2Lip"))
import audio as A, face_detection
from models import Wav2Lip
torch.set_num_threads(4)
vid, wav, out = sys.argv[1], sys.argv[2], sys.argv[3]
cap = cv2.VideoCapture(vid); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
print("frames", len(frames), fps, flush=True)
mel = A.melspectrogram(A.load_wav(wav, 16000))
mel_idx_mult = 80. / fps; chunks = []; i = 0
while True:
    s = int(i * mel_idx_mult)
    if s + 16 > mel.shape[1]: chunks.append(mel[:, -16:]); break
    chunks.append(mel[:, s:s+16]); i += 1
n = min(len(frames), len(chunks)); frames = frames[:n]; chunks = chunks[:n]
print("n", n, flush=True)
# face detection on downscaled frames every 2nd frame, interpolate + smooth
det = face_detection.FaceAlignment(face_detection.LandmarksType._2D, flip_input=False, device="cpu")
cache = out + ".boxes.json"
if os.path.exists(cache): boxes = np.array(json.load(open(cache)))
else:
    sc = 0.5; step = 2; idx = list(range(0, n, step)) + ([n-1] if (n-1) % step else []); raw = {}
    t = time.time()
    for b in range(0, len(idx), 8):
        ii = idx[b:b+8]
        imgs = np.array([cv2.resize(frames[k], None, fx=sc, fy=sc) for k in ii])
        preds = det.get_detections_for_batch(imgs)
        for k, p in zip(ii, preds):
            if p is not None: raw[k] = np.array(p[:4]) / sc
        if b % 80 == 0: print("det", b, len(idx), round(time.time()-t), flush=True)
    ks = sorted(raw); arr = np.array([raw[k] for k in ks])
    boxes = np.stack([np.interp(range(n), ks, arr[:, j]) for j in range(4)], 1)
    k = 7; pad = np.pad(boxes, ((k//2, k//2), (0, 0)), mode="edge")
    boxes = np.stack([pad[i:i+k].mean(0) for i in range(n)])
    json.dump(boxes.tolist(), open(cache, "w"))
model = Wav2Lip(); ck = torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Wav2Lip/checkpoints/wav2lip_gan.pth"), map_location="cpu", weights_only=False)
model.load_state_dict({k.replace("module.", ""): v for k, v in ck["state_dict"].items()}); model.eval()
H, W = frames[0].shape[:2]
vw = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
def crop(i):
    x1, y1, x2, y2 = boxes[i]
    h = y2 - y1; y2 = y2 + 0.12 * h  # include chin
    x1, y1, x2, y2 = int(max(0, x1)), int(max(0, y1)), int(min(W, x2)), int(min(H, y2))
    return x1, y1, x2, y2
t = time.time(); bs = 64
for b in range(0, n, bs):
    ids = range(b, min(n, b+bs)); faces = []; cs = []
    for i in ids:
        x1, y1, x2, y2 = crop(i); cs.append((x1, y1, x2, y2))
        faces.append(cv2.resize(frames[i][y1:y2, x1:x2], (96, 96)))
    faces = np.array(faces); masked = faces.copy(); masked[:, 48:] = 0
    inp = np.concatenate((masked, faces), axis=3) / 255.
    mels = np.array([chunks[i] for i in ids])[..., None]
    with torch.no_grad():
        pred = model(torch.FloatTensor(mels).permute(0, 3, 1, 2), torch.FloatTensor(inp).permute(0, 3, 1, 2))
    pred = (pred.permute(0, 2, 3, 1).numpy() * 255.).clip(0, 255).astype(np.uint8)
    for j, i in enumerate(ids):
        x1, y1, x2, y2 = cs[j]; w, h = x2 - x1, y2 - y1
        p = cv2.resize(pred[j], (w, h), interpolation=cv2.INTER_CUBIC)
        orig = frames[i][y1:y2, x1:x2].astype(np.float32)
        # match colour to original
        p = p.astype(np.float32); m = np.zeros((h, w), np.float32)
        cv2.ellipse(m, (w//2, int(h*0.74)), (int(w*0.36), int(h*0.24)), 0, 0, 360, 1, -1)
        m = cv2.GaussianBlur(m, (0, 0), w*0.05)[..., None]
        reg = m[..., 0] > 0.5
        for c in range(3):
            p[..., c] += orig[..., c][reg].mean() - p[..., c][reg].mean()
        # light sharpen of the generated mouth
        bl = cv2.GaussianBlur(p, (0, 0), 1.2); p = cv2.addWeighted(p, 1.6, bl, -0.6, 0)
        f = frames[i].copy(); f[y1:y2, x1:x2] = (orig * (1 - m) + p * m).clip(0, 255).astype(np.uint8)
        vw.write(f)
    print("gen", b, n, round(time.time()-t), flush=True)
vw.release(); print("done")
