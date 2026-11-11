"""Portrait + overhead token specs for every actor."""
import math, sys
from chibi import *
from chibi import _held, _grip
import props as pr

F = dict  # shorthand

DEVIL = F(skin="#c23a2e", skin_dk="#7a1a14", iris="#ffd27a", slit=True)
CAST = {}


def C(key, portrait, token, bgc="#5a1018"):
    CAST[key] = (portrait, token, bgc)


# ---- extra held items for Avernus
def i_axe():
    return (f'<g transform="translate(730,800) rotate(-25)"><rect x="-16" y="-330" width="32" height="480" rx="12" fill="#5a3416" {S(9)}/>'
            f'<path d="M14 -330 Q180 -300 170 -150 Q90 -190 14 -180 Z" fill="#c8ccd6" {S(10)}/><path d="M-14 -320 Q-150 -290 -140 -170 Q-70 -200 -14 -190 Z" fill="#a8acb6" {S(9)}/></g>')


def i_hammer():
    return (f'<g transform="translate(720,780) rotate(-25)"><rect x="-16" y="-260" width="32" height="420" rx="12" fill="#3a2210" {S(9)}/>'
            f'<rect x="-110" y="-350" width="220" height="120" rx="16" fill="url(#brass)" {S(11)}/><rect x="-110" y="-300" width="220" height="24" fill="#6a4410"/></g>')


def i_glaive():
    return (f'<g transform="translate(250,760) rotate(12)"><rect x="-12" y="-460" width="24" height="640" rx="10" fill="#2a1a1a" {S(8)}/>'
            f'<path d="M0 -460 Q90 -560 40 -700 Q10 -600 -20 -470 Z" fill="#e05a2a" {S(9)}/><path d="M0 -460 Q90 -560 40 -700" stroke="#ffd27a" stroke-width="8" fill="none" filter="url(#glw)"/></g>')


def i_sceptre(top="#5ad08a"):
    return (f'<g transform="translate(720,780) rotate(-20)"><rect x="-14" y="-260" width="28" height="400" rx="10" fill="url(#brass)" {S(8)}/>'
            f'<path d="M0 -360 L50 -280 L0 -230 L-50 -280 Z" fill="{top}" {S(8)}/><circle cy="-290" r="80" fill="{top}" filter="url(#glw)" opacity="0.5"/></g>')


def i_pen():
    return (f'<g transform="translate(720,780) rotate(30)"><rect x="-22" y="-300" width="44" height="380" rx="14" fill="#1a1418" {S(9)}/>'
            f'<path d="M-22 80 L0 170 L22 80 Z" fill="url(#brass)" {S(7)}/><rect x="-22" y="-120" width="44" height="30" fill="url(#brass)" {S(5)}/>'
            f'<circle cy="200" r="36" fill="#c0183a" filter="url(#glw)" opacity="0.7"/></g>')


def i_sickle():
    return (f'<g transform="translate(720,820) rotate(-15)"><rect x="-14" y="-40" width="28" height="200" rx="10" fill="#5a3416" {S(8)}/>'
            f'<path d="M0 -40 Q-10 -240 170 -270 Q40 -200 30 -40 Z" fill="#dfe6ef" {S(9)}/></g>')


def i_tinker():
    return (f'<g transform="translate(720,820)"><circle r="110" fill="url(#brass)" {S(10)}/>'
            + "".join(f'<rect x="-22" y="-150" width="44" height="50" fill="url(#brass)" {S(6)} transform="rotate({a})"/>' for a in range(0, 360, 45))
            + f'<circle r="44" fill="#7ad0ff" {S(7)}/><circle r="80" fill="#7ad0ff" filter="url(#glw)" opacity="0.4"/></g>')


def i_rose():
    return (f'<g transform="translate(720,650)"><path d="M0 0 Q-20 140 10 240" stroke="#2a2830" stroke-width="18" fill="none"/>'
            + "".join(f'<ellipse cx="{math.cos(a)*40:.0f}" cy="{math.sin(a)*40:.0f}" rx="56" ry="34" fill="#4a4652" {S(7)} transform="rotate({math.degrees(a):.0f} {math.cos(a)*40:.0f} {math.sin(a)*40:.0f})"/>' for a in [i*math.pi/3.5 for i in range(7)])
            + f'<circle r="34" fill="#c0183a" {S(7)}/></g>')


i_axe = _held(i_axe, 730, 800, -25, 0, 110)
i_hammer = _held(i_hammer, 720, 780, -25, 0, 110)
i_glaive = _held(i_glaive, 250, 760, 12, 0, 120, "lhand")
i_sceptre = _held(i_sceptre, 720, 780, -20, 0, 100)
i_pen = _held(i_pen, 720, 780, 30, 0, 20)
i_sickle = _held(i_sickle, 720, 820, -15, 0, 110)
i_tinker = _held(i_tinker, 720, 820, 0, 0, 125)
i_rose = _held(i_rose, 720, 650, 0, -4, 175)

HAG = F(skin="#7a8a6a", skin_dk="#4a5a3a", iris="#e8d84a", slit=True)
FIEND = F(skin="#a8303a", skin_dk="#6a1018", iris="#ffd27a", slit=True)


def hellfire(c="#ff5a1a"):
    return f'<rect width="1000" height="1000" fill="{c}" opacity="0.06"/>'


