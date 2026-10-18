# Post spec: "The first fund was built for people without much money" (for the Posting calendar thread)

Not approved yet: post only after Sheetal's "yes". Pinned GitHub base (commit 2bd35f4f19d0fade6b11169b5abb7259cc752b6b, branch claude/project-thread-51sxnf):
https://raw.githubusercontent.com/BLOKCapital/Blok-Content/2bd35f4f19d0fade6b11169b5abb7259cc752b6b/content/carousels/2026-10-18-big-boys-fund/

## Instagram (proposed Mon 19 Oct 15:30 IST / 10:00 UTC), INSTAGRAM ONLY, ig_user_id 28392491727089093
1. Duplicate check: stop if a post starting "The first fund ever made was for people without much money" is up.
2. Workbench curl video/slide-01.mp4 .. slide-05.mp4, md5s in order: 563141a0fa2a9b61f7082b30e1576370 92817b90b2839bc2467fdca91a76f524
   7bdd4187573d198491e962ea2320e7e8 dbfd5e9f2fc7a500b1e4ef780c0987b7 d296370d6d7d799f9dc9276ef7907257; upload_local_file each;
   INSTAGRAM_CREATE_CAROUSEL_CONTAINER with child_video_files in slide order (one continuous panorama, order matters).
   Caption = text between <!-- IG START --> and <!-- IG END --> in caption.md at the base URL (md5 494989109a26923d09adf92742f0c9cb), exactly.
3. Story: jpg/slide-01.jpg (md5 bdb1abebf7a58362e5a16c16d0888fad) padded onto a 1080x1920 #F6F3E8 canvas at y=240, as STORIES.
4. No AI label needed (drawn in code, original music).

## X (proposed Sun 18 Oct 20:00 IST / 14:30 UTC in the freed Buttonwood slot, else next free X slot)
Text = <!-- X START -->..<!-- X END --> in caption.md; self-reply = <!-- XR START -->..<!-- XR END -->.
Video: x/pan.mp4 (md5 01832051856e093e84d2e248fe3d4064, 21 s, 1080x1440) via TWITTER_UPLOAD_LARGE_MEDIA tweet_video.
First line to dedupe on: "the first mutual fund (amsterdam, 1774)".
