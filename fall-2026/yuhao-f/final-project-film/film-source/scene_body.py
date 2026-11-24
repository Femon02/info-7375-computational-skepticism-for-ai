_REEL = _os.path.dirname(_os.path.abspath(__file__))
_REEL_FALLBACK = "/Users/femon/brutalist.art/my-pitch/checkedsql-film"   # Gate A runs scenes.py from a temp copy


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


# ═════════════════════════════ extra cast for the project film ═════════════════════════════

def stack(x, y, n=6, w=1.5, h=0.22, label=None):
    """A tall stack of question pages (a benchmark): flat slabs with thin gaps."""
    g = VGroup()
    for i in range(n):
        g.add(Rectangle(width=w, height=h, fill_color=PAGE_TOP if i % 2 == 0 else PAGE_L, fill_opacity=1,
                        stroke_color=INK, stroke_width=3).move_to([x + (0.05 if i % 2 else 0), y + i * (h + 0.05), 0]))
    return g


def lock(x, y, s=0.32):
    shackle = Arc(radius=s * 0.62, start_angle=0, angle=PI, color=INK, stroke_width=7).move_to([x, y + s * 0.62, 0])
    body = RoundedRectangle(width=s * 1.9, height=s * 1.45, corner_radius=0.06, fill_color=BOX_R, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    hole = Dot([x, y + 0.02, 0], radius=0.06, color=INK)
    return VGroup(shackle, body, hole)


def key_outline(x, y, color=GHOST, sw=7):
    ring = Circle(radius=0.32, color=color, stroke_width=sw).move_to([x - 0.65, y, 0])
    shaft = Line([x - 0.33, y, 0], [x + 0.75, y, 0], color=color, stroke_width=sw)
    teeth = VGroup(Line([x + 0.45, y, 0], [x + 0.45, y - 0.25, 0], color=color, stroke_width=sw),
                   Line([x + 0.7, y, 0], [x + 0.7, y - 0.3, 0], color=color, stroke_width=sw))
    return VGroup(ring, shaft, teeth)


def note(x, y, s=0.5):
    head = Ellipse(width=s * 0.75, height=s * 0.52, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, y, 0]).rotate(0.4)
    stem = Line([x + s * 0.33, y + 0.05, 0], [x + s * 0.33, y + s * 1.5, 0], color=INK, stroke_width=6)
    flag = Line([x + s * 0.33, y + s * 1.5, 0], [x + s * 0.8, y + s * 1.05, 0], color=INK, stroke_width=6)
    return VGroup(head, stem, flag)


def meter(x, y, w=3.2, h=0.5):
    frame = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return frame


def fill_bar(frame, frac, color=BAR2):
    w, h = frame.width, frame.height
    x0 = frame.get_left()[0]
    return Rectangle(width=max(0.02, (w - 0.12) * frac), height=h - 0.12, fill_color=color, fill_opacity=1,
                     stroke_width=0).move_to([x0 + 0.06 + (w - 0.12) * frac / 2, frame.get_center()[1], 0])


def gate(x, y, h=1.6):
    posts = VGroup(Rectangle(width=0.16, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - 0.45, y, 0]),
                   Rectangle(width=0.16, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x + 0.45, y, 0]))
    beam = Rectangle(width=1.06, height=0.16, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y + h / 2, 0])
    return VGroup(posts, beam)


def evidence(self, name, h, cx, cy, iw, ih, date, kind):
    """A real image (screenshot or captured output) with an ink frame, date and tag captions."""
    w = h * iw / ih
    shot = img(name, cx, cy, h)
    frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
    return shot, frame, w


def hl_row(cx, cy, w, h, ih, y0, y1, x0=0.0, x1=1.0):
    """Terracotta outline around image rows y0..y1 (pixels of an image ih px tall), x as fractions."""
    ppu = h / ih
    top, left = cy + h / 2, cx - w / 2
    r = Rectangle(width=(x1 - x0) * w, height=(y1 - y0) * ppu + 0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0)
    return r.move_to([left + (x0 + x1) / 2 * w, top - (y0 + y1) / 2 * ppu, 0])


