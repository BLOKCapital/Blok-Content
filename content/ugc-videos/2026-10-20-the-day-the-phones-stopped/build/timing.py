# timeline.json -> timing.json: line start/end, per-line words, and caption chunks (2-4 words, break on punctuation)
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(f'{D}/timeline.json'))
lines, caps = [], []
for l in tl:
    ws = l['words']
    lines.append({'s': l['s'], 'e': l['e'], 'w': [[w['w'], w['s']] for w in ws]})
    cur = []
    def flush():
        if cur: caps.append({'t': ' '.join(w['w'] for w in cur), 's': cur[0]['s'], 'e': cur[-1]['e']}); cur.clear()
    for j, w in enumerate(ws):
        cur.append(w)
        txt = ' '.join(x['w'] for x in cur)
        nxt = ws[j + 1]['w'] if j + 1 < len(ws) else ''
        orphan = re.search(r'[.,?!]$', nxt) and len(nxt) <= 6 and len(txt) + len(nxt) < 27  # don't leave 'up.' alone
        if re.search(r'[.,?!]$', w['w']) or ((len(cur) >= 3 or len(txt) >= 15) and not orphan): flush()
    flush()
# hold each caption until the next one starts (max 0.6s past its end)
for a, b in zip(caps, caps[1:]): a['e'] = min(b['s'], a['e'] + 0.6)
caps[-1]['e'] += 0.6
json.dump({'lines': lines, 'caps': caps}, open(f'{D}/timing.json', 'w'))
for c in caps: print(f"{c['s']:6.2f} {c['t']}")
