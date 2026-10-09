#!/usr/bin/env python3
"""Generate a human-sounding voiceover + word timings with Microsoft neural voices (free, via edge-tts).

Runs in the Composio remote sandbox (this machine's network can't reach the TTS service):

    pip install -q edge-tts
    curl -sSL -o voiceover.py https://raw.githubusercontent.com/BLOKCapital/Blok-Content/main/scripts/sandbox/voiceover.py
    curl -sSL -o script.txt   https://raw.githubusercontent.com/BLOKCapital/Blok-Content/main/<piece>/build/script.txt
    python3 voiceover.py script.txt vo [voice]

script.txt: one sentence/beat per line, written the way people talk ("And then... it just waits.").
Outputs vo.m4a (48kHz AAC) and vo.json (word timings, seconds). Default voice: en-US-AndrewMultilingualNeural
(the approved BLOK voice). Other good ones: en-US-AvaMultilingualNeural, en-US-EmmaMultilingualNeural,
en-US-BrianMultilingualNeural.
"""
import asyncio, json, subprocess, sys

import edge_tts


async def main(script_path, out, voice):
    text = " ".join(l.strip() for l in open(script_path, encoding="utf-8") if l.strip())
    comm = edge_tts.Communicate(text, voice, rate="+0%", boundary="WordBoundary")
    words = []
    with open(out + ".mp3", "wb") as f:
        async for ch in comm.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                s = ch["offset"] / 1e7
                words.append({"w": ch["text"], "s": round(s, 3), "e": round(s + ch["duration"] / 1e7, 3)})
    json.dump(words, open(out + ".json", "w"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out + ".mp3", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "192k", out + ".m4a"], check=True)
    print(f"{out}.m4a  {len(words)} words  last word ends {words[-1]['e']}s")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "en-US-AndrewMultilingualNeural"))
