"""Build the 'self-made fund' reel: podcast clip + header + word captions + pool outro.
Usage: python3 make_reel.py plan.json out.mp4   (paths in plan are relative to this folder)"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/"
YELLOW = (255, 230, 60)

def font(name, size): return ImageFont.truetype(F + name, size)

def shadowed(layers):
    """layers: list of (xy_center, text, font, fill, stroke). Returns RGBA with soft drop shadow."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds, d = ImageDraw.Draw(sh), ImageDraw.Draw(img)
    for (cx, cy), text, fnt, fill, stroke in layers:
        ds.text((cx + 3, cy + 4), text, font=fnt, fill=(0, 0, 0, 200), anchor="mm", stroke_width=stroke + 2, stroke_fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    for (cx, cy), text, fnt, fill, stroke in layers:
        d.text((cx, cy), text, font=fnt, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return Image.alpha_composite(sh, img)

def header(top, quote):
    return shadowed([((W // 2, 150), top, font("Inter-ExtraBold.otf", 78), (255, 255, 255), 0),
                     ((W // 2, 228), quote, font("Inter-Bold.otf", 44), (255, 255, 255), 0)])

def caption(lines, cy):
    layers, y = [], cy
    for text, style in lines:
        if style == "big":
            f = font("Inter-BlackItalic.otf", 74); layers.append(((W // 2, y), text, f, YELLOW, 3)); y += 72
        elif style == "white":
            f = font("Inter-ExtraBold.otf", 52); layers.append(((W // 2, y), text, f, (255, 255, 255), 2)); y += 60
        else:
            f = font("Inter-BoldItalic.otf", 38); layers.append(((W // 2, y), text, f, YELLOW, 2)); y += 46
    return shadowed(layers)

def main(plan_path, out):
    plan = json.load(open(plan_path))
    tmp = os.path.join(HERE, "overlays"); os.makedirs(tmp, exist_ok=True)
    talk, outro = os.path.join(HERE, plan["talk"]), os.path.join(HERE, plan["outro"])
    t_end, o_len = sum(b - a for a, b, _ in plan["talk_segments"]), plan["outro_len"]
    pngs = []  # (path, t0, t1)
    p = os.path.join(tmp, "header.png"); header(*plan["header"]).save(p); pngs.append((p, 0, t_end))
    for i, c in enumerate(plan["captions"]):
        p = os.path.join(tmp, f"c{i:02d}.png"); caption(c["lines"], c.get("y", 980)).save(p); pngs.append((p, c["t0"], c["t1"]))
    for i, c in enumerate(plan["outro_text"]):
        p = os.path.join(tmp, f"o{i:02d}.png"); caption(c["lines"], c.get("y", 1250)).save(p)
        pngs.append((p, t_end + c["t0"], t_end + c["t1"]))
    total = t_end + o_len
    inputs = ["-i", talk, "-i", outro]
    for p, *_ in pngs: inputs += ["-loop", "1", "-t", f"{total}", "-i", p]
    music = os.path.join(HERE, plan["music"])
    inputs += ["-i", music]
    mi = 2 + len(pngs)
    segs = plan["talk_segments"]  # [start, end, zoom] pieces of the take, joined with jump cuts
    fc = []
    for i, (s0, s1, z) in enumerate(segs):
        zw, zh = int(W * z) // 2 * 2, int(H * z) // 2 * 2
        fc.append(f"[0:v]trim={s0}:{s1},setpts=PTS-STARTPTS,scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1[tv{i}]")
        fc.append(f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS[ta{i}]")
    fc.append("".join(f"[tv{i}][ta{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[a][talka]")
    fc += [
          f"[1:v]trim=0:{o_len},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1[b]",
          "[a][b]concat=n=2:v=1:a=0[v0]"]
    last = "v0"
    for k, (p, t0, t1) in enumerate(pngs):
        fc.append(f"[{last}][{k + 2}:v]overlay=0:0:enable='between(t,{t0},{t1})'[v{k + 1}]"); last = f"v{k + 1}"
    fc.append(f"[talka]afade=t=out:st={t_end - 0.15}:d=0.15,apad=whole_dur={total}[va]")
    fc.append(f"[{mi}:a]atrim=0:{o_len + 0.3},asetpts=PTS-STARTPTS,afade=t=in:d=0.2,afade=t=out:st={o_len - 0.6}:d=0.6,volume=0.7,adelay={int((t_end - 0.3) * 1000)}|{int((t_end - 0.3) * 1000)}[ma]")
    fc.append("[va][ma]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "[aout]",
           "-t", f"{total}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
