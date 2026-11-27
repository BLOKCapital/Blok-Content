const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const out=process.argv[2],audio=process.argv[3];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://localhost:8765/reel/?size=1080x1920&capture');await p.waitForFunction(()=>window.__papercraft&&window.__papercraft.ready&&window.REEL_GROUPS,null,{timeout:90000});
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const fps=30,D=await p.evaluate(()=>window.DURATION),N=Math.round(D*fps);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',audio,'-filter_complex','[0:v]format=yuv420p[v]','-map','[v]','-map','1:a','-c:v','libx264','-crf','23','-preset','medium','-r','30','-c:a','copy','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<N;i++){await p.evaluate(t=>draw(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log(i,N);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done',D)})();
