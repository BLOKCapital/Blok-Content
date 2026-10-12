import json, subprocess, sys, numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FPS = 30; W, H = 1080, 1920
E = json.load(open("edl.json")); VO = E["dur"]; END = 2.6; TOT = VO + END; N = int(round(TOT * FPS))
src = sys.argv[1]; out = sys.argv[2]; preview = [float(x) for x in sys.argv[3:]]
F = "/usr/share/fonts/opentype/inter/Inter-"
def font(w, s): return ImageFont.truetype(F + w + ".otf", s)
LIME, INDIGO, CORAL, LINEN, SKY = (126, 209, 22), (0, 78, 186), (236, 70, 77), (246, 243, 232), (125, 210, 253)
# ---------- captions ----------
words = json.load(open("words.json"))
tok = []
for w, a, b in words:
    if tok and (w.startswith(",") or w.startswith("%") or w.startswith("-")):
        tok[-1][0] += w; tok[-1][2] = b
    else: tok.append([w, a, b])
for t in tok:
    t[0] = t[0].replace("on-chain", "on-chain").replace("maths,", "maths.").replace("phone,", "phone.").replace("report,", "report.")
chunks = []; cur = []
for i, t in enumerate(tok):
    cur.append(t)
    gap = tok[i+1][1] - t[2] if i + 1 < len(tok) else 9
    if t[0][-1] in ".,?!" or len(cur) >= 3 or gap > 0.35: chunks.append(cur); cur = []
if cur: chunks.append(cur)
for k, c in enumerate(chunks):
    c_end = chunks[k+1][0][1] if k + 1 < len(chunks) else c[-1][2] + 0.4
    c.append(min(c_end, c[-1][2] + 0.6))
CF = font("Black", 74)
def draw_caption(img, t, y):
    for c in chunks:
        if c[0][1] - 0.05 <= t < c[-1]:
            ws = c[:-1]; d = ImageDraw.Draw(img)
            parts = [w[0].rstrip(",") for w in ws]; sp = 22
            widths = [d.textlength(p, font=CF) for p in parts]
            total = sum(widths) + sp * (len(parts) - 1); x = (W - total) / 2
            age = t - c[0][1]; s = 1 + 0.08 * max(0, 1 - age / 0.12)
            for p, wd, w in zip(parts, widths, ws):
                col = LIME if w[1] - 0.03 <= t < w[2] + 0.05 else (255, 255, 255)
                d.text((x, y), p, font=CF, fill=col, stroke_width=9, stroke_fill=(0, 0, 0), anchor="lt")
                x += wd + sp
            return
# ---------- inserts ----------
ins = {}
for k, a, b in E["inserts"]:
    im = Image.open(f"clips/{k}_fixed.png" if k == "phone" else f"clips/{k}.png").convert("RGB"); ins[k] = (a, b, im)
def insert_frame(k, t):
    a, b, im = ins[k]; p = (t - a) / (b - a)
    z0 = {"kitchen": 1.24, "phone": 1.10, "stmt": 1.06}[k]
    z = z0 + 0.08 * p; iw, ih = im.size; cw, ch = iw / z, ih / z
    cx = iw / 2 + (p - 0.5) * 40 + 6 * math.sin(t * 2.1); cy = ih / 2 + 5 * math.cos(t * 1.7)
    if k == "kitchen": cy = min(cy, 1680 - ch / 2)
    if k == "phone": cy = 1100
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize((W, H), Image.LANCZOS, box=box)
# ---------- A-roll ----------
segs = E["seg"]
def zoom_for(t):
    for s in segs:
        if s[1] <= t < s[2]: return s[6]
    return 1.0
