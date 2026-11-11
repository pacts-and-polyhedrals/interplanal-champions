"""Chapter headpieces: one vector illustration per chapter / appendix of Book I and Book II.

Each piece is a 1600x520 scene drawn in the chibi house style, with a sky, a set piece and one to six cast figures.
Output: module/assets/art/chapters/<key>.webp (used in the Foundry journals and the PDF chapter openers).
"""
import io, math, os, random, sys
import resvg_py
from PIL import Image
from chibi import DEFS, humanoid, INK, FONTS
from cast import CAST
from keyart import peaks, embers, lava, crown

OUT = "/home/claude/ic/module/assets/art/chapters"
W, H = 1600, 520
GOLD = "#d8aa52"


def S(w=8):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def fig(key, x, y, s, flip=False):
    por = CAST[key][0]
    inner = humanoid(por) if isinstance(por, dict) else por
    fx = f" translate(1000,0) scale(-1,1)" if flip else ""
    return f'<g transform="translate({x},{y}) scale({s}){fx}">{inner}</g>'


def skyg(c1, c2="#3a0610", c3="#070203", cx=0.5, cy=0.35):
    return (f'<radialGradient id="sk" cx="{cx}" cy="{cy}" r="0.95"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="0.55" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/></radialGradient>'
            f'<rect width="{W}" height="{H}" fill="url(#sk)"/>')


