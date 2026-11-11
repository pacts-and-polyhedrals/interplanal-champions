"""Helpers that emit dnd5e 5.3.3 document data.

Only the fields that matter are written; Foundry's data models fill every other
field with its default when the document is loaded. Field names were checked
against the dnd5e release-5.3.3 source (module/data/**).
"""
import hashlib, re

MOD = "interplanal-champions"
ASSET = f"modules/{MOD}/assets"
ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def fid(key: str) -> str:
    """Deterministic 16-character Foundry id from a stable key."""
    h = hashlib.sha256(("ipc:" + key).encode()).digest()
    return "".join(ALNUM[b % 62] for b in h[:16])


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


STATS = {"systemId": "dnd5e", "systemVersion": "5.3.3", "coreVersion": "13.351",
         "createdTime": 1762400000000, "modifiedTime": 1762400000000, "lastModifiedBy": "interplanalbld0"}

SOURCE = {"book": "Interplanal Champions", "page": "", "custom": "", "license": "", "rules": "2014", "revision": 1}

# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------
_act_counter = {}


def _aid(item_key, n):
    return ("rcact" + fid(item_key + str(n)))[:16]


def activation(kind="action", value=1, cond=""):
    return {"type": kind, "value": value, "condition": cond, "override": False}


def consume_legact(cost=1):
    return {"targets": [{"type": "attribute", "target": "resources.legact.value", "value": str(cost),
                         "scaling": {"mode": "", "formula": ""}}], "scaling": {"allowed": False, "max": ""}, "spellSlot": True}


def consume_legres():
    return {"targets": [{"type": "attribute", "target": "resources.legres.value", "value": "1",
                         "scaling": {"mode": "", "formula": ""}}], "scaling": {"allowed": False, "max": ""}, "spellSlot": True}


def consume_item_uses(n=1):
    return {"targets": [{"type": "itemUses", "target": "", "value": str(n), "scaling": {"mode": "", "formula": ""}}],
            "scaling": {"allowed": False, "max": ""}, "spellSlot": True}


def dmg(number, die, bonus="", types=("bludgeoning",), scale_mode="", scale_number=None):
    part = {"number": number, "denomination": die, "bonus": str(bonus), "types": list(types),
            "custom": {"enabled": False, "formula": ""},
            "scaling": {"mode": scale_mode, "number": scale_number, "formula": ""}}
    return part


def dmg_formula(formula, types=("bludgeoning",)):
    return {"number": None, "denomination": None, "bonus": "", "types": list(types),
            "custom": {"enabled": True, "formula": formula}, "scaling": {"mode": "", "number": None, "formula": ""}}


def target(count="", ttype="", tmpl_type="", size="", width="", units="ft", special=""):
    return {"template": {"count": "", "contiguous": False, "type": tmpl_type, "size": str(size), "width": str(width),
                         "height": "", "units": units if tmpl_type else ""},
            "affects": {"count": str(count), "type": ttype, "choice": False, "special": special},
            "prompt": True, "override": False}


def rng(value="", units="ft", special=""):
    return {"value": str(value) if value != "" else "", "units": units, "special": special, "override": False}


def base_activity(kind, key, n, *, name="", act=None, consumption=None, duration=None, rng_=None, tgt=None,
                  effects=None, uses=None):
    _id = _aid(key, n)
    a = {"_id": _id, "type": kind, "name": name, "img": "", "sort": n * 100000,
         "activation": act or activation(),
         "consumption": consumption or {"targets": [], "scaling": {"allowed": False, "max": ""}, "spellSlot": True},
         "description": {"chatFlavor": ""},
         "duration": duration or {"concentration": False, "value": "", "units": "inst", "special": "", "override": False},
         "effects": [{"_id": e} for e in (effects or [])],
         "range": rng_ or {"override": False, "units": "", "special": ""},
         "target": tgt or target(),
         "uses": uses or {"spent": 0, "max": "", "recovery": []}}
    return a


def attack(key, n=0, *, to_hit=None, kind="melee", classification="weapon", parts=(), reach=5, range_=None,
           name="", act=None, consumption=None, effects=None, uses=None, ability="none"):
    a = base_activity("attack", key, n, name=name, act=act, consumption=consumption,
                      rng_=rng(range_ if range_ else reach, "ft"), tgt=target(1, "creature"), effects=effects, uses=uses)
    a["attack"] = {"ability": ability if to_hit is None else "none",
                   "bonus": "" if to_hit is None else str(to_hit),
                   "critical": {"threshold": None}, "flat": to_hit is not None,
                   "type": {"value": kind, "classification": classification}}
    a["damage"] = {"critical": {"bonus": ""}, "includeBase": False, "parts": list(parts)}
    return a


