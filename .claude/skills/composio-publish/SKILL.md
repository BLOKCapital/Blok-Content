---
name: composio-publish
description: Publish, schedule or fetch analytics for BLOK Capital content through Composio (Instagram carousels, stories, Reels; X; and other connected apps). Use when the user asks to post, schedule, upload, cross-post, pull metrics, or connect a social account.
---

# Publish via Composio

**Follow `docs/playbook.md` sections 0 and 6 exactly.** It has the account IDs, tool slugs, the proven
GitHub-raw → Composio-sandbox → Instagram route, and the list of things that don't work. Don't rediscover.

## Rule
Post only after the user has said yes to the **final media + caption** for that specific post. Everything
before that (rendering, uploading to storage, creating containers) needs no approval.

## Steps (summary)
1. Media rendered and QA'd locally; caption final; compliance checklist passed.
2. Show the user the media + caption → wait for "yes".
3. Commit + `git push origin main`.
4. Composio: `COMPOSIO_SEARCH_TOOLS` (get `session_id`) → `COMPOSIO_REMOTE_WORKBENCH`: curl the raw GitHub
   file(s), check md5 against local, `upload_local_file()` → `s3key`(s).
5. `COMPOSIO_MULTI_EXECUTE_TOOL`:
   - Carousel: `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` (`child_image_files`, `caption`)
   - Story: `INSTAGRAM_POST_IG_USER_MEDIA` (`media_type: STORIES`, `image_file`)
   - Reel: `INSTAGRAM_POST_IG_USER_MEDIA` (`media_type: REELS`, `share_to_feed: true`, `thumb_offset`, `video_file`, `caption`)
   then `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` (`ig_user_id: 28392491727089093`, `creation_id`, `max_wait_seconds: 240` for video).
6. Verify with `INSTAGRAM_GET_IG_MEDIA`; log in `content/calendar/published.md`; update `ideas/backlog.md`; push.
7. Tell the user what the API can't do (AI label, music, alt text, link stickers) so they finish it in the app.

## Analytics
`INSTAGRAM_GET_IG_MEDIA_INSIGHTS` / `INSTAGRAM_GET_USER_INSIGHTS` for posts in `content/calendar/published.md`;
write learnings to `content/calendar/learnings.md`.
