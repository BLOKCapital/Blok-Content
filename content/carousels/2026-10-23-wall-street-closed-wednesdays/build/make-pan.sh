#!/bin/bash
# X video: glide across the whole panorama. Frames from `node build/render.mjs frames <dir> 30 21`.
# Hold each slide 3 s, ease 1.5 s to the next (5 holds + 4 moves = 21 s).
F=$1; OUT=$2; M=$3   # frames dir, output mp4, music
X='if(lt(t,3),0,if(lt(t,4.5),1080*(1-cos(PI*(t-3)/1.5))/2,if(lt(t,7.5),1080,if(lt(t,9),1080+1080*(1-cos(PI*(t-7.5)/1.5))/2,if(lt(t,12),2160,if(lt(t,13.5),2160+1080*(1-cos(PI*(t-12)/1.5))/2,if(lt(t,16.5),3240,if(lt(t,18),3240+1080*(1-cos(PI*(t-16.5)/1.5))/2,4320))))))))'
ffmpeg -loglevel error -y -framerate 30 -i "$F/f%04d.jpg" -i "$M" -filter_complex "[0:v]crop=1080:1440:'$X':0,format=yuv420p[v];[1:a]afade=t=out:st=19.5:d=1.5[a]" -map "[v]" -map "[a]" -t 21 -c:v libx264 -preset slow -crf 19 -r 30 -c:a aac -b:a 192k -movflags +faststart "$OUT"
