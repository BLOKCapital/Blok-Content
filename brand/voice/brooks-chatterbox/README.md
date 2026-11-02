# Brooks voice (Chatterbox clone) — the default voice for all BLOK videos

Sheetal approved this voice on 2 Nov 2026 ("this voice is good, use this in future videos").
First used on Who Called It? Part 2: Dow 36,000 (`content/2026-11-01-who-called-it-dow-36000/`).
Free, open source, runs locally on CPU. No ElevenLabs, no Higgsfield credits, no top-ups.

## What it is
- Model: Resemble AI **Chatterbox** (`chatterbox-tts` 0.1.7, weights from Hugging Face `ResembleAI/chatterbox`).
- Voice: zero-shot clone of the "Brooks" narrator take Sheetal picked
  (`content/2026-10-31-small-starts-bogle/voice-samples/B-brooks-unedited.mp3`, first 9.5 s) → `brooks-ref-9s.wav`.
- Settings: `exaggeration=0.5`, `cfg_weight=0.5`, 24 kHz. About 7 s of compute per 1 s of speech on 4 CPUs.

## How to run (about 25 min for a 50 s Reel)
1. `bash setup.sh` once per machine (5–10 min).
2. Write `build/lines.json` as usual: `show` = on-screen words, `say` = what is spoken (spell out years and money),
   `gap` = pause after the line in seconds.
3. From the piece folder: `python <this dir>/gen_all.py build/lines.json <this dir>/brooks-ref-9s.wav`
   → 3 takes per line in `takes/` (different seeds).
4. Score the takes with speech recognition (QA venv from `scripts/qa/setup-models.sh`):
   `python -I <this dir>/score.py build/lines.json takes` → `takes/scores.json`.
5. Assemble: `python <this dir>/assemble.py build/lines.json takes build` → `build/vo.wav` + `build/timeline.js`
   (picks the best take per line; word timings come from torchaudio MMS forced alignment, ~1.2 GB download first time).
   Override a pick with `takes/picks.json`, e.g. `{"5": "takes/l05_t1.wav"}` (use it when a line needs a pause or a different read).
6. Mix, render, then run the full `growth/qa-checklist.md` on the final mp4.

## Tips
- Line by line with 3 takes worked better than one long take: Chatterbox drifts on long text, and per-line picking
  lets us drop a slurred take ("Dao" for "Dow", "the dial") without re-recording everything.
- Whisper writes contractions and numbers its own way ("answer's" → "answer is", "second" → "2"); those are not errors.
- Caption still needs "AI-generated voiceover".
