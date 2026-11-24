# BUILD-PROMPT — how this film was built and how to rebuild it

## The prompt I gave Claude Code (2026-11-24)

The film was built by Claude Code (Claude Opus 5.5, desktop app) in the brutalist.art toolkit. I pasted the
course email "What your project film needs to show" (executive summary, introduction, methods, evaluation, in
that order) and wrote:

> 这是老师的新的作业要求，你帮我全部完成
> ("This is the teacher's new assignment brief. Please complete all of it for me.")

The same rules as my first film (`pitch-2026-10-21/BUILD-PROMPT.md`) carried over: narrate in the first person
as me, no instructor persona, credit line, brand sting or locked outro; one simple drawn image per beat; real
evidence dated and labelled, every drawing labelled "constructed"; the free local pipeline only (Kokoro, Manim);
run the quality gates and fix before stopping. Claude:
- drafted the 14-beat narration in `beat_sheet.json` from my CheckedSQL repository and results;
- checked the prior-work facts against the original papers;
- built and gated the film.

I reviewed the plan and approved it ("我都同意", "I agree to all of it").

## Commands (run from the toolkit root, `brutalist.art/`)

Layout: this folder's `film-source/` = `my-pitch/checkedsql-film/`, and this folder's `beat_sheet.json` = `my-pitch/film_beat_sheet.json`.

```bash
source .venv/bin/activate

# 0. evidence for beats 12 and 13: real CheckedSQL output (in the checkedsql repo, commit 4a3c927)
#    python -m checkedsql run --replies replays/claude-code-subagents.json  > evidence/run-replay.txt
#    python -m checkedsql check-wrong                                       > evidence/check-wrong.txt
#    then rendered as text to assets/out-*.png (Menlo, terminal colours; no other change)

# 1. toolkit beat sheet from my plan (narration copied verbatim)
python3 my-pitch/checkedsql-film/make_sheet.py

# 2. audio first: Kokoro narration, measured durations become the clock
python3 runtime/scripts/generate_audio_kokoro.py my-pitch/checkedsql-film

# 3. scenes.py = show-tell drawing kit + this film's scenes
my-pitch/checkedsql-film/build_scenes.sh

# 4. review cut: Gates F, L, A, W, B (per scene), render at 4K, Gate V
./art run my-pitch/checkedsql-film --height 2160

# 5. master: GATE T, then the clean cut
./art final my-pitch/checkedsql-film --height 2160 --out my-pitch/checkedsql-film/exports/landscape

# 6. captions, then the post-master gates
python3 my-pitch/checkedsql-film/make_captions.py
M=my-pitch/checkedsql-film/exports/landscape/checkedsql-film.mp4
python3 runtime/scripts/master_check.py   my-pitch/checkedsql-film --mp4 $M
python3 runtime/scripts/loudness_check.py my-pitch/checkedsql-film --mp4 $M
python3 runtime/scripts/srt_check.py      my-pitch/checkedsql-film --srt my-pitch/checkedsql-film/checkedsql-film.srt
python3 runtime/qc/factcheck_check.py     my-pitch/checkedsql-film
python3 runtime/scripts/bookend_check.py  my-pitch/checkedsql-film   # fails by design, see FRICTIONAL.md
```

Checks done before the first 4K render, as the show-tell skill asks:

```bash
# low-resolution last frames of each scene, looked at as a contact sheet
manim -ql -s --media_dir <scratch>/m_B01_WhatItIs my-pitch/checkedsql-film/scenes.py B01_WhatItIs   # … one per scene, B01–B14
# Gate A from a folder holding only scenes.py, and the layout audit, per scene
python3 runtime/qc/static_scene_check.py <scratch>/scenes.py --class B01_WhatItIs
python3 runtime/qc/manim_layout_audit.py my-pitch/checkedsql-film/scenes.py --class B01_WhatItIs --curve-strict
# pronunciation check of the narration
whisper my-pitch/checkedsql-film/mp3/beat-B*.mp3 --model base.en --language en --output_format txt
```

After editing a scene: move its `manim/<BID>.mp4` to `_superseded/`, move `media/videos` aside, and rerun steps 4–6.
`./art run` renders only scenes whose clip is missing.
