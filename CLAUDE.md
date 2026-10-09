# CLAUDE.md — BLOK Capital Content Studio

This repo is BLOK Capital's content studio. Everything marketing and content lives here:
ideas, scripts, Instagram carousels, UGC-style videos, X threads, long-form posts,
the content calendar, and the brand knowledge that keeps it all on-message.

Read this file first in every session. For depth, go to `knowledge/` and `brand/`.

---

## 1. What BLOK Capital is (the 60-second version)

**BLOK Capital is a decentralized, non-custodial wealth-management protocol on Arbitrum.**
Anyone with a wallet can "plant a Garden" (a personal on-chain portfolio), then either
follow a curated, auto-rebalancing **Index** or manage it themselves with built-in DeFi
tools. Later, verified on-chain managers called **Gardeners** can manage Gardens for
clients. Throughout, **the user's keys and assets never leave their own wallet.**

- **Founded:** 2023. Run as a **DAO** (Aragon OSx), governed by **$BLOKC** holders.
- **Motto:** *"It's crypto, but different."*
- **Brand promise:** *"Everyone deserves a Garden."*
- **Positioning:** The transparent, accessible alternative to traditional wealth
  management (custodians charging "2-and-20" and sending quarterly PDFs as
  "transparency"). BLOK gives you **on-chain receipts instead of reports**.
- **Who it's for:** time-poor, novice-to-intermediate investors who want structured,
  long-term crypto exposure, *not* high-velocity traders or degens.
  (Docs: "We are going for this market and not professional high velocity traders.")

### The three audiences
| Audience | What they want | What BLOK gives them |
|---|---|---|
| **Investors / Garden Owners** | Grow crypto without babysitting charts, without handing over keys, without minimums | Gardens, curated Indices, self-custody, gasless txs, no KYC at protocol layer, deposit from 10 USDC |
| **Gardeners (managers)** | Publish strategies, take clients, build a verifiable track record | On-chain strategy publishing; reputation recorded in a soulbound (ERC-5484) badge. *Status: coming soon* |
| **Builders (devs)** | Compose with / extend the protocol | Open-source MIT contracts, EIP-2535 Diamond architecture, facets, integrations |

### Core product concepts (use these words consistently)
- **Garden** — your personal on-chain portfolio/vault (technically a Diamond smart contract you own).
- **Garden Owner** — the investor who controls the Garden.
- **Index Garden** — connected to an Index; **rebalances automatically** to target weights.
- **Self-managed Garden** (a.k.a. Yield Garden) — you choose assets and trades; no auto-rebalancing.
- **Index** — a curated basket with calculated weights (e.g. market-cap weighted). Planned
  indices: **BLOKC2, BLOKC5, BLOKC10** (roadmap target Q2 2026 — verify status before claiming live).
- **Gardener** — a verified on-chain manager who can trade/swap inside a client's Garden under
  smart-contract rules, but **can never withdraw or transfer funds out**.
- **Smart Wallet Account (SWA)** — ERC-4337 smart account created at sign-in (Google login via
  Web3Auth MPC). No seed-phrase friction for newcomers.
- **Passes** — soulbound access passes (e.g. Builder Pass, Baddie Pass, Angel Pass) minted at
  onboarding; each pass unlocks one Garden in a collection.
- **Rebalancer Network** — batches rebalances for all Gardens on an Index in one efficient
  transaction; two-step intent → execute to resist flash-loan manipulation.
- **DAO** — protocol upgrades and parameters voted on by BLOKC holders.

### User journey (how a newcomer actually uses it)
1. Sign in with Google → smart wallet created (no seed phrase to scribble down).
2. Optional referral code → soulbound pass minted.
3. Create a Garden in a collection.
4. Fund it (from as little as **10 USDC**).
5. Choose: connect an **Index** (auto) or go **Self-managed** (manual).
6. Track portfolio value, P&L, allocation, rebalancing history in the app.
7. Vote in the DAO tab with BLOKC.

