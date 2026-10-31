# Reel style: "people in scenes" (Sheetal's reference, 30 Oct 2026)

Use this for every Instagram Reel from Small Starts Part 3 onwards. Source: the reference Reel Sheetal shared on
30 Oct ("the 7 biggest assets in the world", 67s). What makes it work, and how we copy it with BLOK branding.

## What the reference does
- **People in every shot.** Photoreal, period-correct scenes where people *do* the thing being said (holding gold,
  harvesting wheat, waving a bond certificate). Faces and gestures create relatability; the eye lands on a person first.
- **Minimal motion.** Locked-off camera, 4–6s per shot, the people move a little (a smile, a gesture, a turn of the head).
  No whip pans, no kinetic type, no shake. Calm visuals let the voice carry the story.
- **One recurring prop: a scoreboard.** A wooden easel chalkboard that fills up row by row as the story goes
  (numbers count up live on the board). It shows progress and keeps an open loop: "what goes in the last row?"
- **Countdown/open-loop structure.** The answer (number 1) is held to the end. Each shot pays off a small loop and opens the next.
- **Small subtitles.** White, medium weight, bottom-centre, 2–4 words at a time in sync with the voice. Key word sometimes larger.
  Nothing covers the faces.
- **Natural voice.** Conversational male narrator, about 160 words a minute, real pauses, small asides ("fun fact").
- **Data beat.** One clean dark chart slide (big "10%", a line drawing itself) as a change of pace mid-video.

## How we do it at BLOK
- **No real people's faces.** (Our rule in `brand/carousel-style.md`; it reads as an endorsement on a finance brand.)
  Use era characters who are clearly ordinary people: a 1970s banker, a young couple at a kitchen table, a trader.
  Real names appear only as text (a desk nameplate, a caption). Sheetal can override this per Reel.
- **Images:** Higgsfield `gpt_image_2_5`, 9:16, "photorealistic cinematic still, <year> <place>, <person doing action>,
  ordinary non-famous people, 35mm film look, no text". Leave boards blank and overlay the numbers in HTML.
- **Motion:** Higgsfield `kling3_0` (std, 5s, sound off, about 7.5 credits) from the still, prompt "static camera, subtle
  natural movement: …". Use it for 3–4 key shots and a slow 3% push on the rest. Check credits first.
- **Voice:** ElevenLabs through Higgsfield `text2speech_v2` (variant `elevenlabs`). Narrator Brooks
  `c2acff45-84b2-4974-892d-89fa2d4e5598`. Generate the whole script in one take (more human than line by line),
  then cut it into phrases at the pauses, tighten pauses to 0.1–0.4s and speed it up with `atempo` 1.15–1.2.
  See `content/short-form/2026-10-31-small-starts-bogle/build/build_vo.py`.
- **Brand layer:** Linen/lime/coral pills top-centre (series name, part, year), Inter subtitles, scoreboard in Earth Brown
  wood with Linen chalk, gold for the key number, linen-on-black end card with the follow CTA, yes/no question
  and risk line. Original piano bed with booms on the hook and the payoff.
- **Hook (first 1s):** start mid-action on the most surprising fact of the story, and put a short promise in the top third
  from frame 0 (e.g. "WHO BUILT IT? NAME AT THE END"). The first spoken line must already be the conflict.
- **Still applies:** no crypto words or visuals on Instagram, USD only, history-to-today angle, $10 access line,
  AI-generated voiceover + imagery disclosure, run `docs/qa-checklist.md`.
