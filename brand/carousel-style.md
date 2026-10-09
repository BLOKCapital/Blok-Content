# Carousel Style: "Sticker" (default for Instagram)

Set by the user on 2026-10-09 from reference carousels by @8xdigitalsolutions (4 slides: "Why Some Brands Grow
Fast (And Others Stay Stuck)", "Fast-Growing Brands:" list, "Bad Ads? You are just making Zuckerberg Richer",
"Want Real Growth in 2026? Start Doing This…"). Reference images are not stored in this public repo (third-party
work and celebrity photos); this file records what to take from them.

## What makes the references work
1. **Slide 1 does the heavy lifting.** One huge, punchy question or bold claim, with a curiosity gap in a lighter
   subtitle: "(And Others Stay Stuck)", "Start Doing This…".
2. **Heavy geometric headline** (black, ExtraBold/Black), left-aligned, one keyword on a **highlighter swipe**.
3. **A big, expressive visual takes up half the slide**: a cut-out with a thick outline "sticker" stroke. In the
   references it's a reaction face (smirk, toast, money eyes). Emotion sells the hook.
4. **Hand-drawn arrows** lead the eye from the text to the visual. **Doodles** (crosshatch corner, burst strokes)
   add energy.
5. **Grid-paper background**: light, clean, "notebook explainer" feel.
6. **Persistent header** (round logo + @handle + one-line descriptor) and **footer** "Share it ↗" / "Save it 🔖".
7. Inner slides: short title + 3–5 bullets **plus** a visual on every slide. Never a text-only slide.

## How BLOK does it (implemented in `scripts/lib/sticker.mjs`, `"style": "sticker"` in slides.json)
- Background: off-white `#FDFCF7` with a linen grid; or `"theme": "dark"` (indigo grid) for one or two contrast slides.
- Headline: **Montserrat 900**; highlight = **lime marker** (`**word**`), coral underline (`__word__`) for warnings.
- Visual: `{"emoji": "🤔", "size": 540, "x": 400, "y": 660, "rotate": 0, "burst": [cx, cy], "burstR": 300}` or
  `{"img": "relative/path.png", ...}`. White + lime outline and soft shadow are added automatically.
  Emoji glyphs render ~1.15× wider than `size`, so keep `x + 1.2*size ≤ 1020`.
- Arrows: `"arrow": {"from": [x, y], "to": [x, y], "bend": -140}` (or `"arrows": [...]`). Negative bend curves
  the other way.
- Slide types: `hook` (cover), `point`, `list`, `flow` (step chain with emoji chips), `compare` (two cards), `cta`.
- Header/footer/page numbers are automatic. The cover gets the crosshatch doodle and no "Save it".

### No celebrities or real people
The references use DiCaprio, Zuckerberg and Mr Bean. **We never use real people's photos or likeness**: it implies
endorsement, breaks image rights, and is a compliance risk for a financial brand. Get the same emotional punch
from expressive emoji faces (🤔😳🫠😏🤯), illustrated objects (🏦📄🔐⏳💸📱), or our own team/creator photos
with consent.

## Cover (slide 1) checklist
- [ ] Question or bold claim in ≤ 7 words; one keyword highlighted
- [ ] Curiosity subtitle in brackets or with "…"
- [ ] A big emotional sticker (≥ 500px) + an arrow pointing at it + a burst or doodle
- [ ] Readable at thumbnail size (look at it at 25%)
- [ ] No crypto words or visuals (Instagram rule)

## Inner slides checklist
- [ ] One idea per slide, ≤ 30 words of body
- [ ] Every slide has a visual (sticker, flow chips, or compare cards)
- [ ] One "honest part" slide on risk
- [ ] Last slide = CTA (below) + disclaimer

## CTA library (last slide + caption)
Primary (use by default):
- Slide: "Want to **own** your portfolio, not just a statement?" + body "Follow BLOK Capital for plain-English
  on-chain portfolio know-how. One idea a week." + button **"Follow @blok.capital"**
Alternatives:
- "Follow @blok.capital: one plain-English on-chain portfolio tip a week."
- "Learn on-chain portfolio management in 60 seconds a week. Follow @blok.capital"
- "Save this, then follow @blok.capital so you don't miss part 2."
- "Send this to the friend who still checks their fund once a quarter."
