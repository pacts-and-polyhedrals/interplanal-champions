"""Ink-style icons for items, abilities, spells, macros and tables (256 px)."""
import math
from chibi import render, INK, DEFS

OUT = "/home/claude/ic/module/assets/icons"


def S(w=8):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


G = {}


def glyph(fn):
    G[fn.__name__] = fn
    return fn


@glyph
def bell(c="#e8c35a"):
    return (f'<path d="M128 40 C80 40 70 90 70 130 C70 160 52 172 46 186 L210 186 C204 172 186 160 186 130 C186 90 176 40 128 40 Z" fill="{c}" {S()}/>'
            f'<circle cx="128" cy="200" r="16" fill="#3a3640" {S(6)}/><circle cx="128" cy="34" r="10" fill="{c}" {S(5)}/>'
            f'<path d="M150 70 Q170 100 168 150" stroke="#fff" stroke-width="7" fill="none" opacity="0.5"/>')


@glyph
def scarf(c="#c0283a"):
    return (f'<path d="M50 70 Q128 110 206 70 L206 100 Q128 140 50 100 Z" fill="{c}" {S()}/>'
            f'<path d="M150 104 L170 220 L130 220 L120 112 Z" fill="{c}" {S()}/>'
            + "".join(f'<line x1="{x}" y1="{82+ (x-50)*0.0}" x2="{x}" y2="{110}" stroke="#f2f2f0" stroke-width="8"/>' for x in (80, 110, 140, 170))
            + "".join(f'<line x1="{132+i*9}" y1="220" x2="{132+i*9}" y2="236" stroke="{INK}" stroke-width="5"/>' for i in range(5)))


@glyph
def candycane(c="#c0283a"):
    d = "M150 222 L150 90 A40 40 0 0 0 70 90"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#f4efe4" stroke-width="30" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="30" stroke-dasharray="16 18"/>')


@glyph
def star(c="#ffd84a"):
    pts = " ".join(f"{128+math.cos(i*math.pi/5-math.pi/2)*(96 if i%2==0 else 40):.1f},{132+math.sin(i*math.pi/5-math.pi/2)*(96 if i%2==0 else 40):.1f}" for i in range(10))
    return f'<polygon points="{pts}" fill="{c}" {S()}/><circle cx="128" cy="132" r="14" fill="#fff" opacity="0.6"/>'


@glyph
def mirror(c="#7ac0e0"):
    return (f'<rect x="114" y="160" width="28" height="80" rx="8" fill="#5a3416" {S(7)}/>'
            f'<ellipse cx="128" cy="100" rx="70" ry="80" fill="#2f7a46" {S()}/><ellipse cx="128" cy="100" rx="52" ry="62" fill="{c}" {S(6)}/>'
            f'<path d="M100 70 l30 -20" stroke="#fff" stroke-width="9" opacity="0.7"/>')


@glyph
def candle(c="#ffd27a"):
    return (f'<ellipse cx="128" cy="62" rx="40" ry="56" fill="{c}" opacity="0.45"/>'
            f'<rect x="96" y="100" width="64" height="110" fill="#f4ecd0" {S()}/><path d="M118 60 Q128 30 138 60 Q140 84 128 90 Q116 84 118 60 Z" fill="{c}" {S(6)}/>'
            f'<rect x="70" y="206" width="116" height="24" rx="10" fill="#c09040" {S(7)}/>')


@glyph
def stocking(c="#c0283a"):
    return (f'<path d="M90 40 L160 40 L160 150 Q160 216 100 216 Q60 216 60 186 Q60 160 96 156 Z" fill="{c}" {S()}/>'
            f'<rect x="80" y="30" width="90" height="40" rx="14" fill="#f2f2f0" {S(7)}/>')


@glyph
def gingerbread(c="#b8762e"):
    return (f'<path d="M128 30 a34 34 0 1 1 -0.1 0 Z" fill="{c}" {S()}/>'
            f'<path d="M98 96 L158 96 L210 130 L196 150 L162 136 L166 228 L136 228 L128 180 L120 228 L90 228 L94 136 L60 150 L46 130 Z" fill="{c}" {S()}/>'
            f'<circle cx="116" cy="60" r="6" fill="{INK}"/><circle cx="140" cy="60" r="6" fill="{INK}"/><path d="M114 78 q14 10 28 0" stroke="#f4ecd0" stroke-width="5" fill="none"/>'
            + "".join(f'<circle cx="128" cy="{y}" r="7" fill="#c0283a"/>' for y in (120, 146)))


@glyph
def soldier(c="#c0283a"):
    return (f'<rect x="96" y="20" width="64" height="60" rx="8" fill="#2c4f8a" {S(7)}/><circle cx="128" cy="98" r="30" fill="#d8a878" {S(7)}/>'
            f'<rect x="88" y="126" width="80" height="80" rx="10" fill="{c}" {S(7)}/><rect x="96" y="204" width="24" height="36" fill="#1a1012" {S(6)}/><rect x="136" y="204" width="24" height="36" fill="#1a1012" {S(6)}/>'
            f'<line x1="120" y1="126" x2="120" y2="206" stroke="#e8c35a" stroke-width="6"/><line x1="136" y1="126" x2="136" y2="206" stroke="#e8c35a" stroke-width="6"/>')


@glyph
def scroll(c="#efe2c0", mark=""):
    return (f'<rect x="60" y="50" width="136" height="160" fill="{c}" {S()}/><rect x="46" y="38" width="164" height="22" rx="10" fill="#c9a86a" {S(6)}/><rect x="46" y="200" width="164" height="22" rx="10" fill="#c9a86a" {S(6)}/>'
            + "".join(f'<line x1="80" y1="{84+i*22}" x2="176" y2="{84+i*22}" stroke="#5a1a1a" stroke-width="5"/>' for i in range(5))
            + (f'<text x="128" y="170" font-family="Cinzel Decorative" font-weight="900" font-size="96" text-anchor="middle" fill="#8e1424" stroke="{INK}" stroke-width="4">{mark}</text>' if mark else ""))


@glyph
def seal(c="#8e1424"):
    return (scroll() + f'<circle cx="168" cy="186" r="34" fill="{c}" {S(7)}/><path d="M168 166 l10 20 l-20 0 Z M168 206 l10 -20 l-20 0 Z" fill="#ffd27a"/>')


@glyph
def chain(c="#9a96a2"):
    return "".join(f'<ellipse cx="{70+i*38}" cy="{70+i*38}" rx="34" ry="20" transform="rotate(45 {70+i*38} {70+i*38})" fill="none" stroke="{INK}" stroke-width="20"/>'
                   f'<ellipse cx="{70+i*38}" cy="{70+i*38}" rx="34" ry="20" transform="rotate(45 {70+i*38} {70+i*38})" fill="none" stroke="{c}" stroke-width="9"/>' for i in range(4))


@glyph
def clock(c="#efe6cf"):
    return (f'<circle cx="128" cy="128" r="96" fill="{c}" {S(10)}/><circle cx="128" cy="128" r="84" fill="none" stroke="#8e1424" stroke-width="6"/>'
            + "".join(f'<line x1="{128+math.cos(a)*70:.0f}" y1="{128+math.sin(a)*70:.0f}" x2="{128+math.cos(a)*82:.0f}" y2="{128+math.sin(a)*82:.0f}" stroke="{INK}" stroke-width="6"/>' for a in [i*math.pi/6 for i in range(12)])
            + f'<line x1="128" y1="128" x2="118" y2="64" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><line x1="128" y1="128" x2="126" y2="50" stroke="#8e1424" stroke-width="6" stroke-linecap="round"/><circle cx="128" cy="128" r="10" fill="#c09040" {S(4)}/>')


