# Cut a subject off a plain (white or light grey) studio background: flood-fill from the borders.
import sys, numpy as np
from PIL import Image, ImageFilter
from collections import deque
src, out, tol = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 22
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.int16)
H, W, _ = a.shape
small = 2  # work at half res for speed
b = a[::small, ::small]; h, w, _ = b.shape
bg = np.zeros((h, w), bool); q = deque()
for x in range(w): q.extend([(0, x), (h - 1, x)])
for y in range(h): q.extend([(y, 0), (y, w - 1)])
seen = np.zeros((h, w), bool)
while q:
    y, x = q.popleft()
    if seen[y, x]: continue
    seen[y, x] = True
    c = b[y, x]
    if c.min() < 180: continue
    # neighbours must be close to this pixel (gradient-friendly)
    bg[y, x] = True
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and not seen[ny, nx] and np.abs(b[ny, nx] - c).max() <= tol:
            q.append((ny, nx))
m = Image.fromarray((~bg * 255).astype(np.uint8)).resize((W, H), Image.NEAREST)
m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
rgba = im.convert('RGBA'); rgba.putalpha(m); rgba.save(out); print(out)
