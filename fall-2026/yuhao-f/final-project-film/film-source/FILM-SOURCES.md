# SOURCES — checkedsql-film

| Source | What it supplies |
|---|---|
| `../film_beat_sheet.json` (Yuhao Fu, author; drafted with Claude 2026-11-24) | All fourteen narration lines and the visual plan, in the course brief's four parts. |
| Course email "What your project film needs to show" (Professor Bear, 2026-11) | The four-part structure: executive summary, introduction, methods, evaluation. |
| Yu et al., "Spider", EMNLP 2018, https://arxiv.org/abs/1809.08887 | B03: 10,181 questions, 200 databases, 2018. |
| Li et al., "Can LLM Already Serve as A Database Interface? (BIRD)", NeurIPS 2023, https://arxiv.org/abs/2305.03111 | B03: 12,751 question–SQL pairs; ChatGPT 40.08% execution accuracy vs human 92.96% (abstract). |
| Zhong, Yu, Klein, "Semantic Evaluation for Text-to-SQL with Distilled Test Suites", EMNLP 2020, https://arxiv.org/abs/2010.02840 | B04, B13: single-database denotation evaluation "might create false positives"; fix: a distilled suite of databases. |
| Vanna, https://github.com/vanna-ai/vanna | B05: open-source (MIT) library to chat with a SQL database and get SQL from an LLM. |
| `assets/shot-tie-2026-10-21.png` (= `../checkedsql-pitch/assets/`, the author's screenshot) | B09: 2009–2012 tied at 83 invoices, 2026-10-21. |
| `evidence/run-replay.txt` → `assets/out-run-2026-11-24.png` | B12: real stdout of `python -m checkedsql run --replies replays/claude-code-subagents.json`, captured 2026-11-24 at checkedsql commit 4a3c927 (`evidence/captured-at.txt`). |
| `evidence/check-wrong.txt` → `assets/out-check-wrong-2026-11-24.png` | B13: real stdout of `python -m checkedsql check-wrong`, same capture. |
| https://github.com/Femon02/checkedsql (README, code, `results/run_20261106-170720.*`) | B07, B08, B10, B11: Chinook data, 20 questions, contract, read-only + 5 s limit, replay method, metrics. |
| `icons/logos/{claude,claude-code,chatgpt,python,sqlite}/*-01.png` (toolkit) | Marks for Claude (B01, B08, B14), Claude Code (B10), ChatGPT (B03), Python and SQLite (B10): LOGO LAW. |