def glow(x, y, r, c="#ff7a1a", op=0.25):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{op}" filter="url(#glw2)"/>'


# ------------------------------------------------------------------ set pieces
def gate(cx, base, w=420, h=360):
    x0, x1 = cx - w / 2, cx + w / 2
    tally = "".join(f'<line x1="{x0 + 30 + i * 22}" y1="{base - h + 70}" x2="{x0 + 30 + i * 22}" y2="{base - h + 110}" '
                    f'stroke="{GOLD}" stroke-width="6"/>' + (f'<line x1="{x0 + 20 + i * 22}" y1="{base - h + 105}" '
                    f'x2="{x0 + 100 + i * 22}" y2="{base - h + 75}" stroke="{GOLD}" stroke-width="5"/>' if i % 5 == 4 else "")
                    for i in range(15))
    bars = "".join(f'<line x1="{cx - 120 + i * 30}" y1="{base - h + 150}" x2="{cx - 120 + i * 30}" y2="{base}" '
                   f'stroke="#1a1012" stroke-width="10"/>' for i in range(9))
    return (f'<rect x="{x0}" y="{base - h}" width="{w}" height="{h}" fill="#2a1418" {S(10)}/>'
            f'<path d="M{cx - 140} {base} L{cx - 140} {base - h + 210} Q{cx} {base - h + 110} {cx + 140} {base - h + 210} '
            f'L{cx + 140} {base} Z" fill="#ff6a1a" opacity="0.85" {S(8)}/>{bars}{tally}'
            + "".join(f'<polygon points="{x0 + i * 60},{base - h} {x0 + 20 + i * 60},{base - h - 50} {x0 + 40 + i * 60},{base - h}" '
                      f'fill="#2a1418" {S(6)}/>' for i in range(int(w // 60) + 1)))


def bridge(x0, x1, y):
    mid = (x0 + x1) / 2
    return (f'<path d="M{x0} {y} Q{mid} {y - 120} {x1} {y} L{x1} {y + 40} Q{mid} {y - 70} {x0} {y + 40} Z" fill="#3a2a2a" {S(8)}/>'
            + "".join(f'<line x1="{x0 + i * (x1 - x0) / 10}" y1="{y - 8 - 100 * math.sin(math.pi * i / 10)}" '
                      f'x2="{x0 + i * (x1 - x0) / 10}" y2="{y - 50 - 100 * math.sin(math.pi * i / 10)}" stroke="{INK}" stroke-width="6"/>'
                      for i in range(1, 10)))


def house(x, base, w, h, roof="#3a2a36", wall="#2a3a44", sunk=0, lit=True):
    y = base - h + sunk
    win = (f'<rect x="{x + w * 0.3}" y="{y + h * 0.25}" width="{w * 0.18}" height="{h * 0.2}" fill="{"#ffd27a" if lit else "#1a2228"}" {S(4)}/>'
           f'<rect x="{x + w * 0.58}" y="{y + h * 0.25}" width="{w * 0.18}" height="{h * 0.2}" fill="#1a2228" {S(4)}/>')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}" {S(7)}/>'
            f'<polygon points="{x - 14},{y} {x + w / 2},{y - h * 0.55} {x + w + 14},{y}" fill="{roof}" {S(7)}/>{win}')


def water(y, c="#123a44", seed=1):
    r = random.Random(seed)
    lines = "".join(f'<path d="M{x} {y + dy} q30 -8 60 0" stroke="#7fd0d8" stroke-width="4" fill="none" opacity="0.5"/>'
                    for x, dy in ((r.randint(0, W), r.randint(15, H - y - 10)) for _ in range(40)))
    return f'<rect x="0" y="{y}" width="{W}" height="{H - y}" fill="{c}" opacity="0.92"/>{lines}'


def banner(x, y, h, col, emblem=""):
    return (f'<line x1="{x}" y1="{y - 20}" x2="{x}" y2="{y + h + 60}" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M{x} {y} h90 v{h} l-45 -34 l-45 34 Z" fill="{col}" {S(7)}/>'
            f'<circle cx="{x + 45}" cy="{y + h * 0.4}" r="22" fill="{GOLD}" {S(5)}/>{emblem}')


def ledgers(x, base, n=5, seed=3):
    r = random.Random(seed)
    out, y = [], base
    for i in range(n):
        w = r.randint(150, 210)
        hh = r.randint(26, 40)
        xx = x + r.randint(-14, 14)
        out.append(f'<rect x="{xx}" y="{y - hh}" width="{w}" height="{hh}" rx="4" fill="{r.choice(["#5e0b18", "#2c3a5a", "#3a2a14", "#4a1a3a"])}" {S(6)}/>'
                   f'<line x1="{xx + 10}" y1="{y - hh / 2}" x2="{xx + w - 10}" y2="{y - hh / 2}" stroke="{GOLD}" stroke-width="4"/>')
        y -= hh
    return "".join(out)


def arena(base):
    tiers = ""
    for i, (yy, hh, c) in enumerate(((base - 300, 70, "#5a3a20"), (base - 230, 80, "#6a4626"), (base - 150, 90, "#7a522c"))):
        tiers += f'<rect x="0" y="{yy}" width="{W}" height="{hh}" fill="{c}" {S(6)}/>'
        tiers += "".join(f'<path d="M{x} {yy + hh} v-{hh * 0.6} a26 26 0 0 1 52 0 v{hh * 0.6}" fill="#1a0e08" {S(5)}/>'
                         for x in range(30 + i * 40, W, 130))
    flags = "".join(f'<line x1="{x}" y1="{base - 300}" x2="{x}" y2="{base - 380}" stroke="{INK}" stroke-width="6"/>'
                    f'<path d="M{x} {base - 380} l50 12 l-50 14 Z" fill="#c0183a" {S(4)}/>' for x in range(80, W, 220))
    return tiers + flags + f'<rect x="0" y="{base - 60}" width="{W}" height="{H - base + 60}" fill="#c8a060" {S(6)}/>'


def thorns(seed=4, y0=H, n=14):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x = r.randint(-50, W + 50)
        d = f"M{x} {y0}"
        cx, cy = x, y0
        for _ in range(5):
            nx, ny = cx + r.randint(-120, 120), cy - r.randint(50, 110)
            d += f" Q{cx + r.randint(-80, 80)} {(cy + ny) / 2} {nx} {ny}"
            out.append(f'<polygon points="{nx - 8},{ny + 4} {nx + 22},{ny - 14} {nx + 6},{ny + 10}" fill="#1a0a0c" {S(3)}/>')
            if r.random() < 0.45:
                out.append(rose(nx, ny, r.uniform(0.6, 1.1)))
            cx, cy = nx, ny
        out.insert(0, f'<path d="{d}" stroke="#1a0a0c" stroke-width="14" fill="none"/><path d="{d}" stroke="#3a1a1c" stroke-width="6" fill="none"/>')
    return "".join(out)


def rose(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><circle r="26" fill="#a3182a" {S(5)}/>'
            f'<path d="M-14 -4 q14 -22 28 0 q-14 18 -28 0" fill="#d8304a" {S(4)}/><circle r="7" fill="#5e0b18"/></g>')


def throne(cx, base, s=1.0):
    return (f'<g transform="translate({cx},{base}) scale({s})">'
            + "".join(f'<rect x="{-260 + i * 40}" y="{-40 - i * 40}" width="{520 - i * 80}" height="40" fill="#2a1418" {S(6)}/>' for i in range(4))
            + f'<path d="M-110 -160 L-110 -470 L-60 -420 L-30 -520 L0 -440 L30 -520 L60 -420 L110 -470 L110 -160 Z" fill="#5e0b18" {S(9)}/>'
            f'<rect x="-130" y="-240" width="260" height="80" fill="#3a0a10" {S(8)}/>'
            f'<circle cx="0" cy="-350" r="40" fill="#c0183a" {S(7)}/><circle cx="0" cy="-350" r="70" fill="#ff3a3a" opacity="0.3" filter="url(#glw)"/></g>')


def seals(cx, cy, r, n=9, rs=30):
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="14 10" opacity="0.8"/>'
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        out += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rs}" fill="#a3182a" {S(5)}/>'
                f'<text x="{x:.0f}" y="{y + rs * 0.35:.0f}" font-family="Cinzel" font-weight="900" font-size="{rs:.0f}" fill="{GOLD}" '
                f'text-anchor="middle">{"I II III IV V VI VII VIII IX".split()[i]}</text>')
    return out


def scroll(x, y, w, h, rot=0, lines=6, seals_=1):
    out = (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="0" y="0" width="{w}" height="{h}" fill="#f0dfb4" {S(6)}/>'
           f'<rect x="-14" y="-16" width="{w + 28}" height="26" rx="13" fill="#c9a96a" {S(6)}/>'
           f'<rect x="-14" y="{h - 10}" width="{w + 28}" height="26" rx="13" fill="#c9a96a" {S(6)}/>')
    out += "".join(f'<line x1="{w * 0.1}" y1="{h * (0.18 + i * 0.11)}" x2="{w * (0.9 - (i % 3) * 0.12)}" y2="{h * (0.18 + i * 0.11)}" '
                   f'stroke="#6a5030" stroke-width="5"/>' for i in range(lines))
    out += "".join(f'<circle cx="{w * (0.3 + 0.2 * k)}" cy="{h * 0.86}" r="20" fill="#a3182a" {S(5)}/>' for k in range(seals_))
    return out + "</g>"


def quill(x, y, s=1.0, rot=-30):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M0 0 Q40 -120 10 -240 Q-30 -120 0 0 Z" '
            f'fill="#f4ecd0" {S(5)}/><line x1="0" y1="10" x2="6" y2="-200" stroke="{INK}" stroke-width="4"/></g>')


