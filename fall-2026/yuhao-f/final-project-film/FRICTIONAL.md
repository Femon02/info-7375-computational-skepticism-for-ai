# FRICTIONAL — CheckedSQL pitch film

Dated log of what went wrong, what I tried, and what I did instead.

## Before 2026-10-21 — Choosing the project and writing the plan
- I wanted something a stranger can check, not something that only looks impressive, and small enough to finish
  honestly. CheckedSQL fits: every answer can be rerun and compared with a hand-checked one.
- Wrote the ten-beat plan (`beat_sheet.json`). I left beat 3's list of alternatives as a `[FILL IN]` placeholder,
  which came back to bite during the build (below).

## 2026-10-21 — Checking my own gold answers
- Ran every gold SQL query on the real Chinook database with `run_eval.py --check-gold`: all 20 ran, 0 errors.
- Running is not the same as being right. Checking my answers by hand, one turned out to be arbitrary: a gold
  question asked which year had the most invoices, and my gold query returned a single year. A `sqlite3` count of
  invoices per year shows 2009, 2010, 2011 and 2012 all tied at 83, so the query had just picked one.
  I changed it so ties are handled.
  Decision: every gold answer gets a hand check, and checker mistakes become their own failure category (beat 8).

## 2026-10-21 — Building the film with Brutalist
- **Placeholder left in the plan.** Beat 3's narration still read `[FILL IN: e.g. asking a chat assistant directly,
  and Vanna.ai]`. Claude stopped and asked rather than speak it. I chose the example text.
- **The toolkit's defaults conflict with the assignment.** The show-tell skill opens with "This is Liam, in for
  Bear" and closes on a locked @NikBearBrown outro, and its default voice is the Liam voice. The assignment says
  to narrate as myself. I dropped the house bookends (beat 10 is the only outro) and chose Kokoro `am_michael`.
- **A person is never drawn, and Professor Bear is out.** The toolkit replaces any drawn person with a Professor
  Bear photo; that is the instructor's likeness, so beat 4's reviewer is shown by what they open instead.
- **Gate B (layout) failed** the first 4K run: the "constructed" tag and two labels sat a few hundredths past the
  safe area. Moved them; re-ran.
- **A clip longer than its audio.** Beat 5's animation ran 0.65 s past its narration, which the compiler fixes by
  silently cutting both ends. Shortened the last animation; re-rendered.
- **GATE T (typography) failed** on beats 2 and 10: a short ink arrow and a scribble on a small card were read as
  35–40 px "text", under the 41 px floor. First guess (a tiny check mark) was wrong; measuring the blobs found the
  arrow. Drew the connectors grey and the scribbles taller; GATE T passed.
- **Late reveals.** Four reveals (beats 5–8) waited for their beat's last words and were on screen for under a
  second. Moved each to the start of its sentence.
- **Render-integrity check passed, with a gap.** `master_check.py` could not run its duration test because
  `clock_check.py` is missing from the toolkit. Checked it by hand instead: every clip is shorter than its audio,
  master 181.29 s vs beat sheet 181.10 s (`gate-reports/GATE-MASTER-clock-manual.md`).
- **The bookend gate fails, on purpose.** `bookend_check.py` requires the locked @NikBearBrown outro and allows no
  exemption. The assignment forbids the instructor's persona and credit line, so I left it failing rather than add it.
- **Pronunciation.** A whisper transcript of the narration matched the text, except "Yuhao" comes out close to
  "YOO-how". I listened and kept it: close enough, and re-voicing my own name would mean a phoneme hack in the toolkit.

## 2026-10-24 — Assembling the submission
- Claude drafted README, PROJECT-BRIEF, BUILD-PROMPT, SOURCES and this log from the build record; I reviewed them.
- `build_scenes.sh` had a path that only worked inside my checkout; made it read `ART_HOME` so the film rebuilds
  from any toolkit checkout (it produces a byte-identical `scenes.py`).
- The submitted `beat_sheet.json` is my plan with beat 3's placeholder replaced by the words actually spoken;
  my original working file still has the placeholder.

## Up to 2026-11-06 — Building CheckedSQL itself
- Claude rebuilt my draft script into the `checkedsql` package (read-only guard, contract check, comparator, tie
  detector, labels, report) with 25 offline tests. No API was called.
- **No API key.** I had planned to run one question on the API first, but I don't have a key. Instead of
  pretending, I chose a replay: 20 fresh Claude subagents in Claude Code, one question each, with the replies
  recorded verbatim. The first attempt failed because the temporary prompt files were deleted before the subagents
  could read them. They were rewritten to a folder that persists, and the run was repeated.
- **20/20 looked too good.** A perfect score on easy questions says little, so Claude wrote 8 deliberately wrong
  answers to test the checker. 7 were caught. The miss is question 16: every `Quantity` in Chinook is 1, so a query
  that forgets it gets the same numbers. This blind spot became the main finding, and a test locks it in.
- Published the repository: https://github.com/Femon02/checkedsql.

## 2026-11-24 — The project film (new course brief)
- **New brief.** The course email asks for four parts in order: executive summary, introduction (what others have
  done), methods, evaluation. The October pitch film didn't have a prior-work section or results, so I made a new
  film rather than patching the old one. The old one is kept in `pitch-2026-10-21/`.
- **Prior work had to be checked, not remembered.** Claude looked up the four works the film cites in their
  original papers before writing a number:
  - **BIRD:** the abstract gives ChatGPT 40.08%, not the higher GPT-4 figure that circulates elsewhere. The film
    attributes the number to "BIRD's original paper".
  - **The 2020 test-suite paper:** checked in its body text (Figure 1) that single-database evaluation "might
    create false positives".
- **Evidence instead of screenshots.** Beats 12 and 13 show CheckedSQL's real terminal output, captured on
  2026-11-24 at commit `4a3c927` and rendered as text images. They are labelled "real output", not "real screenshot".
- **Pronunciation.** Whisper hears "Zhong, Yu and Klein" as "Zhang, you and Klein". Kokoro has no pronunciation
  override, so I left the spelling correct in the captions.
- **Gates.** B01 ran 0.47 s past its audio and was shortened. GATE T failed three beats:
  - B02 and B04: handwriting squiggles too small, so they were drawn taller;
  - B10: the orange Claude Code pixel logo read as low-contrast text, and a backing plate didn't fix it, so it was
    swapped for Claude's standard mark.
  
  Everything passes except the bookend check, which fails by design, as in October.
