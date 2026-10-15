#!/bin/bash
# usage: export.sh <carousel folder>  (expects build/png/slide-0N.png and build/track.m4a)
set -e
C="$1"; cd "$C"; D=4.4
mkdir -p video
for i in 1 2 3 4 5 6 7; do
  n=0$i
  ffmpeg -y -loglevel error -i build/png/slide-$n.png -q:v 2 slide-$n.jpg
  ss=$(python3 -c "print(round(($i-1)*$D,2))")
  ffmpeg -y -loglevel error -loop 1 -framerate 30 -t $D -i build/png/slide-$n.png -ss $ss -t $D -i build/track.m4a \
    -filter_complex "[1:a]afade=t=in:d=0.15,afade=t=out:st=$(python3 -c "print($D-0.4)"):d=0.4[a]" \
    -map 0:v -map "[a]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart video/slide-$n.mp4
done
ffmpeg -y -loglevel error -i slide-01.jpg -i slide-02.jpg -i slide-03.jpg -i slide-04.jpg -i slide-05.jpg -i slide-06.jpg -i slide-07.jpg -f lavfi -i color=c=0xE8E7E3:s=1080x1350 \
  -filter_complex "[0][1][2][3]hstack=4[a];[4][5][6][7]hstack=4[b];[a][b]vstack=2,scale=2160:-1" -frames:v 1 -q:v 3 preview-all-slides.jpg
