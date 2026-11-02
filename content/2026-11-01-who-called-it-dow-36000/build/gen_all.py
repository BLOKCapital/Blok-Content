import json, soundfile as sf, torch, os, sys
from chatterbox.tts import ChatterboxTTS
L=json.load(open('/mnt/project-files/content/2026-11-01-who-called-it-dow-36000/build/lines.json'))
m=ChatterboxTTS.from_pretrained(device='cpu')
for k in range(3):
  for i,l in enumerate(L):
    p=f'takes/l{i:02d}_t{k}.wav'
    if os.path.exists(p): continue
    torch.manual_seed(100*k+i)
    w=m.generate(l['say'], audio_prompt_path='ref10.wav', exaggeration=0.5, cfg_weight=0.5)
    sf.write(p, w.squeeze(0).numpy(), m.sr); print(p, flush=True)
