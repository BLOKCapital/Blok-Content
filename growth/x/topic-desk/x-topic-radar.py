#!/usr/bin/env python3
"""Free X topic radar for @blok_cap (no X API credits needed).

Reads the public profile timelines X serves to embedded widgets
(syndication.twitter.com), plus Hacker News and Google Trends, and writes
growth/x/topic-desk/data/YYYY-MM-DD.json with:
  - fresh posts from the watchlist, ranked by heat (X ranking weights per hour of age)
  - "quote now" (under 2h) and "reply targets" (under 6h, big reply sections)
  - our own last posts with the same metrics (feedback loop)
  - crypto / Web3 and finance news (CoinDesk, The Block, Decrypt, Cointelegraph, Blockworks, The Defiant,
    DL News, Unchained, Bankless, FT Markets, Google News searches on our themes), last 48h
  - Hacker News front page and Google Trends (US, IN, GB) as off-X signals
Run: python3 x-topic-radar.py   (stdlib only; ~1 minute)
Limits: no views or bookmarks (the widget feed doesn't carry them), max ~20 latest posts
per account, and a few accounts come back cached/stale; the script flags those.
"""
import datetime as dt, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (compatible; content-radar/1.0)"}
NOW = dt.datetime.now(dt.timezone.utc)

# Lane -> accounts. Source: growth/x/watchlist/watchlist.md + growth/trends/trend-radar.py. Edit freely.
LANES = {
    "arbitrum": ["arbitrum", "aave", "pendle_fi", "GMX_IO", "Offchain", "ArbitrumDevs"],
    "tokenized funds": ["centrifuge", "Securitize", "tokenterminal", "RWA_xyz", "plumenetwork", "chainlink", "maplefinance", "tomwanhh"],
    "tradfi x on-chain": ["RobinhoodApp", "vladtenev", "EricBalchunas", "JSeyff", "NateGeraci", "Matt_Hougan", "BlackRock"],
    "defi voices": ["nic_carter", "DefiIgnas", "TheDeFinvestor", "thedefiedge", "Route2FI", "Bankless", "TrustlessState", "DefiLlama"],
    "personal finance": ["morganhousel", "awealthofcs", "BrianFeroldi", "ritholtz", "charliebilello", "TheStalwart", "unusual_whales"],
    "ai + builders": ["sama", "paulg", "naval", "levelsio"],
    "voice models": ["galileowilson", "FoxyhitsW", "milesdeutscher"],
}
OWN = "blok_cap"
# Words that make a post unsafe to ride (compliance: price talk, leverage, giveaways, politics, tragedy).
UNSAFE = re.compile(r"\b(airdrop|giveaway|liquidat\w*|leverage|100x|moon|pump|price target|apy|apr|election|trump|biden|war|killed|dead|lawsuit|hack(ed)?|exploit\w*|scam|price|prediction|breakout|rally|plunge\w*|crash\w*|surge\w*|drops?|falls?|bull market|bear market)\b", re.I)


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def parse_time(s):
    return dt.datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")


def heat(t, age_h):
    # X weights: reply 5, quote 5, repost 1, like 0.5 (copy-link and bookmarks aren't public here)
    pts = 5 * (t["replies"] + t["quotes"]) + t["reposts"] + 0.5 * t["likes"]
    return round(pts / max(age_h, 1.0), 1), pts


def timeline(handle):
    try:
        h = get(f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}")
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', h, re.S)
        entries = json.loads(m.group(1))["props"]["pageProps"]["timeline"]["entries"]
    except Exception as e:  # network, rate limit, renamed account
        return handle, {"error": str(e)[:120]}
    posts = []
    for e in entries:
        t = e.get("content", {}).get("tweet")
        if not t or t.get("full_text", "").startswith("RT @"):
            continue
        created = parse_time(t["created_at"])
        u = t.get("user", {})
        posts.append({
            "id": t["id_str"], "url": "https://x.com" + t.get("permalink", f"/{handle}/status/{t['id_str']}"),
            "created": created.isoformat(), "age_h": round((NOW - created).total_seconds() / 3600, 1),
            "text": re.sub(r"\s+", " ", t["full_text"]).replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")[:280],
            "likes": t.get("favorite_count", 0), "replies": t.get("reply_count", 0),
            "reposts": t.get("retweet_count", 0), "quotes": t.get("quote_count", 0),
            "is_reply": bool(t.get("in_reply_to_status_id_str")),
            "followers": u.get("followers_count", 0),
        })
    posts.sort(key=lambda p: p["created"], reverse=True)
    newest = posts[0]["age_h"] if posts else None
    return handle, {"posts": posts, "newest_age_h": newest,
                    "followers": posts[0]["followers"] if posts else 0,
                    "stale": newest is None or newest > 24 * 4}


