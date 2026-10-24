"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills,
and a WRITING KIT (quill, inkwell, paper, scribble lines, branching outline + the write_lines /
grow_tree animations that make the quill write). A PERSON IS NEVER AN ICON: `professor_bear(ratio, …)`
places a random Professor Bear portrait of the right aspect ratio (PROFESSOR BEAR LAW).
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ WRITING KIT (quill, ink, paper, scribble) ═════════════════════════════
# Added 2026-10-07 from Bear's two reference drawings: a quill drawing a branching outline on a
# scroll, and three scattered pages of scribbled handwriting with a quill. Use when a beat is
# about writing, drafting, authorship, notes, a manuscript, a log, a letter, a signature.
# Terracotta here is only the ink drop and the outline's nodes (dots) — never the lines.


def quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point.
    Kraft-filled feather, ink outline, a shaft line and one barb. Rotate with `angle` (radians)."""
    o = np.array([x, y, 0.0])
    def P(u, v):  # icon units (0..1) → scene, nib at origin, tip at (1, 1.1)·s
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10),
                              P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def inkwell(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    """A dark ink bottle (iso box + narrow neck) with one terracotta ink dot on the lid."""
    body = iso.box(x0, y0, z0, s, s, s * 0.9, DARK_TOP, DARK_L, DARK_R)
    neck = iso.box(x0 + s * 0.3, y0 + s * 0.3, z0 + s * 0.9, s * 0.4, s * 0.4, s * 0.25, DARK_TOP, DARK_L, DARK_R)
    drop = Dot(iso.p(x0 + s * 0.5, y0 + s * 0.5, z0 + s * 1.15), radius=0.07, color=TERRA)
    return VGroup(body, neck, drop)


def paper(x, y, w=2.4, h=3.0, tilt=0.0, fill=PAGE_TOP):
    """A flat 2-D sheet (the scattered-pages drawing): white page, ink outline, kraft drop shadow.
    `tilt` in radians. Returns a VGroup; `.sheet` is the page rectangle for placing lines on it."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(shadow, sheet)
    if tilt:
        g.rotate(tilt, about_point=[x, y, 0])
    g.sheet = sheet
    g.cx, g.cy, g.w, g.h, g.tilt = float(x), float(y), float(w), float(h), float(tilt)   # read these; never ask the stub for vertices
    return g


