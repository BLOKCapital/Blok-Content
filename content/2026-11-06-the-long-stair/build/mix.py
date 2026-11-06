# usage: python3 mix.py -> mix.m4a  (VO + our blok-morning-soil track + bundled Pixabay SFX + footsteps)
import json, subprocess
T=json.loads(open('timeline.js').read().split('=',1)[1].rstrip(';\n'))
S=lambda i:T[i]['start']; E=lambda i:T[i]['end']
def wt(L,w):
    for o in T[L]['words']:
        if ''.join(ch for ch in o['w'].lower() if ch.isalpha() or ch=="'")==w: return o['s']
    return S(L)
D=E(9)+1.8
SFX='/mnt/project-files/setup/hyperframes-skills/media-use/audio/assets/sfx/'
ev=[('sfx/step.wav',.9,.4)]
def steps(a,b,dt,g):
    t=a
    while t<b: ev.append(('sfx/step.wav',t,g)); t+=dt
steps(S(5),E(6)+.4,.42,.28); steps(S(7),S(8)+2.6,.38,.22)
ev+=[(SFX+'whoosh.mp3',S(1)-.1,.5),(SFX+'pop.mp3',wt(1,'quit')+.6,.45),(SFX+'whoosh-short.mp3',S(2)-.05,.5),
     (SFX+'impact-bass-2.mp3',wt(2,'applied'),.6),(SFX+'pop.mp3',wt(2,'applied')+.05,.5),
     (SFX+'impact-bass-1.mp3',S(3)+.25,.5),(SFX+'whoosh-cinematic.mp3',wt(3,'going')-.3,.45),
     (SFX+'pop.mp3',wt(5,'video'),.4),(SFX+'pop.mp3',wt(5,'learn'),.4),
     (SFX+'sparkle.mp3',wt(6,'honestly'),.6),(SFX+'riser.mp3',S(8)-9.8,.25),(SFX+'whoosh.mp3',S(8)-.2,.5),
     (SFX+'sparkle.mp3',S(8)+.4,.8),(SFX+'chime.mp3',S(8)+1.0,.45),(SFX+'chime.mp3',E(9)-.2,.45)]
cmd=['ffmpeg','-y','-v','error','-i','vo.wav','-stream_loop','3','-i','/home/user/Blok-Content/assets/music/blok-morning-soil.m4a']
for f,_,_ in ev: cmd+=['-i',f]
fc=f"[0:a]aresample=44100,asplit[v][sc];[1:a]atrim=0:{D},afade=t=in:d=1,afade=t=out:st={D-2}:d=2,volume=0.22[m0];[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m];"
ins='[v][m]'
for j,(f,t,g) in enumerate(ev):
    ms=max(0,int(t*1000)); fc+=f"[{j+2}:a]aresample=44100,volume={g},adelay={ms}|{ms}[e{j}];"; ins+=f"[e{j}]"
fc+=f"{ins}amix=inputs={len(ev)+2}:duration=longest:normalize=0,atrim=0:{D},loudnorm=I=-15.5:TP=-2.5:LRA=11,alimiter=limit=0.72:level=false[out]"
cmd+=['-filter_complex',fc,'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a']
subprocess.run(cmd,check=True); print('events',len(ev),'dur',round(D,2))
