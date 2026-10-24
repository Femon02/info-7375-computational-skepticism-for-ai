# Gate summary — checkedsql-pitch (2026-10-21)

Master: `my-pitch/checkedsql-pitch/exports/landscape/checkedsql-pitch.mp4`
sha256 `d3dde9264a41d01f46cba8809ebeecd24ea63d654757e2c1b85c8e5b65bb8cd1` · 3840×2160 · 24 fps · h264 + aac · 181.29 s

| Gate | What it checks | Result | Report |
|---|---|---|---|
| F | paperwork exists (FACTCHECK, SHOTLIST, PROMPTS) | PASS | `run6-gates.log` |
| F (content) | every fact-check row resolved and sourced | PASS (13 rows, all 10 beats) | `GATE-F-factcheck.log` |
| L | beat-mix lint | PASS | `run6-gates.log` |
| A | static scene pre-flight, all 10 scenes | PASS | `run*-gates.log` |
| W | WCAG contrast, margins, text overlap | PASS | `run*-gates.log` |
| B | pixel layout audit per scene (strict) | PASS (after fixes) | `run*-gates.log` |
| V | frame-level visual QC on the compiled reel | PASS, 0 BLOCKER, 0 MAJOR | `GATE-V-frame-qc.md`, `GATE-V-contact-sheet.png` |
| T | typography (size, contrast, overflow, kerning) | PASS (after fix) | `GATE-T-TYPECHECK.md` |
| MASTER | render integrity: resolution, fps, pix_fmt, codec, audio, no review markers | PASS | `GATE-MASTER-render-integrity.md` |
| MASTER (clock) | every clip ≤ its audio; master length = beat sheet | PASS (manual: the toolkit's `clock_check.py` is missing, so the gate skipped this) | `GATE-MASTER-clock-manual.md` |
| LOUDNESS | −24.00 LUFS, true peak −4.47 dBTP, no silent beat | PASS | `GATE-LOUDNESS.md` |
| SRT | caption file valid (31 cues) | PASS | `GATE-SRT.md` |
| BOOKEND | house bookends incl. locked ClaudeTitleOutro | **FAIL, by the author's rule** | `GATE-BOOKEND.log` |

**BOOKEND.** The gate requires a `ClaudeTitleOutro` beat (@NikBearBrown sign-off) and allows no exemption.
Yuhao's rules forbid any locked outro or brand sting ("the spoken outro is beat 10's narration, nothing else"),
so this failure is expected. Nothing was changed to silence it.

## Fixes made along the way
1. Gate B: the "constructed" tag, the "question" label and "Who checks the checker?" sat just past the ±6.3 safe area; moved or resized them.
2. B05 ran 0.65 s longer than its audio (the compiler would have cut both ends); shortened its last animation.
3. GATE T §8.1 on B02/B10: a short ink arrow and a small-card scribble read as 35–40 px "text"; connectors redrawn grey, scribbles taller.
4. Late reveals in B05–B08 moved to the start of their sentences so they hold on screen.
