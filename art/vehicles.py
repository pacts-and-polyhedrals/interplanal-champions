"""Infernal war machines for the Redline Run: side-view portraits, true-overhead tokens, and the soul-coin icons."""
import math, os, random
from chibi import DEFS, S, INK, render, bg, frame

OUT = "/home/claude/ic/module/assets"


def wheel(cx, cy, r, spikes=True, c="#2a2226"):
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" {S(10)}/><circle cx="{cx}" cy="{cy}" r="{r * 0.55}" fill="#4a4048" {S(7)}/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{r * 0.2}" fill="url(#brass)" {S(5)}/>'
    if spikes:
        for i in range(10):
            a = i * math.pi / 5
            x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
            x2, y2 = cx + (r + 26) * math.cos(a + 0.12), cy + (r + 26) * math.sin(a + 0.12)
            out += f'<polygon points="{x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f} {cx + r * math.cos(a + 0.3):.0f},{cy + r * math.sin(a + 0.3):.0f}" fill="#8a8f99" {S(5)}/>'
    return out


def furnace(cx, cy, w, h, soul="#5ad0e0"):
    bars = "".join(f'<line x1="{cx - w / 2 + i * w / 6:.0f}" y1="{cy - h / 2}" x2="{cx - w / 2 + i * w / 6:.0f}" y2="{cy + h / 2}" stroke="{INK}" stroke-width="8"/>'
                   for i in range(1, 6))
    faces = "".join(f'<ellipse cx="{cx - w * 0.25 + i * w * 0.25:.0f}" cy="{cy}" rx="{w * 0.07:.0f}" ry="{h * 0.16:.0f}" fill="#1a2a2e" opacity="0.6"/>'
                    for i in range(3))
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{w * 0.7}" ry="{h * 0.8}" fill="{soul}" opacity="0.45" filter="url(#glw)"/>'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="18" fill="{soul}" {S(10)}/>{faces}{bars}')


def exhaust(x, y, n=3):
    return "".join(f'<rect x="{x + i * 46}" y="{y - 130 + i * 20}" width="30" height="{130 - i * 20}" fill="#3a3640" {S(7)}/>'
                   f'<ellipse cx="{x + 15 + i * 46}" cy="{y - 150 + i * 20}" rx="34" ry="44" fill="#ff7a1a" opacity="0.8" filter="url(#glw)"/>'
                   f'<path d="M{x + i * 46} {y - 132 + i * 20} q15 -60 30 0" fill="#ffd27a" {S(4)}/>' for i in range(n))


# ---------------------------------------------------------------- side views (1000x1000)
def side_quad(body="#c2410c", blades=False):
    out = (f'<path d="M170 560 L260 470 L520 450 L640 380 L780 400 L840 520 L830 600 L180 620 Z" fill="{body}" {S(12)}/>'
           f'<path d="M260 470 L520 450 L560 520 L250 540 Z" fill="#1a1418" {S(8)}/>'
           f'<rect x="560" y="470" width="200" height="90" rx="14" fill="#3a3640" {S(9)}/>'
           + furnace(660, 515, 150, 70, "#ff9a3a") + exhaust(300, 470, 2)
           + f'<path d="M640 380 L700 300 L760 300" fill="none" stroke="{INK}" stroke-width="22"/><path d="M640 380 L700 300 L760 300" fill="none" stroke="#8a8f99" stroke-width="10"/>'
           + wheel(280, 640, 110) + wheel(740, 640, 110))
    if blades:
        out += "".join(f'<path d="M{x} 600 l70 -40 l-10 80 Z" fill="#c9cfd8" {S(6)}/>' for x in (390, 470, 550))
        out += f'<path d="M830 520 L930 470 L900 560 Z" fill="#c9cfd8" {S(8)}/>'
    else:
        out += f'<path d="M840 520 L920 500 L920 560 L830 580 Z" fill="#3a3640" {S(8)}/>'
    return out


def side_hauler():
    plates = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {S(8)}/>' + "".join(
        f'<circle cx="{x + 14 + k * (w - 28) / 3:.0f}" cy="{y + 14}" r="6" fill="#8a8f99"/>' for k in range(4))
        for x, y, w, h, c in ((120, 420, 260, 200, "#5a5a4a"), (380, 400, 240, 220, "#6a5a3a"), (620, 430, 230, 190, "#4a5a5a")))
    return (plates + furnace(500, 470, 180, 110, "#5ad0e0") + exhaust(160, 420, 3)
            + f'<path d="M850 440 L950 500 L950 600 L850 620 Z" fill="#3a3640" {S(9)}/>'
            + "".join(f'<line x1="870" y1="{470 + i * 30}" x2="940" y2="{500 + i * 25}" stroke="#c9cfd8" stroke-width="8"/>' for i in range(4))
            + f'<path d="M660 400 L760 300 L830 300" fill="none" stroke="{INK}" stroke-width="24"/><path d="M830 300 l40 -20 l0 40 Z" fill="#c9cfd8" {S(5)}/>'
            + f'<rect x="380" y="360" width="90" height="44" fill="#8e1424" {S(6)}/>'
            + wheel(230, 650, 110, False, "#3a3036") + wheel(500, 660, 110, False, "#3a3036") + wheel(760, 650, 110, False, "#3a3036"))


