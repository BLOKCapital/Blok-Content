---
name: composio-publish
description: Publish, schedule or fetch analytics for BLOK Capital content through Composio (Instagram, X/Twitter, LinkedIn, YouTube, TikTok, Telegram, Discord, Google Drive, Notion, Slack…). Use when the user asks to post, schedule, upload, cross-post, pull metrics, or connect a social account.
---

# Publish via Composio

## Golden rule
**Never publish, schedule, DM, or delete anything without the user's explicit confirmation for that exact
post** (show final copy + media + account + time first). Drafts and analytics reads are fine.

## Setup check
1. `composio --version` (CLI). If missing: `bash scripts/setup-composio.sh`.
2. Auth: `COMPOSIO_API_KEY` must be set (environment secret), or run `composio login` in an interactive terminal.
3. See `docs/composio.md` for connecting accounts (Instagram Business, X, LinkedIn page, etc.).
If the CLI can't be installed (network policy), say so and stop; don't fake a post.

## Flow
1. Confirm piece is final: compliance check done, media rendered (`export/*.png` or final mp4).
2. Identify the toolkit + connected account (`composio` CLI or Composio MCP tools if connected).
   Discover the exact action names from Composio rather than guessing (e.g. search tools for "instagram carousel").
3. Media (Instagram): local files can't be sent directly. Proven route:
   - Copy `scripts/render-carousel.mjs` and the piece's `slides.json` into the Composio remote sandbox
     (via the remote bash tool, quoted heredoc) and verify both with `md5sum` against the local copies.
   - In the sandbox: `npm i playwright@1.56.1 && npx playwright install --with-deps chromium`; fetch logos from
     `https://blokcapital.io/brand/logo-wordmark.webp` and `https://docs.blokcapital.io/img/primary-{w,b}.png`
     (mark files resized to 1024px wide); render; convert to JPEG (quality 95, no chroma subsampling).
   - `upload_local_file()` each JPEG → pass the `s3key`s as `child_image_files` to `INSTAGRAM_CREATE_CAROUSEL_CONTAINER`.
   - Pull a contact sheet back and eyeball it against the approved render before publishing.
4. Show a **preview summary** → wait for "yes, post it".
5. Execute; record the result (post URL/ID, time, account) in `content/calendar/published.md`.

## Analytics
Pull reach, saves, shares, comments for posts in `content/calendar/published.md`; write learnings to
`content/calendar/learnings.md` (what hooks/formats won).
