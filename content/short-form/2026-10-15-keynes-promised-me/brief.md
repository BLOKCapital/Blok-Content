# Keynes promised me a 15-hour week (Reel, ~65s)

**Reference:** @base.learn reel DeYtpsNT5sb ("Claude, did I push the API key to GitHub?"), 56s, 1080x1920.
Format we copied: low-poly 3D man in a blue-violet suit sitting on a giant keyboard at night, a small orange
low-poly bot beside him; ping-pong close-ups (one shot per line), occasional wide shots; panicking human,
deadpan bot answering in short dry lines; absurd escalation, one soft beat, callback punchline. No music.

**Angle chosen:** Keynes (1930) predicted a 15-hour work week by ~2030. AI took the man's tasks but not his
hours; his *money* got the short week (stock markets ≈ 6.5 h × 5 days ≈ 32 h of 168). On-chain markets run 24/7.
Callback: it's 3 a.m., he has a meeting at nine, about Claude.

**Facts used:** Keynes, "Economic Possibilities for our Grandchildren" (1930): "three-hour shifts or a fifteen-hour week".
NYSE 9:30–16:00 ET Mon–Fri = 6.5 h/day. No return claims.

**Build (no paid credits):** voices = Kokoro (am_michael for the man, bm_george for the bot), `build/make_voice.py`;
scene = three.js (copy `node_modules/three/build/three.module.js` r169 into build/) low-poly set rendered frame by frame with Playwright (`build/scene.html`, `build/render.mjs`).
`node render.mjs preview 1,5,9` for stills; `node render.mjs full out.mp4 30` for the video.
