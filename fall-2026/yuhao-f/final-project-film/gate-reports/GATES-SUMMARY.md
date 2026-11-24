# Gate summary — checkedsql-film (2026-11-24)

Master: `my-pitch/checkedsql-film/exports/landscape/checkedsql-film.mp4`
sha256 `f5ecd7db69fe62b34ffbd5f3c55483fa0be8f8c529b7914175925c652efc0e6e` · 3840×2160 · 24 fps · h264 + aac · 240.75 s

| Gate | What it checks | Result | Report |
|---|---|---|---|
| F | paperwork exists (FACTCHECK, SHOTLIST, PROMPTS) | PASS (`art run` refuses to render without it; all six runs rendered) | `run*-gates.log` |
| F (content) | every fact-check row resolved and sourced | PASS (22 rows, all 14 beats) | `GATE-F-factcheck.log` |
| L | beat-mix lint | PASS | `run6-gates.log` |
| A | static scene pre-flight, all 14 scenes | PASS (also pre-audited from a folder holding only `scenes.py`) | `run*-gates.log` |
| W | WCAG contrast, margins, text overlap | PASS | `run*-gates.log` |
| B | pixel layout audit per scene (strict) | PASS (after fixes) | `run*-gates.log`, `GATE-B-layout-audit-B04.md` |
| V | frame-level visual QC on the compiled reel | PASS, 0 BLOCKER, 0 MAJOR | `GATE-V-frame-qc.md`, `GATE-V-contact-sheet.png` |
| T | typography (size, contrast, overflow, kerning) | PASS (after fixes) | `GATE-T-TYPECHECK.md` |
| MASTER | render integrity: resolution, fps, pix_fmt, codec, audio, no review markers | PASS | `GATE-MASTER-render-integrity.md` |
| MASTER (clock) | every clip ≤ its audio; master length = beat sheet | PASS (manual: the toolkit's `clock_check.py` is missing, so the gate skipped this) | `GATE-MASTER-clock-manual.md` |
| LOUDNESS | −23.91 LUFS, true peak −4.25 dBTP, no silent beat | PASS | `GATE-LOUDNESS.md` |
| SRT | caption file valid (48 cues) | PASS | `GATE-SRT.md` |
| BOOKEND | house bookends incl. locked ClaudeTitleOutro | **FAIL, by the author's rule** | `GATE-BOOKEND.log` |

**BOOKEND.** The gate requires a `ClaudeTitleOutro` beat (@NikBearBrown sign-off) and allows no exemption. The
assignment says to narrate as myself, with no instructor persona or credit line, so the film ends on beat 14's own
narration. This failure is expected, and nothing was changed to silence it.

## Fixes made along the way
1. Stills first: overlapping labels in B02, B04, B07, B08, B09, B10 and B14 moved before any 4K render.
2. Layout audit: three labels sat past the ±6.3 safe area (B04, B07, B12); moved inside.
3. B01 ran 0.47 s longer than its audio, and the compiler would have trimmed both ends. Its last animation was
   moved earlier, and the clip was re-rendered.
4. Late reveals: the last marks in B09 and B10 were still being drawn as their beat ended. Moved to earlier phrases.
5. GATE T §8.1 on B02 and B04: handwriting squiggles read as 40 px "text" (floor 41 px), so they were drawn taller.
6. GATE T §8.3 on B10: the orange Claude Code pixel logo read as low-contrast accent text, and a dark backing
   plate didn't clear it. Replaced with Claude's standard mark (`claude-01`, which passes in B01/B08/B14),
   keeping the "Claude Code" label.
7. B10's check mark touched the "API version" label; moved above it.
