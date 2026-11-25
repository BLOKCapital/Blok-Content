#!/usr/bin/env python3
"""vref: BLOK's video reference library.

Turns reference videos (mostly Instagram reels) into a browsable study library:
keyframes at every cut, a contact sheet, a hook strip (first 3 seconds), a
transitions strip (before/after each cut), a waveform, pacing stats and a
transcript. Entries are then tagged into category folders (hooks, subtitles,
graphics-motion, transitions, music-sound, ...) with short notes on what works.

REFERENCE ONLY. Nothing in this library may be reuploaded or cut into BLOK videos.
We study how a video works, then build our own from scratch.

Library location: $VREF_LIB, default /mnt/project-files/growth/video-references

Commands
  add <url-or-file> [--url URL] [--title T] [--creator C] [--why TEXT]
                    [--cookies-from-browser chrome] [--cookies FILE] [--no-transcribe]
  tag <id> <category> --note TEXT [--frames 3,7] [--t 1.2-3.4]
  why <id> TEXT                      overall "what makes it work" line
  untag <id> <category>
  lookup [category] [--q words]      print references + notes (for building a video)
  list                               one line per entry
  rebuild                            regenerate category folders + library.html
  categories                         list categories with what to look for
"""
import argparse, datetime as dt, glob, json, os, re, shutil, subprocess, sys, tempfile

LIB = os.environ.get("VREF_LIB", "/mnt/project-files/growth/video-references")
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.expanduser("~/.cache/blok-models/sherpa-onnx-whisper-small.en")

CATEGORIES = {
    "hooks": "First 1-3 seconds: what stops the scroll (visual, line, question, pattern break).",
    "storytelling": "Structure: setup, tension, open loop, payoff, series hooks, narrative beats.",
    "subtitles": "Caption style: font, size, position, word highlight, pop-in timing, emoji use.",
    "graphics-motion": "Motion graphics: kinetic type, charts, icons, 3D, masks, overlays, UI mockups.",
    "transitions": "How shots join: whip, match cut, zoom, mask wipe, morph, jump cut, sound-led cut.",
    "music-sound": "Track choice, beat-synced cuts, SFX (whoosh, pop, riser), silence, voice tone.",
    "pacing-editing": "Cut rate, shot length, speed ramps, punch-ins, rhythm changes.",
    "visual-style": "Colour grade, palette, lighting, framing, texture, set design, typography system.",
    "cta-endings": "Endings and calls to action: comment-to-get, loop endings, cliffhangers, follows.",
    "formats": "Repeatable formats worth stealing the shape of (street quiz, POV, tier list, myth vs fact).",
}

# ---------------------------------------------------------------- helpers

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def die(msg):
    print("vref: " + msg, file=sys.stderr); sys.exit(1)

def slugify(s, n=40):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:n].strip("-") or "video"

def entries_dir():
    return os.path.join(LIB, "entries")

def load(eid):
    p = os.path.join(entries_dir(), eid, "meta.json")
    if not os.path.exists(p):
        matches = [d for d in os.listdir(entries_dir()) if eid in d] if os.path.isdir(entries_dir()) else []
        if len(matches) == 1:
            eid = matches[0]; p = os.path.join(entries_dir(), eid, "meta.json")
        else:
            die(f"no entry '{eid}'" + (f" (matches: {', '.join(matches)})" if matches else ""))
    with open(p) as f:
        return json.load(f)

