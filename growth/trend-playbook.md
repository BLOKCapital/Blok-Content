# Trend playbook: how every post gets picked (Oct 2026)

**Every new post starts here.** Before choosing a topic for any X post, Instagram Reel, carousel or video,
run the trend check below and write down the trend the post rides (or why it's an evergreen exception).
Then write it with `growth/x/x-algorithm-playbook.md` + `growth/x/tweet-style-guide.md` (X) or
`brand/instagram-strategy.md` (Instagram), and check `brand/compliance.md`.

Set by Sheetal on 24 Oct 2026: our posts are educational and well made, but none has gone viral, because we
pick our own topics. Viral posts ride attention that already exists. From now on we pick from what's hot
and say it our way.

## Why (what our numbers already say)

- Educational X posts land at **350 to 660 views** however they're made. The only breakouts were a stance post
  (greentext, 1,057) and an action post (waitlist launch, 4,969, 9 quotes). (`growth/analytics/2026-10-20-analytics-review.md`)
- Our best replies (180 to 386 views) were early replies under big accounts' **fresh** posts: borrowed attention works.
- X decides a post in its **first 2 hours** and drops it after 48. A trend gives us an audience that's already
  looking for posts on that topic during exactly that window.

## The daily trend check (15 minutes, or automatic)

The Idea Deck refresh routine runs this every morning (04:43 UTC) and writes the board to
`growth/trends/YYYY-MM-DD.md` in the shared folder. Anyone making a post later that day reads today's board first;
if it's older than ~6 hours for an X post, re-run step 1.

### 1. X radar (main source, free, verified 24 Oct)
Run `scripts/sandbox/trend-radar.py` (shared-folder copy: `/mnt/project-files/growth/trends/trend-radar.py`) inside
`COMPOSIO_REMOTE_WORKBENCH` (paste the file as `code_to_execute`; it uses
the connected @blok_cap X account through `TWITTER_RECENT_SEARCH`). It prints the hottest posts of the last 24h per
lane, ranked by **heat** = (5×quotes + 5×replies + 3×bookmarks + reposts + 0.5×likes) per hour of age, which mirrors
how X scores posts.

Lanes and watchlist (edit the script to add accounts that keep showing up):
| Lane | Watchlist (examples) | Why it's ours |
|---|---|---|
| Markets + macro | @unusual_whales, @KobeissiLetter, @WatcherGuru, @charliebilello, @TheStalwart | The day's money headline; huge reply counts |
| Personal finance | @morganhousel, @awealthofcs, @BrianFeroldi, @Ritholtz | Our IG audience's language (funds, saving, patience) |
| India investing | @Nithin0dha, @deepakshenoy, @NikhilKamathCIO | Half our audience; SIP / NFO / minimums talk |
| AI + builders | @sama, @paulg, @naval, @levelsio | Biggest culture conversation; history-to-today fuel |
| On-chain + tokenization | @rwa_xyz, @tokenterminal | Our category's news (X only, never IG vocabulary) |
| Keyword lanes | cost of living, funds + minimums, AI + jobs + money, tokenization | Catches posts from accounts not on the list (5,000+ views only) |

Ignore: price moves and liquidations (compliance), giveaway/airdrop/"farm points" posts, story-farm accounts
("here is the exact conversation that made me sign the divorce papers"), anything older than 24h unless it's still climbing.

### 2. Calendar moments (predictable trends, plan a week ahead)
Fed and RBI decisions, US jobs and CPI days, India budget day, big earnings (Nvidia, Apple), Diwali and **Muhurat
trading** (around 8 Nov 2026; confirm the NSE notice), tax deadlines, year-end "wrapped" season, New Year money resolutions, anniversaries of famous
money moments (1929 crash 24 to 29 Oct, Black Monday 19 Oct 1987, Lehman 15 Sep). Keep a running list at the bottom
of `growth/trends/README.md`.

### 3. Instagram and culture (formats, not just topics)
Instagram has no trends API we can use for free, so:
- **X topics cross over.** A money story that's hot on X today is usually a Reel topic on Instagram for the next
  24 to 72 hours. Re-cut it for fund investors (no crypto words).
- **Format trends come from the feed.** When Sheetal or anyone on the team sees a meme format, Reel template or
  trending audio blowing up on Explore, drop a screenshot or link into `growth/trends/inbox/` (any filename). The
  morning check reads the inbox and tries to fit one format to one of our ideas.
- **Paid boost (optional):** Composio's TikHub routes (Instagram search, TikTok trending search words, Reddit popular
  and trending searches, X trending by country) cost about $0.001 a call but the Composio wallet was out of credits on
  24 Oct. If Sheetal tops it up, add `TIK_HUB_TWITTER_WEB_FETCH_TRENDING` (country "UnitedStates" and "India") and
  `TIK_HUB_TIKTOK_WEB_FETCH_TRENDING_SEARCHWORDS` to step 1.