def scribble(x, y, w, amp=0.07, waves=None, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for `w` units. Reads as script, never as type."""
    n = waves or max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def scribble_block(x, y, w, n=3, gap=0.34, last=0.62, color=INK, sw=4):
    """`n` scribble lines stacked downward from (x, y); the last one is `last`× as long (a paragraph end)."""
    return VGroup(*[scribble(x, y - i * gap, w * (last if i == n - 1 else 1.0), color=color, sw=sw) for i in range(n)])


def scribbles_on(page, n=3, inset=0.3, gap=0.34, color=INK, sw=4):
    """Scribble lines laid on a `paper()` group, following its tilt (uses the page's stored geometry)."""
    w = page.w - 2 * inset
    g = scribble_block(page.cx - w / 2, page.cy + page.h / 2 - inset - 0.1, w, n=n, gap=gap, color=color, sw=sw)
    if abs(page.tilt) > 1e-3:
        g.rotate(page.tilt, about_point=[page.cx, page.cy, 0])
    return g


def outline_tree(x, y, h=1.6, levels=2, spread=0.55, color=INK, node=TERRA):
    """A branching outline (the scroll drawing): a trunk rising from (x, y), forking `levels` times,
    a terracotta dot at every tip. Returns VGroup(lines, dots) — draw lines first, dots last."""
    lines, dots = VGroup(), VGroup()
    def grow(px, py, length, lvl, dx):
        qx, qy = px + dx, py + length
        lines.add(Line([px, py, 0], [qx, qy, 0], color=color, stroke_width=4))
        if lvl == 0:
            dots.add(Dot([qx, qy, 0], radius=0.075, color=node))
            return
        for d in (-spread, spread):
            grow(qx, qy, length * 0.62, lvl - 1, d * (0.75 ** (levels - lvl)))
    grow(x, y, h * 0.42, levels, 0.0)
    g = VGroup(lines, dots)
    g.lines, g.dots = lines, dots
    return g


def write_lines(self, q, lines, speed=1.6, hop=0.22, dip=0.06):
    """Animate the quill `q` WRITING each line in `lines`: the nib hops to the line's start, then the
    line draws while the nib rides its tip (the writing motion). `speed` is scene units per second.
    Call between `until()` phrases so each line lands on its words. Works with the midpoint guard."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:          # Gate A's stub has no arc length; any positive number keeps the check moving
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        # the small lift between lines keeps the quill from fusing with the ink at GATE T's midpoint
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


def grow_tree(self, q, tree, per=0.45):
    """Animate the quill drawing an `outline_tree`: each segment draws as the nib rides it; dots land last."""
    for ln in tree.lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=0.18, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=per, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
    self.play(LaggedStart(*[GrowFromCenter(d) for d in tree.dots], lag_ratio=0.15), run_time=0.6)


# ═════════════════════════════ PROFESSOR BEAR (a person is never an icon) ═════════════════════════════
# PROFESSOR BEAR LAW (Bear, 2026-10-07): when a beat needs an icon of a person, or Professor Bear himself,
# do not draw a person token and do not pull a person icon. Show one of the Professor Bear portraits in
# brutalist.art/professor-bear/, chosen at random among those of the right aspect ratio (1x1 · 2x3 · 16x9).
# `./art bear <ratio> --seed <beat>` picks the same way from the shell.
def _pb_dir():
    env = _os.environ.get("ART_HOME")
    cands = [env and _os.path.join(env, "professor-bear")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "professor-bear"))
        cands.append(_os.path.join(here, "professor-bear"))
        here = _os.path.dirname(here)
    cands.append("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/professor-bear")
    for c in cands:
        if c and _os.path.isdir(c):
            return c
    return cands[-1]


_PB_RATIOS = {"1x1": (1.0, 229), "2x3": (2 / 3, 28), "16x9": (16 / 9, 13)}


def _pb_circle(path):
    """A circular cut (alpha outside the circle), cached beside the set in _crops/. Cropping is fine (Bear, 2026-10-07)."""
    from PIL import Image as _Im, ImageDraw as _Dr
    out_dir = _os.path.join(_os.path.dirname(path), "_crops"); _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, _os.path.splitext(_os.path.basename(path))[0] + "-circle.png")
    if not _os.path.exists(out):
        im = _Im.open(path).convert("RGBA"); w, h = im.size; s = min(w, h); top = max(0, (h - s) // 3)
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s))
        mask = _Im.new("L", (s, s), 0); _Dr.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
        im.putalpha(mask); im.save(out)
    return out


def professor_bear(ratio="2x3", height=3.0, seed=None, x=0.0, y=0.0, frame=True, shape="rect"):
    """A Professor Bear portrait (random within `ratio`; `seed` = the beat id for a stable pick across re-renders).
    Returns a Group: kraft drop shadow, the photo, an ink frame. Place with `x, y`; size with `height`.
    `shape="circle"` gives a round cut (use a 1x1 portrait). Cropping is fine: circle, rounded square, tight head shot."""
    import random as _random
    ar, n = _PB_RATIOS[ratio]
    k = _random.Random(str(seed) if seed is not None else None).randint(1, n)
    path = _os.path.join(_pb_dir(), f"professor-bear-{ratio}-{k:02d}.png")
    circle = shape == "circle"
    if circle:
        ar = 1.0
    w = height * ar
    if circle:
        shadow = Circle(radius=height / 2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Circle(radius=height / 2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    else:
        shadow = Rectangle(width=w, height=height, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Rectangle(width=w, height=height, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    try:
        img = ImageMobject(_pb_circle(path) if circle else path)
        img.height = height
        img.move_to([x, y, 0])
    except Exception:
        img = Rectangle(width=w, height=height, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = Group(shadow, img, border) if frame else Group(img)
    g.path = path
    return g


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)

# ═════════════════════════════ CheckedSQL pitch — film cast + scenes ═════════════════════════════
# Built by: cat <toolkit>/skills/make/show-tell/templates/iso_kit.py scene_body.py > scenes.py
# Cast, kept the whole film: the question bubble, the SQL card, the Claude mark, the database,
# the checked-answer card, the check / cross verdicts, the results ledger.
# Every drawn beat carries a small "constructed" tag; B06 and B08 show the real 2026-10-21
# screenshots with their date and a "real screenshot" tag.

_REEL = _os.path.dirname(_os.path.abspath(__file__))
_REEL_FALLBACK = "/Users/femon/brutalist.art/my-pitch/checkedsql-pitch"   # Gate A runs scenes.py from a temp copy


def _asset(name):
    for d in (_REEL, _REEL_FALLBACK):
        p = _os.path.join(d, "assets", name)
        if _os.path.exists(p):
            return p
    return _os.path.join(_REEL_FALLBACK, "assets", name)


def img(name, x, y, h):
    """A bitmap (logo or real screenshot) at (x, y), height h. Falls back to a grey plate if missing."""
    try:
        m = ImageMobject(_asset(name))
        m.height = h
        m.move_to([x, y, 0])
        return m
    except Exception:
        return Rectangle(width=h, height=h, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def tag(text="constructed", x=5.15, y=-3.1):
    return T(text, 32).move_to([x, y, 0])


def G(self, *anims, rt=0.8):
    """Play, but never across the clip midpoint (GATE T and Gate V sample there)."""
    bid = type(self).__name__.split("_")[0]
    mid = _TARGET.get(bid, 10) / 2
    now = _elapsed(self)
    if now < mid + 0.3 and now + rt > mid - 0.3:
        self.wait(max(0.02, mid + 0.32 - now))
    self.play(*anims, run_time=rt)


def bubble(x, y, w=1.7, h=1.25):
    """Speech bubble (the question) with an ink question mark beside its body, not on a terracotta fill."""
    body = RoundedRectangle(width=w, height=h, corner_radius=0.3, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    tail = Polygon([x - w * 0.25, y - h / 2 + 0.02, 0], [x - w * 0.42, y - h / 2 - 0.38, 0], [x - w * 0.05, y - h / 2 + 0.02, 0],
                   fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
    seam = Line([x - w * 0.24, y - h / 2 + 0.02, 0], [x - w * 0.06, y - h / 2 + 0.02, 0], color=CARD, stroke_width=6)
    lines = VGroup(*[Line([x - w * 0.3, y + dy, 0], [x + w * 0.3 - (0.25 if dy < 0 else 0), y + dy, 0], color=BAR1, stroke_width=5)
                     for dy in (0.18, -0.12)])
    return VGroup(tail, body, seam, lines)


def sql_card(x, y, w=1.6, h=2.0, n=4, amp=0.07):
    """The SQL query card: a flat page with handwriting-like query lines."""
    pg = paper(x, y, w, h)
    lw = w - 0.5
    lines = VGroup(*[scribble(x - lw / 2, y + h / 2 - 0.35 - i * 0.36, lw * (0.62 if i == n - 1 else 1.0), amp=amp)
                     for i in range(n)])
    return VGroup(pg, lines)


def cylinder(x, y, w=1.5, h=1.5, top=BOX_TOP, side=BOX_R):
    """The database: a kraft cylinder with an ink outline and two ring lines."""
    rx, ry = w / 2, w * 0.18
    body = VGroup(
        Rectangle(width=w, height=h, fill_color=side, fill_opacity=1, stroke_width=0).move_to([x, y, 0]),
        Ellipse(width=w, height=2 * ry, fill_color=side, fill_opacity=1, stroke_width=0).move_to([x, y - h / 2, 0]))
    edges = VGroup(Line([x - rx, y + h / 2, 0], [x - rx, y - h / 2, 0], color=INK, stroke_width=4),
                   Line([x + rx, y + h / 2, 0], [x + rx, y - h / 2, 0], color=INK, stroke_width=4),
                   Arc(radius=1, start_angle=PI, angle=PI, color=INK, stroke_width=4).stretch(rx, 0).stretch(ry, 1).move_to([x, y - h / 2 - ry / 2, 0]))
    rings = VGroup(*[Arc(radius=1, start_angle=PI, angle=PI, color=BOX_IN2, stroke_width=4).stretch(rx * 0.98, 0).stretch(ry, 1)
                     .move_to([x, y + dy - ry / 2, 0]) for dy in (h * 0.17, -h * 0.17)])
    lid = Ellipse(width=w, height=2 * ry, fill_color=top, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h / 2, 0])
    return VGroup(body, rings, edges, lid)


def cross(x, y, s=0.26, color=INK, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def arrow(a, b, color=INK, sw=5):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25, tip_length=0.2)


def ledger(x, y, marks, w=1.7, row=0.5):
    """A results file: a page with one scribble line per question and its verdict (check or cross) beside it."""
    h = row * len(marks) + 0.5
    pg = paper(x, y, w, h)
    top = y + h / 2 - 0.45
    rows, verdicts = VGroup(), VGroup()
    for i, m in enumerate(marks):
        yy = top - i * row
        rows.add(scribble(x - w / 2 + 0.22, yy, w * 0.45, amp=0.05))
        vx = x + w / 2 - 0.38
        verdicts.add(check(vx - 0.05, yy + 0.04, s=0.13, w=6) if m else cross(vx, yy, s=0.12, w=6))
    g = VGroup(pg, rows, verdicts)
    g.rows, g.verdicts = rows, verdicts
    return g


def bars(x, y, hs=(0.8, 1.4, 1.0), bw=0.42, gap=0.16):
    cols = (BAR1, BAR2, BAR1)
    g = VGroup()
    x0 = x - (len(hs) * bw + (len(hs) - 1) * gap) / 2 + bw / 2
    for i, hh in enumerate(hs):
        g.add(Rectangle(width=bw, height=hh, fill_color=cols[i % 3], fill_opacity=1, stroke_color=INK, stroke_width=3)
              .move_to([x0 + i * (bw + gap), y + hh / 2, 0]))
    half = (len(hs) * bw + (len(hs) - 1) * gap) / 2 + 0.25
    base = Line([x - half, y, 0], [x + half, y, 0], color=INK, stroke_width=4)
    return VGroup(base, g)


def stopwatch(x, y, r=1.0):
    face = Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    crown = Rectangle(width=0.3, height=0.22, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    ticks = VGroup(*[Line([x + 0.8 * r * np.sin(a), y + 0.8 * r * np.cos(a), 0], [x + 0.93 * r * np.sin(a), y + 0.93 * r * np.cos(a), 0],
                          color=BAR1, stroke_width=4) for a in np.linspace(0, 2 * PI, 12, endpoint=False)])
    hand = Line([x, y, 0], [x, y + 0.72 * r, 0], color=INK, stroke_width=6)
    hub = Dot([x, y, 0], radius=0.07, color=TERRA)
    g = VGroup(crown, face, ticks, hand, hub)
    g.hand, g.hub = hand, hub
    return g


def magnifier(x, y, r=0.6):
    ring = Circle(radius=r, stroke_color=INK, stroke_width=8, fill_color=CARD, fill_opacity=0.35).move_to([x, y, 0])
    handle = Line([x + r * 0.72, y - r * 0.72, 0], [x + r * 1.65, y - r * 1.65, 0], color=INK, stroke_width=14)
    return VGroup(ring, handle)


def window(x, y, w=2.0, h=1.5):
    """A web interface: pale panel carried by a dark title bar."""
    panel = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    bar = Rectangle(width=w, height=0.32, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.16, 0])
    lines = VGroup(*[Line([x - w * 0.35, y + dy, 0], [x + w * 0.25, y + dy, 0], color=BAR1, stroke_width=5) for dy in (0.05, -0.3)])
    return VGroup(panel, bar, lines)


def pipeline(y=1.0, s=1.0):
    """The film's pipeline: question → Claude → SQL → run (database) → compare with the checked answer → verdict."""
    xs = [-5.5, -3.35, -1.3, 0.85, 3.0, 5.35]
    g = {}
    g["q"] = bubble(xs[0], y + 0.1, 1.5, 1.1)
    g["claude"] = img("claude-01.png", xs[1], y, 1.15)
    g["sql"] = sql_card(xs[2], y, 1.25, 1.6, n=3, amp=0.09)
    g["db"] = cylinder(xs[3], y, 1.3, 1.3)
    gold = paper(xs[4] + 0.18, y - 0.12, 1.15, 1.45)
    mine = paper(xs[4] - 0.18, y + 0.12, 1.15, 1.45)
    g["cmp"] = VGroup(gold, mine, scribbles_on(mine, n=2, inset=0.22, gap=0.36))
    g["ok"] = check(xs[5] - 0.05, y + 0.75, s=0.3, w=9)
    g["bad"] = cross(xs[5], y - 0.75, s=0.27, w=9)
    half = [0.8, 0.62, 0.66, 0.7, 0.8]                       # half-widths of the five nodes
    # short connectors in grey: a short ink arrow reads as a sub-floor "text run" under GATE T
    g["arrows"] = [arrow((xs[i] + half[i] + 0.12, y), (xs[i + 1] - half[i + 1] - 0.12, y), color=BAR1, sw=7) for i in range(4)]
    g["fork"] = VGroup(arrow((xs[4] + 0.85, y + 0.2), (xs[5] - 0.45, y + 0.68)), arrow((xs[4] + 0.85, y - 0.2), (xs[5] - 0.45, y - 0.68)))
    g["xs"] = xs
    return g


# ═════════════════════════════ scenes ═════════════════════════════

class B01_Hook(Scene):
    def construct(self):
        self.add(tag())
        q = bubble(-4.3, 0.7, 2.1, 1.5)
        a = arrow((-2.9, 0.4), (-0.6, 0.4))
        card = sql_card(1.6, 0.3, 2.0, 2.5, n=4)
        G(self, GrowFromCenter(q), rt=0.6)
        G(self, GrowArrow(a), rt=0.5)
        G(self, FadeIn(card, shift=DOWN * 0.3), rt=0.6)
        lab = T("SQL", 40).move_to([1.6, -1.45, 0])
        G(self, FadeIn(lab), rt=0.4)
        until(self, "looks right")
        ok = check(3.25, 1.15, s=0.28, w=9)
        looks = T("Looks right.", 40).move_to([4.6, 0.2, 0])
        G(self, Create(ok), FadeIn(looks), rt=0.6)
        until(self, "how would you know")
        qm = T("?", 120, bold=True).move_to([1.6, 2.45, 0])
        isit = T("Is it?", 40).move_to([4.6, -0.5, 0])
        G(self, FadeIn(qm, shift=DOWN * 0.4), FadeIn(isit), rt=0.6)
        G(self, Indicate(qm, color=INK, scale_factor=1.15), rt=0.8)
        finish(self)


class B02_Pipeline(Scene):
    def construct(self):
        self.add(tag())
        p = pipeline(1.1)
        xs = p["xs"]
        labs = {k: T(t, 40).move_to([xs[i] + (0.3 if k == "q" else 0), -0.45, 0]) for k, t, i in
                (("q", "question", 0), ("sql", "SQL", 2), ("db", "run", 3), ("cmp", "compare", 4))}
        G(self, GrowFromCenter(p["q"]), FadeIn(labs["q"]), rt=0.6)
        until(self, "turns English questions")
        G(self, GrowArrow(p["arrows"][0]), FadeIn(p["claude"]), rt=0.6)
        until(self, "into SQL")
        G(self, GrowArrow(p["arrows"][1]), FadeIn(p["sql"], shift=DOWN * 0.2), FadeIn(labs["sql"]), rt=0.6)
        until(self, "runs every query")
        G(self, GrowArrow(p["arrows"][2]), FadeIn(p["db"], shift=DOWN * 0.2), FadeIn(labs["db"]), rt=0.6)
        until(self, "checks the result")
        G(self, GrowArrow(p["arrows"][3]), FadeIn(p["cmp"], shift=DOWN * 0.2), FadeIn(labs["cmp"]), rt=0.6)
        G(self, GrowArrow(p["fork"][0]), GrowArrow(p["fork"][1]), rt=0.5)
        G(self, Create(p["ok"]), Create(p["bad"]), rt=0.6)
        until(self, "GitHub repository")
        back, front = Iso(0.6, -3.0, 0.62).open_box(0, 0, 0, 2.2, 1.6, 1.1)
        gh = img("github-01.png", -1.1, -2.15, 0.95)
        repo = T("GitHub repo", 40).move_to([3.4, -2.15, 0])
        G(self, FadeIn(back), FadeIn(front), FadeIn(gh), FadeIn(repo), rt=0.6)
        until(self, "a test set")
        iso = Iso(0.6, -3.0, 0.62)
        items = [iso.page(0.25, 0.2, 0.15, 0.8, 1.1), iso.page(0.75, 0.25, 0.35, 0.8, 1.1), iso.page(1.25, 0.3, 0.55, 0.8, 1.1)]
        for it in items:
            it.set_z_index(1)
        for phrase, it in zip(("a test set", "saved results", "a failure analysis"), items):
            until(self, phrase)
            G(self, FadeIn(it, shift=DOWN * 0.5), rt=0.45)
        finish(self)


class B03_TwoBoxes(Scene):
    def construct(self):
        self.add(tag())
        il, ir = Iso(-3.6, -1.4, 0.75), Iso(2.0, -1.4, 0.75)
        lb, lf = il.open_box(0, 0, 0, 2.2, 1.8, 1.2)
        rb, rf = ir.open_box(0, 0, 0, 2.2, 1.8, 1.2)
        G(self, FadeIn(lb), FadeIn(lf), rt=0.6)
        until(self, "They generate SQL")
        lp = il.page(0.5, 0.4, 0.9, 1.0, 1.2).set_z_index(1)
        llab = T("generates SQL", 40).move_to([-3.6, -2.5, 0])
        G(self, FadeIn(lp, shift=DOWN * 0.6), FadeIn(llab), rt=0.6)
        until(self, "CheckedSQL will")
        rp = ir.page(0.5, 0.4, 0.9, 1.0, 1.2).set_z_index(1)
        led = ledger(5.05, 0.75, [1, 1, 0, 1], w=2.0)
        rlab = T("+ every failure", 40).move_to([2.6, -2.5, 0])
        G(self, FadeIn(rb), FadeIn(rf), FadeIn(rp, shift=DOWN * 0.6), FadeIn(rlab), rt=0.6)
        G(self, FadeIn(led[0]), Create(led.rows), rt=0.6)
        G(self, LaggedStart(*[Create(v) for v in led.verdicts], lag_ratio=0.3), rt=0.9)
        until(self, "its mistakes will be visible")
        bad = led.verdicts[2]
        ring = Circle(radius=0.3, color=TERRA, stroke_width=6).move_to(np.array(bad.get_center()))
        more = T("More checkable.", 44).move_to([0, 2.75, 0])
        G(self, Create(ring), FadeIn(more), rt=0.6)
        finish(self)


class B04_Reviewer(Scene):
    def construct(self):
        self.add(tag())
        readme = paper(-3.6, 0.35, 2.6, 3.2)
        lines = VGroup(*[scribble(-4.6, 1.45 - i * 0.55, 1.45, amp=0.05) for i in range(5)])
        G(self, FadeIn(readme, shift=DOWN * 0.3), rt=0.6)
        G(self, Create(lines), FadeIn(T("README", 40).move_to([-3.6, -1.75, 0])), rt=0.7)
        until(self, "In the first minute")
        sw = stopwatch(0.6, 0.45, 1.1)
        G(self, FadeIn(sw), FadeIn(T("60 s", 40).move_to([0.6, -1.15, 0])), rt=0.5)
        G(self, Rotate(sw.hand, angle=-2 * PI, about_point=np.array([0.6, 0.45, 0])), rt=2.2)
        until(self, "how many questions matched")
        marks = [1, 1, 0, 1, 0]
        vs = VGroup(*[(check(-2.75, 1.5 - i * 0.55, s=0.13, w=6) if m else cross(-2.7, 1.45 - i * 0.55, s=0.12, w=6))
                      for i, m in enumerate(marks)])
        G(self, LaggedStart(*[Create(v) for v in vs], lag_ratio=0.25), rt=1.0)
        until(self, "rerun the check")
        term = Iso(4.0, -0.6, 0.8).box(-0.9, -0.9, 0, 1.8, 1.8, 0.9, DARK_TOP, DARK_L, DARK_R)
        loop = Arc(radius=0.55, start_angle=PI * 0.6, angle=PI * 1.6, color=INK, stroke_width=7).move_to([4.0, 1.75, 0])
        tip = Dot(np.array(loop.get_end()), radius=0.1, color=TERRA)
        G(self, FadeIn(term, shift=DOWN * 0.3), FadeIn(T("rerun", 40).move_to([4.0, -1.75, 0])), rt=0.5)
        G(self, Create(loop), rt=0.6)
        G(self, GrowFromCenter(tip), rt=0.3)
        finish(self)


class B05_ThreeThings(Scene):
    def construct(self):
        self.add(tag())
        # contract: a page with a seal
        con = paper(-4.2, 0.6, 2.1, 2.6)
        con_lines = scribbles_on(con, n=4, inset=0.3, gap=0.42)
        seal = Dot([-3.55, -0.3, 0], radius=0.2, color=TERRA)
        until(self, "a prompt contract")
        G(self, FadeIn(con, shift=DOWN * 0.3), Create(con_lines), FadeIn(T("contract", 40).move_to([-4.2, -1.3, 0])), rt=0.7)
        until(self, "exactly one SELECT")
        G(self, GrowFromCenter(seal), rt=0.4)
        until(self, "verification")
        db = cylinder(0, 0.6, 1.8, 1.9)
        ok = check(1.55, 1.75, s=0.28, w=9)
        G(self, FadeIn(db, shift=DOWN * 0.3), FadeIn(T("verification", 40).move_to([0, -1.3, 0])), rt=0.6)
        until(self, "read-only database")
        G(self, Create(ok), rt=0.5)
        until(self, "and evaluation")
        ch = bars(4.2, -0.5, (0.9, 1.7, 1.25))
        G(self, Create(ch[0]), FadeIn(T("evaluation", 40).move_to([4.2, -1.3, 0])), rt=0.5)
        G(self, LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch[1]], lag_ratio=0.25), rt=0.9)
        until(self, "The evidence will be")
        line = Line([-4.6, -2.45, 0], [4.6, -2.45, 0], color=BAR1, stroke_width=5)
        dots = VGroup(*[Dot([x, -2.45, 0], radius=0.13, color=INK) for x in np.linspace(-4.2, 3.6, 7)])
        last = Dot([4.4, -2.45, 0], radius=0.13, color=TERRA)
        G(self, Create(line), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), rt=0.6)
        G(self, GrowFromCenter(last), rt=0.2)
        finish(self)


