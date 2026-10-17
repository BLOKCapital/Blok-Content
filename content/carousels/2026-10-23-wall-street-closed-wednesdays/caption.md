# Wall Street closed every Wednesday (seamless panorama carousel)

Scheduled: Instagram **Fri 23 Oct 2026, 10:00 IST (04:30 UTC)**, X **Fri 23 Oct 2026, 17:45 IST (12:15 UTC)**.
Requested by Sheetal on 17 Oct ("this type of content … schedule it for 23rd October or so for both Twitter and Instagram").

**Format:** one continuous 5400x1440 panorama cut into 5 slides (1080x1440), so every slide runs into the next.
The ticker tape, the pile of share certificates, the scissors and the timeline all cross the slide edges.
Instagram: 5 video slides (`video/`, 6 s each, 30 fps) carrying an original track, "Ticker Tape"
(`build/make-track.py`, a variant of Morning Soil, mastered with the playbook chain), continuous across slides.
Everything that crosses a slide edge loops every 6 s, so the last frame of one slide meets the first frame of the next.
Stills in `jpg/`. X: one 21 s video (`x/pan.mp4`) that glides across the whole panorama.
All visuals are drawn in code (`build/scene.html`), no AI imagery and no third-party photos, so no AI label is needed.

Build: `node build/render.mjs still 6 <out.png>` for the stills, `node build/render.mjs frames <dir> 30 6` for the loop,
then crop each 1080 px window with ffmpeg (commands in the thread log); `build/make-pan.sh` for the X video.

**Angle chosen** (from five): "Wall Street shut every Wednesday in 1968, for paperwork." It beat Keynes-style
predictions (already used), the 1602 first share (Reel on 24 Oct), NYSE closing for 4 months in 1914 (too close to
the "money keeps office hours" theme) and the ticker-tape parade origin (weak link to today). It is surprising, it is a
literal paper trail, so it suits a panorama, and it lands on settlement time today: one business day, and seconds on a public ledger.

## Instagram caption (between the markers, exactly)
<!-- IG START -->
In 1968, Wall Street closed every Wednesday. Not for a holiday. For paperwork. 📄

Trading had exploded, and every trade still meant a paper certificate that someone typed, signed and carried across town. Back offices fell so far behind that, at the worst point, about $4 billion of shares were late reaching their new owners. So from June to December 1968, the New York Stock Exchange shut one day a week to catch up.

Since then we've been cutting off days, slowly: settling a trade took 5 business days, then 3 (1995), then 2 (2017). Since May 2024, US stock trades settle the next business day. Fund payouts still often take 1 to 3 days.

On a public ledger, the record of who owns what updates in seconds, in an account only you control, and you can check it yourself instead of waiting for a statement.

The catch: it's newer tech, prices can swing, so learn first and start small. The ledger entry on slide 5 is an illustration, not a real trade.

Swipe slowly, it's one long picture 👉

Would you have guessed this happened in 1968? 👇

Sources: NYSE Wednesday closures, June to Dec 1968, during the "paperwork crisis", and ~$4B of shares undelivered at the 1968 peak (Fisher Investments, "The Paper Crunch"; NYSE historical schedules). US settlement moved from 5 to 3 business days (1995), 2 (2017) and 1 (May 2024, SEC). As of Oct 2026. Music: original track.
<!-- IG END -->

## X post (between the markers, exactly)
<!-- X START -->
in 1968 wall street closed every wednesday

not for a holiday. for paperwork

every trade was a paper certificate carried across town. at one point ~$4B of shares were late to their owners

58 years later, "sold" still isn't "paid" the same day

how long should a trade take?
<!-- X END -->

## X self-reply
<!-- XR START -->
settling a trade took 5 business days, then 3 (1995), 2 (2017), 1 (2024)

on a public ledger the record updates in seconds and you can check it yourself. newer tech and prices swing, so start small

sources: fisher investments "the paper crunch", SEC
<!-- XR END -->
