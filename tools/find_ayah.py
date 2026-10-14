#!/usr/bin/env python3
"""Find ayat whose Al-Mukhtasar tafsir mentions given words.
Usage: python3 tools/find_ayah.py WORD [WORD ...] [--ar] [--max 25]
  English words search the English Al-Mukhtasar; with --ar, Arabic words search the Arabic Al-Mukhtasar.
  An ayah matches when its tafsir contains ALL the words given (case-insensitive)."""
import json, sys, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
ar = '--ar' in sys.argv
mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 25
if '--max' in sys.argv: args.remove(str(mx))
if not args: sys.exit(__doc__)
hits = 0
for s in range(1, 115):
    q = json.load(open(f'{ROOT}/quran/{s}.json'))['v']
    tar = dict(json.load(open(f'{ROOT}/tools/tafsir-ar/{s}.json'))) if ar else None
    for a, v in enumerate(q, 1):
        text = tar.get(a, '') if ar else v[3]
        if all(w.lower() in text.lower() for w in args):
            hits += 1
            print(f"{s}:{a}  {v[1][:140]}\n      tafsir: {v[3][:260]}\n")
            if hits >= mx: sys.exit(0)
print(f"{hits} ayat")
