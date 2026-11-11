"""Shared spell / item / subclass presentation used by both the Foundry journals and the PDF."""
SCHOOL = {"abj": "abjuration", "con": "conjuration", "div": "divination", "enc": "enchantment", "evo": "evocation",
          "ill": "illusion", "nec": "necromancy", "trs": "transmutation"}
ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th", 8: "8th", 9: "9th"}
SCRIPTORIUM_ITEMS = ("Golgorath's Quill", "Length of Clause Chain", "Infernal Signet of the Red Clause", "Gavel of the Brass Arbiter")


def spell_type(s):
    y = s["system"]
    lvl = f"{SCHOOL[y['school']]} cantrip".capitalize() if y["level"] == 0 else f"{ORD[y['level']]}-level {SCHOOL[y['school']]}"
    if "ritual" in y["properties"]:
        lvl += " (ritual)"
    return lvl


def spell_lines(s):
    y = s["system"]
    act = y["activation"]
    v = act.get("value") or 1
    ct = {"action": "1 action", "bonus": "1 bonus action", "reaction": "1 reaction", "minute": f"{v} minute{'s' if v != 1 else ''}",
          "hour": f"{v} hour{'s' if v != 1 else ''}"}[act["type"]]
    if act["type"] == "reaction" and act.get("condition"):
        ct += f", which you take {act['condition']}"
    r = y["range"]
    rng = {"self": "Self", "touch": "Touch"}.get(r["units"], f"{r['value']} {'miles' if r['units'] == 'mi' else 'feet'}")
    if r["units"] == "self" and r.get("special"):
        rng += f" ({r['special']})"
    comps = ", ".join({"vocal": "V", "somatic": "S", "material": "M"}[c] for c in y["properties"] if c in ("vocal", "somatic", "material"))
    if y["materials"]["value"]:
        comps += f" ({y['materials']['value']})"
    d = y["duration"]
    dur = {"inst": "Instantaneous", "perm": "Until fulfilled or broken", "disp": "Until dispelled or triggered"}.get(
        d["units"], f"{d['value']} {d['units']}{'s' if str(d['value']) not in ('1', '') else ''}")
    ct = ((s.get("flags") or {}).get("interplanal-champions") or {}).get("castingTime") or ct
    if "concentration" in y["properties"]:
        dur = "Concentration, up to " + dur
    return [("Casting Time", ct), ("Range", rng), ("Components", comps), ("Duration", dur)]


def item_type(i):
    y = i["system"]
    kind = {"consumable": "Wondrous item (consumable)", "equipment": "Wondrous item", "loot": "Document / curio",
            "container": "Wondrous item", "weapon": "Weapon (whip)"}[i["type"]]
    rar = y.get("rarity", "")
    att = ""
    if y.get("attunement"):
        att = " (requires attunement)"
    return f"{kind}{', ' + rar if rar else ''}{att}"


def is_scriptorium_spell(s, MOD):
    return s["flags"][MOD]["group"] == "Asmodeun Scriptorium"
