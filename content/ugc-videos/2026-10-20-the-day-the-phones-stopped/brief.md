# The day the phones stopped answering (Reel)

**Format:** vertical 1080x1920, ~69s, 30fps · **Audience:** fund and ETF investors (Instagram rules apply) · **Status:** rendered 2026-10-15, scheduled for Tue 20 Oct 2026, 18:52 IST
**Follows:** "The night a bank vanished" (2026-10-12), our best post by watch time (29s average watch, lowest skip rate, most comments). Same recurring presenter, same pipeline, same look, 38s shorter.
**Topic choice:** Black Monday's anniversary is 19 October, the day before posting, so "1987 crash" searches and anniversary posts are live. The lesson (can you see and reach what you own when it matters?) ties to "your keys, always" with no crypto vocabulary.

## Beat sheet
| Beat | Line(s) | Visual |
|---|---|---|
| Hushed cold open | "Shh. Hear that?" (phones ringing) | Presenter (same fictional auburn-haired woman, cream cardigan) in a 1987 New York brokerage branch, finger to lips; broker on the phone behind her |
| Title card | "Monday, October nineteenth, 1987. New York. And nobody's picking up." | Fraunces serif: "The day the **phones** stopped answering." (phones in lime #7ED116) over a blinking multi-line desk phone |
| ELI5 simple version | "Back then, to sell a share, you called your broker. That phone line was the only door." | Presenter explaining; hand on a paper order ticket |
| The run | "Today, everyone's calling at once." | Queue at payphones (backs only) |
| Real dated figures | "The Dow fell 22.6%. In one day. 604 million shares traded in New York." | Typed dark screen: MON 19 OCT 1987 / −22.6% / (−508 points) / 604,000,000 shares, sources on screen |
| Phones | "Small investors couldn't get through. Some market makers just stopped answering." | "Calls to my broker" log (busy / no answer, labelled Illustrative), then the unanswered phone |
| Fairness | "Nobody here is a villain. They're overwhelmed. And yes, the market came back, within two years." | Chaotic office; then dusk, empty office, with on-screen note "Stocks were back to their pre-crash highs in under two years. Source: Federal Reserve History" |
| Sting | "But today, a lot of people can't even find out where they stand." | Push-in on presenter |
| Pivot | "So here's the idea." | Present day, morning light |
| Idea | "...an account only you control, on a public ledger that's open around the clock, and anyone can check. Every holding, any hour." | Public-ledger card (Illustrative) |
| Honest catch | "It's newer. Prices can swing. So start small, and learn first." | On-screen note: "Newer · prices can swing · start small / You can lose money. Learn first." |
| Quotable last line | "What you own shouldn't be one busy signal away." | Close-up at dusk |
| End card | | Logo, "Learn it before you need it.", Follow @blok.capital, disclaimer + AI disclosure + sources |

## Fact check (every on-screen and spoken claim)
| Claim | Source and what it says | Status |
|---|---|---|
| Dow fell 22.6% on Mon 19 Oct 1987 (508 points) | Brady Commission, *Report of the Presidential Task Force on Market Mechanisms* (Jan 1988), p. 1: "On October 19, 1987, alone, the Dow fell by 508 points or 22.6 percent." Federal Reserve History, "Stock Market Crash of 1987" (Bernhardt & Eckblad, 2013): the Dow "finished down 508 points, or 22.6 percent". | Verified |
| 604 million shares traded on the NYSE that day | Brady report, p. 36: "...on volume of 604 million shares worth just under $21 billion." | Verified |
| Small investors couldn't get through to brokers | Brady report, p. 47: "an understandable difficulty experienced by small investors in reaching retail brokers". Christian Science Monitor, 28 Oct 1987: "For many people, the most ominous sound of last week's debacle on Wall Street was a telephone busy signal", with "tales of investors who couldn't reach their brokers on the telephone". | Verified; phrased as "small investors" / "many", not "everyone" |
| Some market makers stopped answering their phones | Brady report, p. 50 (OTC/NASDAQ market): "some market makers ceased performing their function, merely by not answering their telephones during this period", and were "unreachable when they were overwhelmed by the volume of telephone orders". SEC Historical Society (Nasdaq gallery): "overwhelmed market makers stopped answering telephones"; Nasdaq made its Small Order Execution System mandatory in 1988 in response. | Verified; script says "some" and "overwhelmed" |
| The market came back within two years | Federal Reserve History: markets "quickly recovered a majority of their Black Monday losses"; the Dow regained 57% of its losses within two sessions; less than two years later US stocks were back at pre-crash highs; no recession or banking crisis followed. | Verified |
| "To sell a share, you called your broker" | General description of 1987 retail trading (orders placed by phone with a broker; no online retail trading). Brady p. 47 and CSM describe exactly this channel failing. | Simplification, fair for the ELI5 beat |
| Call log times (09:41, 10:15...) and ledger rows | Invented to illustrate | Labelled "Illustrative" on screen |
| A public ledger is open around the clock; anyone can check it | brand/instagram-strategy.md fact rules (on-chain markets run 24/7; public ledger is verifiable) | OK |

Not used because it isn't well enough documented in what we could reach: a specific NYSE ticker delay figure (often quoted as "over an hour" / "two hours late"), counts of unanswered calls, and how many investors were affected. The SEC Division of Market Regulation report *The October 1987 Market Break* (Feb 1988; chapters 9 "OTC market" and 12 "Investor complaints") covers the phone problems too, but its scanned PDFs couldn't be read from this environment, so we cite the Brady report pages instead.

## Production
- Stills: Gemini image model (Nano Banana Pro, `gemini-3-pro-image-preview`, 9:16, 2K) via Composio `GEMINI_GENERATE_IMAGE`; 11 stills in `build/img/` (A, B, C, D, F, G, H, K, M, N, S). Same presenter description as the bank Reel: "a woman about 30 with shoulder-length auburn hair, light freckles, small gold hoop earrings, wearing a cream cable-knit cardigan over a white t-shirt". Every prompt ends "Muted, slightly cool cinematic colour grade, film grain, natural, not glossy. No text, no captions, no logos, no legible writing." No real people depicted; bystanders are generic or seen from behind. `N.jpg` is cropped to remove a camera-UI overlay the model drew.
- Voice: Gemini 2.5 Pro TTS (`gemini-2.5-pro-preview-tts`), voice "Aoede", eight takes with per-section direction (hushed → explaining → tense → gentle → brighter at the pivot → slow ending), in `build/takes/`. `build/stitch.py` trims, shortens long pauses to 0.38s, joins with the script's pauses and speeds up 1.1x → `build/vo.wav` (65.1s).
- Word timings: `build/fa.py`, pocketsphinx forced alignment of `vo.wav` to `script.txt` (Whisper in the Composio sandbox ran out of memory and Hugging Face is blocked locally) → `build/vo.json`.
- Music + SFX: original, synthesised in `build/mix.py` (D minor pad turning to D major at "So here's the idea", 1980s two-tone phone rings, busy-signal bursts on the call log, keyboard clicks on the typed figures, tension pulse while everyone calls, sub booms on −22.6% and the sting). −14 LUFS.
- Rebuild: `python3 build/stitch.py` → `python3 build/fa.py` → `python3 build/align.py build` → `python3 build/timing.py` → `node build/preview.mjs "" /tmp` (writes scene.built.html + cues.json) → `python3 build/mix.py` → `node scripts/render-reel.mjs build/scene.built.html build/mix.wav build/raw.mp4 30` → `ffmpeg -i build/raw.mp4 -c:v libx264 -preset slow -crf 21 -maxrate 9M -bufsize 18M -pix_fmt yuv420p -c:a copy -movflags +faststart the-day-the-phones-stopped.mp4` (the grain makes a CRF 18 render ~124MB; this brings it to ~60MB). Cover: frame at 2.9s with captions hidden (`cover.jpg`).

## Compliance
- No crypto vocabulary or visuals; "on-chain portfolio" and "public ledger" only, in plain words.
- No return claims; risk line spoken ("It's newer. Prices can swing. So start small, and learn first."), as an on-screen note, on the end card and in the caption.
- Fair to brokers and markets: "Nobody here is a villain. They're overwhelmed." and "the market came back, within two years" (sourced on screen). No claim that brokers or markets are unsafe today.
- Call log and ledger labelled Illustrative; figures sourced on screen.
- AI disclosure on end card and caption; switch on Instagram's AI label when posting.