@glyph
def sack(c="#7a5a3a"):
    return (f'<path d="M60 220 C30 140 80 70 128 70 C176 70 226 140 196 220 Z" fill="{c}" {S()}/><path d="M100 70 L128 40 L156 70" fill="{c}" {S(7)}/>'
            f'<path d="M98 76 q30 14 60 0" stroke="#c0283a" stroke-width="10" fill="none"/><path d="M90 150 q40 30 80 0" stroke="#4a3220" stroke-width="6" fill="none"/>')


@glyph
def gift(c="#c0283a", r="#e8c35a"):
    return (f'<rect x="50" y="96" width="156" height="126" rx="8" fill="{c}" {S()}/><rect x="40" y="76" width="176" height="36" rx="6" fill="{c}" {S()}/>'
            f'<rect x="116" y="76" width="24" height="146" fill="{r}" {S(5)}/><path d="M128 76 q-60 -70 -70 -14 q40 10 70 14 q60 -70 70 -14 q-40 10 -70 14" fill="{r}" {S(6)}/>')


@glyph
def ribbon(c="#c0283a"):
    return (f'<path d="M30 70 Q90 20 128 90 Q166 160 226 110" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M30 70 Q90 20 128 90 Q166 160 226 110" stroke="{c}" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<path d="M30 180 Q90 130 128 200 Q166 240 226 190" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M30 180 Q90 130 128 200 Q166 240 226 190" stroke="#e8c35a" stroke-width="26" fill="none" stroke-linecap="round"/>')


@glyph
def eye(c="#ff5a1a"):
    return (f'<path d="M24 128 Q128 30 232 128 Q128 226 24 128 Z" fill="#f4ecd0" {S()}/><circle cx="128" cy="128" r="46" fill="{c}" {S(7)}/>'
            f'<ellipse cx="128" cy="128" rx="10" ry="34" fill="#000"/><circle cx="112" cy="110" r="9" fill="#fff"/>')


@glyph
def mask(c="#2f7a46"):
    return (f'<path d="M40 80 Q128 40 216 80 Q220 180 128 220 Q36 180 40 80 Z" fill="{c}" {S()}/>'
            f'<path d="M66 112 q26 -22 52 0 q-26 20 -52 0 Z M138 112 q26 -22 52 0 q-26 20 -52 0 Z" fill="#120909"/>'
            f'<path d="M96 170 q32 24 64 0" stroke="#120909" stroke-width="8" fill="none"/>')


@glyph
def gavel(c="#c09040"):
    return (f'<rect x="56" y="62" width="110" height="56" rx="10" fill="#5a3416" {S()} transform="rotate(-35 111 90)"/>'
            f'<rect x="110" y="96" width="22" height="130" rx="8" fill="#7a4a22" {S(7)} transform="rotate(-35 121 160)"/>'
            f'<rect x="40" y="200" width="120" height="30" rx="8" fill="{c}" {S(7)}/>')


@glyph
def scales(c="#e8c35a"):
    return (f'<line x1="128" y1="40" x2="128" y2="210" stroke="{INK}" stroke-width="16"/><line x1="128" y1="40" x2="128" y2="210" stroke="{c}" stroke-width="7"/>'
            f'<line x1="50" y1="64" x2="206" y2="64" stroke="{INK}" stroke-width="14"/><line x1="50" y1="64" x2="206" y2="64" stroke="{c}" stroke-width="6"/>'
            f'<path d="M30 140 L70 70 L110 140 Z M146 140 L186 70 L226 140 Z" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M24 140 Q70 180 116 140 Z M140 140 Q186 180 232 140 Z" fill="{c}" {S(7)}/><rect x="84" y="206" width="88" height="22" rx="6" fill="{c}" {S(6)}/>')


@glyph
def key(c="#e8c35a"):
    return (f'<circle cx="84" cy="90" r="46" fill="{c}" {S()}/><circle cx="84" cy="90" r="18" fill="#2a1a1a" {S(5)}/>'
            f'<rect x="110" y="110" width="110" height="24" fill="{c}" {S(7)}/><rect x="180" y="134" width="20" height="36" fill="{c}" {S(6)}/><rect x="150" y="134" width="18" height="26" fill="{c}" {S(6)}/>')


@glyph
def ledger(c="#5e0b18"):
    return (f'<path d="M30 70 L128 90 L226 70 L226 200 L128 220 L30 200 Z" fill="{c}" {S()}/>'
            f'<path d="M44 76 L128 94 L128 208 L44 190 Z" fill="#efe2c0" {S(6)}/><path d="M212 76 L128 94 L128 208 L212 190 Z" fill="#f4ead0" {S(6)}/>'
            + "".join(f'<line x1="58" y1="{102+i*20}" x2="116" y2="{114+i*20}" stroke="#5a1a1a" stroke-width="4"/><line x1="140" y1="{114+i*20}" x2="198" y2="{102+i*20}" stroke="#5a1a1a" stroke-width="4"/>' for i in range(4)))


@glyph
def quill(c="#1a1418"):
    return (f'<path d="M70 220 C60 140 120 50 210 30 C190 120 140 190 70 220 Z" fill="{c}" {S()}/>'
            f'<line x1="70" y1="220" x2="190" y2="50" stroke="#8e1424" stroke-width="5"/><path d="M70 220 l-12 20 l22 -6 Z" fill="#e8c35a" {S(4)}/>'
            f'<circle cx="60" cy="236" r="10" fill="#8e1424"/>')


@glyph
def coin(c="#a8301e", face=True):
    return (f'<circle cx="128" cy="128" r="92" fill="{c}" {S(10)}/><circle cx="128" cy="128" r="74" fill="none" stroke="#ffb07a" stroke-width="5" opacity="0.7"/>'
            + (f'<circle cx="112" cy="112" r="8" fill="{INK}"/><circle cx="144" cy="112" r="8" fill="{INK}"/><path d="M104 156 q24 -18 48 0" stroke="{INK}" stroke-width="7" fill="none"/>' if face else ""))


@glyph
def ring(c="#26232a"):
    return (f'<circle cx="128" cy="150" r="72" fill="none" stroke="{INK}" stroke-width="40"/><circle cx="128" cy="150" r="72" fill="none" stroke="{c}" stroke-width="24"/>'
            f'<rect x="88" y="44" width="80" height="60" rx="12" fill="{c}" {S()}/><ellipse cx="128" cy="74" rx="28" ry="20" fill="#c0283a" {S(5)}/>')


@glyph
def collar(c="#c09040"):
    return (f'<ellipse cx="128" cy="128" rx="96" ry="60" fill="none" stroke="{INK}" stroke-width="44"/><ellipse cx="128" cy="128" rx="96" ry="60" fill="none" stroke="{c}" stroke-width="28"/>'
            f'<circle cx="128" cy="188" r="30" fill="#3a3640" {S(7)}/>' + "".join(f'<line x1="128" y1="188" x2="{128+math.cos(a)*26:.0f}" y2="{188+math.sin(a)*26:.0f}" stroke="#c09040" stroke-width="6"/>' for a in [i*math.pi/3 for i in range(6)]))


@glyph
def gear(c="#c09040"):
    pts = " ".join(f"{128+math.cos(i*math.pi/24)*(96 if (i%4) in (1,2) else 78):.1f},{128+math.sin(i*math.pi/24)*(96 if (i%4) in (1,2) else 78):.1f}" for i in range(48))
    return f'<polygon points="{pts}" fill="{c}" {S(8)}/><circle cx="128" cy="128" r="30" fill="#2a1a1a" {S(7)}/>'


@glyph
def flame(c="#ff7a1a"):
    return (f'<path d="M128 24 C170 80 210 110 200 160 C190 210 160 232 128 232 C96 232 66 210 56 160 C50 120 80 100 92 60 C100 90 110 100 120 100 C110 70 116 46 128 24 Z" fill="{c}" {S()}/>'
            f'<path d="M128 110 C150 140 166 160 160 190 C154 214 138 222 128 222 C114 222 98 212 96 190 C94 160 116 150 128 110 Z" fill="#ffe08a"/>')


