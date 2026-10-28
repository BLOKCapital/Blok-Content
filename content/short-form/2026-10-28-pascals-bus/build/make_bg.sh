#!/bin/bash
# Builds bg.mp4 (1080x1920, 30fps) from the animated clips + stills, cut to the voice timing in scene.html.
set -e
read b1 b2 b3 b4 b5 D < <(node render.mjs cuts | python3 -c "import json,sys;j=json.load(sys.stdin);c=j['cuts'];print(c['b1'],c['b2'],c['b3'],c['b4'],c['b5'],j['duration'])")
d() { python3 -c "print(round($1-$2,3))"; }
F="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
kb() { echo "scale=2160:-1,zoompan=z='1+0.0016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=999:s=1080x1920:fps=30,setsar=1"; }
ffmpeg -v error -y -i vid/c1.mp4 -vf "$F,tpad=stop_mode=clone:stop_duration=3" -t $b1 -an seg1.mp4
ffmpeg -v error -y -loop 1 -i img/s2.png -vf "$(kb)" -t $(d $b2 $b1) seg2.mp4
ffmpeg -v error -y -i vid/c3.mp4 -vf "$F,tpad=stop_mode=clone:stop_duration=3" -t $(d $b3 $b2) -an seg3.mp4
ffmpeg -v error -y -i vid/c4.mp4 -vf "$F,tpad=stop_mode=clone:stop_duration=3" -t $(d $b4 $b3) -an seg4.mp4
ffmpeg -v error -y -loop 1 -i img/s5.png -vf "$(kb)" -t $(d $b5 $b4) seg5.mp4
ffmpeg -v error -y -f lavfi -i color=c=0xF6F3E8:s=1080x1920:r=30 -t $(d $D $b5) -pix_fmt yuv420p seg6.mp4
printf "file seg%s.mp4\n" 1 2 3 4 5 6 > segs.txt
ffmpeg -v error -y -f concat -i segs.txt -vf "fps=30,format=yuv420p" -c:v libx264 -crf 16 bg.mp4
rm seg?.mp4 segs.txt
ffprobe -v error -show_entries format=duration -of csv=p=0 bg.mp4