def d20(x, y, s=1.0, c="#a3182a"):
    pts = [(math.cos(-math.pi / 2 + i * math.pi / 3) * 80, math.sin(-math.pi / 2 + i * math.pi / 3) * 80) for i in range(6)]
    poly = " ".join(f"{a:.0f},{b:.0f}" for a, b in pts)
    inner = "0,-50 44,26 -44,26"
    return (f'<g transform="translate({x},{y}) scale({s})"><polygon points="{poly}" fill="{c}" {S(6)}/>'
            f'<polygon points="{inner}" fill="#c0283a" {S(4)}/>'
            + "".join(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{[0, 44, 44, 0, -44, -44][i]}" y2="{[-50, 26, 26, 26, 26, -50][i] if i not in (3,) else 26}" stroke="{INK}" stroke-width="4"/>' for i in range(6))
            + f'<text x="0" y="16" font-family="Cinzel" font-weight="900" font-size="34" fill="{GOLD}" text-anchor="middle">20</text></g>')


def hourglass(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-60" y="-110" width="120" height="16" fill="{GOLD}" {S(5)}/>'
            f'<rect x="-60" y="94" width="120" height="16" fill="{GOLD}" {S(5)}/>'
            f'<path d="M-46 -94 L46 -94 L6 0 L46 94 L-46 94 L-6 0 Z" fill="#f4e6c8" opacity="0.8" {S(5)}/>'
            f'<path d="M-30 94 L30 94 L0 50 Z" fill="#c0283a"/><path d="M-26 -70 L26 -70 L4 -10 L-4 -10 Z" fill="#c0283a"/></g>')


def gears(x, y, r, teeth=10, c="#b8862e"):
    pts = []
    for i in range(teeth * 2):
        a = i * math.pi / teeth
        rr = r if i % 2 == 0 else r * 0.8
        pts.append(f"{x + rr * math.cos(a):.0f},{y + rr * math.sin(a):.0f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}" {S(6)}/><circle cx="{x}" cy="{y}" r="{r * 0.3}" fill="#3a2a14" {S(5)}/>'


def book(x, y, w=360, h=220, glyph=True):
    out = (f'<path d="M{x} {y} Q{x + w / 4} {y - 30} {x + w / 2} {y} Q{x + 3 * w / 4} {y - 30} {x + w} {y} L{x + w} {y + h} '
           f'Q{x + 3 * w / 4} {y + h - 30} {x + w / 2} {y + h} Q{x + w / 4} {y + h - 30} {x} {y + h} Z" fill="#f0dfb4" {S(7)}/>'
           f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="{INK}" stroke-width="5"/>')
    out += "".join(f'<line x1="{x + 24}" y1="{y + 40 + i * 28}" x2="{x + w / 2 - 24}" y2="{y + 40 + i * 28}" stroke="#6a5030" stroke-width="4"/>'
                   for i in range(5))
    if glyph:
        cx, cy = x + 3 * w / 4, y + h / 2
        out += (f'<circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="#a3182a" stroke-width="6"/>'
                f'<polygon points="{cx},{cy - 52} {cx + 45},{cy + 26} {cx - 45},{cy + 26}" fill="none" stroke="#a3182a" stroke-width="5"/>')
    return out


def frame(extra=""):
    return (f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="none" stroke="{GOLD}" stroke-width="5"/>'
            f'<rect x="20" y="20" width="{W - 40}" height="{H - 40}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.6"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{GOLD}" {S(3)}/>' for x in (8, W - 8) for y in (8, H - 8)) + extra)


def vignette():
    return ('<radialGradient id="vg" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0.65"/></radialGradient><rect width="{W}" height="{H}" fill="url(#vg)"/>')


# ------------------------------------------------------------------ pieces
def p_intro():
    return (skyg("#c0182e") + glow(800, 160, 320) + peaks(W, H, 430, 21, "#2a0608", spires=True)
            + lava(W, H, 470, 5) + peaks(W, H, 520, 22, "#070203") + crown(800, 210, 0.75) + seals(800, 160, 230, rs=26))


def p_run():
    clocks = ""
    for i, (x, c, f) in enumerate(((330, "#c0183a", 5), (800, "#b8862e", 3), (1270, "#5a3a8a", 6))):
        clocks += f'<circle cx="{x}" cy="190" r="110" fill="#1a0e10" {S(8)}/>'
        for k in range(8):
            a0, a1 = -math.pi / 2 + k * math.pi / 4, -math.pi / 2 + (k + 1) * math.pi / 4
            if k < f:
                clocks += (f'<path d="M{x} 190 L{x + 100 * math.cos(a0):.0f} {190 + 100 * math.sin(a0):.0f} '
                           f'A100 100 0 0 1 {x + 100 * math.cos(a1):.0f} {190 + 100 * math.sin(a1):.0f} Z" fill="{c}" {S(4)}/>')
        clocks += "".join(f'<line x1="{x}" y1="190" x2="{x + 100 * math.cos(-math.pi / 2 + k * math.pi / 4):.0f}" '
                          f'y2="{190 + 100 * math.sin(-math.pi / 2 + k * math.pi / 4):.0f}" stroke="{INK}" stroke-width="4"/>' for k in range(8))
    return (skyg("#7a3a14", "#2a1006") + glow(800, 200, 380, "#ffb43a", 0.18) + peaks(W, H, 470, 30, "#1a0806")
            + banner(120, 300, 140, "#2f7a46") + banner(1400, 300, 140, "#2c4f8a") + clocks
            + fig("brass-registrar", 560, 230, 0.33) + fig("claims-clerk", 820, 240, 0.32, flip=True))


def p_ch1():
    return (skyg("#d0301a") + glow(1150, 220, 300) + peaks(W, H, 380, 31, "#2a0608", spires=True)
            + gate(1150, 420) + lava(W, H, 430, 9) + bridge(150, 1000, 440)
            + fig("imp-tollkeeper", 420, 120, 0.3) + fig("skull-notary", 1250, 240, 0.28, flip=True) + embers(W, H, 140, 8))


def p_ch2():
    town = "".join(house(x, 430, w, h, sunk=s, lit=(i % 3 == 0)) for i, (x, w, h, s) in enumerate(
        ((60, 150, 180, 30), (260, 120, 230, 60), (420, 170, 160, 20), (980, 140, 210, 50), (1160, 180, 170, 30), (1380, 130, 240, 70))))
    lamp = "".join(f'<line x1="{x}" y1="300" x2="{x}" y2="470" stroke="{INK}" stroke-width="7"/><circle cx="{x}" cy="300" r="14" fill="#9ef0c8" {S(4)}/>'
                   f'<circle cx="{x}" cy="300" r="40" fill="#9ef0c8" opacity="0.35" filter="url(#glw)"/>' for x in (620, 900))
    return (skyg("#2a6a6a", "#0e2a30", "#03080a") + '<circle cx="1300" cy="120" r="60" fill="#d8f0e8" opacity="0.8"/>'
            + peaks(W, H, 330, 41, "#0a1a1e") + town + water(410, seed=4) + lamp
            + fig("janella-greenbottle", 600, 190, 0.32) + fig("greyhurst-survivor", 760, 200, 0.31, flip=True))


def p_ch3():
    stalls = "".join(f'<path d="M{x} 420 v-110 h170 v110" fill="#2a1418" {S(6)}/>'
                     f'<path d="M{x - 15} 310 l100 -60 l100 60 Z" fill="{c}" {S(6)}/>' for x, c in ((60, "#a3182a"), (1360, "#2c4f8a")))
    return (skyg("#8a1a3a", "#2a0614") + glow(800, 160, 300, "#ff4a6a", 0.18) + peaks(W, H, 400, 51, "#1a0408", spires=True) + stalls
            + banner(330, 120, 150, "#a3182a") + banner(1170, 120, 150, "#5a3a8a")
            + ledgers(470, 520, 6) + ledgers(1000, 520, 5, 9) + scroll(220, 330, 160, 170, -12, seals_=2)
            + fig("hollis-valrick", 560, 160, 0.36) + fig("spectral-clerk", 1220, 250, 0.27, flip=True) + quill(1440, 470, 0.8))


def p_ch4():
    return (skyg("#e05a14", "#5a1a06") + glow(800, 120, 300, "#ffd27a", 0.2) + arena(470)
            + fig("iron-heir", 380, 120, 0.38) + fig("masked-champion-living", 860, 130, 0.37, flip=True) + embers(W, H, 120, 12))


def p_ch5():
    moon = '<circle cx="800" cy="170" r="130" fill="#e8d0e8" opacity="0.9"/><circle cx="840" cy="150" r="120" fill="#3a0a2a" opacity="0.55"/>'
    return (skyg("#6a1a5a", "#2a0628", "#070206") + moon + peaks(W, H, 430, 61, "#12040e") + thorns(5)
            + fig("misty", 560, 90, 0.44) + fig("night-hag-advocate", 1080, 200, 0.32, flip=True) + fig("mother-sable", 120, 220, 0.3))


def p_ch6():
    return (skyg("#ff4a2a", "#5e0b18") + glow(800, 240, 360, "#ffd27a", 0.25) + peaks(W, H, 470, 71, "#1a0406", spires=True)
            + throne(800, 520, 0.95) + seals(800, 250, 250, rs=28)
            + fig("marshal-kordren", 60, 200, 0.32) + fig("isolde", 1220, 200, 0.32, flip=True))


def p_ref():
    candle = (f'<rect x="1180" y="300" width="50" height="160" fill="#f4ecd0" {S(5)}/><ellipse cx="1205" cy="285" rx="16" ry="28" fill="#ffd27a"/>'
              f'<circle cx="1205" cy="285" r="70" fill="#ffd27a" opacity="0.35" filter="url(#glw)"/>')
    return (skyg("#5a2a14", "#24100a") + f'<rect x="0" y="420" width="{W}" height="100" fill="#3a2414" {S(6)}/>'
            + book(520, 250, 440, 220) + d20(1020, 400, 0.8) + d20(1340, 430, 0.6, "#2c4f8a") + candle + hourglass(380, 330, 0.9)
            + fig("claims-clerk", 40, 200, 0.32))


def p_appA():
    keys = ["lemure", "imp-tollkeeper", "cadaver-collector", "contract-sentinel", "writ-bailiff", "styx-ferryman"]
    return (skyg("#a3182a") + peaks(W, H, 460, 81, "#1a0406", spires=True)
            + "".join(fig(k, 20 + i * 262, 210, 0.3, flip=i % 2 == 1) for i, k in enumerate(keys)))


def p_appB():
    return (skyg("#c86a14", "#3a1a06") + gears(260, 220, 150) + gears(470, 380, 100, 8, "#8a6a2a") + gears(1340, 250, 170, 12)
            + f'<rect x="0" y="440" width="{W}" height="80" fill="#c8a060" {S(6)}/>'
            + hourglass(800, 260, 1.4) + d20(1050, 400, 0.7) + d20(580, 410, 0.55, "#2c4f8a"))


def p_appC():
    return (skyg("#7a1a24", "#2a0a0e") + scroll(180, 120, 300, 300, -8, seals_=2) + scroll(600, 90, 380, 330, 3, 7, 3)
            + scroll(1120, 130, 300, 290, 9, seals_=1) + quill(1020, 470, 1.0, -20)
            + f'<rect x="980" y="430" width="80" height="60" rx="10" fill="#1a1012" {S(5)}/>')


def p_appD():
    pins = "".join(f'<circle cx="{x}" cy="{y}" r="14" fill="#c0183a" {S(4)}/>' for x, y in ((470, 210), (720, 330), (1010, 190), (1170, 340)))
    route = '<path d="M470 210 Q600 300 720 330 T1010 190 T1170 340" stroke="#a3182a" stroke-width="6" fill="none" stroke-dasharray="16 12"/>'
    rose_ = ("".join(f'<polygon points="0,-110 18,-18 0,0 -18,-18" fill="{GOLD if i % 2 == 0 else "#6a5030"}" {S(4)} transform="rotate({i * 90})"/>'
                     for i in range(4)))
    return (skyg("#4a3018", "#1a0e06") + f'<rect x="300" y="70" width="1000" height="400" fill="#efdcae" {S(8)}/>'
            + "".join(f'<line x1="{300 + i * 100}" y1="70" x2="{300 + i * 100}" y2="470" stroke="#c9b080" stroke-width="2"/>' for i in range(1, 10))
            + '<path d="M330 400 Q500 300 640 380 T980 300 T1280 360" stroke="#c87a3a" stroke-width="22" fill="none" opacity="0.6"/>'
            + route + pins + f'<g transform="translate(1180,170)">{rose_}</g>'
            + f'<rect x="270" y="56" width="30" height="430" rx="15" fill="#c9a96a" {S(6)}/><rect x="1300" y="56" width="30" height="430" rx="15" fill="#c9a96a" {S(6)}/>')


def p_appE():
    abacus = "".join(f'<line x1="1150" y1="{250 + i * 40}" x2="1450" y2="{250 + i * 40}" stroke="{INK}" stroke-width="5"/>'
                     + "".join(f'<circle cx="{1180 + k * 34 + (i * 17) % 60}" cy="{250 + i * 40}" r="15" fill="#a3182a" {S(3)}/>' for k in range(5))
                     for i in range(5))
    return (skyg("#3a2a3a", "#140a14") + book(380, 170, 640, 300, glyph=False)
            + "".join(f'<line x1="{720 + k * 60}" y1="200" x2="{720 + k * 60}" y2="440" stroke="#a3182a" stroke-width="3"/>' for k in range(5))
            + f'<rect x="1130" y="210" width="340" height="240" fill="none" {S(10)}/>' + abacus + quill(300, 470, 1.0, -15))


def p_appF():
    divider = (f'<g transform="translate(1180,120)"><line x1="0" y1="0" x2="-90" y2="320" {S(10)}/><line x1="0" y1="0" x2="90" y2="320" {S(10)}/>'
               f'<circle r="20" fill="{GOLD}" {S(5)}/></g>')
    sketch = ('<path d="M420 360 Q560 160 740 300 T1000 240" stroke="#6a5030" stroke-width="5" fill="none"/>'
              '<rect x="520" y="200" width="160" height="110" fill="none" stroke="#6a5030" stroke-width="4" stroke-dasharray="10 8"/>')
    return (skyg("#2a3a5a", "#0e1424") + f'<polygon points="200,470 1400,470 1300,90 300,90" fill="#efdcae" {S(8)}/>' + sketch
            + f'<rect x="330" y="420" width="700" height="30" fill="{GOLD}" {S(5)}/>'
            + "".join(f'<line x1="{340 + k * 35}" y1="420" x2="{340 + k * 35}" y2="{435 if k % 2 else 445}" stroke="{INK}" stroke-width="3"/>' for k in range(20))
            + divider + fig("brass-registrar", 20, 230, 0.28))


PCS = ["pc-aurelia", "pc-varka", "pc-ilyra", "pc-orren", "pc-caldris", "pc-nema"]


def p_pintro():
    return (skyg("#c0182e") + glow(800, 200, 340) + peaks(W, H, 470, 91, "#2a0608", spires=True) + lava(W, H, 490, 4)
            + scroll(560, 120, 480, 300, 0, 7, 3) + crown(800, 90, 0.35) + seals(800, 260, 360, rs=22))


def p_pheroes():
    return (skyg("#b0201e") + glow(800, 180, 360) + peaks(W, H, 440, 93, "#2a0608", spires=True)
            + "".join(fig(k, 10 + i * 262, 200, 0.31, flip=i >= 3) for i, k in enumerate(PCS)))


def p_popts():
    warden = (f'<g transform="translate(1400,230)"><path d="M-50 60 Q-70 -60 0 -110 Q70 -60 50 60 Q0 100 -50 60 Z" fill="#6a6a6a" '
              f'opacity="0.85" {S(6)}/><circle cx="-18" cy="-40" r="10" fill="#ffb43a"/><circle cx="18" cy="-40" r="10" fill="#ffb43a"/>'
              f'<circle r="120" fill="#ff7a1a" opacity="0.2" filter="url(#glw2)"/></g>')
    return (skyg("#7a1a2a", "#2a0610") + glow(260, 220, 220, "#c0183a", 0.3) + glow(800, 220, 220, "#a3182a", 0.25)
            + glow(1300, 220, 220, "#5a8a3a", 0.25) + thorns(9, H, 6)
            + fig("pc-aurelia", 60, 180, 0.34) + fig("pc-varka", 580, 170, 0.35) + fig("pc-ilyra", 1050, 180, 0.34, flip=True) + warden)


def p_pspells():
    runes = "".join(f'<text x="{x}" y="{y}" font-family="Cinzel" font-weight="900" font-size="{s}" fill="#ffb43a" opacity="0.8">{t}</text>'
                    for x, y, s, t in ((260, 160, 60, "§"), (420, 90, 44, "Ⅸ"), (1160, 120, 56, "✦"), (1340, 200, 48, "§"),
                                       (560, 210, 40, "✠"), (1040, 230, 40, "Ⅲ")))
    circle = ('<circle cx="800" cy="210" r="170" fill="none" stroke="#ff7a1a" stroke-width="6" opacity="0.8"/>'
              '<circle cx="800" cy="210" r="130" fill="none" stroke="#ffd27a" stroke-width="3" stroke-dasharray="12 8"/>'
              + "".join(f'<line x1="{800 + 170 * math.cos(a):.0f}" y1="{210 + 170 * math.sin(a):.0f}" x2="{800 + 170 * math.cos(a + 2.4):.0f}" '
                        f'y2="{210 + 170 * math.sin(a + 2.4):.0f}" stroke="#ff7a1a" stroke-width="4" opacity="0.7"/>' for a in [i * 2.4 for i in range(5)]))
    return (skyg("#4a1a6a", "#1a0628") + glow(800, 210, 260, "#ff7a1a", 0.3) + circle + runes
            + f'<rect x="0" y="440" width="{W}" height="80" fill="#2a1418" {S(6)}/>' + book(580, 330, 440, 150))


def p_prelics():
    ped = "".join(f'<rect x="{x - 90}" y="330" width="180" height="140" fill="#3a2a2a" {S(7)}/><rect x="{x - 110}" y="310" width="220" height="30" fill="#5a3a3a" {S(6)}/>'
                  f'<circle cx="{x}" cy="230" r="90" fill="#ffd27a" opacity="0.2" filter="url(#glw)"/>' for x in (330, 800, 1270))
    dome = f'<path d="M1190 310 v-110 a80 80 0 0 1 160 0 v110" fill="#cfe8f0" opacity="0.35" {S(6)}/>'
    gaunt = (f'<path d="M760 300 v-90 q0 -20 16 -20 v-40 q0 -12 12 -12 q12 0 12 12 v40 v-50 q0 -12 12 -12 q12 0 12 12 v60 q16 -10 22 10 v90 Z" '
             f'fill="#8a8a96" {S(6)}/>')
    marks = "".join(f'<circle cx="{280 + k * 50}" cy="290" r="22" fill="{GOLD}" {S(5)}/><polygon points="{268 + k * 50},290 {280 + k * 50},274 {292 + k * 50},290" fill="#a3182a"/>' for k in range(3))
    return (skyg("#5e0b18", "#1a0406") + ped + marks + gaunt + rose(1270, 250, 1.6) + dome + embers(W, H, 80, 15))


def p_pho():
    return (skyg("#8a2a14", "#2a0a06") + glow(800, 260, 300, "#ffb43a", 0.18) + scroll(560, 70, 480, 380, 0, 8, 0)
            + "".join(f'<circle cx="{620 + (k % 4) * 120}" cy="{390 + (k // 4) * 50}" r="20" fill="#a3182a" {S(5)}/>' for k in range(8))
            + quill(1150, 470, 1.2, -25) + scroll(150, 150, 260, 260, -10, seals_=1) + scroll(1250, 170, 240, 240, 12, seals_=1))


def p_prules():
    scales = (f'<g transform="translate(800,80)"><line x1="0" y1="0" x2="0" y2="360" {S(10)}/><line x1="-260" y1="60" x2="260" y2="20" {S(9)}/>'
              f'<path d="M-330 200 Q-260 250 -190 200 Z" fill="{GOLD}" {S(6)}/><line x1="-260" y1="60" x2="-320" y2="200" stroke="{INK}" stroke-width="4"/>'
              f'<line x1="-260" y1="60" x2="-200" y2="200" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M190 160 Q260 210 330 160 Z" fill="{GOLD}" {S(6)}/><line x1="260" y1="20" x2="200" y2="160" stroke="{INK}" stroke-width="4"/>'
              f'<line x1="260" y1="20" x2="320" y2="160" stroke="{INK}" stroke-width="4"/><rect x="-80" y="360" width="160" height="40" fill="{GOLD}" {S(6)}/></g>')
    return (skyg("#2c3a6a", "#0e1228") + glow(800, 200, 300, "#ffd27a", 0.15) + scales + d20(1060, 220, 0.5) + d20(540, 250, 0.5, "#2c4f8a")
            + hourglass(260, 330, 1.0) + crown(1360, 360, 0.35))


PIECES = {"intro": p_intro, "run": p_run, "ch1": p_ch1, "ch2": p_ch2, "ch3": p_ch3, "ch4": p_ch4, "ch5": p_ch5, "ch6": p_ch6,
          "ref": p_ref, "appA": p_appA, "appB": p_appB, "appC": p_appC, "appF": p_appD, "appE": p_appE, "appH": p_appF,
          "pintro": p_pintro, "pheroes": p_pheroes, "popts": p_popts, "pspells": p_pspells, "prelics": p_prelics,
          "pho": p_pho, "prules": p_prules}


def _side(key, x, y, s, flip=False):
    import vehicles as V
    g = {"quad": V.side_quad("#c2410c"), "spiker": V.side_quad("#2a2226", True), "hauler": V.side_hauler(),
         "reclaimer": V.side_reclaimer()}[key]
    fx = " translate(1000,0) scale(-1,1)" if flip else ""
    return f'<g transform="translate({x},{y}) scale({s}){fx}">{g}</g>'


def claws_band(y, flip=False, seed=3, lo=90, hi=190):
    r = random.Random(seed)
    out = ""
    for x in range(-40, W + 80, 110):
        h = r.randint(lo, hi)
        tip = y + (h if flip else -h)
        out += (f'<path d="M{x} {y} Q{x + 30} {(y + tip) / 2} {x + 55 + r.randint(-20, 20)} {tip} Q{x + 70} {(y + tip) / 2} {x + 110} {y} Z" '
                f'fill="#a3182a" {S(6)}/>')
    return out


def p_interlude():
    dust = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.4}" fill="#5a3a2a" opacity="0.35"/>'
                   for x, y, rx in ((300, 430, 160), (520, 440, 120), (1000, 420, 200), (1300, 450, 150)))
    return (skyg("#ff5a1a", "#5e0b18") + glow(800, 120, 340, "#ffd27a", 0.25)
            + f'<rect x="0" y="0" width="{W}" height="120" fill="#2a0608"/>' + claws_band(120, True, 4)
            + f'<rect x="0" y="330" width="{W}" height="190" fill="#3a1a12"/>' + dust + claws_band(530, False, 7, 50, 100)
            + _side("reclaimer", -40, 70, 0.42) + _side("spiker", 300, 170, 0.3)
            + _side("hauler", 880, 90, 0.4) + _side("quad", 1240, 180, 0.28)
            + '<path d="M420 250 Q700 160 960 250" stroke="#8a8f99" stroke-width="6" fill="none" stroke-dasharray="14 8"/>'
            + embers(W, H, 120, 21))


