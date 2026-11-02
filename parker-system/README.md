# parker-system (vendored for the `hooks` skill)

Installed 2 Nov 2026 at Sheetal's request, from https://github.com/real-simple-labs/parker-brain
(commit 979e09fceb913713efef4fc870aa7565388bbd39). Licence: PolyForm Noncommercial 1.0.0 (`LICENSE.md`).
Sheetal chose to install it after being told the licence bars commercial use.

What's here: the hook taxonomy (`creative-strategy-context/hooks.md`), the psychology behind it (`hook-psychology.md`),
the voice-review doctrine (`ai-writing-tells.md`, `spoken-script-voice.md`), and the two lint/grounding scripts.
The skill lives at `.claude/skills/hooks/`; its review agents at `.claude/agents/`.

## How it maps onto this repo

The skill was written for Parker's "brand brain". There is no `strategy/` or `idea-bank/` here. Use instead:
- brand voice, ICP, compliance: `CLAUDE.md`, `brand/voice.md`, `brand/compliance.md`, `knowledge/audiences.md`
- X rules: `growth/x/x-algorithm-playbook.md` and `growth/x/tweet-style-guide.md` (these win on how a tweet reads)
- scripts: `python3 parker-system/scripts/voice-lint.py <file>`
