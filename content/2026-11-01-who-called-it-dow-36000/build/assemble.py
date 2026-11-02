# usage: assemble.py lines.json takesdir outdir   -> outdir/vo.wav, outdir/timeline.js, outdir/picks.json
import sys, json, os, difflib, numpy as np, soundfile as sf, torch, torchaudio, librosa
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from common import norm
L=json.load(open(sys.argv[1])); TD=sys.argv[2]; OD=sys.argv[3]
sc=json.load(open(TD+'/scores.json'))
picks=json.load(open(TD+'/picks.json')) if os.path.exists(TD+'/picks.json') else {}
SR=24000; LEAD=0.25
def trim(a):
    i=librosa.effects.trim(a,top_db=38,frame_length=512,hop_length=128)[1]
    s=max(0,i[0]-int(.03*SR)); e=min(len(a),i[1]+int(.08*SR)); b=a[s:e].copy()
    f=int(.01*SR); b[:f]*=np.linspace(0,1,f); b[-f*3:]*=np.linspace(1,0,f*3); return b
from torchaudio.pipelines import MMS_FA as B
fa=B.get_model(); dic=B.get_dict(); aligner=B.get_aligner(); tok=B.get_tokenizer()
out=[]; T=[]; t=LEAD; out.append(np.zeros(int(LEAD*SR),np.float32))
for i,l in enumerate(L):
    cands=[(v['ratio'],-v['maxpause'],k) for k,v in sc.items() if v['line']==i]
    p=picks.get(str(i)) or max(cands)[2]; picks[str(i)]=p
    a,sr=sf.read(p,dtype='float32'); assert sr==SR; a=trim(a)
    # forced alignment on say words
    sw=[w.replace("'","") for w in norm(l['say'])]
    wav=torch.tensor(librosa.resample(a,orig_sr=SR,target_sr=16000))[None]
    with torch.inference_mode(): em,_=fa(wav)
    spans=aligner(em[0],tok(sw)); r=wav.shape[1]/em.shape[1]/16000
    st=[(s[0].start*r, s[-1].end*r) for s in spans]
    # map show words -> say tokens
    show=l['show'].split(); toks=[]; own=[]
    for j,w in enumerate(show):
        for x in norm(w): toks.append(x.replace("'","")); own.append(j)
    ws=[[None,None] for _ in show]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,toks,sw,autojunk=False).get_opcodes():
        if op=='equal' or (op=='replace' and i2-i1>0):
            for k in range(i1,i2):
                jj=min(j1+(k-i1),j2-1) if op=='equal' else j1+int((k-i1)*(j2-j1)/(i2-i1))
                o=own[k]; s,e=st[jj]
                ws[o][0]=s if ws[o][0] is None else min(ws[o][0],s); ws[o][1]=e if ws[o][1] is None else max(ws[o][1],e)
    # fill words with no spoken tokens (e.g. punctuation-only) from neighbours
    for j in range(len(ws)):
        if ws[j][0] is None:
            prev=next((ws[k][1] for k in range(j-1,-1,-1) if ws[k][1] is not None),0.0); ws[j]=[prev,prev+0.05]
    words=[{"w":w,"s":round(t+s,3),"e":round(t+e,3)} for w,(s,e) in zip(show,ws)]
    dur=len(a)/SR
    T.append({"text":l['show'],"start":round(t,3),"end":round(t+dur,3),"words":words})
    out.append(a); t+=dur
    g=l['gap'] if i<len(L)-1 else 0
    out.append(np.zeros(int(g*SR),np.float32)); t+=g
v=np.concatenate(out); os.makedirs(OD,exist_ok=True)
sf.write(OD+'/vo.wav',v,SR)
open(OD+'/timeline.js','w').write('window.TIMELINE = '+json.dumps(T)+';')
json.dump(picks,open(OD+'/picks.json','w'),indent=1)
print('total',round(len(v)/SR,2)); [print(i,x['start'],x['end'],picks[str(i)]) for i,x in enumerate(T)]
