const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const m='v';const W=1080,H=1920;const out='../before-the-bell-4-may-day-1975.mp4';
const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:H}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/scene.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const fps=30,D=await p.evaluate(()=>window.DURATION),N=Math.round(D*fps);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',`mix-${m}.m4a`,'-filter_complex','[0:v]format=yuv420p[v]','-map','[v]','-map','1:a','-c:v','libx264','-crf','19','-preset','medium','-r','30','-c:a','copy','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<N;i++){await p.evaluate(t=>draw(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:95});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log(m,i,N);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done',D)})();
