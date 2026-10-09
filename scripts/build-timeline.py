#!/usr/bin/env python3
"""Turn a voiceover's word timings into the timeline a reel scene reads.

    python3 scripts/build-timeline.py <build>/script.txt <build>/vo.json <build>/timeline.js

script.txt has one sentence/beat per line (same file the voiceover was made from). Each line becomes one
timeline entry {text, start, end, words[]}; scenes key their animations off entry starts (S(i) in scene.html).
"""
import json, re, sys

norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

script, words_path, out = sys.argv[1:4]
sents = [l.strip() for l in open(script, encoding="utf-8") if l.strip()]
words = json.load(open(words_path))
i, tl = 0, []
for s in sents:
    target, got, ws = norm(s), "", []
    while got != target:
        if i >= len(words) or not target.startswith(got + norm(words[i]["w"])):
            sys.exit(f"Can't align line: {s!r} (got {got!r})")
        got += norm(words[i]["w"]); ws.append(words[i]); i += 1
    disp = s.split()
    tl.append({"text": s, "start": ws[0]["s"], "end": ws[-1]["e"],
               "words": [{"w": d, "s": w["s"], "e": w["e"]} for d, w in zip(disp, ws)] if len(disp) == len(ws) else None})
open(out, "w").write("window.TIMELINE = " + json.dumps(tl) + ";")
for n, t in enumerate(tl):
    print(f"S({n}) {t['start']:6.2f}–{t['end']:6.2f}  {t['text'][:60]}")
