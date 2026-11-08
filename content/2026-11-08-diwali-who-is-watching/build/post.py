# usage: python3 post.py mix            -> mix.m4a
#        python3 post.py ass             -> captions16.ass, captions9.ass
#        python3 post.py final 16x9 FRAMES_DIR OUT.mp4
import json, subprocess, sys, re, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
T = json.loads(open('timeline.js').read().split('=', 1)[1].rstrip(';\n '))
S = lambda i: T[i]['start']; E = lambda i: T[i]['end']
END = E(len(T) - 1) + 2.4
def word(i, rx):
    for w in T[i]['words']:
        if re.match(rx, w['w'], re.I): return w['s']
    return S(i)
SFX = '/mnt/project-files/content/2026-11-07-the-one-hour-market/build/sfx/'
MUSIC = '/home/user/Blok-Content/assets/music/blok-morning-soil.m4a'

def mix():
    ev = [(SFX + 'boom.wav', 0.05, .8), (SFX + 'thud.wav', word(0, 'stole') , .7), (SFX + 'whoosh.wav', S(2) - 0.4, .4),
          (SFX + 'thud.wav', word(2, 'bank'), .55), (SFX + 'thud.wav', word(2, 'york'), .55), (SFX + 'thud.wav', word(2, 'holiday'), .6),
          (SFX + 'whoosh.wav', S(3) - 0.4, .4), (SFX + 'boom.wav', word(3, 'gone'), .55), (SFX + 'whoosh.wav', S(4) - 0.4, .4),
          (SFX + 'whoosh.wav', S(5) - 0.4, .4), (SFX + 'boom.wav', word(6, 'watching'), .6), (SFX + 'whoosh.wav', S(7) - 0.4, .4),
          (SFX + 'thud.wav', word(7, 'bank'), .45), (SFX + 'thud.wav', word(7, 'broker'), .45), (SFX + 'thud.wav', word(7, 'us'), .5),
          (SFX + 'whoosh.wav', S(9) - 0.4, .4), (SFX + 'boom.wav', word(10, 'happy'), .5)]
    cmd = ['ffmpeg', '-y', '-v', 'error', '-i', 'vo.wav', '-stream_loop', '3', '-i', MUSIC]
    for f, _, _ in ev: cmd += ['-i', f]
    fc = f"[0:a]apad=pad_dur=3,aresample=44100,aformat=channel_layouts=stereo,asplit[v][sc];[1:a]aresample=44100,atrim=0:{END},afade=t=in:d=1,afade=t=out:st={END-2.2}:d=2.2,volume=0.14[m0];[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m];"
    ins = '[v][m]'
    for j, (f, t, g) in enumerate(ev):
        ms = max(0, int(t * 1000)); fc += f"[{j+2}:a]aresample=44100,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[e{j}];"; ins += f"[e{j}]"
    fc += f"{ins}amix=inputs={len(ev)+2}:duration=longest:normalize=0,atrim=0:{END},loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.8:level=false[out]"
    cmd += ['-filter_complex', fc, '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a']
    subprocess.run(cmd, check=True); print('dur', round(END, 2))

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def chunks(words, maxw=4):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= maxw or re.search(r'[.,?!]$', w['w']):
            out.append(cur); cur = []
    if cur: out.append(cur)
    # merge single-word tails into previous chunk when short
    res = []
    for c in out:
        if res and len(c) == 1 and len(res[-1]) < 5 and not re.search(r'[.?!]$', res[-1][-1]['w']): res[-1] += c
        else: res.append(c)
    return res

def ass(vert):
    W, H = (1080, 1920) if vert else (1920, 1080)
    fs = 66 if vert else 58; mv = 520 if vert else 78
    pill_fs = 44 if vert else 40; pill_mv = 250 if vert else 46
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter SemiBold,{fs},&H00FFFFFF,&H00FFFFFF,&H00180E06,&H90000000,0,0,0,0,100,100,0,0,1,4,2,2,60,60,{mv},1
Style: Pill,Inter Display Bold,{pill_fs},&H00241A10,&H00FFFFFF,&H0016D17E,&H00000000,0,0,0,0,100,100,1,0,3,14,0,8,60,60,{pill_mv},1
Style: Small,Inter Medium,{30 if vert else 26},&H00E8F3F6,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,60,60,{390 if vert else 30},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    # top hook pill: open loop, held until the answer starts
    ev.append(f"Dialogue: 1,{ts(0)},{ts(S(3)-0.15)},Pill,,0,0,0,,WHY THAT DAY?")
    ev.append(f"Dialogue: 1,{ts(S(5)-0.1)},{ts(S(7)-0.15)},Pill,,0,0,0,,WHO'S WATCHING YOURS?")
    for i, l in enumerate(T):
        cs = chunks(l['words'])
        for j, c in enumerate(cs):
            st = c[0]['s'] - 0.05
            en = cs[j + 1][0]['s'] - 0.05 if j + 1 < len(cs) else min(c[-1]['e'] + 0.35, (T[i + 1]['start'] - 0.08) if i + 1 < len(T) else END)
            txt = ' '.join(w['w'] for w in c)
            ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{txt}")
    ev.append(f"Dialogue: 0,{ts(E(len(T)-1)+0.2)},{ts(END)},Small,,0,0,0,,Educational only, not financial advice. Investing carries risk. AI-generated voiceover and 3D.")
    open('captions9.ass' if vert else 'captions16.ass', 'w').write(hdr + '\n'.join(ev) + '\n')

def final(aspect, frames, out):
    vert = aspect == '9x16'; W, H = (1080, 1920) if vert else (1920, 1080)
    sub = 'captions9.ass' if vert else 'captions16.ass'
    cmd = ['ffmpeg', '-y', '-v', 'error', '-framerate', '24', '-start_number', '1', '-i', f'{frames}/f%05d.jpg', '-i', 'mix.m4a',
           '-vf', f"scale={W}:{H}:flags=lanczos,unsharp=5:5:0.35,fps=30,subtitles={sub}:fontsdir=/usr/share/fonts/opentype/inter",
           '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
           '-c:a', 'copy', '-movflags', '+faststart', '-shortest', out]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'mix': mix()
    elif a == 'ass': ass(False); ass(True)
    elif a == 'final': final(sys.argv[2], sys.argv[3], sys.argv[4])