class B06_ExistsToday(Scene):
    def construct(self):
        shot = img("shot-check-gold-2026-10-21.png", 0, -0.05, 5.4)
        frame = Rectangle(width=5.4 * 2120 / 1210, height=5.4, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([0, -0.05, 0])
        date = T("2026-10-21", 36).move_to([-3.9, -3.15, 0])
        real = T("real screenshot", 32).move_to([4.6, -3.15, 0])
        self.add(date, real)
        G(self, FadeIn(shot), Create(frame), rt=0.6)
        exists = T("exists: test set, script", 36).move_to([-3.2, 3.1, 0])
        G(self, FadeIn(exists), rt=0.5)
        until(self, "a draft eval script")
        w = 5.4 * 2120 / 1210
        left, top = -w / 2, -0.05 + 2.7
        ppu = 5.4 / 1210
        hl = Rectangle(width=1440 * ppu, height=34 * ppu + 0.12, stroke_color=TERRA, stroke_width=6, fill_opacity=0)
        hl.move_to([left + 720 * ppu + 0.02, top - 18 * ppu, 0])
        G(self, Create(hl), rt=0.6)
        until(self, "all twenty ran")
        ok = check(-0.55, 3.12, s=0.18, w=7)
        G(self, Create(ok), rt=0.5)
        until(self, "The part that calls the model")
        notyet = T("not yet: model run", 36).move_to([3.6, 3.1, 0])
        G(self, FadeIn(notyet), rt=0.5)
        finish(self)


class B07_Scope(Scene):
    def construct(self):
        self.add(tag())
        heads = [T(t, 44, bold=True).move_to([x, 2.6, 0]) for t, x in (("IN", -4.2), ("OUT", 0), ("FIRST", 4.2))]
        rule = VGroup(*[Line([x, 2.1, 0], [x, -2.3, 0], color=GHOST, stroke_width=5) for x in (-2.1, 2.1)])
        G(self, FadeIn(heads[0]), Create(rule), rt=0.6)
        db = cylinder(-4.2, 0.0, 1.8, 1.9)
        ok = check(-2.95, 1.25, s=0.24, w=8)
        G(self, FadeIn(db, shift=DOWN * 0.3), rt=0.6)
        G(self, Create(ok), rt=0.4)
        until(self, "Out:")
        win = window(-0.45, 0.65, 2.0, 1.5)
        dbs = VGroup(cylinder(0.45, -0.9, 0.9, 0.85, top=GHOST, side=BAR3), cylinder(1.35, -0.9, 0.9, 0.85, top=GHOST, side=BAR3))
        G(self, FadeIn(heads[1]), FadeIn(win, shift=DOWN * 0.3), rt=0.6)
        until(self, "no web interface")
        x1 = cross(1.05, 1.15, s=0.24, w=8)
        G(self, Create(x1), rt=0.4)
        until(self, "no other databases")
        x2 = cross(-0.8, -0.9, s=0.24, w=8)
        G(self, FadeIn(dbs, shift=DOWN * 0.3), rt=0.5)
        G(self, Create(x2), rt=0.4)
        until(self, "The first piece")
        q = bubble(3.2, 1.2, 1.2, 0.9)
        G(self, FadeIn(heads[2]), GrowFromCenter(q), rt=0.6)
        until(self, "end to end")
        led = ledger(4.7, -0.55, [1], w=1.7, row=0.5)
        a = arrow((3.25, 0.5), (3.9, -0.3))
        G(self, GrowArrow(a), FadeIn(led[0]), Create(led.rows), rt=0.6)
        until(self, "a results file")
        G(self, Create(led.verdicts), rt=0.5)
        finish(self)


class B08_Risk(Scene):
    def construct(self):
        h = 4.6
        w = h * 1158 / 762
        cx, cy = -6.2 + w / 2, -0.2
        shot = img("shot-tie-2026-10-21.png", cx, cy, h)
        frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
        date = T("2026-10-21", 36).move_to([-4.9, -3.15, 0])
        real = T("real screenshot", 32).move_to([-1.3, -3.15, 0])
        self.add(date, real)
        G(self, FadeIn(shot), Create(frame), rt=0.6)
        iso = Iso(3.75, -1.9, 0.8)
        box = iso.box(-1.0, -1.0, 0, 2.0, 2.0, 1.3)
        lights = VGroup(*[Dot(iso.p(-1.0, -1.0 + f * 2.0, 0.65), radius=0.08, color=GHOST) for f in (0.3, 0.7)])
        label = T("Who checks the checker?", 36).move_to([3.7, 2.75, 0])
        con = tag("constructed", 5.15, -3.15)
        G(self, FadeIn(box, shift=DOWN * 0.3), FadeIn(lights), FadeIn(label), FadeIn(con), rt=0.6)
        until(self, "four years were tied")
        ppu = h / 762
        top, left = cy + h / 2, cx - w / 2
        hl = Rectangle(width=150 * ppu, height=118 * ppu, stroke_color=TERRA, stroke_width=6, fill_opacity=0)
        hl.move_to([left + 70 * ppu, top - 631 * ppu, 0])
        G(self, Create(hl), rt=0.6)
        until(self, "every gold answer gets checked by hand")
        mag = magnifier(2.6, 1.2, 0.6)
        G(self, FadeIn(mag), rt=0.4)
        G(self, mag.animate.shift(np.array([1.2, -0.3, 0])), rt=1.0)
        until(self, "checker mistakes")
        slip = paper(5.6, -0.2, 0.9, 1.1)
        xx = cross(5.6, -0.2, s=0.18, w=7)
        G(self, FadeIn(slip, shift=DOWN * 0.3), rt=0.4)
        G(self, Create(xx), rt=0.4)
        finish(self)


class B09_WhyThis(Scene):
    def construct(self):
        self.add(tag())
        tilt = -0.09                     # right side (learning) leans down
        piv = np.array([0.0, -1.2, 0])
        fulcrum = Polygon([0, -1.25, 0], [-0.55, -2.25, 0], [0.55, -2.25, 0], fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
        plank = Rectangle(width=10.0, height=0.22, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(piv + np.array([0, 0.11, 0]))
        have = T("have", 40).move_to([-3.4, -2.6, 0])
        learn = T("learning", 40).move_to([3.0, -2.6, 0])
        G(self, FadeIn(fulcrum), FadeIn(plank), FadeIn(have), FadeIn(learn), rt=0.6)
        until(self, "leans toward learning")
        G(self, Rotate(plank, angle=tilt, about_point=piv), rt=1.0)

        def on(u, lift):
            """Point u units along the tilted plank from the pivot, `lift` above it."""
            d = np.array([np.cos(tilt), np.sin(tilt), 0])
            nrm = np.array([-np.sin(tilt), np.cos(tilt), 0])
            return piv + d * u + nrm * (0.22 + lift)

        until(self, "something a stranger can check")
        mag = magnifier(-0.4, 2.0, 0.5)
        G(self, FadeIn(mag), rt=0.4)
        G(self, mag.animate.shift(np.array([0.8, 0, 0])), rt=0.8)
        until(self, "Python and SQL basics")
        py = img("python-01.png", *on(-4.1, 0.6)[:2], 1.2)
        sq = sql_card(*on(-2.6, 0.8)[:2], 1.2, 1.6, n=3)
        G(self, FadeIn(py, shift=DOWN * 0.5), rt=0.5)
        G(self, FadeIn(sq, shift=DOWN * 0.5), rt=0.5)
        until(self, "I don't have a repo")
        iso = Iso(-3.3, 1.45, 0.5)
        ghost_box = iso.box(-1.0, -1.0, 0, 2.0, 2.0, 1.4, CARD, CARD, CARD, sw=3)
        gh = img("github-01.png", -4.95, 1.9, 0.8)
        G(self, FadeIn(ghost_box), FadeIn(gh), rt=0.5)
        until(self, "that evidence")
        real_box = iso.box(-1.0, -1.0, 0, 2.0, 2.0, 1.4)
        G(self, FadeIn(real_box), rt=0.6)
        until(self, "calling Claude from my own code")
        cl = img("claude-01.png", *on(1.55, 0.6)[:2], 1.15)
        G(self, FadeIn(cl, shift=DOWN * 0.5), rt=0.5)
        until(self, "building a test set")
        led = ledger(*on(3.05, 1.05)[:2], [1, 0, 1], w=1.3, row=0.45)
        G(self, FadeIn(led, shift=DOWN * 0.5), rt=0.5)
        until(self, "where it fails")
        ch = bars(*on(4.5, 0.0)[:2], (0.6, 1.1, 0.8), bw=0.22, gap=0.1)
        G(self, FadeIn(ch[0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch[1]], lag_ratio=0.25), rt=0.8)
        until(self, "small on purpose")
        tape = iso.tape(-1.0, -1.0, 1.4, 2.0, 2.0, drop=0.5, t=0.18)
        G(self, FadeIn(tape), rt=0.4)
        finish(self)


class B10_Close(Scene):
    def construct(self):
        self.add(tag())
        p = pipeline(0.6)
        name = T("CheckedSQL", 64, bold=True).move_to([0, 2.65, 0])
        self.add(Group(p["q"], p["claude"], p["sql"], p["db"], p["cmp"], *p["arrows"]))
        G(self, FadeIn(name), GrowArrow(p["fork"][0]), GrowArrow(p["fork"][1]), rt=0.6)
        G(self, Create(p["ok"]), Create(p["bad"]), rt=0.5)
        until(self, "whose mistakes you can see")
        bad_c = np.array(p["bad"].get_center())
        ring = Circle(radius=0.55, color=TERRA, stroke_width=7).move_to(bad_c)
        sub = T("mistakes you can see", 44).move_to([0, -1.9, 0])
        G(self, Create(ring), FadeIn(sub), rt=0.6)
        G(self, p["fork"][1].animate.set_stroke(width=9), rt=0.4)
        finish(self)