def p_pfurnace():
    coins = "".join(f'<g transform="translate({x},{y}) scale({sc})"><circle r="60" fill="#5a4a4a" {S(6)}/><circle r="34" fill="{c}" {S(4)}/>'
                    f'<circle cx="-10" cy="-6" r="5" fill="#1a2a2e"/><circle cx="10" cy="-6" r="5" fill="#1a2a2e"/><ellipse cy="12" rx="7" ry="9" fill="#1a2a2e"/></g>'
                    for x, y, sc, c in ((260, 380, 1.1, "#5ad0e0"), (400, 430, 0.9, "#ffd27a"), (1200, 400, 1.0, "#ff5a3a"),
                                        (1340, 350, 0.8, "#5ad0e0"), (180, 250, 0.7, "#ffd27a"), (1420, 230, 0.7, "#5ad0e0")))
    import vehicles as V
    furn = f'<g transform="translate(800,270) scale(2.2) translate(-800,-270)">{V.furnace(800, 270, 220, 150, "#5ad0e0")}</g>'
    return (skyg("#1a6a6a", "#0a2a30", "#030a0c") + glow(800, 270, 340, "#5ad0e0", 0.3) + furn
            + f'<rect x="0" y="460" width="{W}" height="60" fill="#2a1418" {S(6)}/>' + coins
            + "".join(f'<path d="M{x} 120 q20 -40 0 -80" stroke="#cfeff2" stroke-width="5" fill="none" opacity="0.6"/>' for x in (620, 720, 880, 980)))