# ---- Chapter I-II
C("janella-greenbottle",
  F(skin="#e8b896", skin_dk="#b88466", coat="#6a4a2a", trim="#c09040", hair="#c86a2a", hair_style="bun", spectacles=True,
    mouth="frown", brow="worried", nose="button", iris="#3a8a5a", head=1.15, body_w=230, blush=True, item=i_tinker(),
    over='<rect x="390" y="760" width="220" height="40" rx="10" fill="#3a2a1a" stroke="#120909" stroke-width="8"/>', seed=31),
  F(shoulders=200, coat="#6a4a2a", trim="#c09040", cap="hair", cap_c="#c86a2a", bun=True, head=135, item=ot_item("lantern", 1)), "#3a2a14")
C("lila-greenbottle",
  F(skin="#f0c8a8", skin_dk="#c09878", coat="#3a6a4a", hair="#c86a2a", hair_style="messy", mouth="o", brow="worried",
    nose="button", iris="#3a8a5a", head=1.25, body_w=200, blush=True, tears=True, seed=32),
  F(shoulders=170, coat="#3a6a4a", cap="hair", cap_c="#c86a2a", head=130), "#1a3a2a")
C("ash-scrap-golem",
  F(kind="brass", coat="#4a4650", trim="#7a5a3a", ears="none", nose="none", mouth="fixed", eye_glow="#ff7a1a", iris="#ff7a1a",
    brow="none", gloves="url(#iron)", body_w=340, collar=False,
    over='<path d="M300 880 l80 -60 l60 70 l90 -80 l70 60" stroke="#ff7a1a" stroke-width="10" fill="none" filter="url(#glw)"/>', seed=33),
  F(shoulders=300, coat="#4a4650", trim="#7a5a3a", cap="helm", cap_c="url(#iron)", head=150, hand="#5a5660", face=False), "#3a2a1a")
C("iron-warder-damaged",
  F(kind="brass", coat="#3a3a42", trim="#8a2a1a", ears="none", nose="none", mouth="fixed", eye_glow="#7a1a1a", iris="#3a0a0a",
    brow="none", gloves="url(#iron)", body_w=380, head=1.1,
    over='<circle cx="500" cy="840" r="70" fill="#140c0c" stroke="#120909" stroke-width="12"/><path d="M380 300 l60 80 l-30 60" stroke="#120909" stroke-width="10" fill="none"/>'
         '<text x="500" y="980" font-family="Cinzel" font-weight="700" font-size="44" fill="#d8aa52" text-anchor="middle">J.G.</text>', seed=34),
  F(shoulders=360, coat="#3a3a42", trim="#8a2a1a", cap="helm", cap_c="url(#iron)", head=170, hand="#4a4650", face=False), "#26232a")
C("iron-warder-restored",
  F(kind="brass", coat="#3a3a42", trim="#d8aa52", ears="none", nose="none", mouth="fixed", eye_glow="#7ad0ff", iris="#7ad0ff",
    brow="none", gloves="url(#iron)", body_w=380, head=1.1,
    over='<circle cx="500" cy="840" r="70" fill="#7ad0ff" stroke="#120909" stroke-width="12"/><circle cx="500" cy="840" r="110" fill="#7ad0ff" filter="url(#glw)" opacity="0.5"/>', seed=35),
  F(shoulders=360, coat="#3a3a42", trim="#d8aa52", cap="helm", cap_c="url(#iron)", head=170, hand="#4a4650", face=False,
    over='<circle cx="500" cy="560" r="40" fill="#7ad0ff"/>'), "#1a2a4a")
C("iron-heir",
  F(kind="brass", coat="#2a2a30", trim="#c0183a", ears="none", nose="none", mouth="fixed", eye_glow="#ff3a3a", iris="#ff3a3a",
    brow="none", gloves="url(#brass)", body_w=400, head=1.1, hat="crown", hat_c="url(#brass)", item=i_sceptre("#c0183a"), seed=36),
  F(shoulders=380, coat="#2a2a30", trim="#c0183a", cap="helm", cap_c="url(#brass)", head=170, hand="#d8aa52", face=False,
    over='<path d="M380 380 l40 -60 l40 50 l40 -70 l40 70 l40 -50 l40 60 Z" fill="#d8aa52" stroke="#120909" stroke-width="10"/>'), "#3a0a10")
C("contract-sentinel",
  F(kind="brass", coat="#5a2a18", trim="#d8aa52", ears="none", nose="none", mouth="fixed", eye_glow="#ffd27a", iris="#ffd27a",
    brow="none", gloves="url(#brass)", body_w=380, hat="tophat", item=i_hammer(), seed=37,
    over='<rect x="400" y="800" width="200" height="120" fill="#efe2c0" stroke="#120909" stroke-width="8"/><path d="M430 830 h140 M430 860 h140 M430 890 h90" stroke="#5a1a1a" stroke-width="6"/>'),
  F(shoulders=360, coat="#5a2a18", trim="#d8aa52", cap="tophat", head=160, hand="#d8aa52", face=False, item=ot_item("maul", 1)), "#5a3214")
C("writ-bailiff",
  F(**FIEND, coat="#1a1418", trim="#c0183a", horns="small", ears="pointed", mouth="fangs", nose="hook", brow="angry", hat="tophat",
    item=i_mace(), seed=38),
  F(shoulders=260, coat="#1a1418", trim="#c0183a", cap="tophat", head=145, horns=True, ears="pointed", skin="#a8303a",
    skin_dk="#6a1018", hand="#a8303a", item=ot_item("baton", 1)), "#3a0a10")
