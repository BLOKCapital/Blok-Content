# Trend radar for growth/trend-playbook.md.
# Runs INSIDE COMPOSIO_REMOTE_WORKBENCH (it uses the workbench's run_composio_tool helper and the
# connected @blok_cap X account). Paste this file as code_to_execute, or curl it from GitHub raw and exec() it.
# Prints the hottest posts of the last ~24h per lane, ranked by heat = weighted engagement per hour,
# using the X ranking weights (quote/reply 5, bookmark 3 as a copy-link proxy, repost 1, like 0.5).
import datetime

HOURS = 24          # look-back window
TOP_PER_LANE = 6    # rows printed per lane
MIN_VIEWS = 5_000   # keyword lanes only (drops story-farm accounts); watchlist accounts are always kept

# Watchlist: big accounts whose posts set the day's conversation in each lane.
# Edit freely; keep each query under ~480 characters.
WATCHLIST = {
    "markets + macro": ["unusual_whales", "KobeissiLetter", "WatcherGuru", "charliebilello", "TheStalwart"],
    "personal finance": ["morganhousel", "awealthofcs", "BrianFeroldi", "ritholtz"],
    "india investing": ["nithin0dha", "deepakshenoy", "NikhilKamathCIO"],
    "ai + builders": ["sama", "paulg", "naval", "levelsio"],
    "on-chain + tokenization": ["rwa_xyz", "tokenterminal"],
}

# Keyword lanes catch posts from accounts that aren't on the watchlist yet.
KEYWORDS = {
    "cost of living": '("can\'t afford" OR "cost of living" OR "american dream" OR rent OR "house prices") (money OR salary OR income)',
    "funds + minimums": '("minimum investment" OR "index fund" OR "mutual fund" OR "hedge fund" OR "private equity" OR "accredited investor")',
    "ai + jobs + money": '(AI OR "artificial intelligence") (jobs OR layoffs OR salary OR retire OR "work week")',
    "tokenization": '(tokenized OR tokenization OR "on-chain fund" OR "real-world assets")',
}

now = datetime.datetime.now(datetime.timezone.utc)
start = (now - datetime.timedelta(hours=HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")


def search(query):
    r, e = run_composio_tool("TWITTER_RECENT_SEARCH", {
        "query": query + " -is:retweet -is:reply lang:en",
        "max_results": 100, "start_time": start,
        "tweet_fields": ["created_at", "public_metrics"],
        "expansions": ["author_id"], "user_fields": ["public_metrics", "username"],
    })
    if e:
        print("  search failed:", e)
        return []
    d = r.get("data", {})
    users = {u["id"]: u for u in d.get("includes", {}).get("users", [])}
    rows = []
    for t in d.get("data", []) or []:
        m = t["public_metrics"]
        u = users.get(t["author_id"], {})
        age = (now - datetime.datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))).total_seconds() / 3600
        score = 5 * (m["quote_count"] + m["reply_count"]) + 3 * m.get("bookmark_count", 0) + m["retweet_count"] + 0.5 * m["like_count"]
        rows.append({
            "heat": score / max(age, 1), "age": age, "user": u.get("username", "?"),
            "followers": u.get("public_metrics", {}).get("followers_count", 0),
            "views": m.get("impression_count", 0), "quotes": m["quote_count"], "replies": m["reply_count"],
            "url": f"https://x.com/{u.get('username', 'i')}/status/{t['id']}",
            "text": t["text"].replace("\n", " ")[:220],
        })
    return sorted(rows, key=lambda x: -x["heat"])


def show(lane, rows):
    print(f"\n## {lane}")
    for x in rows[:TOP_PER_LANE]:
        print(f"- heat {x['heat']:.0f} | {x['age']:.1f}h | @{x['user']} ({x['followers']:,}) | "
              f"{x['views']:,} views, {x['quotes']} quotes, {x['replies']} replies | {x['url']}\n  {x['text']}")


print(f"# Trend radar {now:%Y-%m-%d %H:%M} UTC (last {HOURS}h)")
for lane, accounts in WATCHLIST.items():
    show(lane, search("(" + " OR ".join("from:" + a for a in accounts) + ")"))
for lane, q in KEYWORDS.items():
    show(lane, [x for x in search(q) if x["views"] >= MIN_VIEWS])
