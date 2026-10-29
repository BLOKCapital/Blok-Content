"""Pronunciation check: python3 scripts/qa/phonemes.py build/lines.json
Prints how the voice will pronounce every name, number word and uncommon word (IPA), so a wrong one is caught before rendering.
Fix a bad one by respelling it in "say" (e.g. "sous" not "sols"), never by hoping."""
import sys, json, re
from kokoro_onnx.tokenizer import Tokenizer
from spellchecker import SpellChecker
t, sp = Tokenizer(), SpellChecker()
seen = set()
for l in json.load(open(sys.argv[1])):
    for w in re.findall(r"[A-Za-z][A-Za-z'-]*", l['say']):
        k = w.lower()
        if k in seen: continue
        seen.add(k)
        if w[0].isupper() or sp.unknown([k]) or len(k) > 9:
            print(f"{w:18} {t.phonemize(w, 'en-us')}")