C("imp-tollkeeper",
  F(**FIEND, coat="#5a2a18", trim="#d8aa52", horns="small", ears="pointed", mouth="grin", nose="hook", brow="angry",
    head=1.25, body_w=190, spectacles=True, item=i_clipboard(), seed=39,
    over='<path d="M180 640 Q60 500 140 380 Q200 520 260 600 Z M820 640 Q940 500 860 380 Q800 520 740 600 Z" fill="#6a1018" stroke="#120909" stroke-width="10"/>'),
  F(shoulders=160, coat="#5a2a18", trim="#d8aa52", head=130, horns=True, ears="pointed", skin="#a8303a", skin_dk="#6a1018",
    hand="#a8303a", item=ot_item("clipboard", 1), cape="#6a1018"), "#5a1a10")
C("skull-notary",
  F(skin="#e8dcc0", skin_dk="#a8987a", coat="#3a5a4a", ears="none", nose="none", mouth="grin", eye_glow="#7ad0a0",
    iris="#120909", brow="none", hands=False, body_w=1, item=i_quill(), eye=1.15,
    over='<rect width="1000" height="1000" fill="#7ad0a0" opacity="0.06"/>', seed=40),
  F(shoulders=1, coat="#3a5a4a", head=200, face=False, skin="#e8dcc0",
    over='<circle cx="430" cy="500" r="40" fill="#120909"/><circle cx="570" cy="500" r="40" fill="#120909"/><circle cx="430" cy="500" r="16" fill="#7ad0a0"/><circle cx="570" cy="500" r="16" fill="#7ad0a0"/>'), "#10302a")
C("styx-ferryman",
  F(kind="ghost", skin="#3a3a4a", skin_dk="#1a1a2a", coat="#1a1a24", coat_dk="#0a0a10", hood="#2a2a3a", ears="none", nose="none",
    mouth="none", eye_glow="#7ad0a0", iris="#7ad0a0", brow="none", hands=False, item=i_staff("#7ad0a0"), seed=41),
  F(shoulders=260, coat="#1a1a24", cap="hood", cap_c="#2a2a3a", head=150, face=False, item=ot_item("staff", 1, "#7ad0a0")), "#0a1a1a")
C("vexa-corven",
  F(skin="#c99070", skin_dk="#8a5a40", coat="#2a3a5a", trim="#c0c4d0", hair="#1a1418", hair_style="long", mouth="smile",
    brow="angry", nose="hook", scar=True, iris="#5a8aa0", item=i_sword(None, -30), seed=42),
  F(shoulders=240, coat="#2a3a5a", trim="#c0c4d0", cap="hair", cap_c="#1a1418", head=145, item=ot_item("sword", 1)), "#1a2a4a")
C("osric-kane",
  F(skin="#d8b0a0", skin_dk="#a87a6a", coat="#4a1a2a", trim="#d8aa52", hair="#8a8a8a", hair_style="fringe", beard="short",
    beard_c="#8a8a8a", mouth="frown", brow="worried", nose="bulb", iris="#5a6a4a", hat="crown", hat_c="#6a6a72",
    item=i_sceptre("#5ad08a"), body_w=320, warts=[(0.5, 0.4)], seed=43),
  F(shoulders=290, coat="#4a1a2a", trim="#d8aa52", cap="hair", cap_c="#8a8a8a", head=150, beard=True, beard_c="#8a8a8a",
    over='<path d="M410 400 l30 -40 l30 30 l30 -40 l30 40 l30 -30 l30 40 Z" fill="#6a6a72" stroke="#120909" stroke-width="8"/>'), "#2a0a1a")
C("lemure",
  F(skin="#c8607a", skin_dk="#8a3a4a", coat="#a04a5a", coat_dk="#6a2a3a", ears="none", nose="none", mouth="o",
    eye_glow="#ff5a5a", iris="#3a0a0a", brow="worried", hands=False, body_w=360, seed=44),
  F(shoulders=280, coat="#a04a5a", head=170, face=False, skin="#c8607a", hand="#c8607a"), "#4a0a1a")
C("cadaver-collector",
  F(kind="brass", coat="#3a3a40", trim="#5a5a62", ears="none", nose="none", mouth="fixed", eye_glow="#7ad0a0", iris="#7ad0a0",
    brow="none", hat="helm", hat_c="url(#iron)", gloves="url(#iron)", body_w=380, item=i_spear(), seed=45,
    over='<circle cx="320" cy="860" r="40" fill="#e8dcc0" stroke="#120909" stroke-width="8"/><circle cx="680" cy="860" r="40" fill="#e8dcc0" stroke="#120909" stroke-width="8"/>'),
  F(shoulders=360, coat="#3a3a40", trim="#5a5a62", cap="helm", cap_c="url(#iron)", head=160, hand="#5a5660", face=False,
    item=ot_item("spear", 1)), "#1a2a2a")
C("brass-registrar",
  F(kind="brass", coat="#5a3a1a", trim="#d8aa52", ears="none", nose="none", mouth="fixed", eye_glow="#ffd27a", iris="#ffd27a",
    brow="none", hat="tophat", spectacles=True, gloves="url(#brass)", item=i_clipboard(), seed=46),
  F(shoulders=260, coat="#5a3a1a", trim="#d8aa52", cap="tophat", head=150, hand="#d8aa52", face=False, item=ot_item("clipboard", 1)), "#5a4214")
