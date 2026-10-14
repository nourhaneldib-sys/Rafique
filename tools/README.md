# Rafiq: daily reflection tools

`reflections.json` (repo root) feeds the "Reflection of the day" card. The app reads only the trend text, the ayah
reference and the questions from it. The ayah's Arabic, translation and tafsir always come from `quran/*.json`,
built from: the Quran (Uthmani text), Pickthall (EN), Hamidullah (FR), Al-Mukhtasar tafsir (EN/FR/AR), Al-Muyassar fi Gharib al-Quran.
Each reflection is written in English, French and Arabic; in Arabic the reader is never addressed with a gendered "you" (see add_reflection.py).

- `python3 tools/find_ayah.py patience trial` : ayat whose English Al-Mukhtasar tafsir mentions all the words.
- `python3 tools/find_ayah.py الصبر --ar` : the same, searching the Arabic Al-Mukhtasar (`tools/tafsir-ar`).
- `python3 tools/add_reflection.py entry.json` : checks an entry and adds it (refuses ayat used in the last 60 days).
