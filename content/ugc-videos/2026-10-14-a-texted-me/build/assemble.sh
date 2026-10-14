set -e
ffmpeg -v error -y -sseof -0.05 -i clip.mp4 -frames:v 1 -vf "scale=1080:1920:flags=lanczos,boxblur=18:2" last.png
ffmpeg -v error -y -i clip.mp4 -loop 1 -t 5.5 -i last.png \
 -loop 1 -i ov-hook.png -loop 1 -i ov-notif.png -loop 1 -i ov-aside.png -loop 1 -t 5.5 -i ov-end.png -i audio.m4a \
 -filter_complex "\
[0:v]scale=1080:1920:flags=lanczos,fps=30,setsar=1,trim=0:8,setpts=PTS-STARTPTS,noise=alls=6:allf=t[c];\
[1:v]fps=30,setsar=1,format=yuv420p[l];\
[5:v]format=rgba,fade=t=in:st=0:d=0.5:alpha=1[e];[l][e]overlay=0:0:shortest=1[tail];\
[c][tail]concat=n=2:v=1:a=0[base];\
[2:v]format=rgba,fade=t=in:st=0.15:d=0.3:alpha=1,fade=t=out:st=1.7:d=0.25:alpha=1[h];\
[3:v]format=rgba[n];[4:v]format=rgba,fade=t=in:st=5.7:d=0.3:alpha=1[a];\
[base][h]overlay=0:0:enable='lt(t,2)':shortest=1[v1];\
[v1][n]overlay=x=0:y='if(lt(t-1.95,0.28),-620+(t-1.95)/0.28*620,0)':enable='between(t,1.95,5.6)'[v2];\
[v2][a]overlay=0:0:enable='between(t,5.7,8)',format=yuv420p[v]" \
 -map "[v]" -map 6:a -t 13.5 -c:v libx264 -preset slow -crf 22 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../a-texted-me.mp4
