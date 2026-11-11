"""Ashen Forms: the Circle of Ashen Covenants wild-shapes into fiends.

The druid's Wild Shape can take fiend forms instead of beasts, with the Circle of the Moon's challenge-rating progression,
and at 10th level an Infernal Form (CR 5 devil) in place of the Moon druid's elementals.
- SRD fiends ship as actors built from the dnd5e 5.3.3 SRD (Lemure, Dretch, Imp, Quasit, Hell Hound, Bearded Devil,
  Barbed Devil), using the system's own tokens.
- Fiends from other official books are listed by book and page only; their stat blocks are not reproduced.
- Seven original fiends of Avernus written for this adventure ship as actors and stat blocks.
"""
import copy, yaml
from lib5e import *

SRD = "/home/claude/ref/dnd5e/packs/_source/monsters/fiend"
FOLDER = "Ashen Forms (Wild Shape)"
P = lambda *x: "".join(f"<p>{y}</p>" for y in x)

# key, srd file, token file, tint (None = system art as is)
SRD_FORMS = [("lemure", "lemure", "Lemure"), ("dretch", "dretch", "Dretch"), ("imp", "imp", "Imp"), ("quasit", "quasit", "Quasit"),
             ("hell-hound", "hell-hound", "HellHound"), ("bearded-devil", "bearded-devil", "BeardedDevil"),
             ("barbed-devil", "barbed-devil", "Barbed")]
# name, size, subtype, CR, flying?, source
BOOK_FORMS = [("Manes", "Small", "demon", 0.125, False, "MM 60"), ("Abyssal Wretch", "Medium", "demon", 0.25, False, "MTF 136"),
              ("Nupperibo", "Medium", "devil", 0.5, False, "MotM 196 / MTF 168"), ("Maw Demon", "Medium", "demon", 1, False, "MotM 176 / VGM 137"),
              ("Vargouille", "Tiny", "—", 1, True, "MotM 251 / VGM 195"), ("Rutterkin", "Medium", "demon", 2, False, "MotM 210 / MTF 136"),
              ("Spined Devil", "Small", "devil", 2, True, "MM 78")]


def _strip(d):
    if isinstance(d, dict):
        d.pop("_key", None)
        for v in d.values():
            _strip(v)
    elif isinstance(d, list):
        for v in d:
            _strip(v)
    return d


def srd_actor(key, f, tokname):
    a = _strip(copy.deepcopy(yaml.safe_load(open(f"{SRD}/{f}.yml"))))
    a["_id"] = fid(f"actor:ashenform:{key}")
    a["folder"] = None
    a["ownership"] = {"default": 2}
    a.pop("_stats", None)
    img = f"systems/dnd5e/tokens/fiend/{tokname}.webp"
    a["img"] = img
    a["prototypeToken"]["texture"]["src"] = img
    a["prototypeToken"].setdefault("ring", {})["enabled"] = False
    a.setdefault("flags", {})[MOD] = {"key": f"ashenform-{key}", "ashenForm": True, "srd": True}
    return a


