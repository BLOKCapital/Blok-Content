#!/usr/bin/env bash
# Build the 5 video slides + a full cut from the CC0 photos (1080x1440 crops) and the text overlays.
#   bash composite.sh <photoDir with hook,myth1,myth2,myth3,cta .jpg> <overlayDir with o1..o5.png> <music.m4a> <outDir>
set -euo pipefail
P=$1; O=$2; M=$3; OUT=$4; SECS=6; FPS=30; N=$((SECS*FPS))
mkdir -p "$OUT"; names=(hook myth1 myth2 myth3 cta); : > "$OUT/.list"
for i in 0 1 2 3 4; do
  n=$((i+1)); fin=$([ $i = 0 ] && echo 0.6 || echo 0.25)
  ffmpeg -y -loglevel error -loop 1 -framerate $FPS -t $SECS -i "$P/${names[$i]}.jpg" -loop 1 -framerate $FPS -t $SECS -i "$O/o$n.png" \
    -ss $((i*SECS)) -t $SECS -i "$M" \
    -filter_complex "[0:v]scale=1620:2160,zoompan=z='1+0.07*on/$N':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1440:fps=$FPS[bg];[1:v]format=rgba,fade=t=in:st=0.15:d=0.5:alpha=1[ov];[bg][ov]overlay=0:0:format=auto,format=yuv420p[v]" \
    -map "[v]" -map 2:a -c:v libx264 -threads 2 -crf 18 -preset medium -r $FPS -t $SECS \
    -af "afade=t=in:st=0:d=$fin,afade=t=out:st=$((SECS-1)).6:d=0.4" -c:a aac -b:a 192k -movflags +faststart "$OUT/slide-0$n.mp4"
  ffmpeg -y -loglevel error -ss 4.5 -i "$OUT/slide-0$n.mp4" -frames:v 1 -q:v 2 "$OUT/slide-0$n.jpg"
  echo "file 'slide-0$n.mp4'" >> "$OUT/.list"; echo "slide $n done"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$OUT/.list" -an -c:v copy "$OUT/.silent.mp4"
ffmpeg -y -loglevel error -i "$OUT/.silent.mp4" -t $((SECS*5)) -i "$M" -map 0:v -map 1:a -c:v copy \
  -af "afade=t=in:st=0:d=0.6,afade=t=out:st=$((SECS*5-2)).5:d=1.5" -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT/full.mp4"
echo "full cut done"
