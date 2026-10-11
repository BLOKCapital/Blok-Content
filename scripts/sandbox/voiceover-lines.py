#!/usr/bin/env python3
"""Voice each line of a script separately (edge-tts) so pauses between beats can be set by hand.

Runs in the Composio remote sandbox (this machine can't reach the TTS service):

    pip install -q edge-tts
    python3 voiceover-lines.py script.txt outdir [voice] [rate]

Writes outdir/line-NN.mp3 + outdir/line-NN.json (word timings, seconds, relative to the line).
Assemble locally with scripts/assemble-vo.py, which adds the pauses and writes vo.wav + vo.json.
"""
import asyncio, json, os, sys

import edge_tts


async def one(text, path, voice, rate):
    comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words = []
    with open(path + ".mp3", "wb") as f:
        async for ch in comm.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                s = ch["offset"] / 1e7
                words.append({"w": ch["text"], "s": round(s, 3), "e": round(s + ch["duration"] / 1e7, 3)})
    json.dump(words, open(path + ".json", "w"))


async def main(script, out, voice, rate):
    os.makedirs(out, exist_ok=True)
    lines = [l.strip() for l in open(script, encoding="utf-8") if l.strip()]
    for i, l in enumerate(lines):
        await one(l, f"{out}/line-{i:02d}", voice, rate)
        print(i, l)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    a = sys.argv
    asyncio.run(main(a[1], a[2], a[3] if len(a) > 3 else "en-US-AndrewMultilingualNeural", a[4] if len(a) > 4 else "+0%"))