@glyph
def baton(c="#c09040"):
    return f'<rect x="114" y="56" width="28" height="180" rx="12" fill="#3a3640" {S(7)} transform="rotate(35 128 146)"/><circle cx="84" cy="70" r="34" fill="{c}" {S()}/>'


@glyph
def sword(c="#e9eef6"):
    return (f'<path d="M190 30 L226 30 L226 66 L100 192 L64 156 Z" fill="{c}" {S()}/><path d="M50 150 L106 206" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M50 150 L106 206" stroke="#c09040" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M78 178 L36 220" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M78 178 L36 220" stroke="#5a3416" stroke-width="14" stroke-linecap="round"/>')


@glyph
def spear(c="#dfe6ef"):
    return f'<line x1="40" y1="216" x2="190" y2="66" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><line x1="40" y1="216" x2="190" y2="66" stroke="#7a4a22" stroke-width="10" stroke-linecap="round"/><path d="M226 30 L210 100 L156 46 Z" fill="{c}" {S(7)}/>'


@glyph
def crossbow(c="#7a4a22"):
    return (f'<path d="M40 90 Q128 20 216 90" fill="none" stroke="{INK}" stroke-width="22"/><path d="M40 90 Q128 20 216 90" fill="none" stroke="{c}" stroke-width="10"/>'
            f'<line x1="40" y1="90" x2="216" y2="90" stroke="#efe2c0" stroke-width="4"/><rect x="116" y="50" width="24" height="180" rx="8" fill="{c}" {S(7)}/><path d="M128 30 l14 30 l-28 0 Z" fill="#dfe6ef" {S(5)}/>')


@glyph
def snowball(c="#eef3f8"):
    return f'<circle cx="128" cy="128" r="86" fill="{c}" {S(10)}/><path d="M80 100 q20 -30 50 -30" stroke="#fff" stroke-width="12" fill="none"/><circle cx="160" cy="160" r="12" fill="#b9c8dc"/><circle cx="110" cy="170" r="8" fill="#b9c8dc"/>'


@glyph
def hoof(c="#3a2a2a"):
    return f'<path d="M50 80 Q50 220 120 220 L120 120 Z M206 80 Q206 220 136 220 L136 120 Z" fill="{c}" {S()}/><path d="M60 60 L196 60" stroke="#ff5a1a" stroke-width="16" stroke-linecap="round"/>'


@glyph
def antler(c="#6a4410"):
    p = "M128 230 L128 150 C110 100 70 80 50 30 M100 110 L40 100 M128 150 C146 100 186 80 206 30 M156 110 L216 100"
    return f'<path d="{p}" stroke="{INK}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="{p}" stroke="{c}" stroke-width="16" fill="none" stroke-linecap="round"/><circle cx="50" cy="30" r="16" fill="#ff7a1a"/><circle cx="206" cy="30" r="16" fill="#ff7a1a"/>'


@glyph
def net(c="#c8b890"):
    return (f'<circle cx="128" cy="128" r="96" fill="none" {S(10)}/>' + "".join(f'<line x1="{32+i*32}" y1="40" x2="{32+i*32}" y2="216" stroke="{c}" stroke-width="6"/><line x1="40" y1="{32+i*32}" x2="216" y2="{32+i*32}" stroke="{c}" stroke-width="6"/>' for i in range(7))
            + "".join(f'<circle cx="{128+math.cos(a)*96:.0f}" cy="{128+math.sin(a)*96:.0f}" r="10" fill="#3a3640" {S(4)}/>' for a in [i*math.pi/4 for i in range(8)]))


@glyph
def mug(c="#efe2b8"):
    return (f'<rect x="60" y="70" width="110" height="140" rx="14" fill="#9a9aa6" {S()}/><path d="M170 100 q50 0 50 40 q0 40 -50 40" fill="none" stroke="{INK}" stroke-width="22"/><path d="M170 100 q50 0 50 40 q0 40 -50 40" fill="none" stroke="#9a9aa6" stroke-width="10"/>'
            f'<path d="M54 70 q20 -40 60 -20 q30 -30 62 6 q12 14 0 14 Z" fill="{c}" {S(7)}/>')


@glyph
def clipboard(c="#c09040"):
    return (f'<rect x="56" y="40" width="144" height="190" rx="10" fill="{c}" {S()}/><rect x="72" y="66" width="112" height="146" fill="#f4ecd0" {S(5)}/>'
            + "".join(f'<line x1="86" y1="{90+i*24}" x2="170" y2="{90+i*24}" stroke="#8e1424" stroke-width="5"/>' for i in range(5))
            + f'<rect x="100" y="28" width="56" height="28" rx="6" fill="#3a3640" {S(5)}/>')


@glyph
def stamp(c="#8e1424"):
    return (f'<rect x="104" y="30" width="48" height="90" rx="14" fill="#5a3416" {S(7)}/><rect x="70" y="118" width="116" height="40" rx="8" fill="#3a3640" {S(7)}/>'
            f'<rect x="60" y="156" width="136" height="30" fill="{c}" {S(7)}/><text x="128" y="234" font-family="Cinzel" font-weight="900" font-size="36" text-anchor="middle" fill="{c}" stroke="{INK}" stroke-width="2">DENIED</text>')


@glyph
def badge(c="#e8c35a"):
    pts = " ".join(f"{128+math.cos(i*math.pi/8)*(100 if i%2==0 else 80):.1f},{128+math.sin(i*math.pi/8)*(100 if i%2==0 else 80):.1f}" for i in range(16))
    return f'<polygon points="{pts}" fill="{c}" {S(8)}/><circle cx="128" cy="128" r="50" fill="#2f5a3a" {S(6)}/><path d="M100 140 L128 96 L156 140 Z" fill="{c}"/>'


@glyph
def ghost(c="#bfe6f0"):
    return (f'<path d="M50 230 L50 110 C50 50 206 50 206 110 L206 230 L180 206 L154 230 L128 206 L102 230 L76 206 Z" fill="{c}" {S()}/>'
            f'<ellipse cx="100" cy="120" rx="14" ry="20" fill="{INK}"/><ellipse cx="156" cy="120" rx="14" ry="20" fill="{INK}"/><ellipse cx="128" cy="168" rx="16" ry="20" fill="{INK}"/>')


@glyph
def shield(c="#2c4f8a"):
    return f'<path d="M128 24 L216 56 C216 140 186 200 128 232 C70 200 40 140 40 56 Z" fill="{c}" {S()}/><path d="M128 50 L190 74 C188 136 166 180 128 204 Z" fill="#fff" opacity="0.18"/>'


@glyph
def crown(c="#e8c35a"):
    return f'<path d="M40 190 L40 80 L86 130 L128 50 L170 130 L216 80 L216 190 Z" fill="{c}" {S()}/><rect x="36" y="186" width="184" height="34" fill="{c}" {S(7)}/>' + "".join(f'<circle cx="{x}" cy="203" r="9" fill="#c0283a"/>' for x in (76, 128, 180))


@glyph
def arrows(c="#e8c35a"):
    return f'<path d="M40 128 L100 70 L100 106 L156 106 L156 70 L216 128 L156 186 L156 150 L100 150 L100 186 Z" fill="{c}" {S()}/>'


@glyph
def slashes(c="#c0283a"):
    return "".join(f'<path d="M{60+i*50} 40 Q{90+i*50} 128 {50+i*50} 216" stroke="{INK}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M{60+i*50} 40 Q{90+i*50} 128 {50+i*50} 216" stroke="{c}" stroke-width="14" fill="none" stroke-linecap="round"/>' for i in range(3))