def tweet_token(tid):
    # Same token the official embed script computes: ((id / 1e15) * pi) in base 36, zeros and dot removed.
    x, digits, out = (int(tid) / 1e15) * 3.141592653589793, "0123456789abcdefghijklmnopqrstuvwxyz", ""
    ip, fp = int(x), x - int(x)
    while ip:
        out = digits[ip % 36] + out
        ip //= 36
    out = (out or "0") + "."
    for _ in range(11):
        fp *= 36
        out += digits[int(fp)]
        fp -= int(fp)
    return re.sub(r"(0+|\.)", "", out)


def own_posts():
    """Metrics for our own posts listed in posted.json (the feedback loop). Free, one call per post."""
    try:
        log = json.load(open(os.path.join(HERE, "posted.json")))
    except Exception:
        return []
    out = []
    for row in log[-30:]:
        tid = re.search(r"status/(\d+)", row.get("url", ""))
        if not tid:
            continue
        tid = tid.group(1)
        try:
            t = json.loads(get(f"https://cdn.syndication.twimg.com/tweet-result?id={tid}&lang=en&token={tweet_token(tid)}"))
        except Exception as e:
            out.append({**row, "error": str(e)[:80]})
            continue
        created = dt.datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
        out.append({**row, "likes": t.get("favorite_count", 0), "replies": t.get("conversation_count", 0),
                    "age_h": round((NOW - created).total_seconds() / 3600, 1), "created": created.isoformat(),
                    "text": re.sub(r"\s+", " ", t.get("text", ""))[:200]})
        time.sleep(0.3)
    return out


# Crypto / Web3 and finance news (Sheetal, 15 Nov: every pick should carry a fresh headline so people see we follow the news).
NEWS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "The Block": "https://www.theblock.co/rss.xml",
    "Decrypt": "https://decrypt.co/feed",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "Blockworks": "https://blockworks.co/feed",
    "The Defiant": "https://thedefiant.io/feed",
    "DL News": "https://www.dlnews.com/arc/outboundfeeds/rss/",
    "Unchained": "https://unchainedcrypto.com/feed/",
    "Bankless": "https://www.bankless.com/rss/feed",
    "FT Markets": "https://www.ft.com/markets?format=rss",
}
GNEWS = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q="
NEWS_SEARCHES = {
    "tokenized funds": "tokenized fund OR tokenization fund when:2d",
    "fund access": "(\"minimum investment\" OR \"retail investors\" OR \"accredited investor\") fund when:2d",
    "arbitrum": "arbitrum when:3d",
    "on-chain finance": "(onchain OR on-chain) (ETF OR fund OR asset manager) when:2d",
}
# Words that make a story ours (bridge to access / owning your fund / receipts / Arbitrum).
OURS = re.compile(r"\b(tokeni[sz]\w*|rwa|real[- ]world asset\w*|fund\w*|etf\w*|index|minimum\w*|retail|accredited|self[- ]custody|custod\w*|asset manager\w*|blackrock|arbitrum|stablecoin\w*|on-?chain|wealth|portfolio\w*)\b", re.I)


def parse_rss(xml_text, source):
    out = []
    root = ET.fromstring(xml_text)
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = it.findtext("pubDate") or ""
        try:
            when = dt.datetime.strptime(pub[:25].strip(), "%a, %d %b %Y %H:%M:%S").replace(tzinfo=dt.timezone.utc)
            age = round((NOW - when).total_seconds() / 3600, 1)
        except Exception:
            age = None
        src = it.findtext("source") or source
        out.append({"title": title, "url": link, "source": src, "age_h": age})
    return out


def news():
    jobs = list(NEWS_FEEDS.items()) + [(f"Google News: {k}", GNEWS + urllib.parse.quote(q)) for k, q in NEWS_SEARCHES.items()]
    items, health = [], {}
    for name, url in jobs:
        try:
            got = parse_rss(get(url), name)
            health[name] = len(got)
        except Exception as e:
            health[name] = "error: " + str(e)[:60]
            continue
        for x in got:
            if x["age_h"] is not None and x["age_h"] > 48:
                continue
            x["feed"] = name
            x["ours"] = bool(OURS.search(x["title"]))
            x["unsafe"] = bool(UNSAFE.search(x["title"]))
            items.append(x)
    seen, uniq = set(), []
    for x in sorted(items, key=lambda x: (not x["ours"], x["age_h"] if x["age_h"] is not None else 99)):
        key = re.sub(r"\W+", " ", x["title"].lower())[:60]
        if key not in seen:
            seen.add(key)
            uniq.append(x)
    return {"items": uniq[:80], "feeds": health}


def hacker_news():
    try:
        d = json.loads(get("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"))
    except Exception as e:
        return {"error": str(e)[:120]}
    out = []
    for x in d["hits"]:
        age = (NOW - dt.datetime.fromtimestamp(x["created_at_i"], dt.timezone.utc)).total_seconds() / 3600
        out.append({"title": x["title"], "points": x.get("points", 0), "comments": x.get("num_comments", 0),
                    "age_h": round(age, 1), "url": x.get("url") or f"https://news.ycombinator.com/item?id={x['objectID']}",
                    "hn": f"https://news.ycombinator.com/item?id={x['objectID']}"})
    return sorted(out, key=lambda x: -x["points"])


