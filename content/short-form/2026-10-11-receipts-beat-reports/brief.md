# Receipts beat reports (Reel / X video)

**Format:** vertical 1080x1920, 45.7s, 30fps · **Audience:** fund and ETF investors (Instagram rules apply) · **Status:** rendered, not posted
**Trend hook:** "asset management should have a public record" (research/2026-10-11-x-trends.md, #2)
**Style:** old money: linen stationery, double-rule frame, Cormorant Garamond italics, chapter numerals, wax seal, solo piano.

## Story (three acts + verdict)
| Act | Lines | What we see |
|---|---|---|
| I · The quiet rule | "Old money has a quiet rule. Don't just read the report. Check the books." | A glossy report and a leather ledger side by side; the ledger lifts |
| II · The report | "Here's the report a fund sends you. Every quarter. Heavy paper. Lovely charts. But look closely. It shows a single day, often weeks after it happened. Everything in between? You take it on trust." | Sealed envelope, report cover flips open, magnifier lands on "As of 30 June", a timeline stretches to "It reaches you", stamp: TAKEN ON TRUST |
| III · The books | "Now, the books. An on-chain portfolio lives on a public ledger, a shared record no one can quietly edit. Every trade is written down the moment it happens. Time-stamped. Permanent. Anyone can check." | Split screen: frozen report vs live ledger with ticking clock; an edit attempt bounces off a lock; a new row types in; a click shows "Checked on the public ledger" |
| Candour | "It's newer, and prices can swing. But the record is always open." | Honest trade-off card |
| Verdict | "One is a report. The other, a receipt. And receipts beat reports." | Report vs printed receipt, title card, end card with disclaimer |

## Sound
- Voice: Andrew (`en-US-AndrewMultilingualNeural`, +0%), voiced line by line and stitched with hand-set pauses (`scripts/assemble-vo.py`).
- Music: original solo piano + string pad synthesised in `build/score.py` (B minor, turns to D major at "Now, the books", resolves on "beat reports"). No samples, no licences needed.
- 58 synthesised SFX keyed to the visuals (`window.CUES` in `build/scene.html` → `build/cues.json`): whooshes on every cut, paper slide, wax-seal thud, page flip, day ticks, stamp, mouse clicks, typewriter keys, lock "deny", verify ding, receipt printer, closing chime.
- Mix: music ducked under voice, loudness -14 LUFS, peak -1.2 dBFS.

## Caption
Old money has a quiet rule: don't just read the report. Check the books.

A fund's quarterly report is a snapshot of one day, often weeks old by the time it reaches you. An on-chain portfolio works differently. Every trade is written to a public ledger the moment it happens: time-stamped, permanent and open for anyone to check.

It's newer, and prices can swing, so learn before you start. But the record never goes quiet.

Receipts beat reports. 🌱

Follow @blok.capital for plain-English lessons on on-chain portfolios.

Educational content only, not financial or investment advice. On-chain assets can be volatile and you can lose money. AI-generated voiceover. Original music.

#investing #mutualfunds #ETF #personalfinance #wealth #financialliteracy #moneytips

## Compliance check
- No crypto vocabulary or visuals; "public ledger" glossed on first use.
- Fair comparison: funds aren't disparaged; disclosure timing hedged with "often" (US quarterly, India monthly).
- No return claims or numbers; ledger rows, holdings and dates labelled "Illustrative".
- Risk line spoken and on the end card; disclaimer + AI voiceover disclosure on end card and caption.
- Turn on Instagram's AI info label in the app when posting.

## Rebuild
```
python3 scripts/assemble-vo.py <build>/vo-lines <build>/vo 0.12 0.25,0.5,0.2,0.35,0.2,0.25,0.55,0.25,0.2,0.2,0.45,0.45,0.35
python3 scripts/build-timeline.py <build>/script.txt <build>/vo.json <build>/timeline.js
node scripts/preview-reel.mjs <build>/scene.html /tmp cues | tail -1 > <build>/cues.json
(cd <build> && python3 score.py)
node scripts/render-reel.mjs <build>/scene.html <build>/mix.wav <piece>/receipts-beat-reports.mp4 30
```
