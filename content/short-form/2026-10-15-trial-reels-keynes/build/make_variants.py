"""Make Instagram trial-reel hook variants of one finished reel.

Each variant keeps the body of the reel identical and changes only the opening:
an on-screen hook card for the first seconds, an optional cold open (a short clip
pulled from later in the reel and played first), and a slight zoom so no two
uploads are pixel-identical (helps avoid Instagram's duplicate-content flag).

Usage: python3 make_variants.py [variant-id ...]   (no args = all)
Needs: ffmpeg, Pillow, Inter fonts in /usr/share/fonts/opentype/inter/.
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SRC = os.path.join(OUT, "..", "2026-10-15-keynes-promised-me", "keynes-promised-me.mp4")
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
W, H = 1080, 1920

INDIGO, LINEN, LIME, CORAL, SKY, INK = "#004EBA", "#F6F3E8", "#7ED116", "#EC464D", "#7DD2FD", "#14122B"

# id, hook text (*word* = accent colour, " | " = line break), card bg, text colour, accent, cold open (start, end) or None, zoom, hook seconds
VARIANTS = [
    ("v1-prediction", "In 1930, Keynes predicted you'd work *15 hours* a week by now.", LINEN, INK, CORAL, None, 1.00, 3.6),
    ("v2-wrong-worker", "Keynes was right about the 15-hour week. He just picked the *wrong worker.*", INK, LINEN, LIME, None, 1.03, 3.8),
    ("v3-saturdays", "Wall Street worked Saturdays until *1952.* | Now your money takes weekends off.", LINEN, INDIGO, CORAL, None, 1.05, 4.0),
    ("v4-3am", "It's 3 a.m. Do you know what *your money* is doing?", INK, LINEN, SKY, (53.55, 55.75), 1.02, 3.0),
    ("v5-waits-for-monday", "Your money has a 9-to-5. And it takes *every weekend* off.", LIME, INK, INDIGO, (32.40, 35.05), 1.04, 3.4),
    ("v6-32-of-168", "Your money works *32 hours* a week. | A week has 168.", CORAL, LINEN, INK, None, 1.06, 3.4),
    ("v7-ai-took-my-emails", "AI took my emails. It didn't give me back *a single hour.*", SKY, INK, INDIGO, (8.20, 11.85), 1.01, 3.8),
]


def wrap(draw, words, font, maxw):
    lines, cur = [], []
    for w in words:
        if w[0] == "|":  # forced line break
            if cur:
                lines.append(cur)
            cur = []
            continue
        trial = " ".join(t for t, _ in cur + [w])
        if cur and draw.textlength(trial, font=font) > maxw:
            lines.append(cur); cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def hook_card(text, bg, fg, accent, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = 80
    font = ImageFont.truetype(FONT, size)
    words, hi = [], False
    for raw in text.split(" "):
        start = raw.startswith("*"); end = raw.endswith("*") or raw.endswith("*.") or raw.endswith("*?")
        hi = hi or start
        words.append((raw.replace("*", ""), hi))
        if end:
            hi = False
    pad_x, pad_y, gap = 56, 48, 14
    maxw = W - 2 * 70 - 2 * pad_x
    lines = wrap(d, words, font, maxw)
    lh = size + gap
    box_w = max(d.textlength(" ".join(t for t, _ in l), font=font) for l in lines) + 2 * pad_x
    box_h = len(lines) * lh - gap + 2 * pad_y + 10
    x0 = (W - box_w) / 2; y0 = 210
    d.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=36, fill=bg)
    y = y0 + pad_y
    space = d.textlength(" ", font=font)
    for l in lines:
        lw = d.textlength(" ".join(t for t, _ in l), font=font)
        x = (W - lw) / 2
        for t, h in l:
            d.text((x, y), t, font=font, fill=accent if h else fg)
            x += d.textlength(t, font=font) + space
        y += lh
    img.save(path)


def render(v):
    vid, text, bg, fg, accent, cold, zoom, hook_s = v
    os.makedirs(os.path.join(HERE, "cards"), exist_ok=True)
    card = os.path.join(HERE, "cards", f"{vid}.png")
    hook_card(text, bg, fg, accent, card)
    out = os.path.join(OUT, f"{vid}.mp4")
    zw, zh = int(round(W * zoom / 2) * 2), int(round(H * zoom / 2) * 2)
    zoomf = f"scale={zw}:{zh},crop={W}:{H}" if zoom != 1.0 else "null"
    if cold:
        a, b = cold
        # the cold clip is opened as its own input (input 2) so ffmpeg never buffers the whole reel
        pre = ["-ss", str(a), "-t", str(round(b - a, 3)), "-i", SRC]
        body = (f"[2:v]setpts=PTS-STARTPTS[cv];[2:a]asetpts=PTS-STARTPTS,afade=t=out:st={round(b-a-0.08,3)}:d=0.08[ca];"
                f"[cv][ca][0:v][0:a]concat=n=2:v=1:a=1[bv][ba];")
        hook_s = round(b - a + 0.6, 2)
    else:
        pre = []
        body = "[0:v]null[bv];[0:a]anull[ba];"
    fc = (body + f"[bv]{zoomf}[zv];"
          f"[1:v]format=rgba,fade=t=out:st={hook_s-0.25}:d=0.25:alpha=1[hk];"
          f"[zv][hk]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", SRC, "-loop", "1", "-framerate", "30", "-t", str(hook_s), "-i", card, *pre,
           "-filter_complex", fc, "-map", "[v]", "-map", "[ba]", "-r", "30",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    # cover = first frame with the hook card (Instagram also lets you pick a frame in-app)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", out, "-frames:v", "1", "-q:v", "3",
                    os.path.join(OUT, f"{vid}-cover.jpg")], check=True)
    print("made", out)


if __name__ == "__main__":
    want = set(sys.argv[1:])
    for v in VARIANTS:
        if not want or v[0] in want:
            render(v)
