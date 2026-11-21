# QA · reel #9 (S4 Countdown + H2 You-POV) · predict-v1.mp4

- Length 43.6 s (target 30 to 36 s: about 8 s over, accepted; three countdown beats need their own scenes). 1080x1920, 30 fps, h264 ~10 Mbps, AAC.
- Loudness -15.2 LUFS integrated (target -14 to -16). Music bed at 0.38.
- Speech check (qa_speech.py on the final mp4): 7 of 8 lines OK. Line 1 flagged only because Whisper writes "nineteen hundred" as "1900" (number formatting). Line 8 (CTA) scored 0.93: Whisper dropped "Comment FUND" at the start of its segment; it's the same CTA take used in reels #3 to #8, and voice level at that point matches reel #7 (-17.0 dB voice, -18.6 dB mix), so the words are there.
- Contact sheet at 1 fps (sheet-v1.jpg): hook phone on screen from frame 0, #3/#2/#1 cards and countdown dots, no overlaps, no photos, no faces.
- Caption: sources listed, risk line, "AI-generated voiceover", no crypto words, under 2,200 characters. US dollars only, no fee attacks, no competitors named.
- On-screen footer on the CTA scene: risk line + AI voiceover + quote source.
- Verdict: PASS.
