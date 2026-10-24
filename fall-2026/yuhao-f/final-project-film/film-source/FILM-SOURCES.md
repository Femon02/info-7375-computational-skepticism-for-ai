# SOURCES — checkedsql-pitch

| Source | What it supplies |
|---|---|
| `../beat_sheet.json` (Yuhao Fu, author) | All ten narration lines, verbatim; the visual plan and on-screen text per beat. Beat 3's `[FILL IN: …]` placeholder replaced with its own example text ("asking a chat assistant directly, and Vanna.ai") on Yuhao's instruction, 2026-10-21. |
| `../screenshots/截屏2026-10-21 12.49.31.png` → `assets/shot-check-gold-2026-10-21.png` | Beat 6: real terminal output of `run_eval.py --db Chinook_Sqlite.sqlite --check-gold`, 20 questions, taken 2026-10-21. Copied byte-identical (sha256 10169c01…6489). |
| `../screenshots/截屏2026-10-21 12.46.54.png` → `assets/shot-tie-2026-10-21.png` | Beat 8: real terminal output: `Gold SQL errors: 0/20` and the `sqlite3` invoices-per-year query showing 2009–2012 tied at 83, taken 2026-10-21. Copied byte-identical (sha256 4fac05e7…c16c). |
| `icons/logos/{claude,github,python}/*-01.png` (toolkit) | Marks for Claude (beats 2, 9, 10), GitHub (beats 2, 9), Python (beat 9) — LOGO LAW. |
