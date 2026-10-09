# Carousel template & renderer

**Instagram default: `"style": "sticker"`.** Schema, visuals, arrows and checklists: `brand/carousel-style.md`.
The schema below is the older editorial style (still supported).

Render: `npm run carousel -- content/carousels/<slug>/slides.json`
Output: `content/carousels/<slug>/export/slide-NN.png` (1080×1350) + `preview.html`.
First time in a fresh environment: `npm install`.

## slides.json schema
```jsonc
{
  "title": "Internal title",
  "handle": "@blok_cap",          // footer handle
  "theme": "linen",               // default theme: linen | indigo | night | lime
  "showPageNumbers": true,
  "disclaimer": "Crypto is volatile…",  // used by slides with "disclaimer": true
  "slides": [
    { "type": "cover",   "kicker": "", "title": "", "subtitle": "" },
    { "type": "text",    "kicker": "", "title": "", "body": "" },
    { "type": "list",    "title": "", "items": ["", ""] },
    { "type": "compare", "title": "", "left": {"label":"Old way","items":[]}, "right": {"label":"A Garden","items":[]} },
    { "type": "stat",    "value": "10 USDC", "title": "", "body": "" },
    { "type": "quote",   "quote": "", "by": "" },
    { "type": "cta",     "title": "", "body": "", "button": "blokcapital.io", "handle": "", "disclaimer": true }
  ]
}
```
Any slide can override `"theme"` and set `"disclaimer": true | "custom text"`.

Inline formatting: `**word**` = brand highlight, `__word__` = coral underline, `\n` = line break.

## Copy limits (keep slides scannable)
| Field | Max |
|---|---|
| cover title | ~8 words |
| h2 title | ~7 words |
| body | ~30 words |
| list items | 3–5 items, ≤ 9 words each |
| compare items | 3–4 per side, ≤ 6 words |

Example: `content/carousels/2026-10-09-what-is-a-garden/`.