# =============================================================================== ORIGINAL FIENDS OF AVERNUS
def _hb():
    from bestiary import Mon, R
    out = []

    def make(key, name, m, tok, tint, **kw):
        a = npc(f"ashenform-{key}", name, img=f"systems/dnd5e/tokens/{tok}.webp", token=f"systems/dnd5e/tokens/{tok}.webp",
                items=m.items, ctype="fiend", subtype="devil", alignment="lawful evil", **kw)
        a["_id"] = fid(f"actor:ashenform:{key}")
        a["ownership"] = {"default": 2}
        a["prototypeToken"]["texture"]["tint"] = tint
        a["flags"][MOD] = {"key": f"ashenform-{key}", "ashenForm": True, "homebrew": True}
        out.append(a)

    m = Mon("cmite")
    m.trait("Ember Body", "A creature that touches the mite or hits it with a melee attack while within 5 feet of it takes 1 fire damage.")
    m.trait("Furnace-Fed", "While touching a fire, a burning object or a soul furnace, the mite regains 2 hit points at the start of its turn.")
    m.atk("Ember Bite", 5, [dmg(1, 4, 3, ["piercing"]), dmg(1, 4, "", ["fire"])], img="ic-embers")
    make("cinder-mite", "Cinder Mite", m, "beast/GiantFireBeetle", "#ff7a4a", size="tiny", cr=0.25, ac=13, hp=10,
         hp_formula="4d4", speed=20, climb=20, abilities=(4, 16, 11, 6, 12, 6), di=("fire", "poison"), ci=("poisoned",),
         senses={"darkvision": 60}, langs=("infernal",), lang_custom="understands Infernal but can't speak",
         bio=P("Thumb-sized devils that nest in the cold furnaces of wrecked war machines and gnaw the ash for the last warmth "
               "of the souls burned there. The Souljack Yard is full of them."))
    m = Mon("tally")
    m.trait("Scent of Ink", "The tallyhound has advantage on Wisdom (Perception) checks that rely on smell, and can smell fresh "
            "ink, sealing wax and signed contracts within 30 feet.")
    m.atk("Bite", 4, [dmg(1, 8, 2, ["piercing"])], "If the target is a creature, it must succeed on a DC 12 Strength saving "
          "throw or be knocked prone.", img="ic-talon")
    make("tallyhound", "Tallyhound", m, "fiend/StingerJackal", "#ffb08a", cr=0.5, ac=13, hp=22, hp_formula="4d8+4",
         speed=40, abilities=(14, 14, 12, 5, 13, 6), skills={"prc": 1}, dr=("cold",), di=("fire", "poison"), ci=("poisoned",),
         senses={"darkvision": 60}, langs=("infernal",), lang_custom="understands Infernal but can't speak",
         bio=P("The hounds of the Counting Gate. A tallyhound tracks unpaid debts the way a bloodhound tracks the wounded, and "
               "it barks once for every name it smells on a contract."))
    m = Mon("gwing")
    m.trait("Devil's Sight", "Magical darkness doesn't impede the gatewing's darkvision.")
    m.trait("Flyby", "The gatewing doesn't provoke opportunity attacks when it flies out of an enemy's reach.")
    m.atk("Seal Talons", 5, [dmg(2, 4, 3, ["slashing"])], "A creature hit is marked with a glowing brass seal until the end of "
          "the gatewing's next turn; the next attack roll against it has advantage.", img="ic-talon")
    make("brass-gatewing", "Brass Gatewing", m, "beast/GiantBat", "#e8b45a", size="sm", cr=1, ac=14, hp=27,
         hp_formula="6d6+6", speed=20, fly=60, abilities=(10, 16, 12, 10, 12, 10), dr=("cold",), di=("fire", "poison"),
         ci=("poisoned",), senses={"darkvision": 120}, langs=("infernal",), lang_custom="understands Common but can't speak it",
         bio=P("Brass-winged couriers of the Brass Registry, carrying writs between the Citadel and the far tollhouses. Their "
               "talons leave a seal that every devil can read."))
    m = Mon("stoke")
    m.trait("Furnace Charge", "If the stokeback moves at least 20 feet straight toward a target and then hits it with a Gore "
            "attack on the same turn, the target takes an extra 2d6 piercing damage. A creature must also succeed on a DC 14 "
            "Strength saving throw or be knocked prone.")
    m.trait("Beast of Burden", "The stokeback counts as one size larger for carrying capacity, and can tow a war machine.")
    m.atk("Gore", 6, [dmg(2, 6, 4, ["piercing"])], img="ic-slam")
    make("stokeback", "Stokeback", m, "beast/GiantBoar", "#ff6a4a", size="lg", cr=2, ac=13, hp=51, hp_formula="6d10+18",
         speed=40, abilities=(18, 10, 16, 3, 10, 5), dr=("cold",), di=("fire", "poison"), ci=("poisoned",),
         senses={"darkvision": 60}, langs=(), lang_custom="understands Infernal but can't speak",
         bio=P("Hunched draught-devils with furnaces in their backs, bred to haul siege engines and souljack rigs across the ash "
               "when the soul fuel runs out."))
    m = Mon("toll")
    m.trait("Barbed Hide", "At the start of each of its turns, the toll-warden deals 1d6 piercing damage to any creature "
            "grappling it.")
    m.trait("Magic Resistance", "The toll-warden has advantage on saving throws against spells and other magical effects.")
    m.multi("The toll-warden makes two Toll Hook attacks.")
    m.atk("Toll Hook", 5, [dmg(1, 8, 3, ["slashing"])], "Once per turn, a creature hit must succeed on a DC 13 Wisdom saving "
          "throw or be unable to take reactions until the end of its next turn, as the toll is exacted.", img="ic-chain")
    make("toll-warden", "Barbed Toll-Warden", m, "fiend/BeardedDevil", "#c9a070", cr=3, ac=15, hp=52, hp_formula="8d8+16",
         speed=30, abilities=(16, 14, 15, 10, 12, 11), saves=("str", "con"), dr=("cold",),
         dr_custom="bludgeoning, piercing and slashing from nonmagical attacks that aren't silvered", di=("fire", "poison"),
         ci=("poisoned",), senses={"darkvision": 120}, langs=("infernal",), lang_custom="telepathy 60 ft.",
         bio=P("Barbed devils who keep the tollhouses on the roads to the Brass Citadel. Every hook on their hide was once a "
               "receipt someone refused to pay."))
    m = Mon("writ")
    m.trait("Relentless Pursuit", "The writ hound always knows the direction of a creature it has bitten within the last 24 "
            "hours, while both are on the same plane.")
    m.trait("Keen Smell", "The writ hound has advantage on Wisdom (Perception) checks that rely on smell.")
    m.multi("The writ hound makes one Bite attack and one Chain Lash attack.")
    m.atk("Bite", 6, [dmg(2, 8, 4, ["piercing"])], img="ic-talon")
    m.atk("Chain Lash", 6, [dmg(1, 10, 4, ["bludgeoning"])], "The target is grappled (escape DC 14) if it is Large or smaller. "
          "Until the grapple ends, the writ hound can't Chain Lash another target.", reach=10, img="ic-chain")
    make("writ-hound", "Writ Hound", m, "fiend/LickerHound", "#ff9a7a", size="lg", cr=4, ac=15, hp=76, hp_formula="9d10+27",
         speed=50, abilities=(18, 14, 17, 6, 13, 8), skills={"prc": 1, "sur": 1}, dr=("cold",), di=("fire", "poison"),
         ci=("poisoned",), senses={"darkvision": 120}, langs=(), lang_custom="understands Infernal but can't speak",
         bio=P("The repossession men's hunting hounds, chained in pairs to the Iron Reclaimer. A writ hound that has tasted a "
               "debtor never loses the scent."))
    m = Mon("hwarden")
    m.trait("Magic Resistance", "The hellwarden has advantage on saving throws against spells and other magical effects.")
    m.trait("Ash Aura", "At the start of each of the hellwarden's turns, each creature of its choice within 10 feet of it takes "
            "5 (1d10) fire damage.")
    m.multi("The hellwarden makes two Ember Fist attacks.")
    m.atk("Ember Fist", 8, [dmg(2, 8, 5, ["bludgeoning"]), dmg(1, 6, "", ["fire"])], img="ic-slam")
    m.sv("Cinder Breath", "dex", 14, [dmg(6, 6, "", ["fire"])], "The hellwarden exhales burning ash in a 15-foot cone. Each "
         "creature in the cone makes a DC 14 Dexterity saving throw, taking 21 (6d6) fire damage on a failure or half as much "
         "on a success.", area=("cone", 15), img="ic-embers", uses_=R(5))
    make("ashen-hellwarden", "Ashen Hellwarden", m, "fiend/Barbed", "#9a9a9a", size="lg", cr=5, ac=16, hp=110,
         hp_formula="13d10+39", speed=40, abilities=(20, 12, 17, 8, 14, 12), saves=("con", "wis"), dr=("cold",),
         dr_custom="bludgeoning, piercing and slashing from nonmagical attacks that aren't silvered", di=("fire", "poison"),
         ci=("poisoned",), senses={"darkvision": 120}, langs=("infernal",), lang_custom="telepathy 60 ft.",
         bio=P("A guardian of grey ash and banked coals, raised where an oath burned out. Ashen druids learn its shape from the "
               "groves that grow on old battlefields: the Circle's Infernal Form."))
    return out