C("spectral-clerk",
  F(kind="ghost", skin="#bfe6f0", skin_dk="#7ab0c0", coat="#9fd0e0", coat_dk="#6a9ab0", hair="#dfe6ef", hair_style="messy",
    spectacles=True, mouth="o", eye_glow="#bfe6ff", iris="#bfe6ff", brow="worried", nose="hook", item=i_quill(), seed=47,
    over='<rect width="1000" height="1000" fill="#bfe6f0" opacity="0.08"/>'),
  F(shoulders=230, coat="#9fd0e0", cap="hair", cap_c="#dfe6ef", head=145, face=False, item=ot_item("clipboard", 1)), "#10303a")
# ---- the Pyric Triune
C("mother-sable",
  F(**HAG, coat="#1a1418", trim="#5a1a3a", hood="#2a1a2a", hat="witch", hat_c="#1a1418", mouth="smile", nose="hook",
    brow="angry", warts=[(0.5, 0.35), (-0.55, -0.2)], spectacles=True, item=i_scroll(), seed=48),
  F(shoulders=240, coat="#1a1418", trim="#5a1a3a", cap="hood", cap_c="#2a1a2a", head=145, skin="#7a8a6a", hand="#7a8a6a",
    item=ot_item("clipboard", 1)), "#1a0a1a")
C("night-hag-advocate",
  F(skin="#4a3a5a", skin_dk="#2a1a3a", iris="#ff5a5a", slit=True, coat="#2a1a2a", trim="#8e1424", hair="#1a1418",
    hair_style="long", mouth="fangs", nose="hook", brow="angry", warts=[(0.45, 0.4), (-0.4, -0.35)], eye_glow="#ff5a5a",
    item=i_scroll(), seed=49),
  F(shoulders=240, coat="#2a1a2a", trim="#8e1424", cap="hair", cap_c="#1a1418", head=145, skin="#4a3a5a", hand="#4a3a5a",
    cape="#1a0a1a"), "#1a0a1a")
C("misty",
  F(skin="#c8b8d8", skin_dk="#8a7aa0", iris="#ff3a5a", slit=True, coat="#3a0a1a", trim="#c0183a", hair="#1a1018",
    hair_style="long", hat="thorns", mouth="smile", nose="button", brow="kind", eye_glow="#ff3a5a", item=i_rose(),
    over=hellfire("#c0183a") + '<path d="M180 980 Q120 760 260 680 M820 980 Q880 760 740 680" stroke="#2a1418" stroke-width="22" fill="none"/>', seed=50),
  F(shoulders=260, coat="#3a0a1a", trim="#c0183a", cap="hair", cap_c="#1a1018", head=150, skin="#c8b8d8", hand="#c8b8d8",
    cape="#1a0a10",
    over='<circle cx="500" cy="420" r="0"/>' + "".join(f'<path d="M{400+i*25} 400 l{(-1)**i*14} -30" stroke="#120909" stroke-width="10"/>' for i in range(9))), "#3a0a1a")
C("misty-unbound",
  F(skin="#8a6aa0", skin_dk="#4a2a60", iris="#ff3a5a", slit=True, coat="#1a0410", trim="#ff3a5a", hair="#0a0408",
    hair_style="long", hat="thorns", horns="curl", mouth="fangs", nose="hook", brow="angry", eye_glow="#ff3a5a", item=i_rose(),
    over=hellfire("#ff1a3a") + '<path d="M120 1000 Q60 700 220 600 M880 1000 Q940 700 780 600 M300 1000 Q260 820 340 740 M700 1000 Q740 820 660 740" stroke="#2a1418" stroke-width="26" fill="none"/>', seed=51),
  F(shoulders=290, coat="#1a0410", trim="#ff3a5a", cap="hair", cap_c="#0a0408", head=160, horns=True, skin="#8a6aa0",
    hand="#8a6aa0", cape="#3a0a1a"), "#2a0410")
C("oathshard",
  F(kind="ghost", skin="#e0c8e8", skin_dk="#a088b0", coat="#5a1a3a", trim="#ff8aaa", hair="#2a1018", hair_style="long",
    hat="thorns", mouth="smile", nose="button", brow="angry", eye_glow="#ff8aaa", iris="#ff8aaa", item=i_spear(), seed=52,
    over='<rect width="1000" height="1000" fill="#ff8aaa" opacity="0.07"/>'),
  F(shoulders=240, coat="#5a1a3a", trim="#ff8aaa", cap="hair", cap_c="#2a1018", head=145, face=False, item=ot_item("spear", 1)), "#3a0a2a")
C("child-of-hell",
  F(**FIEND, coat="#3a0a10", ears="pointed", horns="small", mouth="fangs", nose="button", brow="angry", head=1.3, body_w=200,
    eye_glow="#ffd27a", seed=53),
  F(shoulders=160, coat="#3a0a10", head=140, horns=True, ears="pointed", skin="#a8303a", skin_dk="#6a1018", hand="#a8303a"), "#3a0a10")
C("isolde",
  F(skin="#e8d0c8", skin_dk="#b09890", coat="#5a2a6a", trim="#d8aa52", hair="#d8c0a0", hair_style="long", mouth="fixed",
    brow="kind", nose="button", iris="#8a6ab0",
    over='<path d="M330 400 Q500 340 670 400 L650 520 Q500 560 350 520 Z" fill="#f4ecd0" stroke="#120909" stroke-width="10"/><circle cx="430" cy="455" r="22" fill="#120909"/><circle cx="570" cy="455" r="22" fill="#120909"/>', seed=54),
  F(shoulders=230, coat="#5a2a6a", trim="#d8aa52", cap="hair", cap_c="#d8c0a0", head=145, face=False), "#2a1a3a")
