#!/usr/bin/env python3
"""make_captions.py — checkedsql-pitch.srt from the beat sheet.

Cue text is the narration, verbatim, one cue per sentence. Each beat's window is its measured audio
(actual_duration_s, in film order); inside a beat, a sentence's time is its share of the characters.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
sheet = json.loads((HERE / "beat_sheet.json").read_text())


def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


cues, t0 = [], 0.0
for b in sheet["beats"]:
    dur = float(b["actual_duration_s"])
    parts = [p for p in re.split(r"(?<=[.?!])\s+", b["narration_text"].strip()) if p]
    total = sum(len(p) for p in parts)
    t = t0
    for p in parts:
        d = dur * len(p) / total
        cues.append((t, min(t + d, t0 + dur) - 0.02, p))
        t += d
    t0 += dur

out = HERE / f"{sheet['metadata']['slug']}.srt"
out.write_text("\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1)))
print(out.name, len(cues), "cues,", round(t0, 2), "s")
