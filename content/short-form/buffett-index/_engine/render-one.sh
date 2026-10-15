#!/bin/bash
# Render one collage reel in the Higgsfield sandbox: mix VO + music, render frames, make X stills + cover.
# Usage (from repo root): render-one.sh <slug> <boards> <outdir>
set -e
S=$1; N=$2; OUT=$3; R=content/short-form/buffett-index; B=$R/$S/build
mkdir -p $OUT/$S
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $B/vo.m4a)
T=$(python3 -c "print(round($D+4.5,2))")
ffmpeg -y -loglevel error -i $B/vo.m4a -stream_loop -1 -i assets/music/blok-morning-soil.m4a -filter_complex \
 "[1:a]volume=0.13,afade=t=in:d=0.6,afade=t=out:st=$(python3 -c "print($T-2.2)"):d=2.2[m];[0:a]apad[v];[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:$T,loudnorm=I=-14:TP=-1.5[o]" \
 -map "[o]" -ar 48000 -c:a aac -b:a 192k $B/mix.m4a
node $R/_engine/render-reel.mjs $B/scene.html $B/mix.m4a $OUT/$S/$S.mp4 30
node $R/_engine/preview.mjs $B/scene.html $OUT/$S stills $N
ffmpeg -y -loglevel error -i $OUT/$S/$S.mp4 -vf "select=eq(n\,45)" -frames:v 1 -q:v 3 $OUT/$S/cover.jpg || true
echo DONE $S
