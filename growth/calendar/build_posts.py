# Builds growth/calendar/posts.json: the single list behind the calendar page and posting-plan.md.
import json, datetime as dt
IST = dt.timedelta(hours=5, minutes=30)
P = []
def add(utc, platform, fmt, title, status, link="", source="", owner="", note=""):
    u = dt.datetime.fromisoformat(utc)
    i = u + IST
    P.append(dict(id=f"{u:%Y%m%d-%H%M}-{platform[:2]}-{len(P):03d}", date=f"{i:%Y-%m-%d}", time=f"{i:%H:%M}",
                  utc=f"{u:%Y-%m-%dT%H:%MZ}", platform=platform, format=fmt, title=title, status=status,
                  link=link, source=source, owner=owner, note=note))
IG, X = "instagram", "x"
# ---- already live (pulled from Instagram and X on 15 Oct 22:05 UTC)
for utc, fmt, title, link in [
 ("2026-10-09T09:57","Carousel","You can see your fund's statement. But can you see your fund?","https://www.instagram.com/p/DeRPQiKlSQk/"),
 ("2026-10-09T12:31","Reel","POV: your money keeps office hours","https://www.instagram.com/reel/DeRg7VKCVkc/"),
 ("2026-10-09T13:04","Carousel","Who actually holds your money?","https://www.instagram.com/p/DeRkuV5IFAu/"),
 ("2026-10-10T05:35","Carousel","What is a public ledger, really?","https://www.instagram.com/p/DeTWE4cldnO/"),
 ("2026-10-10T14:38","Carousel","\"Sold\" doesn't mean \"paid\"","https://www.instagram.com/p/DeUUQEeiBdd/"),
 ("2026-10-11T11:58","Reel","Receipts beat reports","https://www.instagram.com/reel/DeWmtrykZR6/"),
 ("2026-10-12T14:43","Reel","The night a bank vanished","https://www.instagram.com/reel/DeZeaBpnefg/"),
 ("2026-10-13T07:57","Carousel","my new money rules","https://www.instagram.com/p/DebUwWUEuBQ/"),
 ("2026-10-13T11:13","Carousel","Wall Street's $114 trillion vault","https://www.instagram.com/p/DebrKQXCOR9/"),
 ("2026-10-14T10:17","Carousel","Up to $10 trillion on-chain by 2030","https://www.instagram.com/p/DeeJiH3DYBG/"),
 ("2026-10-14T13:25","Carousel","Your fund's 1% fee isn't small","https://www.instagram.com/p/DeefHPsD5__/"),
 ("2026-10-15T04:21","Reel","-A checked your \"diversified\" portfolio","https://www.instagram.com/reel/DegFnRWF7Hd/"),
 ("2026-10-15T10:02","Carousel","how to invest your money (for dummies)","https://www.instagram.com/p/Degso5njbuk/"),
]: add(utc, IG, fmt, title, "posted", link)
for utc, fmt, title, sid in [
 ("2026-10-09T08:39","Post","imagine needing permission to move your own money","2108477423901966764"),
 ("2026-10-10T06:02","Post","gm fam, happy saturday","2108800248307191870"),
 ("2026-10-10T14:17","Post","china banning bitcoin every other cycle","2108924982525112604"),
 ("2026-10-11T12:02","Video post","old money says trust the report","2109253181717000642"),
 ("2026-10-12T14:50","Video post","9 March 2023: $42 billion in one day (SVB)","2109657944996601920"),
 ("2026-10-13T08:18","Post","CFTC Chair: \"Not your keys, not your coins\"","2109921581598228991"),
 ("2026-10-13T11:14","Video post","Wall Street's $114 trillion vault","2109965892050108652"),
 ("2026-10-13T14:39","Photo post","$10,000. 30 years. 7% a year. (fee card)","2110017570044608991"),
 ("2026-10-14T10:17","Video post","Morgan Stanley: $3T to $10T by 2030","2110314084537188597"),
 ("2026-10-14T14:38","Video post","$42B tried to leave one bank: DO / DON'T","2110379819376542103"),
 ("2026-10-14T17:30","Video post","Founder Space promo ($40B → $10T)","2110423001304846386"),
 ("2026-10-15T06:01","Video post","3 money myths fund investors still believe","2110612037755703500"),
 ("2026-10-15T12:18","Photo post","how to invest your money (for dummies)","2110706755944546496"),
 ("2026-10-15T14:31","Video post","-A checked your \"diversified\" portfolio","2110740327841624352"),
]: add(utc, X, fmt, title, "posted", f"https://x.com/blok_cap/status/{sid}",
       note="Overlaps a little with the 3 money myths post the same morning (both use the 3-funds line)." if sid=="2110740327841624352" else "")
