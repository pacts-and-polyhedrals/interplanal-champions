"""Six level-12 pregenerated claimants for Interplanal Champions (Book II, Section 8).

Every class, race and SRD class feature is an embedded copy of the dnd5e 5.3.3 SRD compendium document, found by following
the class's own ItemGrant advancements up to level 12. Module subclasses, features, spells and relics come from this module's
own compendia. Where Book II names a non-SRD spell, an SRD spell of the same level is substituted and noted.
"""
import copy
from lib5e import *
import srd
import spells as S
import playeroptions as PO
import items as IT

LEVEL = 12
SAVES = {"Cleric": ("wis", "cha"), "Wizard": ("int", "wis"), "Paladin": ("wis", "cha"), "Warlock": ("wis", "cha"),
         "Barbarian": ("str", "con"), "Druid": ("int", "wis")}
ARMOR = {"Cleric": ["lgt", "med", "shl"], "Wizard": [], "Paladin": ["lgt", "med", "hvy", "shl"], "Warlock": ["lgt"],
         "Barbarian": ["lgt", "med", "shl"], "Druid": ["lgt", "med", "shl"]}
WEAPONS = {"Cleric": ["sim"], "Wizard": ["dagger", "dart", "sling", "quarterstaff", "lightcrossbow"],
           "Paladin": ["sim", "mar"], "Warlock": ["sim"], "Barbarian": ["sim", "mar"],
           "Druid": ["club", "dagger", "dart", "javelin", "mace", "quarterstaff", "scimitar", "sickle", "sling", "spear"]}
HIT_DIE = {"Cleric": 8, "Wizard": 6, "Paladin": 10, "Warlock": 8, "Barbarian": 12, "Druid": 8}
SUBS = {"The Ruby Court": PO.IC.RUBY, "Path of the Blood-Price": PO.IC.BLOOD, "Circle of Ashen Covenants": PO.IC.ASHEN,
        "School of Infernal Contracts": PO.SCHOOL if hasattr(PO, "SCHOOL") else None,
        "Oath of the Infernal Lord": PO.OATH, "Contract Domain": PO.DOMAIN}
FEATS = {f["_id"]: f for f in PO.FEATURES}
POT = ("Potion of Greater Healing", False, False, 2)

