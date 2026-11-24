# PROJECT-BRIEF — CheckedSQL

Written in the four parts of the course brief, in its order. The detail is in the appendix, not in the summary.

## 1. Executive summary: what am I doing, and why would anybody care?

When you ask an AI to write SQL, you get a query that looks right. **CheckedSQL** tells you when it isn't. It takes
the AI's query, runs it on a real database, and compares the answer with one I checked by hand.

Why care: a wrong query doesn't crash. It returns a number that looks just as confident as the right one.
CheckedSQL makes those mistakes visible, and it goes one step further by checking whether the checker itself
can be fooled.

## 2. Introduction: what have other people done?

- **Benchmarks.** Spider (Yu et al., EMNLP 2018) has 10,181 questions over 200 databases. BIRD (Li et al.,
  NeurIPS 2023) has 12,751 question–SQL pairs on larger, messier data (95 databases, 33.4 GB). In BIRD's original
  paper, ChatGPT reached 40.08% execution accuracy, against 92.96% for people.
- **The checker can be wrong.** Zhong, Yu and Klein (EMNLP 2020) showed that executing a query on a single
  database "might create false positives": a wrong query can happen to return the same answer as the gold one.
  Their fix, test-suite accuracy, runs each query on a distilled suite of many databases.
- **Tools.** Open-source libraries such as Vanna let you chat with a database and get SQL back from an LLM.
  They help you write queries. They don't hand you a record of which answers were wrong.

**Why mine still matters.** It isn't a new benchmark, and it isn't more accurate. It's small enough that one person
can read every question, check every answer, and rerun everything with one command. It also reports the checker's
own blind spots as results, instead of hiding them inside a single accuracy number.

## 3. Methods: how am I doing it?

1. **Data.** Chinook, a free public sample database of a made-up music store (MIT licence). I wrote 20 English
   questions and a gold SQL answer for each, and checked every gold answer by hand.
2. **One question, step by step.** The model sees the database schema and a strict contract: reply with exactly
   one SELECT statement, or exactly `CANNOT_ANSWER`. CheckedSQL then:
   - checks the contract, recording a violation rather than repairing it;
   - runs the query on a read-only copy, with a 5-second limit and a cap of 10,000 rows;
   - compares the rows with the gold answer.
3. **Checking the checker.** CheckedSQL also tests its own answer key:
   - `check-gold` flags any gold answer that is an arbitrary pick between ties. One was: on 2026-10-21, four years
     were tied at 83 invoices.
   - `check-wrong` scores a list of deliberately wrong answers, all of which should be caught.
4. **What I have.**
   - The code is Python and SQLite, all free.
   - I don't have API credits yet. So this run was a *replay*: 20 fresh Claude Opus 5.5 subagents inside Claude Code,
     each seeing only the rules and one question. Their replies were recorded verbatim and scored by the same code.
   - The API version is built and tested offline against a fake client, and runs with one command once I have a key.

## 4. Evaluation: how will I know it did a good job?

I measure three things:
- how many answers match the gold answer;
- how many replies keep the contract;
- how many deliberately wrong answers the checker catches.

The checker **works** if every wrong answer is caught. It **fails** if a wrong answer can score as right.

**Results (replay run, 2026-11-06; output re-captured 2026-11-24):**
- **20/20** answers matched, and **20/20** kept the contract. A perfect score on 20 questions mostly tells me the
  questions are easy.
- The checker caught **7 of 8** wrong answers. It missed question 16, revenue as unit price × quantity: every one
  of the 2,240 `InvoiceLine` rows has `Quantity = 1`, so a query that forgets the quantity returns the same
  numbers. This is the single-database false positive that Zhong, Yu and Klein describe, found in my own test set.
  A test in the repository locks it in.

**Next:** harder questions, test data where quantities vary, then a live API run.

## Appendix

- **Repository:** https://github.com/Femon02/checkedsql (README, code, 28 offline tests, `results/`, `replays/`).
- **Commands:**
  - `python -m checkedsql check-gold`
  - `python -m checkedsql check-wrong` (exits 1: one blind spot)
  - `python -m checkedsql run --replies replays/claude-code-subagents.json`
  - `python -m checkedsql run --limit 1` (live, needs `ANTHROPIC_API_KEY`)
- **Verdicts:** MATCH, WRONG_RESULT, SQL_ERROR, REFUSED, CONTRACT_VIOLATION, MODEL_REFUSAL, GOLD_ERROR. Every
  non-match gets a hand-assigned failure category. Checker mistakes are counted separately from model errors.
- **Read-only guard:**
  - SQLite `mode=ro`;
  - an authorizer that denies every non-read action;
  - a progress-handler time limit;
  - one statement per query.
- **Limitations:**
  - 20 easy questions, one run;
  - a replay rather than a bare API call (Claude Code wraps the task in its own system prompt);
  - an order-insensitive comparison that ignores column names;
  - the same model family wrote the checker and answered the questions.
- **Stack:** Python 3.12, SQLite, Anthropic Python SDK 2.6, pytest.
