# python3 mix.py -> mix-v.m4a (VO + music bed + sfx)
import json, subprocess, re
T=json.loads(open('timeline.js').read().split('=',1)[1].rstrip(';\n'))
S=lambda i:T[i]['start']; E=lambda i:T[i]['end']
D=E(len(T)-1)+0.6+2.6
def word(i,rx):
    for w in T[i]['words']:
        if re.match(rx,w['w'],re.I): return w['s']
    return S(i)
ev=[('sfx/boom.wav',0.05,.8),('sfx/thud.wav',word(0,'disaster'),.6),('sfx/whoosh.wav',S(1)-0.4,.4),('sfx/thud.wav',word(1,'small'),.5),
    ('sfx/whoosh.wav',S(2)-0.4,.4),('sfx/boom.wav',word(2,'ended'),.5),('sfx/thud.wav',word(2,'150'),.5),('sfx/whoosh.wav',S(3)-0.4,.5),
    ('sfx/thud.wav',word(3,'stop'),.6),('sfx/whoosh.wav',S(4)-0.4,.4),('sfx/whoosh.wav',S(5)-0.4,.4),('sfx/boom.wav',word(5,'97'),.55),
    ('sfx/whoosh.wav',S(6)-0.4,.4),('sfx/whoosh.wav',S(7)-0.4,.4),('sfx/whoosh.wav',S(8)-0.4,.4)]
cmd=['ffmpeg','-y','-v','error','-i','vo.wav','-stream_loop','3','-i','/home/user/Blok-Content/assets/music/blok-morning-soil.m4a']
for f,_,_ in ev: cmd+=['-i',f]
fc=f"[0:a]apad=pad_dur=4,aresample=44100,aformat=channel_layouts=stereo,asplit[v][sc];[1:a]aresample=44100,atrim=0:{D},afade=t=in:d=1,afade=t=out:st={D-2}:d=2,volume=0.2[m0];[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m];"
ins='[v][m]'
for j,(f,t,g) in enumerate(ev):
    ms=max(0,int(t*1000)); fc+=f"[{j+2}:a]aresample=44100,volume={g},adelay={ms}|{ms}[e{j}];"; ins+=f"[e{j}]"
fc+=f"{ins}amix=inputs={len(ev)+2}:duration=longest:normalize=0,atrim=0:{D},loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.8:level=false[out]"
cmd+=['-filter_complex',fc,'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix-v.m4a']
subprocess.run(cmd,check=True); print('dur',round(D,2))
