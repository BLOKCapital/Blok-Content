# Original score for "The hidden word": slow felt-piano + pad bed, hush before the reveal, bloom on "Patience".
import json, wave, numpy as np
SR=44100; L=json.load(open('lines.json')); S=lambda i:L[i]['start']; E=lambda i:L[i]['end']
T=E(11)+2.6; N=int(SR*T); mix=np.zeros((N,2)); rng=np.random.default_rng(3)
f=lambda m:440*2**((m-69)/12)
def put(sig,at,g=1.0,pan=0.0):
    i=int(at*SR); j=min(N,i+len(sig))
    if j<=i: return
    s=sig[:j-i]*g; mix[i:j,0]+=s*np.sqrt(.5*(1-pan)); mix[i:j,1]+=s*np.sqrt(.5*(1+pan))
def piano(m,d=3.0,v=.5):
    t=np.arange(int(d*SR))/SR; fr=f(m)
    s=sum(a*np.sin(2*np.pi*fr*k*t)*np.exp(-t*(1.6+k*1.3)) for k,a in [(1,1),(2,.35),(3,.12),(4,.05)])
    a=np.minimum(1,t/0.008); return s*a*v
def pad(ms,d,v=.12):
    t=np.arange(int(d*SR))/SR; e=np.minimum(1,t/1.5)*np.minimum(1,(d-t)/1.5)
    s=sum(np.sin(2*np.pi*f(m)*t*(1+dt))+0.5*np.sin(2*np.pi*f(m)*2*t*(1-dt)) for m in ms for dt in (-0.002,0.002))
    return s*e*v/len(ms)
BAR=60/70*4
chords=[(57,[57,60,64,67]),(53,[53,57,60,64]),(48,[55,60,64,67]),(55,[55,59,62,64])]   # Am7 Fmaj7 Cmaj7 G6
hush=S(9)-0.2; bloom=S(10)-0.05
t=0.0; b=0
while t<hush-0.5:
    root,ch=chords[b%4]
    put(pad([root]+ch,BAR+1.4,.10),t)
    put(piano(root-12,4,.35),t)
    arp=[ch[0]+12,ch[2]+12,ch[1]+12,ch[3]+12,ch[2]+12,ch[1]+12]
    for k,m in enumerate(arp):
        at=t+k*BAR/6
        if at<hush-0.3: put(piano(m,2.2,.16),at,pan=(-.3 if k%2 else .3))
    t+=BAR; b+=1
# hush: one held high note while the viewer hunts
put(pad([76],bloom-hush+0.6,.09),hush)
# bloom: C major add9, bell + low swell
put(pad([48,55,60,64,67,74],T-bloom,.16),bloom)
put(piano(36,6,.5),bloom); 
for k,m in enumerate([72,76,79,84]):
    put(piano(m,4,.22),bloom+0.12*k,pan=.2*(k-1.5))
tt=np.arange(int(3*SR))/SR; put(np.sin(2*np.pi*1046.5*tt)*np.exp(-tt*1.2)*.12+np.sin(2*np.pi*1568*tt)*np.exp(-tt*1.6)*.06,bloom)
# low riser into the bloom
d=bloom-hush; tt=np.arange(int(d*SR))/SR; put(rng.standard_normal(len(tt))*(tt/d)**2*.03,hush)
# fade tail
fade=int(1.5*SR); mix[-fade:]*=np.linspace(1,0,fade)[:,None]
mix/=np.abs(mix).max()*1.12
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close(); print('music',T)