# ---- claimants and officials
C("hollis-valrick",
  F(skin="#d8c0b0", skin_dk="#a89080", coat="#2a2a30", trim="#c0183a", hair="#3a3038", hair_style="fringe", spectacles=True,
    mouth="smile", brow="angry", nose="hook", iris="#6a6a7a", item=i_pen(), body_w=250, seed=55),
  F(shoulders=230, coat="#2a2a30", trim="#c0183a", cap="hair", cap_c="#3a3038", head=145, item=ot_item("clipboard", 1)), "#1a1418")
C("marshal-kordren",
  F(**FIEND, coat="#3a0a0a", armor="#4a4650", horns="curl", ears="pointed", mouth="fangs", nose="hook", brow="angry", scar=True,
    item=i_glaive(), body_w=340, seed=56,
    over='<path d="M140 760 Q40 560 160 420 Q240 600 280 700 Z M860 760 Q960 560 840 420 Q760 600 720 700 Z" fill="#5a1418" stroke="#120909" stroke-width="10"/>'),
  F(shoulders=320, coat="#4a4650", trim="#c0183a", cap="helm", cap_c="#3a0a0a", head=150, horns=True, skin="#a8303a",
    item=ot_item("spear", 1), cape="#5a1418"), "#3a0a0a")
C("brass-factor-morn",
  F(skin="#c8a080", skin_dk="#987050", coat="#5a3a1a", armor="url(#brass)", hat="helm", hat_c="url(#brass)", beard="full",
    beard_c="#5a3a2a", mouth_in_beard=True, mouth="none", brow="angry", nose="bulb", iris="#5a4a2a", item=i_hammer(), body_w=340, seed=57),
  F(shoulders=320, coat="url(#brass)", cap="helm", cap_c="url(#brass)", head=150, beard=True, beard_c="#5a3a2a", item=ot_item("maul", 1)), "#5a4214")
C("corda-kain",
  F(skin="#c8a898", skin_dk="#987868", coat="#3a3a42", armor="#8a8f99", hair="#c0c4d0", hair_style="bun", mouth="frown",
    brow="angry", nose="hook", iris="#6a6a7a", item=i_sword(None, -15), seed=58),
  F(shoulders=280, coat="#8a8f99", trim="#c0183a", cap="hair", cap_c="#c0c4d0", bun=True, head=145, item=ot_item("sword", 1)), "#2a2a32")
C("magistrate-khel",
  F(skin="#d8b090", skin_dk="#a88060", coat="#5a3a1a", trim="#d8aa52", hat="tophat", spectacles=True, beard="short",
    beard_c="#3a2a1a", mouth="frown", brow="worried", nose="bulb", iris="#5a4a2a", item=i_clipboard(), seed=59),
  F(shoulders=270, coat="#5a3a1a", trim="#d8aa52", cap="tophat", head=150, beard=True, beard_c="#3a2a1a", item=ot_item("clipboard", 1)), "#5a4214")
C("sergeant-orro",
  F(**FIEND, coat="#3a2a1a", trim="#8a6a3a", horns="small", ears="pointed", mouth="grin", nose="bulb", brow="angry",
    body_w=330, item=i_scroll(), warts=[(0.5, 0.4)], seed=60),
  F(shoulders=290, coat="#3a2a1a", trim="#8a6a3a", head=150, horns=True, ears="pointed", skin="#a8303a", skin_dk="#6a1018",
    hand="#a8303a", item=ot_item("clipboard", 1)), "#3a2a14")
C("claims-clerk",
  F(**FIEND, coat="#2a2a30", trim="#d8aa52", horns="small", ears="pointed", spectacles=True, mouth="fixed", nose="hook",
    brow="worried", item=i_clipboard(), seed=61),
  F(shoulders=220, coat="#2a2a30", trim="#d8aa52", head=140, horns=True, ears="pointed", skin="#a8303a", skin_dk="#6a1018",
    hand="#a8303a", item=ot_item("clipboard", 1)), "#2a1a14")
C("magistrate-docket",
  F(kind="brass", coat="#1a1418", trim="#d8aa52", ears="none", nose="none", mouth="fixed", eye_glow="#ffd27a", iris="#ffd27a",
    brow="none", hat="tophat", gloves="url(#brass)",
    over='<g transform="translate(500,880) scale(0.9)"><path d="M-150 0 h300 M0 -60 v120 M-150 0 l-40 80 h80 Z M150 0 l-40 80 h80 Z" stroke="#d8aa52" stroke-width="12" fill="none"/></g>', seed=62),
  F(shoulders=280, coat="#1a1418", trim="#d8aa52", cap="tophat", head=155, hand="#d8aa52", face=False), "#3a2a10")
C("brass-arbiter", arbiter_p(), "arbiter", "#5a4214")
C("masked-champion-living",
  F(skin="#d8b090", skin_dk="#a88060", coat="#8e1424", trim="#d8aa52", hair="#3a2a1a", hair_style="fringe", mouth="smile",
    brow="kind", nose="button",
    over='<path d="M330 400 Q500 340 670 400 L650 500 Q500 530 350 500 Z" fill="#c0183a" stroke="#120909" stroke-width="10"/><circle cx="430" cy="445" r="22" fill="#120909"/><circle cx="570" cy="445" r="22" fill="#120909"/>', seed=63),
  F(shoulders=240, coat="#8e1424", trim="#d8aa52", cap="hair", cap_c="#3a2a1a", head=145, face=False), "#3a0a10")
