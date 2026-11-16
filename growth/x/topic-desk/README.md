# X topic desk: the daily pipeline for picking what @blok_cap posts (set 15 Nov 2026)

**Problem (Sheetal, 15 Nov):** we're losing at activation. Not enough engagement, and new people don't find us.
**What the numbers say:** followers went 5,772 (21 Oct) to 5,689 (14 Nov). Our own posts land at 190 to 705 views,
mostly seen by people who already follow us. Early, substantive replies under big accounts' fresh posts got 180 to 386
views each, from people who have never seen us. The two breakouts were a stance post and an action post.
So the daily job is: **find the one conversation new people are already in, show up there first, then give them a
reason to reply to us.** Rules still come from `../x-algorithm-playbook.md`, `../tweet-style-guide.md`, the hooks skill,
`../../trend-playbook.md`, `../../qa-checklist.md` and `brand/compliance.md`. Never post without Sheetal's ok.

Page: `growth/x/topic-desk/desk.html` (open in a browser; rebuilt every morning).

## The daily run (part of the 04:43 UTC Idea Deck refresh; anyone can also run it by hand)

1. **Radar (free, ~10 seconds):** `python3 -I growth/x/topic-desk/x-topic-radar.py` (shared-folder path
   `/mnt/project-files/growth/x/topic-desk/`). Writes `data/YYYY-MM-DD.json`:
   - `hot_48h`: watchlist posts under 48h ranked by heat = (5 x replies + 5 x quotes + reposts + 0.5 x likes) per hour
   - `quote_now`: posts under 2h (quote window open), `reply_targets`: posts under 6h from 10k+ accounts with big reply sections
   - `news`: last 48h of crypto / Web3 and finance headlines (CoinDesk, The Block, Decrypt, Cointelegraph, Blockworks,
     The Defiant, DL News, Unchained, Bankless, FT Markets, plus Google News searches for tokenized funds, fund access,
     Arbitrum and on-chain finance). `ours` marks headlines on our themes; price and hack headlines are marked unsafe.
   - `hacker_news`, `google_trends` (US, IN, GB): what the wider internet is talking about
   - `own_posts`: likes and replies on our posts listed in `posted.json` (the feedback loop)
   - `source_health`: which accounts' feeds are fresh. Some accounts' public widget feeds are stuck weeks old; the
     script skips those for 7 days and re-checks. The feed rate-limits at ~30 calls per 15 minutes, so the script stops at 28.
2. **Paid radar (only when X API credit exists):** `growth/trends/trend-radar.py` via Composio. Adds views, bookmarks,
   keyword lanes and personal accounts whose widget feed is stale. If it says "credits depleted", carry on without it.
3. **One WebSearch** for the day's biggest money / AI / culture story, to get a primary source for numbers.
4. **Score the top ~8 candidates, 1 to 5 each** (the trend playbook's four plus one for activation):
   | | 1 | 5 |
   |---|---|---|
   | Heat | old, quiet | under 6h, big reply section, still climbing |
   | Bridge | three jumps to reach us | one sentence to access / $10 fund / owning your fund / receipts |
   | Take | we'd repeat the news | an angle nobody in the replies has |
   | Safety | price, politics, tragedy, named person or competitor | a number or an idea |
   | **Talk** | people would just like it | people would reply with their own answer, argue, or send it to a friend |
   Keep 18+ of 25 with Safety 4+. Safety under 4 is an automatic skip.
5. **Attach fresh news to every pick (Sheetal, 15 Nov):** each pick names 1 to 3 headlines from the last few days
   (`news_hooks`) and the post or its first reply mentions one, so people can see we follow what's happening. Open the
   primary source and check its date: Google News sometimes re-surfaces old stories (on 15 Nov it served a June
   BlackRock story as new). Skim the top crypto and finance headlines even when the pick comes from elsewhere.
6. **Pick one topic of the day + two backups**, and plan four shots from the topic of the day:
   - **A. Quote post** of the freshest big post on it (under 2h is best, never over 48h). The x.com link at the end of
     the text registers as a quote (the API refuses `quote_tweet_id`). Must carry BLOK's own context (Sheetal, 31 Oct).
   - **B. Original post** (stance, history rhyme, number post or question post), in a fixed slot (06:00, 12:15 or 14:30 UTC).
   - **C. 10 to 15 reply drafts** under fresh big posts in the same conversation (from `reply_targets` + hand check),
     each with a number, a counter-example or a real question. Hand-posted, because the API only replies to mentions.
   - **D. Community hook**: the day's question for our own replies (the forced choice B ends on), answered by us for
     2 hours after posting, mutuals first (+15 bonus).
7. **Write `data/YYYY-MM-DD-picks.json`** (shape below), then build the page:
   `python3 -I growth/x/topic-desk/build-desk.py`. It writes `desk.html` (today) and `archive/YYYY-MM-DD.html`.
8. **Before anything goes to Sheetal:** run the QA checklist, the hooks skill gates, the style guide (lowercase,
   conversational, no quotation marks, ends in a reason to reply), compliance (no price, no returns, risk line in the
   first reply when investing comes up, USD only). Hot takes are marked for her.
9. **After posting:** add every post's URL to `posted.json` (`url`, `date`, `topic`, `lane`, `format`, `type`:
   stance / history / number / question / action / quote / reply). The next morning's radar pulls its likes and replies.
   Weekly, compare replies per post by `type` and `lane` on the desk page and lean the next week's picks toward what won.

