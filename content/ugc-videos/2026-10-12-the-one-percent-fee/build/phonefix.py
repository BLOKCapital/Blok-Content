import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
F = "/usr/share/fonts/opentype/inter/Inter-"
def f(w, s): return ImageFont.truetype(F + w + ".otf", s)
SW, SH = 640, 1400
ui = Image.new("RGB", (SW, SH), (250, 249, 245)); d = ImageDraw.Draw(ui)
INK, MUT, IND, LIME = (20, 22, 28), (120, 124, 132), (0, 78, 186), (126, 209, 22)
d.text((40, 120), "My portfolio", font=f("Bold", 44), fill=INK)
d.text((40, 185), "Total value", font=f("Medium", 28), fill=MUT)
d.text((40, 222), "$12,480.22", font=f("ExtraBold", 78), fill=INK)
d.text((40, 318), "Every holding, trade and fee on record", font=f("Medium", 24), fill=IND)
# allocation bar
x = 40
for w, c in [(0.6, (0, 78, 186)), (0.3, (125, 210, 253)), (0.1, (126, 209, 22))]:
    d.rounded_rectangle((x, 380, x + int(560 * w) - 6, 404), 10, fill=c); x += int(560 * w)
rows = [("Global stocks", "60%", (0, 78, 186)), ("Bonds", "30%", (125, 210, 253)), ("Gold", "10%", (126, 209, 22))]
y = 450
for n, p, c in rows:
    d.ellipse((40, y + 8, 64, y + 32), fill=c); d.text((82, y), n, font=f("SemiBold", 32), fill=INK)
    d.text((600 - d.textlength(p, font=f("Bold", 32)), y), p, font=f("Bold", 32), fill=INK); y += 70
d.line((40, y + 10, 600, y + 10), fill=(225, 223, 215), width=2); y += 40
d.text((40, y), "Activity", font=f("Bold", 34), fill=INK); y += 64
for a, b in [("Rebalance", "fee $0.04"), ("Deposit", "$500.00"), ("Rebalance", "fee $0.03")]:
    d.text((40, y), a, font=f("SemiBold", 30), fill=INK); d.text((40, y + 40), "Verified on record  ✓", font=f("Medium", 22), fill=(80, 150, 20))
    d.text((600 - d.textlength(b, font=f("SemiBold", 30)), y), b, font=f("SemiBold", 30), fill=INK); y += 100
uiA = cv2.cvtColor(np.array(ui), cv2.COLOR_RGB2BGR)
im = cv2.imread("clips/phone.png"); H, W = im.shape[:2]
dst = np.float32([[525, 752], [822, 758], [784, 1438], [468, 1428]])
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [SW, 0], [SW, SH], [0, SH]]), dst)
warp = cv2.warpPerspective(uiA, M, (W, H), flags=cv2.INTER_CUBIC)
mask = np.zeros((H, W), np.float32); cv2.fillConvexPoly(mask, dst.astype(np.int32), 1)
# keep the thumbs/fingers that cover the screen (skin-coloured pixels inside these zones)
ycc = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb).astype(np.float32)
skin = ((ycc[..., 1] > 138) & (ycc[..., 1] < 168) & (ycc[..., 2] > 94) & (ycc[..., 2] < 130) & (ycc[..., 0] < 222)).astype(np.uint8)
skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)); skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
zone = np.zeros((H, W), np.uint8)
for poly in [[(690, 1060), (850, 1060), (850, 1300), (690, 1300)], [(430, 1300), (600, 1300), (600, 1470), (430, 1470)], [(430, 860), (540, 860), (540, 1020), (430, 1020)]]:
    cv2.fillPoly(zone, [np.int32(poly)], 1)
mask[(skin * zone) > 0] = 0
mask = cv2.GaussianBlur(mask, (0, 0), 2.0)[..., None]
# match brightness/softness of the photo
warp = cv2.GaussianBlur(warp, (0, 0), 0.8).astype(np.float32) * 0.93
out = im.astype(np.float32) * (1 - mask) + warp * mask
# faint glare
g = np.zeros((H, W), np.float32); cv2.fillConvexPoly(g, np.int32([[520, 742], [700, 745], [520, 1000]]), 1)
g = cv2.GaussianBlur(g, (0, 0), 40)[..., None] * mask * 18
cv2.imwrite("clips/phone_fixed.png", (out + g).clip(0, 255).astype(np.uint8))
c = (out + g).clip(0, 255).astype(np.uint8)[650:1550, 400:950]; cv2.imwrite("phone_fix_check.jpg", c)
