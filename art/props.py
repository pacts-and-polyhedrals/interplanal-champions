"""Top-down vector props. Each returns SVG drawn around (0,0) in pixels (100 px = 5 ft)."""
import math, random
from mapkit import INK

R = random.Random(7)


def _s(w=5):
    return f'stroke="{INK}" stroke-width="{w}"'


def rect(w, h, fill, rx=6, sw=5, extra=""):
    return f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {_s(sw)} {extra}/>'


def stall(w=200, h=120, a="#b51f30", b="#efe6d0", goods=True, seed=0):
    r = random.Random(seed)
    s = rect(w, h * 0.45, "#6e4527", 4).replace(f'y="{-h*0.45/2}"', f'y="{h*0.05}"')
    stripes = []
    n = max(3, int(w // 40))
    for i in range(n):
        x0 = -w / 2 + i * w / n
        stripes.append(f'<rect x="{x0:.1f}" y="{-h/2}" width="{w/n:.1f}" height="{h*0.55:.1f}" fill="{a if i%2==0 else b}"/>')
    awn = (f'<g>{"".join(stripes)}<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h*0.55:.1f}" fill="none" {_s()}/>'
           + "".join(f'<path d="M{-w/2 + i*w/n:.1f} {h*0.05:.1f} q{w/n/2:.1f} 18 {w/n:.1f} 0" fill="{a if i%2==0 else b}" {_s(3)}/>' for i in range(n)) + '</g>')
    gd = ""
    if goods:
        for i in range(int(w // 34)):
            x = -w / 2 + 18 + i * 32
            c = r.choice(["#d24a2a", "#e8c35a", "#5aa05a", "#f0ead8", "#8a4a2a", "#c0283a"])
            gd += f'<circle cx="{x}" cy="{h*0.28:.0f}" r="11" fill="{c}" {_s(3)}/>'
    return s + gd + awn


def pine(r=110, decorated=True, star=True, seed=0):
    rr = random.Random(seed)
    out = [f'<circle r="{r}" fill="#123a24" {_s(6)}/>']
    for k in range(3):
        rad = r * (0.85 - k * 0.25)
        pts = []
        n = 14
        for i in range(n * 2):
            a = i * math.pi / n
            d = rad if i % 2 == 0 else rad * 0.78
            pts.append(f"{math.cos(a)*d:.1f},{math.sin(a)*d:.1f}")
        out.append(f'<polygon points="{" ".join(pts)}" fill="{["#1d5a36", "#257042", "#2f8650"][k]}" {_s(4)}/>')
    # snow
    for _ in range(int(r / 8)):
        a = rr.uniform(0, 6.28)
        d = rr.uniform(0.2, 0.8) * r
        out.append(f'<ellipse cx="{math.cos(a)*d:.0f}" cy="{math.sin(a)*d:.0f}" rx="{rr.uniform(6,14):.0f}" ry="5" fill="#eef3f8" opacity="0.9"/>')
    if decorated:
        for _ in range(int(r / 6)):
            a = rr.uniform(0, 6.28)
            d = rr.uniform(0.25, 0.85) * r
            c = rr.choice(["#c0283a", "#e8c35a", "#e8c35a", "#5ab0d8"])
            out.append(f'<circle cx="{math.cos(a)*d:.0f}" cy="{math.sin(a)*d:.0f}" r="{rr.uniform(5,9):.0f}" fill="{c}" {_s(2)}/>')
        # garland spiral
        pts = " ".join(f"{math.cos(t)*r*0.12*t/2:.0f},{math.sin(t)*r*0.12*t/2:.0f}" for t in [i * 0.3 for i in range(1, 45)])
        out.append(f'<polyline points="{pts}" fill="none" stroke="#e8c35a" stroke-width="4" opacity="0.85"/>')
    if star:
        pts = " ".join(f"{math.cos(i*math.pi/5 - math.pi/2)*(22 if i%2==0 else 9):.1f},{math.sin(i*math.pi/5 - math.pi/2)*(22 if i%2==0 else 9):.1f}" for i in range(10))
        out.append(f'<polygon points="{pts}" fill="#ffd84a" {_s(3)}/>')
    return "".join(out)


def lamppost():
    return (f'<circle r="34" fill="url(#rg-gold)" opacity="0.8"/><circle r="15" fill="#2a262c" {_s(4)}/>'
            f'<circle r="8" fill="#ffd27a" {_s(2)}/>')


def barrel(r=24, fill="#7a4a22"):
    return (f'<circle r="{r}" fill="{fill}" {_s(4)}/><circle r="{r*0.72:.1f}" fill="none" stroke="#3a2210" stroke-width="3"/>'
            f'<circle r="{r*0.4:.1f}" fill="#5a3416" {_s(2)}/>')


def crate(s=60, fill="#8a5a2e"):
    return (rect(s, s, fill, 3) + f'<path d="M{-s/2+6} {-s/2+6} L{s/2-6} {s/2-6} M{s/2-6} {-s/2+6} L{-s/2+6} {s/2-6}" '
            f'stroke="#4a2c12" stroke-width="5"/>' + rect(s - 12, s - 12, "none", 2, 3))


def present(s=40, box="#c0283a", ribbon="#e8c35a"):
    return (rect(s, s, box, 4) + f'<rect x="{-s/2}" y="-4" width="{s}" height="8" fill="{ribbon}" {_s(2)}/>'
            f'<rect x="-4" y="{-s/2}" width="8" height="{s}" fill="{ribbon}" {_s(2)}/>'
            f'<circle r="8" fill="{ribbon}" {_s(2)}/>')


def present_pile(n=7, spread=60, seed=0):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(-spread, spread), r.uniform(-spread, spread)
        s = r.uniform(26, 48)
        box, rib = r.choice([("#c0283a", "#e8c35a"), ("#2f7a46", "#f0ead8"), ("#e8c35a", "#c0283a"),
                             ("#2c4f8a", "#e8c35a"), ("#f0ead8", "#c0283a")])
        out.append(f'<g transform="translate({x:.0f},{y:.0f}) rotate({r.uniform(-30,30):.0f})">{present(s, box, rib)}</g>')
    return "".join(out)


def candy_cane(l=120):
    d = f"M0 {l/2} L0 {-l/2+30} A30 30 0 0 1 60 {-l/2+30}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#f4efe4" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#c0283a" stroke-width="20" stroke-dasharray="12 14" stroke-linecap="butt"/>')


def snowman():
    return (f'<circle r="44" fill="#eef3f8" {_s(5)}/><circle r="30" cy="-6" fill="#f6f9fc" {_s(4)}/>'
            f'<circle r="20" cy="-10" fill="#1c1a1e" {_s(3)}/><rect x="-14" y="-24" width="28" height="10" fill="#8a1424"/>'
            f'<path d="M0 6 l26 6" stroke="#e8701a" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M-30 20 q30 22 60 0" stroke="#c0283a" stroke-width="9" fill="none"/>')


def bench(w=160):
    return rect(w, 40, "#5e3a1e", 5) + "".join(f'<line x1="{-w/2+8}" y1="{y}" x2="{w/2-8}" y2="{y}" stroke="#2e1a0a" stroke-width="2"/>' for y in (-8, 8))


def table(w=160, h=90, fill="#6e4527", cloth=None):
    s = rect(w, h, fill, 6)
    if cloth:
        s += rect(w - 20, h - 20, cloth, 4, 3)
    return s


def round_table(r=50, fill="#6e4527"):
    return f'<circle r="{r}" fill="{fill}" {_s(5)}/><circle r="{r*0.7:.0f}" fill="none" stroke="#3a2210" stroke-width="2"/>'


def chair():
    return rect(34, 34, "#5a3618", 5, 4) + f'<rect x="-17" y="-22" width="34" height="9" fill="#3a2210" {_s(3)}/>'


def bookshelf(w=200, h=40, seed=0):
    r = random.Random(seed)
    out = [rect(w, h, "#3b2314", 3)]
    x = -w / 2 + 6
    while x < w / 2 - 12:
        bw = r.uniform(6, 14)
        out.append(f'<rect x="{x:.1f}" y="{-h/2+6}" width="{bw:.1f}" height="{h-12}" fill="{r.choice(["#8a1a24","#2a4a7a","#2f6a3a","#b38a2e","#5a2a6a","#7a4a22"])}" stroke="{INK}" stroke-width="1.5"/>')
        x += bw + 1
    return "".join(out)


def desk(w=140, h=80):
    return (rect(w, h, "#5a3418", 6) + rect(w * 0.5, h * 0.55, "#efe6cf", 2, 2).replace("<rect", '<rect transform="rotate(-8)"')
            + f'<circle cx="{w*0.32:.0f}" cy="{-h*0.2:.0f}" r="8" fill="#1a1012" {_s(2)}/>'
            + f'<path d="M{w*0.32:.0f} {-h*0.2:.0f} l18 -22" stroke="#e8e0c8" stroke-width="4"/>')


def lectern():
    return (rect(70, 50, "#4a2a14", 6) + f'<rect x="-28" y="-18" width="56" height="30" fill="#efe6cf" {_s(3)} transform="rotate(-6)"/>')


def filing_cabinet(w=80, h=50):
    return rect(w, h, "#55505c", 3) + "".join(f'<rect x="{-w/2+8+i*((w-16)/3):.0f}" y="-8" width="{(w-16)/3-6:.0f}" height="16" fill="#8a8590" {_s(2)}/>' for i in range(3))


def jar_shelf(w=200, h=40, seed=0):
    r = random.Random(seed)
    out = [rect(w, h, "#2e1c12", 3)]
    for i in range(int((w - 16) // 22)):
        x = -w / 2 + 16 + i * 22
        c = r.choice(["#9fe0c8", "#c8a0e0", "#e0c890", "#e09090", "#a0c8e0"])
        out.append(f'<circle cx="{x}" cy="0" r="9" fill="{c}" {_s(2)} opacity="0.95"/><circle cx="{x}" cy="0" r="3" fill="#fff" opacity="0.8"/>')
    return "".join(out)


def gear(r=80, teeth=12, fill="url(#lg-brass)", hole=True):
    pts = []
    for i in range(teeth * 4):
        a = i * math.pi * 2 / (teeth * 4)
        d = r if (i % 4) in (1, 2) else r * 0.82
        pts.append(f"{math.cos(a)*d:.1f},{math.sin(a)*d:.1f}")
    s = f'<polygon points="{" ".join(pts)}" fill="{fill}" {_s(5)}/>'
    s += f'<circle r="{r*0.55:.0f}" fill="none" stroke="#3b2a0c" stroke-width="4"/>'
    for i in range(4):
        a = i * math.pi / 2 + 0.4
        s += f'<line x1="0" y1="0" x2="{math.cos(a)*r*0.55:.0f}" y2="{math.sin(a)*r*0.55:.0f}" stroke="#3b2a0c" stroke-width="8"/>'
    if hole:
        s += f'<circle r="{r*0.15:.0f}" fill="#1a1410" {_s(3)}/>'
    return s


def conveyor(l=800, w=80, boxes=6, seed=0):
    r = random.Random(seed)
    s = rect(l, w, "#2b2a2e", 6, 6)
    s += rect(l - 16, w - 22, "#4a3a2a", 2, 3)
    for i in range(int(l // 30)):
        x = -l / 2 + 12 + i * 30
        s += f'<line x1="{x}" y1="{-w/2+11}" x2="{x}" y2="{w/2-11}" stroke="#1a1410" stroke-width="2"/>'
    for i in range(boxes):
        x = -l / 2 + (i + 0.5) * l / boxes + r.uniform(-20, 20)
        s += f'<g transform="translate({x:.0f},0) rotate({r.uniform(-12,12):.0f})">{present(r.uniform(28, 40), *r.choice([("#c0283a", "#e8c35a"), ("#2f7a46", "#f0ead8"), ("#e8c35a", "#c0283a"), ("#2c4f8a", "#e8c35a")]))}</g>'
    return s


def stamp_press(label=""):
    return (rect(120, 120, "#3a3640", 8) + f'<circle r="42" fill="url(#lg-brass)" {_s(5)}/>'
            + f'<rect x="-50" y="-8" width="100" height="16" fill="#26232a" {_s(3)}/><circle r="16" fill="#8e1424" {_s(3)}/>')


def mech_arm(len_=160, rot=0):
    return (f'<g transform="rotate({rot})"><circle r="26" fill="url(#lg-iron)" {_s(5)}/>'
            f'<rect x="0" y="-12" width="{len_*0.55:.0f}" height="24" fill="url(#lg-brass)" {_s(4)}/>'
            f'<circle cx="{len_*0.55:.0f}" r="14" fill="url(#lg-iron)" {_s(4)}/>'
            f'<rect x="{len_*0.55:.0f}" y="-9" width="{len_*0.45:.0f}" height="18" fill="url(#lg-brass)" {_s(4)} transform="rotate(35 {len_*0.55:.0f} 0)"/>'
            f'</g>')


def pipe_run(pts, w=22, fill="#6e5a3a"):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+10}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#c8a870" stroke-width="{w*0.25:.0f}" stroke-linejoin="round" opacity="0.6"/>')


def clock_face(r=300, hands=(11, 59), numerals=True):
    s = [f'<circle r="{r}" fill="#efe6cf" {_s(10)}/>', f'<circle r="{r*0.92:.0f}" fill="none" stroke="#8e1424" stroke-width="8"/>']
    roman = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
    for i in range(60):
        a = i * math.pi / 30 - math.pi / 2
        r1 = r * (0.8 if i % 5 == 0 else 0.86)
        s.append(f'<line x1="{math.cos(a)*r1:.0f}" y1="{math.sin(a)*r1:.0f}" x2="{math.cos(a)*r*0.9:.0f}" y2="{math.sin(a)*r*0.9:.0f}" stroke="{INK}" stroke-width="{6 if i%5==0 else 2}"/>')
    if numerals:
        for i, n in enumerate(roman):
            a = i * math.pi / 6 - math.pi / 2
            s.append(f'<text x="{math.cos(a)*r*0.68:.0f}" y="{math.sin(a)*r*0.68 + r*0.05:.0f}" font-family="Cinzel" font-weight="700" font-size="{r*0.14:.0f}" text-anchor="middle" fill="{INK}">{n}</text>')
    h, m = hands
    ah = ((h % 12) + m / 60) * math.pi / 6 - math.pi / 2
    am = m * math.pi / 30 - math.pi / 2
    s.append(f'<line x1="0" y1="0" x2="{math.cos(ah)*r*0.5:.0f}" y2="{math.sin(ah)*r*0.5:.0f}" stroke="{INK}" stroke-width="{r*0.06:.0f}" stroke-linecap="round"/>')
    s.append(f'<line x1="0" y1="0" x2="{math.cos(am)*r*0.78:.0f}" y2="{math.sin(am)*r*0.78:.0f}" stroke="#8e1424" stroke-width="{r*0.035:.0f}" stroke-linecap="round"/>')
    s.append(f'<circle r="{r*0.07:.0f}" fill="url(#lg-brass)" {_s(4)}/>')
    return "".join(s)


def trapped_sun(r=90):
    claws = ""
    for i in range(6):
        a = i * math.pi / 3
        x, y = math.cos(a) * r * 1.05, math.sin(a) * r * 1.05
        claws += (f'<path d="M{math.cos(a)*r*1.6:.0f} {math.sin(a)*r*1.6:.0f} L{x:.0f} {y:.0f} '
                  f'L{math.cos(a+0.25)*r*0.85:.0f} {math.sin(a+0.25)*r*0.85:.0f}" fill="none" stroke="{INK}" stroke-width="20" stroke-linejoin="round"/>'
                  f'<path d="M{math.cos(a)*r*1.6:.0f} {math.sin(a)*r*1.6:.0f} L{x:.0f} {y:.0f} '
                  f'L{math.cos(a+0.25)*r*0.85:.0f} {math.sin(a+0.25)*r*0.85:.0f}" fill="none" stroke="#3a3640" stroke-width="10" stroke-linejoin="round"/>')
    return (f'<circle r="{r*1.8:.0f}" fill="url(#rg-gold)" opacity="0.6"/>'
            f'<circle r="{r}" fill="url(#rg-sun)" {_s(6)}/><circle r="{r}" fill="none" stroke="#bfe6ff" stroke-width="6" opacity="0.7"/>'
            f'<ellipse cx="{-r*0.35:.0f}" cy="{-r*0.4:.0f}" rx="{r*0.3:.0f}" ry="{r*0.14:.0f}" fill="#fff" opacity="0.7" transform="rotate(-30)"/>' + claws)


def furnace_pit(r=150):
    return (f'<circle r="{r*1.25:.0f}" fill="url(#rg-fire)" opacity="0.75"/>'
            f'<circle r="{r}" fill="#1a0806" {_s(8)}/>'
            f'<circle r="{r*0.85:.0f}" fill="url(#rg-fire)"/>'
            + "".join(f'<circle cx="{math.cos(i)*r*0.5:.0f}" cy="{math.sin(i)*r*0.5:.0f}" r="{r*0.12:.0f}" fill="#ffe08a" opacity="0.8"/>' for i in range(0, 12, 2))
            + f'<circle r="{r}" fill="none" stroke="#5a5660" stroke-width="16" stroke-dasharray="20 12"/>')


def ledger_book(w=220, h=150):
    chains = "".join(f'<line x1="0" y1="0" x2="{x}" y2="{y}" stroke="{INK}" stroke-width="10" stroke-dasharray="14 6"/>'
                     f'<line x1="0" y1="0" x2="{x}" y2="{y}" stroke="#8a8590" stroke-width="5" stroke-dasharray="14 6"/>'
                     for x, y in ((-170, -150), (170, -150), (-170, 150), (170, 150)))
    lines = "".join(f'<line x1="{-w/2+16}" y1="{-h/2+18+i*14}" x2="{-12}" y2="{-h/2+18+i*14}" stroke="#5a1a1a" stroke-width="2"/>'
                    f'<line x1="{12}" y1="{-h/2+18+i*14}" x2="{w/2-16}" y2="{-h/2+18+i*14}" stroke="#5a1a1a" stroke-width="2"/>' for i in range(8))
    return (chains + rect(w + 20, h + 20, "#5e0b18", 10, 6) + rect(w, h, "#efe2c0", 4, 4) + lines
            + f'<line x1="0" y1="{-h/2}" x2="0" y2="{h/2}" stroke="{INK}" stroke-width="5"/>')


def throne(w=200, h=180):
    return (rect(w, h, "#5e0b18", 20, 7) + rect(w * 0.62, h * 0.6, "#8e1424", 14, 4).replace("<rect", f'<rect transform="translate(0,{h*0.12:.0f})"')
            + f'<path d="M{-w/2-10} {-h/2+10} q-30 -60 10 -90 M{w/2+10} {-h/2+10} q30 -60 -10 -90" stroke="{INK}" stroke-width="18" fill="none" stroke-linecap="round"/>'
            + f'<path d="M{-w/2-10} {-h/2+10} q-30 -60 10 -90 M{w/2+10} {-h/2+10} q30 -60 -10 -90" stroke="#26232a" stroke-width="10" fill="none" stroke-linecap="round"/>'
            + f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="26" fill="url(#lg-brass)" {_s(4)}/>')


def bell_frame(w=260):
    return (f'<rect x="{-w/2}" y="-20" width="{w}" height="40" fill="#3a2614" {_s(6)}/>'
            + "".join(f'<circle cx="{x}" cy="0" r="{rr}" fill="url(#lg-brass)" {_s(5)}/><circle cx="{x}" cy="0" r="{rr*0.35:.0f}" fill="#3b2a0c"/>'
                      for x, rr in ((-w / 2 + 50, 40), (0, 58), (w / 2 - 50, 40))))


def writ_frame():
    return (f'<rect x="-48" y="-48" width="96" height="96" fill="none" stroke="{INK}" stroke-width="14"/>'
            f'<rect x="-48" y="-48" width="96" height="96" fill="none" stroke="#d8aa52" stroke-width="7"/>'
            f'<circle r="54" fill="url(#rg-gold)" opacity="0.35"/>')


def pillar(r=34, fill="#5b5560"):
    return f'<circle r="{r}" fill="{fill}" {_s(6)}/><circle r="{r*0.65:.0f}" fill="none" stroke="#7a7480" stroke-width="4"/>'


def chimney(w=70, h=50):
    return (rect(w, h, "#6a3a30", 3) + rect(w - 18, h - 18, "#1a1012", 2, 3)
            + f'<ellipse cx="0" cy="{-h/2}" rx="{w/2}" ry="8" fill="#eef3f8" opacity="0.9"/>')


def sleigh(w=180, h=110):
    return (f'<path d="M{-w/2} {-h/2+10} Q{-w/2-30} 0 {-w/2} {h/2-10} L{w/2-20} {h/2-10} Q{w/2+10} 0 {w/2-20} {-h/2+10} Z" fill="#8e1424" {_s(6)}/>'
            + f'<path d="M{-w/2+20} {-h/2+24} L{w/2-34} {-h/2+24} L{w/2-34} {h/2-24} L{-w/2+20} {h/2-24} Z" fill="#5e0b18" {_s(3)}/>'
            + f'<path d="M{-w/2-10} {-h/2} L{w/2+30} {-h/2} M{-w/2-10} {h/2} L{w/2+30} {h/2}" stroke="#d8aa52" stroke-width="8" stroke-linecap="round"/>'
            + present_pile(4, 25, 3))


def banner(w=600, text="THE HEARTHLIGHT FOUNDATION"):
    return (f'<rect x="{-w/2}" y="-36" width="{w}" height="72" fill="#8e1424" {_s(6)}/>'
            f'<rect x="{-w/2+8}" y="-28" width="{w-16}" height="56" fill="none" stroke="#d8aa52" stroke-width="3"/>'
            f'<text x="0" y="12" font-family="Cinzel" font-weight="900" font-size="34" text-anchor="middle" fill="#f0d890">{text}</text>'
            f'<circle cx="{-w/2}" cy="0" r="10" fill="#d8aa52" {_s(3)}/><circle cx="{w/2}" cy="0" r="10" fill="#d8aa52" {_s(3)}/>')


def cage(w=200, h=160):
    bars = "".join(f'<line x1="{x}" y1="{-h/2}" x2="{x}" y2="{h/2}" stroke="#26232a" stroke-width="8"/>' for x in range(int(-w / 2), int(w / 2) + 1, 20))
    return (rect(w, h, "#1a1418", 4, 6) + bars + f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="8"/>')


def elevator(r=70):
    return (f'<circle r="{r}" fill="#26232a" {_s(6)}/><circle r="{r*0.85:.0f}" fill="url(#lg-brass)" {_s(4)}/>'
            + "".join(f'<line x1="{-r*0.8:.0f}" y1="{y}" x2="{r*0.8:.0f}" y2="{y}" stroke="#3b2a0c" stroke-width="4"/>' for y in range(int(-r * 0.6), int(r * 0.6) + 1, 16))
            + f'<text y="8" font-family="Cinzel" font-weight="900" font-size="22" text-anchor="middle" fill="#1a1012">999</text>')


def chute(r=60):
    return (f'<circle r="{r}" fill="#0c0a0c" {_s(8)}/><circle r="{r*0.7:.0f}" fill="none" stroke="#3a3640" stroke-width="6"/>'
            f'<circle r="{r*1.08:.0f}" fill="none" stroke="#d8aa52" stroke-width="6" stroke-dasharray="16 10"/>')


def rubble(n=8, spread=50, seed=0):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(-spread,spread):.0f}" cy="{r.uniform(-spread,spread):.0f}" r="{r.uniform(5,14):.0f}" fill="{r.choice(["#7a4a22","#e8d8b0","#c0283a","#f0ead8"])}" {_s(2)}/>' for _ in range(n))


def puddle(rx=90, ry=50, color="#efe2b8"):
    return f'<ellipse rx="{rx}" ry="{ry}" fill="{color}" stroke="#c9b37a" stroke-width="4" opacity="0.92"/>'


def rug(w, h, fill="#6e0f1c", border="#c99a3a"):
    return rect(w, h, fill, 6, 4) + rect(w - 24, h - 24, "none", 4, 0, f'stroke="{border}" stroke-width="5"').replace(f'stroke="{INK}" stroke-width="0" ', "")


def steps(w, n=4, vertical=False):
    out = []
    for i in range(n):
        out.append(f'<rect x="{-w/2}" y="{-n*14 + i*28}" width="{w}" height="28" fill="{["#3a2a30","#46343a","#52404a","#5e4c56"][i%4]}" {_s(3)}/>')
    return "".join(out)


def scales():
    return (f'<line x1="0" y1="-50" x2="0" y2="40" stroke="{INK}" stroke-width="12"/><line x1="0" y1="-50" x2="0" y2="40" stroke="#d8aa52" stroke-width="6"/>'
            f'<line x1="-60" y1="-40" x2="60" y2="-40" stroke="{INK}" stroke-width="10"/><line x1="-60" y1="-40" x2="60" y2="-40" stroke="#d8aa52" stroke-width="5"/>'
            f'<circle cx="-60" cy="-10" r="22" fill="url(#lg-brass)" {_s(4)}/><circle cx="60" cy="-10" r="22" fill="url(#lg-brass)" {_s(4)}/>')


def chain_hang(r=18):
    return f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="10"/><circle r="{r}" fill="none" stroke="#8a8590" stroke-width="5"/>'


def wreath(r=40):
    out = [f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="22"/><circle r="{r}" fill="none" stroke="#2f7a46" stroke-width="14"/>']
    for i in range(8):
        a = i * math.pi / 4
        out.append(f'<circle cx="{math.cos(a)*r:.0f}" cy="{math.sin(a)*r:.0f}" r="5" fill="#c0283a"/>')
    return "".join(out)


def cart(w=160, h=90):
    return (rect(w, h, "#6e4527", 6) + f'<rect x="{-w/2-14}" y="{-h/2-6}" width="16" height="{h+12}" rx="6" fill="#2a1a0e" {_s(3)}/>'
            + f'<rect x="{w/2-2}" y="{-h/2-6}" width="16" height="{h+12}" rx="6" fill="#2a1a0e" {_s(3)}/>'
            + "".join(f'<g transform="translate({x},{y})">{barrel(18)}</g>' for x, y in ((-40, -18), (0, -18), (40, -18), (-20, 18), (20, 18))))


def scroll_rack(w=200, h=46):
    out = [rect(w, h, "#3b2314", 3)]
    for i in range(int((w - 10) // 16)):
        x = -w / 2 + 12 + i * 16
        out.append(f'<circle cx="{x}" cy="-8" r="7" fill="#efe2c0" {_s(2)}/><circle cx="{x+8}" cy="9" r="7" fill="#e6d4a8" {_s(2)}/>')
    return "".join(out)


def railing(l, vertical=False):
    if vertical:
        return f'<line x1="0" y1="{-l/2}" x2="0" y2="{l/2}" stroke="{INK}" stroke-width="12"/><line x1="0" y1="{-l/2}" x2="0" y2="{l/2}" stroke="#b08a3a" stroke-width="6"/>'
    return f'<line x1="{-l/2}" y1="0" x2="{l/2}" y2="0" stroke="{INK}" stroke-width="12"/><line x1="{-l/2}" y1="0" x2="{l/2}" y2="0" stroke="#b08a3a" stroke-width="6"/>'


def machine(w=200, h=140, seed=0):
    r = random.Random(seed)
    s = rect(w, h, "url(#lg-iron)", 10, 6)
    for i in range(3):
        s += f'<circle cx="{-w/2 + 40 + i*(w-80)/2:.0f}" cy="{-h/4:.0f}" r="16" fill="#8e1424" {_s(3)}/>'
    s += f'<rect x="{-w/2+20}" y="{h/8:.0f}" width="{w-40}" height="{h/4:.0f}" fill="#1a1012" {_s(3)}/>'
    s += f'<rect x="{-w/2+24}" y="{h/8+6:.0f}" width="{(w-48)*r.uniform(0.3,0.9):.0f}" height="{h/4-12:.0f}" fill="#d8aa52"/>'
    return s


def hatch(w, h):
    return rect(w, h, "#1a1418", 4, 6) + f'<path d="M{-w/2} {-h/2} L{w/2} {h/2} M{w/2} {-h/2} L{-w/2} {h/2}" stroke="#3a3640" stroke-width="6"/>'
