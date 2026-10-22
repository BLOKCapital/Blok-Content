# timeline.json -> timing.json: line spans + 1-4 word caption chunks (break on punctuation, <=16 chars)
import json
tl = json.load(open('timeline.json'))
lines, caps = [], []
for L in tl:
    lines.append({'s': L['s'], 'e': L['e']})
    ws = L['words']; chunk = []
    def flush(end):
        if chunk: caps.append({'t': ' '.join(w['w'] for w in chunk), 's': chunk[0]['s'], 'e': end})
    for k, w in enumerate(ws):
        txt = ' '.join(x['w'] for x in chunk + [w])
        if chunk and (len(txt) > 16 or len(chunk) >= 4):
            flush(w['s']); chunk = []
        chunk.append(w)
        if w['w'][-1] in '.?!,' and k < len(ws) - 1:
            flush(ws[k + 1]['s']); chunk = []
    flush(L['e'] + 0.25)
# extend each caption to the next caption start (no flicker), cap gaps at 0.6s
for a, b in zip(caps, caps[1:]):
    if b['s'] - a['e'] < 0.6: a['e'] = b['s']
json.dump({'lines': lines, 'caps': caps}, open('timing.json', 'w'))
print(len(caps), 'caps; end', lines[-1]['e'])
for c in caps[:12]: print(round(c['s'],2), c['t'])
print(max(len(c['t']) for c in caps), [c['t'] for c in caps if len(c['t'])>16])