SRD_ACTORS = [srd_actor(*x) for x in SRD_FORMS]
HOMEBREW = _hb()
ACTORS = SRD_ACTORS + HOMEBREW
_BY = {a["flags"][MOD]["key"].replace("ashenform-", ""): a for a in ACTORS}


def _cr(cr):
    return {0.125: "1/8", 0.25: "1/4", 0.5: "1/2"}.get(cr, str(int(cr)) if cr == int(cr) else str(cr))


def _level(cr, fly):
    lv = 2 if cr <= 1 else int(cr * 3)
    return max(lv, 8) if fly else lv


def _rows(link):
    rows = []
    for k, a in _BY.items():
        cr = a["system"]["details"]["cr"]
        fly = bool(a["system"]["attributes"]["movement"].get("fly"))
        nm = f"@UUID[Compendium.{MOD}.actors.Actor.{a['_id']}]{{{a['name']}}}" if link else a["name"]
        src = "This adventure (stat block in Book II)" if a["flags"][MOD].get("homebrew") else "SRD (Foundry actor)"
        rows.append((cr, a["name"], [nm, _cr(cr), ("Infernal Form (10th)" if cr == 5 else str(_level(cr, fly))), src]))
    for n, sz, st, cr, fly, ref in BOOK_FORMS:
        rows.append((cr, n, [n, _cr(cr), str(_level(cr, fly)), f"{ref} (use your own copy)"]))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def table_html(link=True):
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r[2]) + "</tr>" for r in _rows(link))
    return ('<table class="rc-table"><thead><tr><th>Ashen Form</th><th>CR</th><th>Druid level</th><th>Stat block</th></tr>'
            f"</thead><tbody>{body}</tbody></table>")


