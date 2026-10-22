# timeline.json -> timing.json: line start/end + words, and short caption chunks (2-4 words,
# break after punctuation, <= 18 characters) for the lower-third captions.
import json, os
D = os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(f'{D}/timeline.json'))
lines, caps = [], []
for k, l in enumerate(tl):
    ws = l['words']
    lines.append({'s': l['s'], 'e': l['e'], 'words': [{'w': w['w'], 's': w['s'], 'e': w['e']} for w in ws]})
    chunk = []
    def flush():
        if chunk: caps.append({'t': ' '.join(w['w'] for w in chunk), 's': chunk[0]['s'], 'e': chunk[-1]['e']})
    for w in ws:
        txt = ' '.join(x['w'] for x in chunk + [w])
        if chunk and (len(txt) > 18 or len(chunk) >= 4):
            flush(); chunk = []
        chunk.append(w)
        if w['w'][-1:] in '.,?!;:':
            flush(); chunk = []
    flush()
# merge very short chunks into the next one
i = 0
while i < len(caps) - 1:
    if caps[i + 1]['s'] - caps[i]['s'] < 0.4 and caps[i]['t'][-1:] not in '.?!' and len(caps[i]['t'] + caps[i + 1]['t']) <= 22:
        caps[i + 1] = {'t': caps[i]['t'] + ' ' + caps[i + 1]['t'], 's': caps[i]['s'], 'e': caps[i + 1]['e']}; del caps[i]
    else: i += 1
# Whisper spellings -> how we want them on screen
FIX = [(' ,000', ',000'), (' -chain', '-chain'), ('128 pounds', '£128.'), ('124', '£124.'), ('20,000', '£20,000.'),
       ('lost 20', 'lost £20'), ('Shhh', 'Shh'), ('Now,', 'Now?'), ('closer to 10,', 'closer to ten.'), ('10,', 'ten.'),
       ('June 1720,', 'June, 1720.'), ('London, June', 'London. June'), ('Okay,', 'Okay.'), ('stock,', 'stock.'), ('the South Sea', 'The South Sea'),
       ('still a', 'Still, a'), ('Newton,', 'Newton.')]
for c in caps:
    for a, b in FIX: c['t'] = c['t'].replace(a, b)
    c['t'] = c['t'].replace('£124. pounds.', '£124.').replace('£20,000. pounds.', '£20,000.').replace('.. ', '. ').rstrip()
    c['t'] = c['t'].replace('..', '.')
# drop chunks that were only 'pounds.' (the figure already says £) and let the previous one run on
caps = [c for c in caps if c['t'] != 'pounds.']
# each caption stays until the next one starts (max +0.6s), so they don't flicker
for a, b in zip(caps, caps[1:]): a['e'] = min(b['s'], a['e'] + 0.6)
caps[-1]['e'] += 0.8
json.dump({'lines': lines, 'caps': caps}, open(f'{D}/timing.json', 'w'))
for c in caps: print(f"{c['s']:6.2f} {c['t']}")
