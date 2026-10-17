# Britain's wooden receipts: the tally stick (seamless panorama carousel)

Scheduled: Instagram **Sun 25 Oct 2026, 18:52 IST (13:22 UTC)**, X **Mon 26 Oct 2026, 11:30 IST (06:00 UTC)**.
Requested by Sheetal on 17 Oct (a second reference post: "do the same for this one, and based on the schedule,
assign it and make sure that our brand is shown clearly. Add your own creative touches"). The Instagram link
couldn't be opened from the session, so the format follows her earlier ask: a continuation carousel where every
slide runs into the next, animated.

**Format:** one continuous 5400x1440 panorama cut into 5 slides (1080x1440). A single notched hazel stick runs across
all five slides: whole (1), splitting into stock and foil (2), burning (3), your half in pieces (4), rejoined as one
blue ledger record with a sprout growing from it (5). Instagram: 5 video slides (`video/`, 6 s each, 30 fps) with an
original track, "Hazel" (`build/make-track.py`, a Morning Soil variant with woodblock knocks for the notches),
continuous across slides. Flames, embers and the ledger glint loop every 6 s. Stills in `jpg/`.
X: 4 photos (slides 1, 2, 3, 5) per the X playbook (images that carry information); `x/pan.mp4` (21 s glide across
the panorama) is there as an alternative.
**Brand:** BLOK mark next to the slide counter on every slide; wordmark, @blok.capital and "Everyone deserves a Garden."
on slide 5; brand colours only. All art drawn in code (`build/scene.html`), no AI imagery, no third-party photos,
so no AI label is needed.

Build: `node build/render.mjs frames <dir> 30 21`, crop each 1080 px window for 6 s with the matching 6 s of
`build/hazel.m4a`; `node build/render.mjs still 1.8 <png>` for stills; `build/make-pan.sh <dir> x/pan.mp4 build/hazel.m4a`.

**Angle chosen** (from five): Britain's Exchequer kept its records on split wooden tally sticks for ~700 years, the
lender's half was the "stock", and burning the leftovers in 1834 burned down Parliament. It beat: Ben Franklin's
200-year compounding bequest (good, but a compounding/returns story is harder to keep compliant), the 1626 "$24 for
Manhattan" deal (disputed facts), the Medici double-entry ledger (less surprising) and Babylonian clay-tablet IOUs
(weak visual for a long panorama). Why it wins: one physical object can run across all five slides, the split stick
is literally "both sides hold a matching record", and it lands on BLOK's line "receipts, not reports".

## Instagram caption (between the markers, exactly)
<!-- IG START -->
For 700 years, Britain kept its money records on sticks. 🪵

If you lent money to the king, the amount was cut into a hazel stick as notches: a hand's width for £1,000, a thumb for £100, a little finger for £20, a barleycorn for £1. Then the stick was split lengthwise. The lender kept the longer half, called the stock. The borrower kept the foil. If the two halves matched, the record was true. That's where the word "stock" in finance comes from.

Tallies were scrapped in 1826. On 16 October 1834, years of leftover sticks were burned in the furnaces under the House of Lords. The fire spread and burned down most of the Palace of Westminster.

Today the full record of your money lives in your fund's and broker's books. You get a summary, once a month or quarter.

A public ledger brings back the matching half: every holding and trade recorded in the open, in an account only you control, so you can check it yourself any time. Receipts, not reports.

Swipe slowly, it's one long stick 👉

Would you rather have the stick or the statement? 👇

Educational content only, not financial or investment advice. On-chain assets can be volatile and you can lose money. Learn first, start small.

Sources: Science Museum Group, "Medieval Exchequer Tally Sticks" (tallies used 12th to 19th century; stock and foil; abolished 1826; fire of 16 Oct 1834). Notch sizes from the Dialogue of the Exchequer (c. 1180). Music: original track. Illustrations drawn by BLOK.
<!-- IG END -->

## X post (between the markers, exactly) — attach jpg/slide-01, 02, 03, 05 in that order
<!-- X START -->
for 700 years britain's receipts were made of wood

lend the king money and they notched it into a stick, then split it in half

your half was called the stock

if the halves matched, the record was true

today you get a pdf once a quarter. which is the better receipt?
<!-- X END -->

## X self-reply
<!-- XR START -->
in 1834 they burned the old sticks under the House of Lords. the fire took most of Parliament with it

a public ledger is the modern version: both sides hold the matching record and you can check it any time. still new tech, so start small

source: https://collection.sciencemuseumgroup.org.uk/objects/co60506
<!-- XR END -->