# ---- already scheduled by other threads (scheduled tasks exist)
S = "scheduled"
add("2026-10-16T04:30",IG,"Reel","They called it un-American (Bogle's folly, 1976)",S,source="content/2026-10-16-bogles-folly/",owner="Buffett index thread")
add("2026-10-16T06:00",X,"Video post","Anatomy of a public ledger",S,source="content/2026-10-14-anatomy-of-blockchain/",owner="Anatomy thread")
add("2026-10-16T10:00",IG,"Carousel","On-chain finance is 5 old ideas",S,source="content/2026-10-15-five-old-ideas/",owner="On-chain finance carousel thread",note="Comment GARDEN CTA; replies run every 3 hours.")
add("2026-10-16T12:15",X,"Photo post","Bogle's folly (4 photos)",S,source="content/2026-10-16-bogles-folly/",owner="Buffett index thread")
add("2026-10-16T13:22",IG,"Reel","Anatomy of a public ledger",S,source="content/2026-10-14-anatomy-of-blockchain/reel/",owner="IG growth daily run")
add("2026-10-16T14:30",X,"Photo post","1792: 24 brokers under a buttonwood tree (4 photos)",S,source="content/2026-10-17-buttonwood-tree/",owner="Buffett index thread")
add("2026-10-17T04:30",IG,"Reel","24 men and a tree (Buttonwood, 1792)",S,source="content/2026-10-17-buttonwood-tree/",owner="Buffett index thread")
add("2026-10-17T06:00",X,"Photo post","The know-nothing investor (3 photos)",S,source="content/2026-10-17-know-nothing-investor/",owner="Buffett index thread")
add("2026-10-17T10:00",IG,"Reel","The know-nothing investor (Buffett, 1993)",S,source="content/2026-10-17-know-nothing-investor/",owner="Buffett index thread")
add("2026-10-17T12:15",X,"Photo post","The first index fund had 1 customer (3 photos)",S,source="content/2026-10-18-one-customer/",owner="Buffett index thread")
add("2026-10-17T13:22",IG,"Carousel","5 questions to ask about any investment","needs-asset",owner="IG growth daily run",note="Not made yet. The daily run makes it on the day if it isn't ready.")
add("2026-10-18T04:30",IG,"Reel","The first index fund had one customer (1971)",S,source="content/2026-10-18-one-customer/",owner="Buffett index thread")
add("2026-10-18T13:22",IG,"Story","Weekend recap + question sticker",S,owner="IG growth daily run")
# ---- scheduled by this thread
T = "Content calendar thread"
add("2026-10-17T14:30",X,"Post","greentext: the quarterly pdf",S,source="growth/calendar/x-copy.md#X1",owner=T)
add("2026-10-18T06:00",X,"Video post","keynes predicted a 15-hour week",S,source="growth/calendar/x-copy.md#X2",owner=T)
add("2026-10-18T10:00",IG,"Carousel","3 money myths fund investors still believe",S,source="content/carousels/2026-10-15-three-money-myths/ (branch claude/project-thread-abccxj)",owner=T,note="Myths 1 and 2 echo the diversified Reel and the fee carousel; it runs as a Sunday save-it recap.")
add("2026-10-18T12:15",X,"Photo post","5 old ideas your grandma used",S,source="growth/calendar/x-copy.md#X3",owner=T)
add("2026-10-18T14:30",X,"Post","be honest, when did you last open your fund's statement?",S,source="growth/calendar/x-copy.md#X4",owner=T)
add("2026-10-19T06:00",X,"Video post","your portfolio got riskier and you didn't touch it",S,source="growth/calendar/x-copy.md#X5",owner=T)
add("2026-10-19T13:22",IG,"Reel","Your portfolio got riskier (rebalancing whiteboard)",S,source="content/2026-10-14-rebalancing-whiteboard/",owner=T,note="Caption line fixed to 'closer to 70/30' (one good year can't take 60/40 to 75/25).")
add("2026-10-19T14:30",X,"Post","broker: \"your sale went through\" (translation)",S,source="growth/calendar/x-copy.md#X6",owner=T)
add("2026-10-20T06:00",X,"Post","where your money goes when you hit buy",S,source="growth/calendar/x-copy.md#X7",owner=T)
add("2026-10-20T14:30",X,"Post","what we expect vs what actually happens",S,source="growth/calendar/x-copy.md#X8",owner=T)
add("2026-10-21T06:00",X,"Post","a public ledger, explained without the jargon",S,source="growth/calendar/x-copy.md#X9",owner=T)
# ---- Keynes trial reels: Sheetal posts by hand, one every two days
order = [("v2-wrong-worker","He just picked the wrong worker"),("v4-3am","It's 3 a.m. Do you know what your money is doing?"),
         ("v6-32-of-168","Your money works 32 hours a week"),("v7-ai-took-my-emails","AI took my emails"),
         ("v3-saturdays","Wall Street worked Saturdays until 1952"),("v5-waits-for-monday","Your money has a 9-to-5"),
         ("v1-prediction","Keynes predicted a 15-hour week (control)")]
