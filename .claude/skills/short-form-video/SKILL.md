---
name: short-form-video
description: Write faceless / explainer / motion-graphics short-form videos (Reels, TikTok, YouTube Shorts) for BLOK Capital, including scripts, storyboards, voiceover, on-screen text, b-roll lists, and render plans (Remotion/ffmpeg). Use when the video is not creator/UGC-led.
---

# Short-form video (non-UGC)

1. Load `blok-brand` context.
0. **Instagram/Reels:** follow `brand/instagram-strategy.md` (fund/ETF investors, educational, no crypto vocabulary or visuals). It overrides the rest.
2. Folder: `content/short-form/YYYY-MM-DD-<slug>/`.
3. Write:
   - **Storyboard table**: `# | duration | visual (motion/b-roll/screen-record) | VO | on-screen text`.
   - **VO script** (≈2.5 words/sec; 20–45s total).
   - **Design notes** using brand colours (linen bg, indigo headlines, lime growth accents, coral once).
   - **Captions SRT** + post caption + hashtags.
4. Good formats: "X explained with a garden" · animated compare (TradFi vs Garden) · kinetic-type myth-busts ·
   app screen-record walkthrough · "1 term a day" glossary series (`knowledge/glossary.md`).
5. Render: Remotion plugin (preferred if installed) or carousel PNGs → ffmpeg slideshow:
   ```bash
   ffmpeg -framerate 1/3 -pattern_type glob -i 'export/slide-*.png' -vf "scale=1080:1350,pad=1080:1920:0:285:color=0xF6F3E8,format=yuv420p" -r 30 out.mp4
   ```
6. Compliance check from `brand/compliance.md`.
