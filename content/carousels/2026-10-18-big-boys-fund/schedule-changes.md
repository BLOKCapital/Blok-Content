# Proposed schedule changes for the new narrative (18 Oct 2026)

For the "Posting calendar, Instagram + X" thread, via the coordinator. Written by the "new narrative" thread; nothing here has been applied
to the calendar or to any scheduled task by this thread.

**The narrative (Sheetal, 18 Oct; also in the project instructions):** the fund world is for the big boys ($10k to $100k minimums, setup
fees, bank intro fees). BLOK means everyone can have a fund, even your own $10 one. 1% fund fees are reasonable, so the "your 1% fee is
costing you" story is dropped. Lead with access and low minimums.

I checked every enabled scheduled task (list_triggers, 18 Oct 10:40 UTC) and the copy each one posts. Live posts are left alone.

## 1. Pull

| When (IST) | Task | Post | Why | Action |
|---|---|---|---|---|
| Sun 18 Oct 20:00, X | trig_01CZqHRafoqqmwAUeDvf2gNJ | "1792: 24 brokers under a buttonwood tree" (4 photos) | The whole post is the fee story, and the attached photos say "minimum fee 0.25%", "the fee rule lasted 183 years", "fees fell, the middlemen stayed". Text can't fix baked-in photos. | **Already paused by the coordinator (18 Oct).** Delete it, mark the calendar row "pulled (new narrative)". |
| Every 4h until Sun 18 Oct 18:07 UTC | trig_01T5U8mmQMxRpp2KntEZNGeZ "IG FEE DM replies" | DMs the 1% "fee receipt calculator" to anyone who writes FEE | It actively pushes the dropped fee story; the "DM us FEE" CTA lived on the 14 Oct fee carousel. | Disable now (it ends tonight anyway). If anyone DMs FEE later, answer by hand with the new story. |

## 2. Change (copy or photos)

| When (IST) | Task | Post | Change |
|---|---|---|---|
| Fri 23 Oct 11:30, X | trig_01Tyn2EA1xMcg5ySoMNcrx6B | "5 questions to ask before you invest" (4 photos) | Photo 2 is slide-03, the "a 1% gap sounds tiny... leaves you with about 25% less" chart, and the self-reply leads with the same fee maths. **Swap photo 2 to slide-02.jpg (md5 532355c9763b4697414b92e589cd18b0, same commit a8afa62)** and post the text from `replacements/five-questions-x.md` (main text unchanged, new self-reply). Photo order becomes slide-01, slide-02, slide-05, slide-06. |

## 3. Add: the new collage panorama on the new narrative

`content/2026-10-18-big-boys-fund/` ("The first fund was built for people without much money"). Files are pushed to GitHub on branch
`claude/project-thread-51sxnf`; the commit and md5s are in `post-spec.md` in this folder once the push is done. Needs Sheetal's "yes" first.

| When (IST) | Platform | What |
|---|---|---|
| Sun 18 Oct 20:00 (14:30 UTC) | X | Fill the slot freed by Buttonwood: `x/pan.mp4` (21 s) + X text and self-reply from `caption.md` (X / XR blocks). Only if Sheetal says yes before then; otherwise use Mon 19 Oct 17:45 (12:15 UTC) if free, or the next free X slot. |
| Mon 19 Oct 15:30 (10:00 UTC) | Instagram | 5-video carousel, slide order matters (one continuous panorama), caption = IG block, slide-01 as a Story. Keeps 3+ hours clear of the 18:52 rebalancing Reel. Drawn in code with an original track, so no AI label. |

## 4. Checked and left as they are

These mention cost only as "know what you pay", which fits the new story (it says 1% is fair, not hidden), or don't touch fees at all.

- Bogle's folly X (today 17:45): no fee line in the post. Already rewritten replies by the Buffett index thread.
- Know-nothing investor X (Mon 19 11:30): "simple" instead of "cheap" already changed by the Buffett index thread; the small "low cost" tile on a photo is Buffett's own advice, not a fee attack. Keep.
- Greentext "quarterly pdf" X (Mon 19 20:00): "can't find the fee / page 11" is about a hard-to-read statement, not the size of the fee. Keep.
- What your fund owns carousel (IG Wed 21, X Sat 24): step "turn the expense ratio into money: 1% of 10,000 is 100 a year" is plain literacy with no judgement. Keep.
- Statement carousel (IG Fri 23): "the full cost in plain money" is transparency. Keep.
- Rebalancing, Black Monday, Newton, first share, Wednesdays, tally stick, hidden word, Keynes test reels, X7 to X9: no fee angle.

## 5. Off the shelf for good (never scheduled again)

`content/2026-10-12-the-one-percent-fee/`, `content/2026-10-12-the-one-percent-fee-pitch/`, `growth/posts/2026-10-14-the-one-percent-fee/`,
the Fee X-ray calculator and "DM us FEE" play (`growth/creative-plays.md` sections 1 and 2), and the fee hooks in `growth/x/what-goes-viral.md`.
Each now carries a "retired 18 Oct" note.
