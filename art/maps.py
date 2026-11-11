"""The battlemaps of Interplanal Champions: six regional maps after the 2020 originals, plus location maps."""
import math, random, sys, json, os
from mapkit import Map, INK
import props as pr
import props2 as p2
from hellkit import river, scatter, ruin, stain, densify, ground_mottle, near_line

MAPS = {}


def register(fn):
    MAPS[fn.__name__.replace("_", "-")] = fn
    return fn


def hell_env(m, dark=0.15):
    m.env = {"darkness": dark, "globalLight": True}
    m.sounds.append({"x": m.W / 2, "y": m.H / 2, "radius": max(m.w, m.h) * 5, "path": "lava", "volume": 0.4})


def marker(m, x, y, label, page="map-encounters"):
    m.note(x, y, page, label)


def tiled_floor(m, x, y, w, h, tex="ruintile"):
    m.floor_rect(x, y, w, h, tex, layer="floor", stroke=False)


# ======================================================================= MAP 1
@register
def welcome():
    """Map 1, 'Welcome to Hell': the arrival plain. After the 2020 original."""
    S = 44 / 37
    m = Map("welcome", "Map 1: Welcome to Hell", 44, 44, seed=11, bg="#3a1a14")
    hell_env(m)
    m.fill_all("redsand")
    ground_mottle(m, 140, 1)
    P = lambda x, y: (x * S, y * S)
    for (x, y, r) in [(6, 8, 5), (30, 7, 5), (5, 32, 4), (34, 30, 3), (14, 30, 3)]:
        stain(m, *P(x, y), r * S, "#2a0c08", 0.3)
    # lava river, top-left to bottom-centre
    RV = [P(13.5, -1), P(15.5, 8), P(18, 16), P(21, 24), P(23.5, 31), P(25.5, 38)]
    river(m, RV, 7.2 * S, seed=3)

    # --- top-left C-shaped ruin (E1)
    tiled_floor(m, *P(3, 4.5), 6.5 * S, 9 * S)
    ruin(m, [P(4.5, 13.8), P(2.3, 13.2), P(2, 8), P(2.3, 3.6), P(4, 2.5), P(8, 2.6)], seed=1)
    ruin(m, [P(9.6, 4.2), P(10, 9), P(9.8, 13.8)], seed=2)
    ruin(m, [P(6.8, 9.6), P(9.6, 9.6)], seed=4)
    for cy in (6.8, 8.4):
        m.g("props", *P(8.9, cy), p2.chest(88), rot=90)
    m.g("lowprop", *P(5.5, 3.4), p2.skeleton(5), shadow=False)
    m.g("decal", *P(5.7, 11), p2.magic_circle(70, "#4a8aff", 5, runes=False), shadow=False)
    m.light(*P(5.7, 11), 6, 2, color="#4a8aff", alpha=0.4, anim="pulse")

    # --- top-right ruin with summoning circle (boss)
    tiled_floor(m, *P(26, 1), 7 * S, 12 * S)
    ruin(m, [P(28, 0.6), P(25.6, 0.6), P(25.6, 8)], seed=5)
    ruin(m, [P(25.6, 9.6), P(25.6, 13.2), P(28.6, 13.2)], seed=6)
    ruin(m, [P(31, 0.6), P(33.2, 0.6), P(33.2, 5)], seed=7)
    ruin(m, [P(33.2, 8.2), P(33.2, 13.4)], seed=8)
    m.g("props", *P(28, 1.9), p2.chest(88))
    m.g("decal", *P(29.6, 3.6), p2.magic_circle(105, "#e0283a", 5), shadow=False)
    m.light(*P(29.6, 3.6), 10, 4, color="#ff2a3a", alpha=0.45, anim="pulse")
    m.g("lowprop", *P(21.5, 6), p2.skeleton(9), shadow=False)

    # --- bottom-left round ruin with arrival disk (spawn)
    m.floor_circle(*P(4.5, 32.2), 3.9 * S, "ruintile")
    cx, cy, rr = 4.5, 32.2, 3.9
    arcs = [(200, 330), (350, 430), (100, 175)]
    for i, (a0, a1) in enumerate(arcs):
        pts = [P(cx + math.cos(math.radians(a)) * rr, cy + math.sin(math.radians(a)) * rr) for a in range(a0, a1 + 1, 18)]
        ruin(m, pts, seed=20 + i)
    m.g("props", *P(4.3, 29.8), p2.chest(88))
    m.g("decal", *P(4.4, 32.2), p2.spawn_disk(78), shadow=False)
    m.light(*P(4.4, 32.2), 8, 3, color="#4aa0ff", alpha=0.4, anim="pulse")
    m.g("lowprop", *P(7, 33.5), p2.skeleton(13), shadow=False)
    m.g("props", *P(2.5, 3.0), p2.rock(55, 2))

    # --- the dragon skeleton across the river
    dx, dy = P(23.5, 22.6)
    m.g("props", dx, dy, p2.dragon_skeleton(1000), rot=-4, scale=1.7)
    tail = [P(30.5, 21.8), P(33, 21.4), P(35.3, 22.2), P(36.5, 25), P(36.8, 30)]
    d = "M" + " L".join(f"{x*100:.0f} {y*100:.0f}" for x, y in densify(tail, 0.5))
    m.add("props", f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
                   f'<path d="{d}" fill="none" stroke="#e2d6ba" stroke-width="17" stroke-linecap="round"/>'
                   f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="13" stroke-dasharray="3 14"/>')
    m.g("props", *P(35.2, 21.7), p2.rock(95, 31))
    m.light(dx / 100 * 1, dy / 100, 4, 1, color="#ffe27a", alpha=0.3)

    # --- rocks, bones and landmarks from the original
    for (x, y, r, s) in [(21.3, 2.2, 50, 1), (23.3, 6.1, 55, 3), (35, 16.4, 50, 4), (11.3, 26.8, 85, 5), (31.5, 29.6, 60, 6),
                         (34.2, 34.2, 75, 7), (11.6, 34.5, 60, 8), (28.4, 19.2, 50, 9), (5.6, 18.5, 30, 10), (10, 19, 28, 11),
                         (6, 22.4, 30, 12), (35.2, 14, 40, 13), (28.6, 33.5, 35, 14)]:
        m.g("props", *P(x, y), p2.rock(r * 1.9, s))
    for (x, y, s) in [(7.3, 23.2, 1), (17, 32.5, 2), (21.6, 6.2, 3), (27.5, 17.5, 4), (33.4, 31.6, 5)]:
        m.g("lowprop", *P(x, y), p2.skeleton(s), shadow=False, scale=1.5)
    scatter(m, (0.5, 0.5, 43.5, 43.5), 70, ["pebbles", "pebbles", "darkrock", "bones", "debris"], seed=5,
            lines=[(RV, 3.6 * S + 1.4)], avoid=[(*P(5.7, 8.5), 6), (*P(29.5, 7), 7), (*P(4.5, 32), 5)])
    m.g("props", *P(10.5, 16.5), p2.signpost(("WELCOME,", "PROSPECTIVE", "SOVEREIGN")), rot=-6)

    # DM notes (encounter markers are notes, not printed on the art)
    marker(m, *P(4.4, 32.2), "Arrival point (party spawn)")
    marker(m, *P(5.7, 11), "E1: Ruined shrine")
    marker(m, *P(15.3, 26.7), "E2: The scorched rock")
    marker(m, *P(22.5, 22.5), "E3: The wyrm bridge")
    marker(m, *P(34.5, 32.2), "E4: Tail rock ambush")
    marker(m, *P(29.6, 3.6), "Boss: summoning circle")
    marker(m, *P(10.5, 16.5), "The welcome sign (Charter clue)")
    return m


# ======================================================================= MAP 2
def slab(m, x1, y1, x2, y2, seed=0, wall=True):
    ruin(m, [(x1, y1), (x2, y2)], seed=seed, wall=wall)


@register
def findings():
    """Map 2, 'Unexpected Findings': the lava gorge, the stone face and the shrine. After the 2020 original."""
    m = Map("findings", "Map 2: Unexpected Findings", 64, 46, seed=12, bg="#4a3424")
    hell_env(m)
    m.fill_all("ashsand")
    ground_mottle(m, 160, 2, cols=("#4a3424", "#a8885c", "#3a2a3a"))
    for (x, y, r) in [(39, 3, 3.5), (61, 11, 3), (8, 31, 3), (15, 43, 3), (25, 41, 2.5), (12, 37, 3)]:
        stain(m, x, y, r, "#3a3a6a", 0.35)
    RV = [(-2, 2.5), (10, 9.5), (20, 15.5), (30, 22), (38, 27), (50, 34), (66, 42)]
    river(m, RV, 11.5, seed=7, crust=3.0, bank="cavefloor", bank_w=2.2)
    # the carved face rising from the lava (E3 / green)
    m.g("props", 34.3, 27.2, p2.face_rock(480), rot=-12)
    m.light(34.3, 27.2, 8, 3, color="#ff8a3a", alpha=0.3)
    # rock outcrop with standing stones (yellow)
    m.g("props", 21.2, 17.4, p2.rock(300, 41, fill="#8a7e7a", light="#b8acaa"))
    for (x, y, r, s) in [(18, 11.6, 95, 42), (21.6, 11.2, 85, 43), (16.3, 13.6, 80, 44), (15.5, 16, 70, 45), (24, 16.5, 70, 46)]:
        m.g("props", x, y, p2.rock(r * 1.8, s, fill="#7a706e", light="#a8a09c"))
    m.g("props", 21, 17.3, p2.chest(88))
    # octagonal shrine (boss)
    cx, cy, R = 50, 10.7, 3.6
    oct_ = [(cx + R * math.cos(math.radians(22.5 + 45 * i)), cy + R * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    m.floor_poly(oct_, "darkcobble")
    for i in range(8):
        if i in (1, 5):
            continue
        m.wall([oct_[i], oct_[(i + 1) % 8]], "dark")
    m.g("decal", cx, cy, p2.magic_circle(120, "#e0283a", 5), shadow=False)
    m.light(cx, cy, 10, 4, color="#ff2a3a", alpha=0.45, anim="pulse")
    m.g("props", cx + 2, cy - 2, p2.chest(80), rot=-30)
    # ruined building, bottom-left (spawn)
    m.floor_rect(3, 34, 9.8, 5.6, "paleflag")
    m.add("decal", f'<rect x="300" y="3400" width="980" height="560" fill="#3a3a6a" opacity="0.35"/>')
    m.wall([(3, 36.5), (3, 34), (8, 34)], "dark")
    m.wall([(9.5, 34), (12.8, 34), (12.8, 36)], "dark")
    m.wall([(12.8, 37.8), (12.8, 39.6), (6, 39.6)], "dark")
    m.wall([(4.3, 39.6), (3, 39.6), (3, 38)], "dark")
    m.g("decal", 4.9, 38.2, p2.spawn_disk(78), shadow=False)
    m.light(4.9, 38.2, 8, 3, color="#4aa0ff", alpha=0.4, anim="pulse")
    m.g("props", 10, 35.2, p2.chest(80))
    m.g("decal", 16.6, 32, p2.magic_circle(60, "#4a8aff", 5, runes=False), shadow=False)
    # fallen ruin slabs (from the original)
    for i, (a, b, c, d) in enumerate([(35.5, 1.5, 38, 4), (39.5, 2.5, 41.5, 3.8), (45.5, 6.5, 47, 7.8), (47.5, 1, 50.5, 0.8),
                                      (54.5, 3.5, 56.5, 2.5), (57, 9.5, 59.5, 8.2), (51, 15.5, 53.5, 17.5), (55.5, 18, 57.5, 19),
                                      (59, 20, 62, 19.3), (61.5, 5, 61.5, 8.5), (42, 6, 43.5, 5.5),
                                      (2, 28.5, 7, 28.6), (2.5, 32.5, 9.5, 32.4), (8.5, 30, 11.5, 30.4), (1, 42.5, 5, 41.8),
                                      (10.5, 41, 12.5, 43.5), (15, 42.5, 18, 44.5), (20, 43, 22.5, 41.5), (24.5, 44, 27, 45.5),
                                      (22, 39, 24, 40.5), (12.5, 38, 15.5, 37.5), (5, 44.5, 9, 45.3)]):
        slab(m, a, b, c, d, seed=100 + i)
    # bones everywhere
    scatter(m, (0.5, 0.5, 63.5, 45.5), 260, ["bones", "bones", "bones", "skeleton", "pebbles", "rock", "darkrock"], seed=9,
            lines=[(RV, 9.5)], avoid=[(cx, cy, 4.5), (8, 37, 4), (34.3, 27.2, 4.5)])
    marker(m, 4.9, 38.2, "Arrival point (party spawn)")
    marker(m, 16.6, 32, "E1: The shattered hall")
    marker(m, 20.4, 14.4, "E2: The standing stones")
    marker(m, 34.3, 27.2, "E3: The Speaking Face")
    marker(m, 47.6, 5.2, "E4: Shrine approach")
    marker(m, cx, cy, "Boss: the octagon shrine")
    return m


# ======================================================================= roofs & houses
def hiproof(m, x, y, w, h, seed=0, tex="hellroof"):
    """Top-down hipped/pyramidal roof (grid units)."""
    X, Y, W, H = x * 100, y * 100, w * 100, h * 100
    m.floor_rect(x, y, w, h, tex, layer="lowprop")
    r = min(W, H) / 2
    TL, TR, BR, BL = (X, Y), (X + W, Y), (X + W, Y + H), (X, Y + H)
    if W >= H:
        a, b = (X + r, Y + H / 2), (X + W - r, Y + H / 2)
        faces = [([TL, TR, b, a], 0.0), ([TR, BR, b], 0.18), ([BR, BL, a, b], 0.38), ([BL, TL, a], 0.25)]
        hips = [(TL, a), (TR, b), (BR, b), (BL, a), (a, b)]
    else:
        a, b = (X + W / 2, Y + r), (X + W / 2, Y + H - r)
        faces = [([TL, TR, a], 0.0), ([TR, BR, b, a], 0.18), ([BR, BL, b], 0.38), ([BL, TL, a, b], 0.25)]
        hips = [(TL, a), (TR, a), (BR, b), (BL, b), (a, b)]
    for pts, sh in faces:
        p = " ".join(f"{px:.0f},{py:.0f}" for px, py in pts)
        m.add("lowprop", f'<polygon points="{p}" fill="#000" opacity="{sh}" stroke="{INK}" stroke-width="4"/>')
    for u, v in hips:
        m.add("lowprop", f'<line x1="{u[0]:.0f}" y1="{u[1]:.0f}" x2="{v[0]:.0f}" y2="{v[1]:.0f}" stroke="{INK}" stroke-width="16"/>'
                         f'<line x1="{u[0]:.0f}" y1="{u[1]:.0f}" x2="{v[0]:.0f}" y2="{v[1]:.0f}" stroke="#6a5a60" stroke-width="7"/>')
    m.add("lowprop", f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="10"/>')
    m.wall([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], "dark", closed=True, draw=False)


def gableroof(m, x, y, w, h, tex="hellroof"):
    X, Y, W, H = x * 100, y * 100, w * 100, h * 100
    m.floor_rect(x, y, w, h, tex, layer="lowprop")
    if H >= W:
        m.add("lowprop", f'<rect x="{X+W/2}" y="{Y}" width="{W/2}" height="{H}" fill="#000" opacity="0.3"/>'
                         f'<line x1="{X+W/2}" y1="{Y}" x2="{X+W/2}" y2="{Y+H}" stroke="{INK}" stroke-width="18"/><line x1="{X+W/2}" y1="{Y}" x2="{X+W/2}" y2="{Y+H}" stroke="#6a5a60" stroke-width="7"/>')
    else:
        m.add("lowprop", f'<rect x="{X}" y="{Y+H/2}" width="{W}" height="{H/2}" fill="#000" opacity="0.3"/>'
                         f'<line x1="{X}" y1="{Y+H/2}" x2="{X+W}" y2="{Y+H/2}" stroke="{INK}" stroke-width="18"/><line x1="{X}" y1="{Y+H/2}" x2="{X+W}" y2="{Y+H/2}" stroke="#6a5a60" stroke-width="7"/>')
    m.add("lowprop", f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="10"/>')
    m.wall([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], "dark", closed=True, draw=False)


def coneroof(m, cx, cy, r):
    m.floor_circle(cx, cy, r, "hellroof", layer="lowprop")
    for i in range(12):
        a = i * math.pi / 6
        m.add("lowprop", f'<line x1="{cx*100:.0f}" y1="{cy*100:.0f}" x2="{(cx+math.cos(a)*r)*100:.0f}" y2="{(cy+math.sin(a)*r)*100:.0f}" stroke="{INK}" stroke-width="5"/>')
    m.add("lowprop", f'<circle cx="{cx*100:.0f}" cy="{cy*100:.0f}" r="{r*100:.0f}" fill="url(#rg-dark)" opacity="0.5"/><circle cx="{cx*100:.0f}" cy="{cy*100:.0f}" r="30" fill="#3a3036" stroke="{INK}" stroke-width="6"/>')


def house(m, x, y, w, h, doors=(), gaps=(), tex="darkplanks", style="dark"):
    m.floor_rect(x, y, w, h, tex)
    m.room(x, y, w, h, style, doors=doors, gaps=gaps)


def lava_patch(m, pts, seed=0):
    from hellkit import densify as _d
    q = random.Random(seed)
    m.add("floor", f'<polygon points="{" ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in pts)}" fill="#ff5a0a" opacity="0.6" filter="url(#glow)"/>')
    m.floor_poly(pts, "lava")
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    m.light(cx, cy, 10, 4, color="#ff6a1a", alpha=0.5, anim="fire", walls=False)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for _ in range(int((max(xs) - min(xs)) * (max(ys) - min(ys)) / 3) + 3):
        x, y = q.uniform(min(xs), max(xs)), q.uniform(min(ys), max(ys))
        col = q.choice(["#ffe27a", "#ff8a1a", "#c0300a", "#ffd04a"])
        m.add("floor", f'<ellipse cx="{x*100:.0f}" cy="{y*100:.0f}" rx="{q.uniform(50,150):.0f}" ry="{q.uniform(30,90):.0f}" fill="{col}" '
                       f'opacity="{q.uniform(0.15,0.35):.2f}" filter="url(#blur4)" clip-path="url(#cp-{id(pts)})"/>')
    m.defs.append(f'<clipPath id="cp-{id(pts)}"><polygon points="{" ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in pts)}"/></clipPath>')


# ======================================================================= MAP 3
@register
def greyhurst():
    """Map 3, 'The Fallen': the drowned town of Greyhurst on the lava shelf. After the 2020 original."""
    S = 48 / 44
    m = Map("greyhurst", "Map 3: The Fallen (Greyhurst)", 48, 36, seed=13, bg="#2a2426")
    hell_env(m, 0.25)
    m.defs.append('<radialGradient id="rg-dark"><stop offset="0" stop-color="#000" stop-opacity="0.9"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')
    m.fill_all("darkcobble")
    ground_mottle(m, 90, 3, cols=("#000000", "#3a2a22", "#1a1418"))
    P = lambda x, y: (x * S, y * S)
    PP = lambda pts: [P(*p) for p in pts]
    # lava along the top and the right edge
    top = PP([(-1, -1), (32.5, -1), (32, 1.2), (30, 2.8), (24, 3.2), (19, 3.6), (18.6, 4.8), (17.6, 3.6), (9, 3.4), (7.6, 5.6), (7, 3.4), (2, 3.2), (-1, 3.5)])
    lava_patch(m, top, 1)
    lava_patch(m, PP([(43.2, -1), (45, -1), (45, 34), (43.4, 34), (43.6, 20), (43.1, 10)]), 2)
    lava_patch(m, PP([(31.4, 8), (32.8, 7.8), (33.4, 10), (33.2, 13), (33, 16.2), (31.8, 16), (31, 13), (31.2, 10)]), 3)
    for x in range(2, 32, 6):
        m.light(*P(x, 1.5), 12, 4, color="#ff6a1a", alpha=0.5, anim="fire", walls=False)
    # house A (E1): the burgher's house
    house(m, *P(1.7, 7), 8.8 * S, 13.3 * S, doors=[("S", 4.2, 1.2, "wood"), ("E", 6, 1.2, "wood")])
    m.wall(PP([(1.7, 15.3), (4.4, 15.3)]), "timber"); m.wall(PP([(5.6, 15.3), (10.5, 15.3)]), "timber")
    m.wall(PP([(5.4, 7), (5.4, 10.6)]), "timber"); m.wall(PP([(5.4, 10.6), (7.2, 10.6)]), "timber")
    m.wall(PP([(5, 12.5), (5, 13.4), (4, 14.3)]), "timber")
    m.g("props", *P(3, 8.8), p2.bed(110, 180, "#6a1a24"), rot=90)
    m.g("props", *P(8, 8.2), pr.desk(160, 80))
    m.g("props", *P(3, 11.3), pr.barrel(30))
    m.g("props", *P(2.8, 17), p2.bed(110, 180, "#5a4a3a"), rot=-80)
    m.g("props", *P(9, 13.3), pr.table(130, 70), rot=80)
    m.g("lowprop", *P(7, 18), p2.debris(5, 60, 1), shadow=False)
    # the great hall roof and round tower
    gableroof(m, *P(12.6, 6.3), 8.7 * S, 14.2 * S)
    coneroof(m, *P(23, 9.4), 2.1 * S)
    # house C (E3): the clerk's house
    house(m, *P(22, 13), 7.5 * S, 6.7 * S, doors=[("S", 3.6, 1.2, "wood")])
    m.wall(PP([(25.8, 13), (25.8, 15.3)]), "timber"); m.wall(PP([(25.8, 16.5), (29.5, 16.5)]), "timber")
    m.g("props", *P(23, 15), pr.bookshelf(160, 40), rot=90)
    m.g("props", *P(28, 15), p2.bed(100, 170, "#e8dcc0"), rot=-90)
    m.g("props", *P(27.3, 16.9), pr.barrel(28))
    m.g("props", *P(25.4, 18.4), pr.chair())
    # top-right house (boss) with the ritual alcove
    house(m, *P(34.5, 1), 6.5 * S, 7 * S, doors=[("S", 3, 1.2, "iron")])
    m.floor_circle(*P(41.2, 4.4), 1.6 * S, "darkplanks")
    m.g("decal", *P(41.2, 4.4), p2.magic_circle(130, "#e0283a", 5), shadow=False)
    m.light(*P(41.2, 4.4), 8, 3, color="#ff2a3a", alpha=0.45, anim="pulse")
    m.g("props", *P(38, 4.5), pr.round_table(55))
    m.g("props", *P(36, 4.5), pr.chair(), rot=90)
    m.g("props", *P(37.5, 1.8), pr.barrel(28))
    # right hip roofs and house E4
    hiproof(m, *P(35, 10), 8 * S, 7 * S)
    house(m, *P(35.3, 17.5), 7.7 * S, 6.5 * S, doors=[("W", 1.5, 1.2, "wood")])
    m.wall(PP([(35.3, 21), (38.5, 21)]), "timber")
    m.g("props", *P(36.6, 22.8), p2.bed(100, 160, "#7a1a24"), rot=90)
    m.g("props", *P(38, 21.8), pr.barrel(26))
    m.g("props", *P(40, 18.5), pr.crate(50))
    hiproof(m, *P(35, 24.5), 8 * S, 8 * S)
    # bottom rows of hip roofs
    for i in range(3):
        hiproof(m, *P(1 + i * 4.7, 24.5), 4.7 * S, 7.5 * S)
        hiproof(m, *P(18.7 + i * 4.8, 24.5), 4.8 * S, 7.5 * S)
    # arrival disk at the west edge
    m.g("decal", *P(0.9, 22.5), p2.spawn_disk(78), shadow=False)
    m.light(*P(0.9, 22.5), 8, 3, color="#4aa0ff", alpha=0.4, anim="pulse")
    # street dressing: ash, bones, burst cobbles
    scatter(m, (0.3, 4.5, 47.5, 35.5), 70, ["bones", "debris", "pebbles", "darkrock"], seed=13,
            rects=[PP([(1.2, 6.5), (30, 21)]), PP([(34, 0), (44, 33)]), PP([(0.5, 24), (33.5, 33)])], avoid=[(*P(23, 9.4), 2.6), (*P(32.2, 9.5), 2.2), (*P(32.2, 13.5), 2.2)])
    for (x, y) in [(5, 22.2), (14, 22), (30, 22), (31, 5), (22, 5)]:
        m.g("props", *P(x, y), p2.brazier())
        m.light(*P(x, y), 6, 2, color="#ff9a3a", alpha=0.35, anim="torch")
    marker(m, *P(0.9, 22.5), "Arrival point (party spawn)")
    marker(m, *P(8, 9.8), "E1: The burgher's house")
    marker(m, *P(16.8, 27.2), "E2: Ash Street")
    marker(m, *P(25, 13.8), "E3: The clerk's house")
    marker(m, *P(41, 20.5), "E4: The widow's house")
    marker(m, *P(41.2, 4.4), "Boss: the ritual alcove")
    return m


# ======================================================================= MAPS 4-5
def arc_pts(cx, cy, r, a0, a1, step=10):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(a0, a1 + 1, step)]


def mansion_shell(m, upper=False):
    """The shared footprint of Janella's mansion (both floors). Grid units on a 48x32 map."""
    hell_env(m, 0.3)
    m.fill_all("redsand")
    ground_mottle(m, 90, 4)
    # lava corners
    lava_patch(m, [(30, -1), (49, -1), (49, 13), (46.5, 11), (45, 6), (42, 3.5), (36, 2.5), (31, 1.5)], 11)
    lava_patch(m, [(26, 33), (49, 33), (49, 25), (46, 27.5), (41, 28.5), (36, 29.8), (30, 30.5)], 12)
    lava_patch(m, [(-1, 26), (1.5, 27), (2, 30), (3.5, 33), (-1, 33)], 13)
    # crust bands around the lava
    from hellkit import _offset, densify as _dz
    for pts in ([(30, 1.5), (36, 2.5), (42, 3.5), (45, 6), (46.5, 11), (49.5, 13.5)], [(29, 30.6), (36, 29.8), (41, 28.5), (46, 27.5), (49.5, 25)]):
        c = _dz(pts, 0.5)
        q = random.Random(len(pts))
        m.floor_poly(_offset(c, 0.7, q, 0.2) + _offset(c, -0.7, q, 0.2)[::-1], "basalt", layer="floor")
    # floors
    hall = [(11, 4.6), (28.9, 4.6)] + arc_pts(28.9, 15.4, 10.8, -90, 90) + [(28.9, 26.2), (14.3, 26.2), (14.3, 20.7), (11, 20.7)]
    m.floor_poly(hall, "paleflag")
    for (x, y, rot) in ((19, 23.4, 90), (26, 23.4, 90), (34, 15.4, 0), (25, 6.4, 90)):
        m.g("decal", x, y, p2.arch_tracery(220, 520), rot=rot, shadow=False)
    m.floor_rect(0.5, 0.4, 11.4, 17.2, "paleflag")
    oc, R = (8.4, 23.8), 6.1
    octo = [(oc[0] + R * math.cos(math.radians(22.5 + 45 * i)), oc[1] + R * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    m.floor_poly(octo, "manortile")
    # causeway
    m.floor_rect(39.7, 12.2, 9, 5.1, "darkcobble")
    # walls: ritual room / bedroom (top-left)
    m.wall([(11.9, 6), (11.9, 0.4), (0.5, 0.4), (0.5, 17.6), (4.2, 17.6)], "keep")
    m.door(4.2, 17.6, 5.8, 17.6, "iron")
    m.wall([(5.8, 17.6), (11.9, 17.6), (11.9, 7.6)], "keep")
    m.door(11.9, 6, 11.9, 7.6, "wood")
    # hall outer walls
    m.wall([(11.9, 4.6), (28.9, 4.6)] + arc_pts(28.9, 15.4, 10.8, -90, -25, 8), "keep")
    m.wall(arc_pts(28.9, 15.4, 10.8, 25, 90, 8) + [(28.9, 26.2), (14.3, 26.2)], "keep")
    ex = arc_pts(28.9, 15.4, 10.8, -25, 25, 25)
    m.door(*ex[0], *ex[1], "brass"); m.door(*ex[1], *ex[2], "brass")
    m.g("walls", 39.6, 15.4, p2.double_door_gate(560), rot=90)
    # octagon walls with door into the hall
    for i in range(8):
        a, b = octo[i], octo[(i + 1) % 8]
        if i == 0:   # east face: door to the hall
            m.wall([a, (a[0], a[1] + 0.2)], "keep")
            continue
        m.wall([a, b], "keep")
    m.door(octo[0][0], octo[7][1] + 0.6, octo[0][0], octo[0][1] - 0.2, "wood") if False else None
    m.door(14.1, 21.5, 14.1, 25.2, "iron")
    # stair well
    m.wall([(27.6, 8.2), (27.6, 21.3)], "keep")
    m.wall([(31.4, 8.2), (31.4, 21.3)], "keep")
    m.g("props", 29.5, 14.75, p2.stairs(330, 1260, 18), shadow=False)
    m.text(29.5, 7.8, "UP" if not upper else "DOWN", size=44)
    return hall, octo, oc


@register
def mansion_lower():
    """Map 4: Janella's mansion, ground floor. After the 2020 original."""
    m = Map("mansion-lower", "Map 4: The Mansion (Ground Floor)", 48, 32, seed=14, bg="#3a1a14")
    hall, octo, oc = mansion_shell(m)
    # centre chamber with chains (E2 green)
    m.floor_rect(11.9, 8.2, 11.5, 12.5, "flagstone", stroke=False)
    m.wall([(11.9, 8.2), (23.4, 8.2), (23.4, 15.8)], "keep")
    m.door(23.4, 15.8, 23.4, 17.6, "iron")
    m.wall([(23.4, 17.6), (23.4, 20.7), (14.3, 20.7)], "keep")
    m.wall([(11.9, 17.6), (11.9, 20.7), (14.3, 20.7)], "stone", draw=False)
    m.add("decal", '<path d="M1760 830 V2050 M1200 1440 H2320" stroke="#c09040" stroke-width="18" opacity="0.6"/>')
    for x in (14.3, 19.6):
        m.g("props", x, 12, p2.hanging_chains(380, 4, int(x)), shadow=False)
    m.g("props", 17, 11, pr.chair(), rot=180)
    m.g("lowprop", 13.5, 18.5, p2.skeleton(4), shadow=False, scale=1.5)
    m.g("props", 22, 19.5, pr.chair(), rot=30)
    # ritual room: chests, altar, red circle, throne
    for x in (3, 5.1, 7.4, 9.5):
        m.g("props", x, 1.6, p2.chest(88))
    m.g("decal", 6.3, 8.8, p2.magic_circle(260, "#e0283a", 5, glow=True), shadow=False)
    m.g("props", 6.3, 8.8, p2.altar(160, 380))
    m.light(6.3, 8.8, 12, 5, color="#c04aff", alpha=0.4, anim="pulse")
    for (x, y, lab, col) in ((2.6, 5.2, "NAME", "#c0283a"), (10, 5.2, "CONSENT", "#2a8ad0"), (2.6, 12.6, "WITNESS", "#d8aa52"), (10, 12.6, "JURISDICTION", "#7a3ac0")):
        m.g("props", x, y, p2.plinth(lab, col))
    m.g("props", 6.1, 15.6, p2.wardrobe(200, 90))
    # octagon study: desk, circle, astrolabe
    m.g("props", 6.3, 20.8, pr.desk(220, 120), rot=-25)
    m.g("decal", 10.2, 23.8, p2.magic_circle(140, "#e0283a", 7), shadow=False)
    m.light(10.2, 23.8, 8, 3, color="#ffe27a", alpha=0.35, anim="pulse")
    m.g("props", 7.4, 26.8, p2.astrolabe(140))
    m.g("props", 3.6, 22.5, pr.bookshelf(240, 44), rot=-67)
    m.g("lowprop", 4, 25, p2.skeleton(9), shadow=False, scale=1.5)
    for (x, y, r) in ((5.2, 18.7, -45), (2.6, 26, 90), (5.6, 29.3, 135)):
        m.g("props", x, y, p2.mirror(110), rot=r)
    # hall dressing: weapons rack, skeletons, braziers
    m.g("props", 25, 5.3, pr.scroll_rack(300, 46))
    for (x, y) in ((34, 8), (34, 22.5), (16, 23.4), (24, 23.4)):
        m.g("props", x, y, p2.brazier())
        m.light(x, y, 7, 3, color="#ff9a3a", alpha=0.35, anim="torch")
    # outside: wyrm bones
    m.g("lowprop", 42, 6.5, p2.dragon_skeleton(420), shadow=False, rot=10)
    m.g("lowprop", 42.5, 25.5, p2.dragon_skeleton(420), shadow=False, rot=30)
    m.g("decal", 44.5, 14.6, p2.spawn_disk(78), shadow=False)
    m.light(44.5, 14.6, 8, 3, color="#4aa0ff", alpha=0.4, anim="pulse")
    scatter(m, (0.2, 0.2, 47.8, 31.8), 60, ["bones", "pebbles", "rock", "darkrock", "skeleton"], seed=14,
            rects=[((0, 0), (40.2, 31)), ((39.5, 11.8), (49, 17.8)), ((29, -1), (49, 4)), ((43.5, 0), (49, 12.5)), ((25, 28.5), (49, 33)), ((44, 24), (49, 33)), ((-1, 25.5), (4, 33))])
    marker(m, 44.5, 14.6, "Arrival point (causeway)")
    marker(m, 35, 14.6, "E1: The grand hall")
    marker(m, 16.7, 13.5, "E2: The chain room")
    marker(m, 9.8, 7, "E3 / 4B: The inverse circle (four plinths)")
    marker(m, 10.2, 23.8, "E4 / 4D: The soul-split mirrors")
    marker(m, 13.5, 18.5, "4A: The house of witnesses (spectral clerk)")
    marker(m, 33, 19, "4C: Mother Sable's truce")
    return m


@register
def mansion_upper():
    """Map 5: Janella's mansion, upper floor. After the 2020 original."""
    m = Map("mansion-upper", "Map 5: The Mansion (Upper Floor)", 48, 32, seed=15, bg="#3a1a14")
    hall, octo, oc = mansion_shell(m, upper=True)
    # the roof of the chain room, seen from the gallery
    hiproof(m, 11.9, 8.6, 11.5, 12.5)
    # cage cells beside the stair (E2 green)
    m.wall([(23.4, 8.6), (27.6, 8.6)], "keep"); m.wall([(23.4, 21.1), (27.6, 21.1)], "keep")
    m.wall([(23.4, 14.2), (25, 14.2)], "keep"); m.wall([(23.4, 16.2), (25, 16.2)], "keep")
    m.door(23.4, 9.2, 23.4, 10.6, "iron") if False else None
    m.g("props", 25.5, 12.4, pr.cage(150, 120))
    m.g("props", 25.5, 18, pr.cage(150, 120))
    # top-left: broken bed and the drowned bed
    m.g("props", 5.9, 4.6, p2.broken_bed(260, 200))
    m.g("props", 5.9, 12.4, p2.drowned_bed(300, 320))
    m.light(5.9, 12.4, 6, 2, color="#8a6aff", alpha=0.35, anim="pulse")
    m.g("props", 10.6, 3, p2.wardrobe(150, 60), rot=90)
    m.g("props", 9, 9.5, pr.desk(180, 90), rot=90)
    m.g("props", 8.2, 9.5, pr.chair(), rot=-90)
    # treasury octagon (boss red)
    m.g("props", 6, 24.6, p2.gold_pile(170, 3))
    m.light(6, 24.6, 8, 3, color="#ffd84a", alpha=0.35)
    for (x, y) in ((7.4, 19.2), (9.8, 19.2), (7.4, 28.4), (9.8, 28.4)):
        m.g("props", x, y, pr.barrel(36))
    m.g("props", 12, 22.5, p2.chest(88), rot=-90)
    m.add("decal", f'<ellipse cx="900" cy="2400" rx="420" ry="360" fill="#3a1a14" opacity="0.4" filter="url(#blur4)"/>')
    # gallery dressing
    for (x, y) in ((34, 8), (34, 22.5), (18, 5.6)):
        m.g("props", x, y, p2.brazier())
        m.light(x, y, 7, 3, color="#ff9a3a", alpha=0.35, anim="torch")
    m.g("lowprop", 25.5, 5.8, p2.skeleton(6), shadow=False, scale=1.5)
    m.g("props", 18, 23.4, pr.table(240, 90, cloth="#5e0b18"))
    m.g("lowprop", 42, 6.5, p2.dragon_skeleton(420), shadow=False, rot=10)
    m.g("lowprop", 42.5, 25.5, p2.dragon_skeleton(420), shadow=False, rot=30)
    scatter(m, (0.2, 0.2, 47.8, 31.8), 60, ["bones", "pebbles", "rock", "darkrock"], seed=15,
            rects=[((0, 0), (40.2, 31)), ((39.5, 11.8), (49, 17.8)), ((29, -1), (49, 4)), ((43.5, 0), (49, 12.5)), ((25, 28.5), (49, 33)), ((44, 24), (49, 33)), ((-1, 25.5), (4, 33))])
    marker(m, 29.7, 24.3, "E1: The upper gallery")
    marker(m, 25.5, 15.2, "E2: The cage cells")
    marker(m, 8.6, 7.5, "E3 / 5B: Kane's chambers")
    marker(m, 11.2, 24.3, "Boss / 5A: The Treasury of Names")
    marker(m, 25.5, 18, "5C: The warded core")
    return m


# ======================================================================= MAP 6
@register
def arena():
    """Map 6: the Brass Arena of the Interplanal Championship. After the 2020 original."""
    m = Map("arena", "Map 6: The Brass Arena", 40, 40, seed=16, bg="#2a0c08")
    hell_env(m, 0.35)
    m.fill_all("bigbasalt")
    for x, y in ((3, 3), (37, 3), (3, 37), (37, 37)):
        m.light(x, y, 14, 5, color="#ff5a1a", alpha=0.5, anim="fire", walls=False)
    c, ap = 20, 17.0
    R = ap / math.cos(math.radians(22.5))
    octo = [(c + R * math.cos(math.radians(22.5 + 45 * i)), c + R * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    m.floor_poly(octo, "arenastone")
    # gothic arch inlays (3 columns, 2 rows), as in the original floor
    for gx in (9.5, 20, 30.5):
        for gy in (12, 27):
            m.g("decal", gx, gy, p2.arch_tracery(760, 1300), shadow=False)
    # lava cross
    for (x1, y1, x2, y2) in ((4.5, 20.3, 35.5, 20.3), (20, 4.5, 20, 35.5)):
        pts = [(x1, y1), (x2, y2)]
        hw = 0.6
        if y1 == y2:
            poly = [(x1, y1 - hw), (x2, y1 - hw), (x2, y1 + hw), (x1, y1 + hw)]
        else:
            poly = [(x1 - hw, y1), (x1 + hw, y1), (x1 + hw, y2), (x1 - hw, y2)]
        m.add("floor", f'<polygon points="{" ".join(f"{a*100:.0f},{b*100:.0f}" for a, b in poly)}" fill="#ff3a0a" opacity="0.7" filter="url(#glow)"/>')
        m.floor_poly(poly, "lava")
        for t in range(6):
            lx = x1 + (x2 - x1) * (t + 0.5) / 6
            ly = y1 + (y2 - y1) * (t + 0.5) / 6
            m.light(lx, ly, 5, 1.5, color="#ff4a1a", alpha=0.45, anim="fire", walls=False)
    # central nonagon star platform
    m.g("props", c, c + 0.3, p2.central_platform(440), shadow=True)
    m.light(c, c + 0.3, 14, 5, color="#7ae0ff", alpha=0.45, anim="pulse")
    # glyph rings, crystals, chests
    for (x, y) in ((27.8, 12.2), (11.4, 28.1)):
        m.g("decal", x, y, p2.glyph_ring(200), shadow=False)
        m.light(x, y, 6, 2, color="#a88aff", alpha=0.45, anim="sunburst" if False else "pulse")
    m.g("props", 10.8, 11.2, p2.crystal("blue", 4, 1), scale=2.3)
    m.light(10.8, 11.2, 6, 2, color="#7ad0ff", alpha=0.4, anim="pulse")
    m.g("props", 28.7, 26.8, p2.crystal("yellow", 5, 2), scale=2.3)
    m.light(28.7, 26.8, 6, 2, color="#ffe27a", alpha=0.4, anim="pulse")
    m.g("props", 11.8, 7.2, p2.chest(130), rot=30)
    m.g("props", 30.2, 30.6, p2.chest(130), rot=30)
    # the octagonal curtain wall (thick blocks) with the gate on the south face
    out = [(c + (R + 1.6) * math.cos(math.radians(22.5 + 45 * i)), c + (R + 1.6) * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    mid = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(octo, out)]
    blocks = []
    for i in range(8):
        a, b = mid[i], mid[(i + 1) % 8]
        if i == 1:  # south face (between 67.5 and 112.5 degrees): the gate
            ga = (a[0] + (b[0] - a[0]) * 0.18, a[1]); gb = (a[0] + (b[0] - a[0]) * 0.82, a[1])
            blocks.append([(a[0] * 100, a[1] * 100), (ga[0] * 100, ga[1] * 100)])
            blocks.append([(gb[0] * 100, gb[1] * 100), (b[0] * 100, b[1] * 100)])
            m.wall([a, ga], "keep", draw=False); m.wall([gb, b], "keep", draw=False)
            m.door(ga[0], ga[1], gb[0], gb[1], "brass", locked=True)
            gx = (a[0] + b[0]) / 2
            m.g("walls", gx, a[1], p2.gate(abs(gb[0] - ga[0]) * 100 + 60))
            m.g("lowprop", gx, a[1] + 1.3, p2.stairs(abs(gb[0] - ga[0]) * 100 - 80, 160, 3, vertical=True), shadow=False)
            continue
        blocks.append([(a[0] * 100, a[1] * 100), (b[0] * 100, b[1] * 100)])
        m.wall([a, b], "keep", draw=False)
    for i, bl in enumerate(blocks):
        m.g("walls", 0, 0, p2.ruin_blocks(bl, seed=60 + i, w=165, seg=230).replace("#6e6a74", "#5e6a6a").replace("#77737e", "#667272"))
    marker(m, 20, 37, "The Gate of Entry")
    marker(m, 20, 20.3, "6: The Nonagon Dais")
    marker(m, 27.8, 12.2, "2: Summoning glyph (NE)")
    marker(m, 11.4, 28.1, "2: Summoning glyph (SW)")
    marker(m, 10.8, 11.2, "3: Frost crystals")
    marker(m, 28.7, 26.8, "5: Sun crystals")
    marker(m, 20, 9, "4: The burning cross")
    return m


# ======================================================================= LOCATION MAPS (Chapter I-II)
def imp_booth(label):
    return (pr.rect(180, 110, "#5a2e18", 8, 6) + pr.rect(160, 40, "#c09040", 4, 4)
            + f'<text x="0" y="40" font-family="Cinzel" font-weight="700" font-size="20" fill="#f0e2c0" stroke="{INK}" stroke-width="3" paint-order="stroke" text-anchor="middle">{label}</text>')


@register
def counting_gate():
    """1A: The Counting Gate. Two imps, a toll desk and a bone-and-brass curtain wall."""
    m = Map("counting-gate", "1A: The Counting Gate", 26, 20, seed=21, bg="#3a1a14")
    hell_env(m)
    m.fill_all("redsand"); ground_mottle(m, 50, 21)
    m.floor_rect(9, 0, 8, 20, "darkcobble", stroke=False)
    # curtain wall of brass and bone across the road
    m.wall([(0, 8), (10.2, 8)], "brass"); m.wall([(15.8, 8), (26, 8)], "brass")
    for x in range(1, 26, 3):
        if 10 < x < 16:
            continue
        m.g("walls", x, 8, p2.skull(1.3))
    m.g("walls", 10.6, 8, pr.pillar(60, "#5a4a3a")); m.g("walls", 15.4, 8, pr.pillar(60, "#5a4a3a"))
    m.door(10.9, 8, 13, 8, "brass", locked=True); m.door(13, 8, 15.1, 8, "brass", locked=True)
    m.text(13, 7.2, "ALL CLAIMANTS DECLARE", size=40, color="#ffd27a")
    # imp toll booths
    m.g("props", 7.4, 10.3, imp_booth("NAMES"), rot=0)
    m.g("props", 18.6, 10.3, imp_booth("SLATES"), rot=0)
    m.g("props", 13, 11.5, pr.ledger_book(220, 150))
    m.g("props", 13, 13.4, pr.scales(), scale=1.3)
    for x in (7.4, 18.6):
        m.g("props", x, 12.2, p2.brazier())
        m.light(x, 12.2, 6, 2, color="#ff9a3a", alpha=0.35, anim="torch")
    m.g("props", 4, 16, p2.signpost(("ALL COMPLAINTS", "FILED IN", "TRIPLICATE")), rot=8)
    m.g("props", 21.5, 15.5, pr.crate(70)); m.g("props", 22.6, 16.3, pr.crate(60)); m.g("props", 20.5, 16.6, pr.barrel(30))
    # queue rope posts
    for y in (12.5, 14.5, 16.5):
        m.g("props", 10.5, y, pr.pillar(14, "#c09040")); m.g("props", 15.5, y, pr.pillar(14, "#c09040"))
    m.add("lowprop", '<path d="M1050 1250 V1650 M1550 1250 V1650" stroke="#8e1424" stroke-width="10"/>')
    scatter(m, (0.3, 0.3, 25.7, 19.7), 40, ["bones", "rock", "pebbles", "darkrock"], seed=21, rects=[((8.5, 0), (17.5, 20)), ((0, 7), (26, 9))])
    m.token("imp-tollkeeper", 7.4, 9.2); m.token("imp-tollkeeper", 18.6, 9.2)
    marker(m, 13, 11.5, "1A: The toll desk (appeal is free)")
    return m


@register
def ash_bridge():
    """1B-1D: The Ash Bridge, the Three Witnesses and the damaged war machine."""
    m = Map("ash-bridge", "1B: The Ash Bridge", 32, 22, seed=22, bg="#3a1a14")
    hell_env(m)
    m.fill_all("redsand"); ground_mottle(m, 50, 22)
    RV = [(10, -1), (11, 6), (11.5, 12), (12, 18), (12.5, 23)]
    river(m, RV, 12, seed=22, crust=0.8)
    # broken platforms: a 60-foot crossing (12 squares)
    plats = [(6.8, 10.6, 160, 120), (8.6, 11.4, 120, 100), (10.4, 10.6, 140, 120), (12.4, 11.6, 120, 100),
             (14.2, 10.8, 140, 110), (16.2, 11.4, 160, 130)]
    for i, (x, y, w, h) in enumerate(plats):
        m.g("props", x, y, p2.platform(w, h, i))
    m.add("decal", '<path d="M520 1080 L1780 1120" stroke="#3a2a1a" stroke-width="10" stroke-dasharray="40 30" opacity="0.8"/>')
    m.g("props", 3.5, 11, pr.pillar(46, "#5a4a3a")); m.g("props", 19.5, 11.4, pr.pillar(46, "#5a4a3a"))
    # the three witnesses (floating skull notaries)
    for (x, y) in ((22.5, 6), (24.5, 5), (26.5, 6)):
        m.g("high", x, y, f'<circle r="55" fill="#7ad0a0" opacity="0.25"/>{p2.skull(2.2)}')
        m.light(x, y, 4, 1, color="#7ad0a0", alpha=0.4, anim="pulse")
    m.g("props", 24.5, 7.4, pr.lectern())
    # the damaged war machine (1D)
    m.g("props", 25, 16, p2.iron_golem_slumped(0.9).replace("JANELLA", "J.G."))
    m.g("lowprop", 27.4, 17.4, p2.golem_parts(3), shadow=False)
    m.g("props", 4, 4, p2.signpost(("WELCOME,", "PROSPECTIVE", "SOVEREIGN")), rot=-8)
    scatter(m, (0.3, 0.3, 31.7, 21.7), 45, ["bones", "rock", "pebbles", "darkrock", "skeleton"], seed=22,
            lines=[(RV, 7.5)], avoid=[(25, 16, 3), (24.5, 6, 3)])
    m.token("skull-notary", 22.5, 6, hidden=True); m.token("skull-notary", 24.5, 5, hidden=True); m.token("skull-notary", 26.5, 6, hidden=True)
    m.token("iron-warder-damaged", 25, 16, hidden=True)
    marker(m, 11.5, 11, "1B: The crossing (3 successes before 2 failures, DC 16)")
    marker(m, 24.5, 6, "1C: The Three Witnesses (Proof of Survival)")
    marker(m, 25, 16, "1D: The damaged war machine (J.G.)")
    return m


@register
def styx_ferry():
    """2A-2C: Where the black Styx touches the ashflow. The ferryman's landing."""
    m = Map("styx-ferry", "2B: The Ferryman's Landing", 32, 22, seed=23, bg="#2a2426")
    hell_env(m, 0.3)
    m.fill_all("ashsand"); ground_mottle(m, 60, 23, cols=("#3a2a22", "#a8885c", "#2a2a3a"))
    LV = [(-1, 3), (8, 6), (16, 7), (24, 6.5), (33, 4)]
    river(m, LV, 5, seed=23, crust=0.7)
    # the black Styx branch, joining from the south
    ST = [(18, 23), (17, 18), (15.5, 13), (16, 9)]
    from hellkit import _offset
    c = densify(ST, 0.5)
    q = random.Random(5)
    poly = _offset(c, 2.6, q, 0.2) + _offset(c, -2.6, q, 0.2)[::-1]
    m.add("floor", f'<polygon points="{" ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in poly)}" fill="#0e0c14" stroke="{INK}" stroke-width="8"/>')
    for _ in range(40):
        x, y = c[q.randrange(len(c))]
        m.add("floor", f'<ellipse cx="{(x+q.uniform(-1.8,1.8))*100:.0f}" cy="{y*100:.0f}" rx="{q.uniform(40,110):.0f}" ry="{q.uniform(10,24):.0f}" fill="#3a3a5a" opacity="0.4"/>')
    m.add("floor", '<ellipse cx="1600" cy="880" rx="300" ry="140" fill="#ff7a1a" opacity="0.35" filter="url(#glow)"/>')
    m.light(16, 9, 6, 2, color="#ff9a3a", alpha=0.35, anim="smokepatch")
    # landing jetty and ferry
    m.floor_rect(19.4, 13, 6, 2.2, "darkplanks")
    for x in (19.6, 22, 24.8):
        for y in (13.1, 15.1):
            m.g("props", x, y, pr.pillar(18, "#3a2a1a"))
    m.g("props", 17.4, 15.5, p2.ferry(360, 130), rot=-80)
    m.light(17.6, 14.2, 5, 2, color="#7ad0a0", alpha=0.4, anim="torch")
    # the floating docket casket (2A)
    m.g("props", 9, 6.3, pr.rect(80, 50, "#c09040", 6, 5) + '<rect x="-30" y="-6" width="60" height="12" fill="#8a6010"/>', rot=20)
    # the iron warning
    m.g("props", 26, 18.5, pr.rect(340, 70, "#3a3640", 6, 6)
        + f'<text x="0" y="8" font-family="Cinzel" font-weight="700" font-size="22" fill="#d8aa52" text-anchor="middle">THE UNCLAIMED ARE PROPERTY</text>')
    # the Ashclad Petitioners' last stand (2C)
    m.g("props", 6, 17, p2.rock(150, 8)); m.g("props", 8.5, 18.5, p2.rock(110, 9))
    m.g("lowprop", 7.4, 15.4, p2.debris(5, 70, 2), shadow=False)
    scatter(m, (0.3, 0.3, 31.7, 21.7), 55, ["bones", "rock", "pebbles", "darkrock", "skeleton"], seed=23,
            lines=[(LV, 4.4), (ST, 3.4)], rects=[((19, 12.5), (26, 15.6))])
    m.token("styx-ferryman", 17.4, 15.5)
    m.token("vexa-corven", 7, 15.8); m.token("ash-scrap-golem", 4, 13.5)
    marker(m, 9, 6.3, "2A: The floating docket (Exhibit A)")
    marker(m, 17.4, 15.5, "2B: The ferryman's bargain")
    marker(m, 6.5, 16.5, "2C: The Ashclad Petitioners under attack")
    marker(m, 26, 18.5, "The iron warning")
    return m


@register
def tavern():
    """3A: The Drowned Tavern in Greyhurst. A celebration that never happened."""
    m = Map("tavern", "3A: The Drowned Tavern", 26, 20, seed=24, bg="#1a1416")
    hell_env(m, 0.4)
    m.fill_all("darkcobble")
    house(m, 2, 2, 22, 16, doors=[("S", 10, 2, "wood"), ("E", 11, 1.4, "wood")])
    m.wall([(17, 2), (17, 9)], "dark"); m.door(17, 9, 17, 10.4, "wood"); m.wall([(17, 10.4), (17, 18)], "dark")
    # ash drift across the floor
    for (x, y, r) in ((8, 15, 2.5), (13, 6, 1.6), (4, 9, 1.4)):
        stain(m, x, y, r, "#8a8078", 0.45)
    m.g("props", 9.5, 9.2, p2.long_table(900, 1, True))
    for i in range(7):
        m.g("props", 5.8 + i * 1.25, 8.1, pr.chair(), rot=180); m.g("props", 5.8 + i * 1.25, 10.3, pr.chair())
    m.g("props", 9.5, 9.2, '<rect x="-80" y="-50" width="160" height="100" fill="#efe6d0" stroke="#150b0b" stroke-width="4"/>'
        '<text x="0" y="-12" font-family="Cinzel" font-size="20" font-weight="700" fill="#3a1a10" text-anchor="middle">GUESTS</text>'
        '<text x="0" y="16" font-family="Cinzel" font-size="16" fill="#8e1424" text-anchor="middle">MARUS ___</text>', shadow=False)
    m.g("props", 3.2, 4, p2.bar_counter(560, False))
    m.g("props", 2.8, 13.5, p2.keg_rack(3), rot=90)
    m.g("props", 13.5, 4, pr.round_table(55)); m.g("props", 13.5, 15, pr.round_table(55))
    m.g("props", 20.5, 5, p2.bed(110, 190, "#5a1a24")); m.g("props", 22.6, 5, p2.bed(110, 190, "#5a1a24"))
    m.g("props", 20.5, 14.5, pr.crate(70)); m.g("props", 22, 15.5, pr.barrel(30)); m.g("props", 22.5, 13.2, pr.barrel(30))
    m.g("props", 9.5, 3, '<rect x="-180" y="-20" width="360" height="40" fill="#8e1424" stroke="#150b0b" stroke-width="4"/>'
        '<text x="0" y="10" font-family="Cinzel" font-size="24" font-weight="700" fill="#ffd27a" text-anchor="middle">WELCOME HOME</text>', shadow=False)
    for (x, y) in ((6, 6), (13, 12.4), (4.5, 16.5)):
        m.g("props", x, y, p2.brazier(26))
        m.light(x, y, 6, 2, color="#ff9a3a", alpha=0.35, anim="torch")
    m.g("lowprop", 6, 13.5, p2.skeleton(2), shadow=False, scale=1.4)
    m.g("lowprop", 15, 7, p2.debris(4, 50, 4), shadow=False)
    marker(m, 9.5, 9.2, "3A: The guest list (Marus missing)")
    return m


@register
def greenbottle():
    """3B, 3C, 3E: The alley golem, the Greenbottle house and the evacuation bell."""
    m = Map("greenbottle", "3B-3C: The Greenbottle Alley", 30, 22, seed=25, bg="#1a1416")
    hell_env(m, 0.35)
    m.fill_all("darkcobble"); ground_mottle(m, 40, 25, cols=("#000000", "#3a2a22"))
    # collapsed house (3C)
    m.floor_rect(2, 2, 11, 9, "darkplanks")
    m.wall([(2, 6), (2, 2), (13, 2), (13, 5)], "dark")
    m.wall([(13, 7), (13, 11), (8, 11)], "dark"); m.door(6.5, 11, 8, 11, "wood")
    m.wall([(6.5, 11), (2, 11), (2, 8.5)], "dark")
    m.wall([(7, 2), (7, 7)], "timber")
    m.g("lowprop", 3.5, 7.2, p2.debris(8, 90, 5), shadow=False)
    m.g("props", 3.6, 7.2, p2.rock(110, 3, fill="#5a5660", light="#8a8690"))
    m.g("props", 10, 4, p2.workbench(260, 100, 2)); m.g("props", 10, 8.5, p2.forge(80))
    m.light(10, 8.5, 6, 2, color="#ff8a3a", alpha=0.4, anim="torch")
    m.g("props", 4.5, 3.4, p2.bed(100, 160, "#3a5a3a"), rot=90)
    m.g("props", 11.6, 9.8, pr.ledger_book(160, 110))
    # the alley and the slumped Iron Warder (3B)
    m.floor_rect(13, 0, 4, 22, "darkcobble", stroke=False)
    hiproof(m, 17, 1, 11, 8)
    m.wall([(17, 11), (17, 21)], "dark")
    m.g("props", 18.6, 13.5, p2.iron_golem_slumped(1.1))
    m.g("lowprop", 15, 16.5, p2.golem_parts(9), shadow=False)
    # the evacuation bell (3E)
    m.floor_rect(3, 14, 9, 7, "paleflag")
    m.g("props", 7.5, 17.5, pr.bell_frame(260))
    m.text(7.5, 20.4, "SOUND FOR THE LIVING", size=30, color="#ffd27a")
    for (x, y) in ((15, 3), (15, 11), (15, 19)):
        m.g("props", x, y, p2.brazier(26))
        m.light(x, y, 6, 2, color="#ff9a3a", alpha=0.35, anim="torch")
    hiproof(m, 21, 12, 8, 9)
    scatter(m, (0.3, 0.3, 29.7, 21.7), 40, ["bones", "debris", "pebbles"], seed=25,
            rects=[((2, 2), (13, 11)), ((17, 1), (30, 22)), ((3, 14), (12, 21))])
    m.token("iron-warder-damaged", 18.6, 13.5)
    m.token("janella-greenbottle", 10, 5.4, hidden=True); m.token("lila-greenbottle", 9, 5.6, hidden=True)
    marker(m, 18.6, 13.5, "3B: WARD HOUSE, NEVER WAR HOUSE")
    marker(m, 10, 5, "3C: The Greenbottle family hide-out")
    marker(m, 7.5, 17.5, "3E: The evacuation bell")
    marker(m, 15, 8, "3D: The false mayor's guard patrol route")
    return m


# ======================================================================= LOCATION MAPS (Chapter III-V)
@register
def market_names():
    """Session 8: The Market of Names, a bazaar inside the ribcage of a fallen titan."""
    m = Map("market-names", "The Market of Names", 36, 28, seed=26, bg="#2a1a14")
    hell_env(m, 0.2)
    m.fill_all("bonefloor"); ground_mottle(m, 60, 26, cols=("#5a4a3a", "#e8dcc0", "#3a2a1a"))
    m.floor_rect(0, 12, 36, 4, "darkcobble", stroke=False)
    # titan spine and ribs
    for x in range(2, 36, 3):
        m.g("props", x, 14, p2.vertebra(90))
    for i, x in enumerate(range(3, 35, 5)):
        m.g("high", x, 12.2, p2.rib_arc(1000, 1), rot=-10, shadow=False)
        m.g("high", x, 15.8, p2.rib_arc(1000, 1), rot=190, shadow=False)
    # stalls along the avenue
    cols = [("#8e1424", "#d8aa52"), ("#2a4a6a", "#efe6d0"), ("#3a5a2a", "#d8c08a"), ("#5a2a6a", "#e8c35a")]
    q = random.Random(26)
    for i, x in enumerate(range(4, 34, 5)):
        a, b = cols[i % 4]
        m.g("props", x, 9.4, pr.stall(240, 140, a, b, seed=i))
        m.g("props", x + 1.5, 19, pr.stall(240, 140, *cols[(i + 2) % 4], seed=i + 9), rot=180)
    # Orro's ledger stall
    m.g("props", 18, 4.5, p2.ledger_stall(400, 180, 3))
    m.g("props", 18, 6.4, pr.scroll_rack(300, 46))
    m.g("props", 15.4, 4.6, pr.cage(150, 120)); m.g("props", 20.6, 4.6, pr.cage(150, 120))
    m.text(18, 2.4, "NAMES BOUGHT & SOLD", size=44, color="#ffd27a")
    for (x, y) in ((6, 14), (18, 14), (30, 14), (11, 22), (25, 22)):
        m.g("props", x, y + (0 if y != 14 else 0), p2.brazier(26)) if y != 14 else None
        m.light(x, y, 8, 3, color="#ff9a3a", alpha=0.3, anim="torch")
    m.g("props", 18, 24.5, p2.banner_stand("#8e1424", "#d8aa52", "crown"))
    scatter(m, (0.3, 0.3, 35.7, 27.7), 40, ["bones", "pebbles"], seed=26, rects=[((0, 7.5), (36, 21)), ((13, 2), (23, 7.5))])
    m.token("sergeant-orro", 18, 5.6)
    m.token("ash-scrap-golem", 15, 7.5, hidden=True); m.token("ash-scrap-golem", 21, 7.5, hidden=True); m.token("writ-bailiff", 18, 7.8, hidden=True)
    marker(m, 18, 4.5, "Orro's ledger stall (Exhibit E: Chain of Title)")
    return m


@register
def docket():
    """Session 10: The Whispering Docket, a courthouse riding a moving fortress."""
    m = Map("docket", "The Whispering Docket", 30, 26, seed=27, bg="#1a1012")
    hell_env(m, 0.3)
    m.fill_all("hellroof")
    m.floor_rect(2, 2, 26, 22, "marble")
    m.room(2, 2, 26, 22, "brass", doors=[("S", 12, 2, "brass")])
    m.g("decal", 15, 13, pr.rug(800, 1300), shadow=False)
    m.g("props", 15, 5, p2.judge_bench(900, 180))
    m.g("props", 15, 3.4, p2.throne(200, 160) if hasattr(p2, "throne") else pr.throne(200, 160))
    m.g("props", 8.5, 7.5, p2.witness_stand()); m.g("props", 21.5, 7.5, p2.witness_stand())
    m.g("props", 10, 10.6, pr.table(360, 110)); m.g("props", 20, 10.6, pr.table(360, 110))
    for x in (8.6, 10, 11.4, 18.6, 20, 21.4):
        m.g("props", x, 11.6, pr.chair())
    m.add("lowprop", '<path d="M500 1250 H1350 M1650 1250 H2500" stroke="#c09040" stroke-width="16"/>')
    for row in range(4):
        y = 14 + row * 2.2
        m.g("props", 9, y, p2.pew(900)); m.g("props", 21, y, p2.pew(900))
    m.g("props", 4, 4.5, pr.scales(), scale=1.4); m.g("props", 26, 4.5, pr.bookshelf(240, 44), rot=90)
    for (x, y) in ((3.4, 12), (26.6, 12), (3.4, 21), (26.6, 21)):
        m.g("props", x, y, p2.brazier(26))
        m.light(x, y, 7, 3, color="#ff9a3a", alpha=0.3, anim="torch")
    m.light(15, 5, 10, 4, color="#ffd27a", alpha=0.3)
    m.token("magistrate-docket", 15, 4.2); m.token("hollis-valrick", 21.5, 7.5); m.token("mother-sable", 20, 10.6)
    marker(m, 15, 5, "The bench: Admissibility, Authority, Remedy")
    marker(m, 21.5, 7.5, "Hollis's immunity document")
    return m


@register
def masquerade():
    """Session 11: The Trial of False Faces, four chambers of a legal masquerade."""
    m = Map("masquerade", "The Trial of False Faces", 30, 24, seed=28, bg="#140e12")
    hell_env(m, 0.45)
    m.fill_all("hellroof")
    names = [("NAME", "#c0283a", 1, 1), ("WITNESS", "#d8aa52", 16, 1), ("CONSIDERATION", "#2a8ad0", 16, 12.5), ("REMEDY", "#7a3ac0", 1, 12.5)]
    for i, (lab, col, x, y) in enumerate(names):
        m.floor_rect(x, y, 13, 10.5, "marble" if i % 2 == 0 else "carpet")
        m.room(x, y, 13, 10.5, "iron")
        m.text(x + 6.5, y + 1.3, f"CHAMBER OF {lab}", size=40, color=col)
        m.g("decal", x + 6.5, y + 5.5, p2.magic_circle(170, col, 7, glow=True), shadow=False)
        m.light(x + 6.5, y + 5.5, 7, 3, color=col, alpha=0.35, anim="pulse")
        for k in range(3):
            m.g("props", x + 2 + k * 4.5, y + 9, p2.mirror(110))
    m.door(14, 5, 16, 5, "iron"); m.door(22.5, 11.5, 22.5, 12.5, "iron"); m.door(14, 17.5, 16, 17.5, "iron")
    m.floor_rect(14, 4.4, 2, 1.2, "darkplanks", stroke=False); m.floor_rect(14, 16.9, 2, 1.2, "darkplanks", stroke=False)
    m.g("props", 7.5, 4.8, pr.scroll_rack(300, 46)); m.g("props", 22.5, 4.8, pr.lectern())
    m.g("props", 22.5, 16.5, pr.scales(), scale=1.4); m.g("props", 7.5, 16.5, pr.writ_frame())
    for k, (x, y) in enumerate(((5, 7), (10, 7), (20, 18.5))):
        m.token(["masked-champion-living", "masked-champion-construct", "masked-champion-memory"][k], x, y, hidden=True)
    marker(m, 7.5, 6.5, "Chamber 1: Name (the written roster)")
    marker(m, 22.5, 6.5, "Chamber 2: Witness (two accounts)")
    marker(m, 22.5, 18, "Chamber 3: Consideration (who benefited)")
    marker(m, 7.5, 18, "Chamber 4: Remedy (who would suffer)")
    return m


@register
def citadel():
    """Session 12: The Hall of Registrants and the practice floor of the Brass Citadel."""
    m = Map("citadel", "The Hall of Registrants", 34, 26, seed=29, bg="#1a1012")
    hell_env(m, 0.2)
    m.fill_all("darkcobble")
    m.floor_rect(2, 2, 18, 22, "brass")
    m.room(2, 2, 18, 22, "brass", doors=[("S", 8, 2, "brass"), ("E", 16, 2, "brass")])
    m.g("decal", 11, 13, pr.rug(500, 1500), shadow=False)
    # claims desks
    for i, x in enumerate((5, 11, 17)):
        m.g("props", x, 5, pr.desk(260, 110)); m.g("props", x, 4, pr.chair(), rot=180)
        m.g("props", x, 6.6, pr.rect(200, 30, "#8e1424", 4, 3), shadow=False)
    m.text(11, 3.1, "CLAIMS - ONE CLAIMANT PER DESK (by circular)", size=30, color="#ffd27a")
    m.g("props", 4, 12, pr.scroll_rack(240, 46), rot=90); m.g("props", 18, 12, pr.scroll_rack(240, 46), rot=90)
    m.g("props", 11, 9, pr.clock_face(150, (11, 59), False))
    for y in (11, 15, 19):
        m.g("props", 7, y, pr.pillar(40)); m.g("props", 15, y, pr.pillar(40))
    # the practice floor
    m.floor_circle(27, 13, 6, "arenastone")
    m.wall(arc_pts(27, 13, 6.4, 0, 360, 15), "brass")
    m.door(20.6, 12.2, 20.6, 13.8, "brass") if False else None
    m.g("decal", 27, 13, f'<circle r="160" fill="none" stroke="#d8aa52" stroke-width="12"/><circle r="40" fill="#d8aa52"/>', shadow=False)
    for a in (45, 135, 225, 315):
        m.g("props", 27 + 3.8 * math.cos(math.radians(a)), 13 + 3.8 * math.sin(math.radians(a)), p2.brazier(30))
        m.light(27 + 3.8 * math.cos(math.radians(a)), 13 + 3.8 * math.sin(math.radians(a)), 6, 2, color="#ff9a3a", alpha=0.3, anim="torch")
    m.g("props", 27, 18, p2.witness_stand())
    for (x, sh, col) in ((23, "crown", "#8e1424"), (31, "gear", "#6a5a2a"), (23.5, "wing", "#3a3a6a"), (30.5, "thorn", "#3a1a3a")):
        m.g("props", x, 4 if x in (23, 31) else 22, p2.banner_stand(col, "#d8aa52", sh))
    m.token("claims-clerk", 11, 4.1); m.token("vexa-corven", 27, 11, hidden=True)
    marker(m, 11, 5, "Session 12: The claims desk (Hollis's circular)")
    marker(m, 27, 13, "The practice floor (3-round showcase)")
    return m


@register
def iron_quarter():
    """Session 13: The Golemancer's War. Janella's workshop and two command pylons."""
    m = Map("iron-quarter", "The Iron Quarter", 36, 26, seed=30, bg="#1a1416")
    hell_env(m, 0.3)
    m.fill_all("factory") if True else None
    ground_mottle(m, 40, 30, cols=("#000000", "#3a2a22"))
    # workshop
    m.floor_rect(12, 8, 12, 10, "darkplanks")
    m.room(12, 8, 12, 10, "iron", doors=[("N", 5, 2, "iron"), ("S", 5, 2, "iron"), ("W", 4, 2, "iron"), ("E", 4, 2, "iron")])
    m.g("props", 15, 10.5, p2.workbench(260, 100, 5)); m.g("props", 21, 10.5, p2.workbench(260, 100, 6))
    m.g("props", 18, 15, p2.forge(100)); m.light(18, 15, 7, 3, color="#ff8a3a", alpha=0.45, anim="torch")
    m.g("props", 14, 16, p2.anvil()); m.g("props", 22.4, 16, p2.golem_parts(4))
    m.g("props", 18, 9, pr.ledger_book(180, 120))
    # entry corridors and construct yards
    for (x, y) in ((4, 4), (32, 4), (4, 22), (32, 22)):
        m.g("props", x, y, pr.gear(110, 12))
    m.g("props", 30, 13, p2.iron_golem_slumped(0.8)); m.g("props", 6, 13, p2.iron_golem_slumped(0.8))
    m.g("props", 18, 22, pr.conveyor(1200, 90, 6, 3)); m.g("props", 18, 3.5, pr.machine(300, 160, 2))
    # two command pylons
    for (x, y) in ((8, 6), (28, 20)):
        m.g("props", x, y, p2.pylon("#ff4a1a"), scale=1.5)
        m.light(x, y, 6, 2, color="#ff4a1a", alpha=0.5, anim="pulse")
    # civilians shelter
    m.g("props", 13.5, 13, pr.crate(70)); m.g("props", 14.4, 13.6, pr.barrel(30))
    m.token("janella-greenbottle", 18, 12, hidden=False)
    m.token("iron-warder-damaged", 30, 13, hidden=True); m.token("ash-scrap-golem", 6, 13, hidden=True)
    m.token("writ-bailiff", 18, 1.5, hidden=True); m.token("writ-bailiff", 18, 24.5, hidden=True)
    marker(m, 8, 6, "Command pylon A (AC 16, 30 HP / DC 17)")
    marker(m, 28, 20, "Command pylon B (AC 16, 30 HP / DC 17)")
    marker(m, 18, 9, "Hollis's authorization parchment")
    return m


@register
def audience():
    """Session 16: Misty's audience chamber of hanging iron roses."""
    m = Map("audience", "The Chamber of Iron Roses", 28, 24, seed=31, bg="#140a0e")
    hell_env(m, 0.45)
    m.fill_all("hellroof")
    oc = (14, 12)
    R = 11 / math.cos(math.radians(22.5))
    octo = [(oc[0] + R * math.cos(math.radians(22.5 + 45 * i)), oc[1] + R * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    m.floor_poly(octo, "marble")
    for i in range(8):
        if i == 1:
            a, b = octo[1], octo[2]
            m.wall([a, ((a[0] + b[0]) / 2 + 1.2, a[1])], "keep"); m.wall([((a[0] + b[0]) / 2 - 1.2, a[1]), b], "keep")
            m.door((a[0] + b[0]) / 2 + 1.2, a[1], (a[0] + b[0]) / 2 - 1.2, a[1], "red")
            continue
        m.wall([octo[i], octo[(i + 1) % 8]], "keep")
    m.g("decal", 14, 14, pr.rug(300, 1300, "#3a0a14", "#c09040"), shadow=False)
    m.g("props", 14, 3.6, pr.throne(240, 200))
    m.g("decal", 14, 6.4, p2.magic_circle(200, "#a0183a", 7, inverted=True), shadow=False)
    q = random.Random(31)
    for i in range(16):
        a = i * 2 * math.pi / 16
        x, y = 14 + math.cos(a) * 7.5, 12 + math.sin(a) * 7.5
        m.g("high", x, y, p2.iron_rose(48 + q.uniform(0, 20), i))
    for (x, y) in ((9, 8), (19, 8), (9, 17), (19, 17)):
        m.g("props", x, y, p2.mirror(130), rot=q.choice([0, 90, 45]))
    m.light(14, 4, 10, 4, color="#ff3a5a", alpha=0.4, anim="pulse")
    m.light(14, 12, 14, 4, color="#8a2a4a", alpha=0.3)
    m.token("misty", 14, 4.4)
    m.token("mother-sable", 11.5, 5.5); m.token("isolde", 16.5, 5.5)
    marker(m, 14, 4.4, "Misty's offer: the Perpetual First Refusal Writ")
    return m


@register
def reliquary():
    """Session 18-19: The Thorn Reliquary. 90 ft square, dais, two bridges, iron roses, Heartstone behind a prismatic screen."""
    m = Map("reliquary", "The Thorn Reliquary", 26, 26, seed=32, bg="#0e080c")
    hell_env(m, 0.5)
    m.fill_all("hellroof")
    # 90 ft chamber = 18 squares, centred
    X0, Y0 = 4, 4
    m.floor_rect(X0, Y0, 18, 18, "manortile")
    m.room(X0, Y0, 18, 18, "keep", doors=[("S", 8, 2, "red")])
    # chasm under the bridges
    m.floor_rect(X0 + 1, Y0 + 7, 16, 4, "lava", stroke=True)
    m.light(13, 13, 12, 4, color="#ff4a1a", alpha=0.35, anim="fire", walls=False)
    for bx in (X0 + 4, X0 + 14):
        m.floor_rect(bx - 0.8, Y0 + 6.6, 1.6, 4.8, "darkplanks")
        m.g("props", bx, Y0 + 9, pr.railing(460, vertical=True).replace('x1="0"', 'x1="-80"') if False else "", shadow=False)
        m.add("props", f'<line x1="{(bx-0.85)*100:.0f}" y1="{(Y0+6.6)*100:.0f}" x2="{(bx-0.85)*100:.0f}" y2="{(Y0+11.4)*100:.0f}" stroke="#2a2830" stroke-width="10"/>'
                       f'<line x1="{(bx+0.85)*100:.0f}" y1="{(Y0+6.6)*100:.0f}" x2="{(bx+0.85)*100:.0f}" y2="{(Y0+11.4)*100:.0f}" stroke="#2a2830" stroke-width="10"/>')
    # sleeping dais (north)
    m.g("props", 13, Y0 + 3.4, p2.sleeping_dais(360, 240))
    m.light(13, Y0 + 3.4, 6, 2, color="#c04a6a", alpha=0.35, anim="pulse")
    # four hanging iron roses (block sight)
    for (x, y) in ((X0 + 4, Y0 + 4), (X0 + 14, Y0 + 4), (X0 + 4, Y0 + 14), (X0 + 14, Y0 + 14)):
        m.g("high", x, y, p2.iron_rose(70, int(x * 10 + y)), scale=1.4)
        m.wall([(x - 0.6, y - 0.6), (x + 0.6, y - 0.6), (x + 0.6, y + 0.6), (x - 0.6, y + 0.6)], "dark", closed=True, draw=False, sight="normal")
    # Heartstone behind a prismatic screen (east alcove)
    m.g("props", X0 + 16, Y0 + 15.5, p2.heartstone(60))
    m.g("high", X0 + 14.7, Y0 + 15.5, p2.prism_screen(320, horiz=False), shadow=False)
    m.invisible_wall([(X0 + 14.7, Y0 + 13.8), (X0 + 14.7, Y0 + 17.2)])
    m.light(X0 + 16, Y0 + 15.5, 6, 2, color="#ff3a5a", alpha=0.5, anim="pulse")
    # soul siphon and the mosaic by the entrance
    m.g("decal", 13, Y0 + 15.8, p2.soul_mosaic(140), shadow=False)
    m.g("props", X0 + 2.4, Y0 + 15.5, p2.pylon("#a88aff"), scale=1.5)
    m.light(X0 + 2.4, Y0 + 15.5, 6, 2, color="#a88aff", alpha=0.45, anim="pulse")
    m.token("night-hag-advocate", 13, Y0 + 12.5, hidden=True); m.token("writ-bailiff", 9, Y0 + 13, hidden=True); m.token("writ-bailiff", 17, Y0 + 13, hidden=True)
    marker(m, 13, Y0 + 3.4, "The Queen's resting place (Phase 2)")
    marker(m, X0 + 16, Y0 + 15.5, "The Heartstone (AC 20, 70 HP, threshold 10)")
    marker(m, X0 + 2.4, Y0 + 15.5, "The Soul Siphon (DC 19 Arcana / AC 18, 45 HP)")
    marker(m, 13, Y0 + 15.8, "The trapped soul mosaic")
    return m


# ======================================================================= EXTRA LOCATIONS (2026 additions)
def rot_rect(cx, cy, w, h, ang):
    a = math.radians(ang)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]


def broken_ring(m, cx, cy, r, seed, gaps=((40, 70), (200, 230)), w=60):
    q = random.Random(seed)
    a = 0
    while a < 360:
        if any(g0 <= a < g1 for g0, g1 in gaps):
            a += 10
            continue
        a1 = a + 30
        pts = [(cx + r * math.cos(math.radians(t)), cy + r * math.sin(math.radians(t))) for t in range(a, a1 + 1, 10)]
        ruin(m, pts, seed=seed + a, wall=False) if w > 70 else m.g("walls", 0, 0, p2.ruin_blocks([(x * 100, y * 100) for x, y in pts], seed=seed + a, w=w, seg=70))
        a = a1


@register
def breach():
    """The Breach: a mortal graveyard meadow where Avernus is bleeding through, ringed by a crystal-lava portal."""
    m = Map("breach", "The Breach at Hollow Barrow", 40, 30, seed=41, bg="#2a3a1a")
    hell_env(m, 0.1)
    m.fill_all("grass")
    ground_mottle(m, 60, 41, cols=("#2a3a1a", "#8a9a5a", "#3a2a1a"))
    hellzone = [(-1, 17), (4, 15.5), (9, 13), (13, 11.6), (18, 11.2), (24, 12.4), (28, 15), (32, 18), (36, 21.5), (41, 24.5), (41, 31), (-1, 31)]
    m.floor_poly(hellzone, "redsand", stroke=False)
    d = "M" + " L".join(f"{x*100:.0f} {y*100:.0f}" for x, y in densify(hellzone[:10], 0.6))
    m.add("floor", f'<path d="{d}" fill="none" stroke="#3a1a10" stroke-width="80" opacity="0.45" filter="url(#blur4)"/>')
    q = random.Random(41)
    for _ in range(30):  # glowing cracks in the hell ground
        x, y = q.uniform(2, 39), q.uniform(16, 29.5)
        if y < 11 + (x - 18) ** 2 / 60 + 3:
            continue
        m.add("decal", f'<path d="M{x*100:.0f} {y*100:.0f} l{q.uniform(-80,80):.0f} {q.uniform(-60,60):.0f} l{q.uniform(-60,60):.0f} {q.uniform(-60,60):.0f}" stroke="#ffb43a" stroke-width="6" fill="none" opacity="0.8"/>')
    # graveyard (top-left)
    for i in range(34):
        x, y = 2.5 + q.uniform(0, 9) , 1 + q.uniform(0, 8)
        if x + y * 0.6 > 13:
            continue
        m.g("props", x, y, p2.headstone(q.uniform(40, 56), q.randint(0, 1)), rot=q.uniform(-30, 30) - 30)
    for (x, y, r) in ((11.6, 1.3, 30), (14.2, 1.1, 30), (13.6, 3.1, 30), (1, 6.8, 0), (2, 9.6, 0)):
        m.g("props", x, y, p2.tomb_slab(130, 90), rot=r)
    # stone circle (top centre)
    broken_ring(m, 27.5, 4.6, 3.6, 7, gaps=((100, 130), (300, 320)), w=55)
    broken_ring(m, 27.5, 4.6, 2.4, 8, gaps=((20, 60), (180, 230)), w=45)
    m.g("lowprop", 25.2, 3.5, p2.debris(6, 80, 3), shadow=False); m.g("lowprop", 30.2, 8, p2.debris(6, 80, 4), shadow=False)
    # ruined wall running to the trees (top right)
    ruin(m, [(33.5, 3.6), (35, 5), (37.2, 8.6), (38.6, 11.5), (38.4, 14.5)], seed=9)
    # trees
    m.g("high", 1, 0.8, p2.tree(170, 1)); m.g("high", 37.3, 5.3, p2.tree(240, 2)); m.g("high", 38.4, 28.6, p2.tree(210, 3))
    m.g("high", 41.5, 22, p2.tree(160, 5))
    for (x, y) in ((14.8, 9.4), (1.8, 18), (33.5, 12.5), (38.8, 16.6), (31, 10.4)):
        m.g("props", x, y, f'<g>{"".join(f"<path d=\'M0 0 l{math.cos(t)*70:.0f} {math.sin(t)*70:.0f}\' stroke=\'#2a4a1a\' stroke-width=\'9\' stroke-linecap=\'round\'/>" for t in [i*0.5 for i in range(13)])}</g>', shadow=False)
    # the carved face and its hands
    m.g("props", 20.2, 15.6, p2.face_rock(150), rot=-60)
    m.g("props", 16.2, 17.3, '<rect x="-40" y="-90" width="80" height="140" rx="40" fill="#d8d8dc" stroke="#150b0b" stroke-width="5"/>', rot=-20)
    m.g("props", 15, 18.4, '<rect x="-30" y="-70" width="60" height="110" rx="30" fill="#d8d8dc" stroke="#150b0b" stroke-width="5"/>', rot=60)
    m.g("props", 16.8, 18.4, '<rect x="-60" y="-30" width="140" height="60" rx="30" fill="#d8d8dc" stroke="#150b0b" stroke-width="5"/>', rot=-25)
    # the angled temple ruin
    outer = rot_rect(27.6, 18.6, 15.2, 7.6, 35)
    inner = rot_rect(27.6, 18.6, 11.4, 4.4, 35)
    m.floor_poly(outer, "cavefloor")
    ruin(m, [outer[0], outer[1], outer[2]], seed=31, wall=True)
    ruin(m, [outer[2], outer[3], ((outer[3][0] + outer[0][0]) / 2, (outer[3][1] + outer[0][1]) / 2)], seed=32)
    ruin(m, [inner[3], inner[0], inner[1], ((inner[1][0] + inner[2][0]) / 2, (inner[1][1] + inner[2][1]) / 2)], seed=33)
    ruin(m, [((inner[2][0] + inner[3][0]) / 2, (inner[2][1] + inner[3][1]) / 2), inner[3]], seed=34)
    m.g("props", 25.4, 15.9, pr.rect(80, 80, "#5a5a62", 4, 5) + '<rect x="-28" y="-28" width="56" height="56" fill="#3a3a42"/>')
    m.g("lowprop", 26.4, 16.6, p2.skeleton(4), shadow=False, scale=1.4)
    m.g("props", 28.6, 18.6, p2.stairs(110, 260, 5), rot=35)
    # broken cottages (bottom left)
    for pts, sd in (([(0, 19), (3.6, 19), (3.6, 22)], 50), ([(1.4, 21.5), (1.4, 26), (3.6, 26), (3.6, 23.5)], 51),
                    ([(5.8, 18.6), (5.8, 21), (7.8, 21)], 52), ([(7.8, 18.8), (7.8, 25.8), (4.8, 25.8), (4.8, 24)], 53)):
        m.g("walls", 0, 0, p2.ruin_blocks([(x * 100, y * 100) for x, y in pts], seed=sd, w=55, seg=70))
        m.wall(pts, "ruin", draw=False)
    m.g("lowprop", 3.2, 20.6, p2.debris(6, 70, 5), shadow=False)
    # the lava-and-crystal portal ring
    ring = [(17.4 + 8.4 * math.cos(math.radians(t)), 30.5 + 8.4 * math.sin(math.radians(t))) for t in range(180, 361, 6)]
    d = "M" + " L".join(f"{x*100:.0f} {y*100:.0f}" for x, y in ring)
    m.add("floor", f'<path d="{d}" fill="none" stroke="#ff6a0a" stroke-width="420" opacity="0.5" filter="url(#glow)"/>'
                   f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="330"/><path d="{d}" fill="none" stroke="url(#pt-lava)" stroke-width="310"/>')
    m.pattern("lava")
    for i, (x, y) in enumerate(ring[::2]):
        m.g("props", x, y, p2.crystal_mass(220, i), rot=math.degrees(math.atan2(y - 30.5, x - 17.4)) + 90)
    m.floor_circle(17.4, 31, 5.6, "grass")
    for (x, y, r) in ((15.2, 29.4, 140), (18.6, 28.6, 160), (20.4, 30.6, 130), (16.4, 31.6, 150)):
        m.g("high", x, y, p2.tree(r, int(x * 3), "autumn"))
    m.light(17.4, 30.5, 16, 7, color="#ff7a2a", alpha=0.45, anim="fire", walls=False)
    m.light(17.4, 30, 6, 3, color="#ffd27a", alpha=0.3, anim="pulse")
    for i in range(40):
        m.g("lowprop", q.uniform(1, 39), q.uniform(0.5, 29.5), p2.embers(q.randint(1, 3), i), shadow=False)
    scatter(m, (0.3, 9, 39.7, 29.7), 30, ["rock", "pebbles", "bones"], seed=41,
            avoid=[(27.6, 18.6, 8.5), (17.4, 30.5, 10), (4, 22, 4.5), (17.5, 16.5, 3)])
    m.token("ash-scrap-golem", 26, 22, hidden=True)
    marker(m, 6, 4, "The barrow graves")
    marker(m, 27.5, 4.6, "The old stone circle")
    marker(m, 20, 15.6, "The fallen face")
    marker(m, 27.6, 18.6, "The broken chapel")
    marker(m, 17.4, 27, "The crystal portal (way to Avernus)")
    return m


@register
def greyhurst_district():
    """Greyhurst street-level: every house opened up, the burning wreck and the dead dragon."""
    m = Map("greyhurst-district", "Greyhurst: The Burgher's Row", 40, 30, seed=42, bg="#1a1416")
    hell_env(m, 0.3)
    m.fill_all("darkcobble"); ground_mottle(m, 70, 42, cols=("#000000", "#3a2a22", "#1a1418"))
    lava_patch(m, [(-1, -1), (29.5, -1), (28.8, 0.6), (26, 1.2), (24, 1.6), (17, 1.8), (16, 3.2), (15, 2), (8, 3.2), (4, 3.6), (-1, 3.4)], 21)
    lava_patch(m, [(39.2, -1), (41, -1), (41, 31), (39.4, 31), (39.7, 20), (39.2, 8)], 22)
    lava_patch(m, [(27.4, 7.2), (28.6, 7), (29.6, 9.5), (30, 12.5), (29.3, 15), (28.4, 14.6), (27.6, 12), (27.2, 9.5)], 23)
    m.g("props", 4.5, 1.6, p2.wrecked_ship(760, 260), rot=40)
    m.light(4.5, 1.6, 9, 4, color="#ffb43a", alpha=0.5, anim="fire")
    m.g("props", 27.6, 2.6, p2.dragon_corpse(0.8), rot=-20)
    q = random.Random(42)

    def furnish(x0, y0, x1, y1, n, seed):
        r = random.Random(seed)
        for _ in range(n):
            x, y = r.uniform(x0 + 0.8, x1 - 0.8), r.uniform(y0 + 0.8, y1 - 0.8)
            k = r.choice(["rug", "bed", "debris", "barrel", "table", "chair", "glass"])
            if k == "rug":
                m.g("decal", x, y, pr.rug(r.choice([140, 180]), 240, r.choice(["#2a7a8a", "#a84a3a", "#3a3a8a"]), "#d8aa52"), rot=r.uniform(-30, 30), shadow=False)
            elif k == "bed":
                m.g("props", x, y, p2.bed(110, 170, r.choice(["#2a8a7a", "#5a2a9a", "#9a2a2a"])), rot=r.uniform(-20, 20))
            elif k == "debris":
                m.g("lowprop", x, y, p2.debris(4, 50, r.randint(0, 99)), shadow=False)
            elif k == "barrel":
                m.g("props", x, y, pr.barrel(32))
            elif k == "table":
                m.g("props", x, y, pr.table(120, 70), rot=r.uniform(-40, 40))
            elif k == "chair":
                m.g("props", x, y, pr.chair(), rot=r.uniform(0, 360))
            else:
                for _ in range(4):
                    m.g("lowprop", x + r.uniform(-0.4, 0.4), y + r.uniform(-0.4, 0.4), '<polygon points="0,-10 8,4 -6,8" fill="#5ad0c8" stroke="#150b0b" stroke-width="2"/>', shadow=False)

    # house A (left) with its partitions
    house(m, 1.4, 6.3, 8.1, 12.3, doors=[("S", 3.5, 1.2, "wood")])
    for seg in ([(4.8, 6.3), (4.8, 9.6)], [(4.8, 9.6), (6.2, 9.6)], [(3.4, 12), (5.2, 12), (6, 11.2)], [(4, 12), (4, 16)], [(1.4, 16.2), (5.3, 16.2)], [(6.8, 13), (7.6, 15.6), (9.5, 15.6)]):
        m.wall(seg, "timber")
    m.floor_rect(1.6, 16.4, 2.4, 2, "planks", stroke=False)
    furnish(1.4, 6.3, 9.5, 18.6, 12, 1)
    # house B (centre) with octagonal room
    house(m, 11.5, 5.9, 8, 12.4, doors=[("S", 6, 1.2, "wood")])
    for seg in ([(13.8, 5.9), (13.8, 9.3)], [(11.5, 10.9), (14, 10.9)], [(15.6, 10.9), (19.5, 10.9)], [(14, 10.9), (14.4, 13.4)], [(15.6, 11), (15.6, 14)],
                [(16.8, 12), (17.6, 15.2), (19.5, 15.2)], [(14.6, 14.4), (15.4, 18.3)]):
        m.wall(seg, "timber")
    m.room(19.5, 7.5, 3.6, 3.3, "dark", gaps=[("W", 0.4, 2.4)])
    m.floor_rect(19.5, 7.5, 3.6, 3.3, "darkplanks")
    m.g("props", 21.4, 8.4, p2.bed(100, 170, "#2a8a8a"), rot=-75); m.g("props", 21.6, 9.8, p2.bed(100, 170, "#2a8a8a"), rot=-75)
    m.g("props", 12.4, 7.6, pr.barrel(40)); m.g("props", 12.4, 17, pr.barrel(40), rot=90)
    furnish(11.5, 5.9, 19.5, 18.3, 9, 2)
    # house C (centre right)
    house(m, 20.2, 11.6, 6.8, 6.4, doors=[("E", 4.6, 1.2, "wood")])
    m.wall([(23.6, 11.6), (23.6, 14.6), (26.8, 14.6), (26.8, 11.6)], "timber")
    m.g("props", 21.6, 13, p2.bed(100, 170, "#3a2a9a"), rot=-30)
    m.g("props", 25.9, 12.8, p2.debris(4, 40, 3), shadow=False)
    furnish(20.2, 11.6, 27, 18, 4, 3)
    # top-right house with the apse (boss)
    house(m, 31.7, 0.6, 6, 6.2, doors=[("S", 2.4, 1.2, "iron")])
    m.floor_circle(37.7, 3.7, 1.7, "darkplanks")
    m.wall(arc_pts(37.7, 3.7, 1.7, -90, 90, 15), "dark")
    m.g("props", 37, 3.6, '<rect x="-60" y="-90" width="120" height="180" rx="20" fill="#5a1a22" stroke="#150b0b" stroke-width="6"/><circle r="40" fill="#8a2a32"/>')
    m.g("decal", 37.4, 3.7, p2.magic_circle(120, "#e0283a", 5), shadow=False)
    m.light(37.4, 3.7, 7, 3, color="#ff2a3a", alpha=0.4, anim="pulse")
    m.g("props", 36.4, 5.6, p2.stairs(160, 120, 4, vertical=False))
    m.g("props", 34.7, 1.5, pr.chair()); furnish(31.7, 0.6, 36.6, 6.8, 3, 4)
    # the right-hand row
    for i, (y0, y1) in enumerate(((9, 15.2), (15.6, 21.8), (23, 29.3))):
        house(m, 32.3, y0, 6.8, y1 - y0, tex="darkplanks", style="timber", doors=[("W", 1, 1.2, "wood")])
        m.wall([(32.3, y0 + 3.6), (35.5, y0 + 3.6), (35.5, y1 - 0.6)], "timber")
        m.g("props", 34, y0 + 4.6, p2.bed(130, 180, ["#2a8a7a", "#2a8a7a", "#e8dcc0"][i]), rot=-15)
        furnish(32.3, y0, 39.1, y1, 5, 10 + i)
    m.g("props", 38, 18.2, p2.stairs(110, 260, 6), shadow=False)
    # the bottom rows of cells (stone)
    for x0 in (1, 5.2, 9.3, 17.6, 21.7, 25.9):
        m.floor_rect(x0, 22.5, 4.1, 6.4, "darkplanks")
        m.room(x0, 22.5, 4.1, 6.4, "dark", gaps=[("N", 1, 1.6)])
        furnish(x0, 22.5, x0 + 4.1, 28.9, 4, int(x0 * 7))
    for (x, y) in ((10.6, 20.2), (16, 4.4), (25.5, 4.5), (31, 19.6)):
        m.g("props", x, y, p2.brazier(28)); m.light(x, y, 7, 2, color="#ff9a3a", alpha=0.35, anim="torch")
    scatter(m, (0.3, 3.5, 39, 29.7), 40, ["bones", "debris", "pebbles"], seed=42,
            rects=[((1.2, 5.6), (27.2, 18.6)), ((31.5, 0.4), (40, 30)), ((0.8, 22.2), (30.2, 29.2))], avoid=[(28.5, 11, 2.5)])
    m.token("cadaver-collector", 14, 20.3, hidden=True); m.token("cadaver-collector", 15.6, 20.3, hidden=True); m.token("brass-registrar", 14.8, 21, hidden=True)
    marker(m, 4.5, 1.6, "The burning wreck")
    marker(m, 27.6, 2.6, "The dead wyrm")
    marker(m, 5, 9, "The burgher's house")
    marker(m, 15, 9, "The town hall annex")
    marker(m, 37.4, 3.7, "The ritual apse")
    marker(m, 14.8, 20.5, "3D: The false mayor's guard")
    return m


@register
def ashen_caverns():
    """The Ashen Caverns: a lava-veined cavern beneath the Citadel road, with two burning vents."""
    m = Map("ashen-caverns", "The Ashen Caverns", 40, 30, seed=43, bg="#1a1420")
    hell_env(m, 0.45)
    # dark purple rock everywhere, the cave floor carved out of it
    m.fill_all("cavefloor")
    m.add("floor", '<rect width="4000" height="3000" fill="#2a2236" opacity="0.85"/>')
    cave = [(0, 9.5), (2.2, 9.3), (3.6, 6.4), (5.2, 4.8), (6.8, 2.2), (9.8, 1.6), (12.4, 0.6), (14, 1.2), (15.4, 2.6), (17, 1.8), (21, 1.2),
            (22.8, 0.4), (27, 0.6), (31, 0.8), (32.6, 0.3), (36.4, 0.4), (37.8, 1.6), (38.2, 4), (40, 4.6), (40, 6.4), (38.6, 7.4), (38.8, 11),
            (37.8, 15), (38.2, 20), (37.6, 25), (34.8, 26.6), (30.4, 26.4), (26, 24.8), (22.8, 24.2), (18.4, 24.6), (12.6, 26.4), (11.4, 30),
            (5, 30), (5.2, 28), (8.4, 26.6), (9.8, 24.4), (7.2, 22.2), (3.6, 20.8), (0, 22.2), (0, 14.4), (2.4, 13.6), (3.6, 11.6), (0, 11.4)]
    pillar = [(30.8, 11.4), (32.4, 10.2), (34, 10.4), (34.6, 12.8), (34.6, 18), (35, 21.6), (34.2, 23.4), (31.4, 23.2), (30.6, 21), (30.4, 16), (30.2, 13)]
    from hellkit import _offset
    m.floor_poly(cave, "cavefloor")
    m.add("floor", f'<polygon points="{" ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in cave)}" fill="#6a4a40" opacity="0.35"/>')
    d = "M" + " L".join(f"{x*100:.0f} {y*100:.0f}" for x, y in cave) + " Z"
    m.add("floor", f'<path d="{d}" fill="none" stroke="#a88a86" stroke-width="70" opacity="0.5"/><path d="{d}" fill="none" stroke="{INK}" stroke-width="12"/>')
    pl = " ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in pillar)
    m.add("floor", f'<polygon points="{pl}" fill="#1e1828" stroke="#a88a86" stroke-width="70" stroke-opacity="0.5"/><polygon points="{pl}" fill="none" stroke="{INK}" stroke-width="12"/>')
    m.terrain_wall(cave, closed=True) if False else m.wall(cave + [cave[0]], "dark", draw=False)
    m.wall(pillar + [pillar[0]], "dark", draw=False)
    q = random.Random(43)
    for _ in range(70):  # purple boulders in the rock mass
        x, y = q.uniform(0, 40), q.uniform(0, 30)
        m.g("lowprop", x, y, p2.rock(q.uniform(40, 110), q.randint(0, 999), fill=q.choice(["#4a3e5a", "#3e3450", "#56486a"]), light="#7a6a8e"))
    m.add("lowprop", f'<polygon points="{" ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in cave)}" fill="none"/>')
    # re-draw the cave floor above the boulders
    m.floor_poly(cave, "cavefloor", layer="lowprop")
    m.add("lowprop", f'<polygon points="{" ".join(f"{x*100:.0f},{y*100:.0f}" for x, y in cave)}" fill="#6a4a40" opacity="0.35"/><path d="{d}" fill="none" stroke="#a88a86" stroke-width="70" opacity="0.5"/><path d="{d}" fill="none" stroke="{INK}" stroke-width="12"/>')
    m.add("lowprop", f'<polygon points="{pl}" fill="#1e1828" stroke="#a88a86" stroke-width="70" stroke-opacity="0.5"/><polygon points="{pl}" fill="none" stroke="{INK}" stroke-width="12"/>')
    # the lava vein
    flow = [(9, 6.5), (13, 7.6), (15.6, 9.6), (17.6, 12.6), (19.4, 15.6), (21.4, 18.6), (23, 21.4), (25.6, 19), (28, 17.4), (29.6, 15), (30.2, 13.8)]
    c = densify(flow, 0.4)
    widths = [3.2 if i < len(c) * 0.25 else (1.6 if i < len(c) * 0.7 else 0.9) for i in range(len(c))]
    for (x, y), w in zip(c, widths):
        m.add("lowprop", f'<circle cx="{x*100:.0f}" cy="{y*100:.0f}" r="{w*60:.0f}" fill="#ff5a0a" opacity="0.18" filter="url(#glow)"/>')
    for (x, y), w in zip(c, widths):
        m.add("lowprop", f'<circle cx="{x*100:.0f}" cy="{y*100:.0f}" r="{w*45:.0f}" fill="url(#pt-lava)"/>')
    m.pattern("lava")
    for i in range(0, len(c), 6):
        m.light(c[i][0], c[i][1], 8, 3, color="#ff6a1a", alpha=0.5, anim="fire", walls=False)
    # glowing cracks
    for (x0, y0, pts) in ((5, 5.5, [(2, 1), (1, 3), (-1, 2), (0, 4)]), (17, 15, [(-3, 4), (-2, 2), (-4, 3)]), (19.6, 18, [(1.6, 2.5), (0.6, 1.4)]), (24, 19, [(1.4, 1), (2, 2)])):
        dd = f"M{x0*100:.0f} {y0*100:.0f} " + " ".join(f"l{dx*100:.0f} {dy*100:.0f}" for dx, dy in pts)
        m.add("lowprop", f'<path d="{dd}" stroke="#ffb43a" stroke-width="16" fill="none" stroke-linecap="round" opacity="0.9"/>')
    # the two burning vents
    for (x, y) in ((33.6, 5.6), (35.6, 7.6)):
        m.g("lowprop", x, y, f'<circle r="70" fill="#000" opacity="0.6"/><circle r="40" fill="#2a0a06" stroke="#150b0b" stroke-width="5"/><circle r="22" fill="#ff7a1a"/><circle r="10" fill="#ffe27a"/>', shadow=False)
        m.light(x, y, 6, 2, color="#ff6a1a", alpha=0.5, anim="fire")
    scatter(m, (2, 1.5, 37, 25), 50, ["pebbles", "darkrock", "bones"], seed=43, lines=[(flow, 2)], avoid=[(32.5, 16.5, 4)])
    m.token("ash-scrap-golem", 33, 25, hidden=True)
    marker(m, 13, 8, "The lava pool")
    marker(m, 34.6, 6.6, "The burning vents")
    marker(m, 1, 10.5, "West passage")
    marker(m, 8, 29, "South passage")
    return m


@register
def claw_rift():
    """The Claw Rift: a scrolling chase strip between two mirrored jaws of crimson claws.
    Mirror-symmetric top to bottom and seamless left to right (period 10 squares), so it can loop."""
    m = Map("claw-rift", "The Claw Rift (scrolling)", 40, 30, seed=44, bg="#2a1a18")
    hell_env(m, 0.3)
    m.vignette = False
    m.fill_all("cavefloor")
    m.add("floor", '<rect width="4000" height="3000" fill="#6a3a2a" opacity="0.25"/>')
    q = random.Random(44)
    # seamless mottle: each blotch is drawn at x and x +/- 40
    for _ in range(50):
        x, y = q.uniform(0, 40), q.uniform(5, 25)
        rx, ry, col, op = q.uniform(80, 300), q.uniform(60, 200), q.choice(["#1a0e0c", "#6a4a3a", "#3a2a2a"]), q.uniform(0.08, 0.18)
        for ox in (-40, 0, 40):
            m.add("floor", f'<ellipse cx="{(x+ox)*100:.0f}" cy="{y*100:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" opacity="{op:.2f}" filter="url(#blur4)"/>')
    # mirrored fire bands, full width so the edges match
    for y, sgn in ((0, 1), (30, -1)):
        m.add("floor", f'<rect x="-400" y="{y*100 - 300:.0f}" width="4800" height="600" fill="#ff6a0a" opacity="0.5" filter="url(#glow)"/>'
                       f'<rect x="-400" y="{y*100 - 120:.0f}" width="4800" height="240" fill="#ffd25a" opacity="0.55" filter="url(#glow)"/>')
        for x in range(0, 41, 8):
            m.light(x, y + sgn * 0.5, 12, 4, color="#ff6a1a", alpha=0.5, anim="fire", walls=False)
    # one 10-square module of claws, repeated 4x plus a wrap copy, mirrored top/bottom
    module = [(0, 2.0, 0.8, 0.3), (2.5, 1.3, 0.55, -0.4), (5, 2.6, 1.05, 0.0), (7.5, 1.3, 0.55, 0.4)]
    for base in range(0, 41, 10):
        for (dx, depth, size, curl) in module:
            x = base + dx
            if x > 40.01:
                continue
            for top in (True, False):
                y = depth if top else 30 - depth
                rot = 180 if top else 0
                c = curl if top else -curl
                m.g("props", x, y, p2.claw_spike(420 * size, 220 * size, int(dx * 10), c), rot=rot)
                if 0.5 < x < 39.5:
                    m.wall([(x - 0.7, y - 0.7), (x + 0.7, y - 0.7), (x + 0.7, y + 0.7), (x - 0.7, y + 0.7)], "dark", closed=True, draw=False)
        for top in (True, False):
            m.g("props", base + 3.75, 0.6 if top else 29.4, p2.crystal_mass(380, 7), rot=0 if top else 180)
    m.token("iron-heir", 20, 15, hidden=True)
    marker(m, 20, 15, "The killing ground (loops east-west)")
    marker(m, 2, 15, "Scroll seam: the left and right edges join")
    return m


def _vehicle(kind, scale=0.2, dark=False):
    import vehicles as V
    top = {"quad": V.top_quad("#c2410c"), "spiker": V.top_quad("#2a2226", True), "hauler": V.top_hauler(),
           "reclaimer": V.top_reclaimer()}[kind]
    f = '<g opacity="0.55" filter="url(#blur4)"><rect x="-600" y="-600" width="1200" height="1200" fill="#000" opacity="0"/></g>' if dark else ""
    tint = '<rect x="0" y="0" width="1000" height="1000" fill="#1a0e0c" opacity="0.55"/>' if dark else ""
    return f'<g transform="scale({scale}) translate(-500,-500)">{top}{tint}</g>' + f


@register
def souljack_yard():
    """The Souljack Yard: Greyhurst's ruined smithy yard, where the party restores war machines and finds soul coins."""
    m = Map("souljack-yard", "The Souljack Yard (Greyhurst)", 32, 24, seed=61, bg="#1a1416")
    hell_env(m, 0.3)
    m.fill_all("darkcobble"); ground_mottle(m, 50, 61, cols=("#000000", "#3a2a22", "#4a1a10"))
    # iron palisade with the road gate east
    m.wall([(0.5, 0.5), (31.5, 0.5), (31.5, 9)], "dark")
    m.wall([(31.5, 15), (31.5, 23.5), (0.5, 23.5), (0.5, 0.5)], "dark")
    m.g("props", 31.5, 12, p2.gate(560), rot=90)
    m.text(29.6, 12.2, "TO THE BLACKSPINE ROAD", size=30, color="#ffd27a", rot=90)
    m.floor_rect(22, 9, 9.5, 6, "ashsand", stroke=False)
    # Y1: Janella's lift (workshop shed, north-west)
    m.floor_rect(1, 1, 12, 9, "darkplanks")
    m.wall([(1, 1), (13, 1), (13, 6)], "timber"); m.wall([(13, 8.5), (13, 10), (1, 10), (1, 1)], "timber")
    m.door(13, 6, 13, 8.5, "wood")
    m.g("props", 7, 5.5, _vehicle("hauler", 0.42))
    m.g("props", 2.8, 2.8, p2.forge(90)); m.light(2.8, 2.8, 7, 2, color="#ff8a3a", alpha=0.45, anim="torch")
    m.g("props", 11, 2.6, p2.workbench(240, 90, 3)); m.g("props", 11, 8.8, p2.anvil())
    m.g("lowprop", 3, 8.4, p2.golem_parts(61), shadow=False)
    # Y2: the wreck field (south-west)
    q = random.Random(61)
    for (x, y, kind, rot) in ((3.5, 14, "quad", 30), (8, 16.5, "spiker", -60), (4, 20, "reclaimer", 95), (11.5, 20.5, "quad", 160),
                              (13, 14.5, "spiker", 15)):
        m.g("props", x, y, _vehicle(kind, 0.24 if kind != "reclaimer" else 0.36, dark=True), rot=rot)
    m.g("lowprop", 8, 19, p2.debris(10, 260, 7), shadow=False)
    for (x, y) in ((6, 13), (10, 18), (2.5, 17.5)):
        m.add("props", f'<circle cx="{x*100}" cy="{y*100}" r="16" fill="#5ad0e0" opacity="0.9"/><circle cx="{x*100}" cy="{y*100}" r="40" fill="#5ad0e0" opacity="0.35" filter="url(#glow)"/>')
        m.light(x, y, 2, 0.5, color="#5ad0e0", alpha=0.5, anim="pulse")
    # Y3: Broker Grisk's coin booth (centre)
    m.floor_rect(15, 2, 7, 6, "brass")
    m.g("props", 18.5, 4, p2.ledger_stall(300, 140, 2)); m.g("props", 16.5, 6.3, p2.gold_pile(70, 3))
    m.g("props", 20.6, 6.3, p2.hanging_chains(200, 3, 5))
    for i in range(7):
        x = 16.2 + i * 0.9
        m.add("props", f'<circle cx="{x*100:.0f}" cy="250" r="14" fill="#5ad0e0" stroke="{INK}" stroke-width="4"/>')
    m.light(18.5, 4, 6, 2, color="#5ad0e0", alpha=0.35, anim="pulse")
    m.text(18.5, 1.7, "LICENSED COIN BROKER · NINTH SORTING ANNEX", size=24, color="#ffd27a")
    # Y4: the fuel shed and ichor
    m.floor_rect(24, 1, 7, 6, "darkplanks")
    m.wall([(24, 1), (31, 1)], "timber"); m.wall([(24, 7), (24, 1)], "timber")
    m.g("props", 27.5, 3, p2.keg_rack(4)); m.g("props", 29.5, 5.5, p2.brazier(28))
    m.light(29.5, 5.5, 5, 1.5, color="#9aff5a", alpha=0.3, anim="torch")
    # Y5: the loan table and the parked quads (east)
    m.g("props", 18, 12, p2.long_table(300, 4, settings=False))
    for (x, y) in ((24.5, 17.5), (27, 17.5), (29.5, 17.5)):
        m.g("props", x, y, _vehicle("quad", 0.2), rot=0)
    for (x, y) in ((15, 1.5), (14.5, 22), (22, 22.5), (31, 8.5), (31, 15.5)):
        m.g("props", x, y, p2.brazier(26)); m.light(x, y, 6, 2, color="#ff9a3a", alpha=0.3, anim="torch")
    scatter(m, (0.8, 0.8, 31.2, 23.2), 45, ["bones", "debris", "pebbles"], seed=61,
            rects=[((1, 1), (13, 10)), ((15, 2), (22, 8)), ((24, 1), (31, 7)), ((22, 15.5), (31, 20))])
    m.token("janella-greenbottle", 9.5, 7.5); m.token("broker-grisk", 18.5, 5.4)
    m.token("vexa-corven", 18, 13.2, hidden=True)
    m.token("souljack-hauler", 7, 5.5, hidden=True)
    for x in (24.5, 27, 29.5):
        m.token("scorchhound-quad", x, 17.5, hidden=True)
    marker(m, 7, 5.5, "Y1: Janella's lift (restore the Souljack Hauler)", "souljack-yard")
    marker(m, 8, 17, "Y2: The wreck field (salvage soul coins)", "souljack-yard")
    marker(m, 18.5, 4, "Y3: Broker Grisk's coin booth", "souljack-yard")
    marker(m, 27.5, 3, "Y4: The fuel shed (demon ichor)", "souljack-yard")
    marker(m, 18, 12, "Y5: The loan table (Form G-12)", "souljack-yard")
    return m


@register
def redline_run():
    """The Redline Run: the Claw Rift image restaged as a moving road (Blackspine Narrows)."""
    m = claw_rift()
    m.key, m.name = "redline-run", "Interlude: The Redline Run (Claw Rift)"
    m.image = "claw-rift"
    m.tokens, m.notes = [], []
    for lane, y in (("NORTH LANE", 11), ("CENTRE LANE", 15), ("SOUTH LANE", 19)):
        marker(m, 3, y, f"{lane} (20 ft)", "redline")
    marker(m, 20, 6.5, "The Blackspine teeth: collision 3d10 bludgeoning + 2d10 fire", "redline")
    marker(m, 36, 15, "Scroll seam: recentre the convoy each round", "redline")
    m.token("souljack-hauler", 22, 15, hidden=True)
    m.token("scorchhound-quad", 26, 11, hidden=True)
    m.token("iron-reclaimer", 9, 15, hidden=True)
    m.token("cinderfang-spiker", 13, 11, hidden=True)
    m.token("cinderfang-spiker", 13, 19, hidden=True)
    m.token("kestrel-vane", 9, 15, hidden=True)
    return m


ORDER = ["welcome", "findings", "greyhurst", "mansion-lower", "mansion-upper", "arena", "counting-gate", "ash-bridge", "styx-ferry", "tavern",
         "greenbottle", "market-names", "docket", "masquerade", "citadel", "iron-quarter", "audience", "reliquary",
         "breach", "greyhurst-district", "ashen-caverns", "claw-rift", "souljack-yard", "redline-run"]

if __name__ == "__main__":
    out = "/home/claude/ic/module/assets/maps"
    prev = "/home/claude/ic/art/preview"
    os.makedirs(prev, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    which = sys.argv[1:] or ORDER
    data = {}
    if os.path.exists("/home/claude/ic/src/scenes.json"):
        data = json.load(open("/home/claude/ic/src/scenes.json"))
        data = {k: v for k, v in data.items() if k in MAPS}
    for k in which:
        m = MAPS[k]()
        if not getattr(m, "image", None):
            m.render(f"{out}/{k}.webp", f"{prev}/{k}.webp")
        data[k] = m.export()
        if getattr(m, "image", None):
            data[k]["image"] = m.image
        print(k, m.W, m.H, "walls", len(m.walls), "lights", len(m.lights), "notes", len(m.notes))
    json.dump(data, open("/home/claude/ic/src/scenes.json", "w"), indent=0)
