# FACTCHECK — checkedsql-film

Status: claims checked by Claude (agent) on 2026-11-24 against the sources in SOURCES.md and the CheckedSQL repo.
Plan and narration approved by Yuhao Fu on 2026-11-24 ("我都同意"); final watch-through sign-off pending.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B01 | CheckedSQL runs the AI's query on a real database and compares with a hand-checked answer | PASS | checkedsql `evaluate.py`, `data/questions.json` | — |
| 2 | B02 | A wrong query returns a confident-looking result rather than crashing | EXEMPT | author's framing; shown by B13's blind spot | — |
| 3 | B02 | CheckedSQL checks whether the checker can be fooled | PASS | `checkedsql check-gold`, `check-wrong` | — |
| 4 | B03 | Spider, 2018: about ten thousand questions over two hundred databases | PASS | arXiv 1809.08887: 10,181 questions, 200 databases, EMNLP 2018 | — |
| 5 | B03 | BIRD, 2023: over twelve thousand, larger messier data | PASS | arXiv 2305.03111: 12,751 pairs, 95 DBs, 33.4 GB, NeurIPS 2023 | — |
| 6 | B03 | In BIRD's original paper ChatGPT ~40%, people ~93% | PASS | arXiv 2305.03111 abstract: 40.08% vs 92.96% | attributed aloud ("BIRD's original paper") and on screen ("per BIRD paper") |
| 7 | B04 | 2020, Zhong, Yu and Klein: one-database execution can give false positives; fix: many databases | PASS | arXiv 2010.02840 (EMNLP 2020), §1 and Fig. 1 | — |
| 8 | B05 | Vanna is an open-source library to chat with a database and get SQL | PASS | github.com/vanna-ai/vanna (MIT) | — |
| 9 | B05 | Such tools don't hand you a record of which answers were wrong | EXEMPT | author's assessment, scoped to "a record" | — |
| 10 | B06 | Not a new benchmark, not more accurate; small, one-command rerun; reports checker blind spots | PASS / EXEMPT | repo README "Run it", `check-wrong` | — |
| 11 | B07 | Chinook: free public sample DB of a made-up music store; 20 questions with gold SQL, checked by hand | PASS | `data/NOTICE.md` (MIT, Luis Rocha); `data/questions.json`; author's statement for "by hand" | — |
| 12 | B08 | Schema + contract (one SELECT or "cannot answer"); read-only copy; five-second limit; row comparison | PASS | `contract.py` (CANNOT_ANSWER), `db.py` (`mode=ro`, authorizer, `TIME_LIMIT_S = 5.0`), `compare.py` | — |
| 13 | B09 | Flags arbitrary picks between ties; Oct 21 four years tied at 83 | PASS | `gold.py` tie detector + test; `assets/shot-tie-2026-10-21.png` (2009–2012 at 83) | — |
| 14 | B09 | Runs a list of deliberately wrong answers | PASS | `data/wrong_answers.json`, `sensitivity.py` | — |
| 15 | B10 | Python and SQLite, all free; no API credits yet | PASS / EXEMPT | requirements (anthropic SDK free to install); author's statement | — |
| 16 | B10 | This run used Claude Opus 5.5 inside Claude Code, 20 fresh copies, each with only the rules and one question | PASS | `replays/claude-code-subagents.json` ("how"), `replays/prompts/q01–q20.txt` | — |
| 17 | B10 | API version built and tested; one command with a key | PASS | `model.py`, `cli.py run`; tests use a fake client; README says not yet run live | — |
| 18 | B11 | Metrics: match, contract kept, wrong answers caught; pass/fail criterion | PASS | `evaluate.py` verdicts, `check-wrong` exit code | — |
| 19 | B12 | All twenty matched and kept the contract | PASS | `assets/out-run-2026-11-24.png`: 20× MATCH (a contract violation would show as CONTRACT_VIOLATION) | — |
| 20 | B13 | 7 of 8 wrong answers caught; question 16 missed; every Quantity is 1 | PASS | `assets/out-check-wrong-2026-11-24.png`; `SELECT DISTINCT Quantity FROM InvoiceLine` → 1 (test in repo) | — |
| 21 | B13 | That is the false positive Zhong and colleagues warned about | PASS | arXiv 2010.02840 Fig. 1: a wrong query "happens to have the same denotation" on one database | — |
| 22 | B14 | Next: harder questions, varied quantities, API run; "I'm Yuhao Fu." | EXEMPT | author's plan and sign-off | — |