# ═════════════════════════════ scenes ═════════════════════════════
# Part 1 — executive summary

class B01_WhatItIs(Scene):
    def construct(self):
        self.add(tag())
        p = pipeline(0.9)
        xs = p["xs"]
        q_lab = T("question", 40).move_to([xs[0] + 0.3, -0.65, 0])
        G(self, GrowFromCenter(p["q"]), FadeIn(q_lab), rt=0.6)
        until(self, "an AI to write SQL")
        G(self, GrowArrow(p["arrows"][0]), FadeIn(p["claude"]), rt=0.6)
        G(self, GrowArrow(p["arrows"][1]), FadeIn(p["sql"], shift=DOWN * 0.2), FadeIn(T("SQL", 40).move_to([xs[2], -0.65, 0])), rt=0.6)
        until(self, "looks right")
        ok = check(xs[2] + 0.75, 2.0, s=0.22, w=8)
        G(self, Create(ok), rt=0.5)
        until(self, "CheckedSQL")
        name = T("CheckedSQL", 64, bold=True).move_to([0, 2.75, 0])
        G(self, FadeIn(name), FadeOut(ok), rt=0.6)
        until(self, "runs it on a real database")
        G(self, GrowArrow(p["arrows"][2]), FadeIn(p["db"], shift=DOWN * 0.2), FadeIn(T("run", 40).move_to([xs[3], -0.65, 0])), rt=0.6)
        until(self, "compares the answer")
        G(self, GrowArrow(p["arrows"][3]), FadeIn(p["cmp"], shift=DOWN * 0.2), FadeIn(T("compare", 40).move_to([xs[4], -0.65, 0])), rt=0.6)
        G(self, GrowArrow(p["fork"][0]), GrowArrow(p["fork"][1]), rt=0.4)
        G(self, Create(p["ok"]), Create(p["bad"]), rt=0.5)
        until(self, "checked by hand")
        hand = T("checked by hand", 40).move_to([0, -2.1, 0])
        G(self, FadeIn(hand), rt=0.4)
        finish(self)


class B02_WhyCare(Scene):
    def construct(self):
        self.add(tag())
        a = paper(-3.2, 0.4, 2.3, 2.8)
        b = paper(0.2, 0.4, 2.3, 2.8)
        la = VGroup(*[scribble(-4.0, 1.35 - i * 0.5, 1.6 if i < 3 else 1.0, amp=0.11) for i in range(4)])
        lb = VGroup(*[scribble(-0.6, 1.35 - i * 0.5, 1.6 if i < 3 else 1.0, amp=0.11) for i in range(4)])
        G(self, FadeIn(a, shift=DOWN * 0.3), FadeIn(b, shift=DOWN * 0.3), rt=0.6)
        G(self, Create(la), Create(lb), FadeIn(T("answer", 40).move_to([-3.2, -1.45, 0])), FadeIn(T("answer", 40).move_to([0.2, -1.45, 0])), rt=0.8)
        until(self, "just as confident")
        ca, cb = check(-2.35, 2.0, s=0.22, w=8), check(1.05, 2.0, s=0.22, w=8)
        G(self, Create(ca), Create(cb), rt=0.6)
        until(self, "makes those mistakes visible")
        mag = magnifier(-3.6, 0.6, 0.6)
        G(self, FadeIn(mag), rt=0.4)
        G(self, mag.animate.shift(np.array([3.6, -0.1, 0])), rt=1.0)
        bad = cross(1.05, 2.0, s=0.2, w=8)
        G(self, FadeOut(cb), Create(bad), FadeIn(T("wrong", 40).move_to([0.2, -2.15, 0])), rt=0.6)
        until(self, "checks whether the checker itself")
        iso = Iso(4.4, -1.2, 0.75)
        box = iso.box(-1.0, -1.0, 0, 2.0, 2.0, 1.3)
        lights = VGroup(*[Dot(iso.p(-1.0, -1.0 + f * 2.0, 0.65), radius=0.08, color=GHOST) for f in (0.3, 0.7)])
        G(self, FadeIn(box, shift=DOWN * 0.3), FadeIn(lights), FadeIn(T("checker", 40).move_to([4.4, -2.45, 0])), rt=0.6)
        G(self, mag.animate.move_to(np.array([4.6, 1.1, 0])), rt=1.0)
        q = T("?", 96, bold=True).move_to([5.7, 2.4, 0])
        G(self, FadeIn(q), rt=0.4)
        finish(self)


