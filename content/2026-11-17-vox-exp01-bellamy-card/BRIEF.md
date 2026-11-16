# BRIEF.md (locked) · Vox-style demo: "He predicted the credit card in 1888"

Demo for Sheetal of Naomi Metzger's Vox-reel workflow. Not for posting.

## Story
In 1888 Edward Bellamy's novel *Looking Backward* imagined Boston in the year 2000, where people pay with a
pasteboard "credit card" and the clerk pricks off each purchase. 62 years before the first real multipurpose card
(Diners Club, 1950). He got paying right. What he missed: paying got easy for everyone, owning a fund didn't.
Many private funds still ask $100,000+ to get in. BLOK: anyone can start their own fund from $10.

Angle chosen over: (a) 1954 NYSE "$40 a quarter" plan (too close to Thrift Stamps), (b) 1774 first fund (already made
22 Oct), (c) 1900 Ladies' Home Journal predictions (no money hook). Bellamy wins: almost nobody knows the phrase
"credit card" is from an 1888 novel, the real book page is public domain so we can show the receipt on screen,
and "he predicted how we'd pay, not who gets to own" lands the access message without fee-bashing.

## Sources (every claim)
| Claim | Source |
|---|---|
| 1888 novel, Boston, sleeper wakes in 2000 | *Looking Backward: 2000–1887*, Houghton Mifflin (1890 printing scanned at archive.org/details/lookingbackward20000edwa_f6n7) |
| "a credit card issued him", "piece of pasteboard" | Same scan, page 87 (shown on screen) |
| Purchases "pricked off the credit card" | Same scan, ch. 10 |
| First multipurpose charge card, Feb 1950 | Diners Club history (dinersclub.com/about-us/history) |
| Private/hedge funds: typical minimums $100,000 to $2M | SoFi "How to invest in hedge funds"; SEC Investor Bulletin: Hedge Funds (accredited investors only) |
| BLOK from $10 (10 USDC) | CLAUDE.md / knowledge/ ("We're building", not "live") |
| Boston 1880 view | O. H. Bailey & Co. lithograph, Library of Congress 75694557 (public domain) |

## Look rules
- 1080x1920, 30 fps output, **animation on 12s** (stop-motion: positions only update 12 times a second, cut-outs
  jitter ±1.5 px / ±0.4° every other frame). No smooth easing glides.
- Every scene in 6 layers, each moving at a different speed: background (paper/map, slowest drift) → subject cut-out →
  foreground (tape, arrows, highlighter) → text → paper texture (multiply) → film grain (new noise every frame).
- Cut-outs have a white paper border + soft drop shadow, like they were scissored out and laid on the desk.
- Things **drop in one at a time** (fall from above, small overshoot, land with a thud on 12s).
- Real archival material only for the history: the actual 1890 book cover and page 87, the 1880 Boston lithograph.
  No AI faces, no real person's photo (BLOK rule: names as text only).
- Palette: Linen paper #F6F3E8, ink #1d1b17, highlighter Lime #7ED116, Coral #EC464D for the "but", Indigo #004EBA.
- Fonts: captions Plus Jakarta Sans ExtraBold (Sheetal's 15 Nov rule: clean bold sans). Labels/dates Courier Prime
  Bold (typewriter, documentary feel, not AI-looking).
- Captions bottom, inside y 220–1540, 2–5 words at a time, current word in lime highlight.

## Never
Crypto words or visuals · fee-bashing · rupees · return promises · thin display serifs for captions · smooth
glides · overwriting any older version.

## Length
~40 s. Audio first (Brooks Chatterbox, 3 takes per line, Whisper-scored), music bed down, 3 mixes, build to audio.

## Versions
`vox-demo-v1-draft.mp4` (low-quality 540p preview) → `vox-demo-v2.mp4` (full quality). Never overwrite; new number per change.
