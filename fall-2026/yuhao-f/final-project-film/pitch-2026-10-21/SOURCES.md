# SOURCES — CheckedSQL pitch film

## What I made
- **The pitch itself**: the project, the seven answers, and the narration and visual plan in `beat_sheet.json`.
- **The two real screenshots** (`film-source/assets/shot-*.png`), taken on my machine on 2026-10-21, unedited:
  - `shot-check-gold-2026-10-21.png`: `run_eval.py --db Chinook_Sqlite.sqlite --check-gold`, questions 1–20
    (original `截屏2026-10-21 12.49.31.png`, sha256 `10169c01…6489`).
  - `shot-tie-2026-10-21.png`: `Gold SQL errors: 0/20`, then a `sqlite3` invoices-per-year query showing
    2009–2012 tied at 83 (original `截屏2026-10-21 12.46.54.png`, sha256 `4fac05e7…c16c`).
- **The test set**: the twenty English questions and their gold SQL answers, written by me, and the hand check of
  the results (shown in the screenshots).
- **Decisions during the build**: the beat-3 wording, the voice, the no-persona/no-outro rule, the screenshot labels.

## What Claude contributed
- `run_eval.py` (draft eval script): drafted by Claude on 2026-10-21; I ran it and checked its output by hand.
- The film build, by Claude Code (Claude Opus 5.5), 2026-10-21, following my prompt in `BUILD-PROMPT.md`:
  the toolkit beat sheet generator, all ten Manim scenes (`film-source/scene_body.py`), the caption script,
  the paperwork (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`), running every quality gate, and the fixes listed in
  `gate-reports/GATES-SUMMARY.md`.
- Drafts of `README.md`, `PROJECT-BRIEF.md`, `BUILD-PROMPT.md`, this file and `FRICTIONAL.md`, 2026-10-24,
  written from the build record and from my answers to Claude's questions; I reviewed them.
- No Claude response is shown in the film.

## Tools and third-party assets

| Item | Used for | Licence / terms |
|---|---|---|
| brutalist.art toolkit (github.com/nikbearbrown/brutalist.art, commit `9f589ea`) | show-tell builder, drawing kit (`iso_kit.py`), compile and quality gates | Course toolkit; no licence file in the checkout |
| Kokoro-82M voice model, run with kokoro-onnx 0.6.1, voice `am_michael` | narration (local, free) | Model: Apache-2.0 (hexgrad/Kokoro-82M); kokoro-onnx: MIT |
| Manim Community 0.20.1 | every drawing and animation | MIT |
| FFmpeg 9.0.2 | encoding and assembly | LGPL/GPL |
| EB Garamond (font) | on-screen labels | SIL Open Font License 1.1 |
| OpenAI Whisper (`base.en`) | local transcript check of the narration's pronunciation (not in the film) | MIT |
| Claude, GitHub and Python logos (`icons/logos/` in the toolkit) | marks for the tools named in beats 2, 9, 10 | Trademarks of Anthropic, GitHub (Microsoft) and the Python Software Foundation; used only to name the tools. The toolkit's README says they come from a brand logo pack and does not state a licence |
| Chinook sample database (`Chinook_Sqlite.sqlite`) | the public sample data in the screenshots and the project | MIT License, © 2008–2024 Luis Rocha (github.com/lerocha/chinook-database, `LICENSE.md`, checked 2026-10-24) |

## Data and privacy
Only public sample data (Chinook). No résumé, contacts, application tracker, private data or conversation
transcripts are in the film or this folder. The screenshots show my terminal's user and machine name
(`femon@femondeMacBook-Pro`) and nothing else personal.
