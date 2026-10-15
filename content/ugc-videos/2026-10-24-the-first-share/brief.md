# The first share anyone could buy (Reel)

**Format:** vertical 1080x1920, 69.97s, 30fps, H.264 High + AAC 48k, 43.8MB, -14.2 LUFS (md5 f5c298070d1e7caeb4f2f9b3ec7bc354), cover.jpg md5 b1103b1f624eb3aa829acfee3b75cf4f, suggested thumb_offset 2500ms · **Audience:** fund and ETF investors (Instagram rules apply) · **Status:** rendered 2026-10-15, scheduled for Sat 24 Oct 2026, 18:52 IST
**Series:** second "in the room" history Reel, after "The night a bank vanished" (best post by watch time: 29s avg watch, lowest skip rate, most comments). Same presenter, same pipeline, same look.
**Working title / file name:** "The first share ever sold". On screen we say "The first **share** anyone could buy", because the VOC was not the first company ever to issue shares (the English East India Company, 1600, and earlier joint-stock ventures predate it). What the VOC did first was open its subscription to the general public ("all residents of these lands may buy shares", charter art. 10) and let shares be transferred, which is why historians call it the first IPO / first stock exchange.

## The idea
Amsterdam, August 1602. Our presenter whispers to her phone in a candlelit room while a clerk writes names into the VOC subscription book. Simple version: you put money in, you own a piece, but there's no certificate; your ownership is a line in the company's book that only the company's clerk can change. 400 years on, owning a fund still works a lot like this (a line in someone else's records), and mostly that works fine. "So here's the idea": what if the book was public, and only you could sign your own line? That's an on-chain portfolio. Honest catch, then the last line: **"Your name was always in the book. You just never held the pen."**

