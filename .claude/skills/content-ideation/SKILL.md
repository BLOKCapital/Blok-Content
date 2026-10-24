---
name: content-ideation
description: Generate, score and organise BLOK Capital content ideas (carousels, UGC videos, Reels, threads, articles) by pillar, audience and format. Use for brainstorming, filling the content calendar, campaign concepts, or turning a topic/news item/doc page into content angles.
---

# Content ideation

Load `blok-brand` context first (CLAUDE.md, brand/voice.md, knowledge/audiences.md).

## Process
**Step 0, always: the trend check** (`growth/trend-playbook.md`). Read today's board in `growth/trends/`
(or run the radar if it's missing or stale), and build ideas on what's hot today. About 60% of ideas should be
trend-led, ~25% evergreen with a "why now" hook, ~15% action posts. Combine trends with the history-to-today
pattern where it fits, and give several angles before picking the sharpest.

**Instagram ideas** must fit `brand/instagram-strategy.md`: audience = mutual fund / ETF investors, purely educational about on-chain finance, no crypto vocabulary.

1. **Clarify the goal** if unclear: awareness, education, waitlist/app sign-ups, community, builder recruitment, Gardener recruitment.
2. **Generate** ideas across the five pillars (Educate 35%, Contrast 20%, Product 20%, Trust 15%, Community 10%) and the four audiences.
3. For each idea give: **working title · trend it rides (link, heat, age) or "evergreen: why now" · remix move · take temperature (mild/spicy/hot) · hook (first line/first 2s) · pillar · audience · best format(s) · why it'll work · source fact** (file in `knowledge/` or the trend's primary source).
4. **Score** each 1–5 on: Heat (how hot and fresh the trend is) · Hook strength · Brand fit · Clarity · Effort (5 = easy) · Compliance risk (5 = safe). Sum, sort desc. Safety under 4 = drop it, however hot.
5. **Repurpose map** for the top 3: one idea → carousel + UGC/Reel + X thread + caption.

## Remix moves for trends (details in `growth/trend-playbook.md`)
Quote-jack · format-jack · receipt redraw · history rhyme · calm explainer · counter-take · question post.
Spicy is our default; hot takes go to Sheetal first; never insult people, name competitors, or attack 1% fees.

## Hook formulas that suit BLOK
- Myth-bust: "You don't need $100k to have a wealth manager."
- Contrast: "Your bank sends you a PDF. Your Garden sends you receipts."
- Confession/POV (UGC): "POV: you finally stopped checking charts every 10 minutes."
- Explainer: "Crypto index funds, explained with a vegetable garden."
- Question: "Who actually holds your crypto right now?"
- Number: "4 things your crypto exchange doesn't want you to ask."
- Anti-hype: "This is the most boring crypto video you'll watch today. Good."

## Output
- Append one-liners to `ideas/backlog.md` (table row: date, title, pillar, audience, format, score, status=new; put the trend link in the title cell as "(trend: …)").
- For ideas the user picks, create `ideas/<YYYY-MM-DD>-<slug>.md` from `ideas/_template.md`.
