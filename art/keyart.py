"""Title card, journal banner and DMs Guild covers for Interplanal Champions."""
import random, math, io, os, textwrap
from chibi import DEFS, humanoid, INK, FONTS
from cast import CAST
import resvg_py
from PIL import Image

OUT = "/home/claude/ic/module/assets/art"
DIST = "/home/claude/ic/dist"


def peaks(w, h, base, seed=3, color="#0a0406", spires=False):
    r = random.Random(seed)
    pts = [f"0,{h}"]
    x = 0
    while x < w:
        bw = r.randint(60, 200)
        pts.append(f"{x},{base - r.randint(20, 140)}")
        if spires and r.random() < 0.25:
            pts += [f"{x + bw * 0.4:.0f},{base - r.randint(220, 420)}", f"{x + bw * 0.5:.0f},{base - r.randint(150, 230)}"]
        x += bw
    pts += [f"{w},{base - 40}", f"{w},{h}"]
    return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'


def embers(w, h, n, seed=1):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,w):.0f}" cy="{r.uniform(0,h):.0f}" r="{r.uniform(1.5,5):.1f}" '
                   f'fill="{r.choice(["#ffb43a", "#ff7a1a", "#ffd27a"])}" opacity="{r.uniform(0.3,0.9):.2f}"/>' for _ in range(n))


def lava(w, h, y0, seed=2):
    r = random.Random(seed)
    d = f"M0 {y0} " + " ".join(f"Q{x + 60} {y0 + r.randint(-40, 40)} {x + 120} {y0 + r.randint(-20, 20)}" for x in range(0, w, 120))
    return (f'<path d="{d} L{w} {h} L0 {h} Z" fill="#ff5a0a" opacity="0.85"/>'
            f'<path d="{d}" stroke="#ffe27a" stroke-width="10" fill="none" opacity="0.7"/>')


def crown(cx, cy, s=1.0, col="#d8aa52"):
    pts = []
    for i in range(19):
        x = -180 + i * 20
        y = -150 if i % 2 else -40
        if i in (0, 18):
            y = 0
        pts.append(f"{x},{y}")
    return (f'<g transform="translate({cx},{cy}) scale({s})"><polygon points="-180,40 {" ".join(pts)} 180,40" fill="{col}" '
            f'stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{-120 + k * 80}" cy="0" r="18" fill="#c0183a" stroke="{INK}" stroke-width="6"/>' for k in range(4)) + "</g>")


def sky(id_, c1="#c0182e"):
    return (f'<radialGradient id="{id_}" cx="0.5" cy="0.4" r="0.9"><stop offset="0" stop-color="{c1}"/>'
            '<stop offset="0.5" stop-color="#4a0610"/><stop offset="1" stop-color="#070203"/></radialGradient>')


def title():
    W, H = 1920, 1080
    misty = humanoid(CAST["misty"][0])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}{sky("sky")}'
           f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
           '<circle cx="1380" cy="380" r="320" fill="#ff7a1a" opacity="0.2" filter="url(#glw2)"/>'
           + peaks(W, H, 820, 5, "#2a0608", spires=True) + lava(W, H, 900, 3) + peaks(W, H, 1010, 9, "#070203")
           + crown(1380, 140, 0.7)
           + f'<g transform="translate(1000,120) scale(0.85)">{misty}</g>'
           + embers(W, H, 300, 2)
           + f'<text x="90" y="290" font-family="Cinzel" font-weight="700" font-size="40" fill="#ffb38a" letter-spacing="10">INTEREST OF ASMODEUS</text>'
           + f'<text x="80" y="450" font-family="Cinzel Decorative" font-weight="900" font-size="128" fill="#f3d48a" stroke="{INK}" stroke-width="10" paint-order="stroke">Interplanal</text>'
           + f'<text x="80" y="610" font-family="Cinzel Decorative" font-weight="900" font-size="128" fill="#f3d48a" stroke="{INK}" stroke-width="10" paint-order="stroke">Champions</text>'
           + f'<text x="90" y="700" font-family="IM FELL English" font-style="italic" font-size="42" fill="#f4dcc0">The Throne of Avernus · A campaign of infernal succession · Levels 12–17</text>'
           + f'<text x="90" y="1030" font-family="Cinzel" font-weight="700" font-size="28" fill="#d8aa52" letter-spacing="4">ASMO, PACTS &amp; POLYHEDRALS (BEN VALE)</text>'
           + f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#d8aa52" stroke-width="4" opacity="0.7"/></svg>')
    im = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS])))).convert("RGB")
    im.save(f"{OUT}/title.webp", "WEBP", quality=84)
    t = im.copy(); t.thumbnail((400, 400)); t.save(f"{OUT}/cover-thumb.webp", "WEBP", quality=80)


def banner():
    W, H = 1600, 260
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}'
           '<linearGradient id="bn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e0b18"/><stop offset="1" stop-color="#140406"/></linearGradient>'
           f'<rect width="{W}" height="{H}" fill="url(#bn)"/>' + peaks(W, H, 230, 7, "#0a0204", spires=True) + embers(W, H, 140, 4)
           + "".join(crown(x, 70, 0.18) for x in range(80, W, 200))
           + f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="#d8aa52" stroke-width="3" opacity="0.6"/></svg>')
    Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS])))).convert("RGB").save(f"{OUT}/banner.webp", "WEBP", quality=80)


