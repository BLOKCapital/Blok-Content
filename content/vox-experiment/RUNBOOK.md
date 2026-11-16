# Vox reel experiment · daily runbook (Tue 17 to Sun 22 Nov 2026)

Sheetal, 16 Nov 2026: "every day you will create two videos like this, post it on Instagram, read from its analytics,
and try to change the hook, the storyline, the CTA. Run this experiment for a week." Then, 16 Nov 20:42 UTC: "Yes, run the experiment till this Sunday." (22 Nov, 12 reels) By the end of the week, tell me
which hook and which style worked the best." She approved the Bellamy demo as "perfect", so its look is the locked
baseline (`../2026-11-16-vox-demo-bellamy-card/BRIEF.md`). Her ask is the go-ahead to post these 12 reels
automatically once they pass QA. If she says hold or stop, stop posting.

Files: `plan.md` (test matrix, slots, seeds), `log.md` (one row per reel + insights), `kit/` (build scripts).

## Every morning run (07:17 IST)
1. **Analytics first.** Composio `COMPOSIO_SEARCH_TOOLS` (new session id), then `INSTAGRAM_GET_IG_USER_MEDIA`
   (ig_user_id `me`, limit 30, fields `id,caption,permalink,timestamp,media_product_type,like_count,comments_count,
   insights.metric(views,reach,saved,shares,total_interactions,ig_reels_avg_watch_time)`). For every experiment reel in
   `log.md`, fill its 24h columns (first run after it is 24h old) and its 72h columns. Count FUND comments with
   `INSTAGRAM_GET_IG_MEDIA_COMMENTS`. Watch-through = avg watch time / reel length. Record followers
   (`INSTAGRAM_GET_USER_INFO`) once a day in `log.md`.
2. **Score** each reel (see plan.md, "Scoring") and write a 3-line "what we learned so far" under today's date in `log.md`.
   On day 4 and day 6 lock the winner of the previous stage in plan.md before choosing the next variants.
3. **Pick today's 2 reels** from plan.md: variants for slot A and slot B, each with a new topic.
   Topic rules: a surprising, real, sourced historical fact or prediction tied to today's money, investing or owning a fund.
   Lead with access and low minimums (BLOK: anyone can start their own fund from $10). Never attack 1% fees. US dollars only.
   No crypto words or visuals on Instagram. No real person's face (names as text only). Not a repeat of anything in
   `/mnt/project-files/content/` (ls it). Check one primary or reputable source for every claim; drop a topic you can't source.
4. **Build each reel** in `/mnt/project-files/content/2026-11-DD-vox-<slug>/` (work in a local scratch copy, then copy in):
   - Copy `kit/` into `build/`. `BRIEF.md` = story, sources table, variant ids (hook / story / CTA), length target 25 to 35 s.
   - `build/lines.json` (show/say/gap). Last lines = the CTA variant (comment-to-get is required on Instagram; keyword
     stays FUND, DM = the 7 private-banker questions lead magnet).
   - Voice: `bash /mnt/project-files/brand/voice/brooks-chatterbox/setup.sh` if `~/.cache/blok-voice/cb` is missing;
     `pip install faster-whisper` in that venv. Then `gen_all.py`, `score_fw.py`, `assemble_fw.py` (see the Brooks README).
     Re-generate any line under 0.9 match that is a real mis-read.
   - Music: `make_bed.py music-bed.wav <dur> <drop_at> <lift_at>`; edit `mix.py` event list for this story's drops,
     make 3 mixes (0.55 / 0.38 / 0.26) and use 0.38 unless the voice is masked.
   - Scenes: write `scene.html` from `kit/scene-reference-bellamy.html` (keep every helper: cut, tornRect, tape, label,
     stamp, highlighter, dropY, jit, captions, paper, grain). 6 layers per scene, 12 fps stop-motion, drops one at a time,
     real public-domain archival scans (archive.org, Wikimedia Commons, Library of Congress) with a highlighter moment on
     the actual source where possible. Hook on screen from frame 0. Captions inside y 220 to 1540.
   - Draft render first (`node render.cjs mix.m4a ../<slug>-v1-draft.mp4 draft`), check a contact sheet, fix, then
     final `../<slug>-v2.mp4`. Never overwrite a version.
5. **QA** (`growth/qa-checklist.md`): `qa_speech.py` on the final mp4 (all lines OK), loudness -14 to -16 LUFS,
   contact sheet at 2 fps, caption with sources, risk line, "AI-generated voiceover", no crypto words, ≤ 2,200 chars.
   Write `qa-summary.md`. A reel that fails QA is not posted; post the other and log why.
6. **Schedule.** Copy final mp4 + caption.md into the repo (`content/2026-11-DD-vox-<slug>/`), commit and push to branch
   `claude/project-thread-yd20h2`, check raw.githubusercontent serves the same md5. Then create two one-shot scheduled
   tasks (bound to this thread) at 14:30 and 20:30 IST that post with the playbook section 6 route
   (`INSTAGRAM_POST_IG_USER_MEDIA` REELS, share_to_feed, thumb_offset; then `..._MEDIA_PUBLISH`; duplicate check first;
   verify with `INSTAGRAM_GET_IG_MEDIA`), then add the row to `log.md` and `content/calendar/published.md`.
   Keep 4 h between any two reels (check other scheduled posts that day).
7. **Tell Sheetal** in the thread in under 80 words: today's two variants, yesterday's leader, anything that broke.
   She has to turn on the AI info label in the Instagram app for each reel; remind her once a day.

## Final report (Mon 23 Nov, 21:17 IST)
Pull 24h/72h insights for all 12 reels, rank them, and deliver an interactive HTML report in the shared folder
(`growth/analytics/2026-11-23-vox-experiment-report.html`, inline charts, simple words) that names the winning hook,
storyline, CTA and the recommended locked format, with honest caveats (topic differences, small sample).
