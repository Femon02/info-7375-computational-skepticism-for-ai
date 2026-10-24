# BUILD-PROMPT — how this film was built and how to rebuild it

## The prompt I gave Claude Code (2026-10-21)

The film was built by Claude Code (Claude Opus 5.5, desktop app) in the brutalist.art toolkit, from this prompt:

> Read README.md, HOW-TO.md, CLAUDE.md and skills for "show-tell" in this repo first, and follow them.
> Use the show-tell builder to make a pitch film from my-pitch/beat_sheet.json.
> Free local pipeline only: Kokoro voice, Manim/Remotion; no Higgsfield, no paid generation, no upload.
> Python is in .venv — activate it.
>
> Rules:
> - Narration is me, Yuhao Fu, speaking in first person. Use the narration text from the beat sheet exactly.
>   Do not add claims, numbers, users or results.
> - Do not name or introduce "Liam", "Bear", Professor Bear, the nbb persona, or any instructor
>   credit line, brand sting or locked outro. The spoken outro is beat 10's narration, nothing else.
> - One simple drawn image per beat, minimal labels.
> - Beats 6 and 8 must show the REAL screenshots in my-pitch/screenshots/, with their date
>   (2026-10-21) as a caption and a small "real screenshot" label.
> - Every other image is a drawing: show a small "constructed" label on it.
> - Run the toolkit's quality gates, save the reports to my-pitch/gate-reports/,
>   and if the render-integrity check fails, fix and re-render before stopping.
> - When done, tell me the output .mp4 path, the runtime, and the exact commands you ran,
>   so I can paste them into BUILD-PROMPT.md.

Claude asked two questions, and I answered:
- Beat 3 still had the placeholder `[FILL IN: e.g. asking a chat assistant directly, and Vanna.ai]`.
  I chose to speak its example: "asking a chat assistant directly, and Vanna.ai".
- Voice: Kokoro `am_michael`, a neutral local voice (not `am_onyx`, which the toolkit uses for its Liam persona).

Afterwards (2026-10-24) I asked Claude to draft the README, this file, SOURCES, FRICTIONAL and the brief from the
build record and my answers to its questions, and to assemble this folder. I reviewed them.

## Commands (run from the toolkit root, `brutalist.art/`)

Layout: this folder's `film-source/` = `my-pitch/checkedsql-pitch/`, and this folder's `beat_sheet.json` = `my-pitch/beat_sheet.json`.

```bash
source .venv/bin/activate

# 1. toolkit beat sheet from my plan (narration copied verbatim)
python3 my-pitch/checkedsql-pitch/make_sheet.py

# 2. audio first: Kokoro narration, measured durations become the clock
python3 runtime/scripts/generate_audio_kokoro.py my-pitch/checkedsql-pitch

# 3. scenes.py = show-tell drawing kit + this film's scenes
my-pitch/checkedsql-pitch/build_scenes.sh

# 4. review cut: Gates F, L, A, W, B (per scene), render at 4K, Gate V
./art run my-pitch/checkedsql-pitch --height 2160

# 5. master: GATE T, then the clean cut
./art final my-pitch/checkedsql-pitch --height 2160 --out my-pitch/checkedsql-pitch/exports/landscape

# 6. captions, then the post-master gates
python3 my-pitch/checkedsql-pitch/make_captions.py
M=my-pitch/checkedsql-pitch/exports/landscape/checkedsql-pitch.mp4
python3 runtime/scripts/master_check.py   my-pitch/checkedsql-pitch --mp4 $M
python3 runtime/scripts/loudness_check.py my-pitch/checkedsql-pitch --mp4 $M
python3 runtime/scripts/srt_check.py      my-pitch/checkedsql-pitch --srt my-pitch/checkedsql-pitch/checkedsql-pitch.srt
python3 runtime/qc/factcheck_check.py     my-pitch/checkedsql-pitch
python3 runtime/scripts/bookend_check.py  my-pitch/checkedsql-pitch   # fails by design, see FRICTIONAL.md
```

Checks done before the first 4K render, as the show-tell skill asks:

```bash
# low-resolution last frames of each scene, looked at as a contact sheet
manim -ql -s --media_dir <scratch>/m_B01_Hook my-pitch/checkedsql-pitch/scenes.py B01_Hook   # … one per scene, B01–B10
# Gate A from a folder holding only scenes.py, and the layout audit, per scene
python3 runtime/qc/static_scene_check.py <scratch>/scenes.py --class B01_Hook --quiet
python3 runtime/qc/wcag_margin_check.py my-pitch/checkedsql-pitch/scenes.py --class B01_Hook --quiet
python3 runtime/qc/manim_layout_audit.py my-pitch/checkedsql-pitch/scenes.py --class B01_Hook --curve-strict
# pronunciation check of the narration
whisper my-pitch/checkedsql-pitch/mp3/beat-B*.mp3 --model base.en --language en --output_format txt
```

After editing a scene: move its `manim/<BID>.mp4` to `_superseded/`, delete `media/videos`, and rerun steps 4–6.
`./art run` renders only scenes whose clip is missing.
