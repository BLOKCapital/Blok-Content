---
name: video-references
description: Add reference videos (Instagram reels and other links Sheetal sends) to the video reference library, or look up references (hooks, subtitles, motion graphics, transitions, music, storytelling) before building any video.
---

# Video reference library

Read and follow `scripts/video-refs/GUIDE.md`.

- **Adding links:** `python3 scripts/video-refs/vref.py add <url-or-file> [--url URL]`, look at the
  contact sheet, hook strip, transitions strip and waveform, then tag each category with a specific note
  and frame numbers (`vref.py tag <id> <category> --note "..." --frames 2,5`).
- **Building a video:** before scripting or animating, run `vref.py lookup <category>` for the categories
  that matter (hooks, storytelling, subtitles, graphics-motion, transitions, music-sound), view the frames,
  and say in the reply which references shaped the video.
- Library: `/mnt/project-files/growth/video-references/` (browse `library.html`).
- Reference only: never reupload or reuse other creators' clips, music or voices.
