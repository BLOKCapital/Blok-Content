# placeholder timing (2.7 words/s) until the real voice is assembled
import json
L=json.load(open('lines.json')); t=.25; T=[]
for i,l in enumerate(L):
    ws=l['show'].split(); d=len(ws)/2.7; words=[]
    for j,w in enumerate(ws): words.append({"w":w,"s":round(t+j*d/len(ws),3),"e":round(t+(j+1)*d/len(ws),3)})
    T.append({"text":l['show'],"start":round(t,3),"end":round(t+d,3),"words":words}); t+=d+l['gap']
open('timeline.js','w').write('window.TIMELINE = '+json.dumps(T)+';'); print(round(t,2))
