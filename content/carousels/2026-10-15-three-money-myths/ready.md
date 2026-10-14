# 3 money myths: final files (approved for Thu 15 Oct)

Sheetal approved this post for 6:52 PM IST (13:22 UTC) on 15 Oct. The slides are final: don't rewrite or redesign anything.
Reviewed render (14 Oct, 23:14 UTC): 5 video slides, 1080x1440, 6s each with music, plus `full.mp4` (30s) for X.

## Build the files (mechanical, about 2 minutes, Composio workbench)
```
B=https://raw.githubusercontent.com/BLOKCapital/Blok-Content/9c9d7bdef672d27b80ef70e8a28f6a7a8fb783ae/content/carousels/2026-10-15-three-money-myths
mkdir -p /home/user/myths/ov && cd /home/user/myths
for f in composite.sh fetch-photos.sh music.m4a; do curl -sfL $B/$f -o $f; done
for i in 1 2 3 4 5; do curl -sfL $B/overlays/o$i.png -o ov/o$i.png; done
md5sum music.m4a ov/*   # a57ddb0f9cb0837915bb8f5c8d787481, o1 a4a8b440848e18be16f49100e45da909, o2 e8a69fee455d2c81bfb6fdeee3522249, o3 3e6e450ae532d2ae0277498a2091526d, o4 f957e2ad29743bc8f9f68450907f78d2, o5 a23f4d57fca51ab2b71f7c2eaf9eb555
bash fetch-photos.sh ph && nohup bash composite.sh ph ov music.m4a out > log.txt 2>&1 &
```
Poll `log.txt` until "full cut done". Check `out/slide-0N.jpg` stills look like `reference-sheet.jpg` (same photos, same text). Then `upload_local_file` each of out/slide-01..05.mp4, out/full.mp4 and out/slide-01.jpg → s3keys, and write them in the table below and in the Thu 15 row of /mnt/project-files/growth/instagram-100-plan.md (status READY).

## Post
- **Instagram, 13:22 UTC (IG growth daily task):** INSTAGRAM_CREATE_CAROUSEL_CONTAINER, ig_user_id 28392491727089093, child_video_files = slide-01..05.mp4 in order (video/mp4), caption = `caption.md` text under "## Instagram" up to "## X", exactly. Publish with INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH (max_wait_seconds 240). Then slide-01.jpg as a Story.
- **X, 06:00 UTC:** full.mp4 + the text under "## X (attach full.mp4)" in `caption.md`.

## s3keys (filled in after the build)
| File | s3key |
|---|---|
