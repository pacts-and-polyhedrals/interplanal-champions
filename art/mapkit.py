"""Vector battlemap kit.

Authoring is in grid squares (1 square = 5 ft = GRID px). The same wall geometry draws the
art and is exported as Foundry wall segments, so walls line up with the drawn stone exactly.
"""
import math, random, io, json
import numpy as np
from PIL import Image, ImageFilter
import resvg_py

GRID = 100
INK = "#150b0b"
FONTS = "/home/claude/ic/art/fonts"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Map:
    def __init__(self, key, name, w, h, *, seed=1, bg="#2a2224"):
        self.key, self.name, self.w, self.h = key, name, w, h
        self.W, self.H = w * GRID, h * GRID
        self.rnd = random.Random(seed)
        self.defs = []
        self.L = {k: [] for k in ("floor", "decal", "lowprop", "walls", "props", "high", "label")}
        self.walls, self.lights, self.notes, self.tokens, self.sounds = [], [], [], [], []
        self.bg = bg
        self.pat_done = set()
        self.env = {"darkness": 0.0, "globalLight": True}
        self.grain = 0.10
        self.vignette = True
        self._shadow()

    # ------------------------------------------------------------------ utils
    def P(self, v):
        return v * GRID

    def add(self, layer, s):
        self.L[layer].append(s)

    def _shadow(self):
        self.defs.append('<filter id="sh" x="-30%" y="-30%" width="160%" height="160%">'
                         '<feDropShadow dx="7" dy="9" stdDeviation="6" flood-color="#000" flood-opacity="0.55"/></filter>')
        self.defs.append('<filter id="shs" x="-30%" y="-30%" width="160%" height="160%">'
                         '<feDropShadow dx="3" dy="4" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/></filter>')
        self.defs.append('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
                         '<feGaussianBlur stdDeviation="14"/></filter>')
        self.defs.append('<filter id="blur4"><feGaussianBlur stdDeviation="4"/></filter>')
        self.defs.append('<radialGradient id="rg-fire"><stop offset="0" stop-color="#ffe08a"/>'
                         '<stop offset="0.45" stop-color="#ff7a1a"/><stop offset="1" stop-color="#7a0a05" stop-opacity="0"/></radialGradient>')
        self.defs.append('<radialGradient id="rg-gold"><stop offset="0" stop-color="#fff2b0" stop-opacity="0.9"/>'
                         '<stop offset="1" stop-color="#ffb640" stop-opacity="0"/></radialGradient>')
        self.defs.append('<radialGradient id="rg-sun"><stop offset="0" stop-color="#fffbe0"/>'
                         '<stop offset="0.5" stop-color="#ffd25a"/><stop offset="1" stop-color="#ff8a1a"/></radialGradient>')
        self.defs.append('<linearGradient id="lg-brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2b65a"/>'
                         '<stop offset="0.5" stop-color="#a87a2a"/><stop offset="1" stop-color="#6e4a16"/></linearGradient>')
        self.defs.append('<linearGradient id="lg-iron" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5a5660"/>'
                         '<stop offset="1" stop-color="#26232a"/></linearGradient>')
        self.defs.append('<linearGradient id="lg-crimson" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c0283a"/>'
                         '<stop offset="1" stop-color="#5e0b18"/></linearGradient>')

    # --------------------------------------------------------------- textures
    def pattern(self, name):
        if name in self.pat_done:
            return f"url(#pt-{name})"
        self.pat_done.add(name)
        r = random.Random(hash(name) & 0xffff)
        T = 400
        body = []
        if name == "cobble":
            body.append(f'<rect width="{T}" height="{T}" fill="#2e2b33"/>')
            step = 40
            for gy in range(-step, T + step, step):
                for gx in range(-step, T + step, step):
                    cx0 = gx + r.uniform(-6, 6) + (step / 2 if (gy // step) % 2 else 0)
                    cy0 = gy + r.uniform(-6, 6)
                    rad = r.uniform(15, 20)
                    n = r.randint(6, 8)
                    pts = []
                    for i in range(n):
                        a = i * 2 * math.pi / n + r.uniform(-0.25, 0.25)
                        d = rad * r.uniform(0.82, 1.08)
                        pts.append(f"{cx0+math.cos(a)*d:.1f},{cy0+math.sin(a)*d*0.9:.1f}")
                    c = r.choice(["#7f7b88", "#787380", "#86818f", "#6f6a78", "#8b8594", "#7c7470", "#847a76", "#6d6975"])
                    body.append(f'<polygon points="{" ".join(pts)}" fill="{c}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
                    body.append(f'<path d="M{cx0-rad*0.5:.1f} {cy0-rad*0.35:.1f} q{rad*0.5:.1f} -5 {rad:.1f} 0" stroke="#a6a1ae" stroke-width="2.5" fill="none" opacity="0.55"/>')
                    if r.random() < 0.18:
                        body.append(f'<ellipse cx="{cx0:.1f}" cy="{cy0+rad*0.45:.1f}" rx="{rad*0.8:.1f}" ry="5" fill="#eef2f8" opacity="0.8"/>')
        elif name == "snow":
            body.append(f'<rect width="{T}" height="{T}" fill="#d7dfea"/>')
            for _ in range(40):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(20,70):.0f}" ry="{r.uniform(8,26):.0f}" '
                            f'fill="{r.choice(["#c4cfdd", "#e9eef5", "#bccadb", "#f2f5f9"])}" opacity="0.8"/>')
            for _ in range(60):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<path d="M{x:.0f} {y:.0f} q8 -4 16 0" stroke="#9fb0c6" stroke-width="2" fill="none"/>')
        elif name == "slush":
            body.append(f'<rect width="{T}" height="{T}" fill="#7d8592"/>')
            for _ in range(70):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(10,50):.0f}" ry="{r.uniform(6,20):.0f}" '
                            f'fill="{r.choice(["#959dab", "#6b7280", "#b9c3d1", "#a6afbd"])}" opacity="0.8"/>')
        elif name in ("planks", "darkplanks"):
            base = "#6b4426" if name == "planks" else "#3e2718"
            body.append(f'<rect width="{T}" height="{T}" fill="{base}"/>')
            y = 0
            while y < T:
                x = -r.randint(0, 200)
                while x < T:
                    ln = r.randint(160, 300)
                    c = r.choice(["#7a4e2c", "#6e4527", "#83552f", "#5f3b21"] if name == "planks" else
                                 ["#46301f", "#3a2617", "#4d3422", "#33210f"])
                    body.append(f'<rect x="{x}" y="{y}" width="{ln}" height="40" fill="{c}" stroke="{INK}" stroke-width="3"/>')
                    for g in range(3):
                        gy = y + 8 + g * 11 + r.randint(-2, 2)
                        body.append(f'<path d="M{x+6} {gy} C{x+ln/3} {gy-3} {x+2*ln/3} {gy+3} {x+ln-6} {gy}" '
                                    f'stroke="#2a180c" stroke-width="1.5" fill="none" opacity="0.45"/>')
                    body.append(f'<circle cx="{x+8}" cy="{y+20}" r="2.5" fill="#1a1010"/>')
                    x += ln
                y += 40
        elif name == "flagstone":
            body.append(f'<rect width="{T}" height="{T}" fill="#2f2b31"/>')
            for gy in range(0, T, 100):
                off = r.choice([0, 50])
                for gx in range(-off, T, 100):
                    c = r.choice(["#58525c", "#4f4a55", "#615a66", "#4a4450"])
                    body.append(f'<rect x="{gx+3}" y="{gy+3}" width="94" height="94" rx="6" fill="{c}" stroke="{INK}" stroke-width="3"/>')
                    body.append(f'<path d="M{gx+12} {gy+80} l{r.randint(10,40)} {-r.randint(5,25)}" stroke="#2a252c" stroke-width="2"/>')
        elif name == "brass":
            body.append(f'<rect width="{T}" height="{T}" fill="#5d4214"/>')
            for gy in range(0, T, 100):
                for gx in range(0, T, 100):
                    body.append(f'<rect x="{gx+2}" y="{gy+2}" width="96" height="96" fill="url(#lg-brass)" stroke="{INK}" stroke-width="3" opacity="{r.uniform(0.75,1):.2f}"/>')
                    for cx, cy in ((10, 10), (90, 10), (10, 90), (90, 90)):
                        body.append(f'<circle cx="{gx+cx}" cy="{gy+cy}" r="4" fill="#3b2a0c"/>')
                    if r.random() < 0.4:
                        body.append(f'<path d="M{gx+20} {gy+r.randint(30,70)} q30 -10 60 4" stroke="#3a2a0a" stroke-width="3" fill="none" opacity="0.5"/>')
        elif name == "grate":
            body.append(f'<rect width="{T}" height="{T}" fill="#141216"/>')
            for i in range(0, T, 25):
                body.append(f'<rect x="{i}" y="0" width="9" height="{T}" fill="#3a3640" stroke="{INK}" stroke-width="2"/>')
            for i in range(0, T, 100):
                body.append(f'<rect x="0" y="{i}" width="{T}" height="12" fill="#4a4550" stroke="{INK}" stroke-width="2"/>')
        elif name == "marble":
            body.append(f'<rect width="{T}" height="{T}" fill="#141012"/>')
            for gy in range(0, T, 100):
                for gx in range(0, T, 100):
                    dark = ((gx + gy) // 100) % 2 == 0
                    c = "#1e1619" if dark else "#5c1420"
                    body.append(f'<rect x="{gx+2}" y="{gy+2}" width="96" height="96" fill="{c}" stroke="#0a0607" stroke-width="3"/>')
                    vx = r.randint(10, 80)
                    body.append(f'<path d="M{gx+vx} {gy+4} C{gx+vx+20} {gy+40} {gx+vx-20} {gy+60} {gx+vx+8} {gy+96}" '
                                f'stroke="{"#3a2a2e" if dark else "#8a3040"}" stroke-width="2" fill="none" opacity="0.8"/>')
        elif name == "carpet":
            body.append(f'<rect width="{T}" height="{T}" fill="#6e0f1c"/>')
            for gy in range(0, T, 100):
                for gx in range(0, T, 100):
                    body.append(f'<path d="M{gx+50} {gy+12} L{gx+88} {gy+50} L{gx+50} {gy+88} L{gx+12} {gy+50} Z" fill="none" stroke="#c99a3a" stroke-width="3" opacity="0.7"/>')
                    body.append(f'<circle cx="{gx+50}" cy="{gy+50}" r="6" fill="#c99a3a" opacity="0.7"/>')
        elif name == "roof":
            body.append(f'<rect width="{T}" height="{T}" fill="#2c3340"/>')
            for gy in range(0, T, 40):
                off = 0 if (gy // 40) % 2 == 0 else 25
                for gx in range(-off, T, 50):
                    c = r.choice(["#46505f", "#3f4856", "#4c5767", "#394150"])
                    body.append(f'<path d="M{gx+2} {gy} h46 v32 q-23 10 -46 0 Z" fill="{c}" stroke="{INK}" stroke-width="2.5"/>')
                    if r.random() < 0.45:
                        body.append(f'<path d="M{gx+4} {gy+4} h42 v8 q-21 6 -42 0 Z" fill="#e6edf6" opacity="0.85"/>')
        elif name == "factory":
            body.append(f'<rect width="{T}" height="{T}" fill="#2b2e2c"/>')
            for gy in range(0, T, 50):
                for gx in range(0, T, 50):
                    c = r.choice(["#3a3f3b", "#353a36", "#40463f", "#30342f"])
                    body.append(f'<rect x="{gx+1.5}" y="{gy+1.5}" width="47" height="47" fill="{c}" stroke="#151715" stroke-width="2"/>')
            for _ in range(10):
                body.append(f'<ellipse cx="{r.uniform(0,T):.0f}" cy="{r.uniform(0,T):.0f}" rx="{r.uniform(20,60):.0f}" '
                            f'ry="{r.uniform(10,30):.0f}" fill="#1a1612" opacity="0.35"/>')
        elif name == "canvas":
            body.append(f'<rect width="{T}" height="{T}" fill="#e9dfc8"/>')
            for i in range(0, T, 80):
                body.append(f'<rect x="{i}" y="0" width="40" height="{T}" fill="#a3182a"/>')
        elif name == "rug":
            body.append(f'<rect width="{T}" height="{T}" fill="#2a3d2a"/>')
            for gy in range(0, T, 50):
                for gx in range(0, T, 50):
                    body.append(f'<rect x="{gx+15}" y="{gy+15}" width="20" height="20" transform="rotate(45 {gx+25} {gy+25})" fill="#b38a2e" opacity="0.6"/>')
        elif name == "hellstone":
            body.append(f'<rect width="{T}" height="{T}" fill="#1a0c0c"/>')
            for gy in range(0, T, 100):
                off = r.choice([0, 50])
                for gx in range(-off, T, 100):
                    c = r.choice(["#3a1a1a", "#331616", "#401e1c", "#2c1414"])
                    body.append(f'<rect x="{gx+3}" y="{gy+3}" width="94" height="94" rx="4" fill="{c}" stroke="#0a0404" stroke-width="3"/>')
                    if r.random() < 0.3:
                        body.append(f'<path d="M{gx+15} {gy+70} l{r.randint(15,40)} {-r.randint(10,30)} l{r.randint(10,20)} 8" stroke="#c2401a" stroke-width="2.5" fill="none" opacity="0.8"/>')
        elif name in ("redsand", "ashsand", "cavefloor"):
            base, blots, peb = {"redsand": ("#7a3a2c", ["#86432f", "#6c3226", "#924d36", "#713628"], ["#3a1a14", "#a8604a"]),
                                "ashsand": ("#86684a", ["#927457", "#7a5e42", "#9a7c5c", "#6e5440"], ["#4a3424", "#b89874"]),
                                "cavefloor": ("#4a3a36", ["#544440", "#40322e", "#5a4a44"], ["#2a1e1c", "#6e5a52"])}[name]
            body.append(f'<rect width="{T}" height="{T}" fill="{base}"/>')
            for _ in range(28):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(30,90):.0f}" ry="{r.uniform(14,40):.0f}" '
                            f'fill="{r.choice(blots)}" opacity="0.7" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
            for _ in range(70):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5,4.5):.1f}" fill="{r.choice(peb)}" opacity="0.8"/>')
            for _ in range(9):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-30,30):.0f} {r.uniform(8,30):.0f} l{r.uniform(-20,20):.0f} {r.uniform(8,25):.0f}" '
                            f'stroke="{peb[0]}" stroke-width="2" fill="none" opacity="0.6"/>')
        elif name == "lava":
            T = 900
            body.append(f'<rect width="{T}" height="{T}" fill="#f07a14"/>')
            for _ in range(220):
                x, y = r.uniform(-40, T + 40), r.uniform(-40, T + 40)
                body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(18,70):.0f}" ry="{r.uniform(10,34):.0f}" '
                            f'fill="{r.choice(["#ffd25a", "#ffb43a", "#ffe58a", "#e8561a", "#ff9a2a", "#d8400e"])}" opacity="{r.uniform(0.5,0.85):.2f}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
            # cooling crust cracks (wrapping network)
            nodes = [(r.uniform(0, T), r.uniform(0, T)) for _ in range(60)]
            for (x1, y1) in nodes:
                near = sorted(nodes, key=lambda p: (p[0] - x1) ** 2 + (p[1] - y1) ** 2)[1:3]
                for (x2, y2) in near:
                    mx, my = (x1 + x2) / 2 + r.uniform(-15, 15), (y1 + y2) / 2 + r.uniform(-15, 15)
                    for ox in (-T, 0, T):
                        for oy in (-T, 0, T):
                            body.append(f'<path d="M{x1+ox:.0f} {y1+oy:.0f} Q{mx+ox:.0f} {my+oy:.0f} {x2+ox:.0f} {y2+oy:.0f}" stroke="#9a2a08" stroke-width="{r.uniform(2,4.5):.1f}" fill="none" opacity="0.7"/>')
        elif name == "basalt":
            body.append(f'<rect width="{T}" height="{T}" fill="#ff5a14"/>')
            step = 80
            for gy in range(-step, T + step, step):
                for gx in range(-step, T + step, step):
                    cx0, cy0 = gx + r.uniform(-12, 12) + (step / 2 if (gy // step) % 2 else 0), gy + r.uniform(-12, 12)
                    n = r.randint(5, 7)
                    pts = []
                    for i in range(n):
                        a = i * 2 * math.pi / n + r.uniform(-0.3, 0.3)
                        d = r.uniform(30, 40)
                        pts.append(f"{cx0+math.cos(a)*d:.1f},{cy0+math.sin(a)*d:.1f}")
                    c = r.choice(["#2a2a30", "#33323a", "#25242a", "#3a3940"])
                    body.append(f'<polygon points="{" ".join(pts)}" fill="{c}" stroke="#1a0806" stroke-width="3" stroke-linejoin="round"/>')
                    body.append(f'<path d="M{cx0-14:.0f} {cy0-10:.0f} q12 -6 24 0" stroke="#55545e" stroke-width="3" fill="none" opacity="0.6"/>')
        elif name == "paleflag":
            body.append(f'<rect width="{T}" height="{T}" fill="#8a7e7c"/>')
            for gy in range(0, T, 100):
                for gx in range(0, T, 100):
                    c = r.choice(["#cfc4c0", "#c5b9b5", "#d8cfcb", "#bfb2ae"])
                    body.append(f'<rect x="{gx+3}" y="{gy+3}" width="94" height="94" rx="3" fill="{c}" stroke="#5a5050" stroke-width="3"/>')
                    if r.random() < 0.35:
                        body.append(f'<path d="M{gx+10} {gy+r.randint(20,80)} q{r.randint(20,40)} {r.randint(-10,10)} {r.randint(50,80)} {r.randint(-6,6)}" stroke="#a89c98" stroke-width="2" fill="none"/>')
        elif name == "darkcobble":
            body.append(f'<rect width="{T}" height="{T}" fill="#2a2426"/>')
            step = 40
            for gy in range(-step, T + step, step):
                for gx in range(-step, T + step, step):
                    cx0 = gx + r.uniform(-6, 6) + (step / 2 if (gy // step) % 2 else 0)
                    cy0 = gy + r.uniform(-6, 6)
                    rad = r.uniform(15, 20)
                    n = r.randint(6, 8)
                    pts = []
                    for i in range(n):
                        a = i * 2 * math.pi / n + r.uniform(-0.25, 0.25)
                        d = rad * r.uniform(0.82, 1.08)
                        pts.append(f"{cx0+math.cos(a)*d:.1f},{cy0+math.sin(a)*d*0.9:.1f}")
                    c = r.choice(["#6a6266", "#615a5e", "#72686a", "#5a5256", "#6e6462", "#655a58"])
                    body.append(f'<polygon points="{" ".join(pts)}" fill="{c}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
                    body.append(f'<path d="M{cx0-rad*0.5:.1f} {cy0-rad*0.35:.1f} q{rad*0.5:.1f} -5 {rad:.1f} 0" stroke="#8a8084" stroke-width="2.5" fill="none" opacity="0.5"/>')
                    if r.random() < 0.08:
                        body.append(f'<ellipse cx="{cx0:.1f}" cy="{cy0:.1f}" rx="{rad*0.9:.1f}" ry="{rad*0.5:.1f}" fill="#3a2a22" opacity="0.6"/>')
        elif name == "arenastone":
            body.append(f'<rect width="{T}" height="{T}" fill="#221e2a"/>')
            for gy in range(0, T, 50):
                off = 25 if (gy // 50) % 2 else 0
                for gx in range(-off, T, 100):
                    c = r.choice(["#3a3446", "#433c52", "#3e384b", "#36303f"])
                    body.append(f'<rect x="{gx+2}" y="{gy+2}" width="96" height="46" rx="3" fill="{c}" stroke="#16131c" stroke-width="3"/>')
        elif name == "hellroof":
            body.append(f'<rect width="{T}" height="{T}" fill="#2a2226"/>')
            for gy in range(0, T, 30):
                off = 0 if (gy // 30) % 2 == 0 else 20
                for gx in range(-off, T, 40):
                    c = r.choice(["#4a3e44", "#3e3438", "#54464c", "#463a40"])
                    body.append(f'<path d="M{gx} {gy} h40 v18 q-20 14 -40 0 Z" fill="{c}" stroke="#140e10" stroke-width="2.5"/>')
        elif name == "bonefloor":
            body.append(f'<rect width="{T}" height="{T}" fill="#b8a888"/>')
            for _ in range(60):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(8,26):.0f}" ry="{r.uniform(4,10):.0f}" fill="{r.choice(["#d8cbb0", "#a8987a", "#c6b796"])}" '
                            f'stroke="#5a4a3a" stroke-width="2" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
        elif name == "grass":
            body.append(f'<rect width="{T}" height="{T}" fill="#4e6a2a"/>')
            for _ in range(24):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(40,100):.0f}" ry="{r.uniform(25,60):.0f}" fill="{r.choice(["#5a7a30", "#46602a", "#62823a", "#6a7a3a"])}" opacity="0.7"/>')
            for _ in range(420):
                x, y = r.uniform(0, T), r.uniform(0, T)
                body.append(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-5,5):.0f} {-r.uniform(8,16):.0f}" stroke="{r.choice(["#7a9a40", "#3a5020", "#8aaa4a", "#506a28"])}" stroke-width="2.4" stroke-linecap="round"/>')
        elif name == "bigbasalt":
            T = 1200
            body.append(f'<rect width="{T}" height="{T}" fill="#ff4a0a"/>')
            step = 200
            cells = {}
            for gy in range(0, T, step):
                for gx in range(0, T, step):
                    cells[(gx, gy)] = (gx + r.uniform(-25, 25) + (step / 2 if (gy // step) % 2 else 0), gy + r.uniform(-25, 25),
                                       [r.uniform(100, 122) for _ in range(7)], r.uniform(-0.3, 0.3), r.choice(["#2a2a30", "#33323a", "#25242a", "#3a3940", "#2e2a2c"]))
            for (gx, gy), (cx0, cy0, ds, rot, c) in cells.items():
                for ox in (-T, 0, T):
                    for oy in (-T, 0, T):
                        X, Y = cx0 + ox, cy0 + oy
                        if X < -150 or X > T + 150 or Y < -150 or Y > T + 150:
                            continue
                        pts = [(X + math.cos(i * 2 * math.pi / 7 + rot) * d, Y + math.sin(i * 2 * math.pi / 7 + rot) * d) for i, d in enumerate(ds)]
                        pp = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                        body.append(f'<polygon points="{pp}" fill="{c}" stroke="#1a0806" stroke-width="6" stroke-linejoin="round"/>')
                        body.append(f'<path d="M{X-50:.0f} {Y-40:.0f} q36 -20 84 -4" stroke="#5a5864" stroke-width="8" fill="none" opacity="0.55" stroke-linecap="round"/>')
        elif name == "ruintile":
            body.append(f'<rect width="{T}" height="{T}" fill="#5a2a1c"/>')
            for gy in range(0, T, 100):
                for gx in range(0, T, 100):
                    c = r.choice(["#8a4a2a", "#7e4426", "#94522e", "#84462a"])
                    body.append(f'<rect x="{gx+4}" y="{gy+4}" width="92" height="92" rx="4" fill="{c}" stroke="#3a1a10" stroke-width="3"/>')
                    body.append(f'<rect x="{gx+40}" y="{gy+40}" width="20" height="20" fill="#c0703a" stroke="#3a1a10" stroke-width="2" transform="rotate(45 {gx+50} {gy+50})"/>')
                    if r.random() < 0.3:
                        body.append(f'<path d="M{gx+8} {gy+r.randint(10,90)} l{r.randint(20,50)} {r.randint(-15,15)} l{r.randint(10,30)} {r.randint(-10,10)}" stroke="#3a1a10" stroke-width="2" fill="none"/>')
        elif name == "manortile":
            body.append(f'<rect width="{T}" height="{T}" fill="#1e1a22"/>')
            for gy in range(0, T, 100):
                for gx in range(0, T, 100):
                    c = r.choice(["#3e3846", "#463e50", "#3a3442"]) if (gx + gy) // 100 % 2 else r.choice(["#5a3a3a", "#643e3e", "#563636"])
                    body.append(f'<rect x="{gx+3}" y="{gy+3}" width="94" height="94" rx="2" fill="{c}" stroke="#141016" stroke-width="3"/>')
                    if r.random() < 0.25:
                        body.append(f'<path d="M{gx+10} {gy+r.randint(15,85)} l{r.randint(30,70)} {r.randint(-12,12)}" stroke="#141016" stroke-width="2" fill="none"/>')
        else:
            raise KeyError(name)
        self.defs.append(f'<pattern id="pt-{name}" width="{T}" height="{T}" patternUnits="userSpaceOnUse">{"".join(body)}</pattern>')
        return f"url(#pt-{name})"

    # ----------------------------------------------------------------- floors
    def floor_rect(self, x, y, w, h, tex, layer="floor", rx=0, stroke=True):
        s = f' stroke="{INK}" stroke-width="5"' if stroke else ""
        self.add(layer, f'<rect x="{self.P(x)}" y="{self.P(y)}" width="{self.P(w)}" height="{self.P(h)}" rx="{rx}" fill="{self.pattern(tex)}"{s}/>')

    def floor_poly(self, pts, tex, layer="floor", stroke=True):
        d = " ".join(f"{self.P(a):.0f},{self.P(b):.0f}" for a, b in pts)
        s = f' stroke="{INK}" stroke-width="5"' if stroke else ""
        self.add(layer, f'<polygon points="{d}" fill="{self.pattern(tex)}"{s}/>')

    def floor_circle(self, cx, cy, r, tex, layer="floor"):
        self.add(layer, f'<circle cx="{self.P(cx)}" cy="{self.P(cy)}" r="{self.P(r)}" fill="{self.pattern(tex)}" stroke="{INK}" stroke-width="5"/>')

    def fill_all(self, tex):
        self.add("floor", f'<rect width="{self.W}" height="{self.H}" fill="{self.pattern(tex)}"/>')

    # ------------------------------------------------------------------ walls
    WALL_STYLE = {
        "stone": ("#5b5560", "#7a7480", 32),
        "brick": ("#6a3a30", "#8a5444", 30),
        "brass": ("#9a6e24", "#d8aa52", 28),
        "iron": ("#2f2c34", "#57535e", 30),
        "timber": ("#4a3020", "#6e4a30", 24),
        "canvas": ("#a3182a", "#e9dfc8", 14),
        "hell": ("#3a1414", "#7a2a22", 34),
        "shelf": ("#3b2516", "#6b4426", 26),
        "ruin": ("#56525c", "#8a8690", 36),
        "dark": ("#3a3a44", "#5e5e6a", 34),
        "keep": ("#3e4048", "#727680", 62),
    }

    def wall(self, pts, style="stone", closed=False, kind="wall", draw=True, sight="normal"):
        """Draw a thick wall along pts and register Foundry segments."""
        if closed:
            pts = list(pts) + [pts[0]]
        dark, light, th = self.WALL_STYLE[style]
        d = "M" + " L".join(f"{self.P(a):.1f} {self.P(b):.1f}" for a, b in pts)
        if draw:
            self.add("walls", f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{th+10}" stroke-linejoin="round" stroke-linecap="square" filter="url(#sh)"/>')
            self.add("walls", f'<path d="{d}" fill="none" stroke="{dark}" stroke-width="{th}" stroke-linejoin="round" stroke-linecap="square"/>')
            if style == "keep":
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="{th-16}" stroke-linejoin="round" stroke-dasharray="46 8"/>')
                self.add("walls", f'<path d="{d}" fill="none" stroke="#9a9ea8" stroke-width="8" stroke-linejoin="round" stroke-dasharray="30 24" opacity="0.6"/>')
            if style in ("ruin", "dark"):
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="{th-12}" stroke-linejoin="round" stroke-dasharray="34 8"/>')
                self.add("walls", f'<path d="{d}" fill="none" stroke="#2a2830" stroke-width="3" stroke-linejoin="round" stroke-dasharray="1 41" stroke-linecap="round" opacity="0.8"/>')
            if style in ("stone", "brick", "hell"):
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="{th*0.35:.0f}" stroke-linejoin="round" stroke-dasharray="26 10" opacity="0.7"/>')
            elif style == "brass":
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="6" stroke-linejoin="round"/>')
                self.add("walls", f'<path d="{d}" fill="none" stroke="#3a2a0a" stroke-width="7" stroke-dasharray="3 47" stroke-linecap="round"/>')
            elif style == "canvas":
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="8" stroke-dasharray="30 30"/>')
            elif style == "timber":
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="6" stroke-dasharray="60 8"/>')
            elif style == "iron":
                self.add("walls", f'<path d="{d}" fill="none" stroke="{light}" stroke-width="5" stroke-dasharray="12 18"/>')
            elif style == "shelf":
                self.add("walls", f'<path d="{d}" fill="none" stroke="#2a180c" stroke-width="{th-8}" stroke-dasharray="7 4"/>')
        for (a, b), (c, e) in zip(pts, pts[1:]):
            self.walls.append({"c": [self.P(a), self.P(b), self.P(c), self.P(e)], "kind": kind, "sight": sight})

    def window(self, x1, y1, x2, y2):
        self.add("walls", f'<line x1="{self.P(x1)}" y1="{self.P(y1)}" x2="{self.P(x2)}" y2="{self.P(y2)}" stroke="{INK}" stroke-width="22"/>')
        self.add("walls", f'<line x1="{self.P(x1)}" y1="{self.P(y1)}" x2="{self.P(x2)}" y2="{self.P(y2)}" stroke="#9fc6e8" stroke-width="10"/>')
        self.walls.append({"c": [self.P(x1), self.P(y1), self.P(x2), self.P(y2)], "kind": "window", "sight": "normal"})

    def door(self, x1, y1, x2, y2, style="wood", secret=False, locked=False):
        x1p, y1p, x2p, y2p = map(self.P, (x1, y1, x2, y2))
        ln = math.hypot(x2p - x1p, y2p - y1p)
        ang = math.degrees(math.atan2(y2p - y1p, x2p - x1p))
        cx, cy = (x1p + x2p) / 2, (y1p + y2p) / 2
        if not secret:
            fill = {"wood": "#7a4a22", "iron": "#4a4650", "brass": "#c08a30", "red": "#8e1424"}[style]
            g = (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})">'
                 f'<rect x="{-ln/2:.1f}" y="-11" width="{ln:.1f}" height="22" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
                 f'<line x1="{-ln/2+8:.1f}" y1="0" x2="{ln/2-8:.1f}" y2="0" stroke="{INK}" stroke-width="2" opacity="0.6"/>'
                 f'<circle cx="{ln/2-16:.1f}" cy="0" r="5" fill="#e8c35a" stroke="{INK}" stroke-width="2"/></g>')
            self.add("walls", g)
        self.walls.append({"c": [x1p, y1p, x2p, y2p], "kind": "secret" if secret else "door", "locked": locked,
                           "sight": "normal"})

    def invisible_wall(self, pts):
        for (a, b), (c, e) in zip(pts, pts[1:]):
            self.walls.append({"c": [self.P(a), self.P(b), self.P(c), self.P(e)], "kind": "invisible", "sight": "none"})

    def terrain_wall(self, pts, closed=False):
        if closed:
            pts = list(pts) + [pts[0]]
        for (a, b), (c, e) in zip(pts, pts[1:]):
            self.walls.append({"c": [self.P(a), self.P(b), self.P(c), self.P(e)], "kind": "terrain", "sight": "limited"})

    def room(self, x, y, w, h, style="stone", doors=(), gaps=()):
        """Rectangle of walls. doors/gaps: (side, offset, width[, doorstyle]) side in N,E,S,W."""
        sides = {"N": ((x, y), (x + w, y)), "E": ((x + w, y), (x + w, y + h)),
                 "S": ((x + w, y + h), (x, y + h)), "W": ((x, y + h), (x, y))}
        cuts = {}
        for d in list(doors) + [(g[0], g[1], g[2], None) for g in gaps]:
            cuts.setdefault(d[0], []).append(d)
        for side, ((ax, ay), (bx, by)) in sides.items():
            L = math.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / L, (by - ay) / L
            segs, cur = [], 0.0
            for (sd, off, wd, *rest) in sorted(cuts.get(side, []), key=lambda c: c[1]):
                segs.append((cur, off))
                if rest and rest[0]:
                    self.door(ax + ux * off, ay + uy * off, ax + ux * (off + wd), ay + uy * (off + wd), style=rest[0])
                cur = off + wd
            segs.append((cur, L))
            for s0, s1 in segs:
                if s1 - s0 > 0.01:
                    self.wall([(ax + ux * s0, ay + uy * s0), (ax + ux * s1, ay + uy * s1)], style)

    # ----------------------------------------------------------------- props
    def g(self, layer, x, y, inner, rot=0, scale=1, shadow=True):
        f = ' filter="url(#sh)"' if shadow else ""
        self.add(layer, f'<g transform="translate({self.P(x):.1f},{self.P(y):.1f}) rotate({rot}) scale({scale})"{f}>{inner}</g>')

    def text(self, x, y, s, size=40, color="#f0e2c0", font="Cinzel", weight=700, rot=0, anchor="middle", layer="label",
             stroke=True):
        st = f' stroke="{INK}" stroke-width="{size/6:.1f}" paint-order="stroke"' if stroke else ""
        self.add(layer, f'<text x="{self.P(x):.1f}" y="{self.P(y):.1f}" font-family="{font}" font-weight="{weight}" '
                        f'font-size="{size}" fill="{color}" text-anchor="{anchor}" transform="rotate({rot} {self.P(x):.1f} {self.P(y):.1f})"{st}>{esc(s)}</text>')

    # ---------------------------------------------------------------- export
    def light(self, x, y, dim, bright, color="#ffb35a", alpha=0.35, anim=None, speed=3, intensity=3, walls=True,
              luminosity=0.5):
        self.lights.append({"x": self.P(x), "y": self.P(y), "dim": dim, "bright": bright, "color": color,
                            "alpha": alpha, "anim": anim, "speed": speed, "intensity": intensity, "walls": walls,
                            "luminosity": luminosity})

    def note(self, x, y, page, label, icon="book"):
        self.notes.append({"x": self.P(x), "y": self.P(y), "page": page, "label": label, "icon": icon})

    def token(self, actor, x, y, hidden=False, name=None, elevation=0):
        self.tokens.append({"actor": actor, "x": self.P(x), "y": self.P(y), "hidden": hidden, "name": name})

    def svg(self):
        layers = "".join(f'<g id="{k}">{"".join(v)}</g>' for k, v in self.L.items())
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}">'
                f'<defs>{"".join(self.defs)}</defs><rect width="{self.W}" height="{self.H}" fill="{self.bg}"/>{layers}</svg>')

    def render(self, out_webp, preview=None, quality=80):
        png = resvg_py.svg_to_bytes(svg_string=self.svg(), font_dirs=[FONTS], skip_system_fonts=False)
        im = Image.open(io.BytesIO(bytes(png))).convert("RGB")
        im = self._finish(im)
        im.save(out_webp, "WEBP", quality=quality, method=5)
        if preview:
            t = im.copy()
            t.thumbnail((1400, 1400))
            t.save(preview, "WEBP", quality=70)
        return im

    def _finish(self, im):
        """Ink-print grain and a soft vignette over the vector art."""
        w, h = im.size
        rng = np.random.default_rng(len(self.key))
        small = rng.normal(0, 1, (h // 6 + 1, w // 6 + 1)).astype(np.float32)
        noise = np.array(Image.fromarray(((small * 40) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                         dtype=np.float32) / 255.0 - 0.5
        fine = rng.normal(0, 1, (h, w)).astype(np.float32) * 0.5
        arr = np.asarray(im, dtype=np.float32)
        g = (noise * 0.9 + fine * 0.15) * self.grain * 255
        arr = arr + g[..., None]
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        vig = 1 - np.clip(d - 0.75, 0, 1) * (0.45 if self.vignette else 0)
        arr = arr * vig[..., None]
        return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

    def export(self):
        return {"key": self.key, "name": self.name, "width": self.W, "height": self.H, "grid": GRID,
                "walls": self.walls, "lights": self.lights, "notes": self.notes, "tokens": self.tokens,
                "env": self.env, "sounds": self.sounds}