def cover(W=1700, H=2200, out="cover", sub="A Campaign of Infernal Succession", band=None, hero="misty", line="FOR CHARACTERS OF 12TH–17TH LEVEL · AVERNUS"):
    fig = humanoid(CAST[hero][0])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}{sky("sky")}'
           f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
           f'<circle cx="{W/2}" cy="1050" r="560" fill="#ff7a1a" opacity="0.18" filter="url(#glw2)"/>'
           + peaks(W, H, 1780, 11, "#2a0608", spires=True) + lava(W, H, 1880, 7) + peaks(W, H, 2020, 13, "#070203")
           + crown(W / 2, 640, 0.9)
           + f'<g transform="translate(160,600) scale(1.38)">{fig}</g>'
           + f'<rect y="{H-330}" width="{W}" height="330" fill="#070203" opacity="0.72"/>'
           + embers(W, H, 460, 6)
           + f'<text x="{W/2}" y="170" font-family="Cinzel" font-weight="700" font-size="56" fill="#ffb38a" letter-spacing="14" text-anchor="middle">INTEREST OF ASMODEUS</text>'
           + f'<text x="{W/2}" y="340" font-family="Cinzel Decorative" font-weight="900" font-size="170" fill="#f3d48a" stroke="{INK}" stroke-width="12" paint-order="stroke" text-anchor="middle">Interplanal</text>'
           + f'<text x="{W/2}" y="510" font-family="Cinzel Decorative" font-weight="900" font-size="170" fill="#f3d48a" stroke="{INK}" stroke-width="12" paint-order="stroke" text-anchor="middle">Champions</text>'
           + f'<text x="{W/2}" y="2000" font-family="IM FELL English" font-style="italic" font-size="52" fill="#f4dcc0" text-anchor="middle">{sub}</text>'
           + f'<text x="{W/2}" y="2070" font-family="Cinzel" font-weight="700" font-size="38" fill="#d8aa52" text-anchor="middle" letter-spacing="4">{line}</text>'
           + f'<text x="{W-80}" y="2150" font-family="Cinzel" font-weight="700" font-size="30" fill="#d8aa52" text-anchor="end" letter-spacing="3">PACTS &amp; POLYHEDRALS</text>'
           + (f'<rect x="{W/2-460}" y="560" width="920" height="96" rx="12" fill="#5e0b18" stroke="#d8aa52" stroke-width="5"/>'
              f'<text x="{W/2}" y="628" font-family="Cinzel" font-weight="900" font-size="54" fill="#ffe8c8" text-anchor="middle" letter-spacing="8">{band}</text>' if band else "")
           + f'<rect x="28" y="28" width="{W-56}" height="{H-56}" fill="none" stroke="#d8aa52" stroke-width="6" opacity="0.75"/></svg>')
    im = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS])))).convert("RGB")
    os.makedirs(DIST, exist_ok=True)
    im.save(f"{DIST}/dmsguild-{out}.jpg", "JPEG", quality=92)
    return im


def _back(out, quote, paras, bullets, foot=""):
    W, H = 1700, 2200
    y = 520
    t = ""
    for para in paras:
        for l in textwrap.wrap(para, 46):
            t += f'<text x="{W/2}" y="{y}" font-family="EB Garamond" font-size="50" fill="#f4dcc0" text-anchor="middle">{l}</text>'
            y += 70
        y += 40
    y += 60
    t += "".join(f'<text x="{W/2}" y="{y+i*72}" font-family="Cinzel" font-weight="700" font-size="40" fill="#d8aa52" text-anchor="middle">☩ {b}</text>' for i, b in enumerate(bullets))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}'
           '<radialGradient id="sky" cx="0.5" cy="0.3" r="0.9"><stop offset="0" stop-color="#5e0b18"/><stop offset="1" stop-color="#070203"/></radialGradient>'
           f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + peaks(W, H, 2080, 21, "#0a0204", spires=True) + embers(W, H, 260, 9)
           + f'<text x="{W/2}" y="330" font-family="IM FELL English" font-style="italic" font-size="60" fill="#ffcfaa" text-anchor="middle">{quote}</text>'
           + t + (f'<text x="{W/2}" y="{H-140}" font-family="Cinzel" font-weight="700" font-size="34" fill="#d8aa52" text-anchor="middle" letter-spacing="3">{foot}</text>' if foot else "")
           + f'<rect x="28" y="28" width="{W-56}" height="{H-56}" fill="none" stroke="#d8aa52" stroke-width="6" opacity="0.75"/></svg>')
    Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS])))).convert("RGB").save(f"{DIST}/dmsguild-{out}.jpg", "JPEG", quality=90)


def backcover():
    _back("back", "“Every crown is a contract. Read yours.”",
          ["Asmodeus has opened the throne of Avernus to any challenger who can prove Survival, Deviousness and Dominion. "
           "The prize is real. So is every clause.",
           "A drowned town has been registered as unclaimed. A deputy registrar is building champions out of stolen names. "
           "And Misty, Queen of Barbed Chains, wants first refusal on every secret the winner will ever hold."],
          ["A level 12–17 campaign in six chapters", "23 vector battlemaps, the 2020 originals rebuilt",
           "45 creatures including the CR 30 Hag Queen", "The Redline Run: soul-fuelled war machines",
           "6 level-12 claimants, 3 subclasses, 17 spells", "The Championship Charter and contract forms"])


def player_back():
    _back("player-back", "“My crown, our crown, or their crown?”",
          ["The Championship of the First Crown is open. Register alone, as a joint slate, or as a patron's proxy. Nobody makes "
           "you sell your soul. Nobody stops you, either."],
          ["Six level-12 claimants on five-page sheets", "The Ruby Court, Blood-Price and Ashen Covenants",
           "17 contractual spells and 14 relics", "The Soul Furnace: soul coins and war machines",
           "The Nine Articles and eight player contracts"],
          foot="PLAYER'S GUIDE · PACTS &amp; POLYHEDRALS")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    title(); banner(); print("ok")
