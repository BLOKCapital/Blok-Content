---
name: instagram-reel
description: Make a finished Instagram Reel end to end with no filming and no paid tools: conversational script, human-sounding AI voiceover (Andrew), animated on-brand scenes with word-synced captions, rendered to MP4 and ready to post. Use whenever the user asks for a reel, short video, UGC-style video, or explainer video.
---

# Instagram Reel (AI voiceover + motion graphics)

**Follow `docs/playbook.md` section 5 step by step** (then section 6 to publish). Template and helpers:
`templates/reel/scene.html` (+ README), `scripts/sandbox/voiceover.py`, `scripts/build-timeline.py`,
`scripts/render-reel.mjs`. Worked example: `content/ugc-videos/2026-10-09-sell-your-fund-on-a-saturday/`.

Checklist:
1. Read `brand/instagram-strategy.md` (audience, no-crypto rule) and pick one idea from `ideas/backlog.md`.
2. Write `brief.md` (concept, hooks, script, caption, compliance) and `build/script.txt` (one beat per line,
   conversational, 25–35s).
3. Voice: push `script.txt`, generate in the Composio sandbox with Andrew, download `vo.m4a` + `vo.json`.
4. `build-timeline.py` → `timeline.js`; adapt `scene.html`; preview key frames; render; QA frames from the MP4.
5. Send the MP4 + caption to the user. On "yes", publish (section 6), log it, and remind them about the AI label.
