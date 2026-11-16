# python3 mix.py -> mix-v.m4a (VO + music bed + sfx). Music drops out for a beat before the name (line 11).
import json, subprocess, re
T=json.loads(open('timeline.js').read().split('=',1)[1].rstrip(';\n'))
S=lambda i:T[i]['start']; E=lambda i:T[i]['end']
D=E(len(T)-1)+0.6+2.4
def word(i,rx):
    for w in T[i]['words']:
        if re.match(rx,w['w'],re.I): return w['s']
    return S(i)
ev=[('sfx/tick.wav',0.4,.4),('sfx/tick.wav',0.9,.4),('sfx/tick.wav',1.4,.4),('sfx/tick.wav',1.9,.4)]
for i in (1,3,4,5,6,7,10,11,12): ev.append(('sfx/whoosh.wav',S(i)-0.35,.4))
ev+=[('sfx/thud.wav',word(0,'none'),.6),('sfx/boom.wav',word(3,'three'),.5),('sfx/thud.wav',word(4,'day'),.5),
     ('sfx/thud.wav',word(5,'Not'),.5),('sfx/thud.wav',word(8,'twelve|12'),.55),('sfx/thud.wav',word(9,'insiders'),.45),
     ('sfx/boom.wav',word(11,'BLOK'),.45),('sfx/thud.wav',word(13,'FUND'),.55)]
c=S(11)-0.2; w=0.5
cmd=['ffmpeg','-y','-v','error','-i','vo.wav','-stream_loop','3','-i','/home/user/Blok-Content/assets/music/blok-morning-soil.m4a']
for f,_,_ in ev: cmd+=['-i',f]
fc=(f"[0:a]apad=pad_dur=4,aresample=44100,aformat=channel_layouts=stereo,asplit[v][sc];"
    f"[1:a]aresample=44100,atrim=0:{D},afade=t=in:d=1,afade=t=out:st={D-2}:d=2,volume='0.22*min(1,max(0,(abs(t-{c})-{w})/0.4))':eval=frame[m0];"
    "[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m];")
ins='[v][m]'
for j,(f,t,g) in enumerate(ev):
    ms=max(0,int(t*1000)); fc+=f"[{j+2}:a]aresample=44100,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[e{j}];"; ins+=f"[e{j}]"
fc+=f"{ins}amix=inputs={len(ev)+2}:duration=longest:normalize=0,atrim=0:{D},loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.8:level=false[out]"
cmd+=['-filter_complex',fc,'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix-v.m4a']
subprocess.run(cmd,check=True); print('dur',round(D,2))