PREGENS = [
    dict(key="aurelia", name="Aurelia Quill", cls="Warlock", sub="The Ruby Court", race="Tiefling",
         title="Advocate of the Ruby Court", abilities=(8, 14, 16, 14, 10, 20),
         skills={"dec": 1, "inv": 1, "ins": 1, "per": 1, "arc": 1}, langs=["common", "infernal"], lang_custom="one regional language",
         align="Lawful Neutral", color="#c0183a", bg_text="Former Foundation compliance attorney",
         cantrips=["Eldritch Blast", "Mage Hand", "Minor Illusion", ("witness-mark",)],
         always=[], prepared=["Hellish Rebuke", "Protection from Evil and Good", "Comprehend Languages", "Hold Person",
                              "Misty Step", "Counterspell", "Sending", "Dimension Door", "Banishment", "Hold Monster",
                              ("audit-the-false",)],
         known=["Detect Magic", "Identify"], arcanum=["Mass Suggestion"], method="pact",
         choices={"inv": ["Agonizing Blast", "Repelling Blast", "Devil's Sight", "Book of Ancient Secrets", "Mask of Many Faces",
                          "Mire the Mind"], "boon": ["Pact of the Tome"]},
         gear=[("Studded Leather Armor +1", True, False), ("Dagger", True, False), ("@marshals-chain", True, True),
               ("@quill-true-notice", False, False), POT, ("Book", False, False), ("Ink Bottle", False, False),
               ("Ink Pen", False, False), ("Sealing Wax", False, False), ("Parchment", False, False, 10), ("Backpack", False, False)],
         subst="<em>Hex</em> and <em>armor of Agathys</em> (Book II) are not in the SRD; the sheet uses <em>hellish rebuke</em> and "
               "<em>protection from evil and good</em> in their place."),
    dict(key="varka", name="Varka Blackseal", cls="Barbarian", sub="Path of the Blood-Price", race="Half-Orc",
         title="The Blood-Price Marshal", abilities=(20, 14, 18, 8, 12, 10), skills={"ath": 1, "itm": 1, "prc": 1, "sur": 1},
         langs=["common", "orc"], align="Chaotic Good", color="#8e1424", bg_text="Displaced battlefield rescuer",
         cantrips=[], always=[], prepared=[], known=[],
         gear=[("Greataxe +1", True, False), ("Handaxe", False, False, 2), ("@crownmark-gauntlets", True, True), POT,
               ("Hempen Rope (50 ft.)", False, False), ("Backpack", False, False), ("Bedroll", False, False), ("Rations", False, False, 5)]),
    dict(key="ilyra", name="Ilyra Ashroot", cls="Druid", sub="Circle of Ashen Covenants", race="High Elf",
         title="Keeper of Unburnt Names", abilities=(8, 14, 16, 12, 20, 10), skills={"ins": 1, "nat": 1, "med": 1, "prc": 1, "sur": 1},
         langs=["common", "elvish", "sylvan", "druidic"], align="Neutral Good", color="#5a8a3a", bg_text="Planar refugee-warden",
         speed_bonus=5,
         cantrips=["Guidance", "Produce Flame", "Shillelagh", "Druidcraft"],
         always=[], prepared=["Healing Word", "Entangle", "Faerie Fire", "Detect Magic", "Lesser Restoration", "Pass without Trace",
                              "Spike Growth", "Dispel Magic", "Plant Growth", "Call Lightning", "Conjure Woodland Beings",
                              "Freedom of Movement", "Wall of Fire", "Polymorph", "Greater Restoration", "Wall of Stone", "Heal"],
         known=[("writ-of-safe-passage",), ("breach-of-dominion",)],
         gear=[("Hide Armor", True, False), ("Shield +1", True, False), ("@ashen-seed", True, True), ("Sickle", True, False),
               ("Sprig of Mistletoe", True, False), ("Healer's Kit", False, False), POT, ("Backpack", False, False)],
         subst="Ilyra is a wood elf. The SRD has only the high elf, so the sheet uses it, with +5 ft. walking speed for Fleet of Foot; "
               "use Mask of the Wild in place of the high elf cantrip at your table. <em>Thorn whip</em> is replaced by "
               "<em>shillelagh</em>; her <em>+1 wooden shield</em> is a <em>shield +1</em>."),
    dict(key="orren", name="Orren Fenwick", cls="Wizard", sub="School of Infernal Contracts", race="Human",
         title="The Scriptorium Defector", abilities=(8, 14, 14, 20, 12, 10), skills={"arc": 1, "his": 1, "inv": 1, "rel": 1},
         langs=["common", "infernal", "draconic", "abyssal"], align="Neutral", color="#2c4f8a", bg_text="Former infernal archivist",
         cantrips=["Fire Bolt", "Mage Hand", "Prestidigitation", "Minor Illusion", ("ember-receipt",)],
         always=[], prepared=["Mage Armor", "Shield", "Detect Magic", "Find Familiar", "Misty Step", "Mirror Image", "Counterspell",
                              "Dispel Magic", "Fireball", "Fly", "Dimension Door", "Greater Invisibility", "Wall of Force",
                              ("audit-the-false",), "Globe of Invulnerability", "Chain Lightning", "Contingency"],
         known=["Identify", "Comprehend Languages", ("registry-of-names",), ("writ-of-safe-passage",)],
         gear=[("@gavel-of-appeal", True, True), ("Cloak of Protection", True, True), ("Spellbook", True, False),
               ("Component Pouch", True, False), ("Dagger", False, False), ("Ink Bottle", False, False, 3), ("Ink Pen", False, False),
               POT, ("Backpack", False, False)]),
    dict(key="caldris", name="Dame Caldris Vowborne", cls="Paladin", sub="Oath of the Infernal Lord", race="Dragonborn",
         title="The Infernal Paladin", abilities=(20, 10, 16, 8, 10, 18), skills={"ath": 1, "itm": 1, "ins": 1, "per": 1},
         langs=["common", "draconic", "infernal"], align="Lawful Neutral", color="#3a6a8a", bg_text="Veteran oathkeeper",
         extra_race=["Breath Weapon - Red"],
         cantrips=[], always=[], prepared=["Bless", "Command", "Cure Wounds", "Protection from Evil and Good", "Aid",
                                           "Lesser Restoration", "Find Steed", "Revivify", "Dispel Magic", ("writ-of-safe-passage",)],
         known=[], choices={"style": ["Defense"]},
         gear=[("Longsword +1", True, False), ("Shield +1", True, False), ("Plate Armor", True, False), ("@receipt-last-gift", False, False),
               POT, ("Backpack", False, False), ("Bedroll", False, False), ("Parchment", False, False)]),
    dict(key="nema", name="Sister Nema Copperwrit", cls="Cleric", sub="Contract Domain", race="Hill Dwarf",
         title="The Contract Domain Priest", abilities=(10, 12, 16, 12, 20, 10), skills={"ins": 1, "med": 1, "rel": 1, "per": 1},
         langs=["common", "dwarvish", "infernal", "celestial"], align="Lawful Good", color="#b8862e", bg="Acolyte",
         bg_text="Temple notary and advocate",
         cantrips=["Guidance", "Sacred Flame", "Thaumaturgy", "Spare the Dying", ("witness-mark",)],
         always=[], prepared=["Bless", "Healing Word", "Guiding Bolt", "Command", "Aid", "Lesser Restoration", "Spiritual Weapon",
                              "Zone of Truth", "Dispel Magic", "Revivify", "Spirit Guardians", "Death Ward", "Freedom of Movement",
                              "Banishment", "Greater Restoration", "Flame Strike", "Heal"],
         known=[],
         gear=[("Scale Mail", True, False), ("Shield +1", True, False), ("@marshals-chain", True, True), ("Amulet", True, False),
               ("Healer's Kit", False, False), POT, ("Sealing Wax", False, False, 3), ("Backpack", False, False)]),
]


