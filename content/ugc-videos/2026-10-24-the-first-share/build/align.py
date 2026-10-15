# Align script lines to whisper word timings -> timeline.json (line start/end + word list)
import json, re, sys, difflib
d = sys.argv[1]
lines = [l.split('|')[0] for l in open(f'{d}/script.txt') if l.strip()]
words = json.load(open(f'{d}/vo.json'))
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
st = []  # script tokens with line index
for i, l in enumerate(lines):
    for t in l.replace('-', ' ').split():
        st.append((norm(t), i))
wt = [norm(w['w']) for w in words]
sm = difflib.SequenceMatcher(None, [t for t, _ in st], wt, autojunk=False)
line_of_word = [None] * len(words)
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        line_of_word[b + k] = st[a + k][1]
# fill gaps forward
cur = 0
for j in range(len(words)):
    if line_of_word[j] is None: line_of_word[j] = cur
    cur = line_of_word[j]
out = []
for i in range(len(lines)):
    ws = [w for w, li in zip(words, line_of_word) if li == i]
    out.append({'i': i, 'text': lines[i], 's': ws[0]['s'], 'e': ws[-1]['e'], 'words': ws})
json.dump(out, open(f'{d}/timeline.json', 'w'), indent=0)
for o in out: print(f"{o['i']:2d} {o['s']:6.2f}-{o['e']:6.2f} {o['text'][:50]}")
