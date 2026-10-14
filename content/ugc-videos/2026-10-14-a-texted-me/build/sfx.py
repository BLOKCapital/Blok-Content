import numpy as np, wave
sr=44100; T=8.0; t=np.arange(int(sr*T))/sr
def env(x,a,r): return np.clip(np.minimum(x/a,1),0,1)*np.exp(-np.maximum(x,0)/r)
out=np.zeros_like(t)
# dark tense pad: low A minor-ish cluster, slow swell, tremolo
for f,g in [(55,.5),(110,.35),(130.8,.22),(164.8,.15),(116.5,.12)]:
    ph=2*np.pi*f*t
    out+=g*(np.sin(ph)+.3*np.sin(2*ph+.4)+.15*np.sin(3*ph))
out*= (0.25+0.75*np.clip(t/5,0,1)) * (0.85+0.15*np.sin(2*np.pi*3.2*t))
# heartbeat pulses from 3s, faster near the end
beats=[3.0,3.35,4.2,4.55,5.3,5.62,6.2,6.5,7.0,7.27]
for b in beats:
    x=t-b; m=x>=0
    out[m]+=1.1*np.sin(2*np.pi*48*x[m])*np.exp(-x[m]/0.09)
# phone buzz at 1.85-2.35
x=t-1.85; m=(x>=0)&(x<0.5)
out[m]+=0.5*np.sign(np.sin(2*np.pi*170*x[m]))*(0.6+0.4*np.sin(2*np.pi*30*x[m]))*(1-(x[m]>0.22)*(x[m]<0.28))
# message ding at 2.0
for f,d in [(1568,0),(2093,0.09)]:
    x=t-2.0-d; m=x>=0
    out[m]+=0.35*np.sin(2*np.pi*f*x[m])*np.exp(-x[m]/0.25)
out[-int(.3*sr):]*=np.linspace(1,0.3,int(.3*sr))
out=out/np.max(np.abs(out))*0.8
w=wave.open('tension.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
