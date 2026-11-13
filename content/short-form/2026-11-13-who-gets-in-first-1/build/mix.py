# python3 mix.py -> mix-v.m4a (VO + music bed + sfx)
import json, subprocess, re
T=json.loads(open('timeline.js').read().split('=',1)[1].rstrip(';\n'))
S=lambda i:T[i]['start']; E=lambda i:T[i]['end']
D=E(len(T)-1)+0.6+2.6
SCENE=[0,0,1,2,2,3,4,5,6,0,7]
def word(i,rx):
    for w in T[i]['words']:
        if re.match(rx,w['w'],re.I): return w['s']
    return S(i)
ev=[('sfx/boom.wav',0.05,.8)]
t=0.3
while t<S(2)-0.4: ev.append(('sfx/tick.wav',t,.35)); t+=0.5
for i in range(1,len(T)):
    if SCENE[i]!=SCENE[i-1]: ev.append(('sfx/whoosh.wav',S(i)-0.45,.45))
ev+=[('sfx/thud.wav',word(1,'53'),.6),('sfx/boom.wav',word(2,'biggest'),.5),('sfx/thud.wav',word(4,'guarantee'),.6),
     ('sfx/thud.wav',word(5,'still'),.5),('sfx/boom.wav',word(7,'building'),.45),('sfx/thud.wav',word(8,r'\$10'),.55),('sfx/thud.wav',word(10,'FUND'),.55)]
cmd=['ffmpeg','-y','-v','error','-i','vo.wav','-stream_loop','3','-i','/home/user/Blok-Content/assets/music/blok-morning-soil.m4a']
for f,_,_ in ev: cmd+=['-i',f]
fc=f"[0:a]apad=pad_dur=4,aresample=44100,aformat=channel_layouts=stereo,asplit[v][sc];[1:a]aresample=44100,atrim=0:{D},afade=t=in:d=1,afade=t=out:st={D-2}:d=2,volume=0.22[m0];[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m];"
ins='[v][m]'
for j,(f,t,g) in enumerate(ev):
    ms=max(0,int(t*1000)); fc+=f"[{j+2}:a]aresample=44100,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[e{j}];"; ins+=f"[e{j}]"
fc+=f"{ins}amix=inputs={len(ev)+2}:duration=longest:normalize=0,atrim=0:{D},loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.8:level=false[out]"
cmd+=['-filter_complex',fc,'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix-v.m4a']
subprocess.run(cmd,check=True); print('dur',round(D,2))
