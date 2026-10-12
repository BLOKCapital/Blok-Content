# Reel: "Your fund's 1% fee isn't small" (talking head, lip-synced)

**Status:** rendered, awaiting approval. Not posted.
**File:** `the-one-percent-fee.mp4` (1080x1920, 58.6 s, H.264 + AAC, -14 LUFS). Cover: `cover.jpg`. Caption: `caption.md`.

## Format
UGC "car selfie" talking head: an AI presenter in a parked car talks to his phone camera, with traffic passing outside.
Jump cuts and punch-ins between sentences, word-by-word captions (current word in lime), a maths card at the top during the numbers,
two b-roll inserts (a stack of paper statements, and a phone showing a portfolio screen) and a linen end card with the disclaimer.

## Script (voice: ElevenLabs Roger)
Nobody told me this when I started investing. My fund charges one percent a year... who cares? Then I actually did the maths.
$10,000 growing 7% a year for 30 years: about $76,000. Same money, same growth, 1% fee every year: about $57,000.
That's almost $19,000 gone, and you never get a bill for it. It quietly comes out of the fund, a little every day.
I couldn't even see what I owned, just a statement four times a year. That's why I like the idea of an on-chain portfolio:
every holding, every trade, every fee on a public record you can check yourself, any time, from your phone. Not a report. A receipt.
So go look up what your fund charges you. Seriously. Today.

## Fact check
- 10,000 x 1.07^30 = 76,122.55; 10,000 x 1.06^30 = 57,434.91; difference 18,687.64. Simplification: the 1% fee is modelled as 7% - 1% = 6% net (stated in caption).
- Fund expense ratios are taken from fund assets (accrued daily in the NAV), not billed. True for mutual funds and ETFs.
- Holdings disclosure is periodic for most mutual funds (see `brand/instagram-strategy.md`). "A statement four times a year" is the presenter's own experience.
- No return comparison between funds and on-chain portfolios; no crypto vocabulary.

## Production pipeline (all in `build/`)
1. Presenter still: Higgsfield Soul V2 (9:16, 1080p) via Composio instant account.
2. Motion: Higgsfield DOP Lite image-to-video, 5.4 s clips from the same still (prompt keeps hands and phone out of frame; some clips still drift into a phone call, so only clean ranges are used, see `edl.json`).
3. Voice: ElevenLabs `ELEVENLABS_TEXT_TO_SPEECH`, stock Roger only on the instant account. Word timings: faster-whisper base.en (`words.json`).
4. `build_aroll.py` cuts clips (forward and reversed) to the voice timeline.
5. `lipsync.py`: Wav2Lip GAN on CPU, mouth-only ellipse blend with colour match.
6. `restore.py`: GFPGAN v1.4 (vendored arch) restores the mouth area each visible frame (~2 s/frame on 4 CPUs, the slowest step).
7. `phonefix.py` replaces the AI-garbled phone screen with a clean portfolio UI; `render.py` composites captions, card, inserts, end card; `mix.py` builds the sound (car room tone, passing cars, soft pad, pops) and loudnorms.

## Disclosure
Caption and end card state the presenter and voice are AI-generated.
