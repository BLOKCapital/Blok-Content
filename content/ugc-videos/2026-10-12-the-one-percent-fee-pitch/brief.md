# Reel: "Your fund's 1% fee isn't small" (pitch-video edit)

**Status:** rendered, awaiting approval. Not posted.
**File:** `the-one-percent-fee-pitch.mp4` (1080x1920, 52.3 s, 30 fps, H.264 + AAC 48 kHz, -14.5 LUFS). Caption: `caption.md` (same as the talking-head version).

Same lip-synced presenter take as `../2026-10-12-the-one-percent-fee/`, re-edited with the
[pitch-video skill](https://github.com/codeswithroh/pitch-video): pauses trimmed and 1.1x speed-up, word-anchored scenes,
face bubble during product shots, scene chips, a maths explainer animation, filmed (illustrative) app and statement footage,
synth music ducked under the voice, auto SFX, and the skill's `verify.py` QA (RESULT: PASS).

## Scenes
1. Hook (full-frame presenter)
2. The maths: animated chart, $10,000 at 7% vs 6% net over 30 years ($76,123 vs $57,435, gap $18,688), then a "bills sent to you: 0" card
3. What I could see: an illustrative quarterly statement ("holdings as of 30 June", "next update: 3 months")
4. Receipts: an illustrative portfolio app (holdings, activity, a trade entry on a public record), then "Not a report. A receipt."
5. Outro: presenter, then a linen end card with the wordmark, AI disclosure and the disclaimer

## Portrait adaptation of the skill (`build/pitch-video-portrait.patch`)
- Canvas 1080x1920; captions raised above Instagram's bottom UI; face bubble and chip at the top; brand colours; opaque linen end card shown after the last word.
- whisper-cli replaced by a faster-whisper shim (same JSON output).
- Fix: opaque PNG overlays (RGB) froze the card track in the concat demuxer; compose now forces RGBA.
- verify.py: lip-landmark sync is unreliable on a Wav2Lip mouth (scattered, r about 0.15), so a mouth-interior measure was added. It showed Wav2Lip's picture leading the voice by about 100 ms; the take was delayed 3 frames, now 0 ms.

## Compliance
No crypto vocabulary in visuals; app and statement are labelled illustrative with made-up names; maths labelled "Not a forecast";
AI presenter and voice disclosed on the end card and in the caption; standard disclaimer on the end card.