def save(key, n=0, *, ability="dex", dc=15, parts=(), on_save="half", name="", act=None, consumption=None,
         tgt=None, rng_=None, effects=None, uses=None, spell=False, duration=None):
    a = base_activity("save", key, n, name=name, act=act, consumption=consumption, rng_=rng_, tgt=tgt,
                      effects=effects, uses=uses, duration=duration)
    a["damage"] = {"onSave": on_save, "parts": list(parts)}
    a["save"] = {"ability": [ability] if isinstance(ability, str) else list(ability),
                 "dc": {"calculation": "spellcasting" if spell else "", "formula": "" if spell else str(dc)}}
    return a


def damage_act(key, n=0, *, parts=(), name="", act=None, consumption=None, tgt=None, rng_=None, uses=None, effects=None):
    a = base_activity("damage", key, n, name=name, act=act, consumption=consumption, rng_=rng_, tgt=tgt, uses=uses,
                      effects=effects)
    a["damage"] = {"critical": {"allow": False, "bonus": ""}, "parts": list(parts)}
    return a


def heal_act(key, n=0, *, formula_part=None, name="", act=None, consumption=None, tgt=None, rng_=None, uses=None,
             temp=False):
    a = base_activity("heal", key, n, name=name, act=act, consumption=consumption, rng_=rng_, tgt=tgt, uses=uses)
    part = dict(formula_part)
    part["types"] = ["temphp" if temp else "healing"]
    a["healing"] = part
    return a


def utility(key, n=0, *, name="", act=None, consumption=None, roll=None, tgt=None, rng_=None, effects=None,
            uses=None, duration=None):
    a = base_activity("utility", key, n, name=name, act=act, consumption=consumption, tgt=tgt, rng_=rng_,
                      effects=effects, uses=uses, duration=duration)
    a["roll"] = {"formula": roll[0] if roll else "", "name": roll[1] if roll else "", "prompt": False, "visible": False}
    return a


def check_act(key, n=0, *, ability="", skills=(), dc=15, name="", act=None):
    a = base_activity("check", key, n, name=name, act=act)
    a["check"] = {"ability": ability, "associated": list(skills), "dc": {"calculation": "", "formula": str(dc)}}
    return a


def acts(*activities):
    return {a["_id"]: a for a in activities}


def uses(max_="", recovery=None, spent=0):
    rec = []
    for r in (recovery or []):
        if isinstance(r, str):
            rec.append({"period": r, "type": "recoverAll", "formula": ""})
        else:
            rec.append(r)
    return {"max": str(max_), "spent": spent, "recovery": rec}


def recharge(n):
    return {"period": "recharge", "formula": str(n), "type": "recoverAll"}


# ---------------------------------------------------------------------------
# Active effects
# ---------------------------------------------------------------------------

def effect(key, name, img, changes=(), statuses=(), duration=None, transfer=False, description="", disabled=False):
    return {"_id": fid("eff:" + key), "name": name, "img": img, "changes": [
        {"key": k, "mode": m, "value": str(v), "priority": None} for (k, m, v) in changes],
        "statuses": list(statuses), "duration": duration or {}, "transfer": transfer, "disabled": disabled,
        "description": description, "origin": None, "tint": "#ffffff", "flags": {}, "type": "base", "system": {}}


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------

def feat(key, name, desc, *, img, activities=None, uses_=None, ftype="monster", subtype="", effects=None,
         req="", props=(), identifier=None, flags=None, sort=0):
    return {"_id": fid("item:" + key), "name": name, "type": "feat", "img": img, "sort": sort,
            "system": {"description": {"value": desc, "chat": ""}, "source": SOURCE,
                       "uses": uses_ or uses(), "type": {"value": ftype, "subtype": subtype}, "requirements": req,
                       "properties": list(props), "activities": acts(*(activities or [])),
                       "identifier": identifier or slug(name), "enchant": {}, "prerequisites": {"level": None}},
            "effects": effects or [], "flags": flags or {}, "folder": None, "_stats": STATS}