def save(meta):
    d = os.path.join(entries_dir(), meta["id"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)

def all_entries():
    out = []
    for p in sorted(glob.glob(os.path.join(entries_dir(), "*", "meta.json"))):
        with open(p) as f:
            out.append(json.load(f))
    return out

def probe(path):
    r = sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path])
    if r.returncode: die("ffprobe failed: " + r.stderr[-300:])
    j = json.loads(r.stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    if not v: die("no video stream in " + path)
    num, den = (v.get("avg_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 30.0
    w, h = int(v["width"]), int(v["height"])
    rot = int((v.get("tags") or {}).get("rotate", 0) or 0)
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd: rot = int(sd["rotation"])
    if abs(rot) in (90, 270): w, h = h, w
    return dict(duration=float(j["format"]["duration"]), fps=round(fps, 2), width=w, height=h, has_audio=bool(a))

# ---------------------------------------------------------------- download

def download(url, workdir, cookies_browser=None, cookies=None):
    """Download with yt-dlp. Returns (video_path, info_dict)."""
    try:
        import yt_dlp  # noqa
    except ImportError:
        die("yt-dlp missing: pip install yt-dlp")
    cmd = [sys.executable, "-m", "yt_dlp", "--no-playlist", "--no-warnings", "--write-info-json",
           "-f", "bv*[height<=1920]+ba/b", "--merge-output-format", "mp4",
           "-o", os.path.join(workdir, "src.%(ext)s"), url]
    if cookies_browser: cmd[3:3] = ["--cookies-from-browser", cookies_browser]
    if cookies: cmd[3:3] = ["--cookies", cookies]
    r = sh(cmd)
    vids = [p for p in glob.glob(os.path.join(workdir, "src.*")) if not p.endswith(".json")]
    if r.returncode or not vids:
        err = (r.stderr or r.stdout)[-600:]
        hint = ""
        if "429" in err or "login" in err.lower() or "rate" in err.lower() or "cookies" in err.lower():
            hint = ("\nInstagram blocked this machine. Use one of the fallbacks in GUIDE.md: download on "
                    "Sheetal's Mac (yt-dlp --cookies-from-browser chrome) and stage the file, or ask her to "
                    "upload the saved reel, then run: vref.py add <file> --url " + url)
        die("download failed:\n" + err + hint)
    info = {}
    ij = glob.glob(os.path.join(workdir, "src*.info.json"))
    if ij:
        with open(ij[0]) as f: info = json.load(f)
    return vids[0], info

# ---------------------------------------------------------------- analysis

def detect_cuts(path, duration, thresh=0.32):
    r = sh(["ffmpeg", "-hide_banner", "-i", path, "-an", "-vf",
            f"scale=320:-2,select='gt(scene,{thresh})',showinfo", "-f", "null", "-"])
    ts = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    cuts, last = [], -1.0
    for t in ts:
        if t - last >= 0.25 and 0.1 < t < duration - 0.1:
            cuts.append(round(t, 2)); last = t
    return cuts

def pick_keyframes(cuts, duration, max_gap=2.0, cap=30):
    """Frame shortly after each cut, plus fillers so no gap is longer than max_gap."""
    starts = [0.0] + cuts
    ends = cuts + [duration]
    times = []
    for s, e in zip(starts, ends):
        t = s + min(0.2, (e - s) / 2)
        while t < e - 0.05:
            times.append(round(t, 2)); t += max_gap
    times = sorted(set(times))
    if len(times) > cap:  # thin evenly, always keep the first second
        step = len(times) / cap
        times = sorted(set([times[0]] + [times[int(i * step)] for i in range(cap)]))
    return times

def grab(path, t, out, width=540):
    r = sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t,0):.3f}", "-i", path, "-frames:v", "1",
            "-vf", f"scale={width}:-2", "-q:v", "3", out])
    return r.returncode == 0 and os.path.exists(out)

