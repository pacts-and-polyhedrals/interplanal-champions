"""Avernus props for Interplanal Champions. Each returns SVG around (0,0) in pixels (100 px = 5 ft)."""
import math, random
from mapkit import INK
from props import rect, _s


def rock(r=60, seed=0, fill=None, light=None):
    q = random.Random(seed)
    fill = fill or q.choice(["#c9a58a", "#b8937a", "#d2b296", "#a88a76"])
    light = light or "#ecd6c0"
    n = q.randint(7, 10)
    pts = []
    for i in range(n):
        a = i * 2 * math.pi / n + q.uniform(-0.25, 0.25)
        d = r * q.uniform(0.7, 1.05)
        pts.append((math.cos(a) * d, math.sin(a) * d * q.uniform(0.75, 1.0)))
    p = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    hl = " ".join(f"{x*0.55-r*0.12:.0f},{y*0.5-r*0.15:.0f}" for x, y in pts[: n // 2 + 1])
    return (f'<polygon points="{p}" fill="{fill}" {_s(6)} stroke-linejoin="round"/>'
            f'<polyline points="{hl}" fill="none" stroke="{light}" stroke-width="{max(4, r/10):.0f}" stroke-linecap="round" opacity="0.7"/>'
            f'<path d="M{-r*0.2:.0f} {r*0.1:.0f} l{r*0.3:.0f} {r*0.25:.0f}" stroke="{INK}" stroke-width="3" opacity="0.5"/>')


def darkrock(r=60, seed=0):
    return rock(r, seed, fill=random.Random(seed).choice(["#4a4650", "#3e3a44", "#55505c"]), light="#7a7682")


def pebbles(n=10, spread=60, seed=0, dark=False):
    q = random.Random(seed)
    cols = ["#3a3440", "#2a2630", "#4a4450"] if dark else ["#c9a58a", "#a88a76", "#3a2a26", "#d2b296"]
    return "".join(f'<circle cx="{q.uniform(-spread,spread):.0f}" cy="{q.uniform(-spread,spread):.0f}" r="{q.uniform(4,11):.0f}" fill="{q.choice(cols)}" {_s(2)}/>' for _ in range(n))


def bone(l=40, rot=0):
    return (f'<g transform="rotate({rot})"><rect x="{-l/2}" y="-4" width="{l}" height="8" rx="4" fill="#e8dcc0" {_s(2.5)}/>'
            f'<circle cx="{-l/2}" cy="-5" r="6" fill="#e8dcc0" {_s(2.5)}/><circle cx="{-l/2}" cy="5" r="6" fill="#e8dcc0" {_s(2.5)}/>'
            f'<circle cx="{l/2}" cy="-5" r="6" fill="#e8dcc0" {_s(2.5)}/><circle cx="{l/2}" cy="5" r="6" fill="#e8dcc0" {_s(2.5)}/></g>')


def skull(s=1.0):
    return (f'<g transform="scale({s})"><path d="M-16 -4 C-16 -24 16 -24 16 -4 C16 6 10 10 8 16 L-8 16 C-10 10 -16 6 -16 -4 Z" fill="#ece2c8" {_s(3)}/>'
            f'<circle cx="-7" cy="-4" r="5" fill="{INK}"/><circle cx="7" cy="-4" r="5" fill="{INK}"/><path d="M-2 6 l2 -4 l2 4 Z" fill="{INK}"/></g>')


def bones(n=6, spread=50, seed=0, skulls=1):
    q = random.Random(seed)
    s = "".join(f'<g transform="translate({q.uniform(-spread,spread):.0f},{q.uniform(-spread,spread):.0f})">{bone(q.uniform(26,50), q.uniform(0,180))}</g>' for _ in range(n))
    s += "".join(f'<g transform="translate({q.uniform(-spread,spread):.0f},{q.uniform(-spread,spread):.0f}) rotate({q.uniform(-40,40):.0f})">{skull(q.uniform(0.8,1.1))}</g>' for _ in range(skulls))
    return s


def skeleton(seed=0):
    q = random.Random(seed)
    ribs = "".join(f'<path d="M-14 {-20+i*8} q-14 4 -18 12 M14 {-20+i*8} q14 4 18 12" stroke="#e8dcc0" stroke-width="5" fill="none"/>' for i in range(4))
    return (f'<g transform="rotate({q.uniform(0,360):.0f})"><line x1="0" y1="-30" x2="0" y2="30" stroke="{INK}" stroke-width="9"/>'
            f'<line x1="0" y1="-30" x2="0" y2="30" stroke="#e8dcc0" stroke-width="5"/>{ribs}'
            f'<g transform="translate(0,-46)">{skull(0.9)}</g><g transform="translate(-24,46)">{bone(46, 70)}</g>'
            f'<g transform="translate(24,46)">{bone(46, 110)}</g><g transform="translate(-30,-12)">{bone(40, 150)}</g><g transform="translate(30,-12)">{bone(40, 30)}</g></g>')


def _bonestroke(d, w):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+9:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#e2d6ba" stroke-width="{w:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#fff6e0" stroke-width="{max(2,w*0.25):.0f}" stroke-linecap="round" stroke-linejoin="round" opacity="0.6" transform="translate(-2,-2)"/>')


def dragon_skeleton(L=1000, k=1.0):
    """A wyrm skeleton lying along the x-axis: skull at the left, tail to the right (L px long)."""
    out = []
    sx0, sx1 = -L * 0.38, L * 0.5
    spine = lambda x: 10 * math.sin((x - sx0) / L * 7)
    # wing membranes (under everything)
    for sgn in (-1, 1):
        sh = (-L * 0.12, sgn * 22)
        el = (-L * 0.02, sgn * L * 0.2)
        wr = (L * 0.1, sgn * L * 0.3)
        tips = [(wr[0] + L * 0.05 + i * L * 0.07, sgn * (L * 0.42 - i * L * 0.08)) for i in range(4)]
        poly = [sh, el, wr] + tips + [(L * 0.14, sgn * 40)]
        pp = " ".join(f"{x:.0f},{y:.0f}" for x, y in poly)
        out.append(f'<polygon points="{pp}" fill="#6a3424" opacity="0.28" stroke="#3a1a10" stroke-width="3" stroke-dasharray="30 12"/>')
        out.append(_bonestroke(f"M{sh[0]:.0f} {sh[1]:.0f} L{el[0]:.0f} {el[1]:.0f} L{wr[0]:.0f} {wr[1]:.0f}", 16))
        for t in tips:
            out.append(_bonestroke(f"M{wr[0]:.0f} {wr[1]:.0f} L{t[0]:.0f} {t[1]:.0f}", 7))
        for lx, ln in ((-L * 0.17, 1), (L * 0.2, 1.1)):  # legs
            kx, ky = lx - 40, sgn * 110 * ln
            out.append(_bonestroke(f"M{lx:.0f} {sgn*14:.0f} L{kx:.0f} {ky:.0f} L{kx+55:.0f} {ky+sgn*55:.0f}", 13))
            for c in (-18, 0, 18):
                out.append(_bonestroke(f"M{kx+55:.0f} {ky+sgn*55:.0f} l{20+c*0.3:.0f} {sgn*(18+abs(c)*0.3)+c:.0f}", 5))
    # ribs
    for i in range(11):
        x = -L * 0.16 + i * L * 0.032
        h = 105 * math.sin(math.pi * (i + 1) / 12) + 20
        for sgn in (-1, 1):
            out.append(_bonestroke(f"M{x:.0f} {spine(x):.0f} C{x+10:.0f} {sgn*h*0.5:.0f} {x+30:.0f} {sgn*h*0.95:.0f} {x+50:.0f} {sgn*h:.0f}", 9))
    # spine (vertebra beads, tapering)
    n = 46
    for i in range(n):
        t = i / (n - 1)
        x = sx0 + (sx1 - sx0) * t
        r = 16 * (1 - t) ** 0.6 + 4 if t > 0.3 else 13 + 6 * math.sin(t / 0.3 * math.pi / 2)
        out.append(f'<ellipse cx="{x:.0f}" cy="{spine(x):.0f}" rx="{r*0.8:.1f}" ry="{r:.1f}" fill="#e2d6ba" stroke="{INK}" stroke-width="4"/>')
        if i % 2 == 0 and t < 0.75:
            out.append(f'<path d="M{x:.0f} {spine(x)-r:.0f} l6 -{r*0.6:.0f}" stroke="{INK}" stroke-width="4"/>')
    # pelvis and shoulders
    out.append(f'<ellipse cx="{L*0.2:.0f}" cy="0" rx="42" ry="30" fill="#d8ccae" stroke="{INK}" stroke-width="6"/><circle cx="{L*0.2-14:.0f}" cy="-8" r="9" fill="#3a2a22"/><circle cx="{L*0.2-14:.0f}" cy="8" r="9" fill="#3a2a22"/>')
    # skull
    hx = sx0 - 10
    out.append(f'<path d="M{hx:.0f} -46 Q{hx-60:.0f} -54 {hx-130:.0f} -30 L{hx-205:.0f} -12 Q{hx-220:.0f} 0 {hx-205:.0f} 12 L{hx-130:.0f} 30 Q{hx-60:.0f} 54 {hx:.0f} 46 Q{hx+30:.0f} 0 {hx:.0f} -46 Z" fill="#e2d6ba" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    out.append(f'<path d="M{hx-30:.0f} -30 Q{hx-80:.0f} -20 {hx-150:.0f} -10" stroke="#b8aa8a" stroke-width="8" fill="none"/>')
    out.append(f'<ellipse cx="{hx-55:.0f}" cy="-22" rx="18" ry="10" fill="#2a1410" stroke="{INK}" stroke-width="3"/><ellipse cx="{hx-55:.0f}" cy="22" rx="18" ry="10" fill="#2a1410" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<ellipse cx="{hx-185:.0f}" cy="-7" rx="7" ry="4" fill="#2a1410"/><ellipse cx="{hx-185:.0f}" cy="7" rx="7" ry="4" fill="#2a1410"/>')
    for sgn in (-1, 1):
        out.append(_bonestroke(f"M{hx-20:.0f} {sgn*38:.0f} Q{hx+30:.0f} {sgn*70:.0f} {hx+80:.0f} {sgn*62:.0f}", 12))
        out.append(_bonestroke(f"M{hx-40:.0f} {sgn*40:.0f} Q{hx:.0f} {sgn*90:.0f} {hx+30:.0f} {sgn*100:.0f}", 7))
        for tt in range(5):
            out.append(f'<path d="M{hx-90-tt*22:.0f} {sgn*(27-tt*3):.0f} l-4 {sgn*10}" stroke="#fff6e0" stroke-width="4"/>')
    return "".join(out)


def ruin_blocks(pts, seed=0, w=88, seg=105):
    """Chunky irregular stone blocks along a polyline (pixel coordinates), for broken ruins."""
    q = random.Random(seed)
    out = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        n = max(1, round(L / seg))
        for i in range(n):
            t = (i + 0.5) / n
            cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            bl = L / n - 6
            ww = w * q.uniform(0.85, 1.1)
            c = q.choice(["#6e6a74", "#77737e", "#65616c", "#807c86", "#5e5a64"])
            j = lambda: q.uniform(-9, 9)
            poly = [(-bl/2+j(), -ww/2+j()), (-bl/6+j(), -ww/2+j()*0.5), (bl/2+j(), -ww/2+j()), (bl/2+j(), ww/2+j()),
                    (bl/5+j(), ww/2+j()*0.5), (-bl/2+j(), ww/2+j())]
            pp = " ".join(f"{a:.0f},{b:.0f}" for a, b in poly)
            hl = f"{poly[0][0]+10:.0f},{poly[0][1]+12:.0f} {poly[1][0]:.0f},{poly[1][1]+12:.0f} {poly[2][0]-10:.0f},{poly[2][1]+12:.0f}"
            out.append(f'<g transform="translate({cx:.0f},{cy:.0f}) rotate({ang+q.uniform(-5,5):.1f})">'
                       f'<polygon points="{pp}" fill="{c}" {_s(7)} stroke-linejoin="round"/>'
                       f'<polyline points="{hl}" fill="none" stroke="#a8a4b0" stroke-width="9" stroke-linecap="round" opacity="0.75"/>'
                       f'<path d="M{-bl/4:.0f} {-ww/2+18:.0f} l{q.uniform(5,20):.0f} {ww*0.35:.0f} l{q.uniform(-10,10):.0f} {ww*0.3:.0f}" stroke="{INK}" stroke-width="3.5" fill="none" opacity="0.55"/>'
                       f'<path d="M{bl/6:.0f} {ww/2-14:.0f} h{bl*0.25:.0f}" stroke="#4a4650" stroke-width="5" opacity="0.6"/></g>')
            if q.random() < 0.35:  # fallen chunk
                ox, oy = q.uniform(-60, 60), q.choice([-1, 1]) * q.uniform(60, 90)
                out.append(f'<g transform="translate({cx+ox:.0f},{cy+oy:.0f}) rotate({q.uniform(0,90):.0f})"><polygon points="-18,-14 16,-18 20,12 -14,16" fill="{c}" {_s(4)}/></g>')
    return "".join(out)


def chest(w=70, open_=False):
    s = (f'<rect x="{-w/2}" y="{-w*0.32:.0f}" width="{w}" height="{w*0.64:.0f}" rx="6" fill="#8a5a2e" {_s(5)}/>'
         f'<rect x="{-w/2}" y="{-w*0.32:.0f}" width="{w}" height="{w*0.2:.0f}" rx="5" fill="#a86c34" {_s(4)}/>'
         f'<rect x="{-w/2+8}" y="{-w*0.32:.0f}" width="8" height="{w*0.64:.0f}" fill="#4a4650" {_s(2)}/>'
         f'<rect x="{w/2-16}" y="{-w*0.32:.0f}" width="8" height="{w*0.64:.0f}" fill="#4a4650" {_s(2)}/>'
         f'<rect x="-7" y="-4" width="14" height="14" fill="#e8c35a" {_s(2)}/>')
    if open_:
        s += f'<ellipse cx="0" cy="0" rx="{w*0.35:.0f}" ry="{w*0.18:.0f}" fill="#ffd84a" opacity="0.9"/>'
    return s


def magic_circle(r=150, color="#e0283a", star=5, glow=True, runes=True, inverted=False):
    out = []
    if glow:
        out.append(f'<circle r="{r*1.25:.0f}" fill="{color}" opacity="0.18" filter="url(#glow)"/>')
    out.append(f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="16"/><circle r="{r}" fill="none" stroke="{color}" stroke-width="8"/>')
    out.append(f'<circle r="{r*0.82:.0f}" fill="none" stroke="{color}" stroke-width="5"/>')
    pts = []
    for i in range(star):
        a = -math.pi / 2 + i * 2 * math.pi / star + (math.pi if inverted else 0)
        pts.append((math.cos(a) * r * 0.8, math.sin(a) * r * 0.8))
    k = 2 if star in (5, 7) else (4 if star == 9 else 3)
    order = [pts[(i * k) % star] for i in range(star)] + [pts[0]]
    out.append(f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in order)}" fill="none" stroke="{color}" stroke-width="5" stroke-linejoin="round"/>')
    if runes:
        q = random.Random(int(r) + star)
        for i in range(18):
            a = i * 2 * math.pi / 18
            x, y = math.cos(a) * r * 0.91, math.sin(a) * r * 0.91
            out.append(f'<path d="M{x-6:.0f} {y-6:.0f} l{q.choice([6,12])} {q.choice([6,12])} m-12 0 l6 -6" stroke="{color}" stroke-width="3" fill="none"/>')
    return "".join(out)


def spawn_disk(r=70):
    return (f'<circle r="{r*1.4:.0f}" fill="#4aa0ff" opacity="0.2" filter="url(#glow)"/>'
            f'<circle r="{r}" fill="#20385a" {_s(8)}/><circle r="{r*0.78:.0f}" fill="none" stroke="#7ac0ff" stroke-width="6"/>'
            f'<circle r="{r*0.5:.0f}" fill="#4a8ad0" stroke="#bfe0ff" stroke-width="4"/>'
            + "".join(f'<rect x="-6" y="{-r-6}" width="12" height="20" fill="#bfe0ff" {_s(2)} transform="rotate({i*45})"/>' for i in range(8)))


def face_rock(r=380):
    """A colossal carved face rising out of the lava (the 'rock island')."""
    return (f'<ellipse rx="{r*0.92:.0f}" ry="{r*1.08:.0f}" fill="#2a2a30" {_s(10)}/>'
            f'<ellipse rx="{r*0.82:.0f}" ry="{r:.0f}" fill="#9a8270" {_s(10)}/>'
            f'<path d="M{r*0.1:.0f} {-r:.0f} Q{r*0.95:.0f} {-r*0.6:.0f} {r*0.75:.0f} {r*0.4:.0f} Q{r*0.5:.0f} {r*0.95:.0f} 0 {r:.0f} Q{r*0.6:.0f} {r*0.4:.0f} {r*0.1:.0f} {-r:.0f} Z" fill="#7a6252" opacity="0.6"/>'
            f'<path d="M{-r*0.7:.0f} {-r*0.3:.0f} Q0 {-r*1.25:.0f} {r*0.7:.0f} {-r*0.3:.0f}" fill="#b49a84" stroke="none"/>'
            f'<path d="M{-r*0.62:.0f} {-r*0.32:.0f} Q{-r*0.3:.0f} {-r*0.5:.0f} {-r*0.05:.0f} {-r*0.3:.0f}" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<path d="M{r*0.05:.0f} {-r*0.3:.0f} Q{r*0.3:.0f} {-r*0.5:.0f} {r*0.62:.0f} {-r*0.32:.0f}" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{-r*0.33:.0f}" cy="{-r*0.12:.0f}" rx="{r*0.17:.0f}" ry="{r*0.09:.0f}" fill="#2a1a14" {_s(6)}/>'
            f'<ellipse cx="{r*0.33:.0f}" cy="{-r*0.12:.0f}" rx="{r*0.17:.0f}" ry="{r*0.09:.0f}" fill="#2a1a14" {_s(6)}/>'
            f'<path d="M0 {-r*0.1:.0f} L{-r*0.12:.0f} {r*0.25:.0f} L{r*0.12:.0f} {r*0.25:.0f} Z" fill="#8a7262" {_s(6)}/>'
            f'<path d="M{-r*0.32:.0f} {r*0.45:.0f} Q0 {r*0.32:.0f} {r*0.32:.0f} {r*0.45:.0f} Q0 {r*0.85:.0f} {-r*0.32:.0f} {r*0.45:.0f} Z" fill="#3a1410" {_s(8)}/>'
            + "".join(f'<rect x="{-r*0.22 + i*r*0.11:.0f}" y="{r*0.42:.0f}" width="{r*0.08:.0f}" height="{r*0.1:.0f}" fill="#e8dcc0" {_s(3)}/>' for i in range(5))
            + f'<path d="M{r*0.1:.0f} {-r*0.95:.0f} l{-r*0.08:.0f} {r*0.4:.0f} l{r*0.12:.0f} {r*0.3:.0f} l{-r*0.06:.0f} {r*0.5:.0f}" stroke="{INK}" stroke-width="8" fill="none"/>'
            f'<path d="M{-r*0.6:.0f} {r*0.2:.0f} q{r*0.1:.0f} {r*0.2:.0f} {r*0.05:.0f} {r*0.4:.0f}" stroke="#6a5444" stroke-width="10" fill="none"/>')


def ferry(w=360, h=130):
    return (f'<path d="M{-w/2} {-h/2} L{w/2-40} {-h/2} Q{w/2} 0 {w/2-40} {h/2} L{-w/2} {h/2} Z" fill="#3a2a22" {_s(7)}/>'
            + "".join(f'<line x1="{-w/2+20}" y1="{-h/2+20+i*22}" x2="{w/2-50}" y2="{-h/2+20+i*22}" stroke="#55402e" stroke-width="12"/>' for i in range(4))
            + f'<rect x="{-w/2+20}" y="-10" width="60" height="20" fill="#1a1012" {_s(3)}/>'
            f'<line x1="{-w/2-30}" y1="-80" x2="{w/2}" y2="70" stroke="{INK}" stroke-width="12"/><line x1="{-w/2-30}" y1="-80" x2="{w/2}" y2="70" stroke="#8a6a3a" stroke-width="6"/>'
            f'<circle cx="{w/2-70}" cy="-20" r="18" fill="#7ad0a0" {_s(4)}/><circle cx="{w/2-70}" cy="-20" r="40" fill="#7ad0a0" opacity="0.2"/>')


def platform(w=160, h=120, seed=0):
    q = random.Random(seed)
    pts = [(-w / 2 + q.uniform(-10, 10), -h / 2 + q.uniform(-10, 10)), (w / 2 + q.uniform(-10, 10), -h / 2 + q.uniform(-10, 10)),
           (w / 2 + q.uniform(-10, 10), h / 2 + q.uniform(-10, 10)), (-w / 2 + q.uniform(-10, 10), h / 2 + q.uniform(-10, 10))]
    p = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    return (f'<polygon points="{p}" fill="#2e2c34" {_s(7)} stroke-linejoin="round"/>'
            f'<path d="M{-w/4:.0f} {-h/4:.0f} l{w/3:.0f} {h/6:.0f} l{-w/8:.0f} {h/3:.0f}" stroke="#ff7a1a" stroke-width="4" fill="none" opacity="0.8"/>'
            f'<polyline points="{p}" fill="none" stroke="#5a5862" stroke-width="5" stroke-dasharray="20 14" opacity="0.6"/>')


def signpost(text_lines=("WELCOME,", "PROSPECTIVE", "SOVEREIGN"), w=220):
    t = "".join(f'<text x="0" y="{-18+i*22}" font-family="Cinzel" font-weight="700" font-size="17" fill="#2a1408" text-anchor="middle">{l}</text>' for i, l in enumerate(text_lines))
    return (f'<rect x="-8" y="-10" width="16" height="70" fill="#4a3020" {_s(4)}/>'
            f'<g transform="rotate(-8)"><rect x="{-w/2}" y="-46" width="{w}" height="{len(text_lines)*22+16}" rx="6" fill="#c8a878" {_s(5)}/>{t}</g>')


def iron_golem_slumped(s=1.0):
    return (f'<g transform="scale({s})"><ellipse cx="20" cy="30" rx="170" ry="90" fill="#000" opacity="0.25"/>'
            f'<rect x="-110" y="-120" width="220" height="200" rx="40" fill="url(#lg-iron)" {_s(8)}/>'
            f'<circle cx="0" cy="-20" r="46" fill="#140c0c" {_s(6)}/><circle cx="0" cy="-20" r="26" fill="#3a1414" {_s(4)}/>'
            f'<path d="M-50 -66 L50 -66 L60 -40 M-50 -66 L-60 -40" stroke="#8a8690" stroke-width="10" fill="none"/>'
            f'<rect x="-70" y="-190" width="140" height="80" rx="30" fill="#4a4650" {_s(7)}/><rect x="-44" y="-162" width="88" height="16" fill="#1a1012"/>'
            f'<rect x="-210" y="-80" width="100" height="70" rx="24" fill="#4a4650" {_s(7)} transform="rotate(-20 -160 -45)"/>'
            f'<rect x="110" y="-60" width="110" height="70" rx="24" fill="#4a4650" {_s(7)} transform="rotate(25 165 -25)"/>'
            f'<rect x="-90" y="70" width="70" height="120" rx="20" fill="#3e3a44" {_s(7)}/><rect x="20" y="70" width="70" height="120" rx="20" fill="#3e3a44" {_s(7)}/>'
            f'<text x="0" y="40" font-family="Cinzel" font-weight="700" font-size="20" fill="#d8aa52" text-anchor="middle">JANELLA</text></g>')


def anvil():
    return (f'<path d="M-70 -24 L60 -24 Q90 -22 96 -6 L40 0 L40 26 L-40 26 L-40 0 L-70 -6 Z" fill="#3a3640" {_s(6)}/>'
            f'<path d="M-64 -18 L56 -18" stroke="#77737e" stroke-width="5"/>')


def forge(r=110):
    return (f'<circle r="{r*1.3:.0f}" fill="#ff7a1a" opacity="0.25" filter="url(#glow)"/>'
            f'<rect x="{-r}" y="{-r*0.75:.0f}" width="{2*r}" height="{1.5*r:.0f}" rx="16" fill="#4a3a36" {_s(7)}/>'
            f'<rect x="{-r*0.75:.0f}" y="{-r*0.5:.0f}" width="{1.5*r:.0f}" height="{r:.0f}" rx="10" fill="#2a120c" {_s(5)}/>'
            + "".join(f'<circle cx="{-r*0.5 + i*r*0.25:.0f}" cy="{(i%2)*r*0.2-r*0.1:.0f}" r="{r*0.14:.0f}" fill="{["#ffd25a","#ff7a1a","#ffb43a"][i%3]}"/>' for i in range(5)))


def workbench(w=220, h=90, seed=0):
    q = random.Random(seed)
    s = rect(w, h, "#6e4527", 6, 5)
    for i in range(4):
        x = -w / 2 + 30 + i * (w - 60) / 3
        kind = q.choice(["gear", "tool", "core", "paper"])
        if kind == "gear":
            s += f'<circle cx="{x:.0f}" cy="{q.uniform(-15,15):.0f}" r="16" fill="#c09040" {_s(3)}/><circle cx="{x:.0f}" cy="0" r="5" fill="{INK}"/>'
        elif kind == "tool":
            s += f'<rect x="{x-20:.0f}" y="-5" width="40" height="10" fill="#8a8690" {_s(2)} transform="rotate({q.uniform(-40,40):.0f} {x:.0f} 0)"/>'
        elif kind == "core":
            s += f'<circle cx="{x:.0f}" cy="0" r="14" fill="#7ad0ff" {_s(3)}/><circle cx="{x:.0f}" cy="0" r="22" fill="#7ad0ff" opacity="0.25"/>'
        else:
            s += f'<rect x="{x-18:.0f}" y="-16" width="36" height="30" fill="#efe6d0" {_s(2)} transform="rotate({q.uniform(-15,15):.0f} {x:.0f} 0)"/>'
    return s


def golem_parts(seed=0):
    q = random.Random(seed)
    s = ""
    for _ in range(5):
        x, y = q.uniform(-60, 60), q.uniform(-50, 50)
        k = q.choice(["arm", "plate", "gear"])
        if k == "arm":
            s += f'<rect x="{x-40:.0f}" y="{y-14:.0f}" width="80" height="28" rx="12" fill="#4a4650" {_s(4)} transform="rotate({q.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
        elif k == "plate":
            s += f'<rect x="{x-26:.0f}" y="{y-20:.0f}" width="52" height="40" rx="6" fill="#5a5660" {_s(4)}/>'
        else:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="18" fill="#c09040" {_s(3)}/><circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{INK}"/>'
    return s


def bar_counter(l=500, horiz=True):
    w, h = (l, 70) if horiz else (70, l)
    s = rect(w, h, "#5a3418", 6, 6)
    s += rect(w - 20, h - 24, "#7a4a24", 4, 2)
    for i in range(int(l // 70)):
        x = -l / 2 + 40 + i * 70
        cx, cy = (x, 0) if horiz else (0, x)
        s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="10" fill="#d8c08a" {_s(2)}/>'
    return s


def keg_rack(n=3):
    return "".join(f'<g transform="translate({-((n-1)*36)+i*72},0)"><circle r="32" fill="#7a4a22" {_s(5)}/><circle r="20" fill="none" stroke="#3a2a1a" stroke-width="4"/><circle r="6" fill="#3a2a1a"/></g>' for i in range(n))


def long_table(l=500, seed=0, settings=True):
    q = random.Random(seed)
    s = rect(l, 100, "#6e4527", 6, 6) + rect(l - 30, 70, "#efe6d0", 4, 2)
    if settings:
        for i in range(int(l // 60)):
            x = -l / 2 + 40 + i * 60
            for y in (-24, 24):
                s += f'<circle cx="{x:.0f}" cy="{y}" r="12" fill="#f8f4ea" {_s(2)}/>'
        for i in range(3):
            s += f'<circle cx="{-l/3 + i*l/3:.0f}" cy="0" r="10" fill="#ffd27a" {_s(2)}/>'
    return s


def bed(w=100, h=180, fill="#5a1a24"):
    return (rect(w, h, "#4a3020", 6, 5) + f'<rect x="{-w/2+8}" y="{-h/2+40}" width="{w-16}" height="{h-50}" rx="6" fill="{fill}" {_s(3)}/>'
            f'<rect x="{-w/2+12}" y="{-h/2+8}" width="{w-24}" height="28" rx="10" fill="#efe6d0" {_s(3)}/>')


def wardrobe(w=140, h=60):
    return rect(w, h, "#4a2e1a", 4, 5) + f'<line x1="0" y1="{-h/2}" x2="0" y2="{h/2}" stroke="{INK}" stroke-width="3"/>'


def debris(n=6, spread=80, seed=0):
    q = random.Random(seed)
    s = ""
    for _ in range(n):
        x, y = q.uniform(-spread, spread), q.uniform(-spread, spread)
        s += f'<rect x="{x-40:.0f}" y="{y-8:.0f}" width="{q.uniform(50,110):.0f}" height="16" fill="#4a3020" {_s(3)} transform="rotate({q.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    return s + pebbles(8, spread, seed, dark=True)


def plinth(label="NAME", color="#c0283a"):
    return (f'<rect x="-46" y="-46" width="92" height="92" rx="8" fill="#5a5660" {_s(6)}/><rect x="-34" y="-34" width="68" height="68" rx="4" fill="#3a3640" {_s(3)}/>'
            f'<circle r="18" fill="{color}" opacity="0.8" {_s(3)}/>'
            f'<text x="0" y="66" font-family="Cinzel" font-weight="700" font-size="18" fill="#f0e2c0" stroke="{INK}" stroke-width="3" paint-order="stroke" text-anchor="middle">{label}</text>')


def mirror(w=90):
    return (f'<ellipse rx="{w/2}" ry="{w*0.18:.0f}" fill="#9fc6e8" {_s(5)}/><ellipse rx="{w/2-8}" ry="{w*0.1:.0f}" fill="#d8ecff" opacity="0.8"/>'
            f'<rect x="{-w/2-6}" y="{w*0.14:.0f}" width="{w+12}" height="12" rx="4" fill="#c09040" {_s(3)}/>')


def gold_pile(r=110, seed=0):
    q = random.Random(seed)
    s = f'<ellipse rx="{r}" ry="{r*0.85:.0f}" fill="#e8b830" {_s(6)}/>'
    for _ in range(60):
        x, y = q.uniform(-r * 0.85, r * 0.85), q.uniform(-r * 0.7, r * 0.7)
        if x * x / (r * r) + y * y / (r * r * 0.7) < 0.8:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{q.uniform(6,11):.0f}" fill="{q.choice(["#ffd84a","#f0c030","#ffe680"])}" stroke="#8a6010" stroke-width="2"/>'
    for _ in range(4):
        s += f'<rect x="{q.uniform(-r*0.6,r*0.6):.0f}" y="{q.uniform(-r*0.5,r*0.5):.0f}" width="16" height="16" fill="{q.choice(["#c0283a","#2a6ad0","#2fa046"])}" {_s(2)} transform="rotate(45)"/>'
    return s


def crystal(color="blue", n=4, seed=0):
    q = random.Random(seed)
    c1, c2 = {"blue": ("#7ad0ff", "#2a6ad0"), "yellow": ("#ffe680", "#d8a020"), "red": ("#ff7a7a", "#a01828")}[color]
    s = f'<circle r="90" fill="{c1}" opacity="0.22" filter="url(#glow)"/>'
    for i in range(n):
        x, y, sz = q.uniform(-40, 40), q.uniform(-40, 40), q.uniform(28, 46)
        rot = q.uniform(0, 180)
        s += (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})"><polygon points="0,{-sz:.0f} {sz*0.55:.0f},{-sz*0.2:.0f} {sz*0.4:.0f},{sz*0.7:.0f} {-sz*0.4:.0f},{sz*0.7:.0f} {-sz*0.55:.0f},{-sz*0.2:.0f}" fill="{c2}" {_s(5)}/>'
              f'<polygon points="0,{-sz:.0f} {sz*0.2:.0f},{-sz*0.1:.0f} 0,{sz*0.6:.0f} {-sz*0.25:.0f},{-sz*0.15:.0f}" fill="{c1}"/></g>')
    return s


def glyph_ring(r=120):
    s = f'<circle r="{r*1.2:.0f}" fill="#9a7aff" opacity="0.15" filter="url(#glow)"/>'
    for rr in (r, r * 0.75):
        s += f'<circle r="{rr:.0f}" fill="none" stroke="{INK}" stroke-width="14"/><circle r="{rr:.0f}" fill="none" stroke="#c8c4d0" stroke-width="8"/>'
    s += f'<circle r="{r*0.45:.0f}" fill="#7a3a1a" {_s(6)}/><circle r="{r*0.3:.0f}" fill="#c0601a" {_s(3)}/>'
    s += f'<path d="M{-r*1.05:.0f} 0 H{r*1.05:.0f} M0 {-r*1.05:.0f} V{r*1.05:.0f}" stroke="#c8c4d0" stroke-width="6"/>'
    q = random.Random(int(r))
    for _ in range(6):
        a = q.uniform(0, 2 * math.pi)
        x, y = math.cos(a) * r, math.sin(a) * r
        s += f'<path d="M{x:.0f} {y:.0f} l{q.uniform(-20,20):.0f} {q.uniform(-20,20):.0f} l{q.uniform(-20,20):.0f} {q.uniform(-20,20):.0f}" stroke="#a88aff" stroke-width="3" fill="none"/>'
    return s


def central_platform(r=330):
    s = f'<circle r="{r*1.12:.0f}" fill="#c0281a" opacity="0.4" filter="url(#glow)"/>'
    s += f'<circle r="{r*1.05:.0f}" fill="#2a1414" stroke="#ff5a1a" stroke-width="16"/>'
    s += f'<circle r="{r}" fill="#3a5a70" {_s(10)}/><circle r="{r*0.93:.0f}" fill="#4a7a96" stroke="#2a4a60" stroke-width="6"/>'
    pts = [(math.cos(-math.pi / 2 + i * 2 * math.pi / 9) * r * 0.85, math.sin(-math.pi / 2 + i * 2 * math.pi / 9) * r * 0.85) for i in range(9)]
    for k in (2, 4):
        order = [pts[(i * k) % 9] for i in range(9)] + [pts[0]]
        s += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in order)}" fill="none" stroke="#7ae0ff" stroke-width="6" stroke-linejoin="round"/>'
    s += f'<circle r="{r*0.38:.0f}" fill="#6aa8c8" stroke="#bff0ff" stroke-width="6"/>'
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        s += f'<rect x="-14" y="-14" width="28" height="28" fill="#5a6a7a" {_s(4)} transform="translate({math.cos(a)*r*1.12:.0f},{math.sin(a)*r*1.12:.0f}) rotate(20)"/>'
    return s


def arch_tracery(w=300, h=700):
    """Gothic arch inlay on the arena floor (decal)."""
    return (f'<path d="M{-w/2} {h/2} V{-h/6:.0f} Q{-w/2} {-h/2} 0 {-h/2} Q{w/2} {-h/2} {w/2} {-h/6:.0f} V{h/2}" fill="none" stroke="#a89e96" stroke-width="22" opacity="0.45"/>'
            f'<path d="M{-w/2} {h/2} V{-h/6:.0f} Q{-w/2} {-h/2} 0 {-h/2} Q{w/2} {-h/2} {w/2} {-h/6:.0f} V{h/2}" fill="none" stroke="#6a625a" stroke-width="4" stroke-dasharray="40 10" opacity="0.5"/>'
            f'<path d="M{-w/3:.0f} {h/6:.0f} Q0 {-h/6:.0f} {w/3:.0f} {h/6:.0f} Q0 {h/3:.0f} {-w/3:.0f} {h/6:.0f} Z" fill="none" stroke="#a89e96" stroke-width="16" opacity="0.4"/>')


def gate(w=600):
    return (rect(w, 120, "#3a3a40", 10, 7) + f'<g transform="translate(0,-23)">{rect(w - 60, 34, "#c09040", 4, 4)}</g>'
            + f'<g transform="translate(0,23)">{rect(w - 60, 34, "#c09040", 4, 4)}</g>'
            + "".join(f'<line x1="{-w/2+50+i*(w-100)/10:.0f}" y1="-50" x2="{-w/2+50+i*(w-100)/10:.0f}" y2="50" stroke="#1a1418" stroke-width="6"/>' for i in range(11)))


def rib_arc(l=900, sgn=1):
    return (f'<path d="M0 0 C{sgn*120} {-l*0.15:.0f} {sgn*180} {-l*0.6:.0f} {sgn*60} {-l:.0f}" stroke="{INK}" stroke-width="86" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 0 C{sgn*120} {-l*0.15:.0f} {sgn*180} {-l*0.6:.0f} {sgn*60} {-l:.0f}" stroke="#e0d2b2" stroke-width="66" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 0 C{sgn*120} {-l*0.15:.0f} {sgn*180} {-l*0.6:.0f} {sgn*60} {-l:.0f}" stroke="#b8a888" stroke-width="18" fill="none" stroke-dasharray="40 30" stroke-linecap="round"/>')


def vertebra(r=90):
    return (f'<rect x="{-r}" y="{-r*0.6:.0f}" width="{2*r}" height="{1.2*r:.0f}" rx="{r*0.5:.0f}" fill="#d8cbab" {_s(7)}/>'
            f'<circle r="{r*0.3:.0f}" fill="#8a7a5a" {_s(4)}/>')


def judge_bench(w=600, h=160):
    return (rect(w + 60, h + 60, "#2a1a14", 8, 6) + rect(w, h, "#5a2e18", 6, 6)
            + f'<rect x="{-w/2+20}" y="{-h/2+16}" width="{w-40}" height="30" fill="#c09040" {_s(3)}/>'
            + f'<circle cx="0" cy="{h/2+10}" r="30" fill="#c09040" {_s(4)}/><path d="M-12 {h/2+10} h24 M0 {h/2-2} v24" stroke="{INK}" stroke-width="4"/>')


def witness_stand():
    return (f'<rect x="-60" y="-60" width="120" height="120" rx="10" fill="#5a2e18" {_s(6)}/>'
            f'<rect x="-44" y="-44" width="88" height="88" rx="6" fill="#3a1e10" {_s(3)}/><circle r="16" fill="#c09040" {_s(3)}/>')


def pew(l=400):
    return rect(l, 50, "#4a2818", 6, 5) + f'<rect x="{-l/2}" y="14" width="{l}" height="12" fill="#2a1408" {_s(2)}/>'


def iron_rose(r=50, seed=0):
    q = random.Random(seed)
    s = f'<line x1="0" y1="0" x2="{q.uniform(-30,30):.0f}" y2="-160" stroke="#2a2830" stroke-width="5" stroke-dasharray="10 6"/>'
    for i in range(7):
        a = i * 2 * math.pi / 7
        s += f'<ellipse cx="{math.cos(a)*r*0.45:.0f}" cy="{math.sin(a)*r*0.45:.0f}" rx="{r*0.5:.0f}" ry="{r*0.3:.0f}" fill="#4a4652" {_s(4)} transform="rotate({math.degrees(a):.0f} {math.cos(a)*r*0.45:.0f} {math.sin(a)*r*0.45:.0f})"/>'
    s += f'<circle r="{r*0.35:.0f}" fill="#8e1424" {_s(4)}/><circle r="{r*0.15:.0f}" fill="#ff5a5a"/>'
    return s


def sleeping_dais(w=320, h=240):
    return (rect(w + 80, h + 80, "#2a1018", 20, 7) + rect(w, h, "#5a1424", 14, 6)
            + f'<rect x="{-w/2+20}" y="{-h/2+20}" width="{w-40}" height="50" rx="20" fill="#d8c8d0" {_s(4)}/>'
            + "".join(f'<path d="M{-w/2-30+i*(w+60)/6:.0f} {-h/2-30} q20 40 0 {h+60}" stroke="#7a2a3a" stroke-width="8" fill="none" opacity="0.7"/>' for i in range(7)))


def heartstone(r=60):
    return (f'<circle r="{r*2.4:.0f}" fill="#ff3a5a" opacity="0.2" filter="url(#glow)"/>'
            f'<rect x="{-r*1.1:.0f}" y="{-r*1.1:.0f}" width="{r*2.2:.0f}" height="{r*2.2:.0f}" rx="10" fill="#3a3640" {_s(6)} transform="rotate(45)"/>'
            f'<path d="M0 {-r:.0f} L{r*0.7:.0f} {-r*0.2:.0f} L0 {r:.0f} L{-r*0.7:.0f} {-r*0.2:.0f} Z" fill="#c0183a" {_s(5)}/>'
            f'<path d="M0 {-r:.0f} L{r*0.25:.0f} {-r*0.2:.0f} L0 {r*0.6:.0f} Z" fill="#ff7a8a"/>')


def prism_screen(l=500, horiz=True):
    cols = ["#ff5a5a", "#ffb43a", "#ffe680", "#7ae07a", "#7ad0ff", "#a08aff"]
    out = []
    for i, c in enumerate(cols):
        off = -25 + i * 10
        if horiz:
            out.append(f'<line x1="{-l/2}" y1="{off}" x2="{l/2}" y2="{off}" stroke="{c}" stroke-width="9" opacity="0.8"/>')
        else:
            out.append(f'<line x1="{off}" y1="{-l/2}" x2="{off}" y2="{l/2}" stroke="{c}" stroke-width="9" opacity="0.8"/>')
    return "".join(out)


def soul_mosaic(r=120):
    s = f'<circle r="{r}" fill="#1a1426" {_s(7)}/>'
    for i in range(12):
        a = i * 2 * math.pi / 12
        s += f'<path d="M0 0 L{math.cos(a)*r:.0f} {math.sin(a)*r:.0f} A{r} {r} 0 0 1 {math.cos(a+0.52)*r:.0f} {math.sin(a+0.52)*r:.0f} Z" fill="{["#3a2a5a","#5a3a7a","#2a3a6a"][i%3]}" stroke="#8a7aff" stroke-width="3"/>'
    s += f'<circle r="{r*0.3:.0f}" fill="#d8d0ff" opacity="0.8" {_s(3)}/>'
    return s


def pylon(color="#ff4a1a"):
    return (f'<circle r="70" fill="{color}" opacity="0.2" filter="url(#glow)"/>'
            f'<polygon points="0,-46 40,-23 40,23 0,46 -40,23 -40,-23" fill="#3a3640" {_s(6)}/>'
            f'<circle r="18" fill="{color}" {_s(3)}/>')


def banner_stand(color="#8e1424", emblem="#d8aa52", shape="crown"):
    em = {"crown": '<path d="M-22 10 L-22 -10 L-11 0 L0 -16 L11 0 L22 -10 L22 10 Z"',
          "gear": '<circle r="16"', "thorn": '<path d="M0 -20 L6 -4 L20 0 L6 4 L0 20 L-6 4 L-20 0 L-6 -4 Z"',
          "wing": '<path d="M-24 6 Q-10 -20 0 -4 Q10 -20 24 6 Z"'}[shape]
    return (f'<rect x="-50" y="-14" width="100" height="28" fill="#2a2228" {_s(4)}/>'
            f'<path d="M-40 -10 h80 v70 l-40 -16 l-40 16 Z" fill="{color}" {_s(5)}/>'
            f'<g transform="translate(0,18)">{em} fill="{emblem}" {_s(3)}/></g>')


def siege_engine(w=240, h=160):
    return (rect(w, h, "#5a3a20", 8, 6) + f'<line x1="{-w/2}" y1="0" x2="{w/2+60}" y2="-30" stroke="{INK}" stroke-width="22"/>'
            f'<line x1="{-w/2}" y1="0" x2="{w/2+60}" y2="-30" stroke="#8a6a3a" stroke-width="12"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="#3a2a1a" {_s(5)}/>' for x in (-w / 2, w / 2) for y in (-h / 2, h / 2)))


def ledger_stall(w=240, h=120, seed=0):
    from props import stall
    return stall(w, h, "#5e0b18", "#d8aa52", goods=False, seed=seed) + f'<rect x="-60" y="10" width="120" height="40" fill="#efe6d0" {_s(3)}/>'


def lava_bubble(r=30):
    return (f'<circle r="{r}" fill="#ffd25a" stroke="#c0400a" stroke-width="5"/><circle cx="{-r*0.3:.0f}" cy="{-r*0.3:.0f}" r="{r*0.3:.0f}" fill="#fff2b0"/>')


def stairs(w=200, h=400, n=10, vertical=True):
    out = [rect(w, h, "#3a3640", 4, 6)]
    for i in range(n):
        if vertical:
            y = -h / 2 + i * h / n
            out.append(f'<rect x="{-w/2+6}" y="{y+3:.0f}" width="{w-12}" height="{h/n-6:.0f}" fill="{["#5a5660","#4e4a54"][i%2]}" {_s(3)}/>')
        else:
            x = -w / 2 + i * w / n
            out.append(f'<rect x="{x+3:.0f}" y="{-h/2+6}" width="{w/n-6:.0f}" height="{h-12}" fill="{["#5a5660","#4e4a54"][i%2]}" {_s(3)}/>')
    return "".join(out)


def double_door_gate(w=240):
    return (f'<rect x="{-w/2}" y="-40" width="{w}" height="80" rx="8" fill="#3a3640" {_s(6)}/>'
            f'<rect x="{-w/2+16}" y="-28" width="{w/2-20}" height="56" fill="#c09040" {_s(4)}/><rect x="4" y="-28" width="{w/2-20}" height="56" fill="#c09040" {_s(4)}/>'
            f'<circle cx="-14" cy="0" r="7" fill="{INK}"/><circle cx="14" cy="0" r="7" fill="{INK}"/>')


def brazier(r=34):
    return (f'<circle r="{r*2.6:.0f}" fill="#ff8a1a" opacity="0.22" filter="url(#glow)"/>'
            + "".join(f'<rect x="-5" y="{r-2}" width="10" height="{r*0.6:.0f}" fill="#2a2830" {_s(3)} transform="rotate({a})"/>' for a in (0, 120, 240))
            + f'<circle r="{r}" fill="#3a3640" {_s(6)}/><circle r="{r*0.75:.0f}" fill="#2a120c" {_s(2)}/>'
            f'<circle r="{r*0.55:.0f}" fill="#ff7a1a"/><circle cx="-4" cy="-4" r="{r*0.32:.0f}" fill="#ffd25a"/><circle cx="-6" cy="-6" r="{r*0.14:.0f}" fill="#fff2b0"/>')


def altar(w=180, h=360, color="#5a2a8a"):
    return (rect(w + 40, h + 40, "#3a3640", 8, 6) + rect(w, h, color, 6, 5)
            + f'<rect x="{-w/2+14}" y="{-h/2+14}" width="{w-28}" height="{h-28}" fill="none" stroke="#c09040" stroke-width="5"/>'
            + f'<path d="M0 {-h/3:.0f} L{w/4:.0f} 0 L0 {h/3:.0f} L{-w/4:.0f} 0 Z" fill="#8a4ac0" stroke="#c09040" stroke-width="4"/>'
            + "".join(f'<circle cx="{sx*(w/2+6):.0f}" cy="{sy*(h/2+6):.0f}" r="12" fill="#ffd27a" {_s(3)}/>' for sx in (-1, 1) for sy in (-1, 1)))


def astrolabe(r=110):
    s = f'<circle r="{r}" fill="#2a1a3a" {_s(7)}/><circle r="{r*0.92:.0f}" fill="none" stroke="#c09040" stroke-width="8"/>'
    s += f'<circle r="{r*0.7:.0f}" fill="none" stroke="#d8aa52" stroke-width="5"/><ellipse rx="{r*0.85:.0f}" ry="{r*0.35:.0f}" fill="none" stroke="#7ad0ff" stroke-width="5" transform="rotate(30)"/>'
    s += f'<ellipse rx="{r*0.85:.0f}" ry="{r*0.35:.0f}" fill="none" stroke="#e05a8a" stroke-width="5" transform="rotate(-40)"/>'
    for i in range(12):
        a = i * math.pi / 6
        s += f'<line x1="{math.cos(a)*r*0.78:.0f}" y1="{math.sin(a)*r*0.78:.0f}" x2="{math.cos(a)*r*0.9:.0f}" y2="{math.sin(a)*r*0.9:.0f}" stroke="#d8aa52" stroke-width="4"/>'
    return s + f'<circle r="{r*0.14:.0f}" fill="#ffd25a" {_s(3)}/>'


def hanging_chains(l=320, n=4, seed=0):
    q = random.Random(seed)
    s = f'<rect x="-10" y="{-l/2}" width="20" height="{l}" fill="#2a2830" {_s(4)}/>'
    for i in range(n):
        y = -l / 2 + (i + 0.5) * l / n
        s += "".join(f'<ellipse cx="{12+k*14}" cy="{y:.0f}" rx="8" ry="5" fill="none" stroke="#6a6670" stroke-width="4"/>' for k in range(4))
        if q.random() < 0.6:
            s += f'<g transform="translate(78,{y:.0f}) scale(0.7)">{skull()}</g>'
    return s


def drowned_bed(w=260, h=300):
    return (f'<rect x="{-w/2-20}" y="{-h/2-20}" width="{w+40}" height="{h+40}" fill="#4a2010" {_s(6)}/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#3a2a6a" {_s(4)}/>'
            f'<path d="M{-w/2} {-h/4:.0f} q{w/3:.0f} -30 {w/2:.0f} 10 t{w/2:.0f} -20 V{h/2} H{-w/2} Z" fill="#5a3a9a" opacity="0.7"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#c8b8e8" opacity="0.6"/>' for x, y in ((-60, -40), (40, 20), (-20, 80), (70, -90)))
            + "".join(f'<circle cx="{sx*(w/2+10):.0f}" cy="{sy*(h/2+10):.0f}" r="18" fill="#6a3a1a" {_s(4)}/>' for sx in (-1, 1) for sy in (-1, 1))
            + f'<rect x="{-w/2-30}" y="{-h/2+20}" width="{w*0.6:.0f}" height="22" fill="#6a3a1a" {_s(4)} transform="rotate(-25)"/>')


def broken_bed(w=240, h=200):
    return (f'<ellipse cx="0" cy="10" rx="{w*0.55:.0f}" ry="{h*0.5:.0f}" fill="#3a3436" opacity="0.6"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="22" fill="#6a3a1a" {_s(4)}/>'
            f'<rect x="{-w/2+10}" y="{-h/2}" width="22" height="{h}" fill="#6a3a1a" {_s(4)} transform="rotate(8)"/>'
            f'<rect x="{w/2-30}" y="{-h/2}" width="22" height="{h*0.8:.0f}" fill="#6a3a1a" {_s(4)} transform="rotate(-6)"/>'
            f'<rect x="{-w/2+20}" y="{h/2-40}" width="{w*0.7:.0f}" height="20" fill="#6a3a1a" {_s(4)} transform="rotate(-12)"/>'
            + debris(5, 70, 3))


def tree(r=180, seed=0, palette="green"):
    q = random.Random(seed)
    pal = {"green": ["#5a7a2a", "#6e8e34", "#4a6a24", "#82a040"], "autumn": ["#c8782a", "#d89a3a", "#a85a20", "#e0b04a", "#8a3a3a"],
           "dead": ["#4a3a30", "#5a4a3a", "#3a2e26"]}[palette]
    s = f'<circle r="{r*1.05:.0f}" fill="#000" opacity="0.3" transform="translate(18,22)"/>'
    for i in range(9):
        a = i * 2 * math.pi / 9 + q.uniform(-0.2, 0.2)
        d = r * q.uniform(0.35, 0.55)
        s += f'<circle cx="{math.cos(a)*d:.0f}" cy="{math.sin(a)*d:.0f}" r="{r*q.uniform(0.42,0.55):.0f}" fill="{q.choice(pal)}" {_s(5)}/>'
    s += f'<circle r="{r*0.5:.0f}" fill="{q.choice(pal)}" {_s(4)}/>'
    for _ in range(14):
        a, d = q.uniform(0, 6.28), q.uniform(0, r * 0.8)
        s += f'<path d="M{math.cos(a)*d:.0f} {math.sin(a)*d:.0f} q8 -10 18 -2" stroke="#e8f0a0" stroke-width="3" fill="none" opacity="0.5"/>'
    return s


def headstone(w=50, kind=0):
    if kind == 0:
        return f'<path d="M{-w/2} {w*0.3:.0f} V{-w*0.1:.0f} Q0 {-w*0.5:.0f} {w/2} {-w*0.1:.0f} V{w*0.3:.0f} Z" fill="#8a8a90" {_s(4)}/><path d="M-8 -4 h16 M0 -12 v18" stroke="#4a4a50" stroke-width="3"/>'
    return f'<rect x="{-w/2}" y="{-w*0.22:.0f}" width="{w}" height="{w*0.44:.0f}" rx="4" fill="#7a7a82" {_s(4)}/><rect x="{-w/2+5}" y="{-w*0.22+4:.0f}" width="{w-10}" height="6" fill="#a8a8b0"/>'


def tomb_slab(w=130, h=90):
    return (rect(w, h, "#7a7a82", 6, 5) + f'<rect x="{-w/2+10}" y="{-h/2+10}" width="{w-20}" height="{h-20}" rx="4" fill="#9a9aa2" stroke="#4a4a50" stroke-width="3"/>'
            + f'<path d="M0 {-h/2+18} V{h/2-18} M-16 {-h/2+32} H16" stroke="#4a4a50" stroke-width="5"/>')


def embers(n=3, seed=0):
    q = random.Random(seed)
    return "".join(f'<circle cx="{q.uniform(-14,14):.0f}" cy="{q.uniform(-14,14):.0f}" r="{q.uniform(5,8):.0f}" fill="#ff5a2a" stroke="#8a1a0a" stroke-width="2"/>' for _ in range(n))


def claw_spike(l=300, w=110, seed=0, curl=0.4):
    q = random.Random(seed)
    c = curl * l
    d = f"M{-w/2:.0f} 0 Q{-w*0.6:.0f} {-l*0.6:.0f} {c:.0f} {-l:.0f} Q{w*0.4:.0f} {-l*0.5:.0f} {w/2:.0f} 0 A{w/2:.0f} {w*0.45:.0f} 0 0 1 {-w/2:.0f} 0 Z"
    s = f'<path d="{d}" fill="#7a1a1a" {_s(7)} stroke-linejoin="round"/>'
    s += f'<path d="M{-w*0.2:.0f} -10 Q{-w*0.2:.0f} {-l*0.55:.0f} {c*0.8:.0f} {-l*0.92:.0f}" stroke="#c0402a" stroke-width="8" fill="none" opacity="0.7"/>'
    for _ in range(6):
        y = -q.uniform(0.1, 0.8) * l
        s += f'<path d="M{q.uniform(-w*0.3,w*0.1):.0f} {y:.0f} l{q.uniform(10,30):.0f} {q.uniform(-25,-5):.0f}" stroke="#2a0808" stroke-width="3"/>'
    return s


def crystal_mass(w=260, seed=0, cols=("#c88ab8", "#5ab8a8", "#a86ab0", "#7ad0c0")):
    q = random.Random(seed)
    s = ""
    for _ in range(int(w / 18)):
        x, y = q.uniform(-w / 2, w / 2), q.uniform(-w / 5, w / 5)
        sz = q.uniform(22, 44)
        s += (f'<polygon points="{x:.0f},{y-sz:.0f} {x+sz*0.7:.0f},{y-sz*0.2:.0f} {x+sz*0.4:.0f},{y+sz*0.7:.0f} {x-sz*0.5:.0f},{y+sz*0.6:.0f} {x-sz*0.7:.0f},{y-sz*0.1:.0f}" '
              f'fill="{q.choice(cols)}" {_s(3)}/><path d="M{x:.0f} {y-sz:.0f} L{x:.0f} {y+sz*0.6:.0f}" stroke="#fff" stroke-width="3" opacity="0.5"/>')
    return s


def wrecked_ship(l=700, w=260):
    return (f'<path d="M{-l/2} 0 Q{-l/2} {-w/2} {-l/4:.0f} {-w/2} H{l/3:.0f} Q{l/2} {-w/4:.0f} {l/2} 0 Q{l/2} {w/4:.0f} {l/3:.0f} {w/2} H{-l/4:.0f} Q{-l/2} {w/2} {-l/2} 0 Z" fill="#7a5030" {_s(8)}/>'
            + "".join(f'<line x1="{-l/2+40}" y1="{-w/2+30+i*40}" x2="{l/2-40}" y2="{-w/2+30+i*40}" stroke="#5a3a20" stroke-width="10"/>' for i in range(5))
            + f'<path d="M{-l/8:.0f} {-w/2} l40 {w*0.6:.0f} l-70 {w*0.3:.0f}" stroke="#1a0a06" stroke-width="22" fill="none"/>'
            + f'<line x1="0" y1="0" x2="{l*0.55:.0f}" y2="{w*0.9:.0f}" stroke="{INK}" stroke-width="22"/><line x1="0" y1="0" x2="{l*0.55:.0f}" y2="{w*0.9:.0f}" stroke="#8a6a3a" stroke-width="12"/>'
            + f'<circle r="{l*0.35:.0f}" fill="#ffb43a" opacity="0.35" filter="url(#glow)"/>')


def dragon_corpse(s=1.0):
    return (f'<g transform="scale({s})"><path d="M-40 0 L-240 -180 L-160 -20 L-260 40 L-60 40 Z" fill="#5a1a22" {_s(7)}/>'
            f'<path d="M40 0 L240 -160 L170 -10 L250 60 L60 40 Z" fill="#5a1a22" {_s(7)}/>'
            f'<ellipse rx="80" ry="140" fill="#6a2028" {_s(8)}/><path d="M0 -130 q-20 -80 10 -150 l20 10 q-20 60 0 140 Z" fill="#6a2028" {_s(6)}/>'
            f'<path d="M0 130 q40 80 20 170" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M0 130 q40 80 20 170" stroke="#6a2028" stroke-width="28" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M-50 {y} q50 18 100 0" stroke="#3a0e14" stroke-width="6" fill="none"/>' for y in range(-90, 110, 30)) + '</g>')
