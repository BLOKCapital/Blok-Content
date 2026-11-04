import json,sys,re,shutil
P='/tmp/claude-0/hf169/story/'
if len(sys.argv)>1: shutil.copy(sys.argv[1],P+'timeline.js')
T=json.loads(re.sub(r'^window.TIMELINE = |;$','',open(P+'timeline.js').read().strip()))
dur=round(T[-1]['end']+5.2,2)
open(P+'index.html','w').write(open('/tmp/claude-0/hf169/index.template.txt').read().replace('__DUR__',str(dur)))
print('dur',dur)
