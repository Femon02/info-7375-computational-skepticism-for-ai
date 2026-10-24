#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for checkedsql-pitch (show-tell builder).

Source: ../beat_sheet.json, Yuhao Fu's own pitch plan. Narration is copied VERBATIM from it.
The one change: beat 3's "[FILL IN: e.g. asking a chat assistant directly, and Vanna.ai]"
placeholder is replaced by its own example text, on Yuhao's instruction (2026-10-21).

Deviations from the show-tell house spine, set by Yuhao (the author) for this film:
  - Narration is Yuhao, first person. No Liam / Bear / Professor Bear / nbb persona, no
    instructor credit, no brand sting, no locked outro. Beat 10's narration IS the outro.
  - So the house bookends (hesitant writer, key terms, Your Turn, ClaudeTitleOutro) are left out.
  - Voice: Kokoro am_michael (neutral local voice), chosen by Yuhao.
  - Beats 6 and 8 show the REAL screenshots (dated 2026-10-21, labelled "real screenshot");
    every other image is a drawing labelled "constructed".
  - A person is never drawn (house law) and Professor Bear is excluded (Yuhao), so beat 4's
    reviewer is shown by what they open: the README, the stopwatch, the rerun.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = json.loads((HERE.parent / "beat_sheet.json").read_text())
SLUG = "checkedsql-pitch"
TITLE = "CheckedSQL — pitch"
VOICE = "am_michael"

FILL = "[FILL IN: e.g. asking a chat assistant directly, and Vanna.ai]"
FILL_WITH = "asking a chat assistant directly, and Vanna.ai"

CLASSES = {1: "B01_Hook", 2: "B02_Pipeline", 3: "B03_TwoBoxes", 4: "B04_Reviewer", 5: "B05_ThreeThings",
           6: "B06_ExistsToday", 7: "B07_Scope", 8: "B08_Risk", 9: "B09_WhyThis", 10: "B10_Close"}
REAL = {6, 8}

SPARSE = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and "
          "contrast still apply.")


def norm_box(x0, y0, x1, y1):
    """Manim coords (frame 14.222 x 8) -> normalised [x0, y0, x1, y1] (top-left origin)."""
    W, H = 14.2222, 8.0
    return [round((x0 + W / 2) / W, 4), round((H / 2 - y1) / H, 4), round((x1 + W / 2) / W, 4), round((H / 2 - y0) / H, 4)]


# Designed-type regions on the screenshot beats (everything else on those frames is the real
# screenshot, whose terminal text is image content, not authored typography). Must match scenes.py.
TYPO = {
    6: [{"label": "caption: date + real screenshot tag", "box": norm_box(-6.3, -3.75, 6.3, -2.85)},
        {"label": "exists / not yet labels", "box": norm_box(-6.3, 2.85, 6.3, 3.75)}],
    8: [{"label": "caption: date + real screenshot tag", "box": norm_box(-6.3, -3.75, 0.9, -2.85)},
        {"label": "checker label + constructed tag", "box": norm_box(1.2, -3.75, 6.3, 3.75)}],
}

beats = []
for src in SRC["beats"]:
    n = src["id"]
    text = src["narration"]
    if FILL in text:
        text = text.replace(FILL, FILL_WITH)
    assert "[" not in text and "FILL" not in text, f"beat {n}: placeholder left in narration"
    bid = f"B{n:02d}"
    b = {"beat_id": bid, "act": src["idea"], "lane": "manim", "proof_gate": "SHOW",
         "narration_text": text, "estimated_duration_s": round(len(text.split()) / 2.5, 1),
         "voice": VOICE, "engine": "kokoro",
         "image_label": "real screenshot" if n in REAL else "constructed",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": src["visual"],
                  "motion_claim": src["visual"], "on_screen_text_plan": src["on_screen_text"],
                  "manim": {"class": CLASSES[n]}}}
    qc = {"sparse_by_design": True, "sparse_reason": SPARSE}
    if n in REAL:
        b["shot"]["evidence"] = {"file": "assets/shot-check-gold-2026-10-21.png" if n == 6 else "assets/shot-tie-2026-10-21.png",
                                 "taken": "2026-10-21", "kind": "real terminal screenshot, unedited"}
        qc["typography_regions"] = TYPO[n]
        qc["typography_reason"] = ("Real terminal screenshot (2026-10-21): its text is captured image content at "
                                   "capture size, not designed typography. Only the authored caption and labels are checked.")
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
    "slug": SLUG, "title": TITLE, "topic": "CHECKEDSQL · PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "author": "Yuhao Fu", "narrator": "Yuhao Fu (first person, Kokoro am_michael)", "persona": "Yuhao Fu",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Author's rules (Yuhao Fu, 2026-10-21): a first-person project pitch; no instructor persona, "
                              "credit line, brand sting or locked outro. The spoken outro is beat 10's narration, nothing else."),
    "audience": "course reviewers and hiring managers",
    "source_doc": "my-pitch/beat_sheet.json (Yuhao Fu) + my-pitch/screenshots/ (two real terminal screenshots, 2026-10-21)",
    "tags": ["CheckedSQL", "text-to-SQL", "evaluation", "pitch"]},
    "beats": beats}
old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(beats), "beats; est", round(sum(b["estimated_duration_s"] for b in beats)), "s")
