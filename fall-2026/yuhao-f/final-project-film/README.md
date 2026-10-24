# CheckedSQL — Final Project Pitch Film

| | |
|---|---|
| Name | Yuhao Fu |
| Course | INFO 7375 |
| Project (working title) | **CheckedSQL**: English questions to SQL on a public sample database; every query is run and checked against an answer I verified by hand |
| Target role | Software Development Engineer (SDE) |
| Film | [`checkedsql-pitch.mp4`](checkedsql-pitch.mp4) · 3 min 01 s (181.3 s) · 3840×2160, 24 fps · captions in [`checkedsql-pitch.srt`](checkedsql-pitch.srt) |
| Stack (project) | Python, SQLite (the public Chinook sample database), Claude API |
| Stack (film) | Brutalist toolkit, show-tell builder: Kokoro TTS (local), Manim, ffmpeg. Free local pipeline; no paid generation, no upload |

This is a pitch, not a build. What exists today and what will exist are listed at the end of
[`PROJECT-BRIEF.md`](PROJECT-BRIEF.md). In the film, beats 6 and 8 show real terminal screenshots dated
2026-10-21; every other picture is a drawing labelled "constructed".

## What is in this folder

| File | What it is |
|---|---|
| `checkedsql-pitch.mp4`, `checkedsql-pitch.srt` | The film and its captions |
| `PROJECT-BRIEF.md` | The seven questions answered in text, plus "exists today" / "will exist" |
| `beat_sheet.json` | My narration and visual plan (the source the film is built from) |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, third-party assets and licences |
| `FRICTIONAL.md` | Dated log of what went wrong and what I did |
| `gate-reports/` | The toolkit's quality-gate reports (start with `GATES-SUMMARY.md`) |
| `film-source/` | Everything the build needs besides the toolkit: sheet generator, scene code, caption script, the two real screenshots, the fact-check and shot list |

## How to rebuild the film

You need a checkout of the toolkit and its setup (Python 3.10+, ffmpeg, Node, the Kokoro model):

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art && ./setup --install
```

Then copy this folder's `film-source/` into the toolkit as `my-pitch/checkedsql-pitch/`, with this folder's
`beat_sheet.json` beside it at `my-pitch/beat_sheet.json`, and run the commands in
[`BUILD-PROMPT.md`](BUILD-PROMPT.md) from the toolkit root. Built with toolkit commit
`9f589eacc0e5357c9909e8d1d4c6be789843ce22`, Python 3.12.15, Manim Community 0.20.1, ffmpeg 9.0.2, kokoro-onnx 0.6.1.
The narration is regenerated locally ($0.00); the master comes out at the same length because the audio is the clock.