@glyph
def devil(c="#c23a2e"):
    return (f'<path d="M70 70 C40 30 40 10 60 10 C70 40 90 50 100 60 Z M186 70 C216 30 216 10 196 10 C186 40 166 50 156 60 Z" fill="#1c1418" {S(6)}/>'
            f'<path d="M50 100 C50 40 206 40 206 100 C206 180 170 230 128 230 C86 230 50 180 50 100 Z" fill="{c}" {S()}/>'
            f'<path d="M76 110 L116 124 L76 134 Z M180 110 L140 124 L180 134 Z" fill="#ffd27a" {S(5)}/><path d="M86 180 Q128 210 170 180 Q128 196 86 180 Z" fill="#120909" {S(5)}/>')


@glyph
def staple(c="#dfe6ef"):
    return f'<path d="M50 200 L50 70 L206 70 L206 200" fill="none" stroke="{INK}" stroke-width="34" stroke-linejoin="miter"/><path d="M50 200 L50 70 L206 70 L206 200" fill="none" stroke="{c}" stroke-width="18" stroke-linejoin="miter"/>'


@glyph
def sting(c="#c0283a"):
    return f'<path d="M40 40 Q160 40 180 140 L220 216 L150 170 Q60 150 40 40 Z" fill="{c}" {S()}/><path d="M180 140 L220 216 L150 170 Z" fill="#dfe6ef" {S(5)}/>'


@glyph
def invisible(c="#9fd0e0"):
    return f'<circle cx="128" cy="76" r="40" fill="none" stroke="{c}" stroke-width="8" stroke-dasharray="14 10"/><path d="M60 230 Q60 130 128 126 Q196 130 196 230" fill="none" stroke="{c}" stroke-width="8" stroke-dasharray="14 10"/>'


@glyph
def sun(c="#ffd27a"):
    return (f'<circle cx="128" cy="128" r="56" fill="{c}" {S(8)}/>' + "".join(f'<path d="M{128+math.cos(a)*70:.0f} {128+math.sin(a)*70:.0f} L{128+math.cos(a+0.15)*104:.0f} {128+math.sin(a+0.15)*104:.0f} L{128+math.cos(a-0.15)*104:.0f} {128+math.sin(a-0.15)*104:.0f} Z" fill="{c}" {S(5)}/>' for a in [i*math.pi/6 for i in range(12)]))


@glyph
def brand(c="#ff5a1a"):
    return f'<circle cx="128" cy="128" r="90" fill="#3a1414" {S(8)}/><path d="M128 50 L150 110 L210 110 L162 146 L180 206 L128 170 L76 206 L94 146 L46 110 L106 110 Z" fill="none" stroke="{c}" stroke-width="12"/>'


@glyph
def pentagram(c="#c0283a"):
    pts = [(128 + math.cos(-math.pi / 2 + i * 4 * math.pi / 5) * 90, 128 + math.sin(-math.pi / 2 + i * 4 * math.pi / 5) * 90) for i in range(5)]
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + " Z"
    return f'<circle cx="128" cy="128" r="100" fill="#1a0808" {S(8)}/><circle cx="128" cy="128" r="90" fill="none" stroke="{c}" stroke-width="6"/><path d="{d}" fill="none" stroke="{c}" stroke-width="9"/>'


@glyph
def manacles(c="#9a96a2"):
    return (f'<circle cx="76" cy="150" r="46" fill="none" stroke="{INK}" stroke-width="30"/><circle cx="76" cy="150" r="46" fill="none" stroke="{c}" stroke-width="16"/>'
            f'<circle cx="180" cy="150" r="46" fill="none" stroke="{INK}" stroke-width="30"/><circle cx="180" cy="150" r="46" fill="none" stroke="{c}" stroke-width="16"/>'
            f'<path d="M110 120 Q128 70 146 120" fill="none" stroke="{INK}" stroke-width="20"/><path d="M110 120 Q128 70 146 120" fill="none" stroke="{c}" stroke-width="8"/>')


@glyph
def hands(c="#e8b496"):
    return (f'<path d="M20 150 L90 100 L140 120 L110 150 L160 150 L200 120 L236 150 L180 200 L90 200 Z" fill="{c}" {S()}/>'
            f'<path d="M110 150 L170 150" stroke="{INK}" stroke-width="6"/><circle cx="128" cy="70" r="26" fill="#8e1424" {S(6)}/>')


@glyph
def lips(c="#c0283a"):
    return f'<path d="M30 128 Q80 70 128 100 Q176 70 226 128 Q176 200 128 190 Q80 200 30 128 Z" fill="{c}" {S()}/><path d="M30 128 Q128 150 226 128" stroke="{INK}" stroke-width="8" fill="none"/><text x="128" y="70" font-family="Cinzel" font-weight="900" font-size="40" text-anchor="middle" fill="#ffd27a" stroke="{INK}" stroke-width="2">NOMEN</text>'


@glyph
def magnifier(c="#7ac0e0"):
    return scroll() + f'<circle cx="150" cy="140" r="54" fill="{c}" fill-opacity="0.4" {S(12)}/><line x1="188" y1="178" x2="232" y2="222" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><line x1="188" y1="178" x2="232" y2="222" stroke="#5a3416" stroke-width="12" stroke-linecap="round"/>'


@glyph
def coal(c="#ff5a1a"):
    return f'<path d="M50 150 L80 70 L170 50 L216 120 L190 200 L90 210 Z" fill="#1a1418" {S()}/><path d="M90 120 L120 90 M150 150 L180 120 M100 180 L140 160" stroke="{c}" stroke-width="10"/><circle cx="128" cy="128" r="100" fill="{c}" opacity="0.15"/>'


@glyph
def hand(c="#e8b496"):
    return (f'<path d="M80 230 L70 120 Q66 100 84 100 Q98 100 100 120 L104 70 Q104 50 120 50 Q136 50 136 70 L138 60 Q140 40 156 42 Q170 44 170 64 L170 80 Q172 64 186 66 Q200 68 198 90 L192 170 Q186 220 160 236 Z" fill="{c}" {S()}/>'
            f'<text x="128" y="246" font-family="Cinzel" font-weight="900" font-size="30" text-anchor="middle" fill="#ffd27a" stroke="{INK}" stroke-width="2">OBJECTION</text>')


@glyph
def heart(c="#c0283a"):
    return f'<path d="M128 220 C40 160 30 100 60 70 C90 40 120 60 128 86 C136 60 166 40 196 70 C226 100 216 160 128 220 Z" fill="{c}" {S()}/><path d="M60 150 Q128 110 196 150" stroke="#e8c35a" stroke-width="12" fill="none"/>'


@glyph
def letter(c="#8e1424", ch="A"):
    return f'<text x="128" y="190" font-family="Cinzel Decorative" font-weight="900" font-size="170" text-anchor="middle" fill="{c}" stroke="{INK}" stroke-width="7">{ch}</text>'


@glyph
def shard(c="#ffd27a"):
    return f'<circle cx="128" cy="128" r="90" fill="{c}" opacity="0.3"/><path d="M128 20 L180 110 L150 236 L90 180 L76 80 Z" fill="#cfe8ff" {S()}/><path d="M128 40 L160 110 L140 210" stroke="{c}" stroke-width="10" fill="none"/>'


@glyph
def musicbox(c="#8e1424"):
    return f'<rect x="40" y="110" width="176" height="110" rx="8" fill="{c}" {S()}/><path d="M40 110 L60 50 L236 50 L216 110 Z" fill="#5e0b18" {S()}/><circle cx="128" cy="166" r="20" fill="#e8c35a" {S(5)}/><path d="M150 30 l0 -10 M170 40 q10 -20 20 -10" stroke="#e8c35a" stroke-width="6" fill="none"/>'


