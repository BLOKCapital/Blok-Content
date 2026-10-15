# Forced alignment without ASR: split script words across speech segments (between pauses) by DP,
# then spread word times inside each segment by character weight -> vo.json
import json, re, sys, wave
d = sys.argv[1] if len(sys.argv) > 1 else '.'
lines = [l.split('|')[0] for l in open(f'{d}/script.txt') if l.strip()]
words = []
for i, l in enumerate(lines):
    for t in l.split(): words.append((t, i))
w = wave.open(f'{d}/vo.wav'); dur = w.getnframes() / w.getframerate()
sil = [tuple(map(float, l.split())) for l in open(f'{d}/sil.txt') if l.strip()]
segs, cur = [], 0.0
for a, b in sil:
    if a - cur > 0.08: segs.append((cur, a))
    cur = b
if dur - cur > 0.08: segs.append((cur, dur))
spoken = lambda t: len(re.sub(r'[^A-Za-z0-9]', '', t.replace('1602', 'sixteen oh two').replace('1606', 'sixteen oh six'))) + 1.5
W, K = len(words), len(segs)
wt = [spoken(t) for t, _ in words]
pre = [0]
for x in wt: pre.append(pre[-1] + x)
rate = sum(e - s for s, e in segs) / pre[-1]
def endp(j):  # bonus if word j-1 ends a sentence / line
    t, li = words[j - 1]
    if j == W or words[j][1] != li: return -0.6
    return -0.35 if t[-1] in '.?!,' else 0.4
INF = 1e18
dp = [[INF] * (W + 1) for _ in range(K + 1)]; bk = [[0] * (W + 1) for _ in range(K + 1)]
dp[0][0] = 0
for k in range(1, K + 1):
    sd = segs[k - 1][1] - segs[k - 1][0]
    for j in range(1, W + 1):
        best, bi = INF, 0
        for i in range(max(0, j - 25), j):
            if dp[k - 1][i] >= INF: continue
            est = (pre[j] - pre[i]) * rate
            c = dp[k - 1][i] + ((sd - est) / max(0.3, sd)) ** 2 + endp(j)
            if c < best: best, bi = c, i
        dp[k][j], bk[k][j] = best, bi
j, assign = W, []
for k in range(K, 0, -1):
    i = bk[k][j]; assign.append((k - 1, i, j)); j = i
assign.reverse()
out = []
for k, i, j in assign:
    s, e = segs[k]; tot = pre[j] - pre[i]; t = s
    for m in range(i, j):
        dt = (e - s) * wt[m] / tot
        out.append({'w': words[m][0], 's': round(t, 3), 'e': round(t + dt, 3)}); t += dt
    print(f"{s:6.2f}-{e:6.2f} {' '.join(x[0] for x in words[i:j])}")
json.dump(out, open(f'{d}/vo.json', 'w'))
