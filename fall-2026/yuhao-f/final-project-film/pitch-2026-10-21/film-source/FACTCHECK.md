# FACTCHECK — checkedsql-pitch

Status: claims checked by Claude (agent) on 2026-10-21 against the two real screenshots; signed off by Yuhao Fu on 2026-10-24 after watching the film and confirming beat 3 (I did look at both alternatives).
Every claim is the author's own statement about his own project (first person, from `../beat_sheet.json`).
Nothing was added. Claims checkable against the real screenshots are marked PASS with that evidence; plans and
personal statements are EXEMPT (author's own intent/biography, not verifiable here).

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B01 | AI-written SQL can look right and be wrong | EXEMPT | author's framing question | — |
| 2 | B02 | Final project will be CheckedSQL: CLI, English → SQL on a public sample database, runs every query, checks against hand-verified answers; GitHub repo with test set, saved results, failure analysis | EXEMPT | author's plan (future tense) | — |
| 3 | B03 | Author looked at asking a chat assistant directly, and Vanna.ai | EXEMPT | author's statement; text confirmed by author 2026-10-21 (placeholder filled with its example) | placeholder removed |
| 4 | B03 | Those tools don't give a small reproducible record of wrong answers; not claiming more accuracy | EXEMPT | author's assessment, explicitly hedged | — |
| 5 | B04 | Reader is a hiring manager; README → results → one-command rerun | EXEMPT | author's plan | — |
| 6 | B05 | Prompt contract (one SELECT or refusal), read-only DB, fixed test set with saved results | EXEMPT | author's plan | — |
| 7 | B06 | A test set of twenty questions exists | PASS | `assets/shot-check-gold-2026-10-21.png`: questions [1]–[20] | — |
| 8 | B06 | All twenty answer queries ran on the real database, October 21 | PASS | both screenshots, dated 2026-10-21; `Gold SQL errors: 0/20` in `assets/shot-tie-2026-10-21.png` | — |
| 9 | B06 | Draft eval script written with Claude's help; model-calling part has not run | EXEMPT | author's statement (screenshot shows `run_eval.py --check-gold` only) | — |
| 10 | B07 | Scope: read-only, one sample DB; no web UI, no other DBs; first milestone one question end to end | EXEMPT | author's plan | — |
| 11 | B08 | One hand-checked answer was arbitrary: four years tied, query picked one | PASS | `assets/shot-tie-2026-10-21.png`: 2009, 2010, 2011, 2012 each 83 invoices (2013: 80) | — |
| 12 | B09 | Biography: SE master's student, SDE roles, self-taught Python/SQL from YouTube, no proving repo yet | EXEMPT | author's own statement | — |
| 13 | B10 | Close: mistakes you can see; "I'm Yuhao Fu." | EXEMPT | author's sign-off | — |
