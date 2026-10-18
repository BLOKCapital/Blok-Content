#!/bin/bash
# Instagram slides: crop each 1080-wide slice out of the panorama frames, 6 s each, with the matching 6 s of music
# (slide n gets seconds 6(n-1)..6n of the track, so the music carries on as you swipe).
# Frames 0..179 = t 0..6 s from `node build/render-range.mjs <dir> 30 0 180`.
F=$1; OUT=$2; M=$3   # frames dir, output dir, music
mkdir -p "$OUT/video" "$OUT/jpg"
for n in 1 2 3 4 5; do
  X=$(( (n-1)*1080 )); A=$(( (n-1)*6 ))
  ffmpeg -loglevel error -y -framerate 30 -i "$F/f%04d.jpg" -ss $A -t 6 -i "$M" \
    -filter_complex "[0:v]trim=end_frame=180,crop=1080:1440:$X:0,format=yuv420p[v];[1:a]afade=t=in:d=0.05,afade=t=out:st=5.9:d=0.1[a]" \
    -map "[v]" -map "[a]" -t 6 -c:v libx264 -preset slow -crf 19 -r 30 -c:a aac -b:a 192k -movflags +faststart "$OUT/video/slide-0$n.mp4"
done