### Key facts & proof points (safe to use)
- Chain: **Arbitrum One** today. Cross-chain Gardens (Arbitrum, Base, others) are a **roadmap** item (Q4 2027 target).
- **Self-custody:** "Your keys, always." No one, including Gardeners and BLOK, can withdraw your funds.
- **Gasless** transactions today; **no platform fees currently** (future fees set by DAO vote).
- **No minimums** (10 USDC), **no geographic restrictions**, **no KYC at protocol layer**, withdraw anytime.
- **Everything on-chain:** every position and transaction is verifiable.
- **Open source:** MIT-licensed contracts, EIP-2535 Diamond pattern.
- **Integrations / ecosystem:** Uniswap, Camelot, GMX, Aave, Pendle, Chainlink oracles,
  Web3Auth, ZeroDev, Pimlico, Transak, Aragon.
- **Security:** reviews by CredShields, SolidityScan, Octane (at least one contract still under
  review); bug bounty (Immunefi) and audit contests (Cantina, Code4rena) announced.
  Say "security-reviewed", never "fully audited" or "unhackable".

### $BLOKC token
- ERC-20 on Arbitrum, **10B supply**, 18 decimals. Contract: `0xbc4d9d3dfe6ab1d36ede90050ce96fcb937469f0`.
- Utility: governance voting, fee payments between investors and Gardeners, loyalty rewards
  for good long-term behaviour, staking tiers (Bronze/Silver/Gold/Diamond), referral rewards.
- **IDO planned Q2 2027.** Treat all token content with extra care (see compliance below).
- Full allocation table: `knowledge/tokenomics.md`.

### Team (core DAO contributors)
0xSheetal (Sheetal Nehra, founder), 0xChintan, Elvis, John Adebayo, Mohammed Raihani,
Prof. Andy Wynn, Aditya Biradar, Vansh Sahay, Devang Gandhi, Rohit Purkait.
Don't invent titles for anyone; ask if a role is needed.

