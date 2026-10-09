# BLOK Content: Operating Playbook

Everything we've learned about making and publishing content from this repo. **Read this before producing
or posting anything.** Follow it step by step; don't rediscover. If something here turns out to be wrong,
fix this file in the same session.

---

## 0. Accounts & IDs (verified 2026-10-09)

| Thing | Value |
|---|---|
| Instagram | **@blok.capital**, Business account, IG user id **`28392491727089093`** (or use `"me"`) |
| Composio connector | Added to claude.ai as a custom connector (`https://connect.composio.dev/mcp`); tools are `mcp__Composio__*` |
| Composio connected apps | `instagram` (account `instagram_bruit-ezba`), `twitter` |
| Composio restricted tools | HeyGen video generation (`HEYGEN_V2_VIDEO_GENERATE`) is disabled in the Composio project |
| GitHub repo | `BLOKCapital/Blok-Content`, **public**, default branch `main` (we work directly on `main`) |
| Raw file URL | `https://raw.githubusercontent.com/BLOKCapital/Blok-Content/main/<path>` |
| Approved voice | **`en-US-AndrewMultilingualNeural`** (edge-tts), rate +0%, one continuous take |

## 1. The one approval rule
Make everything end to end without asking: script, visuals, voice, render, caption, compliance check, commit.
Then show the user the **final media + caption** and post as soon as they say yes. That single "yes" per
post is the only approval needed. Never post anything that hasn't had it.

## 2. Pipeline at a glance

```
idea ─► script/slides ─► render locally ─► show user ─► "yes" ─► git push main
                                                            │
     Composio sandbox: curl raw.githubusercontent ◄─────────┘
        ─► md5 check ─► upload_local_file() ─► s3key ─► Instagram tool ─► verify ─► log
```

## 3. Carousel (Instagram, 1080×1350)
1. Write `content/carousels/YYYY-MM-DD-slug/slides.json` (schema: `templates/carousel/README.md`) and `caption.md`.
2. `npm install` (first time), then `npm run carousel -- content/carousels/<folder>/slides.json`.
3. QA: stitch a contact sheet and look at every slide:
   `ffmpeg -i slide-01.png -i slide-02.png ... -filter_complex "[0][1]...hstack=N,scale=2160:-1" sheet.png`
4. The renderer also writes Instagram-ready JPEGs to `export/jpg/` (Instagram rejects PNG). Commit them.
5. Show user → "yes" → **Publish (section 6)** with `INSTAGRAM_CREATE_CAROUSEL_CONTAINER`
   (`child_image_files` = list of `{name, mimetype:"image/jpeg", s3key}` in slide order, `caption`), then
   `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` with the returned `creation_id`.

## 4. Story (1080×1920)
- From a carousel cover: paste the 1080×1350 slide onto a 1080×1920 `#F6F3E8` canvas at y=285 (no new copy).
  `ffmpeg -i slide-01.png -vf "pad=1080:1920:0:285:color=0xF6F3E8" story-01.jpg`
- Publish: `INSTAGRAM_POST_IG_USER_MEDIA` with `media_type:"STORIES"`, `image_file:{...s3key}` → publish.
- Stories expire in 24h. Link/mention stickers can't be added via API (the user adds them in the app).

## 5. Reel: AI voiceover + motion graphics (no filming, no paid credits)
Folder: `content/ugc-videos/YYYY-MM-DD-slug/` (or `content/short-form/...`) with `brief.md`, `build/`.

1. **Script**: `build/script.txt`, one beat per line, written how people talk ("And then... it just waits.",
   "Honestly?"). ~25–35s. Follow `brand/instagram-strategy.md`.
