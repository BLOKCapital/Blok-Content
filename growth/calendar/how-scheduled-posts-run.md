# How the calendar's scheduled posts run

Calendar page: https://claude.ai/artifact/9CxBF6kZquPmWFMEhhCvNr (shared db collection `posts`, one doc per slot; doc ids are in posts.json).
Each post has a one-shot scheduled task that wakes the "Content calendar" thread at the slot time. On wake:

## X post (text from growth/calendar/x-copy.md, block Xn)
1. Duplicate check: TWITTER_RECENT_SEARCH `from:blok_cap -is:reply -is:retweet`, max 10. Stop (mark the doc "posted" with the existing link) if the post's first line is already up.
2. Text = the block between `<!-- Xn START -->` and `<!-- Xn END -->`, exactly. Reply = the `Xn REPLY` block, if there is one.
3. Media, if the task names a URL: in COMPOSIO_REMOTE_WORKBENCH curl it, check the md5, upload_local_file; then TWITTER_UPLOAD_MEDIA (image) or TWITTER_UPLOAD_LARGE_MEDIA (video, tweet_video, poll until succeeded).
4. TWITTER_CREATION_OF_A_POST (text + media id). Then the reply with reply_in_reply_to_tweet_id = the new post id.
5. Log: ArtifactData get then update the calendar doc (status "posted", link). Add a row to growth/x/tracker.md.
6. No thread reply on success (update the thread status only). On failure: retry once, then reply in the thread saying exactly what failed, and set the doc status to "needs-asset" with a note.

## Instagram post
Same shape: duplicate check with INSTAGRAM_GET_IG_USER_MEDIA (limit 5), publish with the files and caption the task names, cover as a Story,
then update the calendar doc and content/calendar/published.md. Remind Sheetal (one line, in the success status) to switch on the AI label in the app when the piece is AI video.

## Daily check (20:15 IST, 16 to 31 Oct)
- Pull the last 24h of posts from Instagram (INSTAGRAM_GET_IG_USER_MEDIA) and X (TWITTER_RECENT_SEARCH) and mark matching calendar docs "posted" with their links,
  including posts other threads' tasks made. A slot that passed with nothing live becomes "missed" in its note (keep status, add the note).
- On trial days (16, 18, 20, 22, 24, 26, 28 Oct) reply in the thread to Sheetal: which variant to post now as a Trial, its file and caption
  (content/2026-10-15-trial-reels-keynes/README.md), and ask for the previous trial's 24h views and skip rate (or to type them into the calendar row).
- On 30 Oct, once the trial numbers are in, pick the winner (lowest skip rate; tiebreak average watch time, then shares + saves per 1,000 views) and schedule it as a normal Reel.