def spell(key, name, desc, *, img, level, school, activities, comps=("vocal", "somatic"), materials="",
          mat_cost=0, mat_consumed=False, act=None, duration=None, rng_=None, tgt=None, ritual=False,
          concentration=False, effects=None, method="spell", prepared=0, classes="", sort=0):
    props = list(comps)
    if ritual:
        props.append("ritual")
    if concentration:
        props.append("concentration")
    return {"_id": fid("spell:" + key), "name": name, "type": "spell", "img": img, "sort": sort,
            "system": {"description": {"value": desc, "chat": ""}, "source": SOURCE,
                       "activation": act or activation(), "duration": duration or {"value": "", "units": "inst"},
                       "target": tgt or target(), "range": rng_ or rng(30), "uses": uses(), "level": level,
                       "school": school,
                       "materials": {"value": materials, "consumed": mat_consumed, "cost": mat_cost, "supply": 0},
                       "method": method, "prepared": prepared, "properties": props, "activities": acts(*activities),
                       "identifier": slug(name)},
            "effects": effects or [], "flags": {}, "folder": None, "_stats": STATS}


def item(key, name, itype, desc, *, img, rarity="", price=0, weight=0.0, attune="", activities=None, uses_=None,
         subtype="", effects=None, props=(), extra=None, quantity=1, identifier=None, sort=0, flags=None):
    sysd = {"description": {"value": desc, "chat": "", "unidentified": ""}, "source": SOURCE,
            "quantity": quantity, "weight": {"value": weight, "units": "lb"},
            "price": {"value": price, "denomination": "gp"}, "rarity": rarity, "attunement": attune,
            "identified": True, "properties": list(props), "uses": uses_ or uses(),
            "activities": acts(*(activities or [])), "identifier": identifier or slug(name)}
    if itype in ("consumable", "equipment", "weapon", "loot", "tool"):
        sysd["type"] = {"value": subtype, "subtype": ""}
    if extra:
        for k, v in extra.items():
            sysd[k] = v
    return {"_id": fid("item:" + key), "name": name, "type": itype, "img": img, "sort": sort, "system": sysd,
            "effects": effects or [], "flags": flags or {}, "folder": None, "_stats": STATS}


# ---------------------------------------------------------------------------
# Actors
# ---------------------------------------------------------------------------
SKILL_ABIL = {"acr": "dex", "ani": "wis", "arc": "int", "ath": "str", "dec": "cha", "his": "int", "ins": "wis",
              "itm": "cha", "inv": "int", "med": "wis", "nat": "int", "prc": "wis", "prf": "cha", "per": "cha",
              "rel": "int", "slt": "dex", "ste": "dex", "sur": "wis"}


def npc(key, name, *, img, token, size="med", ctype="fiend", subtype="", alignment="", cr=1, ac=10, ac_calc="natural",
        hp=10, hp_formula="", speed=30, fly=0, climb=0, hover=False, abilities=(10, 10, 10, 10, 10, 10),
        saves=(), skills=None, di=(), dr=(), dv=(), ci=(), dr_custom="", di_custom="", senses=None, langs=(),
        lang_custom="", bio="", items=(), legact=0, legres=0, lair=False, disposition=-1, tsize=None,
        spellcasting="", spell_level=0, folder=None, flags=None, sight=False, effects=None, gm_note=""):
    ab = {}
    for k, v in zip(("str", "dex", "con", "int", "wis", "cha"), abilities):
        ab[k] = {"value": v, "proficient": 1 if k in saves else 0}
    sk = {}
    for k, v in (skills or {}).items():
        sk[k] = {"value": v, "ability": SKILL_ABIL[k]}
    s = senses or {}
    aid = fid("actor:" + key)
    t = tsize or {"tiny": 0.5, "sm": 1, "med": 1, "lg": 2, "huge": 3, "grg": 4}[size]
    actor = {
        "_id": aid, "name": name, "type": "npc", "img": img, "sort": 0, "folder": folder,
        "system": {
            "abilities": ab,
            "attributes": {"ac": {"flat": ac, "calc": ac_calc}, "hp": {"value": hp, "max": hp, "formula": hp_formula},
                           "movement": {"walk": speed, "fly": fly, "climb": climb, "swim": 0, "burrow": 0,
                                        "units": "ft", "hover": hover},
                           "senses": {"darkvision": s.get("darkvision", 0), "blindsight": s.get("blindsight", 0),
                                      "tremorsense": 0, "truesight": s.get("truesight", 0), "units": "ft",
                                      "special": s.get("special", "")},
                           "spellcasting": spellcasting},
            "details": {"biography": {"value": bio, "public": ""}, "alignment": alignment,
                        "type": {"value": ctype, "subtype": subtype, "swarm": "", "custom": ""},
                        "cr": cr, "spellLevel": spell_level, "environment": ""},
            "traits": {"size": size,
                       "di": {"value": list(di), "bypasses": [], "custom": di_custom},
                       "dr": {"value": list(dr), "bypasses": [], "custom": dr_custom},
                       "dv": {"value": list(dv), "bypasses": [], "custom": ""},
                       "ci": {"value": list(ci), "custom": ""},
                       "languages": {"value": list(langs), "custom": lang_custom}},
            "skills": sk,
            "resources": {"legact": {"value": legact, "max": legact}, "legres": {"value": legres, "max": legres},
                          "lair": {"value": lair, "initiative": 20 if lair else None}},
            "source": SOURCE},
        "prototypeToken": proto_token(name, token, t, disposition, sight=sight),
        "items": list(items), "effects": effects or [], "flags": flags or {}, "_stats": STATS}
    if gm_note:
        actor["flags"].setdefault(MOD, {})["gmNote"] = gm_note
    return actor