# Part 2 — introduction: what others have done

class B03_Benchmarks(Scene):
    def construct(self):
        self.add(tag())
        s1 = stack(-4.6, -1.6, n=9)
        G(self, LaggedStart(*[FadeIn(r, shift=DOWN * 0.3) for r in s1], lag_ratio=0.12), rt=1.0)
        until(self, "Spider, from 2018")
        G(self, FadeIn(T("Spider 2018", 40).move_to([-4.6, -2.35, 0])), rt=0.5)
        until(self, "ten thousand questions")
        G(self, FadeIn(T("~10k questions", 36).move_to([-4.6, 1.55, 0])), rt=0.5)
        until(self, "BIRD, from 2023")
        s2 = stack(-1.6, -1.6, n=11)
        G(self, LaggedStart(*[FadeIn(r, shift=DOWN * 0.3) for r in s2], lag_ratio=0.1), FadeIn(T("BIRD 2023", 40).move_to([-1.6, -2.35, 0])), rt=1.0)
        until(self, "over twelve thousand")
        G(self, FadeIn(T("12.7k", 36).move_to([-1.6, 2.1, 0])), rt=0.5)
        until(self, "ChatGPT got about forty percent")
        base = Line([1.4, -1.6, 0], [5.9, -1.6, 0], color=INK, stroke_width=4)
        b1 = Rectangle(width=1.1, height=4.0 * 0.40, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([2.6, -1.6 + 0.8, 0])
        gpt = img("chatgpt-01.png", 2.6, -2.25, 0.6)
        G(self, Create(base), FadeIn(gpt), rt=0.5)
        G(self, GrowFromEdge(b1, DOWN), FadeIn(T("40%", 40).move_to([2.6, 0.55, 0])), rt=0.8)
        until(self, "ninety-three percent for people")
        b2 = Rectangle(width=1.1, height=4.0 * 0.93, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([4.6, -1.6 + 1.86, 0])
        G(self, GrowFromEdge(b2, DOWN), FadeIn(T("people", 36).move_to([4.6, -2.25, 0])), rt=0.8)
        G(self, FadeIn(T("93%", 40).move_to([4.6, 2.65, 0])), FadeIn(T("per BIRD paper", 32).move_to([1.9, 2.9, 0])), rt=0.5)
        finish(self)


class B04_CheckerWrong(Scene):
    def construct(self):
        self.add(tag())
        pp = paper(-5.0, -1.2, 1.5, 1.9)
        G(self, FadeIn(pp, shift=DOWN * 0.3), Create(VGroup(*[scribble(-5.5, -0.6 - i * 0.45, 1.0, amp=0.11) for i in range(3)])), rt=0.7)
        G(self, FadeIn(T("2020 paper", 36).move_to([-5.0, -2.6, 0])), rt=0.4)
        until(self, "running a query on just one database")
        wrong = sql_card(-2.4, 1.3, 1.2, 1.5, n=3, amp=0.11)
        gold = sql_card(-2.4, -1.2, 1.2, 1.5, n=3, amp=0.11)
        G(self, FadeIn(wrong, shift=DOWN * 0.2), FadeIn(gold, shift=DOWN * 0.2), rt=0.6)
        G(self, FadeIn(T("wrong", 36).move_to([-3.85, 1.3, 0])), FadeIn(T("gold", 36).move_to([-3.75, -1.2, 0])), rt=0.4)
        db = cylinder(0.3, 0.05, 1.3, 1.3)
        a1, a2 = arrow((-1.6, 1.1), (-0.5, 0.35), color=BAR1, sw=7), arrow((-1.6, -1.0), (-0.5, -0.25), color=BAR1, sw=7)
        G(self, FadeIn(db, shift=DOWN * 0.2), GrowArrow(a1), GrowArrow(a2), rt=0.6)
        until(self, "false positive")
        r1, r2 = paper(2.5, 1.0, 1.0, 0.8), paper(2.5, -0.9, 1.0, 0.8)
        o1, o2 = arrow((1.1, 0.35), (1.9, 0.9), color=BAR1, sw=7), arrow((1.1, -0.25), (1.9, -0.8), color=BAR1, sw=7)
        G(self, GrowArrow(o1), GrowArrow(o2), FadeIn(r1), FadeIn(r2), rt=0.6)
        same = T("same answer", 36).move_to([2.5, 2.0, 0])
        G(self, FadeIn(same), Create(check(3.2, 1.0, s=0.17, w=7)), Create(check(3.2, -0.9, s=0.17, w=7)), rt=0.5)
        until(self, "test each query on many databases")
        more = VGroup(*[cylinder(4.9, y, 0.8, 0.7) for y in (1.3, 0.0, -1.3)])
        G(self, LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in more], lag_ratio=0.25), rt=0.8)
        x = cross(5.8, 1.3, s=0.18, w=7)
        G(self, Create(x), FadeIn(T("many databases", 36).move_to([4.7, -2.35, 0])), rt=0.5)
        finish(self)


