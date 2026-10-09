---
name: ugc-video
description: Plan and write UGC-style (user-generated-content look) short videos for BLOK Capital, covering concepts, hook variants, timestamped scripts, shot lists, on-screen text, captions/SRT, creator briefs, AI-avatar/voice prompts, and post-production. Use for TikTok/Reels/Shorts UGC, creator ads, testimonial-style, POV, talking-head, green-screen or "street interview" formats.
---

# UGC video

UGC = looks like a real person filmed it on their phone: authentic, imperfect, native to the feed.
For BLOK it must also be **honest**: no fake customers, no fake gains, disclosed partnerships.

## 1. Load context
**For Instagram (Reels/UGC), read `brand/instagram-strategy.md` first and follow it over everything below:** audience = mutual fund / ETF investors, purely educational about on-chain finance, no crypto words, visuals or token talk.

`blok-brand` reading list + `knowledge/audiences.md`. Choose ONE audience and ONE message pillar per video.

## 2. Pick a format
| Format | Best for | Notes |
|---|---|---|
| **POV / relatable skit** | Busy Grower awareness | "POV: you stopped doom-checking charts" |
| **Talking head explainer** | Education | Creator explains one concept, phone selfie, captions |
| **Green-screen reaction** | Contrast pillar | Creator over a screenshot (a fee schedule, an exchange collapse headline, the BLOK app) |
| **"I tried it" walkthrough** | Product | Screen-record onboarding: Google sign-in → Garden → fund 10 USDC. Real flow only |
| **Street/desk interview** | Awareness | "Who holds your crypto?" Real answers, then the reveal |
| **Founder/BTS** | Trust, community | Team members, no script feel |
| **Duet/stitch reply** | Trend-jacking | Reply to "crypto is a scam" takes with nuance |

## 3. Deliverables (write to `content/ugc-videos/YYYY-MM-DD-<slug>/`)
Use `templates/ugc-brief.md` as the skeleton. Produce:
1. **Concept**: one line, audience, pillar, goal, platform(s), length (15/30/45/60s).
2. **5 hook variants** (first 1–3s): spoken line + on-screen text + visual action. Mix: question, contrarian, POV, pattern-interrupt, "nobody tells you".
3. **Script** as a timestamped table: `time | visual/shot | spoken (VO) | on-screen text | SFX/music`.
   Structure: Hook (0–3s) → Problem (3–8s) → Turn/insight (8–20s) → Proof/demo (20–35s) → CTA (last 3–5s).
   Spoken pace about 2.5 words/sec. One idea. Plain English. Garden metaphor ≤1.
4. **Shot list**: angle, framing, location, props, B-roll (phone screen-record of app, coffee, commute, plants 🌱).
5. **Captions**: `captions.srt` (≤ 32 chars/line, 2 lines max) + post caption + 3–5 hashtags.
6. **Creator brief** (if using a real creator): do's/don'ts, mandatory lines, banned words, disclosure (#ad / paid-partnership toggle), deliverables, usage rights.
7. **AI production prompts** (if using AI avatars/voice): avatar description, voice tone, and an explicit "AI-generated" disclosure plan. Never present an AI avatar as a real customer with a real result.
8. **Compliance check** from `brand/compliance.md` written at the bottom of the brief.

## 4. Production options
- **Real creators** (preferred for authenticity): send the creator brief.
- **AI avatar tools** (HeyGen, Synthesia, Arcads-style): use the AI prompts section; label as AI.
- **Programmatic** (faceless/motion): Remotion plugin (if installed) or ffmpeg.
- **Burn captions with ffmpeg** onto a 9:16 clip:
  ```bash
  ffmpeg -i raw.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles=captions.srt:force_style='FontName=Inter,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H002B1B0B,BorderStyle=1,Outline=2,Alignment=2,MarginV=180'" -c:a copy final.mp4
  ```

## 5. Rules
- Hook must land in under 2s with on-screen text (80%+ watch muted).
- Show the real product UI only; never mock dashboards with fake returns (label "illustrative" if conceptual).
- Risk line in caption whenever investing is discussed.
- Keep specs: 1080×1920, safe zone per `brand/visual-identity.md`.

If the Social Media Skills plugin is installed, `ugc-and-influencer`, `hook-writer`, `short-form-video-script`
and `talking-head-and-piece-to-camera` complement this skill; BLOK rules here win on conflicts.
