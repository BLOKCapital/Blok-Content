---
name: blok-brand
description: Load BLOK Capital brand context (product facts, voice, visual identity, compliance) before writing or reviewing ANY BLOK content: posts, carousels, scripts, threads, captions, emails, articles. Also use to review a draft for on-brand voice and compliance.
---

# BLOK brand loader & reviewer

## Before writing
Read, in order (skip any already in context this session):
1. `CLAUDE.md` (sections 1–4)
2. `brand/voice.md`
3. `brand/compliance.md`
4. `knowledge/product.md`, `knowledge/glossary.md`, `knowledge/audiences.md` as relevant
5. `brand/visual-identity.md` if the piece is visual
6. `brand/instagram-strategy.md` for **anything going to Instagram** (it overrides the rest)

For any fact not in `knowledge/`, check `knowledge/snapshots/` or fetch
https://docs.blokcapital.io/llms-full.txt. Never invent stats, partners, dates, or features.

## Review mode (when asked to check a draft)
Return a short report:
- **Voice score (1–5)** with 2–3 concrete line edits (warm, plain, anti-hype, garden metaphor ≤2).
- **Compliance:** walk the checklist in `brand/compliance.md`; list every violation with the fix.
- **Facts:** flag any claim not traceable to `knowledge/`; flag roadmap items phrased as live.
- **Jargon:** every technical term glossed on first use?
- **Revised version** of the draft with fixes applied.
