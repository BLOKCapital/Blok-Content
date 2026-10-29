# Ambassador Program launch film (29 Oct 2026)

**Ask (Sheetal):** a launch video "frame for frame" like the reference she shared (`/mnt/project-files/download.mp4`,
a 60s brand film: stock montage, cuts every ~0.5s, calm narrator with small subtitles, three huge italic title
cards, product inserts, logo end card), with BLOK branding, for the Ambassador Program (video creators only).

**Why not edit the reference directly:** its footage is someone else's licensed material (including a film clip).
We kept its structure, pacing and devices and rebuilt every shot as original BLOK motion graphics.

## Angles considered
1. **"Every finance video looks the same"** (chosen): mirrors the reference's arc (monotony → diversity), speaks
   straight to video creators, and lands the brand narrative (funds were for the big boys; now anyone can own a
   $10 fund) as the reason we need new explainers. Opens a question in second one, answers it at the end.
2. Bogle's index fund was mocked as "Bogle's Folly" until people explained it: good history hook but the
   reference's visual rhythm doesn't fit a single story.
3. Keynes' 15-hour week: already used on 15 Oct.

## Structure (52.5s, 16:9 and 9:16 from the same scene)
| Time | Beat | Reference equivalent |
|---|---|---|
| 0–15 | Wall of identical thumbnails, arrows, shouting faces, factsheets, static, eyes; one tile lights up and opens like a door | "People get comfortable with good / monotony" |
| 15–26 | Columns, velvet rope, vault, the big boys; $10,000 → $100,000 minimums, SETUP FEE stamp, BANK INTRO ticket; seed sprouts; everyone's fund; $10 | "unending realities / different approaches" |
| 26–34.7 | Starfield, a crowd that hasn't heard, REC viewfinder, waveform, ring light, six creator styles in 2s, light through the BLOK mark splits into colours | "natural explorers / giving people more choice" |
| 34.7–41.8 | EVERY VOICE / perks UI / Discord role / YOUR STYLE / early access click / MAKE IT CLICK / community spotlight | "EVERY MODEL / YOUR RULES / ALL KINDS OF BRILLIANT" |
| 41.8–52.5 | Prism logo, AMBASSADOR PROGRAM, NOW OPEN, VIDEO CREATORS ONLY, end card | prism logo end card |

## Build
- Voice: Kokoro `af_heart` 1.0 (`build/lines.json` → `python3 ../../../../scripts/qa/make_vo.py af_heart 1.0` in `build/`).
- Music: original synth score, `python3 build/music.py build/music.wav` (120 BPM, drops on the cuts).
- Visuals: `build/scene.html` (canvas, `?v=1` = 9:16); render with `node build/render.mjs build/scene.html out.mp4 [0|1]`.
- Mix: music side-chain ducked under the voice, loudnorm to -14 LUFS, true peak -1.5 dB.
