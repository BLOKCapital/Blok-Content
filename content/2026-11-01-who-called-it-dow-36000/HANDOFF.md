# Who Called It? Part 2: Dow 36,000 (handoff, 2 Nov 2026)

Status (2 Nov, later): FINAL RENDERED with Chatterbox voice cloned from Brooks: `who-called-it-dow-36000.mp4`, `cover.jpg`, `caption.md`. QA passed (build/qa-speech.txt, -15.6 LUFS, peak -1.4). Waiting for Sheetal's yes, then post.
Chatterbox install tip: `pip install --no-deps chatterbox-tts` + its deps, keep CPU torch (otherwise it pulls CUDA torch 2.6). Scripts: build/gen_all.py, score.py, assemble.py (MMS forced alignment for word timings).
Earlier status: visuals and motion done (`draft-motion-preview.mp4`, placeholder Kokoro voice). Only the natural voice is missing.
Sheetal: no paid top-ups. She wants a free, very human voice (Kokoro sounds "very AI" to her).

## Do next
1. Needs huggingface.co (+ PyPI) reachable. Install Chatterbox (`pip install chatterbox-tts`, CPU torch from PyPI), clone the narrator
   Sheetal picked from `content/2026-10-31-small-starts-bogle/voice-samples/B-brooks-unedited.mp3` (first 5.4s = "This fund flopped so hard,
   the bankers wanted to give the money back."). Generate the `say` text in `build/lines.json` as one natural take (natural pace, pauses ≤1s).
   (Tried here: ZipVoice from sherpa-onnx GitHub release came out garbled. Pocket TTS / Chatterbox need Hugging Face.)
2. Split into lines by silences, rebuild `build/timeline.js` (format: [{text,start,end,words:[{w,s,e}]}], same as `mk_timeline.py` output).
3. `BOOMS="..." ./mix.sh vo.wav <DURATION> mix.m4a` (booms at: line 2 start, word 3 of line 5 "Not", line 6 start + 3.8s, word 8 of line 10 "$10").
4. Render: `NODE_PATH=$(npm root -g) node scripts/render-reel.mjs build/scene.html mix.m4a final.mp4 30` (run inside build/).
5. QA per growth/qa-checklist.md: `scripts/qa/qa_speech.py`, contact sheet, loudness -14 to -16 LUFS.
6. Caption (below), send to Sheetal for "yes", then post as a Reel (share_to_feed true) + first comment.

## Facts and sources
- Dow 36,000 (Glassman & Hassett), published fall 1999 with the Dow just above 10,000; predicted 36,000 within 3 to 5 years (Wikipedia; 247wallst "The Ghost of Dow 36,000", May 2026).
- Low 7,286.27 on 9 Oct 2002 (Dow Jones Industrial Average history).
- "perhaps the most spectacularly wrong investing book ever": The Washington Post (via 247wallst/Wikipedia).
- First close above 36,000: 36,052.63 on 2 Nov 2021 (CBS News, Fortune 1 Nov 2021).
- Glassman later: "Never associate a date with a number." (Wikipedia, citing Bloomberg Nov 2021).
- Part 3 tease: BusinessWeek "The Death of Equities", 13 Aug 1979.

## Draft Instagram caption
Did "Dow 36,000" happen? Yes or no 👇

1999: two authors publish a book saying the Dow will more than triple, to 36,000, within 3 to 5 years.
2002: it's at 7,286. The book gets called "the most spectacularly wrong investing book ever."

Watch to the end before you answer.

This is part 2 of Who Called It?, a series on famous money predictions and how they aged. Part 3: "The Death of Equities" (1979). Follow @blok.capital so you don't miss it.

A fund of your own should start at $10, not $10,000.

Did you guess right? Yes or no 👇

Educational content only, not financial or investment advice. Investing involves risk, including loss of what you put in. Past results don't predict future ones.

Sources: Glassman & Hassett, Dow 36,000 (1999); The Washington Post; Dow Jones Industrial Average closes 9 Oct 2002 and 2 Nov 2021 (CBS News); Bloomberg, Nov 2021. Chart path approximate. Scenes are dramatised; the people shown are not real. AI-generated voiceover. AI-generated imagery. Original music.

#moneyhistory #investing #personalfinance #stockmarket #financialliteracy

First comment (pin): "Yes or no: did Dow 36,000 happen? 👇 Part 3 drops next: The Death of Equities."
