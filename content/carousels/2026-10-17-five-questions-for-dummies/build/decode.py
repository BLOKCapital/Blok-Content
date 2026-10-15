# decode compact hex cut-out (0-e gray levels, f / [n] = transparent) into an upscaled RGBA PNG
import sys, re, numpy as np
from PIL import Image, ImageFilter
src, out, scale = sys.argv[1], sys.argv[2], int(sys.argv[3])
rows = []
for line in open(src):
    line = line.strip()
    if not line: continue
    line = re.sub(r'\[(\d+)\]', lambda m: 'f'*int(m.group(1)), line)
    rows.append(line)
W = max(len(r) for r in rows)
rows = [r.ljust(W, 'f') for r in rows]
H = len(rows)
g = np.zeros((H, W), np.float32); a = np.zeros((H, W), np.float32)
for y, r in enumerate(rows):
    for x, c in enumerate(r):
        if c == 'f' or c not in '0123456789abcde': g[y, x] = np.nan
        else: g[y, x] = int(c, 16) / 14.0; a[y, x] = 1
# fill transparent gray with nearest-ish average for clean upscale
mask = ~np.isnan(g); fill = np.where(mask, g, 0)
gi = Image.fromarray((fill*255).astype(np.uint8)); mi = Image.fromarray((mask*255).astype(np.uint8))
for _ in range(4):
    b = np.asarray(gi.filter(ImageFilter.BoxBlur(1)), np.float32); m = np.asarray(mi.filter(ImageFilter.BoxBlur(1)), np.float32)
    est = np.where(m > 0, b / np.maximum(m, 1e-3) * 255, 255)
    cur = np.asarray(gi, np.float32); cm = np.asarray(mi, np.float32)
    gi = Image.fromarray(np.where(cm > 0, cur, np.clip(est, 0, 255)).astype(np.uint8)); mi = Image.fromarray(np.where(m > 0, 255, cm).astype(np.uint8))
G = gi.resize((W*scale, H*scale), Image.BICUBIC)
A = Image.fromarray((a*255).astype(np.uint8)).resize((W*scale, H*scale), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale*0.4))
A = A.point(lambda v: 255 if v > 128 else 0)
rgba = Image.merge('RGBA', (G, G, G, A)); rgba.save(out); print(out, rgba.size)