### Official links
- Site: https://blokcapital.io · Docs: https://docs.blokcapital.io (full corpus: `/llms-full.txt`)
- X: [@blok_cap](https://x.com/blok_cap) · Telegram: t.me/BLOKCapital · Discord: discord.com/invite/blokc · Farcaster: warpcast.com/blokc
- GitHub: github.com/BLOKCapital · Whitepaper: docsend.com/view/4j6qvvrudyr6izyb

---

## 2. Brand voice (summary; full guide in `brand/voice.md`)

**Warm, plain-spoken, editorial, a little playful, and anti-hype.** We sound like a
smart friend who's good with money and allergic to BS, not like a crypto shill or a bank.

- **Garden metaphor everywhere:** plant, seed, grow, tend, prune (rebalance), soil, harvest,
  season. Use it with a light touch; one or two per piece, not every sentence.
- **Signature lines:** "It's crypto, but different." · "Everyone deserves a Garden." ·
  "Compound, not pump. Boring is a feature." · "Receipts beat reports." · "Your keys, always." ·
  "Built by the community, for the world." · Sign-off: "Yours in the soil."
- **Explain like a human:** every jargon term gets a plain-English gloss the first time.
- **Pick fights with the status quo, not with people:** TradFi gatekeeping, opaque fees,
  quarterly PDFs, custodial blow-ups, "trust me bro" influencers.
- **Never:** moon/lambo/100x/"not financial advice but…", rocket-emoji spam, FOMO countdowns,
  price predictions, guaranteed returns.

## 3. Visual identity (summary; full guide in `brand/visual-identity.md`)

| Name | Hex | Use |
|---|---|---|
| Sky Blue | `#7DD2FD` | Primary highlight, from the logo |
| Deep Indigo | `#004EBA` | Depth, credibility, headlines on light |
| Lime Green | `#7ED116` | Growth/action (the Garden colour) |
| Neutral Linen | `#F6F3E8` | Backgrounds ("paper") |
| Coral Red | `#EC464D` | Sparingly: CTAs, key moments |
| Earth Brown | `#844947` | Outlines, shadows, support elements |

Logo files: `brand/assets/` (mark on white, mark on black, horizontal wordmark).

## 4. Compliance guardrails (non-negotiable)

Crypto marketing is regulated and BLOK's whole brand is trust. Every piece must pass
`brand/compliance.md`. The short list:
1. No promises or projections of returns. No "earn X%", "guaranteed", "risk-free", "safe".
2. Any performance figure must be real, sourced, dated, and labelled; site dashboards are **illustrative**.
3. Roadmap items are **targets**, phrased as "planned"/"coming", never as live.
4. No token price talk, no "buy $BLOKC" calls, no IDO hype. Token content = utility and governance only.
5. Include a risk line where content discusses investing ("Crypto is volatile. Only invest what you can afford to lose.").
6. Don't name or disparage competitors by name without approval.
7. UGC must disclose partnership (#ad / "paid partnership") when creators are compensated.

---

## 5. How this repo is organised

```
CLAUDE.md                 ← you are here
brand/                    voice, visual identity, compliance, logo assets
knowledge/                product facts, glossary, tokenomics, audiences, FAQs, sources
ideas/                    idea backlog + one file per idea worth developing
content/
  carousels/              Instagram/LinkedIn carousels (slides.json → rendered PNGs)
  ugc-videos/             UGC video briefs, scripts, shot lists, creator briefs
  short-form/             Reels/TikTok/Shorts scripts (non-UGC: faceless, explainer, motion)
  x-threads/              X posts and threads
  long-form/              blog posts, newsletters, Mirror/Paragraph articles
  calendar/               content calendar and campaign plans
templates/                reusable templates (carousel HTML, briefs, scripts)
scripts/                  tooling: carousel renderer, Composio setup
.claude/skills/           project skills (carousel, UGC, ideation, threads, publishing…)
```

### File naming
`YYYY-MM-DD-short-slug` for every dated piece, e.g.
`content/carousels/2026-10-12-what-is-a-garden/`. One folder per multi-file piece.

### Workflow for any piece of content
1. **Idea** → `ideas/backlog.md` (one line) → promote to `ideas/<slug>.md` when worth developing.
2. **Draft** in the right `content/` folder using the matching skill.
3. **Self-check** against `brand/voice.md` and `brand/compliance.md`.
4. **Render/produce** (carousel PNGs via `scripts/render-carousel.mjs`; video via brief/script).
5. **Publish/schedule** via Composio (only when the user explicitly says to post).
6. Log it in `content/calendar/` with link + date.

## 6. Skills & tools

Project skills in `.claude/skills/` (invoke with `/skill-name`):
- `blok-brand` — load brand context + voice + compliance before writing anything.
- `content-ideation` — generate and score ideas by pillar and audience.
- `instagram-carousel` — write + design + render on-brand carousels to PNG (1080×1350).
- `ugc-video` — UGC briefs, hooks, scripts, shot lists, creator briefs, AI-avatar prompts.
- `short-form-video` — faceless/explainer Reels & TikToks, captions, b-roll lists.
- `x-thread` — X posts and threads in BLOK voice.
- `composio-publish` — publish/schedule via Composio (Instagram, X, LinkedIn, etc.).

Recommended marketplace plugins (install from the Claude plugin directory):
**Social Media Skills**, **Remotion** (programmatic video rendering), **Marketing** (Anthropic).

**Composio** — see `scripts/setup-composio.sh` and `docs/composio.md`. Needs
`COMPOSIO_API_KEY` set as an environment secret. **Never post publicly without explicit
user confirmation for that specific post.**

## 7. Rules for Claude in this repo
- Ground every factual claim in `knowledge/` or the live docs. If unsure, check
  https://docs.blokcapital.io/llms-full.txt or ask. Don't invent stats, partners, or dates.
- When facts change (launches, roadmap, team), update `knowledge/` **and** this file.
- Default formats: Instagram carousel 1080×1350 (4:5), Reels/TikTok 1080×1920 (9:16), X ≤ 280 chars/post.
- Write in **English** by default; docs also exist in Spanish and French if localising.
