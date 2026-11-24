# SOURCES — CheckedSQL project film

## What I made
- **The project**: CheckedSQL (https://github.com/Femon02/checkedsql). I chose it and wrote the 20 questions and their
  gold SQL. I found the tied "busiest year" answer by hand on 2026-10-21, and chose the replay approach when I had
  no API key.
- **The real screenshot** in beat 9: `film-source/assets/shot-tie-2026-10-21.png`, taken on my machine on
  2026-10-21, unedited (the same file as in the pitch film).
- **Decisions during the build**: approving the four-part plan and narration, the voice, and the
  no-persona/no-outro rule.

## What Claude contributed
- **The CheckedSQL code and tests** (see the repository's `SOURCES.md`), and the 8 deliberately wrong answers that
  found the Quantity = 1 blind spot.
- **The replayed answers**: 20 fresh Claude Opus 5.5 subagents in Claude Code, one question each
  (`replays/` in the repository).
- **The film build**, by Claude Code (Claude Opus 5.5), 2026-11-24:
  - the 14-beat narration and visual plan (`beat_sheet.json`), drafted from the repository and results and
    approved by me;
  - checking the prior-work facts against the original papers;
  - all fourteen Manim scenes (`film-source/scene_body.py`);
  - rendering the captured terminal output as images;
  - the paperwork (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `FILM-SOURCES.md`);
  - running every quality gate, and the fixes in `gate-reports/GATES-SUMMARY.md`.
- **Drafts of this folder's documents**, 2026-11-24.
- No Claude chat response is shown in the film. Beats 12 and 13 show CheckedSQL's own terminal output.

## Prior work cited in the film

| Work | Used in |
|---|---|
| Yu et al., "Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task", EMNLP 2018, https://arxiv.org/abs/1809.08887 | beat 3 |
| Li et al., "Can LLM Already Serve as A Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs" (BIRD), NeurIPS 2023, https://arxiv.org/abs/2305.03111 | beat 3 |
| Zhong, Yu, Klein, "Semantic Evaluation for Text-to-SQL with Distilled Test Suites", EMNLP 2020, https://arxiv.org/abs/2010.02840 | beats 4, 13 |
| Vanna, https://github.com/vanna-ai/vanna (MIT) | beat 5 |

## Tools and third-party assets

| Item | Used for | Licence / terms |
|---|---|---|
| brutalist.art toolkit (github.com/nikbearbrown/brutalist.art, commit `9f589ea`) | show-tell builder, drawing kit (`iso_kit.py`), compile and quality gates | Course toolkit; no licence file in the checkout |
| Kokoro-82M voice model, run with kokoro-onnx 0.6.1, voice `am_michael` | narration (local, free) | Model: Apache-2.0 (hexgrad/Kokoro-82M); kokoro-onnx: MIT |
| Manim Community 0.20.1 | every drawing and animation | MIT |
| FFmpeg 9.0.2 | encoding and assembly | LGPL/GPL |
| EB Garamond (font); Menlo (font, macOS, for the rendered terminal output) | on-screen labels; captured output images | SIL OFL 1.1; Apple system font |
| OpenAI Whisper (`base.en`) | local transcript check of the narration's pronunciation (not in the film) | MIT |
| Claude, ChatGPT, Python and SQLite logos (`icons/logos/` in the toolkit) | marks for the tools named in beats 1, 3, 8, 10, 14 | Trademarks of Anthropic, OpenAI, the Python Software Foundation, and the SQLite project (Hwaci); used only to name the tools. The toolkit says they come from a brand logo pack and states no licence |
| Chinook sample database | the project's data | MIT License, © 2008–2024 Luis Rocha (github.com/lerocha/chinook-database) |

## Data and privacy
Only public sample data (Chinook). No résumé, contacts, application tracker, private data or conversation
transcripts are in the film or this folder. The 2026-10-21 screenshot shows my terminal's user and machine name
(`femon@femondeMacBook-Pro`), and nothing else personal.
