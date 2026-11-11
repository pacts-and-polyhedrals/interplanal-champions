import re
"""Grotesque-chibi gothic portraits (front view) and true overhead tokens, as vector SVG."""
import math, random, io, os
import resvg_py
from PIL import Image

INK = "#120909"
FONTS = "/home/claude/ic/art/fonts"
OUT = "/home/claude/ic/module/assets"


def render(svg, path, size):
    png = resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[FONTS], width=size, height=size)
    im = Image.open(io.BytesIO(bytes(png))).convert("RGBA")
    im.save(path, "WEBP", quality=86, method=5)


def S(w=10):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


DEFS = ('<defs>'
        '<pattern id="hatch" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
        f'<line x1="0" y1="0" x2="0" y2="16" stroke="{INK}" stroke-width="3.2"/></pattern>'
        '<pattern id="hatch2" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">'
        f'<line x1="0" y1="0" x2="0" y2="12" stroke="{INK}" stroke-width="2.4"/></pattern>'
        '<filter id="glw" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>'
        '<filter id="glw2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>'
        '<filter id="tsh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity="0.6"/></filter>'
        '<linearGradient id="brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0c868"/><stop offset="0.5" stop-color="#b8862e"/><stop offset="1" stop-color="#6a4410"/></linearGradient>'
        '<linearGradient id="iron" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6e6a76"/><stop offset="1" stop-color="#26232a"/></linearGradient>'
        '</defs>')


def bg(color, seed=0):
    r = random.Random(seed)
    s = [f'<radialGradient id="bgg" cx="0.5" cy="0.45" r="0.7"><stop offset="0" stop-color="{color}"/>'
         f'<stop offset="0.65" stop-color="#1a0c0e"/><stop offset="1" stop-color="#070304"/></radialGradient>',
         '<rect width="1000" height="1000" fill="url(#bgg)"/>']
    for i in range(46):
        a = r.uniform(0, 6.283)
        r0, r1 = r.uniform(380, 460), r.uniform(560, 760)
        s.append(f'<line x1="{500+math.cos(a)*r0:.0f}" y1="{450+math.sin(a)*r0:.0f}" x2="{500+math.cos(a)*r1:.0f}" y2="{450+math.sin(a)*r1:.0f}" stroke="#000" stroke-width="{r.uniform(2,6):.1f}" opacity="0.55"/>')
    for i in range(30):
        x, y = r.uniform(0, 1000), r.uniform(0, 1000)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,6):.0f}" fill="#fff" opacity="{r.uniform(0.25,0.7):.2f}"/>')
    return "".join(s)


def frame():
    return (f'<rect x="14" y="14" width="972" height="972" fill="none" stroke="{INK}" stroke-width="24"/>'
            '<rect x="26" y="26" width="948" height="948" fill="none" stroke="#b8862e" stroke-width="6"/>')