def side_reclaimer():
    books = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}" {S(8)}/><line x1="{x + 10}" y1="{y + h / 2}" x2="{x + w - 10}" y2="{y + h / 2}" stroke="#d8aa52" stroke-width="6"/>'
                    for x, y, w, h, c in ((90, 380, 300, 70, "#1a1418"), (90, 450, 300, 80, "#2a1a20"), (90, 530, 300, 90, "#1a1418"),
                                          (390, 360, 280, 90, "#2a1a20"), (390, 450, 280, 170, "#1a1418")))
    plow = (f'<path d="M670 380 L900 430 L960 620 L670 640 Z" fill="#3a3640" {S(10)}/>'
            + "".join(f'<polygon points="{720 + i * 50},{640} {745 + i * 50},{700} {770 + i * 50},{640}" fill="#c9cfd8" {S(5)}/>' for i in range(5))
            + "".join(f'<rect x="{700 + i * 70}" y="{450 + (i % 2) * 40}" width="56" height="70" fill="#f0dfb4" {S(4)} transform="rotate({-8 + i * 6} {728 + i * 70} {485})"/>' for i in range(3)))
    return (books + plow + furnace(530, 400, 150, 90, "#ffd27a") + exhaust(120, 380, 3)
            + f'<path d="M260 380 L330 270 L420 270" fill="none" stroke="{INK}" stroke-width="26"/><circle cx="420" cy="270" r="26" fill="url(#brass)" {S(6)}/>'
            + wheel(200, 660, 120) + wheel(470, 670, 120) + wheel(740, 660, 120))


# ---------------------------------------------------------------- overhead tokens (1000x1000)
def top_quad(body="#c2410c", blades=False):
    out = '<ellipse cx="500" cy="520" rx="300" ry="440" fill="#000" opacity="0.35" filter="url(#glw)"/>'
    out += "".join(f'<rect x="{x}" y="{y}" width="110" height="200" rx="30" fill="#2a2226" {S(10)}/>' for x in (230, 660) for y in (160, 640))
    out += (f'<path d="M330 120 L670 120 L720 420 L700 880 L300 880 L280 420 Z" fill="{body}" {S(12)}/>'
            f'<rect x="400" y="480" width="200" height="260" rx="20" fill="#3a3640" {S(9)}/>' + furnace(500, 300, 220, 120, "#ff9a3a")
            + f'<circle cx="500" cy="600" r="70" fill="#1a1418" {S(8)}/><path d="M380 180 L620 180" stroke="#8a8f99" stroke-width="20"/>')
    if blades:
        out += "".join(f'<path d="M{x} {y} l{d * 120} 30 l{-d * 120} 30 Z" fill="#c9cfd8" {S(6)}/>' for x, d in ((700, 1), (300, -1)) for y in (440, 560))
    return out


def top_hauler():
    out = '<ellipse cx="500" cy="510" rx="340" ry="470" fill="#000" opacity="0.35" filter="url(#glw)"/>'
    out += "".join(f'<rect x="{x}" y="{y}" width="90" height="170" rx="24" fill="#3a3036" {S(10)}/>' for x in (180, 730) for y in (110, 420, 720))
    out += (f'<rect x="250" y="60" width="500" height="880" rx="40" fill="#5a5a4a" {S(12)}/>'
            f'<rect x="290" y="110" width="420" height="230" fill="#4a5a5a" {S(8)}/>' + furnace(500, 480, 260, 170, "#5ad0e0")
            + f'<rect x="300" y="640" width="400" height="260" fill="#6a5a3a" {S(8)}/>'
            + "".join(f'<circle cx="{330 + k * 85}" cy="{690 + j * 90}" r="10" fill="#8a8f99"/>' for k in range(5) for j in range(3))
            + f'<path d="M420 40 L580 40 L560 80 L440 80 Z" fill="#c9cfd8" {S(7)}/>')
    return out


