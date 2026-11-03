# What parents yell about: build notes (3 Nov 2026)

- Skill: motion-lab (github.com/codeswithroh/motion-lab) on HyperFrames 0.9.8. Composition: build/hyperframes/
  (index.template.txt + build.py fills the duration from timeline.js). Rendered 1080x1920, 30 fps, 38.5 s.
- One worked example travels the whole film: the same kid through 2000s > 2010s > 2022 > 2026, a year rail across the
  top lights each era, then the kid grows into the 2026 dad. The "?" node becomes 2045 at the end.
- Voice: Brooks (Chatterbox clone), 3 takes per line, all 30 takes transcribed word-perfect; picks in picks.json
  (line 3 uses take 2 for the pause before "Now.").
- Music: blok-morning-soil bed + low booms at 0.25 s (hook), 20.0 s (look closer), 23.5 s (the reveal), 31.2 s (2045).
- Checks: hyperframes check passed (0 errors). Remaining warnings: synced 3-word captions are on screen under 1 s each,
  kept on purpose because they follow the voice word by word.
- QA: build/qa-speech.txt on the final mp4: every line heard with the right words (CHECK lines are only "2010s" vs
  "twenty tens" number formatting). Loudness -15.7 LUFS, peak -1.5 dBFS. Contact sheet: build/contact-sheet.jpg.
- Fixed after first render: "Yelled at. Then yelling." overlapped the fading dad bubble for 0.15 s at 28.5 s.
- Weakest beat: the speech bubbles pop in empty for about 1 s while the year is read, before the scold words appear.