def spell_doc(entry, *, prepared, ability, method="spell"):
    if isinstance(entry, tuple):
        key = entry[0]
        s = copy.deepcopy(next(x for x in S.SPELLS if x["_id"] == fid("spell:" + key)))
        s.pop("_key", None)
        s["system"]["prepared"] = prepared if s["system"]["level"] > 0 else 0
        s["system"]["method"] = method
        s["system"]["ability"] = ""
        s["_stats"] = dict(STATS, compendiumSource=f"Compendium.{MOD}.spells.Item.{s['_id']}")
        return s
    d = srd.get("spells", entry)
    return srd.embed(d, prepared=(prepared if d["system"]["level"] > 0 else 0), method=method)


def _module_item(key):
    d = copy.deepcopy(next(i for v in IT.ITEMS.values() for i in v if i["_id"] == fid("item:" + key)))
    d.pop("_key", None)
    d["_stats"] = dict(STATS, compendiumSource=f"Compendium.{MOD}.items.Item.{d['_id']}")
    return d


def _mod_copy(doc, pack):
    d = copy.deepcopy(doc)
    d.pop("_key", None)
    d["_stats"] = dict(STATS, compendiumSource=f"Compendium.{MOD}.{pack}.Item.{doc['_id']}")
    return d


def build(p):
    from pregen_lore import SHEET
    SH = SHEET[p["key"]]
    cls = srd.get("classes", p["cls"])
    items = []
    added = set()

    def add(doc):
        if doc["_id"] in added:
            return
        added.add(doc["_id"])
        items.append(doc)

    c = srd.embed(cls, levels=LEVEL)
    for adv in c["system"]["advancement"]:
        if adv["type"] == "HitPoints":
            adv["value"] = {"1": "max", **{str(i): "avg" for i in range(2, LEVEL + 1)}}
    add(c)
    # module subclass + its features and always-prepared subclass spells, by advancement
    sub = SUBS[p["sub"]]
    add(_mod_copy(sub, "options"))
    ability = {"Cleric": "wis", "Wizard": "int", "Paladin": "cha", "Warlock": "cha", "Druid": "wis"}.get(p["cls"], "")
    for adv in sub["system"]["advancement"]:
        if adv["type"] != "ItemGrant" or adv["level"] > LEVEL:
            continue
        for it in adv["configuration"]["items"]:
            u = it["uuid"]
            if ".options." in u:
                add(_mod_copy(FEATS[u.split(".")[-1]], "options"))
            elif ".spells." in u and MOD in u:
                sd = copy.deepcopy(next(x for x in S.SPELLS if x["_id"] == u.split(".")[-1]))
                sd.pop("_key", None)
                sd["system"]["prepared"] = 2
                sd["system"]["method"] = "spell"
                sd["_stats"] = dict(STATS, compendiumSource=f"Compendium.{MOD}.spells.Item.{sd['_id']}")
                add(sd)
            else:
                d = srd.by_uuid(u)
                add(srd.embed(d, prepared=2, method="spell"))
    for adv, u in srd.grants_upto(cls, LEVEL):
        d = srd.by_uuid(u)
        if d["__pack"] == "spells":
            continue
        add(srd.embed(d))
    ch = p.get("choices", {})
    for name in ch.get("inv", []) + ch.get("boon", []) + ch.get("style", []):
        add(srd.embed(srd.get("classfeatures", name)))
    race = srd.get("races", p["race"])
    add(srd.embed(race))
    for adv, u in srd.grants_upto(race, LEVEL):
        d = srd.by_uuid(u)
        add(srd.embed(d, method="innate", prepared=0) if d["__pack"] == "spells" else srd.embed(d))
    for r in p.get("extra_race", []):
        add(srd.embed(srd.get("races", r)))
    if p.get("bg"):
        add(srd.embed(srd.get("backgrounds", p["bg"])))
    meth = p.get("method", "spell")
    for e in p["cantrips"]:
        add(spell_doc(e, prepared=0, ability=ability, method=meth))
    for e in p["always"]:
        add(spell_doc(e, prepared=2, ability=ability, method=meth))
    for e in p["prepared"]:
        add(spell_doc(e, prepared=1, ability=ability, method=meth))
    for e in p["known"]:
        add(spell_doc(e, prepared=0, ability=ability, method=meth))
    for e in p.get("arcanum", []):
        sd = spell_doc(e, prepared=1, ability=ability, method="innate")
        sd["system"]["uses"] = {"max": "1", "spent": 0, "recovery": [{"period": "lr", "type": "recoverAll", "formula": ""}]}
        add(sd)
    for g in p["gear"]:
        name, equipped, attuned = g[:3]
        if name.startswith("@"):
            e = _module_item(name[1:])
            e["system"]["equipped"] = equipped
            if attuned:
                e["system"]["attuned"] = True
        else:
            upd = {"equipped": equipped}
            if attuned:
                upd["attuned"] = True
            if len(g) > 3:
                upd["quantity"] = g[3]
            e = srd.embed(srd.get("items", name), **upd)
        while e["_id"] in added:
            e["_id"] = fid("gear:" + e["_id"])
        add(e)

    ab = {}
    for k, v in zip(("str", "dex", "con", "int", "wis", "cha"), p["abilities"]):
        ab[k] = {"value": v, "proficient": 1 if k in SAVES[p["cls"]] else 0}
    skills = {k: {"value": v, "ability": SKILL_ABIL[k]} for k, v in p["skills"].items()}
    con = (p["abilities"][2] - 10) // 2
    die = HIT_DIE[p["cls"]]
    dwarf = p["race"] == "Hill Dwarf"
    hp = die + (LEVEL - 1) * (die // 2 + 1) + LEVEL * con + (LEVEL if dwarf else 0)
    bio = "".join(f"<p>{b}</p>" for b in p["bio"])
    dr = {"Tiefling": ["fire"], "Dragonborn": ["fire"], "Hill Dwarf": ["poison"]}.get(p["race"], [])
    traits = {"size": "med",
              "languages": {"value": [l for l in p["langs"]], "custom": p.get("lang_custom", "")},
              "armorProf": {"value": ARMOR[p["cls"]], "custom": ""}, "weaponProf": {"value": WEAPONS[p["cls"]], "custom": ""},
              "dr": {"value": dr, "bypasses": [], "custom": ""}, "di": {"value": [], "bypasses": [], "custom": ""},
              "dv": {"value": [], "bypasses": [], "custom": ""}, "ci": {"value": [], "custom": ""}}
    tools = {}
    if p["cls"] == "Druid":
        tools["herb"] = {"value": 1, "ability": "int"}
    if p["cls"] == "Wizard":
        tools["calligrapher"] = {"value": 1, "ability": "dex"}
    effects = []
    if p.get("speed_bonus"):
        effects.append(effect("pc-" + p["key"] + "-fleet", "Fleet of Foot (Wood Elf)", icon("ic-ashen"), transfer=False,
                              changes=[("system.attributes.movement.walk", 2, str(p["speed_bonus"]))],
                              description="<p>Wood elf: base walking speed 35 feet.</p>"))
    aid = fid("actor:pregen-" + p["key"])
    actor = {
        "_id": aid, "name": p["name"], "type": "character", "img": portrait("pc-" + p["key"]), "sort": 0, "folder": None,
        "system": {
            "abilities": ab, "skills": skills, "tools": tools,
            "attributes": {"hp": {"value": hp, "max": None, "temp": None, "tempmax": None,
                                  "bonuses": {"level": "1" if dwarf else "", "overall": ""}},
                           "ac": {"calc": "unarmoredBarb" if p["cls"] == "Barbarian" else "default"},
                           "spellcasting": ability, "inspiration": True},
            "details": {"biography": {"value": bio, "public": bio}, "alignment": p["align"], "xp": {"value": 100000},
                        "trait": " ".join(SH["traits"]), "ideal": SH["ideal"], "bond": SH["bond"], "flaw": SH["flaw"],
                        "appearance": SH["appearance"], "originalClass": c["_id"], "age": SH["age"], "height": SH["height"],
                        "weight": SH["weight"], "eyes": SH["eyes"], "hair": SH["hair"], "skin": SH["skin"],
                        "gender": SH["gender"], "faith": SH["faith"]},
            "traits": traits, "currency": {"gp": 400, "sp": 20, "cp": 0, "pp": 10, "ep": 0}},
        "prototypeToken": proto_token(p["name"], tok("pc-" + p["key"]), 1, disposition=1, sight=True, actor_link=True),
        "items": items, "effects": effects,
        "flags": {MOD: {"pregen": True, "title": p["title"], "color": p["color"], "expectedHp": hp}}, "_stats": STATS}
    for ef in actor["effects"]:
        ef["transfer"] = False
    actor["prototypeToken"]["sight"]["range"] = 0
    actor["prototypeToken"]["displayBars"] = 30
    actor["prototypeToken"]["displayName"] = 30
    seen = set()
    for it in actor["items"]:
        while it["_id"] in seen:
            it["_id"] = fid("dup:" + aid + it["_id"])
        seen.add(it["_id"])
    return actor


from pregen_lore import bio_paragraphs
for _p in PREGENS:
    _p["bio"] = bio_paragraphs(_p["key"])
ACTORS = [build(p) for p in PREGENS]
