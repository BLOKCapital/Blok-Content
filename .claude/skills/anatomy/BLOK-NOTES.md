# Anatomy skill in this repo

Installed 2026-10-14 from https://github.com/wheresryan22/anatomy (commit e6600ff, MIT). Zero dependencies;
its scripts only talk to a local headless Chrome. `scripts/publish.mjs` pushes to the author's public gallery:
never run it without Sheetal's explicit OK.

Trimmed to keep the repo light: the heavy examples (raptor-engine, turning-dial, arcade-cabinet, ripple-tank)
and `.github/` were left out, so SKILL.md mentions examples that aren't here. The full copy is one
`git clone` away.

BLOK use: `content/carousels/2026-10-14-anatomy-of-blockchain/` (figure/build.mjs builds the interactive
figure with brand tokens; slides/render.mjs turns it into 1080x1440 video slides with music).
In Chromium here use CHROME_PATH=/opt/pw-browsers/chromium for scripts/lines.mjs.