- **Web:** one WebSearch for the day's biggest money / AI / culture story to confirm what the radar shows and get a
  primary source (the article, the filing, the chart) to cite.

### 4. Score and pick
For each of the top ~8 candidates, score 1 to 5:
| | 1 | 5 |
|---|---|---|
| **Heat** | under 50 heat, old | 500+ heat, under 6h old, still climbing |
| **Bridge** | needs three jumps to reach us | one sentence connects it to access / low minimums, owning your fund, receipts, 24/7 |
| **Take** | we'd only repeat the news | we have an angle nobody in the replies has |
| **Safety** | tragedy, politics, a named person or competitor | a number or an idea, nobody gets hurt |

Keep anything scoring 15+ with Safety 4+. **Safety under 4 is an automatic skip**, however hot.
The bridge sentence is mandatory; if you can't write it, the trend isn't ours.

### 5. Write the board
`growth/trends/YYYY-MM-DD.md` (template in `growth/trends/README.md`): top trends with link, heat, age, bridge sentence,
remix move, take temperature, and a ready draft for the best 2 or 3.

## The mix from now on

| Share of posts | Type | Example |
|---|---|---|
| **~60%** | **Trend-led**: rides something hot today or this week | quote-post on the $5.32M "American dream" stat |
| ~25% | **Evergreen with a "why now" hook**: an educational idea opened with a current trend | the T+1 explainer opened with this week's market drop |
| ~15% | **Action posts** (comment STEPS / reply with your amount) | weekly "reply with the amount you'd start with" |

Every post's brief, caption file or calendar row records `trend:` (the link) or `trend: evergreen (why: …)`.
History-to-today (the favourite pattern) still counts as trend-led **when the "today" half is a live trend**:
Keynes' 15-hour week only lands as a trend post on a day layoffs or AI jobs are trending.

## Speed rules

- **X quote-jack / reply: within 2 hours** of the source post, while it's still climbing. A day late is worthless.
- **X original on a trend: same day.**
- **Instagram Reel on a trend: within 24 to 48 hours** (we render in about an hour; script + voice + render the same day).
- Pre-built **templates** make speed possible: keep the reel scene template, a "stat card" image layout and a
  "translation joke" card ready so a trend post is a 20-minute job, not a 3-hour one.

## Seven remix moves (how to make a trend ours)

1. **Quote-jack (X).** Quote the viral post with the one angle only we have, plus a number. Quote, never tag.
   Best for big accounts' news posts: they bring the audience, we bring the take.
2. **Format-jack.** Copy the *shape* of what's going viral (a ladder, a translation joke, a "the American dream now
   costs…" price list, a meme template, a POV Reel) and fill it with our substance. Shapes aren't owned; words are.
3. **Receipt redraw.** Rebuild the viral chart or stat as our own on-brand card and add the one comparison line it was
   missing (their stat + "and here's what it costs just to get into a fund"). Credit the source in the image or reply.
4. **History rhyme.** Today's trend + a surprising historical precedent ("1930: keynes predicted a 15-hour week. 2026:
   30,000 layoffs at one company"). This is Sheetal's favourite pattern, applied to a live topic.
5. **The calm explainer.** "everyone's talking about X. here's what it means for your money in 30 seconds." Best for
   Instagram Reels the day after a big money headline. Plain, no panic, no prediction.
