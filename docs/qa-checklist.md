# Pre-publish QA checklist (standing rule, set 28 Oct 2026)

Sheetal made us **head of distribution**: nothing goes out on Instagram or X until it passes every box below,
checked like a professional editor would. Why: the 28 Oct Reel ("The first bus had one rule") went out with the voice
saying "souls" for *sols*, "lavadas" for *labourers* and "seed" for *seat*. Nobody had listened back.

Tools: `scripts/qa/` (run `bash scripts/qa/setup-models.sh` once per machine; everything runs locally, no credits).
Write the results into the piece's folder (`build/qa-speech.txt`) and summarise them in the message to Sheetal.

## 1. Voice (every Reel or video with a voiceover)
- [ ] Voice is **Kokoro `af_heart`** (natural, local, checkable) at speed 1.0 to 1.1, unless Sheetal picks another.
      Edge-tts Andrew is retired for voiceovers.
- [ ] Script lives in `build/lines.json`: `show` = on-screen words, `say` = what the voice reads. In `say`, spell out
      years ("nineteen twenty-nine"), money ("ten dollars"), and anything ambiguous. Avoid foreign words, rare
      possessives ("Raskob's" was heard as "Raskov's") and words that sound like other words (sols/souls, seat/seed).
- [ ] `python3 scripts/qa/phonemes.py build/lines.json` and read every name and uncommon word. Fix any wrong one by
      respelling it in `say`.
- [ ] After the final render: `python3 scripts/qa/qa_speech.py <final.mp4> build/lines.json build/timeline.js`.
      Every line must come back with the right words. Homophones in the transcript (B/"be", C/"see") are fine;
      a wrong, missing or cut-off word is not. Run it on the **final mp4**, not the raw voice: on 28 Oct the music mix
      swallowed the last word ("thousand") and only the final-file check caught it.
- [ ] Loudness about -14 to -16 LUFS, no clipping (`ffmpeg -i f.mp4 -af ebur128=peak=true -f null -`).

## 2. On-screen text (every frame)
- [ ] Contact sheet at 2 frames a second (`ffmpeg -i f.mp4 -vf "fps=2,scale=180:-1,tile=12x7" -frames:v 1 sheet.jpg`)
      and look at every tile: nothing overlapping, cut off, off-centre or outside y=220 to 1540.
- [ ] Full-size check of every frame with small print (sources, disclaimers, chart labels).
- [ ] Captions match the voice word for word, and quotes on screen match the real quote exactly.
- [ ] The first 2 seconds show the hook on screen (not an empty frame).
- [ ] A quiz or reveal never gives the answer away early (highlights, order, cover image).

## 3. Copy (caption, X posts, replies)
- [ ] `python3 scripts/qa/check_copy.py caption.md build/lines.json`: every X block is 280 characters or less
      (measure, don't guess), no unknown words except checked names, no rupees, no crypto words in the Instagram
      caption, risk line and "AI-generated voiceover" present, no hype words.
- [ ] Read the caption and every X post out loud once. Fix anything that reads like a press release.
- [ ] X: watchlist and playbook rules (`growth/x/`), tweet style guide, quote target under 48 hours old at posting time.

## 4. Facts and compliance
- [ ] Every number, date and quote has a primary or reputable source in the caption or first reply.
- [ ] Amounts in US dollars. Past results labelled as such; no return promises (`brand/compliance.md`).
- [ ] Instagram: no crypto vocabulary or visuals (`brand/instagram-strategy.md`).

## 5. Sign-off
- [ ] Watch and listen to the whole final file start to finish once more after the last fix.
- [ ] Send Sheetal the final media, caption, X copy and a short QA summary (what was checked, what was fixed).
      **Post only after her "yes".**
