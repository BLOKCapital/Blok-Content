Papercraft build (skill: .claude/skills/papercraft). To render: copy the skill's assets/lib to ./lib and
assets/templates/popup-3d/harness.js here, copy ../timeline.js here, add fonts/ (Instrument Serif, Space Mono), then
python .claude/skills/papercraft/scripts/capture.py <this dir> seg:video=68.5,24 --size 1920x1080
(4 parallel segments with FROM = 0, 17.125, 34.25, 51.375 took ~25 min on 4 CPUs). Mux with build/mix (music.py + vo).
