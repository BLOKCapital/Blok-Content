"""Copy QA: python3 scripts/qa/check_copy.py <caption.md> [build/lines.json]
- measures every ``` block (X posts) against 280 characters
- spell-checks the caption and on-screen lines (names will show up: confirm each one by eye)
- flags rupees, crypto words in the Instagram caption, missing risk line / AI-voice note, hype words"""
import sys, re, json
from spellchecker import SpellChecker
s = open(sys.argv[1]).read(); bad = 0
for i, b in enumerate(re.findall(r'```\n(.*?)\n```', s, re.S)):
    n = len(b); print(f"X block {i}: {n} chars {'OK' if n <= 280 else 'TOO LONG'}"); bad += n > 280
ig = s.split('<!-- IG START -->')[1].split('<!-- IG END -->')[0] if '<!-- IG START -->' in s else ''
txt = s + ' '.join(l['show'] for l in json.load(open(sys.argv[2]))) if len(sys.argv) > 2 else s
unk = sorted(w for w in SpellChecker().unknown({w.lower() for w in re.findall(r"[A-Za-z][a-z']+", txt)}) if len(w) > 2)
print('unknown words (check each):', unk)
checks = [('rupee/₹ amount', re.search(r'₹|rupee|lakh|crore', s, re.I)),
          ('crypto words in IG caption', re.search(r'crypto|token|blockchain|on-chain|wallet|defi|\$BLOKC', ig, re.I)),
          ('hype words', re.search(r'guarantee|risk-free|100x|moon|lambo|to the moon', s, re.I)),
          ('IG risk line missing', ig and not re.search(r'involves risk|carries risk', ig)),
          ('IG AI-voice note missing', ig and not re.search(r'AI-generated', ig))]
for name, hit in checks:
    if hit: print('FLAG:', name); bad += 1
print('copy issues:', bad)