class B05_Tools(Scene):
    def construct(self):
        self.add(tag())
        win = window(-2.8, 0.4, 4.2, 3.2)
        G(self, FadeIn(win, shift=DOWN * 0.3), rt=0.6)
        G(self, FadeIn(T("chat with your database", 36).move_to([-2.8, -1.65, 0])), rt=0.4)
        until(self, "chat with your database")
        q = bubble(-3.6, 0.6, 1.4, 0.95)
        G(self, GrowFromCenter(q), rt=0.5)
        until(self, "get SQL back")
        s = sql_card(-1.5, 0.15, 1.1, 1.3, n=3)
        G(self, FadeIn(s, shift=LEFT * 0.4), rt=0.6)
        until(self, "They don't hand you")
        led = ledger(3.3, 0.4, [1, 1, 1, 1], w=2.2)
        G(self, FadeIn(led[0]), rt=0.4)
        ghost_rows = VGroup(*[Line([2.45, y, 0], [3.7, y, 0], color=GHOST, stroke_width=5) for y in np.linspace(1.15, -0.35, 4)])
        G(self, Create(ghost_rows), FadeIn(T("record of wrong answers", 36).move_to([3.3, -1.65, 0])), rt=0.6)
        nx = cross(4.6, 2.05, s=0.2, w=8)
        G(self, Create(nx), rt=0.4)
        finish(self)