6. **The counter-take.** Say the defensible opposite of the consensus in the replies ("everyone's blaming AI for
   layoffs. the real problem is how few people own a slice of the companies using it").
7. **The question post.** Turn the trend into a forced choice about the reader ("$5.32M for the american dream.
   which line item would you cut first?"). Cheapest replies there are; max 1 in 5 posts.

**What we never copy:** someone's words, their image or video file, their face, or their creator voice. We take the
public fact and the format, credit data with "via" or a quote-post, and make our own visual. No reposting media.

## Hot takes without getting reported

X subtracts **234** for a report, 58.8 for a mute and 47.5 for "not interested". One reported post wipes out ~47 replies.
So we write **spicy, never toxic**.

### The temperature ladder
| Temp | What it is | Example (access narrative) | Rule |
|---|---|---|---|
| Mild | A sharp observation | "the hardest part of investing was never picking. it was being allowed in" | Post freely |
| **Spicy** | **An unpopular opinion people will argue with** | "the fund industry's real product was never returns. it was the minimum" | **Our default.** Post under standing approval |
| Hot | Challenges a rule or institution head-on | "accredited investor rules protect the rich from competition more than the poor from risk" | Draft, send to Sheetal first |
| Scorching | Insults a group, a person or a company | "fund managers are thieves" | Never |

### The rules
1. **Fight systems and ideas, never people.** Minimums, gatekeeping, paperwork, office hours, quarterly PDFs. No named
   person, company or competitor as the villain, and no attacking 1% fees (Sheetal, 18 Oct: 1% is reasonable).
2. **Defensible in one reply.** If someone pushes back, we can answer with a number or a source. If not, don't post it.
3. **The take must be true, the framing can be bold.** Exaggerate the tone, never the facts.
4. **No identity, no politics, no tragedy.** Elections, wars, deaths, religion, gender, nationality, a person's looks:
   skip the trend, however big. Policy only when it's about access to investing, and then "hot" (Sheetal first).
5. **Never tag strangers or reply-guy a stranger with a take on *them*.** Quote-post the topic; tagging invites blocks.
6. **No bait-and-switch.** Line 1 promises exactly what the post delivers. Clickbait earns "not interested".
7. **End open, not smug.** Close on a forced choice or a question so disagreement turns into replies, not reports:
   "agree or disagree?", "where's the line for you?".
8. **Compliance still wins:** no return promises, no price talk (a market crash is a skip, not a take), no "buy",
   risk line in the first reply when investing is discussed, roadmap as "planned".
9. **Instagram is gentler.** Same takes, softer edges, zero crypto words, and funds are good products we're comparing
   fairly (`brand/instagram-strategy.md`). Spicy at most; hot takes stay on X.

## CTAs on trend posts

- **X:** end on a forced choice, a question about the reader, or an arguable verdict (style guide rule 9). Once a week,
  the action post: "reply with the amount you'd start with and we'll send you the 3 steps"; answer every reply within
  2 hours, mutuals first (`growth/comments/comment-strategy.md`).
- **Instagram:** end card "Want your own fund, even a $10 one? Comment STEPS." once the comment-to-DM bot is live
  (status in `growth/comments/comment-strategy.md`; until then, end on a question). Send line in the caption, follow
  ask in the DM, two asks max in the video.

## Measuring it

- Tag each row in `growth/x/tracker.md` and the calendar with `trend: yes/no`, the lane and the remix move.
- Weekly (with the analytics pull): median views of trend-led vs evergreen posts, quotes and replies per post, which
  lanes and remix moves won. Keep winners, drop losers, and update this file.
- **Targets by 7 Nov 2026:** trend-led X posts median **2x** evergreen; at least one X post over **10,000 views**;
  at least one Reel over **1,000 reach**.

## Worked example: the 24 Oct radar

The radar run at 18:01 UTC on 24 Oct turned up (full board: `growth/trends/2026-10-24.md`):
| Trend | Heat / age | Verdict |
|---|---|---|
| "The American dream now costs $5.32 million over a lifetime" (@unusual_whales, Investopedia analysis) | 900, 1h, 115 replies | **Take it.** Bridge: the dream's priciest door is investing itself, funds want $10k+ just to let you in |
| 2026 layoffs list: UPS 30,000, Oracle 30,000, Amazon 16,000 (@KobeissiLetter) | 575, 27h, 453 replies | **Take it** as a history rhyme (Keynes' 15-hour week) |
| US family health premium hits record $28,303 (@KobeissiLetter) | 1,314, 2h | Weak bridge (insurance, not investing). Skip |
| Crypto drops, $200M liquidated (@WatcherGuru) | 2,141, 4h | **Skip:** price talk, compliance |
| "could have invested in an index fund and eventually bought a senator" (@dieworkwear) | 604, 2h | **Skip:** politics + a named person. Great *shape* though (regret joke) |
| "History doesn't repeat itself, but it often rhymes" on AI (@Nithin0dha) | 64, 12h, 84 replies | Good reply target for a substantive early reply, not a post |