d0 = dt.datetime(2026,10,16,15,0)
for k,(f,h) in enumerate(order):
    d = d0 + dt.timedelta(days=2*k)
    r = d + dt.timedelta(days=1)
    add(f"{d:%Y-%m-%dT%H:%M}",IG,"Trial reel",f"Keynes trial {k+1}/7: {h}","by-hand",
        source=f"content/2026-10-15-trial-reels-keynes/{f}.mp4",owner="Sheetal (Instagram app)",
        note=f"Post as Trial, Share manually, AI label on. Read skip rate at 24h ({r:%a %d %b}) and 48h, before the next one.")
add("2026-10-30T13:22",IG,"Reel","Keynes promised me: winning hook as a normal Reel","needs-asset",
    source="content/2026-10-15-trial-reels-keynes/",owner=T,note="Lowest skip rate across the 7 trials wins. Can move earlier if one hook is clearly ahead after 4.")
# ---- open slots from Mon 19: IG 1 feed post a day at 18:52 IST, X 2 a day
taken = {(p["utc"]) for p in P}
day = dt.date(2026,10,19)
while day <= dt.date(2026,10,31):
    for hhmm, plat in [("13:22",IG),("06:00",X),("14:30",X)]:
        u = f"{day:%Y-%m-%d}T{hhmm}"
        if u+"Z" not in taken:
            add(u, plat, "Open slot", "Open: needs a new piece", "open")
    day += dt.timedelta(days=1)
# ---- on the shelf
for title, src, note in [
 ("-A texted me (fee version)","content/2026-10-14-a-texted-me/","First draft of the -A Reel; the diversified version went out instead. Fee topic already posted 3 times."),
 ("Your fund's 1% fee isn't small (Reel, two cuts)","content/2026-10-12-the-one-percent-fee/","Same maths as the 14 Oct fee carousel and the 13 Oct X fee card. Hold for a month."),
 ("Anatomy of a public ledger (carousel cut)","content/2026-10-14-anatomy-of-blockchain/","Backup of the 16 Oct Reel."),
]:
    P.append(dict(id="shelf-"+src.split('/')[1], date="", time="", utc="", platform=IG, format="Held", title=title,
                  status="held", link="", source=src, owner="", note=note))
P.sort(key=lambda p: (p["utc"] or "9999", p["platform"]))
json.dump(P, open("/mnt/project-files/growth/calendar/posts.json","w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(P), Counter(p["status"] for p in P))