class B06_WhyMine(Scene):
    def construct(self):
        self.add(tag())
        big = VGroup(stack(-5.0, -1.6, n=9), stack(-3.2, -1.6, n=11))
        big.set_opacity(0.35)
        G(self, FadeIn(big), FadeIn(T("benchmarks", 36).move_to([-4.1, -2.35, 0])), rt=0.6)
        until(self, "It isn't a new benchmark")
        iso = Iso(1.3, -1.9, 0.7)
        back, front = iso.open_box(0, 0, 0, 2.2, 1.8, 1.1)
        G(self, FadeIn(back), FadeIn(front), FadeIn(T("CheckedSQL", 40, bold=True).move_to([1.6, -2.65, 0])), rt=0.6)
        until(self, "read every question")
        pages = [iso.page(0.25 + 0.5 * i, 0.25, 0.15 + 0.2 * i, 0.8, 1.0).set_z_index(1) for i in range(3)]
        G(self, LaggedStart(*[FadeIn(pg, shift=DOWN * 0.5) for pg in pages], lag_ratio=0.3), FadeIn(T("20 questions", 36).move_to([1.6, 2.5, 0])), rt=0.9)
        until(self, "check every answer")
        G(self, Create(check(3.6, 1.4, s=0.26, w=9)), rt=0.5)
        until(self, "rerun everything with one command")
        loop = Arc(radius=0.55, start_angle=PI * 0.6, angle=PI * 1.6, color=INK, stroke_width=7).move_to([4.9, 0.0, 0])
        tip = Dot(np.array(loop.get_end()), radius=0.1, color=TERRA)
        G(self, Create(loop), FadeIn(T("one command", 36).move_to([4.9, -1.05, 0])), rt=0.6)
        G(self, GrowFromCenter(tip), rt=0.3)
        until(self, "blind spots")
        mag = magnifier(0.2, 1.3, 0.45)
        G(self, FadeIn(mag), rt=0.4)
        G(self, mag.animate.shift(np.array([0.9, -0.3, 0])), rt=0.8)
        finish(self)


# Part 3 — methods

