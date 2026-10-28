"""Voiceover from lines.json (run inside build/): python3 scripts/qa/make_vo.py [voice=af_heart] [speed=1.1]
lines.json = [{"show": on-screen text, "say": what the voice reads (numbers and years spelled out), "gap": pause s}]
Writes vo.wav, vo.json (word timings for captions) and script.txt (the show text) for build-timeline.py."""
import json, sys, numpy as np, soundfile as sf, os, re
from kokoro_onnx import Kokoro
M=os.environ.get('BLOK_MODELS',os.path.expanduser('~/.cache/blok-models')); voice=sys.argv[1] if len(sys.argv)>1 else 'af_heart'; speed=float(sys.argv[2]) if len(sys.argv)>2 else 1.1
k=Kokoro(f'{M}/kokoro-v1.0.onnx',f'{M}/voices-v1.0.bin')
L=json.load(open('lines.json')); out=[]; words=[]; t=0.25; sr=24000
out.append(np.zeros(int(sr*0.25),np.float32))
for l in L:
    a,sr=k.create(l['say'],voice=voice,speed=speed,lang='en-us')
    # trim leading/trailing silence
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-480):idx[-1]+3600]
    d=len(a)/sr; ws=l['show'].split(); w=[len(re.sub(r'\W','',x))+2 for x in ws]; tot=sum(w); c=t
    for x,n in zip(ws,w):
        dd=d*n/tot; words.append({"w":x,"s":round(c,3),"e":round(c+dd,3)}); c+=dd
    out+= [a, np.zeros(int(sr*l['gap']),np.float32)]; t+=d+l['gap']
sf.write('vo.wav',np.concatenate(out),sr); json.dump(words,open('vo.json','w'))
open('script.txt','w').write('\n'.join(l['show'] for l in L)+'\n')
print(round(t,2))
