#!/bin/bash
# usage: mix.sh vo.wav duration out.m4a  ; booms at times in BOOMS env (space separated)
VO=$1; D=$2; OUT=$3; M=${MUSIC:-/home/user/Blok-Content/assets/music/blok-morning-soil.m4a}
ff=(-y -v error -i "$VO" -stream_loop 3 -i "$M")
filt="[1:a]atrim=0:$D,afade=t=in:d=0.5,afade=t=out:st=$(python3 -c "print($D-2)"):d=2,volume=0.16[m];"
n=2; mixin="[0:a]volume=1.0[v];[v][m]"; cnt=2
for b in $BOOMS; do
  ff+=(-f lavfi -t 1.5 -i "sine=frequency=55:sample_rate=44100")
  filt+="[$n:a]afade=t=out:st=0:d=1.4:curve=exp,volume=0.7,adelay=$(python3 -c "print(int($b*1000))")|$(python3 -c "print(int($b*1000))")[b$n];"
  mixin+="[b$n]"; n=$((n+1)); cnt=$((cnt+1))
done
filt+="${mixin}amix=inputs=$cnt:duration=longest:normalize=0,atrim=0:$D,loudnorm=I=-15:TP=-1.5:LRA=11[out]"
ffmpeg "${ff[@]}" -filter_complex "$filt" -map "[out]" -ar 44100 -c:a aac -b:a 192k "$OUT"