RULES = P(
    "When you use Wild Shape, you can transform into a fiend from the <strong>Ashen Forms</strong> list instead of a beast. "
    "The Circle teaches the shapes of Hell's lesser servants so that its druids can walk among them, and turn them.",
    "<strong>Challenge rating.</strong> Your Ashen Forms follow the Circle of the Moon's limits: challenge rating 1 or lower "
    "from 2nd level; from 6th level, up to your druid level divided by 3, rounded down (CR 2 at 6th, CR 3 at 9th, CR 4 at "
    "12th, CR 5 at 15th). A form with a flying speed needs druid level 8. Unlike the Circle of the Moon, assuming an Ashen "
    "Form still takes your action.",
    "<strong>In fiend form.</strong> The normal Wild Shape rules apply. You gain the form's traits, including Magic "
    "Resistance, Devil's Sight and telepathy, but you can't use a Shapechanger trait, spellcasting, innate spells or any "
    "ability that summons or gates in other creatures. Devils and demons see you as one of their own kind until you give "
    "yourself away; that can be worth more in Avernus than any claw.",
    "<strong>Other books.</strong> Forms marked with a book and page use that book's stat block. They are listed so a table "
    "that owns those books can use them; nothing here reproduces them. A table without them simply uses the other forms.")
INFERNAL = P(
    "You can expend two uses of Wild Shape at the same time to take an <strong>Infernal Form</strong>: a "
    "<strong>Barbed Devil</strong> or an <strong>Ashen Hellwarden</strong> (both CR 5). This works like the Circle of the "
    "Moon's Elemental Wild Shape. The Ash Warden Spirit draws on the same Wild Shape uses, so an Infernal Form and the spirit "
    "compete for the same pool.")


def looks_html():
    return ""
