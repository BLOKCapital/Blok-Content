#!/usr/bin/env python3
"""Build the X topic desk page from the radar data and the day's picks.

Reads  data/YYYY-MM-DD.json        (x-topic-radar.py output)
       data/YYYY-MM-DD-picks.json  (written by the daily run, shape in README.md; optional)
Writes desk.html (latest) and archive/YYYY-MM-DD.html. Stdlib only, no CDN (page is self-contained).
Usage: python3 build-desk.py [YYYY-MM-DD]
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def latest_date():
    days = sorted(os.path.basename(p)[:10] for p in glob.glob(os.path.join(HERE, "data", "20??-??-??.json")))
    if not days:
        sys.exit("no radar data yet: run x-topic-radar.py first")
    return days[-1]


def main():
    day = sys.argv[1] if len(sys.argv) > 1 else latest_date()
    radar = json.load(open(os.path.join(HERE, "data", f"{day}.json")))
    pp = os.path.join(HERE, "data", f"{day}-picks.json")
    picks = json.load(open(pp)) if os.path.exists(pp) else None
    payload = json.dumps({"day": day, "radar": radar, "picks": picks}).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload).replace("__DAY__", day)
    os.makedirs(os.path.join(HERE, "archive"), exist_ok=True)
    for path in (os.path.join(HERE, "desk.html"), os.path.join(HERE, "archive", f"{day}.html")):
        open(path, "w").write(html)
    print("wrote desk.html and archive/%s.html (%s picks)" % (day, len(picks["picks"]) if picks else "no"))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>X Topic Desk</title>
<style>
:root{--paper:#F6F3E8;--card:#fff;--ink:#1d2433;--muted:#5f6675;--line:#e3dfd2;--indigo:#004EBA;--sky:#7DD2FD;--lime:#7ED116;--coral:#EC464D;--brown:#844947;--amber:#E8A317}
@media (prefers-color-scheme:dark){:root{--paper:#14171f;--card:#1d212c;--ink:#eef0f4;--muted:#a3a9b6;--line:#2e3442;--indigo:#7DD2FD}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:20px 16px 60px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:34px 0 10px}h3{font-size:16px;margin:0 0 6px}
.muted{color:var(--muted)}.small{font-size:13px}
.hero{background:var(--indigo);color:#fff;border-radius:16px;padding:20px}
.hero .t{font-size:22px;font-weight:700;margin:6px 0}
.hero .muted{color:#dbe8ff}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
.step{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px}
.step b{display:block}.tag{display:inline-block;font-size:11px;font-weight:700;border-radius:20px;padding:1px 8px;margin-top:4px}
.free{background:#e5f6cf;color:#2f5a00}.paid{background:#fde1e2;color:#9b1c22}.hand{background:#ddeeff;color:#003b8c}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:14px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:760px){.row{grid-template-columns:1fr}}
.score{display:grid;grid-template-columns:70px 1fr 24px;gap:6px;align-items:center;font-size:13px}
.bar{height:9px;border-radius:5px;background:var(--line);overflow:hidden}.bar i{display:block;height:100%;background:var(--lime)}
.draft{white-space:pre-wrap;background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px;font-size:14px}
.btn{cursor:pointer;border:1px solid var(--indigo);color:var(--indigo);background:transparent;border-radius:8px;padding:3px 10px;font-size:12px;font-weight:600}
.btn:hover{background:var(--indigo);color:#fff}
.pill{display:inline-block;border-radius:20px;padding:1px 9px;font-size:12px;font-weight:600;border:1px solid var(--line);margin-right:4px}
.ok{color:#2f7a00}.warn{color:#b26a00}.bad{color:var(--coral)}
main-table-fix{}
.card{overflow-x:auto}table{width:100%;min-width:520px;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:7px 6px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}.tabs button{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:20px;padding:5px 12px;cursor:pointer}
.tabs button.on{background:var(--indigo);color:#fff;border-color:var(--indigo)}
.hb{display:inline-block;height:8px;background:var(--sky);border-radius:4px;vertical-align:middle}
a{color:var(--indigo)}
.chips span{display:inline-block;font-size:12px;border-radius:6px;padding:2px 7px;margin:2px;background:var(--card);border:1px solid var(--line)}
.chips .f{border-color:var(--lime)}.chips .s{opacity:.55;text-decoration:line-through}
.big{font-size:28px;font-weight:700}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}
</style></head><body><div class="wrap">
<div class="hero"><div class="muted small">X topic desk · __DAY__ · <span id="runat"></span></div>
<div class="t" id="tod">No picks written yet today</div><div id="why" class="muted"></div></div>

<h2>How the day works</h2>
<div class="flow">
<div class="step"><b>1. Radar</b><span class="small muted">watchlist feeds, crypto + finance news, Hacker News, Google Trends</span><br><span class="tag free">free, automatic</span></div>
<div class="step"><b>2. Score</b><span class="small muted">heat, bridge, take, safety, talk (18+ of 25)</span><br><span class="tag free">automatic</span></div>
<div class="step"><b>3. Pick one topic</b><span class="small muted">plus two backups</span><br><span class="tag free">automatic</span></div>
<div class="step"><b>4. Four shots</b><span class="small muted">quote, original, 10 to 15 replies, our own reply thread</span><br><span class="tag hand">Sheetal's ok, then post</span></div>
<div class="step"><b>5. Stay 2 hours</b><span class="small muted">answer every reply, mutuals first</span><br><span class="tag hand">by hand</span></div>
<div class="step"><b>6. Learn</b><span class="small muted">log the link in posted.json, next morning shows what won</span><br><span class="tag free">automatic</span></div>
</div>

<h2>Today's picks</h2><div id="picks"></div>

<h2>Reply targets <span class="small muted">(where new people already are; best under 6 hours old, hand-posted)</span></h2>
<div class="card"><table id="replies"></table></div>

<h2>Radar</h2>
<div class="tabs" id="rtabs"></div><div class="card" id="radar"></div>

<h2>What's working for us <span class="small muted">(our posts in posted.json, likes and replies)</span></h2>
<div class="kpis" id="kpis"></div><div class="card" id="own" style="margin-top:10px"></div>

<h2>Skipped today and why</h2><div class="card" id="skipped"></div>

<h2>Source health</h2>
<div class="card"><div class="small muted">Green = fresh free feed. Struck through = the free feed is stuck weeks old for that account (needs the paid radar or a hand check).</div><div class="chips" id="health"></div></div>

<h2>Needs X API credit</h2><div class="card" id="credit"></div>
<p class="small muted">Rules behind this page: growth/x/x-algorithm-playbook.md, tweet-style-guide.md, trend-playbook.md, qa-checklist.md, brand/compliance.md. Nothing posts without Sheetal's ok.</p>
</div>
<script>
const D=__DATA__;const R=D.radar,P=D.picks;
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const ageH=iso=>(Date.now()-new Date(iso))/36e5;
const fmtAge=h=>h<1?Math.round(h*60)+"m":h<48?h.toFixed(1)+"h":Math.round(h/24)+"d";
const xlen=s=>String(s).replace(/https?:\/\/\S+/g,"x".repeat(23)).length;
function windowNote(iso){if(!iso)return"";const h=ageH(iso),left=48-h;
 if(h<=2)return`<span class="ok">quote window best now (${fmtAge(h)} old)</span>`;
 if(left>0)return`<span class="warn">${fmtAge(h)} old, window closes in ${fmtAge(left)}</span>`;
 return`<span class="bad">${fmtAge(h)} old, past 48h: don't quote, pick another post</span>`}
function copyBtn(t){return`<button class="btn" data-copy="${esc(t)}">copy</button>`}
document.addEventListener("click",e=>{const b=e.target.closest("[data-copy]");if(!b)return;
 navigator.clipboard?.writeText(b.dataset.copy).then(()=>{b.textContent="copied";setTimeout(()=>b.textContent="copy",1200)})});
$("runat").textContent="radar run "+(R.run_at||"").replace("T"," ")+" UTC";
if(P){$("tod").textContent=P.topic_of_day;$("why").textContent=P.why||"";}
// picks
const dims=["heat","bridge","take","safety","talk"];
$("picks").innerHTML=!P?'<div class="card muted">No picks file for today yet. The morning run writes data/YYYY-MM-DD-picks.json.</div>':P.picks.map(p=>{
 const tot=dims.reduce((a,k)=>a+(p.scores[k]||0),0);
 const sc=dims.map(k=>`<div class="score"><span>${k}</span><div class="bar"><i style="width:${p.scores[k]*20}%"></i></div><b>${p.scores[k]}</b></div>`).join("");
 const q=p.quote?`<h3>A. Quote post ${copyBtn(p.quote.draft+"\n\n"+p.quote.target_url)}</h3>
  <div class="small"><a href="${esc(p.quote.target_url)}" target="_blank">open the post</a> · ${windowNote(p.quote.target_created)}</div>
  <div class="small muted">${esc(p.quote.target_note)}</div><div class="draft">${esc(p.quote.draft)}</div>
  <div class="small muted">${xlen(p.quote.draft)+24} / 280 with the quote link</div>`:"";
 const o=p.original?`<h3>B. Original, ${esc(p.original.slot)} ${copyBtn(p.original.draft)}</h3>
  <div class="small muted">hook: ${esc(p.original.hook_type)}</div><div class="draft">${esc(p.original.draft)}</div>
  <div class="small muted">${xlen(p.original.draft)} / 280</div>
  <div class="small" style="margin-top:6px"><b>First reply</b> ${copyBtn(p.original.first_reply)}</div><div class="draft small">${esc(p.original.first_reply)}</div>`:"";
 return`<div class="card"><div class="row"><div>
  <span class="pill">#${p.rank}</span><span class="pill">${esc(p.lane)}</span><span class="pill">${esc(p.temp)}</span>
  <h3 style="margin-top:8px">${esc(p.title)}</h3>
  <div class="small"><a href="${esc(p.trend_url)}" target="_blank">trend</a> · ${esc(p.heat_note)}</div>
  <p class="small"><b>Bridge:</b> ${esc(p.bridge)}<br><b>Remix:</b> ${esc(p.remix)}</p>
  ${sc}<div class="small" style="margin-top:4px"><b>${tot} / 25</b> ${tot>=18&&p.scores.safety>=4?'<span class="ok">keep</span>':'<span class="bad">below the bar</span>'}</div>
  ${(p.news_hooks||[]).length?`<div class="small" style="margin-top:8px"><b>News this rides</b>${p.news_hooks.map(n=>`<div>• <a href="${esc(n.url)}" target="_blank">${esc(n.title)}</a> <span class="muted">${esc(n.source)}, ${esc(n.date)}</span></div>`).join("")}</div>`:""}
  ${(p.flags||[]).length?`<p class="small warn">${p.flags.map(esc).join("<br>")}</p>`:""}
 </div><div>${q}${o}</div></div></div>`}).join("");
// replies
const rt=P?.reply_targets||[];
$("replies").innerHTML=`<tr><th>Post</th><th>Age</th><th>Followers</th><th>Draft reply</th><th></th></tr>`+(rt.length?rt.map(r=>`<tr>
 <td><a href="${esc(r.url)}" target="_blank">@${esc(r.handle)}</a><div class="muted">${esc(r.note)}</div></td>
 <td>${r.created?fmtAge(ageH(r.created)):""}</td><td>${(r.followers||0).toLocaleString()}</td>
 <td style="min-width:220px">${esc(r.draft)}<div class="muted">${xlen(r.draft)} chars</div></td><td>${copyBtn(r.draft)}</td></tr>`).join(""):'<tr><td colspan="5" class="muted">No reply drafts today.</td></tr>');
// radar tabs
const tabs={"Hot on X, last 48h":"x","Quote now (under 2h)":"q","Crypto + finance news":"nw","Hacker News":"hn","Google Trends":"gt"};
let cur="x";
$("rtabs").innerHTML=Object.entries(tabs).map(([k,v])=>`<button data-t="${v}">${k}</button>`).join("");
$("rtabs").onclick=e=>{const t=e.target.dataset.t;if(t){cur=t;drawRadar()}};
function xTable(rows){if(!rows.length)return'<p class="muted">Nothing here on this run.</p>';const mx=Math.max(...rows.map(r=>r.heat),1);
 return`<table><tr><th>Heat / h</th><th>Age now</th><th>Account</th><th>Post</th><th>Replies</th><th>Quotes</th></tr>`+rows.map(r=>`<tr>
 <td><span class="hb" style="width:${Math.max(4,r.heat/mx*90)}px"></span> ${r.heat}</td><td>${fmtAge(ageH(r.created))}</td>
 <td>@${esc(r.handle)}<div class="muted">${esc(r.lane)}</div></td><td><a href="${esc(r.url)}" target="_blank">${esc(r.text.slice(0,140))}</a></td>
 <td>${r.replies}</td><td>${r.quotes}</td></tr>`).join("")+"</table>"}
function drawRadar(){[...$("rtabs").children].forEach(b=>b.classList.toggle("on",b.dataset.t===cur));let h="";
 if(cur==="x")h=xTable(R.hot_48h||[]);
 if(cur==="q")h=xTable(R.quote_now||[]);
 if(cur==="nw"){const N=R.news||{items:[]};const l=N.items.filter(x=>!x.unsafe);
  h=`<div class="small muted">Last 48h from ${Object.keys(N.feeds||{}).length} feeds. Price and hack headlines are hidden. <b>ours</b> = touches funds, tokenization, access, custody or Arbitrum. Google News items can be old stories re-posted: check the date on the primary source.</div><table><tr><th>Age</th><th>Feed</th><th>Headline</th></tr>`+l.slice(0,40).map(x=>`<tr><td>${x.age_h==null?"":fmtAge(x.age_h)}</td><td>${esc(x.feed)}${x.ours?' <span class="pill ok">ours</span>':''}</td><td><a href="${esc(x.url)}" target="_blank">${esc(x.title)}</a></td></tr>`).join("")+"</table>"}
 if(cur==="hn"){const l=Array.isArray(R.hacker_news)?R.hacker_news:[];h=`<table><tr><th>Points</th><th>Comments</th><th>Age at run</th><th>Story</th></tr>`+l.slice(0,25).map(x=>`<tr><td>${x.points}</td><td>${x.comments}</td><td>${fmtAge(x.age_h)}</td><td><a href="${esc(x.hn)}" target="_blank">${esc(x.title)}</a></td></tr>`).join("")+"</table>"}
 if(cur==="gt"){h=Object.entries(R.google_trends||{}).map(([g,l])=>`<h3>${g}</h3><table>`+(Array.isArray(l)?l:[]).slice(0,10).map(x=>`<tr><td style="width:30%">${esc(x.term)}</td><td style="width:12%">${esc(x.traffic)}</td><td><a href="${esc(x.news_url)}" target="_blank">${esc(x.news)}</a></td></tr>`).join("")+"</table>").join("")}
 $("radar").innerHTML=h}
drawRadar();
// own posts
const own=(R.own_posts||[]).filter(o=>!o.error);
const byType={};own.forEach(o=>{(byType[o.type]=byType[o.type]||[]).push(o.replies)});
const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
$("kpis").innerHTML=Object.keys(byType).length?Object.entries(byType).sort((a,b)=>avg(b[1])-avg(a[1])).map(([t,a])=>`<div class="kpi"><div class="small muted">${esc(t)} posts (${a.length})</div><div class="big">${avg(a).toFixed(1)}</div><div class="small muted">replies per post</div></div>`).join(""):'<div class="kpi muted">Add post links to posted.json to see this.</div>';
const mxr=Math.max(1,...own.map(o=>o.replies));
$("own").innerHTML=own.length?`<table><tr><th>Post</th><th>Type</th><th>Replies</th><th>Likes</th></tr>`+own.map(o=>`<tr><td><a href="${esc(o.url)}" target="_blank">${esc(o.topic)}</a><div class="muted">${esc(o.date)} · ${esc(o.format)}</div></td><td>${esc(o.type)}</td><td><span class="hb" style="width:${o.replies/mxr*120}px;background:var(--lime)"></span> ${o.replies}</td><td>${o.likes}</td></tr>`).join("")+"</table>":'<p class="muted">No posts logged yet.</p>';
// skipped, health, credit
$("skipped").innerHTML=(P?.skipped||[]).map(s=>`<div class="small"><b>${esc(s.what)}</b>: ${esc(s.why)}</div>`).join("")||'<span class="muted">Nothing logged.</span>';
$("health").innerHTML=(R.source_health||[]).map(h=>`<span class="${h.error?'s':h.stale?'s':'f'}" title="${esc(h.error||('newest post '+fmtAge(h.newest_age_h||0)+' old at run'))}">@${esc(h.handle)}</span>`).join("");
$("credit").innerHTML=(P?.needs_credit||["Views, bookmarks, keyword search, mentions"]).map(x=>`<div class="small">• ${esc(x)}</div>`).join("")+'<div class="small muted" style="margin-top:6px">Fix: top up billing for the @blok_cap app in the X Developer Portal. Everything above still runs without it.</div>';
</script></body></html>"""

if __name__ == "__main__":
    main()
