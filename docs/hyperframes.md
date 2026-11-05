# HyperFrames skills: how video threads use them

Installed 2026-11-05 from `npx hyperframes skills update reverse-any-video` (HyperFrames CLI v0.9.15, HeyGen's
open-source HTML-to-video tool). Skills live in `.claude/skills/` so every session on this repo gets them:

| Skill | Use it for |
|---|---|
| `/hyperframes` | Read first for any HyperFrames video: build an HTML composition, render to MP4 |
| `/hyperframes-cli` | CLI commands: `init --skip-skills`, `preview`, `lint`, `render`, `transcribe` |
| `/hyperframes-registry` | Ready-made effects, transitions, caption styles, charts. Search before hand-coding one |
| `/media-use` | Music beds, sound effects, stock images, icons, logos, grading, mixing |
| `/reverse-any-video` | Rebuild an existing video as an editable project. **Needs HyperFrames Pro** |

## Rules that override the skills' defaults

1. **Voiceover stays the Chatterbox Brooks clone** (`brand/voice/brooks-chatterbox/` in the shared folder).
   Do not use HeyGen TTS / Voice Turbo or Kokoro for the voice unless Sheetal says so. Use `/media-use` for music,
   SFX and images only.
2. **Size:** HyperFrames defaults to 1920×1080. Instagram Reels are 1080×1920; X videos are 16:9. Ask which
   platform first (project rule) and set the size to match.
3. Instagram videos still end with the comment-to-get CTA; X videos never do.
4. Run the QA checklist (`growth/qa-checklist.md`) on every render as before.
5. Catalog music/SFX/images are licensed through HeyGen for use in videos. Openverse SFX need a CC BY credit in
   the caption.

## Sign-in (needed for the free music, SFX, stock images)

The catalog (10k+ tracks, SFX, 75k+ images) is free but needs a HeyGen sign-in. Cloud sessions are fresh
containers, so the sign-in does not carry over between threads. In each video thread:

```bash
npx hyperframes auth status            # check first
npx hyperframes auth login --device    # headless: prints a link + code
```

Post the link and code to Sheetal, she approves it in her browser (her HyperFrames account is her HeyGen
account), then continue. Do not sign in with an API key: that bills HeyGen API credits and has no HyperFrames plan.
Without sign-in, fall back to the bundled/Openverse SFX and our own stills, and say so.

Pro (paid) adds `/reverse-any-video` and the generative models (generated music, images, video shots, avatars).
Never spend credits without Sheetal's ok.

## Getting media into a project

```bash
npx hyperframes media-use resolve --type bgm   --intent "calm, curious piano bed, 30s" --project <dir>
npx hyperframes media-use resolve --type sfx   --intent "soft paper swoosh"            --project <dir>
npx hyperframes media-use resolve --type image --intent "1930s office workers"         --project <dir>
```

Files land in the project's `assets/` with a ledger record; renders never fetch from the network.

## Refreshing

`npx hyperframes skills update` installs into `~/.claude/skills`, which is thrown away with the container. To
refresh the repo copy: run it with `HOME` pointed at a scratch folder, then copy the five folders from
`<scratch>/.claude/skills/` over `.claude/skills/`. Check with `npx hyperframes skills check`.
