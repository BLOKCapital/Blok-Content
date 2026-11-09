# usage: python3 mix.py v|h -> mix-v.m4a / mix-h.m4a (VO + our track + boom/thud/whoosh)
import json, subprocess, sys, re
M=sys.argv[1]
T=json.loads(open('timeline.js').read().split('=',1)[1].rstrip(';\n'))
if M=='h': T=T[:10]
S=lambda i:T[i]['start']; E=lambda i:T[i]['end']
D=E(len(T)-1)+0.6+(2.6 if M=='v' else 3.4)
def word(i,rx):
    for w in T[i]['words']:
        if re.match(rx,w['w'],re.I): return w['s']
    return S(i)
ev=[('sfx/boom.wav',0.05,.8),('sfx/thud.wav',word(0,'down'),.7),('sfx/whoosh.wav',S(2)-0.4,.5),('sfx/whoosh.wav',S(3)-0.4,.4),
    ('sfx/thud.wav',word(4,r'Reuters'),.7),('sfx/whoosh.wav',S(6)-0.4,.5),('sfx/boom.wav',word(7,'slept'),.6),('sfx/whoosh.wav',S(9)-0.4,.4)]
if M=='v': ev.append(('sfx/whoosh.wav',S(10)-0.4,.4))
V='vo.wav' if M=='v' else 'vo-h.wav'
if M=='h':
    subprocess.run(['ffmpeg','-y','-v','error','-i','vo.wav','-t',str(E(9)+0.1),'vo-h.wav'],check=True)
cmd=['ffmpeg','-y','-v','error','-i',V,'-stream_loop','3','-i','/home/user/Blok-Content/assets/music/blok-morning-soil.m4a']
for f,_,_ in ev: cmd+=['-i',f]
fc=f"[0:a]apad=pad_dur=4,aresample=44100,aformat=channel_layouts=stereo,asplit[v][sc];[1:a]aresample=44100,atrim=0:{D},afade=t=in:d=1,afade=t=out:st={D-2}:d=2,volume=0.2[m0];[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m];"
ins='[v][m]'
for j,(f,t,g) in enumerate(ev):
    ms=max(0,int(t*1000)); fc+=f"[{j+2}:a]aresample=44100,volume={g},adelay={ms}|{ms}[e{j}];"; ins+=f"[e{j}]"
fc+=f"{ins}amix=inputs={len(ev)+2}:duration=longest:normalize=0,atrim=0:{D},loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.8:level=false[out]"
cmd+=['-filter_complex',fc,'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k',f'mix-{M}.m4a']
subprocess.run(cmd,check=True); print('dur',round(D,2))
