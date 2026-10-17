import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
S="/tmp/claude-0/-home-claude-Blok-Content/a82bc49a-aff0-55fc-8c41-833a1bba2742/scratchpad/"
k=Kokoro(S+"kokoro-v1.0.onnx",S+"voices-v1.0.bin")
voice=sys.argv[1]; speed=float(sys.argv[2])
lines=[l.strip() for l in open("script.txt") if l.strip()]
gaps=[0.6]+[0.45]*8+[1.1,0.7,0.5]  # pause BEFORE each line (after hook / before reveal longer)
gaps[1]=0.8; gaps[9]=1.3
sr=24000; out=[]; tl=[]; t=0.35; out.append(np.zeros(int(sr*0.35)))
for i,l in enumerate(lines):
    if i: out.append(np.zeros(int(sr*gaps[i]))); t+=gaps[i]
    a,sr=k.create(l.replace("1935","nineteen thirty-five").replace("2010","twenty ten"),voice=voice,speed=speed,lang="en-us")
    tl.append({"i":i,"text":l,"start":round(t,3),"end":round(t+len(a)/sr,3)}); out.append(a); t+=len(a)/sr
out.append(np.zeros(int(sr*0.5)))
sf.write("vo.wav",np.concatenate(out),sr); json.dump(tl,open("lines.json","w"),indent=1)
print(round(t,2)); [print(x["start"],x["end"],x["text"][:40]) for x in tl]
