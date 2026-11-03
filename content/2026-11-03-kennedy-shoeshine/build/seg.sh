#!/bin/bash
# usage: seg.sh name dur  (photos: crop x y w h zoom_end ; video: src start)
TINT="hue=s=0,colorchannelmixer=rr=1.0:gg=0.93:bb=0.80,eq=contrast=1.08:brightness=-0.02,noise=alls=10:allf=t,vignette=PI/4.5"
photo(){ # name dur img cx cy cw ch zend
  n=$1; d=$2; f=$(echo "$d*30/1" | bc); 
  ffmpeg -v error -y -loop 1 -i assets/$3 -vf "crop=$6:$7:$4:$5,scale=1620:2880:flags=lanczos,zoompan=z='1+($8-1)*on/$f':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$f:s=1080x1920:fps=30,$TINT,format=yuv420p" -frames:v $f -c:v libx264 -crf 18 -preset fast seg/$n.mp4; }
video(){ # name dur src start  [zoom]
  n=$1; d=$2; z=${5:-1.0}
  ffmpeg -v error -y -ss $4 -i assets/$3 -t $d -an -vf "scale=-2:1920*$z:flags=lanczos,crop=1080:1920,unsharp=5:5:0.6,fps=30,$TINT,format=yuv420p" -c:v libx264 -crf 18 -preset fast seg/$n.mp4; }
"$@"