def font(size, bold=False):
    from PIL import ImageFont
    names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", "Arial Bold.ttf" if bold else "Arial.ttf"]
    for d in ["/usr/share/fonts/truetype/dejavu", "/Library/Fonts", "/System/Library/Fonts/Supplemental"]:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def sheet(images, labels, out, cols=6, tw=240, title=None):
    from PIL import Image, ImageDraw
    if not images: return
    ims = [Image.open(p).convert("RGB") for p in images]
    th = int(tw * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    top = 44 if title else 0
    S = Image.new("RGB", (cols * tw + (cols + 1) * 8, top + rows * (th + 30) + 8), (246, 243, 232))
    d = ImageDraw.Draw(S)
    if title: d.text((10, 10), title, fill=(0, 40, 90), font=font(22, True))
    for i, (im, lab) in enumerate(zip(ims, labels)):
        x = 8 + (i % cols) * (tw + 8); y = top + 8 + (i // cols) * (th + 30)
        S.paste(im.resize((tw, th)), (x, y))
        d.text((x + 2, y + th + 4), lab, fill=(40, 40, 40), font=font(15))
    S.save(out, quality=85)

def loudness(path):
    r = sh(["ffmpeg", "-hide_banner", "-i", path, "-vn", "-af", "ebur128", "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None

def waveform(path, out, duration, cuts):
    tmp = out + ".raw.png"
    r = sh(["ffmpeg", "-v", "error", "-y", "-i", path, "-filter_complex",
            "aformat=channel_layouts=mono,showwavespic=s=1600x200:colors=0x004EBA", "-frames:v", "1", tmp])
    if r.returncode: return False
    from PIL import Image, ImageDraw
    im = Image.open(tmp).convert("RGBA")
    bg = Image.new("RGBA", im.size, (246, 243, 232, 255)); bg.alpha_composite(im)
    d = ImageDraw.Draw(bg)
    for c in cuts:  # cut markers so beat sync is visible
        x = int(c / duration * im.width); d.line([(x, 0), (x, im.height)], fill=(236, 70, 77, 255), width=2)
    for s in range(0, int(duration) + 1, 5):
        x = int(s / duration * im.width); d.text((x + 2, 2), f"{s}s", fill=(80, 80, 80, 255), font=font(14))
    bg.convert("RGB").save(out, quality=88); os.remove(tmp)
    return True

def transcribe(path):
    """Local whisper (sherpa-onnx small.en). Returns text or None if not installed."""
    try:
        import numpy as np, sherpa_onnx
    except ImportError:
        return None
    if not os.path.exists(os.path.join(MODEL, "small.en-encoder.int8.onnx")): return None
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{MODEL}/small.en-encoder.int8.onnx", decoder=f"{MODEL}/small.en-decoder.int8.onnx",
        tokens=f"{MODEL}/small.en-tokens.txt", num_threads=4)
    pcm = sh_bytes(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    parts, step = [], 16000 * 28
    for i in range(0, len(a), step):
        chunk = a[i:i + step]
        if len(chunk) < 8000: continue
        st = rec.create_stream(); st.accept_waveform(16000, chunk); rec.decode_stream(st)
        parts.append(f"[{i // 16000}s] " + st.result.text.strip())
    return "\n".join(p for p in parts if p.split("] ", 1)[-1])

def sh_bytes(cmd):
    return subprocess.run(cmd, capture_output=True, check=True).stdout

# ---------------------------------------------------------------- add

def cmd_add(a):
    src = a.source
    work = tempfile.mkdtemp(prefix="vref-")
    info = {}
    try:
        if re.match(r"https?://", src):
            url = src
            print("downloading", url)
            path, info = download(url, work, a.cookies_from_browser, a.cookies)
        else:
            if not os.path.exists(src): die("no such file: " + src)
            path, url = src, a.url
        return process(path, url, info, a)
    finally:
        shutil.rmtree(work, ignore_errors=True)

def process(path, url, info, a):
    P = probe(path)
    creator = a.creator or info.get("uploader") or info.get("channel") or ""
    title = a.title or info.get("title") or info.get("description", "")[:60] or os.path.basename(path)
    if url and not creator:
        m = re.search(r"instagram\.com/([^/]+)/(reel|p)/", url)
        if m: creator = m.group(1)
    vid = info.get("id") or (re.search(r"/(?:reel|p|shorts|video)/([A-Za-z0-9_-]+)", url or "") or [None, None])[1]
    eid = f"{dt.date.today().isoformat()}-{slugify(creator or 'ref', 18)}-{slugify(vid or title, 22)}"
    for e in all_entries():
        if url and e.get("url") == url and not a.force:
            print(f"already in library as {e['id']} (use --force to redo)"); return e
    d = os.path.join(entries_dir(), eid); fr = os.path.join(d, "frames")
    if os.path.isdir(d): shutil.rmtree(d)
    os.makedirs(fr)
    print(f"analysing {P['duration']:.1f}s {P['width']}x{P['height']} -> {eid}")

    cuts = detect_cuts(path, P["duration"])
    times = pick_keyframes(cuts, P["duration"])
    frames = []
    for i, t in enumerate(times, 1):
        name = f"f{i:02d}_{t:05.1f}s.jpg"
        if grab(path, t, os.path.join(fr, name)): frames.append(dict(n=i, t=t, file=f"frames/{name}"))
    sheet([os.path.join(d, f["file"]) for f in frames], [f"#{f['n']}  {f['t']:.1f}s" for f in frames],
          os.path.join(d, "sheet.jpg"), title=f"{creator}  ·  {P['duration']:.0f}s  ·  {len(cuts)} cuts")

    # hook strip: first 3 seconds
    hook_t = [0.0, 0.4, 0.8, 1.2, 1.8, 2.4, 3.0]
    hook_t = [t for t in hook_t if t < P["duration"]]
    hp = []
    for t in hook_t:
        out = os.path.join(fr, f"hook_{t:03.1f}s.jpg")
        if grab(path, t, out): hp.append(out)
    sheet(hp, [f"{t:.1f}s" for t in hook_t[:len(hp)]], os.path.join(d, "hook.jpg"), cols=len(hp) or 1,
          tw=220, title="Hook: first 3 seconds")
    for p in hp: os.remove(p)

    # transitions strip: just before / just after the first 8 cuts
    tp, tl = [], []
    for k, c in enumerate(cuts[:8], 1):
        for side, dt_ in (("before", -0.12), ("after", 0.08)):
            out = os.path.join(fr, f"cut{k:02d}_{side}.jpg")
            if grab(path, c + dt_, out, 360): tp.append(out); tl.append(f"cut {k} {side} {c:.1f}s")
    if tp:
        sheet(tp, tl, os.path.join(d, "transitions.jpg"), cols=4, tw=200, title="Transitions: before / after each cut")
    for p in tp: os.remove(p)

    has_wave = P["has_audio"] and waveform(path, os.path.join(d, "waveform.jpg"), P["duration"], cuts)
    lufs = loudness(path) if P["has_audio"] else None

    # low-res study proxy (reference only, never reupload)
    sh(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", "scale=-2:640", "-c:v", "libx264", "-crf", "30",
        "-preset", "veryfast", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart",
        os.path.join(d, "preview.mp4")])

    transcript = None
    if P["has_audio"] and not a.no_transcribe:
        print("transcribing…"); transcript = transcribe(path)
    words = len(re.sub(r"\[\d+s\]", "", transcript or "").split())
    shots = [b - s for s, b in zip([0.0] + cuts, cuts + [P["duration"]])]
    meta = dict(
        id=eid, url=url or "", source_id=vid or "", creator=creator, title=title,
        caption=(info.get("description") or "")[:2000], posted=info.get("upload_date") or "",
        views=info.get("view_count"), likes=info.get("like_count"), comments=info.get("comment_count"),
        added=dt.datetime.now().isoformat(timespec="minutes"), **P,
        stats=dict(cuts=len(cuts), cuts_per_min=round(len(cuts) / P["duration"] * 60, 1),
                   avg_shot=round(sum(shots) / len(shots), 2), first_cut=cuts[0] if cuts else None,
                   longest_shot=round(max(shots), 2), lufs=lufs,
                   words=words, wpm=round(words / P["duration"] * 60) if words else 0),
        cuts=cuts, frames=frames, transcript=transcript or "",
        files=dict(sheet="sheet.jpg", hook="hook.jpg", transitions="transitions.jpg" if tp else "",
                   waveform="waveform.jpg" if has_wave else "", preview="preview.mp4"),
        why=a.why or "", tags={}, status="untagged")
    save(meta)
    rebuild(quiet=True)
    print(f"added {eid}: {len(frames)} keyframes, {len(cuts)} cuts, {meta['stats']['cuts_per_min']}/min")
    print(f"next: look at {os.path.join(d, 'sheet.jpg')} (and hook.jpg, transitions.jpg), then run "
          f"vref.py tag {eid} <category> --note '...' --frames N,N")
    return meta

# ---------------------------------------------------------------- tagging

def parse_frames(s):
    return [int(x) for x in re.split(r"[,\s]+", s or "") if x.strip().isdigit()]

def cmd_tag(a):
    if a.category not in CATEGORIES:
        die(f"unknown category '{a.category}'. Pick one of: {', '.join(CATEGORIES)}")
    m = load(a.id)
    fr = parse_frames(a.frames)
    bad = [n for n in fr if n not in {f["n"] for f in m["frames"]}]
    if bad: die(f"frame numbers {bad} not in this entry (1..{len(m['frames'])})")
    m["tags"][a.category] = dict(note=a.note.strip(), frames=fr, t=a.t or "")
    m["status"] = "tagged"
    save(m); rebuild(quiet=True)
    print(f"{m['id']} -> {a.category}")

def cmd_untag(a):
    m = load(a.id); m["tags"].pop(a.category, None)
    if not m["tags"]: m["status"] = "untagged"
    save(m); rebuild(quiet=True)

def cmd_why(a):
    m = load(a.id); m["why"] = a.text.strip(); save(m); rebuild(quiet=True)

# ---------------------------------------------------------------- outputs

def rebuild(quiet=False):
    E = all_entries()
    cdir = os.path.join(LIB, "categories")
    if os.path.isdir(cdir): shutil.rmtree(cdir)
    for c, desc in CATEGORIES.items():
        cd = os.path.join(cdir, c); os.makedirs(cd)
        hits = [e for e in E if c in e["tags"]]
        lines = [f"# {c}", "", desc, "", f"{len(hits)} reference(s). Reference only: never reupload these clips.", ""]
        for e in hits:
            t = e["tags"][c]
            lines += [f"## {e['creator'] or 'unknown'} · {e['id']}", f"- Source: {e['url'] or 'local file'}",
                      f"- Note: {t['note']}"]
            if t.get("t"): lines.append(f"- Moment: {t['t']}")
            if e.get("why"): lines.append(f"- Why it works overall: {e['why']}")
            for n in t["frames"]:
                f = next((f for f in e["frames"] if f["n"] == n), None)
                if not f: continue
                dst = f"{e['id']}__f{n:02d}.jpg"
                shutil.copyfile(os.path.join(entries_dir(), e["id"], f["file"]), os.path.join(cd, dst))
                lines.append(f"- Frame #{n} at {f['t']:.1f}s: ![]({dst})")
            lines += [f"- Full breakdown: ../../entries/{e['id']}/", ""]
        with open(os.path.join(cd, "README.md"), "w") as f: f.write("\n".join(lines))
    with open(os.path.join(LIB, "library.json"), "w") as f:
        json.dump(dict(categories=CATEGORIES, entries=E, built=dt.datetime.now().isoformat(timespec="minutes")), f, indent=1)
    with open(os.path.join(HERE, "library_template.html")) as f: tpl = f.read()
    data = json.dumps(dict(categories=CATEGORIES, entries=E), ensure_ascii=False).replace("</", "<\\/")
    with open(os.path.join(LIB, "library.html"), "w") as f: f.write(tpl.replace("/*__DATA__*/null", data))
    g = os.path.join(HERE, "GUIDE.md")
    if os.path.exists(g): shutil.copyfile(g, os.path.join(LIB, "GUIDE.md"))
    inbox = os.path.join(LIB, "inbox.md")
    if not os.path.exists(inbox):
        with open(inbox, "w") as f:
            f.write("# Inbox\n\nPaste reference links here, one per line. Threads process them with "
                    "`vref.py add` and move them into the library.\n\n")
    if not quiet: print(f"rebuilt {len(E)} entries -> {os.path.join(LIB, 'library.html')}")

def cmd_lookup(a):
    E = all_entries(); q = (a.q or "").lower().split()
    for e in E:
        cats = [a.category] if a.category else list(e["tags"]) or ["(untagged)"]
        for c in cats:
            if a.category and c not in e["tags"]: continue
            t = e["tags"].get(c, {})
            blob = " ".join([e["creator"], e["title"], e.get("why", ""), t.get("note", ""), e.get("transcript", "")]).lower()
            if q and not all(w in blob for w in q): continue
            s = e["stats"]
            print(f"[{c}] {e['id']}  ({e['creator']}, {e['duration']:.0f}s, {s['cuts_per_min']} cuts/min, avg shot {s['avg_shot']}s)")
            if t: print(f"   note: {t['note']}" + (f"  @ {t['t']}" if t.get('t') else ""))
            if e.get("why"): print(f"   why:  {e['why']}")
            d = os.path.join(entries_dir(), e["id"])
            fr = [os.path.join(d, f["file"]) for f in e["frames"] if f["n"] in t.get("frames", [])]
            print(f"   look: {os.path.join(d, 'sheet.jpg')}" + "".join(f"\n         {p}" for p in fr))

def cmd_list(a):
    for e in all_entries():
        print(f"{e['id']:<55} {e['status']:<9} {','.join(e['tags']) or '-'}")

def cmd_categories(a):
    for c, d in CATEGORIES.items(): print(f"{c:<16} {d}")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add"); p.add_argument("source")
    p.add_argument("--url"); p.add_argument("--title"); p.add_argument("--creator"); p.add_argument("--why")
    p.add_argument("--cookies-from-browser"); p.add_argument("--cookies")
    p.add_argument("--no-transcribe", action="store_true"); p.add_argument("--force", action="store_true")
    p.set_defaults(f=cmd_add)
    p = sp.add_parser("tag"); p.add_argument("id"); p.add_argument("category")
    p.add_argument("--note", required=True); p.add_argument("--frames"); p.add_argument("--t")
    p.set_defaults(f=cmd_tag)
    p = sp.add_parser("untag"); p.add_argument("id"); p.add_argument("category"); p.set_defaults(f=cmd_untag)
    p = sp.add_parser("why"); p.add_argument("id"); p.add_argument("text"); p.set_defaults(f=cmd_why)
    p = sp.add_parser("lookup"); p.add_argument("category", nargs="?"); p.add_argument("--q")
    p.set_defaults(f=cmd_lookup)
    sp.add_parser("list").set_defaults(f=cmd_list)
    sp.add_parser("rebuild").set_defaults(f=lambda a: rebuild())
    sp.add_parser("categories").set_defaults(f=cmd_categories)
    a = ap.parse_args()
    os.makedirs(entries_dir(), exist_ok=True)
    a.f(a)

if __name__ == "__main__":
    main()