## What we copied from the bank Reel
| Bank Reel | This Reel |
|---|---|
| Presenter (auburn hair, freckles, cream cable-knit cardigan, gold hoops) "in the room" at a real night | Same woman, time-slipped into a 1602 Amsterdam merchant house, clerk writing behind her |
| Cold open "Shh. Look at his phone." | "Shh. Watch the clerk's pen." |
| Serif title, one word lime | "The first **share** anyone could buy." (Fraunces, #7ED116) |
| ELI5 "simple version" | "A company needs money for ships. You chip in..." |
| Real dated figures typed on a dark screen with source | SAT 31 AUG 1602 · 1,143 people · f 3,679,915 (Petram); 09 SEP 1606 · Enkhuizen · 150 guilders (Westfries Archief) |
| Fair to the old system | "Mostly, that's fine." + Illustrative "who keeps the record" screen (fund house / registrar / custodian, "varies by country") |
| "So here's the idea" pivot, public-ledger card | "What if the book was public?" card: who can read it: anyone; who can change it: only you |
| Quotable last line | "Your name was always in the book. You just never held the pen." |

## Script (`build/script.txt`)
Shh. Watch the clerk's pen. / It's August 1602. Amsterdam. / And he's writing down the first shares anyone could buy. / Okay. Simple version. / A company needs money for ships. You chip in. / Now you own a tiny piece of it. That's a share. / But you don't get a certificate. / You get a line in their book. Your name, your amount. / By the last night, eleven hundred and forty-three people had signed, in Amsterdam alone. / Almost three point seven million guilders. / Want to sell? A director watches the clerk move your line to someone else. / The oldest receipt ever found? 1606. / A city messenger. A hundred and fifty guilders. / Four hundred years on, owning a fund still works like this. / Your units are a line in someone else's records. Mostly, that's fine. / So here's the idea. / What if the book was public, for anyone to read? / And only you could sign your line? / That's an on-chain portfolio. / It's newer. Prices can swing. So start small, and learn first. / But the idea is four hundred years old. / Your name was always in the book. You just never held the pen.

## Fact check (sources and exactly what each says)
| Claim on screen / in VO | Source | What it says |
|---|---|---|
| Subscription closed Saturday 31 Aug 1602, at director Dirck van Os's house, Amsterdam | Erste Asset Management blog "420 years: the birth of the stock exchange" (2022) · The Low Countries, "Dirk van Os, Antwerp native in the VOC" | Book closed at midnight on Sat 31 Aug 1602 at Van Os's house on the Nes; registration took place at his home |
| 1,143 investors in Amsterdam; f3,679,915 | J. Ekama, Leiden University PhD thesis (2018), citing L. Petram, *The World's First Stock Exchange* (Columbia UP, 2014) | "1,143 investors together raised f3,679,915" in the Amsterdam chamber |
| No certificate; ownership was a line in the company's books | Ekama (2018) citing Petram; Westfries Archief | "No share papers were issued; the account books were the only proof of ownership." Westfries Archief: the VOC "did not issue stock certificates and tracked shares in its own ledgers" |
| Selling: a director witnesses, the bookkeeper moves the line | Ekama (2018) citing Petram; Euronews (13 Apr 2025) citing Petram | Transfers witnessed by one or two directors, on a form signed by buyer, seller and director; bookkeeper credits the new owner. Charter provision: shares could be transferred through the chamber's bookkeeper |
| "First shares anyone could buy" | Euronews (2025) quoting VOC charter art. 10 | "All the residents of these lands may buy shares in this Company" |
| Oldest receipt: 9 Sep 1606, a city messenger, 150 guilders | Westfries Archief "The world's oldest share"; Guinness World Records "Oldest share certificate" | Pieter Harmensz, city messenger of Enkhuizen, bought a 150-guilder share in the Enkhuizen chamber in 1602, paid in instalments, received the receipt ("note of remittance") on 9 Sep 1606 when he made the last payment |
| Found in 2010 by a Utrecht University student | Business History Conference news (2010); DutchNews (11 Sep 2010) | Found by Ruben Schalk, a master's student at Utrecht University, in the Westfries Archief (Hoorn) |
| Funds: units are a line in someone else's records | `brand/instagram-strategy.md` fact rules | Funds involve intermediaries (fund house, custodian, registrar/transfer agent); screen says "Illustrative · typical setup, varies by country" |

Not used / could not verify: the exact physical location of the 1602 Amsterdam subscription register today; the total VOC capital across all chambers (commonly ~f6.4m) was left out on purpose.

## Production
- **Stills** (`build/img/A-K.jpg`): Gemini 3 Pro Image (Nano Banana Pro), 9:16, 2K, via Composio. Presenter described with the same traits as the bank Reel; clerk, director, townspeople are anonymous and stylised (faces turned or generic). No real people depicted. Receipt shot (H) is a generic prop, not a reproduction of the real document, and is cropped so no coins show.
- **Voice:** Gemini 2.5 Pro TTS, voice "Aoede", hushed vlogger direction, four takes (`build/takes/`). Take 1 is the "brisk" re-take; takes 2-4 are the first pass (the sandbox kernel restarted before the re-takes could be copied out). Trimmed, joined with 0.45s gaps, sped up 1.2x with ffmpeg `atempo` to land at ~70s (`build/vo.wav`).
- **Word timings:** no Whisper available on this machine (Hugging Face blocked), so `build/fa.py` force-aligns the known script to the audio: pauses from `silencedetect` (`build/sil.txt`) split speech into segments, a DP assigns script words to segments, words are spread by character weight. Then `align.py` → `timeline.json`, `mktiming.py` → `timing.json` (line spans + 1-4 word captions).
- **Music + SFX:** original, synthesised in `build/mix.py` (D minor pad turning to D major at "So here's the idea", quill scratches, keyboard clicks on the figure screens, low pulse while the book fills, boom on the guilders figure, ticks + ding on the ledger card, end chime). -14 LUFS.
- **Rebuild:** `python3 build/fa.py build && python3 build/align.py build && (cd build && python3 mktiming.py) && node build/preview.mjs "" /tmp && python3 build/mix.py && node scripts/render-reel.mjs build/scene.built.html build/mix.wav the-first-share.mp4 30`

## Compliance
- No crypto vocabulary or visuals (checked script, screens, caption): "on-chain portfolio" and "public ledger" only.
- No return claims. Historical figures are subscriptions, not returns. Risk line spoken ("It's newer. Prices can swing. So start small, and learn first.") and on the end card.
- Fair to funds: "Mostly, that's fine."; intermediaries screen labelled Illustrative and "varies by country".
- AI disclosure on end card and caption ("AI-generated voice and visuals; events dramatised"). Switch on Instagram's AI label when posting (API can't).
- Original music (no library track).
