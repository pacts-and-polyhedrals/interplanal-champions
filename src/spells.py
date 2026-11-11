"""Spells: the Asmodeun Scriptorium's contract magic (carried over) plus the 17 contractual spells of Interplanal Champions.

Rules pass against the 2014 PHB conventions; every change is recorded in SPELL_NOTES.
"""
from lib5e import *

SPELL_NOTES = []


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def dur(value, units, conc=False):
    return {"value": str(value) if value != "" else "", "units": units}


def ACTD(value, units, conc=False):
    return {"concentration": conc, "value": str(value), "units": units, "special": "", "override": False}


SCH_ICON = {"abj": "sp-abj", "con": "sp-con", "div": "sp-div", "enc": "sp-enc", "evo": "sp-evo", "ill": "sp-ill",
            "nec": "sp-nec", "trs": "sp-trs"}

LISTS = {}  # spell key -> class list text


def add(key, *, classes, notes=None, **kw):
    LISTS[key] = classes
    if notes:
        SPELL_NOTES.append(f"<strong>{kw['name']}:</strong> {notes}")
    name = kw.pop("name")
    desc = kw.pop("desc")
    desc += f"<p class='rc-spell-classes'><strong>Spell Lists.</strong> {classes}</p>"
    return spell(key, name, desc, img=icon(kw.pop("img")), **kw)


INFERNAL = "Cleric, Paladin, Wizard, Warlock (The Fiend)"
SPELLS = []

# ---------------------------------------------------------------------------
# THE ASMODEUN SCRIPTORIUM (expanded edition: 26 spells, generated from the manuscript)
# ---------------------------------------------------------------------------
import scriptorium_v2 as _V
_scr, _lists = _V.build_spells()
SPELLS.extend(_scr)
LISTS.update(_lists)
SPELL_NOTES += [
    "<strong>Asmodeun Scriptorium spells</strong> follow the expanded manuscript and its rules audit: <em>devil's due</em> no "
    "longer ignores resistance; <em>binding clause</em>'s geas deals 4d10 and can be ended by <em>dispel magic</em> (5th) or "
    "<em>greater restoration</em>; <em>soul covenant</em> grants advantage instead of a flat +5; <em>contract of the soulforged "
    "blade</em> caps soul-fuelled spells at 3rd level (5th when upcast); <em>true name revelation</em> now allows a Charisma save; "
    "<em>contract of the infernal fury</em> is an evocation with a real Forbidden Term; <em>Seer's Vigil</em> is a proper "
    "3rd-level divination. <em>Infernal binding</em> is replaced by <em>contract of infernal servitude</em> (6th).",
    "The 17 <strong>Interplanal Champions</strong> spells follow Book II exactly. They extend the Scriptorium's ladder without "
    "duplicating it; none of them can forge consent, and a magical restraint is never a soul bargain.",
]

import spells_ic as _IC
SPELLS.extend(_IC.build(add))

for s in SPELLS:
    s["flags"].setdefault(MOD, {"group": "Interplanal Champions"})
