# usage: python gen_all.py build/lines.json [brooks-ref-9s.wav]   (run from the piece folder; writes takes/)
import json, soundfile as sf, torch, os, sys
from chatterbox.tts import ChatterboxTTS
import sys
L=json.load(open(sys.argv[1])); REF=sys.argv[2] if len(sys.argv)>2 else 'brooks-ref-9s.wav'; os.makedirs('takes',exist_ok=True)
m=ChatterboxTTS.from_pretrained(device='cpu')
for k in range(3):
  for i,l in enumerate(L):
    p=f'takes/l{i:02d}_t{k}.wav'
    if os.path.exists(p): continue
    torch.manual_seed(100*k+i)
    w=m.generate(l['say'], audio_prompt_path=REF, exaggeration=0.5, cfg_weight=0.5)
    sf.write(p, w.squeeze(0).numpy(), m.sr); print(p, flush=True)