def top_reclaimer():
    out = '<ellipse cx="500" cy="510" rx="360" ry="480" fill="#000" opacity="0.35" filter="url(#glw)"/>'
    out += "".join(f'<rect x="{x}" y="{y}" width="100" height="180" rx="26" fill="#2a2226" {S(10)}/>' for x in (150, 750) for y in (180, 480, 760))
    out += (f'<path d="M180 120 L820 120 L760 30 L240 30 Z" fill="#3a3640" {S(10)}/>'
            + "".join(f'<polygon points="{230 + i * 90},30 {275 + i * 90},-30 {320 + i * 90},30" fill="#c9cfd8" {S(5)}/>' for i in range(6))
            + f'<rect x="230" y="120" width="540" height="840" rx="20" fill="#1a1418" {S(12)}/>'
            + "".join(f'<line x1="250" y1="{200 + i * 90}" x2="750" y2="{200 + i * 90}" stroke="#d8aa52" stroke-width="6"/>' for i in range(8))
            + furnace(500, 460, 240, 150, "#ffd27a")
            + f'<rect x="380" y="700" width="240" height="180" fill="#2a1a20" {S(8)}/><circle cx="500" cy="790" r="50" fill="#8e1424" {S(7)}/>')
    return out


VEHICLES = {
    "scorchhound-quad": (side_quad("#c2410c"), top_quad("#c2410c"), "#3a1406", 2),
    "cinderfang-spiker": (side_quad("#2a2226", True), top_quad("#2a2226", True), "#2a0a10", 2),
    "souljack-hauler": (side_hauler(), top_hauler(), "#1a2a2a", 3),
    "iron-reclaimer": (side_reclaimer(), top_reclaimer(), "#2a0a10", 3),
}


def coin_icon(glow="#5ad0e0", seal=None):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">' + DEFS
         + f'<circle cx="500" cy="500" r="420" fill="{glow}" opacity="0.35" filter="url(#glw2)"/>'
         + f'<circle cx="500" cy="500" r="360" fill="#5a4a4a" {S(22)}/><circle cx="500" cy="500" r="300" fill="#7a6a6a" {S(12)}/>'
         + f'<circle cx="500" cy="500" r="190" fill="{glow}" opacity="0.85" {S(12)}/>'
         + '<ellipse cx="450" cy="470" rx="34" ry="44" fill="#1a2a2e"/><ellipse cx="550" cy="470" rx="34" ry="44" fill="#1a2a2e"/>'
         + '<ellipse cx="500" cy="580" rx="50" ry="62" fill="#1a2a2e"/>'
         + "".join(f'<path d="M{500 + 330 * math.cos(a):.0f} {500 + 330 * math.sin(a):.0f} l{18 * math.cos(a + 1.6):.0f} {18 * math.sin(a + 1.6):.0f}" stroke="{INK}" stroke-width="12"/>'
                   for a in [i * math.pi / 9 for i in range(18)])
         + (f'<rect x="560" y="660" width="300" height="130" rx="16" fill="#1a1418" {S(10)}/><text x="710" y="748" font-family="Cinzel" '
            f'font-weight="900" font-size="74" fill="#d8aa52" text-anchor="middle">{seal}</text>' if seal else "") + "</svg>")
    return s


def build():
    os.makedirs(f"{OUT}/portraits", exist_ok=True)
    for key, (side, top, bgc, _) in VEHICLES.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">{DEFS}'
               f'{bg(bgc, hash(key) & 255)}<rect x="0" y="760" width="1000" height="240" fill="#2a1410" opacity="0.8"/><g transform="translate(-90,-170) scale(1.18)">{side}</g>{frame()}</svg>')
        render(svg, f"{OUT}/portraits/{key}.webp", 768)
        render(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">{DEFS}{top}</svg>',
               f"{OUT}/tokens/{key}.webp", 400)
    render(coin_icon(), f"{OUT}/icons/ic-soul-coin.webp", 256)
    render(coin_icon("#ff5a3a", "MIST"), f"{OUT}/icons/ic-soul-coin-mist.webp", 256)
    render(coin_icon("#ffd27a"), f"{OUT}/icons/ic-soul-coin-gold.webp", 256)


if __name__ == "__main__":
    build()
    print(len(VEHICLES), "vehicles")