C("masked-champion-construct",
  F(kind="brass", coat="#8e1424", trim="#d8aa52", ears="none", nose="none", mouth="fixed", eye_glow="#7ad0ff", iris="#7ad0ff",
    brow="none",
    over='<path d="M330 400 Q500 340 670 400 L650 500 Q500 530 350 500 Z" fill="#c0183a" stroke="#120909" stroke-width="10"/><circle cx="430" cy="445" r="22" fill="#7ad0ff"/><circle cx="570" cy="445" r="22" fill="#7ad0ff"/>', seed=64),
  F(shoulders=240, coat="#8e1424", trim="#d8aa52", cap="helm", cap_c="url(#brass)", head=145, face=False), "#3a0a10")
C("masked-champion-memory",
  F(kind="ghost", skin="#bfe6f0", skin_dk="#7ab0c0", coat="#8e1424", trim="#d8aa52", hair="#dfe6ef", hair_style="long",
    mouth="o", brow="worried", nose="button", eye_glow="#bfe6ff", iris="#bfe6ff",
    over='<path d="M330 400 Q500 340 670 400 L650 500 Q500 530 350 500 Z" fill="#c0183a" stroke="#120909" stroke-width="10" opacity="0.8"/>', seed=65),
  F(shoulders=240, coat="#8e1424", trim="#d8aa52", cap="hair", cap_c="#dfe6ef", head=145, face=False), "#3a0a10")
C("ashclad-petitioner",
  F(skin="#b08a70", skin_dk="#806048", coat="#5a5a5a", hood="#4a4a4a", mouth="frown", brow="worried", nose="bulb", iris="#5a6a5a",
    item=i_spear(), seed=66),
  F(shoulders=240, coat="#5a5a5a", cap="hood", cap_c="#4a4a4a", head=145, item=ot_item("spear", 1)), "#2a2a2a")
C("greyhurst-survivor",
  F(skin="#e0b8a0", skin_dk="#a88068", coat="#4a3a2a", hair="#6a5a4a", hair_style="messy", mouth="frown", brow="worried",
    tears=True, nose="button", iris="#4a6a8a", seed=67),
  F(shoulders=220, coat="#4a3a2a", cap="hair", cap_c="#6a5a4a", head=140), "#2a2014")
# ---- pregenerated claimants (level 12)
C("pc-aurelia",
  F(skin="#b0304a", skin_dk="#701a2a", coat="#2a1a2e", trim="#c0183a", horns="curl", hair="#1a1418", hair_style="long",
    mouth="smile", brow="angry", nose="button", iris="#ffd27a", slit=True, spectacles=True, item=i_quill(), seed=70,
    over='<path d="M330 740 h340" stroke="#d8aa52" stroke-width="10"/>'),
  F(shoulders=240, coat="#2a1a2e", trim="#c0183a", cap="hair", cap_c="#1a1418", horns=True, head=145, skin="#b0304a",
    hand="#b0304a", item=ot_item("clipboard", 1)), "#5a0a2a")
C("pc-varka",
  F(skin="#7a9a6a", skin_dk="#4a6a3a", coat="#3a2a1a", armor="#6a5a4a", hair="#1a1418", hair_style="messy", mouth="fangs",
    brow="angry", nose="bulb", iris="#c0183a", scar=True, item=i_axe(), body_w=350, seed=71,
    over='<path d="M300 760 l400 0" stroke="#8e1424" stroke-width="30"/>'),
  F(shoulders=320, coat="#3a2a1a", cap="hair", cap_c="#1a1418", head=150, skin="#7a9a6a", hand="#7a9a6a", item=ot_item("maul", 1),
    cape="#8e1424"), "#3a1a10")
C("pc-ilyra",
  F(skin="#c89878", skin_dk="#987058", coat="#3a4a2a", trim="#8a2a1a", hair="#e8e0d0", hair_style="long", ears="pointed",
    mouth="smile", brow="kind", nose="button", iris="#5aa06a", item=i_sickle(), seed=72,
    over='<g transform="translate(500,330)">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="34" ry="16" fill="#8a2a1a" stroke="#120909" stroke-width="6" transform="rotate({r} {x} {y})"/>' for x, y, r in ((-120, 0, -30), (-60, -30, -10), (0, -40, 0), (60, -30, 10), (120, 0, 30))) + '</g>'),
  F(shoulders=230, coat="#3a4a2a", trim="#8a2a1a", cap="hair", cap_c="#e8e0d0", head=145, ears="pointed", item=ot_item("staff", 1, "#ff7a1a")), "#1a2a14")
C("pc-orren",
  F(skin="#e0b090", skin_dk="#b08060", coat="#2c2a4a", trim="#d8aa52", hair="#6a4a2a", hair_style="messy", spectacles=True,
    mouth="o", brow="worried", nose="hook", iris="#3a5a8a", item=i_staff("#7ad0ff"), beard="short", beard_c="#6a4a2a", seed=73),
  F(shoulders=230, coat="#2c2a4a", trim="#d8aa52", cap="hair", cap_c="#6a4a2a", head=145, beard=True, beard_c="#6a4a2a",
    item=ot_item("staff", 1, "#7ad0ff")), "#1a1a3a")
C("pc-caldris",
  F(skin="#3a6a8a", skin_dk="#1a3a5a", coat="#2a2a30", armor="#a8acb6", hat="helm", hat_c="#3a3a42", mouth="fangs",
    brow="angry", nose="none", iris="#ffd27a", slit=True, item=i_sword("#ffb43a"), body_w=340, seed=74,
    emblem='<path d="M440 800 h120 l-20 90 h-80 Z" fill="#c0183a" stroke="#120909" stroke-width="7"/>',
    over='<path d="M380 390 l-60 -70 M620 390 l60 -70" stroke="#d8c8a0" stroke-width="22" stroke-linecap="round"/>'),
  F(shoulders=320, coat="#a8acb6", trim="#c0183a", cap="helm", cap_c="#3a3a42", head=150, skin="#3a6a8a",
    item=ot_item("sword", 1, "#ffb43a")), "#2a2a3a")