@glyph
def bear(c="#a8743a"):
    return (f'<circle cx="80" cy="60" r="30" fill="{c}" {S()}/><circle cx="176" cy="60" r="30" fill="{c}" {S()}/><circle cx="128" cy="110" r="70" fill="{c}" {S()}/>'
            f'<ellipse cx="128" cy="200" rx="70" ry="44" fill="{c}" {S()}/><circle cx="104" cy="100" r="9" fill="{INK}"/><circle cx="152" cy="100" r="9" fill="{INK}"/><ellipse cx="128" cy="134" rx="22" ry="16" fill="#e8c8a0" {S(5)}/>')


@glyph
def dice(c="#8e1424"):
    pts = " ".join(f"{128+math.cos(i*math.pi/3+math.pi/6)*100:.0f},{128+math.sin(i*math.pi/3+math.pi/6)*100:.0f}" for i in range(6))
    return f'<polygon points="{pts}" fill="{c}" {S(10)}/><path d="M128 28 L128 128 L41 178 M128 128 L215 178" stroke="#ffd27a" stroke-width="6"/><text x="128" y="110" font-family="Cinzel" font-weight="900" font-size="54" text-anchor="middle" fill="#ffd27a">20</text>'


@glyph
def sigil(c="#c0283a"):
    return f'<circle cx="128" cy="128" r="96" fill="none" stroke="{c}" stroke-width="10"/><path d="M128 40 L128 216 M60 90 L196 166 M60 166 L196 90" stroke="{c}" stroke-width="12"/><circle cx="128" cy="128" r="24" fill="{c}" {S(6)}/>'


@glyph
def wings(c="#3a1418"):
    return (f'<path d="M128 140 C90 60 40 40 16 60 C40 90 30 120 50 150 C70 140 90 150 128 170 Z" fill="{c}" {S()}/><path d="M128 140 C166 60 216 40 240 60 C216 90 226 120 206 150 C186 140 166 150 128 170 Z" fill="{c}" {S()}/>'
            + devil("#c23a2e").replace('<path d="M50 100', '<path transform="translate(64,90) scale(0.5)" d="M50 100'))


@glyph
def book(c="#2c1a2e"):
    return f'<rect x="50" y="40" width="156" height="180" rx="8" fill="{c}" {S()}/><rect x="60" y="40" width="20" height="180" fill="#120909"/>' + pentagram("#c0283a").replace('<circle cx="128" cy="128" r="100" fill="#1a0808"', '<circle cx="138" cy="128" r="0" fill="none"').replace('cx="128" cy="128" r="90"', 'cx="138" cy="128" r="54"')


@glyph
def blueprint(c="#2c4f8a"):
    pts = " ".join(f"{128+math.cos(i*math.pi/24)*(70 if (i%4) in (1,2) else 56):.1f},{128+math.sin(i*math.pi/24)*(70 if (i%4) in (1,2) else 56):.1f}" for i in range(48))
    return (f'<rect x="30" y="50" width="196" height="156" fill="{c}" {S()}/>'
            f'<polygon points="{pts}" fill="none" stroke="#cfe8ff" stroke-width="6"/><circle cx="128" cy="128" r="18" fill="none" stroke="#cfe8ff" stroke-width="6"/>')


@glyph
def manifest(c="#efe2c0"):
    return scroll(c) + '<text x="128" y="230" font-family="Cinzel" font-weight="900" font-size="26" text-anchor="middle" fill="#8e1424">NESSUS</text>'




@glyph
def thorn(c="#8e1424"):
    return (f'<path d="M60 200 C100 150 150 110 200 56" stroke="{INK}" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<path d="M60 200 C100 150 150 110 200 56" stroke="#3a2a2a" stroke-width="14" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M{x} {y} l{dx} {dy} l10 6 Z" fill="{c}" {S(4)}/>' for x, y, dx, dy in ((92, 168, -26, -20), (120, 138, 24, 14), (150, 108, -24, -22), (176, 84, 24, 12))))


@glyph
def rose(c="#c0183a"):
    import math
    return (f'<path d="M128 140 Q120 200 132 236" stroke="{INK}" stroke-width="16" fill="none"/><path d="M128 140 Q120 200 132 236" stroke="#2a3a2a" stroke-width="8" fill="none"/>'
            + "".join(f'<ellipse cx="{128+math.cos(a)*30:.0f}" cy="{100+math.sin(a)*30:.0f}" rx="42" ry="26" fill="#5a5662" {S(5)} transform="rotate({math.degrees(a):.0f} {128+math.cos(a)*30:.0f} {100+math.sin(a)*30:.0f})"/>' for a in [i*0.9 for i in range(7)])
            + f'<circle cx="128" cy="100" r="28" fill="{c}" {S(5)}/>')


@glyph
def hourglass(c="#ffd27a"):
    return (f'<rect x="64" y="36" width="128" height="22" rx="6" fill="#8a5a2a" {S(6)}/><rect x="64" y="198" width="128" height="22" rx="6" fill="#8a5a2a" {S(6)}/>'
            f'<path d="M80 58 L176 58 L136 128 L176 198 L80 198 L120 128 Z" fill="#cfe8ff" fill-opacity="0.35" {S(7)}/>'
            f'<path d="M92 72 L164 72 L128 122 Z M128 140 L170 192 L86 192 Z" fill="{c}" {S(4)}/>')


@glyph
def lantern(c="#ffd27a"):
    return (f'<circle cx="128" cy="140" r="80" fill="{c}" opacity="0.35"/><path d="M100 40 Q128 20 156 40" stroke="{INK}" stroke-width="10" fill="none"/>'
            f'<rect x="84" y="56" width="88" height="24" rx="6" fill="#8a5a2a" {S(6)}/><rect x="92" y="80" width="72" height="110" rx="8" fill="{c}" {S(7)}/>'
            f'<path d="M110 80 V190 M146 80 V190" stroke="{INK}" stroke-width="6"/><rect x="80" y="190" width="96" height="24" rx="6" fill="#8a5a2a" {S(6)}/>')


@glyph
def shears(c="#2a2a30"):
    return (f'<path d="M128 128 L60 40 L80 36 L138 118 Z M128 128 L196 40 L176 36 L118 118 Z" fill="{c}" {S(6)}/>'
            f'<circle cx="88" cy="186" r="34" fill="none" stroke="{INK}" stroke-width="20"/><circle cx="88" cy="186" r="34" fill="none" stroke="#5a2a2a" stroke-width="10"/>'
            f'<circle cx="168" cy="186" r="34" fill="none" stroke="{INK}" stroke-width="20"/><circle cx="168" cy="186" r="34" fill="none" stroke="#5a2a2a" stroke-width="10"/>'
            f'<path d="M110 160 L128 128 L146 160" stroke="{INK}" stroke-width="12" fill="none"/><circle cx="128" cy="128" r="10" fill="#c09040" {S(4)}/>')


@glyph
def seed(c="#8e1424"):
    return (f'<path d="M128 40 C190 70 200 170 128 220 C56 170 66 70 128 40 Z" fill="{c}" {S()}/>'
            f'<path d="M128 60 C150 100 150 170 128 200" stroke="#ff7a5a" stroke-width="7" fill="none" opacity="0.7"/>'
            f'<path d="M128 40 q20 -20 40 -10" stroke="#3a5a2a" stroke-width="10" fill="none" stroke-linecap="round"/>')


@glyph
def gauntlet(c="#c09040"):
    return (f'<path d="M80 220 L80 120 Q80 70 110 64 L110 40 Q122 30 134 40 L134 64 L150 40 Q162 32 172 44 L162 80 Q190 90 186 130 L176 220 Z" fill="{c}" {S()}/>'
            f'<rect x="72" y="200" width="112" height="32" rx="6" fill="#8e1424" {S(6)}/><path d="M96 120 h70 M96 150 h70" stroke="{INK}" stroke-width="5"/>')


