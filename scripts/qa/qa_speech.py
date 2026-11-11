"""Speech QA: python3 scripts/qa/qa_speech.py <final.mp4> build/lines.json build/timeline.js
Transcribes each line of the finished render and compares it with what the voice was meant to say.
CHECK lines: listen to them. Homophones (B/be, C/see) and number formatting are fine; a wrong or missing word is not."""
import sys, json, re, subprocess, numpy as np, sherpa_onnx, os, difflib
M=os.path.join(os.environ.get('BLOK_MODELS',os.path.expanduser('~/.cache/blok-models')),'sherpa-onnx-whisper-small.en')
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{M}/small.en-encoder.int8.onnx',decoder=f'{M}/small.en-decoder.int8.onnx',tokens=f'{M}/small.en-tokens.txt',num_threads=4)
pcm=subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
a=np.frombuffer(pcm,np.int16).astype(np.float32)/32768
L=json.load(open(sys.argv[2])); T=json.loads(open(sys.argv[3]).read().split('=',1)[1].rstrip(';\n'))
ones='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
tens='_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()
def n2w(n):
    n=int(n)
    if n<20: return ones[n]
    if n<100: return tens[n//10]+('' if n%10==0 else ' '+ones[n%10])
    if n<1000: return ones[n//100]+' hundred'+('' if n%100==0 else ' '+n2w(n%100))
    if 1100<=n<2000 and n%100!=0 and n//100!=10: return n2w(n//100)+' '+(n2w(n%100) if n%100>=10 else 'oh '+ones[n%100])
    return n2w(n//1000)+' thousand'+('' if n%1000==0 else ' '+n2w(n%1000))
def norm(s):
    s=s.lower().replace('$','').replace('-',' ')
    s=re.sub(r'(\d),(\d)',r'\1\2',s)
    s=re.sub(r'\d+',lambda m:n2w(m.group()),s)
    s=re.sub(r'\bdollars?\b','',s)
    return re.sub(r"[^a-z' ]",' ',s).split()
bad=0
for i,(l,t) in enumerate(zip(L,T)):
    s=max(0,int((t['start']-0.12)*16000)); e=int((t['end']+0.2)*16000)
    st=rec.create_stream(); st.accept_waveform(16000,a[s:e]); rec.decode_stream(st)
    heard=st.result.text.strip(); A,B=norm(l['say']),norm(heard)
    r=difflib.SequenceMatcher(None,A,B).ratio()
    diff=[(op,' '.join(A[i1:i2]),' '.join(B[j1:j2])) for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,B).get_opcodes() if op!='equal']
    flag='OK ' if r>=0.92 else 'CHECK'; bad+= r<0.92
    print(f"{flag} {i} {t['start']:5.2f}s match={r:.2f}\n   want: {l['say']}\n   heard: {heard}" + (f"\n   diff: {diff}" if diff else ''))
print('lines to check:',bad)
