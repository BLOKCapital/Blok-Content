# Video Reference Library: guide for threads

The library lives in the shared folder at `growth/video-references/`
(`/mnt/project-files/growth/video-references/`). The tool lives in the repo at
`scripts/video-refs/vref.py`. Open `library.html` to browse everything.

**Reference only.** We study how other creators' videos work, then build our own from scratch.
Never reupload, remix, or cut any clip, frame, track or voice from this library into a BLOK video.

## What each entry holds

`entries/<id>/`
- `sheet.jpg`: contact sheet, one numbered frame per shot (frame numbers are what you tag)
- `hook.jpg`: the first 3 seconds, frame by frame
- `transitions.jpg`: the frame just before and just after each of the first 8 cuts
- `waveform.jpg`: audio waveform with red lines at every cut (shows beat-synced editing)
- `preview.mp4`: 640p study copy, reference only
- `meta.json`: source link, creator, caption, length, cuts, cuts per minute, average shot length,
  loudness, words per minute, transcript, and the category tags with notes

`categories/<name>/README.md` lists every reference tagged in that category, with the note and the
tagged frames copied next to it. Categories: hooks, storytelling, subtitles, graphics-motion,
transitions, music-sound, pacing-editing, visual-style, cta-endings, formats
(`python3 scripts/video-refs/vref.py categories` prints what to look for in each).

## One-time setup in a new container

```bash
bash scripts/video-refs/setup.sh   # yt-dlp, sherpa-onnx, the local whisper model (~375 MB, free)
```
Transcripts are skipped quietly if the model is missing; everything else still works.

## Adding links Sheetal sends

1. Paste each link into `growth/video-references/inbox.md` so nothing is lost.
2. Get the video, trying these in order:
   - **A. Straight from the link (cloud):** `python3 scripts/video-refs/vref.py add <url>`.
     Works for many sites. Instagram usually blocks cloud machines (HTTP 429), so expect B or C for reels.
   - **B. Sheetal's Mac (best for Instagram):** with her computer linked to the thread and folder access
     to a folder such as `~/Downloads/blok-refs`, run on the device:
     `yt-dlp --cookies-from-browser chrome -o "~/Downloads/blok-refs/%(id)s.%(ext)s" <url>`
     (needs `brew install yt-dlp` once; use the browser she is signed in to Instagram with).
     Then pull the file into the container with `device_stage_files` and run
     `vref.py add <staged file> --url <url>`.
   - **C. She uploads the file:** she saves or screen-records the reel and drops it in the thread.
     Uploads land in `/mnt/project-files/uploads/hearth/`. Run `vref.py add <that file> --url <url>`.
   Add `--creator <handle>` when the creator is not in the link.
3. Look at `sheet.jpg`, `hook.jpg`, `transitions.jpg` and `waveform.jpg` (Read them as images), and read the
   transcript in `meta.json`.
4. Tag every category where the video teaches something, with a short, specific note and the frame numbers
   that show it:
   ```bash
   V="python3 scripts/video-refs/vref.py"
   $V tag <id> subtitles --note "Two-word chunks, yellow active word, centred at 60% height, pops in on the beat" --frames 3,4
   $V tag <id> hooks --note "Opens on the answer, then rewinds: 'This cost him $40M. Here's how.'" --frames 1 --t 0-1.5s
   $V why <id> "Every 2s something new appears, and the question at 0:01 is only answered at 0:28."
   ```
   Good notes say *what* and *why it works* so someone can rebuild the idea without seeing the clip:
   sizes, positions, colours, timing, what changes on each beat. Avoid "nice captions".
5. Remove the link from `inbox.md`. `library.html` and the category folders rebuild on every add and tag.
   Run `vref.py rebuild` if you edit `meta.json` by hand.

`<id>` can be any unique part of the entry name (for example the reel code).

## Looking up references when building a video

```bash
V="python3 scripts/video-refs/vref.py"
$V lookup subtitles                 # every subtitle reference with notes and frame paths
$V lookup hooks --q question        # hooks whose notes or transcript mention "question"
$V lookup --q chart                 # any category
$V list                             # everything, with tags
```
Open the frame paths it prints to see the exact look. Before building a motion-graphics or storytelling
video, pull 2 to 3 references per relevant category, say in the reply which ones shaped the video, and
translate each into BLOK's own palette, fonts and voice (brand/visual-identity.md, brand/reel-style.md).

## Rules
- Reference only; never reupload or reuse other creators' clips, music or voices.
- Keep notes factual and specific. No guesses about view counts that the source did not give.
- Don't commit the library to the repo; it lives in the shared folder. Commit tool changes only.
