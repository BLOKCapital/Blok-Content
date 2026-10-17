# The hidden word (Reel, 22 Oct 2026)

**Ask (Sheetal, 17 Oct):** a reel like @mmmanifest_'s "The universe is testing you…" (144K likes): a short story whose
hidden message lands at the end, carried by a striking visual. Our scraper got the reference's title, thumbnail and tags
(a restaurant/ordering story with a life-lesson twist), not the video itself, so the format is inferred from that.

## Angles considered
1. **Grace Groner, 1935 → 2010, with the lesson hidden as an acrostic** (chosen). The first letters of the 8 story lines spell
   PATIENCE; the reel challenges you to find it, then reveals it. The hidden message is literally hidden, which drives
   rewatches (Reels ranks on watch-through and replays) and "found it in 12 seconds" comments.
2. Ronald Read, the janitor who left $8M (2014): same lesson, better known, less cinematic.
3. Newton losing a third of his fortune in the South Sea Bubble (1720): already made (`2026-10-22-a-genius-lost-his-fortune`, unscheduled).
4. The 1626 Manhattan "$24" purchase compounded: overused and the numbers are shaky.
5. A restaurant-bill story where the hidden message is a fee line: the fee topic already ran 3 times this month.

## Build
- Script: `build/script.txt` (12 lines: hook, 8 acrostic lines, reveal, lesson, CTA).
- Voice: Kokoro `am_michael` (open-source, local), speed 1.0, one take per line with set pauses (`build/tts.py` → `vo.wav`, `lines.json`).
  Andrew (edge-tts) wasn't reachable: this machine can't reach the TTS host and the Composio sandbox's file links are blocked here.
- Visual: `build/scene.html` (night indigo, film grain, a linen ledger page that writes itself line by line, year counter 1935 → 2010,
  value counter $180 → $7,000,000+, then a lime marker sweeps the first letters and they fly out to spell PATIENCE).
- Music: `build/music.py`, original (slow Am7–Fmaj7–Cmaj7–G6 felt piano and pad, hush while you hunt, C major bloom on "Patience").
- Mix: voice compressed, music ducked under it, loudnorm -14 LUFS (`mix.m4a`).
- Render: `node scripts/render-reel.mjs <build>/scene.html <build>/mix.m4a master.mp4 30`, then `ffmpeg -i master.mp4 -c:v libx264 -preset slow -crf 27 -maxrate 6M -bufsize 12M -c:a copy -movflags +faststart the-hidden-word.mp4` (the film grain makes the raw render 127 MB). Cover: `node <build>/cover.mjs <build>/scene.html cover.jpg`.
