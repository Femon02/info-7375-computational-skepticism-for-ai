#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for checkedsql-film (show-tell builder).

Source: ../film_beat_sheet.json, the four-part project film (course brief: executive summary,
introduction, methods, evaluation). Narration copied verbatim from it.

Deviations from the show-tell house spine, as for the 2026-10-21 pitch film (author's rules):
  - Narration is Yuhao Fu, first person. No Liam / Bear / Professor Bear / nbb persona, no
    instructor credit, no brand sting, no locked outro. Beat 14's narration IS the outro.
  - So the house bookends (hesitant writer, key terms, Your Turn, ClaudeTitleOutro) are left out.
  - Voice: Kokoro am_michael (neutral local voice), chosen by Yuhao.
  - Beat 9 shows the REAL 2026-10-21 screenshot (labelled "real screenshot"); beats 12 and 13 show
    REAL CheckedSQL output captured 2026-11-24 (labelled "real output"). Every other image is a
    drawing labelled "constructed". No person is drawn.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = json.loads((HERE.parent / "film_beat_sheet.json").read_text())
SLUG = "checkedsql-film"
TITLE = "CheckedSQL — project film"
VOICE = "am_michael"

CLASSES = {1: "B01_WhatItIs", 2: "B02_WhyCare", 3: "B03_Benchmarks", 4: "B04_CheckerWrong", 5: "B05_Tools",
           6: "B06_WhyMine", 7: "B07_Data", 8: "B08_Pipeline", 9: "B09_CheckChecker", 10: "B10_Resources",
           11: "B11_Measure", 12: "B12_FirstResult", 13: "B13_BlindSpot", 14: "B14_Close"}
EVIDENCE = {9: ("assets/shot-tie-2026-10-21.png", "2026-10-21", "real terminal screenshot, unedited"),
            12: ("assets/out-run-2026-11-24.png", "2026-11-24", "real CheckedSQL stdout (evidence/run-replay.txt), rendered as text"),
            13: ("assets/out-check-wrong-2026-11-24.png", "2026-11-24", "real CheckedSQL stdout (evidence/check-wrong.txt), rendered as text")}

SPARSE = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and "
          "contrast still apply.")


def norm_box(x0, y0, x1, y1):
    """Manim coords (frame 14.222 x 8) -> normalised [x0, y0, x1, y1] (top-left origin)."""
    W, H = 14.2222, 8.0
    return [round((x0 + W / 2) / W, 4), round((H / 2 - y1) / H, 4), round((x1 + W / 2) / W, 4), round((H / 2 - y0) / H, 4)]


# Designed-type regions on the evidence beats; the rest of those frames is captured terminal text. Must match scenes.
TYPO = {
    9: [{"label": "caption: date + real screenshot tag", "box": norm_box(-6.3, -3.75, 0.9, -2.85)},
        {"label": "drawn checker + labels + constructed tag", "box": norm_box(1.2, -3.75, 6.3, 3.75)}],
    12: [{"label": "caption: date + real output tag", "box": norm_box(-6.3, -3.75, 6.3, -2.85)},
         {"label": "heading label", "box": norm_box(-6.3, 2.85, 6.3, 3.75)}],
    13: [{"label": "caption: date + real output tag", "box": norm_box(-6.3, -3.75, 6.3, -2.85)},
         {"label": "heading label", "box": norm_box(-6.3, 2.85, 6.3, 3.75)}],
}

beats = []
for src in SRC["beats"]:
    n = src["id"]
    text = src["narration"]
    bid = f"B{n:02d}"
    b = {"beat_id": bid, "act": f"{src['part']} · {src['idea']}", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": text, "estimated_duration_s": round(len(text.split()) / 2.5, 1),
         "voice": VOICE, "engine": "kokoro", "image_label": src["label"],
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": src["visual"],
                  "motion_claim": src["visual"], "manim": {"class": CLASSES[n]}}}
    qc = {"sparse_by_design": True, "sparse_reason": SPARSE}
    if n in EVIDENCE:
        f, taken, kind = EVIDENCE[n]
        b["shot"]["evidence"] = {"file": f, "taken": taken, "kind": kind}
        qc["typography_regions"] = TYPO[n]
        qc["typography_reason"] = ("Real terminal text (screenshot or captured stdout): image content, not designed "
                                   "typography. Only the authored caption and labels are checked.")
        qc["typography_fill"] = "#F2F0E9"
    b["qc"] = qc
    beats.append(b)

# carry measured audio forward across re-runs (SKILL: make_sheet must keep audio_file + actual_duration_s)
old = HERE / "beat_sheet.json"
if old.exists():
    prev = {b["beat_id"]: b for b in json.loads(old.read_text()).get("beats", [])}
    for b in beats:
        p = prev.get(b["beat_id"], {})
        if p.get("narration_text") == b["narration_text"]:
            for k in ("audio_file", "actual_duration_s"):
                if k in p:
                    b[k] = p[k]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "CHECKEDSQL · PROJECT FILM", "skill": "show-tell", "style_preset": "show-tell",
    "author": "Yuhao Fu", "narrator": "Yuhao Fu (first person, Kokoro am_michael)", "persona": "Yuhao Fu",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Author's rules (Yuhao Fu): a first-person project film; no instructor persona, credit line, "
                              "brand sting or locked outro. The spoken outro is beat 14's narration, nothing else."),
    "audience": "course reviewers and hiring managers",
    "source_doc": "my-pitch/film_beat_sheet.json (Yuhao Fu) + real evidence in assets/ and evidence/",
    "tags": ["CheckedSQL", "text-to-SQL", "evaluation", "project film"]},
    "beats": beats}
old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(beats), "beats; est", round(sum(b["estimated_duration_s"] for b in beats)), "s")
