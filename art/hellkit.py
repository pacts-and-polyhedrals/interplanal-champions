"""Shared helpers for the Avernus maps: lava rivers, scatter, ruins."""
import math, random
from mapkit import INK
import props2 as p2


def _offset(pts, d, q, jag=0.0):
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        dd = d + (q.uniform(-jag, jag) if jag else 0)
        out.append((x + nx * dd, y + ny * dd))
    return out


def densify(pts, step=0.6):
    out = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for i in range(n):
            t = i / n
            out.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
    out.append(pts[-1])
    # light smoothing
    sm = [out[0]]
    for i in range(1, len(out) - 1):
        sm.append(((out[i - 1][0] + 2 * out[i][0] + out[i + 1][0]) / 4, (out[i - 1][1] + 2 * out[i][1] + out[i + 1][1]) / 4))
    sm.append(out[-1])
    return sm


def river(m, center, width, seed=1, crust=0.9, lights=True, glow=True, bank=None, bank_w=0):
    """Lava river along a centre polyline (grid units). Returns the left and right bank lines."""
    q = random.Random(seed)
    c = densify(center)
    half = width / 2
    if bank:
        Lb = _offset(c, half + crust + bank_w, q, 0.4)
        Rb = _offset(c, -(half + crust + bank_w), q, 0.4)
        m.floor_poly(Lb + Rb[::-1], bank, layer="floor")
    # crust band
    L = _offset(c, half + crust, q, 0.25)
    R = _offset(c, -(half + crust), q, 0.25)
    m.floor_poly(L + R[::-1], "basalt", layer="floor")
    if glow:
        Lg = _offset(c, half * 1.1, q)
        Rg = _offset(c, -half * 1.1, q)
        d = " ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in Lg + Rg[::-1])
        m.add("floor", f'<polygon points="{d}" fill="#ff5a0a" opacity="0.55" filter="url(#glow)"/>')
    Li = _offset(c, half, q, 0.18)
    Ri = _offset(c, -half, q, 0.18)
    m.floor_poly(Li + Ri[::-1], "lava", layer="floor")
    # hot core streak
    core = _offset(c, q.uniform(-half * 0.2, half * 0.2), q, 0.1)
    d = "M" + " L".join(f"{x*100:.0f} {y*100:.0f}" for x, y in core)
    m.add("floor", f'<path d="{d}" fill="none" stroke="#ffe27a" stroke-width="{width*28:.0f}" opacity="0.35" stroke-linecap="round" filter="url(#blur4)"/>')
    # break up the texture repeat with soft blotches
    for _ in range(int(len(c) * 1.6)):
        x, y = c[q.randrange(len(c))]
        ox = q.uniform(-half * 0.8, half * 0.8)
        col = q.choice(["#ffe27a", "#ff8a1a", "#c0300a", "#ffd04a"])
        m.add("floor", f'<ellipse cx="{(x+ox)*100:.0f}" cy="{(y+q.uniform(-0.5,0.5))*100:.0f}" rx="{q.uniform(60,180):.0f}" ry="{q.uniform(40,110):.0f}" '
                       f'fill="{col}" opacity="{q.uniform(0.15,0.35):.2f}" filter="url(#blur4)" transform="rotate({q.uniform(0,180):.0f} {(x+ox)*100:.0f} {y*100:.0f})"/>')
    # bubbles
    for _ in range(int(len(c) * 0.5)):
        x, y = c[q.randrange(len(c))]
        m.g("decal", x + q.uniform(-half * 0.7, half * 0.7), y + q.uniform(-0.3, 0.3), p2.lava_bubble(q.uniform(10, 22)), shadow=False)
    if lights:
        for i in range(0, len(c), 8):
            x, y = c[i]
            m.light(x, y, width * 1.5 + 6, width * 0.8 + 2, color="#ff6a1a", alpha=0.45, anim="fire", speed=2, intensity=2, walls=False)
    return Li, Ri


def scatter(m, box, n, kinds, seed=0, avoid=(), lines=(), rects=()):
    """Scatter small props in box=(x0,y0,x1,y1) avoiding circles (x,y,r)."""
    q = random.Random(seed)
    placed = 0
    tries = 0
    while placed < n and tries < n * 30:
        tries += 1
        x, y = q.uniform(box[0], box[2]), q.uniform(box[1], box[3])
        if any((x - ax) ** 2 + (y - ay) ** 2 < ar * ar for ax, ay, ar in avoid):
            continue
        if any(r0[0] <= x <= r1[0] and r0[1] <= y <= r1[1] for r0, r1 in rects):
            continue
        if any(_dist_line(x, y, pl) < hw for pl, hw in lines):
            continue
        k = q.choice(kinds)
        s = q.randint(0, 9999)
        if k == "rock":
            m.g("props", x, y, p2.rock(q.uniform(65, 125), s))
        elif k == "bigrock":
            m.g("props", x, y, p2.rock(q.uniform(110, 170), s))
        elif k == "darkrock":
            m.g("props", x, y, p2.darkrock(q.uniform(35, 80), s))
        elif k == "pebbles":
            m.g("lowprop", x, y, p2.pebbles(q.randint(5, 12), 50, s, dark=q.random() < 0.5), shadow=False)
        elif k == "bones":
            m.g("lowprop", x, y, p2.bones(q.randint(3, 7), 40, s, skulls=q.randint(0, 1)), shadow=False)
        elif k == "skeleton":
            m.g("lowprop", x, y, p2.skeleton(s), shadow=False)
        elif k == "debris":
            m.g("lowprop", x, y, p2.debris(q.randint(3, 6), 50, s), shadow=False)
        placed += 1


def ruin(m, pts, seed=0, wall=True):
    """Broken ruin wall along grid polyline: drawn as chunky blocks with Foundry walls."""
    m.g("walls", 0, 0, p2.ruin_blocks([(x * 100, y * 100) for x, y in pts], seed=seed), shadow=True)
    if wall:
        m.wall(pts, "ruin", draw=False)


def ground_mottle(m, n=120, seed=0, cols=("#2a0c08", "#7a3a24", "#4a1a10")):
    q = random.Random(seed)
    for _ in range(n):
        x, y = q.uniform(0, m.w), q.uniform(0, m.h)
        m.add("floor", f'<ellipse cx="{x*100:.0f}" cy="{y*100:.0f}" rx="{q.uniform(80,320):.0f}" ry="{q.uniform(60,220):.0f}" fill="{q.choice(cols)}" '
                       f'opacity="{q.uniform(0.08,0.2):.2f}" filter="url(#blur4)" transform="rotate({q.uniform(0,180):.0f} {x*100:.0f} {y*100:.0f})"/>')


def stain(m, x, y, r, color="#3a0e0a", op=0.35):
    m.add("decal", f'<ellipse cx="{x*100:.0f}" cy="{y*100:.0f}" rx="{r*100:.0f}" ry="{r*80:.0f}" fill="{color}" opacity="{op}" filter="url(#blur4)"/>')


def _dist_line(x, y, pts):
    best = 1e9
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy or 1
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / L2))
        best = min(best, math.hypot(x - x1 - t * dx, y - y1 - t * dy))
    return best


def near_line(x, y, pts, hw):
    return _dist_line(x, y, pts) < hw
