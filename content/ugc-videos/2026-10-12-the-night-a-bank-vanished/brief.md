# The night a bank vanished (Reel)

**Format:** vertical 1080x1920, 107s, 30fps · **Audience:** fund and ETF investors (Instagram rules apply) · **Status:** published 2026-10-12 (instagram.com/reel/DeZeaBpnefg)
**Reverse-engineered from:** @maya.creates.history, "The night Bitcoin was born" (instagram.com/reel/DdUibQFTzRv, 15K likes).
**Topic choice:** "Is my money safe in the bank?" is one of the most-searched money questions every time a bank wobbles (searches rose 43% during the 2023 bank failures, MediaPost). It ties straight to BLOK's "your keys, always" idea, told without any crypto vocabulary.

## What the reference does (and what we copied)
| Reference | Ours |
|---|---|
| Recurring AI presenter "in the room" at a real historic night, whispering to a phone camera | Same woman (auburn hair, cream cardigan) in a startup office on 9 March 2023, the night of the Silicon Valley Bank run |
| Cold open that makes you lean in ("Don't film their face.") | "Shh. Look at his phone." |
| Title card: heavy serif, one word in green ("The night **Bitcoin** was born.") | "The night a **bank** vanished." (Fraunces, lime #7ED116) |
| "Simple version" ELI5 with tiny numbers ("You've got 50, I've got 20") | "Your balance is a promise. You've got a hundred, they owe you a hundred." |
| A real dated prop (that morning's newspaper headline) | Real dated figures typed on a dark screen: $42B asked back in one day, $100B expected next day (US Federal Reserve) |
| "So here's the idea." pivot to the solution | Same pivot to an account only you control on a public ledger |
| Small lowercase monospace captions, 2–4 words, lower third | Same (JetBrains Mono) |
| Ends on a quotable line that lingers | "A promise to pay you isn't the same as owning it." |
| Moody blue night grade, handheld, film grain, edge colour fringing | Same: Ken Burns + handheld wobble, grain, vignette, chromatic edge |

## Production
- Stills: Gemini image model (Nano Banana Pro) via Composio, prompts in this file's history (`build/img/*.jpg`). No real people depicted.
- Voice: Gemini 2.5 Pro TTS, voice "Aoede", hushed vlogger direction, five takes stitched (`build/vo.wav`), word timings from Whisper (`build/vo.json`). Edge TTS (Andrew) now returns 403 from the sandbox.
- Music + SFX: original, synthesised in `build/mix.py` (D minor pad turning to D major at "So here's the idea", phone buzzes, message pops, keyboard clicks, tension pulse during the run, sub booms). -14 LUFS.
- Rebuild: `python3 build/align.py build` → (caption chunking in thread notes) `build/timing.json` → `node build/preview.mjs "" /tmp` (writes scene.built.html + cues.json) → `python3 build/mix.py` → `node scripts/render-reel.mjs build/scene.built.html build/mix.wav the-night-a-bank-vanished.mp4 30`.

## Fact check
- 8 Mar 2023: SVB announced a $1.8B loss on securities sales and a plan to raise capital (Axios timeline).
- 9 Mar 2023: customers withdrew/attempted to withdraw $42B in one day; ~$100B more was queued for 10 Mar (Fed Vice Chair Barr testimony, 28 Mar 2023; CNBC, Fortune).
- 10 Mar 2023 morning: California regulator closed the bank, FDIC appointed receiver.
- 12 Mar 2023 (Sunday): regulators guaranteed all deposits; depositors were made whole. Hence "for a whole weekend, nobody knew".

## Caption
The night a bank vanished. 🌱

9 March 2023. Customers asked Silicon Valley Bank for $42 billion back in a single day. By the next morning it was shut down. Everyone did get their money back in the end, but for a whole weekend nobody knew.

The simple lesson: a bank balance is a promise. An on-chain portfolio sits in an account only you control, on a public ledger anyone can check. It's newer and prices can swing, so start small and learn first.

Would you rather hold a promise, or the thing itself? 👇

Follow @blok.capital for plain-English lessons on on-chain portfolios.

Figures: US Federal Reserve (Barr testimony, March 2023). Educational content only, not financial or investment advice. On-chain assets can be volatile and you can lose money. AI-generated voice and visuals; events dramatised. Original music.

#investing #personalfinance #banking #moneytips #financialliteracy #mutualfunds #ETF

## Compliance
- No crypto vocabulary or visuals; "public ledger" and "on-chain portfolio" in plain words.
- No return claims; risk line spoken ("newer, prices can swing, you're responsible") and on end card.
- Fair to banks: says depositors were made whole; no "unsafe" claims about banks in general.
- Chat screen and ledger labelled Illustrative; figures sourced on screen.
- AI disclosure on end card and caption; switch on Instagram's AI label when posting.