def google_trends(geo):
    try:
        root = ET.fromstring(get(f"https://trends.google.com/trending/rss?geo={geo}"))
    except Exception as e:
        return {"error": str(e)[:120]}
    ns = {"ht": "https://trends.google.com/trending/rss"}
    out = []
    for it in root.iter("item"):
        news = it.find("ht:news_item", ns)
        out.append({"term": it.findtext("title"), "traffic": it.findtext("ht:approx_traffic", namespaces=ns),
                    "news": news.findtext("ht:news_item_title", namespaces=ns) if news is not None else "",
                    "news_url": news.findtext("ht:news_item_url", namespaces=ns) if news is not None else ""})
    return out


HEALTH = os.path.join(HERE, "data", "source-health.json")
MAX_CALLS = 28  # the widget feed rate-limits at roughly 30 to 40 calls per ~15 minutes


def load_health():
    try:
        return json.load(open(HEALTH))
    except Exception:
        return {}


def main():
    handles = [(lane, h) for lane, hs in LANES.items() for h in hs]
    lane_of = {h: lane for lane, h in handles}
    known = load_health()
    # Skip accounts whose widget feed was stale on a check in the last 7 days (re-check weekly).
    def skip(h):
        k = known.get(h)
        return k and k.get("stale") and (NOW - dt.datetime.fromisoformat(k["checked"])).days < 7
    todo = [(l, h) for l, h in handles if not skip(h)][:MAX_CALLS]
    results = {}
    for lane, h in todo:
        h, r = timeline(h)
        results[h] = r
        if "429" in str(r.get("error", "")):
            print("rate limited after", len(results), "calls; stopping X reads (run again in ~15 min)")
            break
        time.sleep(0.6)
    for h, r in results.items():
        if not r.get("error"):
            known[h] = {"stale": r["stale"], "newest_age_h": r["newest_age_h"], "checked": NOW.isoformat()}
    os.makedirs(os.path.dirname(HEALTH), exist_ok=True)
    json.dump(known, open(HEALTH, "w"), indent=1)

    fresh, health = [], []
    for h, r in results.items():
        health.append({"handle": h, "lane": lane_of.get(h, "?"), "error": r.get("error"),
                       "newest_age_h": r.get("newest_age_h"), "stale": r.get("stale"), "followers": r.get("followers")})
        if h == OWN or "posts" not in r:
            continue
        for p in r["posts"]:
            if p["age_h"] > 48 or p["is_reply"]:
                continue  # over 48h it has left For You
            p["heat"], p["points"] = heat(p, p["age_h"])
            p["handle"], p["lane"] = h, lane_of.get(h, "?")
            p["unsafe"] = bool(UNSAFE.search(p["text"]))
            fresh.append(p)
    fresh.sort(key=lambda p: -p["heat"])
    safe = [p for p in fresh if not p["unsafe"]]

    own = own_posts()

    data = {
        "run_at": NOW.isoformat(timespec="minutes"),
        "quote_now": [p for p in safe if p["age_h"] <= 2][:10],
        "reply_targets": sorted([p for p in safe if p["age_h"] <= 6 and p["followers"] >= 10_000],
                                key=lambda p: -(p["replies"] / max(p["age_h"], 0.5)))[:15],
        "hot_48h": safe[:30],
        "skipped_unsafe": [p for p in fresh if p["unsafe"]][:10],
        "own_posts": own,
        "news": news(),
        "hacker_news": hacker_news(),
        "google_trends": {g: google_trends(g) for g in ("US", "IN", "GB")},
        "source_health": health,
    }
    out_dir = os.path.join(HERE, "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, NOW.strftime("%Y-%m-%d") + ".json")
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
    bad = [x["handle"] for x in health if x["error"] or x["stale"]]
    print(f"wrote {path}")
    print(f"{len(fresh)} watchlist posts under 48h ({len(safe)} safe), {len(data['quote_now'])} under 2h, "
          f"{len(data['reply_targets'])} reply targets, {len(own)} own posts")
    nw = data["news"]["items"]
    print(f"{len(nw)} news items under 48h, {sum(x['ours'] for x in nw)} on our themes")
    for x in [x for x in nw if x["ours"] and not x["unsafe"]][:10]:
        print(f"  news {x['age_h']}h  {x['feed']}: {x['title'][:100]}")
    print("stale or failed accounts:", ", ".join(bad) or "none")
    for p in data["hot_48h"][:12]:
        print(f"  {p['heat']:>7} heat  {p['age_h']:>5}h  @{p['handle']:<15} r{p['replies']} q{p['quotes']}  {p['text'][:90]}")


if __name__ == "__main__":
    main()
