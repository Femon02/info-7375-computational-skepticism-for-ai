
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