C("pc-nema",
  F(skin="#d89878", skin_dk="#a86848", coat="#5a3a1a", armor="#9a8a6a", hair="#c86a2a", hair_style="bun", beard="short",
    beard_c="#c86a2a", mouth="smile", brow="kind", nose="bulb", iris="#5a7a4a", item=i_scroll(), body_w=320, seed=75,
    emblem='<circle cx="500" cy="840" r="50" fill="url(#brass)" stroke="#120909" stroke-width="8"/>'),
  F(shoulders=300, coat="#9a8a6a", trim="#d8aa52", cap="hair", cap_c="#c86a2a", bun=True, head=145, beard=True, beard_c="#c86a2a",
    item=ot_item("clipboard", 1)), "#5a3a14")

# ---- The Redline Run and the Souljack Yard
C("kestrel-vane",
  F(**FIEND, coat="#1a1418", armor="#3a3a42", trim="#d8aa52", horns="big", ears="pointed", mouth="grin", nose="hook",
    brow="angry", hat="tophat", item=i_mace(), scar=True, seed=91,
    over='<path d="M330 820 q170 60 340 0" stroke="#8a8f99" stroke-width="22" fill="none" stroke-dasharray="26 10"/>'
         '<rect x="440" y="860" width="120" height="70" fill="url(#brass)" stroke="#120909" stroke-width="8"/>'),
  F(shoulders=300, coat="#3a3a42", trim="#d8aa52", cap="tophat", head=150, horns=True, ears="pointed", skin="#a8303a",
    skin_dk="#6a1018", hand="#a8303a", item=ot_item("baton", 1)), "#2a1418")
C("ash-road-reaver",
  F(**FIEND, coat="#3a2418", armor="#5a4a3a", trim="#ff7a1a", horns="small", ears="pointed", mouth="fangs", nose="hook",
    brow="angry", hat="helm", hat_c="#4a4a52", item=i_dagger(), seed=92,
    over='<rect x="370" y="380" width="260" height="70" rx="30" fill="#2a1a12" stroke="#120909" stroke-width="10"/>'
         '<circle cx="440" cy="415" r="26" fill="#ff9a3a" stroke="#120909" stroke-width="6"/>'
         '<circle cx="560" cy="415" r="26" fill="#ff9a3a" stroke="#120909" stroke-width="6"/>'),
  F(shoulders=280, coat="#3a2418", trim="#ff7a1a", cap="helm", cap_c="#4a4a52", head=140, horns=True, skin="#a8303a",
    skin_dk="#6a1018", hand="#a8303a", item=ot_item("dagger", 1)), "#3a1a0a")
C("broker-grisk",
  F(**FIEND, coat="#4a1a2a", trim="#d8aa52", horns="small", ears="pointed", mouth="grin", nose="bulb", brow="worried",
    beard="full", beard_c="#2a1418", mouth_in_beard=True, hat="tophat", item=i_sack(), body_w=360, seed=93,
    emblem='<circle cx="500" cy="840" r="46" fill="#c9c4b8" stroke="#120909" stroke-width="8"/>'
           '<circle cx="500" cy="840" r="22" fill="#5ad0e0" opacity="0.8"/>'),
  F(shoulders=320, coat="#4a1a2a", trim="#d8aa52", cap="tophat", head=150, horns=True, beard=True, beard_c="#2a1418",
    skin="#a8303a", skin_dk="#6a1018", hand="#a8303a", item=ot_item("sack", 1)), "#3a0a1a")


# ---- The Soulforged artificer's servitors
C("soulforged-enforcer",
  F(kind="brass", coat="#3a3a42", trim="#c09040", ears="none", nose="none", mouth="fixed", eye_glow="#5ad0e0", iris="#5ad0e0",
    brow="none", gloves="url(#iron)", body_w=400, head=1.05, hat="helm", hat_c="url(#iron)", seed=95,
    over='<rect x="420" y="790" width="160" height="110" rx="12" fill="#1a2a2e" stroke="#120909" stroke-width="10"/>'
         '<rect x="440" y="805" width="120" height="80" rx="8" fill="#5ad0e0"/>'
         + "".join(f'<line x1="{455 + k * 30}" y1="805" x2="{455 + k * 30}" y2="885" stroke="#120909" stroke-width="7"/>' for k in range(4))
         + '<ellipse cx="500" cy="845" rx="120" ry="80" fill="#5ad0e0" filter="url(#glw)" opacity="0.4"/>'),
  F(shoulders=380, coat="#3a3a42", trim="#c09040", cap="helm", cap_c="url(#iron)", head=165, hand="#4a4650", face=False,
    over='<rect x="460" y="520" width="80" height="80" rx="10" fill="#5ad0e0"/>'), "#1a2a3a")
C("soulforged-attendant",
  F(kind="brass", coat="#4a3a2a", trim="#5ad0e0", ears="none", nose="none", mouth="fixed", eye_glow="#ffd27a", iris="#ffd27a",
    brow="none", gloves="url(#brass)", body_w=320, head=1.15, hat="tophat", hat_c="#2a2a30", item=i_tinker(), seed=96,
    over='<circle cx="430" cy="840" r="34" fill="#5ad0e0" stroke="#120909" stroke-width="8"/>'),
  F(shoulders=300, coat="#4a3a2a", trim="#5ad0e0", cap="tophat", head=150, hand="url(#brass)", face=False,
    item=ot_item("clipboard", 1)), "#2a2a1a")