def proto_token(name, src, size, disposition=-1, sight=False, vision_range=60, light=None, actor_link=False):
    return {"name": name, "displayName": 20, "actorLink": actor_link, "width": size, "height": size,
            "disposition": disposition, "displayBars": 20, "bar1": {"attribute": "attributes.hp"},
            "bar2": {"attribute": None}, "lockRotation": True, "rotation": 0,
            "texture": {"src": src, "scaleX": 1, "scaleY": 1, "fit": "contain", "anchorX": 0.5, "anchorY": 0.5,
                        "tint": "#ffffff", "alphaThreshold": 0.75},
            "sight": {"enabled": sight, "range": vision_range, "angle": 360, "visionMode": "basic", "brightness": 0,
                      "saturation": 0, "contrast": 0, "attenuation": 0.1, "color": None},
            "light": light or {"bright": 0, "dim": 0, "alpha": 0.5, "angle": 360, "color": None,
                               "animation": {"type": None, "speed": 5, "intensity": 5, "reverse": False}},
            "ring": {"enabled": False}, "appendNumber": not actor_link, "prependAdjective": False,
            "randomImg": False, "alpha": 1, "flags": {}}


def key_items(actor):
    """Give every embedded document a _key so the Foundry CLI can compile it."""
    aid = actor["_id"]
    actor["_key"] = f"!actors!{aid}"
    for it in actor["items"]:
        it["_key"] = f"!actors.items!{aid}.{it['_id']}"
        for ef in it.get("effects", []):
            ef["_key"] = f"!actors.items.effects!{aid}.{it['_id']}.{ef['_id']}"
    for ef in actor.get("effects", []):
        ef["_key"] = f"!actors.effects!{aid}.{ef['_id']}"
    return actor


def key_item(doc):
    iid = doc["_id"]
    doc["_key"] = f"!items!{iid}"
    for ef in doc.get("effects", []):
        ef["_key"] = f"!items.effects!{iid}.{ef['_id']}"
    return doc


def uuid_item(key, name=None):
    i = fid("item:" + key)
    return f"@UUID[Compendium.{MOD}.items.Item.{i}]" + (f"{{{name}}}" if name else "")


def uuid_spell(key, name=None):
    i = fid("spell:" + key)
    return f"@UUID[Compendium.{MOD}.spells.Item.{i}]" + (f"{{{name}}}" if name else "")


def uuid_actor(key, name=None):
    i = fid("actor:" + key)
    return f"@UUID[Compendium.{MOD}.actors.Actor.{i}]" + (f"{{{name}}}" if name else "")


def uuid_journal(jkey, pkey=None, name=None):
    j = fid("journal:" + jkey)
    s = f"@UUID[Compendium.{MOD}.journals.JournalEntry.{j}"
    if pkey:
        s += f".JournalEntryPage.{fid('page:' + jkey + ':' + pkey)}"
    return s + "]" + (f"{{{name}}}" if name else "")


def uuid_table(key, name=None):
    return f"@UUID[Compendium.{MOD}.tables.RollTable.{fid('table:' + key)}]" + (f"{{{name}}}" if name else "")


def uuid_macro(key, name=None):
    return f"@UUID[Compendium.{MOD}.macros.Macro.{fid('macro:' + key)}]" + (f"{{{name}}}" if name else "")


def icon(name):
    return f"{ASSET}/icons/{name}.webp"


def portrait(name):
    return f"{ASSET}/portraits/{name}.webp"


def tok(name):
    return f"{ASSET}/tokens/{name}.webp"