# --------------------------------------------------------------------------- humanoid
def humanoid(p):
    """p: dict of look options. Returns inner SVG for a 1000x1000 portrait."""
    r = random.Random(p.get("seed", 1))
    skin = p.get("skin", "#e8b496")
    skin_dk = p.get("skin_dk", "#b47a5e")
    coat = p.get("coat", "#8e1424")
    coat_dk = p.get("coat_dk", "#4e0a12")
    trim = p.get("trim")
    hs = p.get("head", 1.0)
    tall = p.get("hat") in ("santa", "shako", "tophat", "elf", "candles", "baker", "witch", "crown", "thorns")
    hx, hy = 500, p.get("hy", 500 if tall else 450)
    if tall:
        hs *= 0.92
    hw, hh = 225 * hs, 210 * hs
    kind = p.get("kind", "flesh")
    out = []
    # body
    bw = p.get("body_w", 300)
    out.append(f'<path d="M{500-bw} 1000 C{500-bw} 760 {500-bw*0.6} 640 500 630 C{500+bw*0.6} 640 {500+bw} 760 {500+bw} 1000 Z" fill="{coat}" {S(12)}/>')
    out.append(f'<path d="M{500+bw*0.15} 650 C{500+bw*0.6} 660 {500+bw*0.95} 780 {500+bw} 1000 L{500+bw*0.25} 1000 Z" fill="url(#hatch)" opacity="0.55"/>')
    if trim:
        out.append(f'<path d="M{500-bw*0.75} 700 Q500 790 {500+bw*0.75} 700" fill="none" stroke="{INK}" stroke-width="66"/>'
                   f'<path d="M{500-bw*0.75} 700 Q500 790 {500+bw*0.75} 700" fill="none" stroke="{trim}" stroke-width="50"/>')
        out.append(f'<line x1="500" y1="760" x2="500" y2="1000" stroke="{INK}" stroke-width="58"/><line x1="500" y1="760" x2="500" y2="1000" stroke="{trim}" stroke-width="42"/>')
    if p.get("belt"):
        out.append(f'<rect x="{500-bw*0.95}" y="900" width="{bw*1.9}" height="56" fill="{p["belt"]}" {S(10)}/><rect x="460" y="892" width="80" height="72" rx="8" fill="url(#brass)" {S(8)}/>')
    if p.get("collar"):
        out.append(f'<rect x="420" y="618" width="160" height="44" rx="10" fill="url(#brass)" {S(8)}/><circle cx="500" cy="640" r="18" fill="#8e1424" {S(5)}/>')
    if p.get("armor"):
        out.append(f'<path d="M{500-bw*0.7} 720 Q500 690 {500+bw*0.7} 720 L{500+bw*0.6} 1000 L{500-bw*0.6} 1000 Z" fill="{p["armor"]}" {S(10)}/>')
        out.append(f'<path d="M{500-bw*0.5} 760 Q500 740 {500+bw*0.5} 760" fill="none" stroke="#fff" stroke-width="8" opacity="0.4"/>')
        if p.get("emblem"):
            out.append(p["emblem"])
    # back hair / hood
    hair = p.get("hair")
    if p.get("hood"):
        out.append(f'<path d="M{hx-hw*1.25} {hy+hh*1.3} C{hx-hw*1.4} {hy-hh*1.1} {hx+hw*1.4} {hy-hh*1.1} {hx+hw*1.25} {hy+hh*1.3} Z" fill="{p["hood"]}" {S(12)}/>')
    if hair and p.get("hair_style") == "long":
        out.append(f'<path d="M{hx-hw*1.05} {hy-hh*0.3} C{hx-hw*1.3} {hy+hh*0.9} {hx-hw*0.9} {hy+hh*1.6} {hx-hw*0.4} {hy+hh*1.5} L{hx+hw*0.4} {hy+hh*1.5} C{hx+hw*0.9} {hy+hh*1.6} {hx+hw*1.3} {hy+hh*0.9} {hx+hw*1.05} {hy-hh*0.3} Z" fill="{hair}" {S(10)}/>')
    # ears
    ear = p.get("ears", "round")
    if ear == "pointed":
        for sgn in (-1, 1):
            out.append(f'<path d="M{hx+sgn*hw*0.9} {hy-10} L{hx+sgn*hw*1.55} {hy-hh*0.75} L{hx+sgn*hw*0.95} {hy+hh*0.25} Z" fill="{skin}" {S(10)}/>')
    elif ear == "round" and kind == "flesh":
        for sgn in (-1, 1):
            out.append(f'<ellipse cx="{hx+sgn*hw*0.98}" cy="{hy+10}" rx="{hw*0.18}" ry="{hh*0.26}" fill="{skin}" {S(10)}/>')
    # head
    if kind == "bell":
        out.append(f'<path d="M{hx-hw*0.9} {hy+hh*0.85} C{hx-hw*0.95} {hy-hh*0.2} {hx-hw*0.55} {hy-hh*0.95} {hx} {hy-hh*0.98} C{hx+hw*0.55} {hy-hh*0.95} {hx+hw*0.95} {hy-hh*0.2} {hx+hw*0.9} {hy+hh*0.85} Q{hx} {hy+hh*1.1} {hx-hw*0.9} {hy+hh*0.85} Z" fill="url(#brass)" {S(12)}/>')
        out.append(f'<ellipse cx="{hx}" cy="{hy+hh*0.9}" rx="{hw*0.95}" ry="{hh*0.22}" fill="#6a4410" {S(10)}/>')
        out.append(f'<circle cx="{hx}" cy="{hy+hh*1.02}" r="{hw*0.16}" fill="url(#iron)" {S(8)}/>')
        out.append(f'<path d="M{hx+hw*0.2} {hy-hh*0.6} C{hx+hw*0.6} {hy-hh*0.4} {hx+hw*0.8} {hy+hh*0.2} {hx+hw*0.8} {hy+hh*0.7}" fill="none" stroke="url(#hatch)" stroke-width="60" opacity="0.5"/>')
        out.append(f'<circle cx="{hx}" cy="{hy-hh*1.05}" r="26" fill="url(#iron)" {S(8)}/>')
    else:
        fill = {"flesh": skin, "wood": "#d8a878", "brass": "url(#brass)", "ghost": "#bfe6f0", "snow": "#f2f6fb"}[kind]
        jaw = p.get("jaw", 1.0)
        out.append(f'<path d="M{hx-hw} {hy} C{hx-hw} {hy-hh*1.15} {hx+hw} {hy-hh*1.15} {hx+hw} {hy} C{hx+hw*jaw} {hy+hh*0.95} {hx+hw*0.35} {hy+hh*1.12} {hx} {hy+hh*1.1} C{hx-hw*0.35} {hy+hh*1.12} {hx-hw*jaw} {hy+hh*0.95} {hx-hw} {hy} Z" fill="{fill}" {S(12)} {"opacity=\"0.85\"" if kind=="ghost" else ""}/>')
        # shading hatch on right side
        out.append(f'<path d="M{hx+hw*0.35} {hy-hh*0.85} C{hx+hw*0.95} {hy-hh*0.6} {hx+hw*1.0} {hy+hh*0.5} {hx+hw*0.4} {hy+hh*1.0} C{hx+hw*0.75} {hy+hh*0.4} {hx+hw*0.75} {hy-hh*0.4} {hx+hw*0.35} {hy-hh*0.85} Z" fill="url(#hatch)" opacity="0.45"/>')
        if kind == "wood":
            for k in range(4):
                out.append(f'<path d="M{hx-hw*0.8+k*40} {hy-hh*0.8} q20 {hh*0.8} -10 {hh*1.6}" fill="none" stroke="#8a5a2e" stroke-width="4" opacity="0.6"/>')
            out.append(f'<circle cx="{hx-hw*0.55}" cy="{hy+hh*0.35}" r="34" fill="#e05a5a" opacity="0.8"/><circle cx="{hx+hw*0.55}" cy="{hy+hh*0.35}" r="34" fill="#e05a5a" opacity="0.8"/>')
        if kind == "brass":
            for (rx_, ry_) in ((-0.7, -0.5), (0.7, -0.5), (-0.75, 0.4), (0.75, 0.4)):
                out.append(f'<circle cx="{hx+hw*rx_}" cy="{hy+hh*ry_}" r="10" fill="#6a4410" {S(4)}/>')
    # warts, scars
    for (wx, wy) in p.get("warts", []):
        out.append(f'<circle cx="{hx+wx*hw}" cy="{hy+wy*hh}" r="13" fill="{skin_dk}" {S(5)}/>')
    if p.get("scar"):
        out.append(f'<path d="M{hx-hw*0.6} {hy-hh*0.55} l{hw*0.35} {hh*0.6}" stroke="{INK}" stroke-width="8"/>'
                   + "".join(f'<line x1="{hx-hw*0.6+hw*0.35*t-14}" y1="{hy-hh*0.55+hh*0.6*t+6}" x2="{hx-hw*0.6+hw*0.35*t+14}" y2="{hy-hh*0.55+hh*0.6*t-6}" stroke="{INK}" stroke-width="5"/>' for t in (0.25, 0.5, 0.75)))
    # eyes
    ey = hy - hh * 0.05
    esz = p.get("eye", 1.0)
    for sgn in (-1, 1):
        ex = hx + sgn * hw * 0.42
        if p.get("eye_glow"):
            out.append(f'<ellipse cx="{ex}" cy="{ey}" rx="{60*esz}" ry="{52*esz}" fill="{p["eye_glow"]}" filter="url(#glw)" opacity="0.9"/>')
        white = "#fff8e8" if not p.get("eye_glow") else "#ffe9a0"
        out.append(f'<ellipse cx="{ex}" cy="{ey}" rx="{56*esz}" ry="{60*esz}" fill="{white}" {S(9)}/>')
        iris = p.get("iris", "#3a6a9a")
        if p.get("button_eyes"):
            out.append(f'<circle cx="{ex}" cy="{ey}" r="{40*esz}" fill="#1a1012" {S(6)}/><circle cx="{ex-10}" cy="{ey-12}" r="8" fill="#fff"/>')
        else:
            out.append(f'<circle cx="{ex+sgn*-6}" cy="{ey+8}" r="{30*esz}" fill="{iris}" {S(5)}/>')
            pup = '<ellipse cx="{x}" cy="{y}" rx="7" ry="22" fill="#000"/>' if p.get("slit") else '<circle cx="{x}" cy="{y}" r="13" fill="#000"/>'
            out.append(pup.format(x=ex + sgn * -6, y=ey + 8))
            out.append(f'<circle cx="{ex-12}" cy="{ey-8}" r="8" fill="#fff"/>')
        # heavy brows
        brow = p.get("brow", "angry")
        if brow == "angry":
            out.append(f'<path d="M{ex-sgn*62} {ey-58*esz-10} L{ex+sgn*58} {ey-58*esz+22}" stroke="{p.get("brow_c", INK)}" stroke-width="22" stroke-linecap="round"/>')
        elif brow == "worried":
            out.append(f'<path d="M{ex-sgn*58} {ey-58*esz+16} Q{ex} {ey-80*esz} {ex+sgn*58} {ey-62*esz-6}" stroke="{p.get("brow_c", INK)}" stroke-width="16" fill="none" stroke-linecap="round"/>')
        elif brow == "kind":
            out.append(f'<path d="M{ex-58} {ey-62*esz} Q{ex} {ey-88*esz} {ex+58} {ey-62*esz}" stroke="{p.get("brow_c", INK)}" stroke-width="16" fill="none" stroke-linecap="round"/>')
        # bags
        out.append(f'<path d="M{ex-40} {ey+64*esz} q40 18 80 0" stroke="{INK}" stroke-width="4" fill="none" opacity="0.7"/>')
    if p.get("spectacles"):
        for sgn in (-1, 1):
            ex = hx + sgn * hw * 0.42
            out.append(f'<circle cx="{ex}" cy="{ey}" r="{70*esz}" fill="#cfe8ff" fill-opacity="0.15" stroke="{INK}" stroke-width="16"/><circle cx="{ex}" cy="{ey}" r="{70*esz}" fill="none" stroke="#d8aa52" stroke-width="7"/>')
        out.append(f'<path d="M{hx-hw*0.42+70*esz} {ey} q{hw*0.42-70*esz} -22 {(hw*0.42-70*esz)*2} 0" stroke="#d8aa52" stroke-width="7" fill="none"/>')
    # nose
    nose = p.get("nose", "bulb")
    ny = hy + hh * 0.3
    if nose == "bulb":
        out.append(f'<ellipse cx="{hx}" cy="{ny}" rx="{46}" ry="{38}" fill="{p.get("nose_c", skin_dk)}" {S(9)}/><circle cx="{hx-14}" cy="{ny-10}" r="8" fill="#fff" opacity="0.6"/>')
    elif nose == "hook":
        out.append(f'<path d="M{hx-10} {ny-70} C{hx+60} {ny-30} {hx+70} {ny+30} {hx+10} {ny+40} C{hx-10} {ny+42} {hx-20} {ny+20} {hx-4} {ny+10}" fill="{skin_dk}" {S(9)}/>')
    elif nose == "button":
        out.append(f'<circle cx="{hx}" cy="{ny}" r="16" fill="{skin_dk}" {S(6)}/>')
    elif nose == "carrot":
        out.append(f'<path d="M{hx-20} {ny-16} L{hx+150} {ny+10} L{hx-20} {ny+22} Z" fill="#e8701a" {S(8)}/>')
    # mouth
    my = hy + hh * 0.66
    mouth = p.get("mouth", "grin")
    mw = p.get("mouth_w", 1.0) * 120
    if mouth in ("grin", "fixed"):
        out.append(f'<path d="M{hx-mw} {my-20} Q{hx} {my+90} {hx+mw} {my-20} Q{hx} {my+20} {hx-mw} {my-20} Z" fill="#3a0608" {S(9)}/>')
        n = 7
        for i in range(n):
            tx = hx - mw * 0.8 + i * (mw * 1.6) / (n - 1)
            th = r.uniform(18, 30)
            out.append(f'<rect x="{tx-11}" y="{my-14 + abs(i-(n-1)/2)*-2}" width="22" height="{th:.0f}" rx="4" fill="#f4ecd0" {S(4)} transform="rotate({r.uniform(-12,12):.0f} {tx} {my})"/>')
        if mouth == "fixed":
            out.append(f'<path d="M{hx-mw-20} {my-34} q-14 20 6 34 M{hx+mw+20} {my-34} q14 20 -6 34" stroke="{INK}" stroke-width="7" fill="none"/>')
    elif mouth == "frown":
        out.append(f'<path d="M{hx-mw*0.7} {my+20} Q{hx} {my-30} {hx+mw*0.7} {my+20}" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/>')
    elif mouth == "smile":
        out.append(f'<path d="M{hx-mw*0.7} {my-10} Q{hx} {my+50} {hx+mw*0.7} {my-10}" stroke="{INK}" stroke-width="13" fill="none" stroke-linecap="round"/>')
    elif mouth == "o":
        out.append(f'<ellipse cx="{hx}" cy="{my}" rx="34" ry="42" fill="#3a0608" {S(9)}/>')
    elif mouth == "fangs":
        out.append(f'<path d="M{hx-mw} {my-20} Q{hx} {my+70} {hx+mw} {my-20} Z" fill="#3a0608" {S(9)}/>')
        out.append(f'<path d="M{hx-mw*0.6} {my-12} l14 40 l14 -38 M{hx+mw*0.6} {my-12} l-14 40 l-14 -38" fill="#f4ecd0" {S(5)}/>')
    if p.get("tears"):
        out.append(f'<path d="M{hx-hw*0.5} {ey+70} q-14 50 0 90 q14 -40 0 -90" fill="#8fd0ff" {S(5)}/>')
    if p.get("blush"):
        for sgn in (-1, 1):
            out.append(f'<ellipse cx="{hx+sgn*hw*0.62}" cy="{hy+hh*0.42}" rx="44" ry="24" fill="#e05a6a" opacity="0.55"/>')
    # beard
    beard = p.get("beard")
    if beard:
        bcol = p.get("beard_c", "#f2f2f0")
        size = {"huge": 1.0, "full": 0.75, "short": 0.45}[beard]
        pts = []
        n = 18
        for i in range(n + 1):
            a = math.pi * i / n
            rr = (hw * 1.05 + 260 * size) * (1 if i % 2 == 0 else 0.9)
            pts.append(f"{hx + math.cos(a) * rr * 0.8:.0f},{hy + hh*0.45 + math.sin(a) * rr * (0.55+size*0.4):.0f}")
        out.append(f'<polygon points="{hx-hw*0.95:.0f},{hy+hh*0.2:.0f} {" ".join(pts[::-1])} {hx+hw*0.95:.0f},{hy+hh*0.2:.0f}" fill="{bcol}" {S(11)}/>')
        for k in range(9):
            bx = hx - hw * 0.8 + k * hw * 0.2
            out.append(f'<path d="M{bx:.0f} {hy+hh*0.9:.0f} q{(k-4)*6} {120*size+40:.0f} {(k-4)*14} {220*size+60:.0f}" stroke="#9aa0aa" stroke-width="5" fill="none" opacity="0.7"/>')
        out.append(f'<path d="M{hx-hw*0.7} {my-40} Q{hx} {my-70} {hx+hw*0.7} {my-40}" fill="{bcol}" {S(10)}/>')  # moustache
        if p.get("beard_bells"):
            for i in range(6):
                bx = hx - 200 + i * 80
                out.append(f'<circle cx="{bx}" cy="{hy+hh*0.45 + 300*size*0.8 + (40 if i in (2,3) else 0)}" r="22" fill="url(#brass)" {S(6)}/>')
        if p.get("mouth_in_beard"):
            out.append(f'<path d="M{hx-mw*0.8} {my-6} Q{hx} {my+60} {hx+mw*0.8} {my-6} Z" fill="#3a0608" {S(8)}/>')
            for i in range(6):
                tx = hx - mw * 0.6 + i * mw * 0.24
                out.append(f'<rect x="{tx-10}" y="{my-4}" width="20" height="{r.uniform(18,26):.0f}" rx="3" fill="#f4ecd0" {S(3)}/>')
    # hair fringe / top
    if hair and p.get("hair_style") in ("fringe", "long", "messy", "bun"):
        out.append(f'<path d="M{hx-hw*1.02} {hy-hh*0.1} C{hx-hw*1.1} {hy-hh*1.3} {hx+hw*1.1} {hy-hh*1.3} {hx+hw*1.02} {hy-hh*0.1} C{hx+hw*0.7} {hy-hh*0.7} {hx+hw*0.2} {hy-hh*0.45} {hx} {hy-hh*0.7} C{hx-hw*0.3} {hy-hh*0.45} {hx-hw*0.7} {hy-hh*0.7} {hx-hw*1.02} {hy-hh*0.1} Z" fill="{hair}" {S(10)}/>')
        if p.get("hair_style") == "bun":
            out.append(f'<circle cx="{hx}" cy="{hy-hh*1.08}" r="{hw*0.38}" fill="{hair}" {S(10)}/>')
        if p.get("hair_style") == "messy":
            for k in range(7):
                a = math.pi * (1.1 + k * 0.12)
                out.append(f'<path d="M{hx+math.cos(a)*hw*0.9:.0f} {hy-hh*0.3+math.sin(a)*hh*0.8:.0f} l{math.cos(a)*60:.0f} {math.sin(a)*60:.0f}" stroke="{INK}" stroke-width="18" stroke-linecap="round"/><path d="M{hx+math.cos(a)*hw*0.9:.0f} {hy-hh*0.3+math.sin(a)*hh*0.8:.0f} l{math.cos(a)*60:.0f} {math.sin(a)*60:.0f}" stroke="{hair}" stroke-width="8" stroke-linecap="round"/>')
    # horns
    horns = p.get("horns")
    if horns == "curl":
        for sgn in (-1, 1):
            out.append(f'<path d="M{hx+sgn*hw*0.55} {hy-hh*0.8} C{hx+sgn*hw*1.1} {hy-hh*1.6} {hx+sgn*hw*1.75} {hy-hh*1.2} {hx+sgn*hw*1.45} {hy-hh*0.55} C{hx+sgn*hw*1.35} {hy-hh*0.95} {hx+sgn*hw*1.0} {hy-hh*1.1} {hx+sgn*hw*0.8} {hy-hh*0.6} Z" fill="#1c1418" {S(10)}/>')
            out.append(f'<path d="M{hx+sgn*hw*0.75} {hy-hh*1.0} C{hx+sgn*hw*1.1} {hy-hh*1.35} {hx+sgn*hw*1.45} {hy-hh*1.15} {hx+sgn*hw*1.45} {hy-hh*0.8}" stroke="#5a4a50" stroke-width="7" fill="none"/>')
    elif horns == "small":
        for sgn in (-1, 1):
            out.append(f'<path d="M{hx+sgn*hw*0.4} {hy-hh*0.85} Q{hx+sgn*hw*0.55} {hy-hh*1.45} {hx+sgn*hw*0.85} {hy-hh*1.5} Q{hx+sgn*hw*0.65} {hy-hh*1.1} {hx+sgn*hw*0.75} {hy-hh*0.7} Z" fill="#3a1418" {S(9)}/>')
    # hats
    hat = p.get("hat")
    hc = p.get("hat_c", "#8e1424")
    if hat == "santa":
        out.append(f'<path d="M{hx-hw*1.05} {hy-hh*0.55} C{hx-hw*0.7} {hy-hh*1.7} {hx+hw*0.6} {hy-hh*1.9} {hx+hw*1.5} {hy-hh*1.1} L{hx+hw*1.05} {hy-hh*0.55} Z" fill="{hc}" {S(12)}/>')
        out.append(f'<circle cx="{hx+hw*1.5}" cy="{hy-hh*1.05}" r="52" fill="#f2f2f0" {S(10)}/>')
        out.append(f'<rect x="{hx-hw*1.15}" y="{hy-hh*1.0}" width="{hw*2.3}" height="88" rx="44" fill="#f2f2f0" {S(11)}/>')
    elif hat == "elf":
        out.append(f'<path d="M{hx-hw*1.0} {hy-hh*0.55} L{hx-hw*0.2} {hy-hh*2.0} Q{hx+hw*0.9} {hy-hh*2.4} {hx+hw*1.2} {hy-hh*1.6} L{hx+hw*1.0} {hy-hh*0.55} Z" fill="{hc}" {S(12)}/>')
        out.append(f'<circle cx="{hx+hw*1.22}" cy="{hy-hh*1.55}" r="30" fill="url(#brass)" {S(8)}/>')
        out.append(f'<rect x="{hx-hw*1.1}" y="{hy-hh*0.72}" width="{hw*2.2}" height="70" rx="20" fill="#8e1424" {S(10)}/>')
    elif hat == "shako":
        out.append(f'<rect x="{hx-hw*0.85}" y="{hy-hh*2.0}" width="{hw*1.7}" height="{hh*1.4}" rx="20" fill="{hc}" {S(12)}/>')
        out.append(f'<rect x="{hx-hw*0.95}" y="{hy-hh*0.75}" width="{hw*1.9}" height="56" rx="12" fill="#1a1012" {S(10)}/>')
        out.append(f'<circle cx="{hx}" cy="{hy-hh*1.4}" r="42" fill="url(#brass)" {S(8)}/>')
        out.append(f'<path d="M{hx} {hy-hh*2.0} q-20 -90 30 -130 q-10 70 -30 130" fill="#e8c35a" {S(8)}/>')
    elif hat == "tophat":
        out.append(f'<rect x="{hx-hw*0.7}" y="{hy-hh*2.0}" width="{hw*1.4}" height="{hh*1.3}" rx="10" fill="#1a1418" {S(12)}/>')
        out.append(f'<rect x="{hx-hw*1.15}" y="{hy-hh*0.8}" width="{hw*2.3}" height="50" rx="20" fill="#1a1418" {S(11)}/>')
        out.append(f'<rect x="{hx-hw*0.7}" y="{hy-hh*1.0}" width="{hw*1.4}" height="40" fill="#8e1424" {S(6)}/>')
    elif hat == "helm":
        out.append(f'<path d="M{hx-hw*1.08} {hy-hh*0.05} C{hx-hw*1.1} {hy-hh*1.4} {hx+hw*1.1} {hy-hh*1.4} {hx+hw*1.08} {hy-hh*0.05} L{hx+hw*0.85} {hy-hh*0.3} L{hx-hw*0.85} {hy-hh*0.3} Z" fill="{hc}" {S(12)}/>')
        out.append(f'<rect x="{hx-18}" y="{hy-hh*1.2}" width="36" height="{hh*1.05}" fill="url(#brass)" {S(7)}/>')
    elif hat == "cap":
        out.append(f'<path d="M{hx-hw*1.05} {hy-hh*0.45} C{hx-hw*1.0} {hy-hh*1.35} {hx+hw*1.0} {hy-hh*1.35} {hx+hw*1.05} {hy-hh*0.45} Z" fill="{hc}" {S(12)}/>')
        out.append(f'<path d="M{hx-hw*1.15} {hy-hh*0.45} Q{hx} {hy-hh*0.25} {hx+hw*1.15} {hy-hh*0.45}" stroke="{INK}" stroke-width="40" fill="none"/><path d="M{hx-hw*1.15} {hy-hh*0.45} Q{hx} {hy-hh*0.25} {hx+hw*1.15} {hy-hh*0.45}" stroke="{hc}" stroke-width="26" fill="none"/>')
        if p.get("badge"):
            out.append(f'<circle cx="{hx}" cy="{hy-hh*0.85}" r="34" fill="url(#brass)" {S(7)}/>')
    elif hat == "candles":
        out.append(f'<path d="M{hx-hw*1.0} {hy-hh*0.6} Q{hx} {hy-hh*0.95} {hx+hw*1.0} {hy-hh*0.6}" stroke="{INK}" stroke-width="46" fill="none"/><path d="M{hx-hw*1.0} {hy-hh*0.6} Q{hx} {hy-hh*0.95} {hx+hw*1.0} {hy-hh*0.6}" stroke="#2f7a46" stroke-width="32" fill="none"/>')
        for i in range(5):
            cx = hx - hw * 0.8 + i * hw * 0.4
            cy = hy - hh * 0.75 - (30 if i in (1, 3) else (50 if i == 2 else 0))
            out.append(f'<rect x="{cx-14}" y="{cy-90}" width="28" height="90" fill="#f4ecd0" {S(6)}/><ellipse cx="{cx}" cy="{cy-110}" rx="14" ry="26" fill="#ffd27a" {S(4)}/><ellipse cx="{cx}" cy="{cy-110}" rx="30" ry="44" fill="#ffd27a" filter="url(#glw)" opacity="0.7"/>')
    elif hat == "veil":
        out.append(f'<path d="M{hx-hw*1.2} {hy+hh*1.2} C{hx-hw*1.3} {hy-hh*1.4} {hx+hw*1.3} {hy-hh*1.4} {hx+hw*1.2} {hy+hh*1.2} L{hx+hw*0.95} {hy+hh*0.3} C{hx+hw*0.95} {hy-hh*0.75} {hx-hw*0.95} {hy-hh*0.75} {hx-hw*0.95} {hy+hh*0.3} Z" fill="{hc}" {S(12)}/>')
        out.append(f'<path d="M{hx-hw*0.98} {hy-hh*0.3} Q{hx} {hy-hh*0.95} {hx+hw*0.98} {hy-hh*0.3}" stroke="#f4ecd0" stroke-width="22" fill="none"/>')
        if p.get("sun"):
            out.append(f'<circle cx="{hx}" cy="{hy-hh*0.85}" r="40" fill="#ffd27a" {S(7)}/>' + "".join(f'<line x1="{hx+math.cos(a)*50:.0f}" y1="{hy-hh*0.85+math.sin(a)*50:.0f}" x2="{hx+math.cos(a)*72:.0f}" y2="{hy-hh*0.85+math.sin(a)*72:.0f}" stroke="#ffd27a" stroke-width="9"/>' for a in [i*math.pi/4 for i in range(8)]))
    elif hat == "bandana":
        out.append(f'<path d="M{hx-hw*1.02} {hy-hh*0.35} C{hx-hw*1.0} {hy-hh*1.25} {hx+hw*1.0} {hy-hh*1.25} {hx+hw*1.02} {hy-hh*0.35} Z" fill="{hc}" {S(11)}/><path d="M{hx+hw*0.9} {hy-hh*0.45} l90 40 l-20 50 Z" fill="{hc}" {S(9)}/>')
    elif hat == "bonnet":
        out.append(f'<path d="M{hx-hw*1.15} {hy+hh*0.2} C{hx-hw*1.25} {hy-hh*1.4} {hx+hw*1.25} {hy-hh*1.4} {hx+hw*1.15} {hy+hh*0.2} C{hx+hw*0.9} {hy-hh*0.6} {hx-hw*0.9} {hy-hh*0.6} {hx-hw*1.15} {hy+hh*0.2} Z" fill="{hc}" {S(11)}/>')
    elif hat == "baker":
        out.append(f'<path d="M{hx-hw*0.8} {hy-hh*0.75} C{hx-hw*1.3} {hy-hh*1.6} {hx-hw*0.3} {hy-hh*2.1} {hx} {hy-hh*1.7} C{hx+hw*0.3} {hy-hh*2.1} {hx+hw*1.3} {hy-hh*1.6} {hx+hw*0.8} {hy-hh*0.75} Z" fill="#f4f0e6" {S(11)}/>')
        out.append(f'<rect x="{hx-hw*0.85}" y="{hy-hh*0.85}" width="{hw*1.7}" height="56" rx="10" fill="#f4f0e6" {S(10)}/>')
    elif hat == "witch":
        out.append(f'<path d="M{hx-hw*1.4} {hy-hh*0.55} Q{hx} {hy-hh*0.85} {hx+hw*1.4} {hy-hh*0.55} Q{hx} {hy-hh*0.25} {hx-hw*1.4} {hy-hh*0.55} Z" fill="{hc}" {S(11)}/>')
        out.append(f'<path d="M{hx-hw*0.75} {hy-hh*0.62} L{hx+hw*0.15} {hy-hh*2.3} Q{hx+hw*0.7} {hy-hh*2.15} {hx+hw*0.9} {hy-hh*1.6} Q{hx+hw*0.45} {hy-hh*1.7} {hx+hw*0.75} {hy-hh*0.62} Z" fill="{hc}" {S(12)}/>')
        out.append(f'<rect x="{hx-hw*0.78}" y="{hy-hh*0.86}" width="{hw*1.56}" height="46" fill="#8e1424" {S(8)}/>')
    elif hat in ("crown", "thorns"):
        n = 7
        pts = []
        for i in range(n * 2 + 1):
            x = hx - hw * 0.95 + i * hw * 1.9 / (n * 2)
            y = hy - hh * 0.65 - (hh * (0.75 if hat == "crown" else 0.6) if i % 2 else 0)
            pts.append(f"{x:.0f},{y:.0f}")
        col = hc if hat == "crown" else "#2a1418"
        out.append(f'<polygon points="{hx-hw*0.95:.0f},{hy-hh*0.45:.0f} {" ".join(pts)} {hx+hw*0.95:.0f},{hy-hh*0.45:.0f}" fill="{col}" {S(11)}/>')
        if hat == "thorns":
            for i in range(9):
                x = hx - hw * 0.85 + i * hw * 0.21
                out.append(f'<path d="M{x:.0f} {hy-hh*0.55:.0f} l{(-1)**i*26} -22" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
            out.append(f'<circle cx="{hx}" cy="{hy-hh*0.95}" r="30" fill="#c0183a" {S(7)}/>')
        else:
            for i in range(3):
                out.append(f'<circle cx="{hx-hw*0.5+i*hw*0.5}" cy="{hy-hh*0.6}" r="20" fill="{["#c0283a", "#2a8ad0", "#2fa046"][i]}" {S(6)}/>')
    # held item
    item = p.get("item")
    hand = skin if kind == "flesh" else ("#d8a878" if kind == "wood" else ("url(#brass)" if kind in ("brass", "bell") else skin))
    if p.get("gloves"):
        hand = p["gloves"]
    if item:
        out.append(item)
    grips = {}
    for side, gx, gy in re.findall(r"<!--(l?hand):(-?\d+),(-?\d+)-->", item or ""):
        grips[-1 if side == "lhand" else 1] = (int(gx), int(gy))
    for sgn in (-1, 1):
        hx2, hy2 = grips.get(sgn, (500 + sgn * bw * 0.72, 870))
        if p.get("hands", True):
            out.append(f'<ellipse cx="{hx2}" cy="{hy2}" rx="78" ry="70" fill="{hand}" {S(10)}/>'
                       + "".join(f'<path d="M{hx2-40+k*26} {hy2-48} q6 -34 18 0" fill="{hand}" {S(7)}/>' for k in range(4)))
    if p.get("over"):
        out.append(p["over"])
    return "".join(out)


# --------------------------------------------------------------------------- items held
def i_clipboard():
    return (f'<g transform="translate(660,780) rotate(14)"><rect x="-90" y="-120" width="180" height="230" rx="10" fill="url(#brass)" {S(10)}/>'
            f'<rect x="-70" y="-90" width="140" height="180" fill="#f4ecd0" {S(6)}/>'
            + "".join(f'<line x1="-55" y1="{-60+i*26}" x2="55" y2="{-60+i*26}" stroke="#8e1424" stroke-width="5"/>' for i in range(6))
            + f'<rect x="-36" y="-136" width="72" height="34" rx="8" fill="url(#iron)" {S(6)}/></g>')


def i_sack():
    return (f'<path d="M560 980 C520 760 640 560 860 600 C1000 640 1000 900 960 1000 Z" fill="#7a5a3a" {S(12)}/>'
            f'<path d="M640 640 q80 -60 160 -20" stroke="{INK}" stroke-width="10" fill="none"/>'
            f'<path d="M700 760 q60 40 140 10 M660 860 q90 50 210 0" stroke="#4a3220" stroke-width="7" fill="none"/>'
            f'<path d="M760 620 l-20 -60 l40 10 Z" fill="#c0283a" {S(6)}/>')


def i_baton():
    return f'<g transform="translate(720,760) rotate(-35)"><rect x="-20" y="-220" width="40" height="300" rx="16" fill="url(#iron)" {S(10)}/><circle cy="-230" r="38" fill="url(#brass)" {S(9)}/></g>'


def i_sabre():
    return f'<g transform="translate(740,800) rotate(-25)"><path d="M-14 -300 Q30 -150 14 40 L-14 40 Q0 -150 -14 -300 Z" fill="#dfe6ef" {S(9)}/><rect x="-48" y="40" width="96" height="22" rx="8" fill="url(#brass)" {S(8)}/><rect x="-14" y="62" width="28" height="70" fill="#5a3416" {S(8)}/></g>'


def i_staff(top="#ffd27a"):
    return f'<g transform="translate(270,760) rotate(10)"><rect x="-16" y="-420" width="32" height="560" rx="12" fill="#5a3416" {S(9)}/><circle cy="-440" r="46" fill="{top}" {S(9)}/><circle cy="-440" r="70" fill="{top}" filter="url(#glw)" opacity="0.6"/></g>'


def i_mace():
    return f'<g transform="translate(730,760) rotate(-30)"><rect x="-16" y="-160" width="32" height="300" rx="12" fill="#5a3416" {S(9)}/><circle cy="-190" r="70" fill="url(#brass)" {S(10)}/>' + "".join(f'<path d="M{math.cos(a)*60:.0f} {-190+math.sin(a)*60:.0f} l{math.cos(a)*40:.0f} {math.sin(a)*40:.0f}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><path d="M{math.cos(a)*60:.0f} {-190+math.sin(a)*60:.0f} l{math.cos(a)*40:.0f} {math.sin(a)*40:.0f}" stroke="#f0c868" stroke-width="9" stroke-linecap="round"/>' for a in [i*math.pi/4 for i in range(8)]) + '<circle cy="-190" r="110" fill="#fff2b0" filter="url(#glw2)" opacity="0.45"/></g>'


def i_sword(glow=None, rot=-20, x=740):
    g = f'<path d="M0 -380 L26 -330 L20 40 L-20 40 L-26 -330 Z" fill="{glow}" filter="url(#glw)" opacity="0.7"/>' if glow else ""
    return f'<g transform="translate({x},820) rotate({rot})">{g}<path d="M0 -380 L26 -330 L20 40 L-20 40 L-26 -330 Z" fill="#e9eef6" {S(9)}/><rect x="-80" y="40" width="160" height="28" rx="10" fill="url(#brass)" {S(8)}/><rect x="-16" y="68" width="32" height="90" fill="#3a2210" {S(8)}/></g>'


def i_maul():
    return f'<g transform="translate(720,760) rotate(-28)"><rect x="-18" y="-260" width="36" height="420" rx="12" fill="#5a3416" {S(9)}/><rect x="-120" y="-360" width="240" height="140" rx="18" fill="url(#iron)" {S(11)}/><rect x="-120" y="-310" width="240" height="30" fill="url(#brass)" {S(6)}/></g>'


def i_lute():
    return f'<g transform="translate(700,820) rotate(-30)"><ellipse cx="0" cy="40" rx="120" ry="150" fill="#b8762e" {S(11)}/><circle cy="40" r="36" fill="#2a1408" {S(7)}/><rect x="-22" y="-330" width="44" height="260" fill="#5a3416" {S(9)}/><rect x="-36" y="-370" width="72" height="60" rx="10" fill="#3a2210" {S(8)}/></g>'


def i_dagger():
    return f'<g transform="translate(720,830) rotate(-40)"><path d="M0 -220 L22 -180 L16 20 L-16 20 L-22 -180 Z" fill="#dfe6ef" {S(8)}/><rect x="-50" y="20" width="100" height="22" rx="8" fill="#5a2a6a" {S(7)}/><rect x="-14" y="42" width="28" height="70" fill="#2a1a12" {S(7)}/></g>'


def i_bread():
    return f'<g transform="translate(690,830) rotate(-10)"><path d="M-150 -40 Q-140 -120 0 -110 Q140 -120 150 -40 L130 80 L-130 80 Z" fill="#7a4a22" {S(10)}/>' + "".join(f'<ellipse cx="{x}" cy="-70" rx="60" ry="38" fill="#d89848" {S(7)}/>' for x in (-70, 10, 80)) + '</g>'


def i_quill():
    return f'<g transform="translate(700,770) rotate(25)"><path d="M0 120 C-40 0 -40 -180 40 -300 C60 -160 40 -40 0 120 Z" fill="#1a1418" {S(9)}/><line x1="0" y1="120" x2="20" y2="-260" stroke="#8e1424" stroke-width="5"/><path d="M0 120 l-8 40 l16 0 Z" fill="#d8aa52" {S(5)}/></g>'


def i_tankard():
    return f'<g transform="translate(700,820)"><rect x="-80" y="-110" width="160" height="200" rx="18" fill="#9a9aa6" {S(10)}/><path d="M80 -70 q70 0 70 60 q0 60 -70 60" fill="none" stroke="{INK}" stroke-width="26"/><path d="M80 -70 q70 0 70 60 q0 60 -70 60" fill="none" stroke="#9a9aa6" stroke-width="12"/><ellipse cy="-110" rx="86" ry="30" fill="#f2ecd8" {S(8)}/></g>'


def i_scroll():
    return f'<g transform="translate(680,820) rotate(-12)"><rect x="-150" y="-100" width="300" height="200" fill="#efe2c0" {S(9)}/><rect x="-170" y="-120" width="40" height="240" rx="18" fill="#c9a86a" {S(8)}/><rect x="130" y="-120" width="40" height="240" rx="18" fill="#c9a86a" {S(8)}/>' + "".join(f'<line x1="-110" y1="{-60+i*30}" x2="110" y2="{-60+i*30}" stroke="#5a1a1a" stroke-width="5"/>' for i in range(5)) + '</g>'


def i_spear():
    return f'<g transform="translate(760,700) rotate(-8)"><rect x="-12" y="-560" width="24" height="760" fill="#5a3416" {S(8)}/><path d="M0 -660 L36 -560 L-36 -560 Z" fill="#dfe6ef" {S(8)}/></g>'


def i_present():
    return f'<g transform="translate(700,840) rotate(8)"><rect x="-110" y="-110" width="220" height="200" rx="8" fill="#2f7a46" {S(10)}/><rect x="-20" y="-110" width="40" height="200" fill="#e8c35a" {S(6)}/><path d="M0 -110 q-80 -90 -100 -20 q60 10 100 20 q80 -90 100 -20 q-60 10 -100 20" fill="#e8c35a" {S(7)}/></g>'


# --------------------------------------------------------------------------- grips: the hand sits on the handle, never mid-item
def _grip(tx, ty, rot, lx, ly, side="hand"):
    a = math.radians(rot)
    return f"<!--{side}:{tx + lx * math.cos(a) - ly * math.sin(a):.0f},{ty + lx * math.sin(a) + ly * math.cos(a):.0f}-->"


def _held(fn, tx, ty, rot, lx, ly, side="hand"):
    def w(*a, **k):
        return fn(*a, **k) + _grip(tx, ty, rot, lx, ly, side)
    w.__name__ = fn.__name__
    return w


i_clipboard = _held(i_clipboard, 660, 780, 14, 92, 20)
i_sack = _held(i_sack, 720, 610, 0, 0, 0)
i_baton = _held(i_baton, 720, 760, -35, 0, 40)
i_sabre = _held(i_sabre, 740, 800, -25, 0, 97)
i_staff = _held(i_staff, 270, 760, 10, 0, 60, "lhand")
i_mace = _held(i_mace, 730, 760, -30, 0, 90)
i_maul = _held(i_maul, 720, 760, -28, 0, 110)
i_lute = _held(i_lute, 700, 820, -30, 0, -200)
i_dagger = _held(i_dagger, 720, 830, -40, 0, 77)
i_bread = _held(i_bread, 690, 830, -10, 0, 95)
i_quill = _held(i_quill, 700, 770, 25, 0, 60)
i_tankard = _held(i_tankard, 700, 820, 0, 118, -10)
i_scroll = _held(i_scroll, 680, 820, -12, 150, 20)
i_spear = _held(i_spear, 760, 700, -8, 0, 130)
i_present = _held(i_present, 700, 840, 8, 70, 90)
_i_sword = i_sword


def i_sword(glow=None, rot=-20, x=740):
    return _i_sword(glow, rot, x) + _grip(x, 820, rot, 0, 113)


# --------------------------------------------------------------------------- non-humanoids
def reindeer(body, eye, antler="#3a2614", flame=False, mech=False):
    out = []
    out.append(f'<path d="M180 1000 C160 760 300 640 500 640 C700 640 840 760 820 1000 Z" fill="{body}" {S(12)}/>')
    # antlers
    for sgn in (-1, 1):
        base = (500 + sgn * 130, 260)
        out.append(f'<path d="M{base[0]} {base[1]} C{500+sgn*200} 160 {500+sgn*260} 120 {500+sgn*330} 40 M{500+sgn*215} 165 l{sgn*-20} -110 M{500+sgn*270} 105 l{sgn*90} -40 M{500+sgn*300} 70 l{sgn*-10} -60" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round"/>')
        out.append(f'<path d="M{base[0]} {base[1]} C{500+sgn*200} 160 {500+sgn*260} 120 {500+sgn*330} 40 M{500+sgn*215} 165 l{sgn*-20} -110 M{500+sgn*270} 105 l{sgn*90} -40 M{500+sgn*300} 70 l{sgn*-10} -60" fill="none" stroke="{antler}" stroke-width="22" stroke-linecap="round"/>')
        if flame:
            for (fx, fy) in ((500 + sgn * 330, 40), (500 + sgn * 195, 55), (500 + sgn * 360, 65)):
                out.append(f'<ellipse cx="{fx}" cy="{fy-30}" rx="40" ry="70" fill="#ff7a1a" filter="url(#glw)" opacity="0.9"/><path d="M{fx-26} {fy} Q{fx-30} {fy-60} {fx} {fy-110} Q{fx+30} {fy-60} {fx+26} {fy} Z" fill="#ffb03a" {S(6)}/>')
    # ears
    for sgn in (-1, 1):
        out.append(f'<path d="M{500+sgn*150} 330 L{500+sgn*290} 280 L{500+sgn*170} 400 Z" fill="{body}" {S(10)}/>')
    # head (long muzzle)
    out.append(f'<path d="M330 330 C330 200 670 200 670 330 C690 470 620 640 500 660 C380 640 310 470 330 330 Z" fill="{body}" {S(12)}/>')
    out.append(f'<path d="M560 260 C660 300 670 470 590 600" fill="none" stroke="url(#hatch)" stroke-width="70" opacity="0.5"/>')
    if mech:
        for (x, y) in ((380, 300), (620, 300), (400, 520), (600, 520)):
            out.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#3b2a0c" {S(4)}/>')
        out.append(f'<circle cx="500" cy="300" r="40" fill="url(#iron)" {S(7)}/>' + "".join(f'<line x1="500" y1="300" x2="{500+math.cos(a)*40:.0f}" y2="{300+math.sin(a)*40:.0f}" stroke="{INK}" stroke-width="5"/>' for a in [i*math.pi/3 for i in range(6)]))
    for sgn in (-1, 1):
        out.append(f'<ellipse cx="{500+sgn*95}" cy="380" rx="52" ry="58" fill="{eye}" filter="url(#glw)" opacity="0.9"/><ellipse cx="{500+sgn*95}" cy="380" rx="44" ry="50" fill="#fff2b0" {S(8)}/><ellipse cx="{500+sgn*95}" cy="388" rx="12" ry="32" fill="#000"/>')
    out.append(f'<ellipse cx="500" cy="590" rx="80" ry="58" fill="#c0283a" {S(10)}/><circle cx="478" cy="572" r="14" fill="#fff" opacity="0.6"/>')
    out.append(f'<path d="M420 640 Q500 700 580 640" stroke="{INK}" stroke-width="10" fill="none"/>')
    out.append(f'<path d="M300 760 Q500 840 700 760" stroke="{INK}" stroke-width="40" fill="none"/><path d="M300 760 Q500 840 700 760" stroke="#8e1424" stroke-width="26" fill="none"/>')
    for x in (360, 430, 500, 570, 640):
        out.append(f'<circle cx="{x}" cy="{805 - abs(x-500)*0.25:.0f}" r="22" fill="url(#brass)" {S(6)}/>')
    return "".join(out)


def snowman_p():
    return humanoid(dict(kind="snow", skin="#f2f6fb", skin_dk="#c8d4e2", coat="#eef3f8", coat_dk="#c8d4e2", ears="none",
                         nose="carrot", mouth="o", hat="tophat", button_eyes=True, brow="worried", body_w=330,
                         hands=False, over=f'<path d="M260 700 Q500 800 740 700" stroke="{INK}" stroke-width="70" fill="none"/><path d="M260 700 Q500 800 740 700" stroke="#c0283a" stroke-width="54" fill="none"/>'
                                                         + "".join(f'<circle cx="500" cy="{y}" r="22" fill="#1a1418"/>' for y in (850, 940))
                                                         + f'<path d="M190 760 l-120 -160 M150 700 l-60 -10 M810 760 l120 -160 M850 700 l60 -10" stroke="#3a2614" stroke-width="16" stroke-linecap="round"/>'))


def writ(numeral, color):
    return (f'<rect x="210" y="130" width="580" height="740" fill="{color}" filter="url(#glw2)" opacity="0.5"/>'
            f'<rect x="200" y="120" width="600" height="760" rx="10" fill="none" stroke="{INK}" stroke-width="54"/>'
            f'<rect x="200" y="120" width="600" height="760" rx="10" fill="none" stroke="url(#brass)" stroke-width="34"/>'
            f'<path d="M270 190 h460 v560 q-40 60 -120 20 q-80 -40 -150 10 q-90 60 -190 -10 Z" fill="#efe2c0" {S(10)}/>'
            f'<text x="500" y="320" font-family="Cinzel Decorative" font-weight="900" font-size="140" text-anchor="middle" fill="#8e1424" stroke="{INK}" stroke-width="5">{numeral}</text>'
            + "".join(f'<line x1="320" y1="{380+i*48}" x2="{680 - (i%3)*50}" y2="{380+i*48}" stroke="#5a1a1a" stroke-width="9"/>' for i in range(6))
            + f'<circle cx="620" cy="700" r="70" fill="#8e1424" {S(10)}/><path d="M620 650 l20 40 l-40 0 Z M620 750 l20 -40 l-40 0 Z" fill="#ffd27a"/>'
            + f'<ellipse cx="400" cy="560" rx="160" ry="200" fill="url(#hatch2)" opacity="0.15"/>')


def ledger_p():
    return (f'<ellipse cx="500" cy="720" rx="380" ry="200" fill="#ff5a1a" filter="url(#glw2)" opacity="0.7"/>'
            + "".join(f'<line x1="{x}" y1="0" x2="{x2}" y2="420" stroke="{INK}" stroke-width="30" stroke-dasharray="44 14"/><line x1="{x}" y1="0" x2="{x2}" y2="420" stroke="#8a8590" stroke-width="16" stroke-dasharray="44 14"/>' for x, x2 in ((180, 260), (820, 740)))
            + f'<path d="M140 420 L500 470 L860 420 L860 760 L500 820 L140 760 Z" fill="#5e0b18" {S(14)}/>'
            + f'<path d="M170 430 L500 480 L500 790 L170 740 Z" fill="#efe2c0" {S(10)}/><path d="M830 430 L500 480 L500 790 L830 740 Z" fill="#f4ead0" {S(10)}/>'
            + "".join(f'<line x1="210" y1="{500+i*34}" x2="460" y2="{535+i*34}" stroke="#5a1a1a" stroke-width="6"/><line x1="540" y1="{535+i*34}" x2="790" y2="{500+i*34}" stroke="#5a1a1a" stroke-width="6"/>' for i in range(7))
            + f'<rect x="300" y="860" width="400" height="80" rx="20" fill="#1a0806" {S(10)}/>')


def engine_p():
    import props as pr
    return (f'<g transform="translate(500,520) scale(1.3)">{pr.clock_face(300, (11, 59))}</g>'
            f'<g transform="translate(500,160) scale(0.9)">{pr.trapped_sun(95)}</g>')


def lock_p():
    return (f'<rect x="230" y="260" width="540" height="560" rx="40" fill="url(#iron)" {S(16)}/>'
            f'<circle cx="500" cy="480" r="150" fill="url(#brass)" {S(14)}/>'
            + "".join(f'<rect x="{500+math.cos(a)*150-22:.0f}" y="{480+math.sin(a)*150-22:.0f}" width="44" height="44" fill="url(#brass)" {S(6)} transform="rotate({math.degrees(a):.0f} {500+math.cos(a)*150:.0f} {480+math.sin(a)*150:.0f})"/>' for a in [i*math.pi/6 for i in range(12)])
            + f'<path d="M470 460 a30 30 0 1 1 60 0 l-12 120 h-36 Z" fill="#120909"/>'
            + f'<text x="500" y="760" font-family="Cinzel" font-weight="900" font-size="64" text-anchor="middle" fill="#ff6a5a" stroke="{INK}" stroke-width="4">RESTRICTED</text>')


def seam_p():
    return (i_sack().replace('M560 980 C520 760 640 560 860 600 C1000 640 1000 900 960 1000 Z', 'M160 980 C100 500 400 220 640 260 C900 300 960 700 860 980 Z')
            + "".join(f'<path d="M{400+i*60} {380+i*80} l60 30" stroke="{INK}" stroke-width="12"/><path d="M{430+i*60} {370+i*80} l-10 60" stroke="#e8c35a" stroke-width="8"/>' for i in range(6))
            + f'<path d="M460 430 Q540 600 520 860" stroke="#ff4a3a" stroke-width="8" fill="none" stroke-dasharray="20 14"/>')


def arbiter_p():
    import props as pr
    return (humanoid(dict(kind="brass", coat="#3a2614", coat_dk="#1a0c06", ears="none", nose="none", mouth="frown", brow="none",
                          eye_glow="#ffd27a", iris="#ffd27a", body_w=330, hy=470, trim="#b8862e", hands=True, gloves="url(#brass)",
                          hat="helm", hat_c="url(#brass)"))
            + f'<g transform="translate(500,160) scale(2.2)">{pr.scales()}</g>')


def engine_drone():
    return (f'<path d="M150 700 Q160 470 500 450 Q840 470 850 700 Q700 860 500 860 Q300 860 150 700 Z" fill="#8e1424" {S(14)}/>'
            f'<path d="M150 700 L850 700" stroke="url(#brass)" stroke-width="24"/>'
            + "".join(f'<g transform="translate({x},420)"><circle r="120" fill="url(#brass)" {S(10)}/>' + "".join(f'<rect x="-14" y="-140" width="28" height="40" fill="url(#brass)" {S(5)} transform="rotate({k*30})"/>' for k in range(12)) + f'<circle r="40" fill="url(#iron)" {S(7)}/></g>' for x in (200, 800))
            + f'<circle cx="500" cy="600" r="110" fill="url(#iron)" {S(12)}/><circle cx="500" cy="600" r="70" fill="#ffd27a" {S(8)}/><circle cx="500" cy="600" r="120" fill="#ffd27a" filter="url(#glw2)" opacity="0.6"/>'
            + f'<rect x="420" y="780" width="160" height="110" rx="20" fill="url(#iron)" {S(10)}/><circle cx="500" cy="840" r="32" fill="#120909"/>')


# --------------------------------------------------------------------------- overhead tokens
def token_overhead(t):
    """True 90-degree overhead view. t: dict with shoulders, coat, head, cap, horns, beard, item, size."""
    out = [f'<ellipse cx="500" cy="530" rx="400" ry="380" fill="#000" opacity="0.38" filter="url(#glw)"/>']
    sw = t.get("shoulders", 300)
    coat = t.get("coat", "#8e1424")
    if t.get("sack"):
        out.append(f'<ellipse cx="500" cy="{500 - sw*0.75:.0f}" rx="{sw*0.85:.0f}" ry="{sw*0.6:.0f}" fill="#7a5a3a" {S(14)}/><path d="M{500-sw*0.4:.0f} {500-sw*0.75:.0f} q{sw*0.4:.0f} 50 {sw*0.8:.0f} 0" stroke="#4a3220" stroke-width="10" fill="none"/>')
    if t.get("cape"):
        out.append(f'<path d="M{500-sw*1.05} 470 Q500 {470-sw*1.0} {500+sw*1.05} 470 Q{500+sw*0.9} {470+sw*0.6} 500 {470+sw*0.4} Q{500-sw*0.9} {470+sw*0.6} {500-sw*1.05} 470 Z" fill="{t["cape"]}" {S(12)}/>')
    # arms + hands
    hand = t.get("hand", "#e8b496")
    for sgn in (-1, 1):
        out.append(f'<ellipse cx="{500+sgn*sw*0.95:.0f}" cy="540" rx="{sw*0.22:.0f}" ry="{sw*0.38:.0f}" fill="{coat}" {S(12)}/>')
        out.append(f'<circle cx="{500+sgn*sw*0.95:.0f}" cy="{540+sw*0.42:.0f}" r="{sw*0.19:.0f}" fill="{hand}" {S(10)}/>')
    if t.get("item"):
        out.append(t["item"])
    out.append(f'<ellipse cx="500" cy="500" rx="{sw:.0f}" ry="{sw*0.55:.0f}" fill="{coat}" {S(14)}/>')
    out.append(f'<path d="M{500+sw*0.2:.0f} {500-sw*0.5:.0f} Q{500+sw*0.95:.0f} {500-sw*0.3:.0f} {500+sw*0.85:.0f} {500+sw*0.25:.0f} Q{500+sw*0.4:.0f} {500+sw*0.5:.0f} {500+sw*0.2:.0f} {500-sw*0.5:.0f} Z" fill="url(#hatch)" opacity="0.45"/>')
    if t.get("trim"):
        out.append(f'<ellipse cx="500" cy="500" rx="{sw*0.98:.0f}" ry="{sw*0.53:.0f}" fill="none" stroke="{t["trim"]}" stroke-width="22"/>')
    if t.get("beard"):
        out.append(f'<path d="M{500-sw*0.42:.0f} 560 Q500 {560+sw*0.85:.0f} {500+sw*0.42:.0f} 560 Z" fill="{t.get("beard_c","#f2f2f0")}" {S(11)}/>')
    hr = t.get("head", 170)
    hc = t.get("head_c", "#5a3a22")
    out.append(f'<circle cx="500" cy="490" r="{hr}" fill="{hc}" {S(14)}/>')
    # face edge peeking at the bottom (token faces down)
    if t.get("face", True):
        out.append(f'<path d="M{500-hr*0.62:.0f} {490+hr*0.72:.0f} Q500 {490+hr*1.12:.0f} {500+hr*0.62:.0f} {490+hr*0.72:.0f}" fill="{t.get("skin","#e8b496")}" {S(10)}/>')
        out.append(f'<ellipse cx="500" cy="{490+hr*0.98:.0f}" rx="{hr*0.16:.0f}" ry="{hr*0.13:.0f}" fill="{t.get("nose_c", t.get("skin_dk","#b47a5e"))}" {S(7)}/>')
    cap = t.get("cap")
    if cap == "santa":
        out.append(f'<circle cx="500" cy="490" r="{hr*0.95:.0f}" fill="#8e1424" {S(10)}/><circle cx="500" cy="490" r="{hr*1.0:.0f}" fill="none" stroke="#f2f2f0" stroke-width="30"/><circle cx="{500+hr*0.35:.0f}" cy="{490-hr*0.4:.0f}" r="{hr*0.32:.0f}" fill="#f2f2f0" {S(8)}/>')
    elif cap == "elf":
        out.append(f'<circle cx="500" cy="490" r="{hr*0.95:.0f}" fill="#2f7a46" {S(10)}/><path d="M500 490 L{500+hr*0.3:.0f} {490-hr*1.6:.0f}" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M500 490 L{500+hr*0.3:.0f} {490-hr*1.6:.0f}" stroke="#2f7a46" stroke-width="24" stroke-linecap="round"/><circle cx="{500+hr*0.3:.0f}" cy="{490-hr*1.6:.0f}" r="22" fill="url(#brass)" {S(6)}/>')
    elif cap == "shako":
        out.append(f'<circle cx="500" cy="490" r="{hr*1.02:.0f}" fill="#1a1012" {S(10)}/><circle cx="500" cy="490" r="{hr*0.75:.0f}" fill="{t.get("cap_c","#2c4f8a")}" {S(8)}/><circle cx="500" cy="490" r="{hr*0.25:.0f}" fill="#e8c35a" {S(6)}/>')
    elif cap == "bell":
        out.append(f'<circle cx="500" cy="490" r="{hr:.0f}" fill="url(#brass)" {S(12)}/><circle cx="500" cy="490" r="{hr*0.55:.0f}" fill="none" stroke="#6a4410" stroke-width="12"/><circle cx="500" cy="490" r="{hr*0.2:.0f}" fill="url(#iron)" {S(7)}/>')
    elif cap == "tophat":
        out.append(f'<circle cx="500" cy="490" r="{hr*1.15:.0f}" fill="#1a1418" {S(10)}/><circle cx="500" cy="490" r="{hr*0.7:.0f}" fill="#26222a" {S(8)}/><circle cx="500" cy="490" r="{hr*0.78:.0f}" fill="none" stroke="#8e1424" stroke-width="16"/>')
    elif cap == "helm":
        out.append(f'<circle cx="500" cy="490" r="{hr:.0f}" fill="{t.get("cap_c","#8a8f99")}" {S(12)}/><rect x="485" y="{490-hr:.0f}" width="30" height="{hr*1.4:.0f}" fill="url(#brass)" {S(6)}/>')
    elif cap == "veil":
        out.append(f'<ellipse cx="500" cy="470" rx="{hr*1.15:.0f}" ry="{hr*1.25:.0f}" fill="{t.get("cap_c","#f4ecd0")}" {S(10)}/><circle cx="500" cy="{490-hr*0.2:.0f}" r="{hr*0.32:.0f}" fill="#ffd27a" {S(7)}/>')
    elif cap == "candles":
        out.append(f'<circle cx="500" cy="490" r="{hr*0.95:.0f}" fill="#2f7a46" {S(10)}/>' + "".join(f'<circle cx="{500+math.cos(a)*hr*0.65:.0f}" cy="{490+math.sin(a)*hr*0.65:.0f}" r="26" fill="#ffd27a" {S(6)}/><circle cx="{500+math.cos(a)*hr*0.65:.0f}" cy="{490+math.sin(a)*hr*0.65:.0f}" r="44" fill="#ffd27a" filter="url(#glw)" opacity="0.7"/>' for a in [i*2*math.pi/5 for i in range(5)]))
    elif cap == "cap":
        out.append(f'<circle cx="500" cy="490" r="{hr*0.98:.0f}" fill="{t.get("cap_c","#2f5a3a")}" {S(10)}/><path d="M{500-hr*0.8:.0f} {490+hr*0.55:.0f} Q500 {490+hr*1.1:.0f} {500+hr*0.8:.0f} {490+hr*0.55:.0f}" fill="{t.get("cap_c","#2f5a3a")}" {S(8)}/>')
    elif cap == "baker":
        out.append(f'<circle cx="500" cy="480" r="{hr*1.05:.0f}" fill="#f4f0e6" {S(10)}/>' + "".join(f'<circle cx="{500+math.cos(a)*hr*0.5:.0f}" cy="{480+math.sin(a)*hr*0.5:.0f}" r="{hr*0.45:.0f}" fill="#f4f0e6" {S(6)}/>' for a in [i*math.pi/3 for i in range(6)]))
    elif cap == "hair":
        out.append(f'<circle cx="500" cy="485" r="{hr*0.98:.0f}" fill="{t.get("cap_c","#3a2414")}" {S(10)}/>' + "".join(f'<path d="M500 490 L{500+math.cos(a)*hr*0.95:.0f} {490+math.sin(a)*hr*0.95:.0f}" stroke="{INK}" stroke-width="4" opacity="0.5"/>' for a in [i*math.pi/8 for i in range(16)]))
        if t.get("bun"):
            out.append(f'<circle cx="500" cy="{490-hr*0.3:.0f}" r="{hr*0.4:.0f}" fill="{t.get("cap_c")}" {S(8)}/>')
    elif cap == "hood":
        out.append(f'<ellipse cx="500" cy="480" rx="{hr*1.1:.0f}" ry="{hr*1.2:.0f}" fill="{t.get("cap_c","#3a2a4a")}" {S(10)}/>')
    if t.get("horns"):
        for sgn in (-1, 1):
            out.append(f'<path d="M{500+sgn*hr*0.55:.0f} {490-hr*0.55:.0f} C{500+sgn*hr*1.3:.0f} {490-hr*1.2:.0f} {500+sgn*hr*1.7:.0f} {490-hr*0.4:.0f} {500+sgn*hr*1.3:.0f} {490+hr*0.2:.0f} C{500+sgn*hr*1.25:.0f} {490-hr*0.3:.0f} {500+sgn*hr*1.0:.0f} {490-hr*0.6:.0f} {500+sgn*hr*0.75:.0f} {490-hr*0.3:.0f} Z" fill="#1c1418" {S(10)}/>')
    if t.get("ears") == "pointed":
        for sgn in (-1, 1):
            out.append(f'<path d="M{500+sgn*hr*0.85:.0f} 480 L{500+sgn*hr*1.55:.0f} 440 L{500+sgn*hr*0.9:.0f} 540 Z" fill="{t.get("skin","#e8b496")}" {S(8)}/>')
    if t.get("over"):
        out.append(t["over"])
    return "".join(out)


def ot_item(kind, side=1, color=None):
    x = 500 + side * 300
    if kind == "sword":
        return f'<g transform="translate({x},640)"><path d="M0 0 L16 300 L0 340 L-16 300 Z" fill="{color or "#e9eef6"}" {S(8)}/><rect x="-60" y="-10" width="120" height="22" rx="8" fill="url(#brass)" {S(6)}/></g>'
    if kind == "staff":
        return f'<g transform="translate({x},640)"><rect x="-14" y="-300" width="28" height="560" rx="10" fill="#5a3416" {S(7)}/><circle cy="-310" r="40" fill="{color or "#ffd27a"}" {S(7)}/></g>'
    if kind == "baton":
        return f'<g transform="translate({x},640) rotate(20)"><rect x="-18" y="0" width="36" height="260" rx="14" fill="url(#iron)" {S(8)}/><circle cy="270" r="32" fill="url(#brass)" {S(7)}/></g>'
    if kind == "maul":
        return f'<g transform="translate({x},640) rotate(10)"><rect x="-14" y="0" width="28" height="260" fill="#5a3416" {S(7)}/><rect x="-80" y="250" width="160" height="90" rx="12" fill="url(#iron)" {S(9)}/></g>'
    if kind == "clipboard":
        return f'<g transform="translate({x},660) rotate(15)"><rect x="-70" y="-90" width="140" height="180" rx="8" fill="url(#brass)" {S(8)}/><rect x="-55" y="-70" width="110" height="140" fill="#f4ecd0" {S(5)}/></g>'
    if kind == "lute":
        return f'<g transform="translate({x},660) rotate(25)"><ellipse rx="90" ry="110" fill="#b8762e" {S(9)}/><rect x="-16" y="-260" width="32" height="170" fill="#5a3416" {S(7)}/></g>'
    if kind == "spear":
        return f'<g transform="translate({x},500)"><rect x="-10" y="-380" width="20" height="760" fill="#5a3416" {S(6)}/><path d="M0 410 L26 340 L-26 340 Z" fill="#dfe6ef" {S(6)}/></g>'
    if kind == "basket":
        return f'<g transform="translate({x},680)"><ellipse rx="110" ry="80" fill="#a87a3a" {S(9)}/><ellipse rx="80" ry="54" fill="#d89848" {S(6)}/></g>'
    if kind == "lantern":
        return f'<g transform="translate({x},680)"><circle r="90" fill="#ffd27a" filter="url(#glw)" opacity="0.8"/><circle r="50" fill="#ffd27a" {S(8)}/></g>'
    return ""
