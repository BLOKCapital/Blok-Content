# QA summary · Before the Bell, Part 3: the 25 cent stamp (11 Nov 2026)
- Voice: Brooks (Chatterbox), 3 takes per line, best picked by speech recognition. Final mp4 check: 6 of 9 lines exact; 3 flagged only for spelling ("AI"/"A I", "IPO"/"I P O", "$4.12" vs "four dollars and twelve cents") plus two soft spots heard by Whisper: "savings stamp" heard as "saving stamp" (the s runs into "stamp") and "you'd trade it" heard as "you traded". build/qa-speech.txt
- Loudness -15.0 LUFS, peak -1.9 dBFS. Length 60s.
- Contact sheet at 2 fps (build/sheet.jpg): nothing cut off or overlapping; hook + "TODAY'S 25¢ VERSION: AT THE END" on screen from frame 0; answer ($10 fund) held to the end.
- Copy: check_copy.py 0 issues; no rupees, no crypto words, risk line + AI voiceover note present.
- Facts (independent grounding review, 5 lines fixed): War Savings stamp $4.12 Dec 1917 to Jan 1918, worth $5 on 1 Jan 1923; 25 cent Thrift stamps, 16 to a card (Wikipedia). Retail slice: "weighing", "still being discussed", 15-20% of IPO shares (Bloomberg via Finimize); company never named, no price, no buy talk. $10,000+ phrased as "a fund of your own, run just for you".
- Voice review: 3 rewrites applied, lint 0 flags.
- Lead magnet for FUND: growth/lead-magnets/2026-11-03-private-banker-prompts/ (same as Parts 1 and 2).
