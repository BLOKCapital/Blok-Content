# build.py [timeline.js]: writes index.html with duration from the timeline (end card 5.6 s)
import json,sys,re,shutil
P='/tmp/claude-0/hfp/parents-video/'
if len(sys.argv)>1: shutil.copy(sys.argv[1],P+'timeline.js')
T=json.loads(re.sub(r'^window.TIMELINE = |;$','',open(P+'timeline.js').read().strip()))
dur=round(T[-1]["end"]+2.5,2)
open(P+'index.html','w').write(open('/tmp/claude-0/hfp/index.template.txt').read().replace('__DUR__',str(dur)))
print('dur',dur)
