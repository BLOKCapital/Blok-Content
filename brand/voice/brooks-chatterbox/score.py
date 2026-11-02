import sys, json, glob, subprocess, numpy as np, sherpa_onnx, os, difflib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from common import norm
M=os.path.expanduser('~/.cache/blok-models/sherpa-onnx-whisper-small.en')
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{M}/small.en-encoder.int8.onnx',decoder=f'{M}/small.en-decoder.int8.onnx',tokens=f'{M}/small.en-tokens.txt',num_threads=4)
L=json.load(open(sys.argv[1])); out={}
for p in sorted(glob.glob(sys.argv[2]+'/l*_t*.wav')):
    i=int(os.path.basename(p)[1:3])
    pcm=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
    a=np.frombuffer(pcm,np.int16).astype(np.float32)/32768
    st=rec.create_stream(); st.accept_waveform(16000,a); rec.decode_stream(st); h=st.result.text.strip()
    r=difflib.SequenceMatcher(None,norm(L[i]['say']),norm(h)).ratio()
    # longest internal pause
    sd=subprocess.run(['ffmpeg','-i',p,'-af','silencedetect=n=-40dB:d=0.3','-f','null','-'],capture_output=True,text=True).stderr
    durs=[float(x.split(':')[1]) for x in sd.split('\n') if 'silence_duration' in x for x in [x.split('|')[1]]]
    out[p]=dict(line=i,ratio=r,heard=h,dur=len(a)/16000,maxpause=max(durs) if durs else 0)
    print(f"{p} {r:.2f} {len(a)/16000:.1f}s pause{out[p]['maxpause']:.1f} | {h}",flush=True)
json.dump(out,open(sys.argv[2]+'/scores.json','w'),indent=1)