def special_token(kind):
    if kind.startswith("reindeer"):
        _, body, eye = kind.split(":")
        return (f'<ellipse cx="500" cy="540" rx="300" ry="420" fill="#000" opacity="0.35" filter="url(#glw)"/>'
                f'<ellipse cx="500" cy="560" rx="230" ry="360" fill="{body}" {S(14)}/>'
                f'<ellipse cx="500" cy="560" rx="120" ry="260" fill="url(#hatch)" opacity="0.3"/>'
                + "".join(f'<path d="M{500+s*70} 250 C{500+s*170} 160 {500+s*230} 120 {500+s*330} 50 M{500+s*190} 150 l{s*-10} -110 M{500+s*260} 100 l{s*80} -10" fill="none" stroke="#120909" stroke-width="34" stroke-linecap="round"/><path d="M{500+s*70} 250 C{500+s*170} 160 {500+s*230} 120 {500+s*330} 50 M{500+s*190} 150 l{s*-10} -110 M{500+s*260} 100 l{s*80} -10" fill="none" stroke="#3a2614" stroke-width="18" stroke-linecap="round"/><ellipse cx="{500+s*330}" cy="40" rx="30" ry="40" fill="#ff7a1a" filter="url(#glw)"/>' for s in (-1, 1))
                + f'<ellipse cx="500" cy="290" rx="110" ry="150" fill="{body}" {S(12)}/>'
                + f'<ellipse cx="500" cy="420" rx="60" ry="46" fill="#c0283a" {S(8)}/>'
                + "".join(f'<circle cx="{500+s*60}" cy="300" r="22" fill="{eye}" {S(5)}/>' for s in (-1, 1))
                + f'<path d="M290 540 Q500 620 710 540" stroke="#120909" stroke-width="30" fill="none"/><path d="M290 540 Q500 620 710 540" stroke="#8e1424" stroke-width="18" fill="none"/>')
    if kind == "snowman":
        return (f'<circle cx="500" cy="520" r="380" fill="#000" opacity="0.3" filter="url(#glw)"/><circle cx="500" cy="500" r="330" fill="#eef3f8" {S(14)}/>'
                f'<circle cx="500" cy="500" r="230" fill="#f6f9fc" {S(10)}/><circle cx="500" cy="500" r="190" fill="none" stroke="#c0283a" stroke-width="40"/>'
                f'<circle cx="500" cy="490" r="140" fill="#1a1418" {S(10)}/><circle cx="500" cy="490" r="90" fill="#26222a" {S(6)}/>'
                f'<path d="M500 640 L500 760" stroke="#120909" stroke-width="40" stroke-linecap="round"/><path d="M500 640 L500 760" stroke="#e8701a" stroke-width="24" stroke-linecap="round"/>'
                f'<path d="M180 500 l-140 -40 M820 500 l140 -40" stroke="#3a2614" stroke-width="20" stroke-linecap="round"/>')
    if kind.startswith("writ"):
        n = kind.split(":")[1]
        return writ(n, "#ffd27a")
    if kind == "ledger":
        return ledger_p()
    if kind == "engine":
        return f'<g transform="translate(500,500) scale(1.55)">{pr.clock_face(300, (11, 59))}</g>'
    if kind == "lock":
        return lock_p()
    if kind == "seam":
        return seam_p()
    if kind == "drone":
        return (f'<ellipse cx="500" cy="520" rx="420" ry="400" fill="#000" opacity="0.3" filter="url(#glw)"/>'
                f'<g transform="translate(500,500) scale(2.6)">{pr.sleigh(200, 130)}</g>'
                + "".join(f'<g transform="translate({x},{y})"><circle r="120" fill="url(#brass)" {S(10)}/><circle r="40" fill="url(#iron)" {S(7)}/></g>' for x, y in ((170, 200), (830, 200), (170, 800), (830, 800)))
                + f'<circle cx="500" cy="500" r="80" fill="#ffd27a" {S(9)}/><circle cx="500" cy="500" r="120" fill="#ffd27a" filter="url(#glw2)" opacity="0.6"/>')
    if kind == "arbiter":
        return token_overhead(F(shoulders=340, coat="#3a2614", trim="#b8862e", cap="helm", cap_c="url(#brass)", head=170,
                                hand="#d8aa52", face=False,
                                over=f'<g transform="translate(500,760) scale(1.6)">{pr.scales()}</g>'))
    raise KeyError(kind)


def build(keys=None):
    os.makedirs(f"{OUT}/portraits", exist_ok=True)
    os.makedirs(f"{OUT}/tokens", exist_ok=True)
    for key, (por, tk, bgc) in CAST.items():
        if keys and key not in keys:
            continue
        inner = humanoid(por) if isinstance(por, dict) else por
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">{DEFS}'
               f'{bg(bgc, hash(key) & 255)}<g>{inner}</g>{frame()}</svg>')
        render(svg, f"{OUT}/portraits/{key}.webp", 768)
        tinner = token_overhead(tk) if isinstance(tk, dict) else special_token(tk)
        tsvg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">{DEFS}{tinner}</svg>'
        render(tsvg, f"{OUT}/tokens/{key}.webp", 400)


if __name__ == "__main__":
    build(sys.argv[1:] or None)
    print(len(CAST), "subjects")
