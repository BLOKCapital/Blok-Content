---
name: content-ideation
description: Generate, score and organise BLOK Capital content ideas (carousels, UGC videos, Reels, threads, articles) by pillar, audience and format. Use for brainstorming, filling the content calendar, campaign concepts, or turning a topic/news item/doc page into content angles.
---

# Content ideation

Load `blok-brand` context first (CLAUDE.md, brand/voice.md, knowledge/audiences.md).

## Process
**Instagram ideas** must fit `brand/instagram-strategy.md`: audience = mutual fund / ETF investors, purely educational about on-chain finance, no crypto vocabulary.

1. **Clarify the goal** if unclear: awareness, education, waitlist/app sign-ups, community, builder recruitment, Gardener recruitment.
2. **Generate** ideas across the five pillars (Educate 35%, Contrast 20%, Product 20%, Trust 15%, Community 10%) and the four audiences.
3. For each idea give: **working title · hook (first line/first 2s) · pillar · audience · best format(s) · why it'll work · source fact** (file in `knowledge/`).
4. **Score** each 1–5 on: Hook strength · Brand fit · Clarity · Effort (5 = easy) · Compliance risk (5 = safe). Sum, sort desc.
5. **Repurpose map** for the top 3: one idea → carousel + UGC/Reel + X thread + caption.

## Hook formulas that suit BLOK
- Myth-bust: "You don't need $100k to have a wealth manager."
- Contrast: "Your bank sends you a PDF. Your Garden sends you receipts."
- Confession/POV (UGC): "POV: you finally stopped checking charts every 10 minutes."
- Explainer: "Crypto index funds, explained with a vegetable garden."
- Question: "Who actually holds your crypto right now?"
- Number: "4 things your crypto exchange doesn't want you to ask."
- Anti-hype: "This is the most boring crypto video you'll watch today. Good."

## Output
- Append one-liners to `ideas/backlog.md` (table row: date, title, pillar, audience, format, score, status=new).
- For ideas the user picks, create `ideas/<YYYY-MM-DD>-<slug>.md` from `ideas/_template.md`.
