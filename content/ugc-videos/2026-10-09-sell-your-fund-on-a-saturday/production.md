# Production notes (AI voice + motion version)

Final file: `reel-final.mp4` (1080×1920, 30fps, ~34s, H.264 + AAC).

## Voice
- Microsoft neural voice **en-US-AndrewMultilingualNeural** via `edge-tts` (free), rate +0%, one continuous take
  of the conversational script in `build/voices/` (word timings in `andrew.json`).
- Alternatives generated: Kokoro `af_heart`, `am_michael` (open-source, run in the Composio sandbox), edge `Ava`.
  Samples in `build/voices/sample-*.mp3`.
- The voice is AI-generated, so the post carries Instagram's **AI label** and "AI-generated voiceover" in caption + end card.

## Visuals
- `build/scene.html` draws every frame from `window.draw(t)`; scenes are timed off `build/timeline.js`
  (sentence + word timings), so swapping the voice only needs a new `timeline.js` + `vo.m4a`.
- Render: `node scripts/render-reel.mjs build/scene.html build/vo.m4a reel-final.mp4 30` (~1 min).

## Script as voiced (conversational edit of the approved script)
POV: you try to sell your index fund... on a Saturday. Order placed. And then... it just waits. Until Monday.
Because markets keep office hours. Weekdays only. On-chain investing works a little differently. Same idea, a basket
of assets, but it runs on a public ledger that never closes. Trades settle in minutes. And you can check every holding
yourself. Is it riskier? Honestly? It's newer, and it can swing more. So, learn first. Follow for plain-English money stuff.