cap = cv2.VideoCapture(src)
def aroll(fr, t):
    z = zoom_for(t); h0, w0 = fr.shape[:2]; cw, ch = w0 / z, h0 / z
    cx = w0 / 2; cy = min(max(0.41 * h0, ch / 2), h0 - ch / 2)
    x1, y1 = int(cx - cw / 2), int(cy - ch / 2)
    crop = fr[y1:y1 + int(ch), x1:x1 + int(cw)]
    up = cv2.resize(crop, (W, H), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(up, (0, 0), 1.4); up = cv2.addWeighted(up, 1.35, bl, -0.35, 0)
    return Image.fromarray(cv2.cvtColor(up, cv2.COLOR_BGR2RGB))
# ---------- overlays ----------
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def hook(img, t):
    if t > 2.55: return
    d = ImageDraw.Draw(img); f = font("ExtraBold", 54)
    lines = ["Your fund's 1% fee", "isn't small."]
    a = ease(t / 0.25); y = 210
    for ln in lines:
        tw = d.textlength(ln, font=f); x = (W - tw) / 2
        d.rounded_rectangle((x - 26, y - 14, x + tw + 26, y + 70), 18, fill=(255, 255, 255))
        d.text((x, y), ln, font=f, fill=(15, 15, 15)); y += 92
CARD = [(10.1, "$10,000 · 7% a year · 30 years", font("SemiBold", 42), (40, 40, 40)),
        (15.5, "No fee   →   $76,123", font("ExtraBold", 60), INDIGO),
        (21.2, "1% fee   →   $57,435", font("ExtraBold", 60), INDIGO),
        (23.0, "Lost to fees: $18,688", font("Black", 66), CORAL)]
def card(img, t):
    if not (10.1 <= t < 27.6): return False
    a = ease((t - 10.1) / 0.3) * (1 - ease((t - 27.3) / 0.3))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    y0 = 120 - int((1 - a) * 60); x0, x1 = 70, W - 70
    shown = [c for c in CARD if t >= c[0]]
    hh = 40 + sum(72 if c[2].size < 50 else 92 for c in shown) + 52
    d.rounded_rectangle((x0, y0, x1, y0 + hh), 34, fill=(255, 255, 255, int(240 * a)))
    y = y0 + 34
    for (ts, txt, f, col) in shown:
        p = ease((t - ts) / 0.22); tw = d.textlength(txt, font=f)
        d.text(((W - tw) / 2, y + (1 - p) * 20), txt, font=f, fill=col + (int(255 * a * p),))
        y += 72 if f.size < 50 else 92
    fs = font("Medium", 27); s = "Illustrative maths, not a forecast."
    d.text(((W - d.textlength(s, font=fs)) / 2, y + 4), s, font=fs, fill=(120, 120, 120, int(255 * a)))
    img.paste(ov, (0, 0), ov); return True
LOGO = Image.open("logo-wordmark.png").convert("RGBA")
def endcard(t):
    img = Image.new("RGB", (W, H), LINEN); d = ImageDraw.Draw(img)
    lw = 560; lg = LOGO.resize((lw, int(LOGO.size[1] * lw / LOGO.size[0])), Image.LANCZOS)
    img.paste(lg, ((W - lw) // 2, 700), lg)
    f = font("ExtraBold", 66); s = "Receipts beat reports."
    d.text(((W - d.textlength(s, font=f)) / 2, 700 + lg.size[1] + 70), s, font=f, fill=INDIGO)
    f3 = font("Bold", 40); s3 = "Follow @blok.capital"
    d.text(((W - d.textlength(s3, font=f3)) / 2, 1130), s3, font=f3, fill=(40, 40, 40))
    f2 = font("Medium", 28)
    for k, s2 in enumerate(["Educational content only, not financial or investment advice.", "On-chain assets can be volatile and you can lose money.", "AI-generated presenter and voice."]):
        d.text(((W - d.textlength(s2, font=f2)) / 2, 1470 + k * 44), s2, font=f2, fill=(110, 110, 110))
    return img
# ---------- main ----------
proc = None
if not preview:
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
want = set(int(round(p * FPS)) for p in preview); last = None
for i in range(N):
    t = i / FPS
    if t < VO:
        ok, fr = cap.read()
        if ok: last = fr
        fr = last
    if preview and i not in want: continue
    if t < VO:
        cur = None
        for k, (a, b, _) in ins.items():
            if a <= t < b: cur = k
        img = insert_frame(cur, t) if cur else aroll(fr, t)
        hook(img, t)
        has_card = card(img, t)
        draw_caption(img, t, 1330)
        if t > VO - 0.35:
            img = Image.blend(img, endcard(t), ease((t - (VO - 0.35)) / 0.35))
    else:
        img = endcard(t)
    if preview: img.save(f"prev_{t:05.2f}.jpg", quality=88)
    else: proc.stdin.write(img.tobytes())
if proc: proc.stdin.close(); proc.wait()
print("done", N)