## Format experiment and closing-line rule (Sheetal, 16 Nov 2026)
- **Don't end every post on the same pitch.** The line "we're building blok so your own fund, from $10..." went out on
  almost every post and reads like an ad. Keep BLOK's context, but put the product line in the **first reply** on most
  days; at most 2 posts a week carry it in the post itself, and never with the same wording twice in a week.
- **One format a day for 7 days** on the same kind of topic and the same slot, so only the format changes: greentext,
  translation joke, plain question, real headline screenshot as the image, 3-post thread, 10 to 15s meme video, ladder.
  Log each in `posted.json` with `format`; after 24h compare replies per post on the desk page and keep the winners.
  Also append each experiment post (by tweet id, never rewriting other entries) to
  `/mnt/project-files/growth/dashboard/x-posts.json` with `experiment: "x-format-7day"`, `format`, `topic`, `posted_at`,
  first line as `text`, and at 24h fill `metrics` (views, likes, replies, reposts, quotes, bookmarks, profile_clicks,
  link_clicks, follows, checked_at, hours_after_post; null where unknown, by hand from X analytics while the API is out).
  Then run `python3 /mnt/project-files/growth/dashboard/build.py`.
- Every day's picks offer the topic in **2 to 3 different formats**, not one draft.

## Picks file shape (`data/YYYY-MM-DD-picks.json`)
```json
{
  "date": "2026-11-15",
  "topic_of_day": "one line",
  "why": "why this one beats the others, one or two sentences",
  "picks": [
    {"rank": 1, "title": "...", "lane": "...", "trend_url": "...", "source_url": "...", "heat_note": "HN 1,420 pts, 8h",
     "scores": {"heat": 5, "bridge": 4, "take": 4, "safety": 5, "talk": 4},
     "bridge": "one sentence", "remix": "history rhyme", "temp": "spicy",
     "quote": {"target_url": "...", "target_note": "...", "draft": "..."},
     "original": {"slot": "12:15 UTC", "hook_type": "...", "draft": "...", "first_reply": "..."},
     "news_hooks": [{"title": "...", "source": "CoinDesk", "date": "2026-11-14", "url": "..."}],
     "flags": ["..."]}
  ],
  "reply_targets": [{"url": "...", "handle": "...", "note": "...", "draft": "..."}],
  "skipped": [{"what": "...", "why": "..."}],
  "needs_credit": ["what we could not check today without X API credit"]
}
```

## What still needs X API credit (Developer Portal, billing)
- Views and bookmarks (the widget feed has likes, replies, reposts, quotes only)
- Keyword search across all of X (who is talking about minimums, index funds, tokenization right now)
- Personal accounts whose widget feed is stale (most commentators: @nic_carter, @morganhousel, @EricBalchunas...)
- Mentions, auto-replies on our own posts, and follower lists (the engagement sweep and reply desk)
