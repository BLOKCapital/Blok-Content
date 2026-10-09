# BLOK Content

The content studio for **[BLOK Capital](https://blokcapital.io)**, the decentralized wealth-management
protocol on Arbitrum. *It's crypto, but different. Everyone deserves a Garden.* 🌱

Ideas, Instagram carousels, UGC videos, Reels, X threads, long-form, and the calendar all live here,
along with the brand and product knowledge Claude uses to keep everything on-message.

## Quick start
```bash
npm install                                   # carousel renderer (Playwright)
npm run carousel -- content/carousels/2026-10-09-what-is-a-garden/slides.json
bash scripts/setup-composio.sh && composio login   # publishing via Composio
```

## Map
- `CLAUDE.md`: BLOK context + rules for Claude (start here)
- `brand/`: voice, visual identity, compliance, logos
- `knowledge/`: product, glossary, tokenomics, audiences, FAQs, docs snapshot
- `ideas/`: backlog and developed ideas
- `content/`: carousels, UGC videos, short-form, X threads, long-form, calendar
- `templates/`: carousel schema, UGC brief
- `.claude/skills/`: `blok-brand`, `content-ideation`, `instagram-carousel`, `ugc-video`, `short-form-video`, `x-thread`, `composio-publish`
- `docs/composio.md`: Composio setup