@glyph
def axe(c="#c8ccd6"):
    return (f'<rect x="118" y="40" width="20" height="190" rx="8" fill="#5a3416" {S(6)}/>'
            f'<path d="M138 50 Q220 60 214 140 Q170 120 138 120 Z" fill="{c}" {S(7)}/><path d="M118 56 Q50 70 54 130 Q90 116 118 112 Z" fill="{c}" {S(6)}/>')


@glyph
def vow(c="#c0183a"):
    return (f'<circle cx="128" cy="128" r="90" fill="none" stroke="{INK}" stroke-width="22"/><circle cx="128" cy="128" r="90" fill="none" stroke="{c}" stroke-width="12"/>'
            f'<path d="M84 128 l30 30 l58 -66" stroke="{INK}" stroke-width="24" fill="none" stroke-linecap="round"/><path d="M84 128 l30 30 l58 -66" stroke="#ffd27a" stroke-width="12" fill="none" stroke-linecap="round"/>')


@glyph
def tree(c="#4a3a30"):
    return (f'<rect x="114" y="120" width="28" height="110" fill="#2a1a12" {S(6)}/>'
            f'<path d="M128 120 L80 60 M128 120 L176 50 M128 140 L70 110 M128 140 L190 104" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="M128 120 L80 60 M128 120 L176 50 M128 140 L70 110 M128 140 L190 104" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
            f'<circle cx="80" cy="60" r="10" fill="#ff7a1a"/><circle cx="176" cy="50" r="10" fill="#ff7a1a"/><circle cx="190" cy="104" r="10" fill="#ff7a1a"/>')


@glyph
def spirit(c="#ff7a1a"):
    return (f'<circle cx="128" cy="128" r="90" fill="{c}" opacity="0.3"/><path d="M128 40 C180 90 190 150 160 200 Q128 230 96 200 C66 150 76 90 128 40 Z" fill="{c}" {S()}/>'
            f'<path d="M128 90 C150 120 150 160 128 190 C106 160 106 120 128 90 Z" fill="#ffe27a"/><circle cx="112" cy="140" r="8" fill="{INK}"/><circle cx="144" cy="140" r="8" fill="{INK}"/>')


@glyph
def golem(c="#5a5660"):
    return (f'<rect x="60" y="100" width="136" height="120" rx="24" fill="{c}" {S()}/><rect x="86" y="40" width="84" height="70" rx="18" fill="{c}" {S()}/>'
            f'<rect x="100" y="66" width="56" height="12" fill="#ff7a1a"/><circle cx="128" cy="160" r="26" fill="#7ad0ff" {S(6)}/>')


@glyph
def portal(c="#ff6a1a"):
    return (f'<ellipse cx="128" cy="128" rx="96" ry="110" fill="{INK}"/><ellipse cx="128" cy="128" rx="88" ry="102" fill="none" stroke="{c}" stroke-width="22"/>'
            f'<ellipse cx="128" cy="128" rx="60" ry="74" fill="#3a6a3a"/><ellipse cx="128" cy="128" rx="88" ry="102" fill="none" stroke="#ffe27a" stroke-width="6" stroke-dasharray="14 18"/>')


