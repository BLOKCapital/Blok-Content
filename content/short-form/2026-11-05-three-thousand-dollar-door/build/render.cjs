const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/overlay.html');await p.evaluate(()=>document.fonts.ready);
const fps=30,D=await p.evaluate(()=>window.DURATION),N=Math.round(D*fps);
const ff=spawn('ffmpeg',['-y','-v','error','-i','bg.mp4','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-i','mix.m4a','-filter_complex','[0:v][1:v]overlay=format=auto,format=yuv420p[v]','-map','[v]','-map','2:a','-c:v','libx264','-crf','19','-preset','medium','-r','30','-c:a','copy','-shortest','-movflags','+faststart','../the-three-thousand-dollar-door.mp4'],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<N;i++){await p.evaluate(t=>draw(t),i/fps);const buf=await p.screenshot({type:'png',omitBackground:true});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log(i,N);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done',D)})();