PIECES["interlude"] = p_interlude
PIECES["pfurnace"] = p_pfurnace


def thanks_page(out, names=()):
    """Full-page art for the closing thanks (used to keep printed books at an even page count)."""
    TW, TH = 1700, 2200
    import vehicles as V
    def shield(cx, cy, title, col, glyph):
        return (f'<g transform="translate({cx},{cy})"><path d="M-170 -200 H170 V40 Q170 170 0 230 Q-170 170 -170 40 Z" fill="{col}" '
                f'stroke="{INK}" stroke-width="12"/><path d="M-140 -170 H140 V40 Q140 140 0 195 Q-140 140 -140 40 Z" fill="none" '
                f'stroke="{GOLD}" stroke-width="6"/>{glyph}'
                f'<rect x="-230" y="250" width="460" height="80" rx="12" fill="#1a0a0c" stroke="{GOLD}" stroke-width="5"/>'
                f'<text y="304" font-family="Cinzel" font-weight="900" font-size="38" fill="#f3d48a" text-anchor="middle">{title}</text></g>')
    pp = (f'<polygon points="0,-110 95,-55 95,55 0,110 -95,55 -95,-55" fill="#a3182a" stroke="{INK}" stroke-width="8"/>'
          f'<text y="22" font-family="Cinzel Decorative" font-weight="900" font-size="64" fill="{GOLD}" text-anchor="middle">P&amp;P</text>')
    ba = ("".join(f'<path d="M{-120 + i * 10} {-70 + i * 50} q60 -50 120 0 t120 0" stroke="#cfeff2" stroke-width="16" fill="none" '
                  f'stroke-linecap="round"/>' for i in range(3)))
    im = (f'<circle r="100" fill="#2c4f8a" stroke="{INK}" stroke-width="8"/><path d="M-60 40 L0 -70 L60 40 Z" fill="#f3d48a" '
          f'stroke="{INK}" stroke-width="6"/><circle cy="-80" r="18" fill="#ffd27a"/>')
    if names:
        names = [" · ".join(names)]
    lines = list(names) or ["Every player who crossed the first lava river, argued the first appeal,",
                            "and signed (or refused to sign) the first contract."]
    body = "".join(f'<text x="{TW / 2}" y="{1760 + i * 62}" font-family="IM FELL English" font-style="italic" font-size="46" '
                   f'fill="#f4dcc0" text-anchor="middle">{l}</text>' for i, l in enumerate(lines[:6]))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TW} {TH}" width="{TW}" height="{TH}">{DEFS}'
           f'<radialGradient id="tk" cx="0.5" cy="0.35" r="0.9"><stop offset="0" stop-color="#c0182e"/><stop offset="0.55" stop-color="#3a0610"/>'
           f'<stop offset="1" stop-color="#070203"/></radialGradient><rect width="{TW}" height="{TH}" fill="url(#tk)"/>'
           + f'<circle cx="{TW / 2}" cy="760" r="520" fill="#ff7a1a" opacity="0.15" filter="url(#glw2)"/>'
           + f'<g transform="translate(0,1150)">{peaks(TW, 1050, 520, 31, "#2a0608", spires=True)}</g>'
           + f'<rect x="0" y="1340" width="{TW}" height="{TH - 1340}" fill="#070203" opacity="0.72"/>'
           + crown(TW / 2, 330, 0.8)
           + f'<text x="{TW / 2}" y="220" font-family="Cinzel Decorative" font-weight="900" font-size="120" fill="#f3d48a" '
             f'stroke="{INK}" stroke-width="10" paint-order="stroke" text-anchor="middle">With Thanks</text>'
           + shield(TW / 2 - 520, 800, "PACTS &amp; POLYHEDRALS", "#5e0b18", pp)
           + shield(TW / 2, 760, "BLOWN AWAY", "#1a3a4a", ba)
           + shield(TW / 2 + 520, 800, "IMAGI-NATIONS", "#2a2a5a", im)
           + f'<text x="{TW / 2}" y="1420" font-family="IM FELL English" font-size="52" fill="#f4dcc0" text-anchor="middle">'
             f'To the Pacts &amp; Polyhedrals, Blown Away and Imagi-Nations Discord servers,</text>'
           + f'<text x="{TW / 2}" y="1490" font-family="IM FELL English" font-size="52" fill="#f4dcc0" text-anchor="middle">'
             f'and to our playtesters, who were here first.</text>'
           + f'<text x="{TW / 2}" y="1660" font-family="Cinzel" font-weight="700" font-size="40" fill="{GOLD}" letter-spacing="6" '
             f'text-anchor="middle">THE PLAYTESTERS</text>' + body
           + embers(TW, TH, 260, 33)
           + f'<text x="{TW / 2}" y="2120" font-family="Cinzel" font-weight="700" font-size="34" fill="{GOLD}" letter-spacing="4" '
             f'text-anchor="middle">ASMO, PACTS &amp; POLYHEDRALS (BEN VALE)</text>'
           + f'<rect x="28" y="28" width="{TW - 56}" height="{TH - 56}" fill="none" stroke="{GOLD}" stroke-width="6" opacity="0.75"/></svg>')
    im_ = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS])))).convert("RGB")
    im_.save(out, "JPEG", quality=90)
    return im_


def render(key):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}'
           f'<clipPath id="cl"><rect x="8" y="8" width="{W - 16}" height="{H - 16}"/></clipPath>'
           f'<g clip-path="url(#cl)">{PIECES[key]()}{vignette()}</g>{frame()}</svg>')
    im = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS])))).convert("RGB")
    os.makedirs(OUT, exist_ok=True)
    im.save(f"{OUT}/{key}.webp", "WEBP", quality=84)
    return im


if __name__ == "__main__":
    if sys.argv[1:2] == ["thanks"]:
        thanks_page("/home/claude/ic/dist/thanks-page.jpg"); print("thanks"); sys.exit()
    keys = sys.argv[1:] or list(PIECES)
    for k in keys:
        render(k)
    print(len(keys), "chapter pieces")
