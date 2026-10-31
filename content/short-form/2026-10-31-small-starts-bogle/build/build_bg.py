"""Background track for the "people in scenes" style: one shot per beat, hard cuts on the voice.
python3 build_bg.py  -> bg.mp4 + shots.js. Clips (vid/*.mp4) play at normal speed and freeze on their last frame
if the beat is longer; stills get a slow 3% push, except the scoreboard (static, so the chalk overlay stays put)."""
import json, subprocess
T = json.loads(open('timeline.js').read().split('=', 1)[1].rstrip(';\n'))
FPS = 30
# (source, first line of the shot)
SHOTS = [('vid/v20.mp4', 0), ('img/c11.jpg', 1), ('vid/v21.mp4', 3), ('vid/v22.mp4', 5), ('img/c12.jpg', 7),
         ('img/c11.jpg', 8), ('img/c13.jpg', 9), ('vid/v23.mp4', 10), ('img/b6.jpg', 11), (None, 11.4)]
STATIC = {'img/c11.jpg'}
END = T[-1]['end'] + 1.5
# 11.4 = line 11 from its 5th word ('Next:'): the end card takes over there
starts = [0.0 if l == 0 else round(T[11]['words'][4]['s'] - 0.1, 3) if l == 11.4 else round(T[l]['start'] - 0.12, 3) for _, l in SHOTS]
parts = []
for k, (src, l) in enumerate(SHOTS):
    d = (starts[k + 1] if k + 1 < len(SHOTS) else END) - starts[k]
    nf = round((starts[k + 1] if k + 1 < len(SHOTS) else END) * FPS) - round(starts[k] * FPS)  # frame-exact cuts
    o = f'seg{k}.mp4'; parts.append(o)
    cover = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1'
    if src is None:
        cmd = ['-f', 'lavfi', '-i', f'color=black:s=1080x1920:r={FPS}:d={d + 1}']
    elif src.endswith('.mp4'):
        cd = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
        slow = max(1.0, (d + 0.05) / cd)  # stretch a clip a little rather than freeze it
        cmd = ['-i', src, '-vf', f'setpts={slow:.4f}*PTS,{cover},fps={FPS},tpad=stop_mode=clone:stop_duration={d}', '-an']
    elif src in STATIC:
        cmd = ['-loop', '1', '-i', src, '-vf', f'{cover},fps={FPS}']
    else:
        n = int(d * FPS) + 1
        cmd = ['-loop', '1', '-i', src, '-vf', f'scale=2160:3840,zoompan=z=1+0.03*on/{n}:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps={FPS}']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *cmd, '-frames:v', str(nf), '-c:v', 'libx264', '-preset', 'fast', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', str(FPS), o], check=True)
open('concat.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'bg.mp4'], check=True)
open('shots.js', 'w').write('window.SHOTS = ' + json.dumps([{'src': s, 'line': l, 'start': st} for (s, l), st in zip(SHOTS, starts)]) + ';')
print('bg.mp4', round(END, 2))
