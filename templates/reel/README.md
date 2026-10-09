# Reel template (AI voiceover + motion graphics)

`scene.html` is the scene file from the first published Reel ("POV: you try to sell your index fund on a
Saturday"). Copy it into a new piece's `build/` folder and edit it.

## How a scene works
- `timeline.js` (generated) sets `window.TIMELINE`: one entry per line of `script.txt` with `start`, `end`
  and per-word timings.
- `S(i)` = the start time of line *i*. Every animation keys off these, so the visuals stay in sync with
  whatever voice you generate.
- `window.draw(t)` sets the whole frame for time `t` (seconds). The renderer calls it for every frame.
- Scenes are absolutely positioned `.scene` divs faded with `win(t, a, b)`; elements pop in with
  `pop(el, t, at)`.
- Captions are automatic: word-by-word highlight, up to 6 words at a time, using the real word timings.
- `window.DURATION` = last word + 1.6s hold on the end card.

## Rules
- 1080×1920. Keep text between y=220 and y=1540 (Instagram UI covers the rest). Captions sit at y=1400.
- Brand palette only (CSS vars at the top). Fonts: Fraunces / Inter / JetBrains Mono.
- Emoji: load `Noto Color Emoji` from Google Fonts and set `font-family:'Noto Color Emoji'` on the element (the system has no colour-emoji font).
- Instagram content: no crypto words or visuals (`brand/instagram-strategy.md`).
- End card: logo + follow button + "Educational only · Not financial advice" + "AI-generated voiceover".
- Logo path `../../../../brand/assets/logo-wordmark.png` assumes the file lives at `content/<type>/<slug>/build/`.
