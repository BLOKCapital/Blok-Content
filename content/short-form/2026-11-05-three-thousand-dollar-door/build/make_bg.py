# Builds bg.mp4 (1080x1920, 30fps) from timeline.js: one archive photo per line with a slow push.
import json,re,subprocess,sys,os
T=json.loads(re.search(r'=\s*(\[.*\])',open('timeline.js').read(),re.S).group(1))
DUR=float(sys.argv[1]) if len(sys.argv)>1 else T[-1]['end']+2.0
# line index -> (image, crop centre x frac, centre y frac, zoom_end)
SHOTS={0:('S82-33289.jpg',.50,.45,1.10),1:('KSC-01pp0171.jpg',.50,.55,1.12),2:('KSC-98pc343.jpg',.55,.5,1.08),
 3:('KSC-01pp0172.jpg',.40,.5,1.08),4:('s04-41-1206.jpg',.5,.5,1.06,'eq=brightness=-0.22:contrast=1.1,'),5:('sts068-272-075.jpg',.55,.55,1.08)}
TINT="eq=contrast=1.05:saturation=0.9,noise=alls=6:allf=t,vignette=PI/5"
os.makedirs('seg',exist_ok=True); segs=[]
starts=[0]+[T[i]['start']-0.05 for i in range(1,len(T))]
cut=[(starts[i], starts[i+1] if i+1<len(T) else DUR) for i in range(len(T))]
for i,(a,b) in enumerate(cut):
    d=b-a; f=max(1,round(d*30)); out=f'seg/s{i:02d}.mp4'
    if i in SHOTS:
        img,cx,cy,z,*pre=SHOTS[i]; pre=pre[0] if pre else ''
        from PIL import Image; w,h=Image.open('assets/'+img).size
        # crop to 9:16 around centre
        cw=min(w,int(h*9/16)); ch=int(cw*16/9)
        if ch>h: ch=h; cw=int(h*9/16)
        x=int(max(0,min(w-cw,cx*w-cw/2))); y=int(max(0,min(h-ch,cy*h-ch/2)))
        vf=(f"crop={cw}:{ch}:{x}:{y},scale=2160:3840:flags=lanczos,zoompan=z='1+({z}-1)*on/{f}':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f}:s=1080x1920:fps=30,{pre}{TINT},format=yuv420p")
        cmd=['ffmpeg','-v','error','-y','-loop','1','-i','assets/'+img,'-vf',vf,'-frames:v',str(f),'-c:v','libx264','-crf','18','-preset','fast',out]
    else:
        cmd=['ffmpeg','-v','error','-y','-f','lavfi','-i',f'color=c={"0xF6F3E8" if i>=8 else "0x0b0d12"}:s=1080x1920:r=30','-frames:v',str(f),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p',out]
    subprocess.run(cmd,check=True); segs.append(out)
open('seg/list.txt','w').write(''.join(f"file '{os.path.basename(s)}'\n" for s in segs))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c','copy','bg.mp4'],check=True)
print('bg.mp4',DUR)