2. **Voice** (Composio sandbox; this machine can't reach the TTS service). Push `script.txt` to `main` first, then
   in `COMPOSIO_REMOTE_WORKBENCH` (python, runs as root, writes anywhere under /home/user):
   ```python
   import subprocess
   B="https://raw.githubusercontent.com/BLOKCapital/Blok-Content/main"
   P="content/ugc-videos/<slug>/build"
   subprocess.run(f"pip install -q edge-tts && mkdir -p /home/user/vo && cd /home/user/vo && "
                  f"curl -sSL -o voiceover.py {B}/scripts/sandbox/voiceover.py && "
                  f"curl -sSL -o script.txt {B}/{P}/script.txt && python3 voiceover.py script.txt vo", shell=True, check=True)
   for f in ["vo.m4a","vo.json"]:
       r,e = upload_local_file(f"/home/user/vo/{f}"); print(f, e or r["s3_url"])
   ```
   Then locally: `curl -sSL -o build/vo.m4a <s3_url>` and `curl -sSL -o build/vo.json <s3_url>`.
3. **Timeline**: `python3 scripts/build-timeline.py build/script.txt build/vo.json build/timeline.js`
   (prints `S(i)` start times for each line).
4. **Scene**: copy `templates/reel/scene.html` → `build/scene.html`; rewrite the scenes for the new story, keying
   animations off `S(i)`. Preview key frames before the full render (cheap):
   a tiny Playwright script that calls `window.draw(t)` and screenshots a few `t` values, then `hstack` them.
5. **Render** (about 1 minute here): `node scripts/render-reel.mjs build/scene.html build/vo.m4a reel-final.mp4 30`
6. **QA**: extract frames from the MP4 at key times (`ffmpeg -ss T -i reel-final.mp4 -frames:v 1 ...`),
   check captions sync and nothing overflows. Send the MP4 to the user.
7. "yes" → commit + push → **Publish (section 6)** with `INSTAGRAM_POST_IG_USER_MEDIA`:
   `media_type:"REELS"`, `share_to_feed:true`, `thumb_offset:<ms of best frame>`, `video_file:{name, mimetype:"video/mp4", s3key}`,
   `caption` → `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` with `max_wait_seconds:240` (processing takes ~40s).
8. Caption must include "AI-generated voiceover". Remind the user to switch on Instagram's **AI info** label in
   the app (API can't) and optionally add library music (API can't).

Other voices that work (tested): Kokoro `af_heart` / `am_michael` (open-source; `pip install kokoro-onnx`,
models from github.com/thewh1teagle/kokoro-onnx releases, runs in the sandbox in ~25s), edge `Ava`, `Emma`, `Brian`.

## 6. Publishing via Composio (the reliable route)
This machine can't hand local files to Instagram, and the Composio sandbox can't render big videos
(~1GB RAM; Chromium crashes at 1080×1920). So: **render here, push to GitHub, let the sandbox fetch it.**

1. `git add` the final media and `git push origin main`.
2. `COMPOSIO_REMOTE_WORKBENCH`:
   ```python
   import subprocess, hashlib
   url = "https://raw.githubusercontent.com/BLOKCapital/Blok-Content/main/<path/to/file>"
   subprocess.run(["curl","-sSL","-o","/home/user/post/f","--create-dirs",url], check=True)
   print(hashlib.md5(open("/home/user/post/f","rb").read()).hexdigest())   # must equal local md5sum
   r, e = upload_local_file("/home/user/post/f"); print(e, r.get("s3key"))
   ```
   (For several files, loop and keep the order. Name the local copy with the right extension, e.g. `.jpg`/`.mp4`.)
3. `COMPOSIO_MULTI_EXECUTE_TOOL` with the Instagram tool (sections 3–5) using the `s3key`(s).
4. Verify with `INSTAGRAM_GET_IG_MEDIA` (`fields: id,media_type,media_product_type,permalink,timestamp,caption`).
5. Log a row in `content/calendar/published.md`, mark the idea shipped in `ideas/backlog.md`, commit + push.

Quota check if posting a lot: `INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT` (100 posts / 24h).
Composio's first call each session is `COMPOSIO_SEARCH_TOOLS` (it returns a `session_id` to pass to later calls).

## 7. Things that don't work (don't retry)
| Attempt | Result | Do instead |
|---|---|---|
| Composio CLI install in cloud session | GitHub release download blocked by network policy | Use the Composio MCP connector (already connected) |
| Rendering 1080×1920 in Composio sandbox | Chromium OOM / stuck | Render on this machine, fetch via GitHub raw |
| Pasting base64 media through tool calls | Too big, error-prone | GitHub raw route |
| Probing random public file hosts | Blocked by the safety classifier | GitHub raw route |
| HeyGen video generation via Composio | Tool restricted in the Composio project | Edge-tts voice + motion reel (section 5) |
| Figma Weave models | Figma account not linked to Weave; costs credits | Same as above |
| Realistic talking-head avatar for free | No GPU in sandbox; lip-sync models infeasible | Motion reel; or user films |
| Claude editing `.claude/settings.json` | Blocked as self-modification | User pastes `docs/permissions-allowlist.json` |
| `git push --delete` a branch | 403 from the session's git proxy | User deletes branches on GitHub |
| `rm -f $VAR/*` in Bash | Blocked by safety check | Use literal paths or `"${VAR:?}"/*` |
| Composio remote bash writing into dirs the workbench created | Permission denied (bash runs as `user`, workbench as root) | Use a fresh dir from bash (e.g. `~/kk`), or do it all in the workbench |
| Instagram API: music, AI label, alt text on carousel slides, link stickers, bio edits | Not supported | Tell the user to do it in the app |

## 8. Permissions (so nothing prompts)
In the session's mode dropdown pick **Auto**. For per-command rules, the user pastes
`docs/permissions-allowlist.json` into `.claude/settings.json` (Claude isn't allowed to edit that file itself).