ICONS = {
    # items
    "it-bell": ("bell", "#e8e8f0", "#2c4f8a"), "it-bell9": ("bell", "#e8c35a", "#5a1008"), "it-candle": ("candle", "#ffd27a", "#5a3a10"),
    "it-candycane": ("candycane", "#c0283a", "#1a4a2a"), "it-certificate": ("seal", "#8e1424", "#3a2a1a"),
    "it-chainwhip": ("chain", "#c0283a", "#3a0a12"), "it-citation": ("stamp", "#8e1424", "#1a4a2a"),
    "it-clipboard": ("clipboard", "#c09040", "#1a4a2a"), "it-collar": ("collar", "#c09040", "#26262e"),
    "it-dawnglass": ("shard", "#ffd27a", "#5a3a10"), "it-exhibit-a": ("letter", "#c09040", "#3a1a1a", "A"),
    "it-exhibit-b": ("letter", "#c09040", "#1a2a4a", "B"), "it-exhibit-c": ("letter", "#c09040", "#1a3a3a", "C"),
    "it-exhibit-d": ("letter", "#c09040", "#3a1a3a", "D"), "it-gavel": ("gavel", "#c09040", "#5a4214"),
    "it-gingerbread": ("gingerbread", "#b8762e", "#3a1a0a"), "it-manifest": ("manifest", "#efe2c0", "#3a2a1a"),
    "it-memo": ("seal", "#1a1418", "#5a0a12"), "it-mirror": ("mirror", "#7ac0e0", "#1a4a2a"),
    "it-musicbox": ("musicbox", "#8e1424", "#26262e"), "it-quill": ("quill", "#1a1418", "#5a0a12"),
    "it-receipt": ("scroll", "#efe2c0", "#3a2a1a"), "it-scarf": ("scarf", "#c0283a", "#2c4f8a"),
    "it-schematic": ("blueprint", "#2c4f8a", "#1a2a3a"), "it-scroll": ("scroll", "#efe2c0", "#5a0a12"),
    "it-signet": ("ring", "#26232a", "#5a0a12"), "it-soldier": ("soldier", "#c0283a", "#2c4f8a"),
    "it-soulcoin": ("coin", "#a8301e", "#26262e"), "it-star": ("star", "#ffd84a", "#1a2a4a"),
    "it-stocking": ("stocking", "#c0283a", "#1a4a2a"), "it-token": ("coin", "#c09040", "#5a4214"),
    "it-toybear": ("bear", "#a8743a", "#26262e"),
    # abilities
    "rc-antler": ("antler", "#6a4410", "#5a1008"), "rc-badge": ("badge", "#e8c35a", "#1a3a2a"), "rc-baton": ("baton", "#c09040", "#1a3a2a"),
    "rc-bell": ("bell", "#e8c35a", "#2c4f8a"), "rc-breach": ("scroll", "#efe2c0", "#8e1424", "!"), "rc-broken": ("scroll", "#c8b890", "#26262e", "✕"),
    "rc-candle": ("candle", "#bfe6ff", "#10303a"), "rc-chain": ("chain", "#9a96a2", "#5a0a12"), "rc-citation": ("clipboard", "#c0283a", "#5a0a12"),
    "rc-clipboard": ("clipboard", "#c09040", "#1a4a2a"), "rc-clock": ("clock", "#efe6cf", "#101a3a"), "rc-collar": ("collar", "#c09040", "#26262e"),
    "rc-crossbow": ("crossbow", "#7a4a22", "#1a3a2a"), "rc-eggnog": ("mug", "#efe2b8", "#5a4214"), "rc-eye": ("eye", "#ff5a1a", "#3a0a0a"),
    "rc-fineprint": ("magnifier", "#7ac0e0", "#26262e"), "rc-furnace": ("flame", "#ff7a1a", "#3a0a0a"), "rc-gavel": ("gavel", "#c09040", "#5a4214"),
    "rc-gear": ("gear", "#c09040", "#26262e"), "rc-ghost": ("ghost", "#bfe6f0", "#10303a"), "rc-gift": ("gift", "#c0283a", "#1a4a2a"),
    "rc-hoof": ("hoof", "#3a2a2a", "#5a1008"), "rc-invisible": ("invisible", "#9fd0e0", "#10303a"), "rc-key": ("key", "#e8c35a", "#2c4f8a"),
    "rc-ledger": ("ledger", "#5e0b18", "#26262e"), "rc-legendary": ("crown", "#e8c35a", "#5a0a12"), "rc-manifest": ("manifest", "#efe2c0", "#5a4214"),
    "rc-mask": ("mask", "#2f7a46", "#3a0a12"), "rc-multi": ("slashes", "#c0283a", "#26262e"), "rc-net": ("net", "#c8b890", "#26262e"),
    "rc-order": ("arrows", "#2f7a46", "#1a3a2a"), "rc-phase2": ("devil", "#c23a2e", "#120404"), "rc-relocate": ("arrows", "#e8c35a", "#26262e"),
    "rc-resist": ("shield", "#8e1424", "#26262e"), "rc-ribbon": ("ribbon", "#c0283a", "#1a4a2a"), "rc-sabre": ("sword", "#e9eef6", "#2c4f8a"),
    "rc-sack": ("sack", "#7a5a3a", "#5a0a12"), "rc-scales": ("scales", "#e8c35a", "#5a4214"), "rc-signet": ("ring", "#26232a", "#5a0a12"),
    "rc-snowball": ("snowball", "#eef3f8", "#2c4f8a"), "rc-spear": ("spear", "#dfe6ef", "#1a3a2a"), "rc-stamp": ("stamp", "#8e1424", "#1a4a2a"),
    "rc-staple": ("staple", "#dfe6ef", "#5a0a12"), "rc-sting": ("sting", "#c0283a", "#3a0a12"), "rc-writ": ("seal", "#c09040", "#5a0a12"),
    # spells (school colours)
    "sp-appeal": ("scroll", "#efe2c0", "#3a2a5a", "↺"), "sp-binding": ("pentagram", "#ff5a3a", "#3a0a3a"), "sp-blade": ("sword", "#ff7a6a", "#2a0a14"),
    "sp-clause": ("manacles", "#9a96a2", "#1a2a4a"), "sp-coal": ("coal", "#ff5a1a", "#3a0a0a"), "sp-covenant": ("hands", "#e8b496", "#3a2a5a"),
    "sp-dawn": ("sun", "#ffd27a", "#3a1a0a"), "sp-due": ("scales", "#8e1424", "#2a0a14"), "sp-fineprint": ("magnifier", "#7ac0e0", "#10303a"),
    "sp-fury": ("flame", "#ff7a1a", "#3a0a0a"), "sp-mark": ("brand", "#ff5a1a", "#2a0a14"), "sp-quill": ("quill", "#1a1418", "#3a2a1a"),
    "sp-seal": ("seal", "#8e1424", "#3a2a5a"), "sp-snare": ("ribbon", "#c0283a", "#3a2a1a"), "sp-stay": ("hand", "#e8b496", "#1a2a4a"),
    "sp-truename": ("lips", "#c0283a", "#10303a"), "sp-vigil": ("eye", "#7ac0e0", "#10303a"), "sp-witness": ("heart", "#c0283a", "#10303a"),
    # subclasses
    "sub-aura": ("shield", "#ff7a1a", "#3a0a0a"), "sub-avatar": ("wings", "#3a1418", "#2a0404"), "sub-binding": ("pentagram", "#ffd27a", "#3a0a3a"),
    "sub-chains": ("chain", "#ff5a3a", "#2a0a14"), "sub-oath": ("sword", "#c0283a", "#120404"), "sub-pact": ("hands", "#c23a2e", "#2a0a14"),
    "sub-rebuke": ("flame", "#ff5a1a", "#2a0a14"), "sub-rune": ("sigil", "#ff7a1a", "#26262e"), "sub-school": ("book", "#2c1a2e", "#3a0a3a"),
    "sub-sigil": ("sigil", "#c0283a", "#3a2a1a"), "sub-summon": ("pentagram", "#c0283a", "#120404"), "sub-ward": ("shield", "#8e1424", "#3a2a5a"),
    # macros & tables
    "mc-bells": ("bell", "#e8c35a", "#5a0a12"), "mc-exhibit": ("scales", "#e8c35a", "#3a1a1a"), "mc-handout": ("scroll", "#efe2c0", "#3a2a1a"),
    "mc-fine": ("stamp", "#8e1424", "#1a4a2a"), "mc-challenge": ("dice", "#2c4f8a", "#10203a"), "mc-phase": ("devil", "#c23a2e", "#120404"),
    "mc-setup": ("gear", "#c09040", "#26262e"), "mc-night": ("sun", "#7a90c0", "#0a0a1a"), "mc-writ": ("seal", "#c09040", "#5a0a12"),
    "mc-save": ("shield", "#2c4f8a", "#10203a"), "mc-gift": ("gift", "#2f7a46", "#3a0a12"), "tb-dice": ("dice", "#8e1424", "#26262e"),
    "rc-title": ("devil", "#c23a2e", "#3a0a0a"),
    # Scriptorium v2 spells and the Contract Domain
    "sp-fine": ("magnifier", "#e8c35a", "#2a0a14"), "sp-sulfur": ("seal", "#ffb03a", "#2a1a0a"), "sp-arrears": ("ledger", "#c0283a", "#1a0a14"),
    "sp-objection": ("gavel", "#e8c35a", "#3a0a14"), "sp-retainer": ("coin", "#e8c35a", "#2a2a0a"), "sp-summons": ("letter", "#efe2c0", "#3a0a14", "§"),
    "sp-injunction": ("hand", "#c0283a", "#2a0a14"), "sp-repossess": ("sack", "#7a5a3a", "#2a0a14"), "sp-classaction": ("scroll", "#ff7a1a", "#3a0a0a"),
    "sp-servitude": ("manacles", "#9a96a2", "#3a0a3a"), "sp-amend": ("quill", "#c0283a", "#10303a"), "sp-foreclosure": ("coin", "#a8301e", "#120404"),
    "sp-cessation": ("gavel", "#9a96a2", "#10102a"), "sp-charter": ("key", "#c09040", "#2a0a14"), "sp-advocate": ("devil", "#c23a2e", "#1a0a14"),
    "sp-primeval": ("pentagram", "#ff5a1a", "#120404"), "sp-damnation": ("brand", "#ff2a1a", "#120404"),
    "sub-domain": ("ledger", "#e8c35a", "#3a0a14"), "sub-notary": ("stamp", "#c0283a", "#2a1a0a"), "sub-writ": ("letter", "#efe2c0", "#2a0a14", "W"),
    "sub-audit": ("magnifier", "#c09040", "#2a0a14"), "sub-lien": ("flame", "#c0283a", "#120404"), "sub-ledgermaster": ("crown", "#e8c35a", "#2a0a14"),
    "sub-retainer": ("devil", "#c23a2e", "#2a1a0a"), "mc-carol": ("bell", "#ffd84a", "#2f7a46"), "sub-authority": ("manacles", "#ff7a1a", "#2a0a14"),
}

