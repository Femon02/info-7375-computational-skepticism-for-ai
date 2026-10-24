# PROJECT-BRIEF — CheckedSQL

**1. What is it?**
CheckedSQL will be a command-line tool that turns English questions into SQL for a public sample database
(Chinook, in SQLite), runs every query, and checks the result against an answer I verified by hand. When it is
done it will be a GitHub repository with a test set, saved results, and a failure analysis.

**2. Why would anyone care?**
I looked at asking a chat assistant directly, and Vanna.ai. They generate SQL, but they do not give me a small,
reproducible record of which answers were wrong and why. CheckedSQL will. I am not claiming it is more accurate,
only that its mistakes will be visible: every question gets a saved SQL query, a result, and a verdict against a
hand-checked answer.

**3. Who opens it, and what do they do?**
The reader is a hiring manager screening an SDE candidate. In the first minute they will open the README, see how
many questions matched and why the others failed, and rerun the check with one command.

**4. What does it prove about me?**
Three things from this course. A prompt contract: the model must output exactly one SELECT, or a refusal.
Verification: every query runs on a read-only database. Evaluation: a fixed test set with saved results. The
evidence will be the result files and the commit history. A reviewer could fairly conclude that I can build a small
LLM tool with a checkable contract and measure where it fails; not that it is accurate on SQL in general.

**5. In, out, first.**
In: read-only questions on one sample database. Out: no web interface and no other databases. First: one question
end to end. You will know it ran because a results file will show the SQL and a verdict.

**6. What could sink it?**
The checker itself can be wrong. It already happened once: when I checked my own answers by hand, one turned out
to be arbitrary. Invoices per year are tied at 83 for 2009, 2010, 2011 and 2012, and my query just picked one.
So every gold answer gets checked by hand, and checker mistakes are counted as their own failure category.

**7. Why this project?**
A mix, and honestly it leans toward learning. I am a software engineering master's student applying for SDE roles,
and I wanted something a stranger can check, not something that just looks impressive.
- *Skills I already have:* Python and SQL basics, self-taught from YouTube. Evidence so far: the gold-answer check
  I ran on 2026-10-21 (screenshots in the film); I do not yet have a repository that proves these skills. This
  project will be that evidence.
- *Skills that are new to me:* calling Claude from my own code, building a test set, and measuring where it fails
  (evaluation and failure analysis).
I chose something small on purpose, so I can finish it honestly.

**Stack:** Python, SQLite (Chinook sample database), Claude API.

## Exists today (2026-10-21, shown in the film)
- A test set of twenty English questions, each with a gold (hand-written) SQL answer.
- A draft evaluation script, `run_eval.py`, written with Claude's help, with a `--check-gold` mode.
- A run of every gold query on the real Chinook database: all twenty ran (`Gold SQL errors: 0/20`).
- One checker problem found by hand: the four-way tie in invoices per year (2009–2012, 83 each).
- This pitch film.

## Will exist
- The part that calls the model (not run yet), under the prompt contract: exactly one SELECT or a refusal.
- Read-only execution of every model query, and a results file per run with the SQL and a verdict.
- A hand check of every gold answer, with checker mistakes counted as their own failure category.
- A README a reviewer can read in a minute, a one-command rerun, saved results, and a failure analysis.
- The public GitHub repository holding all of it, with its commit history.