class B07_Data(Scene):
    def construct(self):
        self.add(tag())
        db = cylinder(-4.5, 0.2, 2.0, 2.0)
        n = note(-4.7, 2.1, 0.45)
        G(self, FadeIn(db, shift=DOWN * 0.3), rt=0.6)
        G(self, FadeIn(n), FadeIn(T("Chinook", 40).move_to([-4.5, -1.6, 0])), rt=0.5)
        until(self, "a made-up music store")
        G(self, FadeIn(T("public sample data", 36).move_to([-4.5, -2.3, 0])), rt=0.5)
        until(self, "twenty English questions")
        qs = VGroup(*[bubble(-1.6 + 1.05 * (i % 5), 1.6 - 1.25 * (i // 5), 0.85, 0.6) for i in range(10)])
        G(self, LaggedStart(*[GrowFromCenter(b) for b in qs], lag_ratio=0.08), FadeIn(T("20 questions", 36).move_to([0.5, 2.75, 0])), rt=1.0)
        until(self, "a gold SQL answer")
        golds = VGroup(*[sql_card(-1.6 + 1.05 * i, -1.2, 0.75, 0.95, n=2, amp=0.05) for i in range(5)])
        G(self, LaggedStart(*[FadeIn(g, shift=DOWN * 0.2) for g in golds], lag_ratio=0.12), FadeIn(T("gold SQL", 36).move_to([0.5, -2.3, 0])), rt=0.9)
        until(self, "checked every gold answer by hand")
        ticks = VGroup(*[check(-1.25 + 1.05 * i, -0.55, s=0.13, w=6) for i in range(5)])
        G(self, LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), rt=0.9)
        G(self, FadeIn(T("checked by hand", 36).move_to([4.6, -1.2, 0])), rt=0.4)
        finish(self)


class B08_Pipeline(Scene):
    def construct(self):
        self.add(tag())
        p = pipeline(0.7)
        xs = p["xs"]
        G(self, GrowFromCenter(p["q"]), rt=0.5)
        until(self, "the model sees the database schema")
        G(self, GrowArrow(p["arrows"][0]), FadeIn(p["claude"]), FadeIn(T("schema", 36).move_to([xs[1], -0.75, 0])), rt=0.6)
        until(self, "a strict contract")
        seal = Dot([xs[2] + 0.45, 0.0, 0], radius=0.18, color=TERRA)
        G(self, GrowArrow(p["arrows"][1]), FadeIn(p["sql"], shift=DOWN * 0.2), rt=0.6)
        G(self, GrowFromCenter(seal), FadeIn(T("one SELECT", 36).move_to([xs[2], -1.4, 0])), rt=0.5)
        until(self, "checks the contract")
        g = gate(xs[2], 0.7, 2.2)
        G(self, FadeIn(g), FadeIn(T("contract", 36).move_to([xs[2], 2.35, 0])), rt=0.5)
        until(self, "runs the query on a read-only copy")
        G(self, GrowArrow(p["arrows"][2]), FadeIn(p["db"], shift=DOWN * 0.2), rt=0.6)
        lk = lock(xs[3] + 0.85, 1.75, 0.26)
        G(self, FadeIn(lk), FadeIn(T("read-only", 36).move_to([xs[3], -0.75, 0])), rt=0.5)
        until(self, "five second limit")
        sw = stopwatch(xs[3] + 0.4, -2.3, 0.5)
        G(self, FadeIn(sw), FadeIn(T("5 s", 36).move_to([xs[3] + 1.35, -2.3, 0])), rt=0.5)
        G(self, Rotate(sw.hand, angle=-PI, about_point=np.array([xs[3] + 0.4, -2.3, 0])), rt=0.8)
        until(self, "compares the rows")
        G(self, GrowArrow(p["arrows"][3]), FadeIn(p["cmp"], shift=DOWN * 0.2), FadeIn(T("compare", 36).move_to([xs[4], -0.75, 0])), rt=0.6)
        G(self, GrowArrow(p["fork"][0]), GrowArrow(p["fork"][1]), rt=0.5)
        G(self, Create(p["ok"]), Create(p["bad"]), rt=0.5)
        finish(self)


class B09_CheckChecker(Scene):
    def construct(self):
        h = 4.6
        w = h * 1158 / 762
        cx, cy = -6.2 + w / 2, -0.2
        shot = img("shot-tie-2026-10-21.png", cx, cy, h)
        frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
        self.add(T("2026-10-21", 36).move_to([-4.9, -3.15, 0]), T("real screenshot", 32).move_to([-1.3, -3.15, 0]))
        iso = Iso(3.75, -1.9, 0.8)
        box = iso.box(-1.0, -1.0, 0, 2.0, 2.0, 1.3)
        lights = VGroup(*[Dot(iso.p(-1.0, -1.0 + f * 2.0, 0.65), radius=0.08, color=GHOST) for f in (0.3, 0.7)])
        G(self, FadeIn(box, shift=DOWN * 0.3), FadeIn(lights), FadeIn(T("checker", 36).move_to([3.75, 2.75, 0])),
          FadeIn(tag("constructed", 5.15, -3.15)), rt=0.6)
        until(self, "arbitrary pick between ties")
        G(self, FadeIn(shot), Create(frame), rt=0.6)
        until(self, "four years were tied")
        ppu = h / 762
        top, left = cy + h / 2, cx - w / 2
        hl = Rectangle(width=150 * ppu, height=118 * ppu, stroke_color=TERRA, stroke_width=6, fill_opacity=0)
        hl.move_to([left + 70 * ppu, top - 631 * ppu, 0])
        G(self, Create(hl), rt=0.6)
        until(self, "it runs a list")
        slips = VGroup(*[paper(2.15 + 1.05 * i, 1.75, 0.8, 0.9) for i in range(3)])
        G(self, LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in slips], lag_ratio=0.25), FadeIn(T("wrong answers", 36).move_to([3.2, 0.8, 0])), rt=0.8)
        until(self, "which should all be caught")
        xs_ = VGroup(*[cross(2.15 + 1.05 * i, 1.75, s=0.17, w=7) for i in range(3)])
        G(self, LaggedStart(*[Create(x) for x in xs_], lag_ratio=0.2), rt=0.6)
        finish(self)


class B10_Resources(Scene):
    def construct(self):
        self.add(tag())
        shelf = Rectangle(width=4.6, height=0.18, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.6, 0.35, 0])
        G(self, FadeIn(shelf), rt=0.4)
        until(self, "The code is Python and SQLite")
        py, sq = img("python-01.png", -4.7, 1.25, 1.3), img("sqlite-01.png", -2.4, 1.25, 1.9)
        G(self, FadeIn(py, shift=DOWN * 0.4), FadeIn(sq, shift=DOWN * 0.4), rt=0.6)
        until(self, "all free")
        G(self, FadeIn(T("free", 40).move_to([-3.6, -0.25, 0])), Create(check(-2.75, -0.2, s=0.18, w=7)), rt=0.5)
        until(self, "I don't have API credits yet")
        k = key_outline(-3.6, -1.6)
        G(self, Create(k), FadeIn(T("API key: not yet", 36).move_to([-3.6, -2.35, 0])), rt=0.6)
        until(self, "inside Claude Code")
        cc = img("claude-01.png", 1.0, 1.6, 1.15)
        G(self, FadeIn(cc), FadeIn(T("Claude Code", 36).move_to([1.0, 0.45, 0])), rt=0.6)
        until(self, "twenty fresh copies")
        cards = VGroup(*[RoundedRectangle(width=0.62, height=0.46, corner_radius=0.08, fill_color=CARD, fill_opacity=1,
                                          stroke_color=BAR1, stroke_width=4).move_to([3.0 + 0.7 * (i % 5), 1.9 - 0.62 * (i // 5), 0])
                           for i in range(20)])
        G(self, LaggedStart(*[GrowFromCenter(c) for c in cards], lag_ratio=0.05), FadeIn(T("20 copies", 36).move_to([4.4, -0.75, 0])), rt=1.1)
        until(self, "each seeing only the rules and one question")
        dots = VGroup(*[Dot(c.get_center(), radius=0.06, color=INK) for c in cards])
        G(self, LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.04), rt=0.9)
        until(self, "The API version is built and tested")
        iso = Iso(2.6, -3.0, 0.5)
        box = iso.box(-1.0, -1.0, 0, 2.0, 2.0, 1.1)
        G(self, FadeIn(box, shift=DOWN * 0.3), FadeIn(T("API version", 36).move_to([4.75, -2.0, 0])), rt=0.6)
        until(self, "runs with one command")
        G(self, Create(check(4.75, -1.4, s=0.17, w=7)), rt=0.4)
        finish(self)


# Part 4 — evaluation

class B11_Measure(Scene):
    def construct(self):
        self.add(tag())
        rows = [("match gold", 1.6), ("keep contract", 0.2), ("wrong caught", -1.2)]
        frames = [meter(1.2, y, 5.0, 0.6) for _, y in rows]
        labs = [T(t, 40).move_to([-3.6, y, 0]) for t, y in rows]
        until(self, "I measure three things")
        G(self, FadeIn(frames[0]), FadeIn(labs[0]), rt=0.5)
        until(self, "how many replies keep the contract")
        G(self, FadeIn(frames[1]), FadeIn(labs[1]), rt=0.5)
        until(self, "how many deliberately wrong answers")
        G(self, FadeIn(frames[2]), FadeIn(labs[2]), rt=0.5)
        until(self, "It works if every wrong answer is caught")
        full = fill_bar(frames[2], 1.0)
        G(self, GrowFromEdge(full, LEFT), rt=0.8)
        G(self, Create(check(4.3, -1.2 + 0.0, s=0.2, w=8).move_to([4.35, -0.35, 0])), FadeIn(T("works", 36).move_to([5.3, -0.35, 0])), rt=0.5)
        until(self, "It fails if a wrong answer can score as right")
        gap = Rectangle(width=0.55, height=0.48, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([3.35, -1.2, 0])
        G(self, FadeIn(gap), rt=0.4)
        G(self, Create(cross(4.35, -2.1, s=0.18, w=8)), FadeIn(T("fails", 36).move_to([5.3, -2.1, 0])), rt=0.5)
        finish(self)


class B12_FirstResult(Scene):
    def construct(self):
        iw, ih = 1512, 1240
        h = 5.4
        w = h * iw / ih
        cx, cy = 0.0, -0.15
        self.add(T("2026-11-24", 36).move_to([-4.6, -3.15, 0]), T("real output", 32).move_to([4.6, -3.15, 0]))
        shot = img("out-run-2026-11-24.png", cx, cy, h)
        frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
        G(self, FadeIn(shot), Create(frame), rt=0.6)
        until(self, "All twenty answers matched")
        hl = hl_row(cx, cy, w, h, ih, 1108, 1156, 0.02, 0.6)
        G(self, Create(hl), FadeIn(T("20 / 20 match", 40).move_to([-4.6, 3.1, 0])), rt=0.6)
        until(self, "mostly tells me my questions are easy")
        G(self, FadeIn(T("questions too easy?", 40).move_to([4.1, 3.1, 0])), rt=0.5)
        finish(self)


class B13_BlindSpot(Scene):
    def construct(self):
        iw, ih = 1676, 642
        w = 12.0
        h = w * ih / iw
        cx, cy = 0.0, -0.1
        self.add(T("2026-11-24", 36).move_to([-4.6, -3.15, 0]), T("real output", 32).move_to([4.6, -3.15, 0]))
        shot = img("out-check-wrong-2026-11-24.png", cx, cy, h)
        frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
        G(self, FadeIn(shot), Create(frame), rt=0.6)
        until(self, "seven of eight wrong answers")
        hl1 = hl_row(cx, cy, w, h, ih, 556, 602, 0.01, 0.56)
        G(self, Create(hl1), FadeIn(T("7 of 8 caught", 40).move_to([-4.3, 3.1, 0])), rt=0.6)
        until(self, "question sixteen")
        hl2 = hl_row(cx, cy, w, h, ih, 326, 372, 0.01, 0.995)
        G(self, Create(hl2), rt=0.6)
        until(self, "Every quantity in this database is one")
        G(self, FadeIn(T("every Quantity = 1", 40).move_to([3.9, 3.1, 0])), rt=0.5)
        finish(self)


class B14_Close(Scene):
    def construct(self):
        self.add(tag())
        p = pipeline(0.6)
        self.add(Group(p["q"], p["claude"], p["sql"], p["db"], p["cmp"], *p["arrows"]))
        G(self, GrowArrow(p["fork"][0]), GrowArrow(p["fork"][1]), rt=0.5)
        G(self, Create(p["ok"]), Create(p["bad"]), rt=0.5)
        until(self, "harder questions")
        new = VGroup(*[bubble(-5.5 + 1.0 * i, -1.6, 0.8, 0.55) for i in range(3)])
        G(self, LaggedStart(*[GrowFromCenter(b) for b in new], lag_ratio=0.2), FadeIn(T("harder questions", 36).move_to([-4.5, -2.5, 0])), rt=0.7)
        until(self, "quantities vary")
        dbs = VGroup(*[cylinder(0.2 + 0.95 * i, -1.65, 0.75, 0.65) for i in range(3)])
        G(self, LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in dbs], lag_ratio=0.2), FadeIn(T("new test data", 36).move_to([1.15, -2.5, 0])), rt=0.7)
        until(self, "run it on the API")
        k = key_outline(4.8, -1.65, color=INK, sw=7)
        G(self, Create(k), FadeIn(T("API", 36).move_to([4.8, -2.45, 0])), rt=0.6)
        until(self, "whose mistakes you can see")
        name = T("CheckedSQL", 64, bold=True).move_to([0, 2.65, 0])
        ring = Circle(radius=0.55, color=TERRA, stroke_width=7).move_to(np.array(p["bad"].get_center()))
        G(self, FadeIn(name), Create(ring), rt=0.6)
        until(self, "I'm Yuhao Fu")
        G(self, FadeIn(T("Yuhao Fu", 40).move_to([0, 1.85, 0])), rt=0.5)
        finish(self)
