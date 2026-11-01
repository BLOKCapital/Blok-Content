"""Cut the single ElevenLabs take into phrases and write vo.wav, vo.json, script.txt.
python3 build_vo.py [tempo] [natural]
natural (what Sheetal picked on 31 Oct): keep the take's own pauses (capped at 1s) and its own speed (tempo 1).
Otherwise the pauses are tightened to the gaps in L and the take is sped up by tempo."""
import json, sys, re, subprocess, numpy as np, soundfile as sf
T=float(sys.argv[1]) if len(sys.argv)>1 else 1.15
NAT='natural' in sys.argv
segs=json.load(open('segs.json'))
a,sr=sf.read('vo_raw.wav'); a=a.mean(1) if a.ndim>1 else a
# lines: (show text per segment, inner gaps between segments, gap after line)
L=[ (["This fund flopped so hard,","the bankers wanted to give the money back."],[0.12],0.25),
    (["The goal?","$150 million."],[0.18],0.22),
    (["It raised...","$11 million."],[0.5],0.3),
    (["Wall Street called it a folly."],[],0.15),
    (["Critics called it","un-American."],[0.04],0.3),
    (["Its founder had two words."],[],0.35),
    (["Hell no."],[],0.4),
    (["The first index fund for everyday investors."],[],0.3),
    (["And today?","That same fund holds over $1.7 trillion."],[0.25],0.4),
    (["His name was Jack Bogle."],[],0.35),
    (["Every big fund started small.","Yours can start","at $10."],[0.2,0.03],0.4),
    (["Small Starts,","part 3.","Next:","the gift that waited","200 years."],[0.06,0.25,0.1,0.03],0.0)]
SAY={'$150':'ahundredandfifty','$11':'eleven','$1.7':'onepointseven','$10':'tendollars','200':'twohundred','3':'three','un-American':'unamerican'}
# phrases re-recorded on their own because the long take slurred them (index into segs.json)
FIX={6:'fix_wallstreet.wav'}
flat=[s for l in L for s in l[0]]; assert len(flat)==len(segs),(len(flat),len(segs))
out=[np.zeros(int(sr*0.08))]; t=0.08; words=[]; k=0
for shows,inner,gap in L:
    for j,sh in enumerate(shows):
        s,e,_=segs[k]; k+=1
        x=a[max(0,int((s-0.04)*sr)):int((e+0.06)*sr)]
        if k-1 in FIX: x,_=sf.read(FIX[k-1]); x=np.concatenate([np.zeros(int(sr*0.04)),x,np.zeros(int(sr*0.06))])
        d=len(x)/sr; ws=sh.split(); w=[len(SAY.get(q.strip('.,?:'),re.sub(r'\W','',q)))+2 for q in ws]; tot=sum(w); c=t+0.04
        for q,n in zip(ws,w):
            dd=(d-0.1)*n/tot; words.append({"w":q,"s":c,"e":c+dd}); c+=dd
        g=inner[j] if j<len(inner) else gap
        if NAT: g=min(1.0,max(0.15,(segs[k][0]-e-0.1) if k<len(segs) else 0.0))
        out+=[x,np.zeros(int(sr*g))]; t+=d+g
sf.write('vo_cut.wav',np.concatenate(out),sr)
subprocess.run(['ffmpeg','-v','error','-y','-i','vo_cut.wav','-af',f'atempo={T}','vo.wav'],check=True)
for w in words: w['s']=round(w['s']/T,3); w['e']=round(w['e']/T,3)
json.dump(words,open('vo.json','w'))
open('script.txt','w').write('\n'.join(' '.join(l[0]) for l in L)+'\n')
print(round(t/T,2))
