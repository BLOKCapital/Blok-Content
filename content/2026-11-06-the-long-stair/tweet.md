# The long stair (ambassador applications closed, 6 Nov 2026) · X only, 16:9

Concept: Sheetal's. A long staircase, you took the first step, the climb will be exciting, we welcome you at the top to grow with us.
Message: Ambassador Program applications are closed and we are reviewing who to select.

Angle chosen: Part 2 of the ambassador story. It calls back to yesterday's miner who quit one swing away
("you didn't quit, you applied"), holds what is at the top behind clouds until the last beat, then reveals the
BLOK team holding the door open. Ends on "see you at the top" so Part 3 can be the reveal of who got in.

Video: `the-long-stair-16x9.mp4` (40.8s, 1920x1080). Cover: `cover.jpg`.
- Voice: Brooks (Chatterbox clone), 3 takes per line, best picked by speech recognition. Captions word-synced (MMS forced alignment).
- Music: our blok-morning-soil track. SFX: bundled Pixabay set (no credit needed) + footsteps.
- Art: original canvas animation (no reference art).
- QA: all 10 lines heard correctly in the final file (Whisper writes gonna as going to, not an error), -15.7 LUFS, peak -2.8 dB, frames proofread at 1 fps, top stays hidden until the reveal. Script passed an independent voice review (L4 to L10 rewritten to sound spoken).

## Post (280 chars, emoji counts as 2)

<!-- X START 0 -->
ambassador applications are closed

and honestly, you already did the hardest part. you took the first step

now we're going through every single application

we'll let you know who made it very soon

be honest, how many times have you checked your inbox today? 😭

(ai voiceover)
<!-- X END 0 -->

Rebuild: `build/` (lines.json, timeline.js, vo.wav, scene.html, mix.py, render.mjs). `node build/render.mjs build/scene.html build/mix.m4a out.mp4 30`