ICONS.update({
    "ic-soulforged": ("golem", "#c09040", "#3a1a10"), "ic-sf-enforcer": ("golem", "#7ad0ff", "#1a2a4a"),
    "ic-sf-attendant": ("gear", "#5ad0e0", "#1a2a3a"), "ic-sf-directive": ("chain", "#5ad0e0", "#1a1a2a"),
    "ic-sf-conduit": ("spirit", "#5ad0e0", "#1a2a3a"), "ic-sf-twin": ("golem", "#ff9a3a", "#3a1a0a"),
    "ic-sf-mercy": ("heart", "#5ad0e0", "#1a2a3a"), "ic-sf-overclock": ("flame", "#ff5a1a", "#3a0a0a"),
    "ic-sf-imprint": ("coin", "#5ad0e0", "#2a1a2a"), "ic-sf-record": ("manifest", "#efe2c0", "#1a2a3a"),
    "ic-sf-covenant": ("scroll", "#efe2c0", "#1a2a3a", "SF"), "ic-sf-engineering": ("gear", "#c09040", "#3a2a10"),
    "ic-sf-etched": ("sigil", "#5ad0e0", "#1a1a2a"), "ic-sf-dominion": ("crown", "#7ad0ff", "#1a2a4a"),
    # Interplanal relics
    "ic-quill": ("quill", "#c0183a", "#3a2a1a"), "ic-receipt": ("scroll", "#efe2c0", "#5a1008", "H-25"),
    "ic-gauntlets": ("gauntlet", "#c09040", "#5a3214"), "ic-manacles": ("manacles", "#9ac08a", "#1a3a1a"),
    "ic-chain": ("chain", "#d8aa52", "#3a2a10"), "ic-seed": ("seed", "#8e1424", "#1a2a14"),
    "ic-glassheart": ("gear", "#7ad0ff", "#1a2a4a"), "ic-pyric-ring": ("ring", "#c0183a", "#3a0a1a"),
    "ic-splitter": ("sword", "#ffd27a", "#3a2a10"), "ic-gavel": ("gavel", "#3a2a1a", "#5a4214"),
    "ic-writshield": ("shield", "#8e1424", "#2a1a14"), "ic-hourglass": ("hourglass", "#ffd27a", "#3a2a10"),
    "ic-lantern": ("lantern", "#ffd27a", "#2a1a2a"), "ic-shears": ("shears", "#2a2a30", "#3a0a10"),
    "ic-crownmark": ("crown", "#e8c35a", "#5a1008"), "ic-proof": ("seal", "#d8aa52", "#3a2a1a"),
    "ic-exhibit": ("scroll", "#efe2c0", "#3a2a1a", "EX"), "ic-core": ("heart", "#7ad0ff", "#1a2a4a"),
    "ic-roster": ("manifest", "#efe2c0", "#3a1a1a"), "ic-writ": ("scroll", "#ffb4b4", "#3a0a1a", "M-9"),
    "ic-heartstone": ("heart", "#ff3a5a", "#3a0a1a"), "ic-stamp": ("stamp", "#c0183a", "#2a1a14"),
    "ic-key": ("key", "#d8aa52", "#2a1a2a"), "ic-soulcoin": ("coin", "#a8301e", "#3a0a10"),
    # subclass features
    "ic-ruby": ("sigil", "#c0183a", "#3a0a1a"), "ic-term": ("scroll", "#efe2c0", "#3a0a1a", "T"),
    "ic-consideration": ("coin", "#c0183a", "#2a0a14"), "ic-reserved": ("shield", "#c0183a", "#2a0a14"),
    "ic-final-notice": ("chain", "#ff5a5a", "#3a0a10"), "ic-bloodprice": ("axe", "#c8ccd6", "#3a0a0a"),
    "ic-vow": ("vow", "#c0183a", "#3a0a0a"), "ic-guardian": ("shield", "#8a2a1a", "#2a1a14"),
    "ic-witness": ("eye", "#ffd27a", "#3a0a0a"), "ic-pricedue": ("slashes", "#c0183a", "#2a0a0a"),
    "ic-ashen": ("tree", "#4a3a30", "#2a1a10"), "ic-accord": ("hands", "#d8a888", "#2a1a10"),
    "ic-warden": ("spirit", "#ff7a1a", "#2a1a10"), "ic-remedy": ("thorn", "#5a8a3a", "#1a2a10"),
    "ic-embers": ("flame", "#ff7a1a", "#2a1a10"), "ic-court-ash": ("tree", "#8a8a8a", "#1a1a1a"),
    # creature actions
    "ic-slam": ("golem", "#5a5660", "#2a1a14"), "ic-golem": ("golem", "#7ad0ff", "#1a2a4a"), "ic-shrapnel": ("slashes", "#ff7a1a", "#2a1a14"),
    "ic-bolt": ("brand", "#7ad0ff", "#1a2a4a"), "ic-hex": ("pentagram", "#8a5ac0", "#1a0a2a"),
    "ic-talon": ("thorn", "#c0183a", "#2a0a14"), "ic-needle": ("staple", "#8a5ac0", "#1a0a2a"),
    "ic-glare": ("eye", "#ff3a5a", "#2a0a14"), "ic-drain": ("heart", "#5a1a2a", "#1a0a10"),
    "ic-portal": ("portal", "#ff6a1a", "#2a1a10"), "ic-glaive": ("spear", "#ff7a1a", "#3a0a0a"),
    "ic-hammer": ("gavel", "#c09040", "#3a2a10"), "ic-edict": ("crown", "#c0183a", "#2a0a0a"),
    "ic-pen": ("quill", "#c0183a", "#1a1418"), "ic-sceptre": ("key", "#5ad08a", "#1a2a1a"),
    "ic-rose": ("rose", "#c0183a", "#2a0a14"), "ic-sabre": ("sword", "#e9eef6", "#1a2a4a"),
    # spells (new 17)
    "ic-sp-witness": ("eye", "#ffd27a", "#3a2a10"), "ic-sp-ember": ("coal", "#ff5a1a", "#3a1a10"),
    "ic-sp-objection": ("lips", "#c0183a", "#2a1a2a"), "ic-sp-promissory": ("shield", "#d8aa52", "#2a1a14"),
    "ic-sp-registry": ("ledger", "#2c4f8a", "#1a1a2a"), "ic-sp-chains": ("chain", "#d8aa52", "#2a1a10"),
    "ic-sp-passage": ("key", "#ffd27a", "#3a2a10"), "ic-sp-duel": ("sword", "#e9eef6", "#3a0a10"),
    "ic-sp-memory": ("musicbox", "#8a5ac0", "#1a0a2a"), "ic-sp-breach": ("gear", "#ff5a1a", "#2a1a10"),
    "ic-sp-injunction": ("gavel", "#c0183a", "#2a0a14"), "ic-sp-audit": ("magnifier", "#7ac0e0", "#1a2a3a"),
    "ic-sp-sever": ("shears", "#c0c4d0", "#2a1a2a"), "ic-sp-reprieve": ("portal", "#7ad0ff", "#1a2a3a"),
    "ic-sp-sovereign": ("crown", "#c0183a", "#2a0a14"), "ic-sp-dawn": ("sun", "#ffd27a", "#3a2a10"),
    "ic-sp-statute": ("crown", "#e8c35a", "#3a2a10"),
    # macros / misc
    "ic-title": ("crown", "#e8c35a", "#5a1008"), "ic-tracker": ("scales", "#e8c35a", "#3a2a10"),
    "ic-arena": ("dice", "#8e1424", "#3a0a0a"), "ic-tribunal": ("gavel", "#c09040", "#3a2a10"),
    "ic-battle": ("arrows", "#e8c35a", "#3a2a10"), "ic-clock": ("clock", "#efe6cf", "#2a1a14"),
})


def build():
    import os
    os.makedirs(OUT, exist_ok=True)
    for name, spec in ICONS.items():
        g, col, bgc = spec[0], spec[1], spec[2]
        fn = G[g]
        if g in ("letter",):
            inner = fn(col, spec[3])
        elif g == "scroll" and len(spec) > 3:
            inner = fn(col, spec[3])
        else:
            inner = fn(col)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">{DEFS}'
               f'<radialGradient id="ib"><stop offset="0" stop-color="{bgc}"/><stop offset="1" stop-color="#0a0405"/></radialGradient>'
               f'<rect x="4" y="4" width="248" height="248" rx="26" fill="url(#ib)" stroke="#120909" stroke-width="8"/>'
               f'<rect x="12" y="12" width="232" height="232" rx="20" fill="none" stroke="#b8862e" stroke-width="3" opacity="0.8"/>'
               f'<g transform="translate(128,128) scale(0.8) translate(-128,-128)">{inner}</g></svg>')
        render(svg, f"{OUT}/{name}.webp", 256)
    print(len(ICONS), "icons")


if __name__ == "__main__":
    build()
