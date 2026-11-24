# CheckedSQL — Final Project Film

| | |
|---|---|
| Name | Yuhao Fu |
| Course | INFO 7375 |
| Project | **CheckedSQL**: an evaluation tool for AI-written SQL that also checks its own checker · code: https://github.com/Femon02/checkedsql |
| Film | [`checkedsql-film.mp4`](checkedsql-film.mp4) · 4 min 01 s (240.8 s) · 3840×2160, 24 fps · captions in [`checkedsql-film.srt`](checkedsql-film.srt) |
| Stack (project) | Python, SQLite (the public Chinook sample database), Anthropic Python SDK |
| Stack (film) | Brutalist toolkit, show-tell builder: Kokoro TTS (local), Manim, ffmpeg. Free local pipeline; no paid generation, no upload |

The film follows the course brief "What your project film needs to show", in its four parts and order:

| Part | Beats | Time | What it covers |
|---|---|---|---|
| 1. Executive summary | 1–2 | 0:00–0:32 | what CheckedSQL is, and why anyone should care |
| 2. Introduction | 3–6 | 0:32–1:43 | what others have done (Spider, BIRD, test-suite evaluation, Vanna), and why mine still matters |
| 3. Methods | 7–10 | 1:43–2:58 | data, the step-by-step pipeline, checking the checker, and what I have (and don't: API credits) |
| 4. Evaluation | 11–14 | 2:58–4:01 | what I measure, what counts as success, the real results, next steps |

The same four parts are written out in [`PROJECT-BRIEF.md`](PROJECT-BRIEF.md), with the detail in its appendix.
In the film, beat 9 shows a real terminal screenshot dated 2026-10-21, and beats 12 and 13 show real CheckedSQL
output captured on 2026-11-24. Every other picture is a drawing labelled "constructed".

## What is in this folder

| File | What it is |
|---|---|
| `checkedsql-film.mp4`, `checkedsql-film.srt` | The film and its captions |
| `PROJECT-BRIEF.md` | The four parts in text, plus an appendix with the detail |
| `beat_sheet.json` | My narration and visual plan, the source the film is built from |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, third-party assets and licences |
| `FRICTIONAL.md` | Dated log of what went wrong and what I did, for both films |
| `gate-reports/` | The toolkit's quality-gate reports (start with `GATES-SUMMARY.md`) |
| `film-source/` | Everything the build needs besides the toolkit: sheet generator, scene code, caption script, the real screenshot and captured output, the fact-check and shot list |
| `pitch-2026-10-21/` | The earlier pitch film (2026-10-21) with its own brief and build files, kept unchanged |

## How to rebuild the film

You need a checkout of the toolkit and its setup (Python 3.10+, ffmpeg, Node, the Kokoro model):

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art && ./setup --install
```

Then copy this folder's `film-source/` into the toolkit as `my-pitch/checkedsql-film/`, with this folder's
`beat_sheet.json` beside it at `my-pitch/film_beat_sheet.json`, and run the commands in
[`BUILD-PROMPT.md`](BUILD-PROMPT.md) from the toolkit root. Built with toolkit commit
`9f589eacc0e5357c9909e8d1d4c6be789843ce22`, Python 3.12.15, Manim Community 0.20.1, ffmpeg 9.0.2, kokoro-onnx 0.6.1.
The narration is regenerated locally ($0.00). The master comes out at the same length because the audio is the clock.
