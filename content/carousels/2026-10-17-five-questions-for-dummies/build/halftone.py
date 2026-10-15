import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
src, out, cell, outline, contrast = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
im = Image.open(src).convert('RGBA')
bbox = im.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()
im = im.crop(bbox)
pad = outline + 6
canvas = Image.new('RGBA', (im.width + 2*pad, im.height + 2*pad), (0,0,0,0)); canvas.paste(im, (pad,pad)); im = canvas
alpha = im.getchannel('A')
g = ImageOps.grayscale(Image.alpha_composite(Image.new('RGBA', im.size, (255,255,255,255)), im))
g = ImageEnhance.Contrast(ImageEnhance.Brightness(g).enhance(1.18)).enhance(contrast)
# rotated dot screen (45deg)
W, H = g.size; D = int((W**2 + H**2) ** .5) + cell*2
big = Image.new('L', (D, D), 255); big.paste(g, ((D-W)//2, (D-H)//2))
rot = big.rotate(45, resample=Image.BILINEAR, fillcolor=255)
arr = np.asarray(rot, dtype=np.float32) / 255.0
ss = 3  # supersample
dots = Image.new('L', (D*ss, D*ss), 255); dr = ImageDraw.Draw(dots)
for y in range(0, D, cell):
    for x in range(0, D, cell):
        v = 1 - arr[y:y+cell, x:x+cell].mean()
        if v < 0.04: continue
        r = cell * 0.5 * 1.25 * (v ** 0.62) * ss
        cx, cy = (x + cell/2) * ss, (y + cell/2) * ss
        dr.ellipse((cx-r, cy-r, cx+r, cy+r), fill=0)
dots = dots.resize((D, D), Image.LANCZOS).rotate(-45, resample=Image.BILINEAR, fillcolor=255)
dots = dots.crop(((D-W)//2, (D-H)//2, (D-W)//2 + W, (D-H)//2 + H))
# white sticker outline
a_bin = alpha.point(lambda a: 255 if a > 110 else 0)
grown = a_bin
k = 9
for _ in range(max(1, outline // 4)):
    grown = grown.filter(ImageFilter.MaxFilter(k))
grown = grown.filter(ImageFilter.GaussianBlur(1.5)).point(lambda a: 255 if a > 128 else 0).filter(ImageFilter.GaussianBlur(0.8))
res = Image.new('RGBA', (W, H), (255,255,255,0))
white = Image.new('RGBA', (W, H), (255,255,255,255)); res.paste(white, (0,0), grown)
ink = Image.merge('RGBA', (dots, dots, dots, Image.new('L', (W,H), 255)))
ink = Image.composite(Image.new('RGBA', (W,H),(20,20,20,255)), Image.new('RGBA',(W,H),(255,255,255,255)), ImageOps.invert(dots))
res.paste(ink, (0,0), a_bin.filter(ImageFilter.GaussianBlur(0.7)))
res.save(out)
print(out, res.size)
