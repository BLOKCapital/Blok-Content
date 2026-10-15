# Trial reels test: "Keynes promised me" × 7 hooks

**Base video:** `content/2026-10-15-keynes-promised-me/keynes-promised-me.mp4` (64s, not posted yet).
**Why this one:** it is our purest history-to-today story (Keynes 1930 → your money works 32 of 168 hours), the body
holds with a joke every few seconds, and it hasn't been posted, so the winning hook can become its first normal post.
Its weak spot is the opening: no on-screen hook, and the point ("your money got the short week") arrives at 18s.

**What changes per variant:** only the first 2 to 4 seconds: a hook card on screen from frame 0, a cold open on three
of them, and a 0 to 6 percent zoom so no two uploads are identical. Everything after that is the original reel.
How it's built: `build/make_variants.py` (ffmpeg + Pillow; rerun with `python3 build/make_variants.py`).

How to post: **Sheetal posts these by hand in the Instagram app** (our Composio tool can't make trial reels).
New Reel → pick the file → caption below → on the last screen turn on **Trial** → choose **"Share manually"** →
turn on the AI label → Share. If there's no Trial toggle, stop and tell Claude (don't post them as normal reels).

## The variants
| # | File | On-screen hook (first seconds) | Opening | Angle |
|---|---|---|---|---|
| 1 | `v1-prediction.mp4` | In 1930, Keynes predicted you'd work **15 hours** a week by now. | original start | the prediction (control) |
| 2 | `v2-wrong-worker.mp4` | Keynes was right about the 15-hour week. He just picked the **wrong worker.** | original start | twist on the prediction |
| 3 | `v3-saturdays.mp4` | Wall Street worked Saturdays until **1952.** Now your money takes weekends off. | original start | forgotten history fact |
| 4 | `v4-3am.mp4` | It's 3 a.m. Do you know what **your money** is doing? | cold open: "It's three in the morning now." | nod to the old "It's 10 p.m., do you know where your children are?" TV line |
| 5 | `v5-waits-for-monday.mp4` | Your money has a 9-to-5. And it takes **every weekend** off. | cold open: "Nothing. It waits for Monday. Like you." | relatable office-hours |
| 6 | `v6-32-of-168.mp4` | Your money works **32 hours** a week. A week has 168. | original start | one number |
| 7 | `v7-ai-took-my-emails.mp4` | AI took my emails. It didn't give me back **a single hour.** | cold open: "I took your emails. Your slides. Your spreadsheets." | AI today |

Each has a matching `-cover.jpg` (frame with the hook card) if the app asks for a cover.

## Captions
Every caption = its own first line + the shared body below.

1. In 1930, Keynes predicted you'd work 15 hours a week by now. Did anyone get that memo? 👀
2. Keynes was right about the 15-hour week. He just picked the wrong worker.
3. Until 1952, Wall Street opened on Saturdays. Now your money takes the whole weekend off.
4. It's 3 a.m. Do you know what your money is doing?
5. Your money has a 9-to-5. And it takes every weekend off.
6. Your money works about 32 hours a week. A week has 168.
7. AI took my emails, my slides and my spreadsheets. It didn't give me back a single hour.

Shared body:
```
In 1930, John Maynard Keynes predicted that by about now we'd work 15 hours a week. He was half right. Your money got the short week.

Most stock markets are open roughly 6.5 hours a day, weekdays only. That's about 32 hours out of 168. Evenings, weekends and holidays, your money waits for Monday.

On-chain markets run on a public ledger that never closes: 24 hours a day, 7 days a week, and anyone can check what's happening, any time.

Which would you rather have: the 15-hour week, or money that works the other 136 hours? 👇

Educational only, not financial advice. On-chain assets are volatile; only invest what you can afford to lose.
AI-generated voices and animation.

#investing #personalfinance #mutualfunds #etf #indexfunds #keynes #moneytips #financialliteracy #futureofmoney #ai
```
(For variant 1 drop the first sentence of the body, since the first line already says it.)

## Posting slots (UTC)
Trials only reach non-followers, so they don't crowd the main feed schedule in `growth/tracker.md`.
| Variant | Post as trial | Read at 24h | Read at 72h |
|---|---|---|---|
| 4 (3 a.m.) | Fri 16 Oct 12:00 | Sat 17 12:00 | Mon 19 12:00 |
| 2 (wrong worker) | Fri 16 Oct 13:30 | Sat 17 13:30 | Mon 19 13:30 |
| 6 (32 of 168) | Fri 16 Oct 15:00 | Sat 17 15:00 | Mon 19 15:00 |
| 3 (Saturdays) | Fri 16 Oct 16:30 | Sat 17 16:30 | Mon 19 16:30 |
| 1 (prediction) | Sat 17 Oct 12:00 | Sun 18 12:00 | Tue 20 12:00 |
| 5 (waits for Monday) | Sat 17 Oct 13:30 | Sun 18 13:30 | Tue 20 13:30 |
| 7 (AI) | Sat 17 Oct 15:00 | Sun 18 15:00 | Tue 20 15:00 |

## How the winner is picked
Read each trial's Insights at 24h. **Winner = lowest skip rate** (viewers who swiped away in the first 3 seconds).
Tiebreak: average watch time, then (shares + saves) per 1,000 views. Ignore likes. Confirm at 72h, then post the winning
file as a normal Reel to the feed (full caption, its cover) and archive the other trials.

| Variant | Views 24h | Skip rate | Avg watch time | Shares | Saves | Views 72h | Notes |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |

## Fact check
- Keynes, "Economic Possibilities for our Grandchildren" (1930): "three-hour shifts or a fifteen-hour week".
- NYSE regular hours 9:30 to 16:00 ET, Mon to Fri = 6.5 h a day, 32.5 h a week.
- NYSE ended Saturday trading in 1952 (Emory GBSL, "NYSE ends Saturday session").
- "It's 10 p.m. Do you know where your children are?" is a US TV public-service line from the late 1960s onward; we only echo its shape.
- No return claims; risk line in every caption; AI disclosure in caption and via the app label.
