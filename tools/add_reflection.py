#!/usr/bin/env python3
"""Check a reflection and add it to reflections.json (newest first, last 60 kept).
Usage: python3 tools/add_reflection.py entry.json [--replace]
entry.json fields (all required):
  date "YYYY-MM-DD", ayah "surah:ayah",
  title_en, title_fr, title_ar          (<= 90 chars, neutral headline of the trend)
  summary_en, summary_fr, summary_ar    (<= 480 chars, neutral, what is happening and why people are talking about it)
  why_en, why_fr, why_ar                (<= 420 chars, how the ayah's own meaning, per its tafsir, relates; never claims the ayah is about the event)
  prompts_en, prompts_fr, prompts_ar    (exactly 3 open questions each)
  step_en, step_fr, step_ar             (<= 220 chars, one small thing to do today)
Arabic (Modern Standard Arabic): the reader may be a man or a woman, so the questions are in the first person
("ماذا أفعل…؟") and the step uses verbal nouns ("قراءة الآية، ثم…"), never a gendered "you". In why_ar, quote the
Arabic Al-Mukhtasar (printed below) and the ayah exactly, in «» and ﴿﴾.
  sources                  ([{name, url}], 1 to 4 reputable outlets, https only)"""
import json, sys, os, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = f'{ROOT}/reflections.json'
e = json.load(open(sys.argv[1])); replace = '--replace' in sys.argv
err = []
def need(k, mx=None):
    v = e.get(k)
    if not isinstance(v, str) or not v.strip(): err.append(f'{k} missing')
    elif mx and len(v) > mx: err.append(f'{k} is {len(v)} chars (max {mx})')
try: datetime.date.fromisoformat(e.get('date', ''))
except Exception: err.append('date must be YYYY-MM-DD')
m = re.fullmatch(r'(\d{1,3}):(\d{1,3})', e.get('ayah', ''))
if not m: err.append('ayah must be "surah:ayah"')
else:
    s, a = int(m[1]), int(m[2])
    if not 1 <= s <= 114: err.append('no such surah')
    else:
        v = json.load(open(f'{ROOT}/quran/{s}.json'))['v']
        if not 1 <= a <= len(v): err.append(f'surah {s} has {len(v)} ayat')
        else: print(f"Ayah {s}:{a}\n  {v[a-1][0]}\n  {v[a-1][1]}\n  tafsir: {v[a-1][3][:400]}\n  تفسير المختصر: {v[a-1][6] if len(v[a-1]) > 6 else ''}\n")
for k, mx in [('title_en', 90), ('title_fr', 100), ('title_ar', 100), ('summary_en', 480), ('summary_fr', 560), ('summary_ar', 560),
              ('why_en', 420), ('why_fr', 500), ('why_ar', 500), ('step_en', 220), ('step_fr', 260), ('step_ar', 260)]: need(k, mx)
for k in ('title_ar', 'summary_ar', 'why_ar', 'step_ar'):
    if isinstance(e.get(k), str) and not re.search(r'[\u0600-\u06FF]', e[k]): err.append(f'{k} must be in Arabic')
for k in ['prompts_en', 'prompts_fr', 'prompts_ar']:
    p = e.get(k)
    if not (isinstance(p, list) and len(p) == 3 and all(isinstance(x, str) and 10 < len(x) < 220 for x in p)): err.append(f'{k} must be 3 questions, each under 220 chars')
src = e.get('sources')
if not (isinstance(src, list) and 1 <= len(src) <= 4 and all(isinstance(x, dict) and x.get('name') and str(x.get('url', '')).startswith('https://') for x in src)):
    err.append('sources must be 1-4 items with name and https url')
data = json.load(open(F)) if os.path.exists(F) else {"items": []}
items = data['items']
if any(x['date'] == e.get('date') for x in items) and not replace: err.append(f"a reflection for {e.get('date')} exists (use --replace)")
recent = [x['ayah'] for x in sorted(items, key=lambda x: x['date'], reverse=True)[:60] if x['date'] != e.get('date')]
if e.get('ayah') in recent: err.append(f"ayah {e['ayah']} was used in the last 60 reflections; choose another")
if err: sys.exit('NOT ADDED:\n- ' + '\n- '.join(err))
keep = {k: e[k] for k in ['date', 'ayah', 'title_en', 'title_fr', 'title_ar', 'summary_en', 'summary_fr', 'summary_ar', 'why_en', 'why_fr', 'why_ar',
                          'prompts_en', 'prompts_fr', 'prompts_ar', 'step_en', 'step_fr', 'step_ar', 'sources']}
items = [x for x in items if x['date'] != e['date']] + [keep]
items.sort(key=lambda x: x['date'], reverse=True)
json.dump({"items": items[:60]}, open(F, 'w'), ensure_ascii=False, indent=1)
print(f"Added reflection for {e['date']} ({len(items[:60])} kept).")
