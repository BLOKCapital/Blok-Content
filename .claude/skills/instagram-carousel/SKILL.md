---
name: instagram-carousel
description: Write, design and render on-brand Instagram/LinkedIn carousels for BLOK Capital as 1080x1350 PNGs, plus caption and hashtags. Use whenever the user asks for a carousel, slide post, swipe post, educational slides or an infographic series.
---

> **Style:** use `"style": "sticker"` and follow `brand/carousel-style.md` (killer cover, a visual on every slide, no real people, CTA library). Example: `content/carousels/2026-10-10-who-holds-your-money/`.
> **Rendering and publishing:** follow `docs/playbook.md` sections 3 and 6. The renderer writes publish-ready JPEGs to `export/jpg/`.


# Instagram carousel

## 1. Load context
**Read `brand/instagram-strategy.md` first. It overrides the general brand guide for Instagram:** the audience is mutual fund / ETF investors, the content is purely educational about on-chain finance, and there's no crypto vocabulary or imagery at all. Footer handle: `@blok.capital`.

Use the `blok-brand` skill's reading list. Pick the audience and pillar (`knowledge/audiences.md`).

## 2. Structure (7–10 slides; 7 is the sweet spot)
| Slide | Job | Type |
|---|---|---|
| 1 | **Hook**: a scroll-stopping promise, question or contrarian line. ≤8 words. | `cover` |
| 2 | **Problem / tension**: why this matters; name the status-quo pain. | `text` or `compare` |
| 3–N-2 | **Value**: one idea per slide, concrete, glossed jargon, garden metaphor ≤2 total | `text` `list` `stat` `compare` |
| N-1 | **Payoff / reframe**: the "aha" or signature line | `quote` or `text` (theme `indigo`) |
| N | **CTA**: save/share/follow/visit + risk disclaimer if investing is discussed | `cta` with `"disclaimer": true` |

Rules: one idea per slide · ≤30 words body · every slide must make sense alone · end slides on
a micro-cliffhanger to drive swipes · alternate themes sparingly (mostly `linen`, 1–2 `indigo`/`night` for rhythm).

## 3. Write `slides.json`
Folder: `content/carousels/YYYY-MM-DD-<slug>/`. Schema: `templates/carousel/README.md`.
Example: `content/carousels/2026-10-09-what-is-a-garden/slides.json`.

## 4. Render & QA
```bash
npm install            # first time only
npm run carousel -- content/carousels/<folder>/slides.json
```
Then **look at every PNG** (Read the images, or stitch a contact sheet with ffmpeg `hstack`) and check:
text overflow, orphaned words, contrast, logo visible, slide count label, disclaimer present.
Fix copy (not CSS) first; adjust `scripts/render-carousel.mjs` only for systemic issues.

## 5. Caption → `caption.md` in the same folder
- Line 1: hook restated (≤125 chars so it shows before "more").
- 3–6 short lines of value, 1–2 emoji max (🌱).
- CTA: "Save this 🌱" / "Plant your first Garden: link in bio".
- Disclaimer from `brand/instagram-strategy.md` when investing is discussed.
- 3–5 hashtags, no crypto tags: #InvestingBasics #MutualFunds #ETFInvesting #PersonalFinance #FinancialLiteracy #OnChainFinance.
- Alt text for slide 1.

## 6. Compliance pass
Run the `brand/compliance.md` checklist. Then hand off to `composio-publish` only if the user asks to post.

If the Social Media Skills plugin is installed, its `carousel-writer` and `hook-writer` skills can be used for extra hook variants; BLOK rules here win on conflicts.
