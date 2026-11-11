"""Every creature, NPC and battlefield object of Interplanal Champions as dnd5e 5.3.3 NPC actors.

Numbers follow Book I (NPC Dossiers, Appendix A and Appendix B). Where a number had to be supplied or adjusted,
the reason is recorded in DESIGN_NOTES for the GM's audit page.
"""
from lib5e import *

DESIGN_NOTES = []


def note(s):
    DESIGN_NOTES.append(s)


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


BONUS = lambda c="": activation("bonus", 1, c)
REACT = lambda c="": activation("reaction", 1, c)
LEG = lambda n=1: activation("legendary", n)
LAIR = activation("lair", 1, "Initiative count 20 (losing initiative ties)")
SPECIAL = activation("special", None)
DT = {"blud": "bludgeoning", "pier": "piercing", "slas": "slashing"}


class Mon:
    """Small builder so each stat block reads like the book."""

    def __init__(self, key):
        self.k, self.items, self.n = key, [], 0

    def _f(self, name, desc, img, acts=(), uses_=None, effects=None):
        self.n += 1
        self.items.append(feat(f"{self.k}-{self.n}", name, desc, img=icon(img), activities=list(acts), uses_=uses_,
                               effects=effects, sort=self.n * 100))
        return self

    def trait(self, name, desc, img="ic-proof"):
        return self._f(name, P(desc) if not desc.startswith("<") else desc, img)

    def multi(self, desc):
        return self._f("Multiattack", P(desc), "ic-slam", [utility(f"{self.k}-m{self.n}", 0)])

    def atk(self, name, hit, parts, desc="", reach=5, rng_=None, kind="melee", cls="weapon", img="ic-slam", act=None,
            consumption=None, uses_=None, extra=""):
        t = "Ranged" if kind == "ranged" else "Melee"
        c = "Spell" if cls == "spell" else "Weapon"
        reach_txt = f"range {rng_} ft." if rng_ else f"reach {reach} ft."
        d = P(f"<em>{t} {c} Attack:</em> [[/attack extended]], {reach_txt}, one target. <em>Hit:</em> [[/damage extended]]."
              + (f" {desc}" if desc else "")) + extra
        a = attack(f"{self.k}-a{self.n}", 0, to_hit=hit, kind=kind, classification=cls, reach=reach, range_=rng_,
                   parts=parts, act=act, consumption=consumption)
        return self._f(name, d, img, [a], uses_=uses_)

    def sv(self, name, ability, dc, parts, desc, *, area=None, rng_=None, on_save="half", img="ic-hex", act=None,
           uses_=None, consumption=None, effects=None, count=""):
        tgt = target(count or "", "creature", area[0], area[1]) if area else target(count or 1, "creature")
        a = save(f"{self.k}-s{self.n}", 0, ability=ability, dc=dc, parts=parts, on_save=on_save, tgt=tgt,
                 rng_=rng(rng_) if rng_ else None, act=act, uses=None, consumption=consumption,
                 effects=[e["_id"] for e in (effects or [])])
        return self._f(name, P(desc), img, [a], uses_=uses_, effects=effects)

    def util(self, name, desc, img="ic-proof", act=None, uses_=None, consumption=None, effects=None, roll=None):
        a = utility(f"{self.k}-u{self.n}", 0, act=act, consumption=consumption, roll=roll,
                    effects=[e["_id"] for e in (effects or [])])
        return self._f(name, P(desc) if not desc.startswith("<") else desc, img, [a], uses_=uses_, effects=effects)

    def heal(self, name, formula, desc, img="ic-drain", act=None, uses_=None, consumption=None, temp=False):
        a = heal_act(f"{self.k}-h{self.n}", 0, formula_part=dmg_formula(formula), act=act, consumption=consumption,
                     tgt=target("", "self"), temp=temp)
        return self._f(name, P(desc), img, [a], uses_=uses_)


def R(n):
    return uses(1, [recharge(n)])


USE1 = consume_item_uses()


def day(n):
    return uses(n, ["day"])


def per(n, period="lr"):
    return uses(n, [period])


FOLDERS = {}


def put(folder, actor):
    FOLDERS.setdefault(folder, []).append(actor)
    return actor


def make(folder, key, name, m, **kw):
    kw.setdefault("img", portrait(key))
    kw.setdefault("token", tok(key))
    return put(folder, npc(key, name, items=m.items, **kw))


F1 = "Chapter I — Welcome to Hell"
F2 = "Chapter II — The Fallen (Greyhurst)"
F3 = "Chapter III–IV — The War of Claims & the Citadel"
F4 = "Chapter V — The Pyric Triune"
F5 = "Rival Claimants & Sponsors"
F6 = "Allies, Officials & Witnesses"
F7 = "Battlefield Objects"

# =========================================================================== CHAPTER I
m = Mon("imp")
m.trait("Devil's Sight", "Magical darkness doesn't impede the imp's darkvision.")
m.trait("Magic Resistance", "The imp has advantage on saving throws against spells and other magical effects.")
m.trait("Filing Surcharge", "The imp insists the right of appeal costs a fee. It doesn't. A DC 15 Insight check or an "
        "evidence-based legal argument earns the tiny brass receipt <em>EXEMPT FROM FRAUDULENT FEES</em> (Exhibit, one use).")
m.atk("Sting", 5, [dmg(1, 4, 3, ["piercing"]), dmg(3, 6, "", ["poison"])], "The poison damage is halved on a DC 11 "
      "Constitution save (roll it separately).", img="ic-needle")
m.util("Invisibility", "The imp magically turns invisible until it attacks or until its concentration ends.",
       img="ic-hex")
make(F1, "imp-tollkeeper", "Imp Tollkeeper", m, size="tiny", ctype="fiend", subtype="devil", alignment="lawful evil",
     cr=1, ac=13, hp=10, hp_formula="3d4+3", speed=20, fly=40, abilities=(6, 17, 13, 11, 12, 14),
     skills={"dec": 4, "ins": 3, "prf": 4, "ste": 5}, dr=("cold",), dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks that aren't silvered",
     di=("fire", "poison"), ci=("poisoned",), senses={"darkvision": 120}, langs=("infernal", "common"),
     bio=P("Two imps keep the Counting Gate. They ask every arrival for a name, a slate and whether they claim the right of "
           "appeal, and they lie about the price of the last question."))

m = Mon("notary")
m.trait("Floating Witness", "The notary hovers and cannot be knocked prone. It is immune to effects that would make it "
        "testify falsely; it can refuse to answer.")
m.trait("Proof of Survival", "Three notaries together can certify that the party crossed without sacrificing an unwilling "
        "bystander. Their joint testimony creates the <strong>Proof of Survival</strong>. If the party rescued a stranded "
        "courier, they also certify one bonus Survival Crown Mark.")
m.atk("Bite of Record", 4, [dmg(1, 6, 2, ["piercing"]), dmg(1, 4, "", ["psychic"])], img="ic-talon")
make(F1, "skull-notary", "Skull Notary", m, size="tiny", ctype="undead", alignment="lawful neutral", cr=0.5, ac=13,
     hp=13, hp_formula="3d4+6", speed=0, fly=40, hover=True, abilities=(4, 14, 14, 14, 14, 10), di=("poison",),
     ci=("poisoned", "exhaustion", "prone"), senses={"darkvision": 60}, langs=("infernal", "common"), disposition=0,
     bio=P("A skull wrapped in a notary's ribbon, sealing wax dripping from its jaw. It wants a clean record more than it "
           "wants anything else."))

m = Mon("ferry")
m.trait("Defined Price", "The ferryman offers passage for 'the one memory you can most easily afford to lose'. The exact "
        "memory and its consequence must be named before signing; he cannot take an unspecified memory by trick. Use the "
        "Memory Escrow template (Form IC-04 style) and a stated return condition.")
m.trait("Styx-Touched", "A creature that drinks from or deliberately immerses itself in the black Styx branch must succeed "
        "on a DC 15 Intelligence saving throw or lose memories of the last 24 hours until a <em>greater restoration</em>.")
m.atk("Pole of the Black Water", 6, [dmg(2, 8, 3, ["bludgeoning"]), dmg(1, 8, "", ["necrotic"])], reach=10, img="ic-glaive")
make(F1, "styx-ferryman", "The Styx Ferryman", m, ctype="undead", alignment="neutral", cr=5, ac=15, hp=90,
     hp_formula="12d8+36", speed=30, abilities=(16, 12, 16, 14, 16, 16), saves=("wis", "cha"), di=("poison",),
     ci=("charmed", "frightened", "poisoned"), senses={"truesight": 60}, langs=("common", "infernal", "abyssal"),
     disposition=0, bio=P("Hooded, patient and scrupulously exact. He is not cruel; he is a vendor."))

m = Mon("scrap")
m.trait("Constructive Repair", "<em>Mending</em> restores 5 hit points once per golem per long rest. It never heals from fire damage.")
m.trait("Volatile End", "When destroyed, the golem sheds sparks in 5 feet: DC 14 Dexterity save, 2d6 fire damage, half on a "
        "success. No explosion if it is disabled by a lawful shutdown order, or by a DC 17 Arcana check as an action within 5 feet.")
m.multi("The golem makes two Scrap Slam attacks.")
m.atk("Scrap Slam", 7, [dmg(2, 8, 4, ["bludgeoning"])])
m.sv("Shrapnel Vent (Recharge 5–6)", "dex", 15, [dmg(4, 6, "", ["piercing"])],
     "Each creature in a 15-foot cone makes a [[/save]] saving throw, taking [[/damage extended]] on a failure, or half as "
     "much on a success.", area=("cone", 15), img="ic-shrapnel", uses_=R(5), consumption=USE1)
m.sv("Volatile End (on destruction)", "dex", 14, [dmg(2, 6, "", ["fire"])], "Sparks in 5 feet when the golem is destroyed.",
     area=("radius", 5), img="ic-embers", act=SPECIAL)
make(F1, "ash-scrap-golem", "Ash-Scrap Golem", m, ctype="construct", alignment="unaligned", cr=5, ac=16, hp=88,
     hp_formula="11d8+33", speed=30, abilities=(18, 10, 16, 3, 10, 1), saves=("con",), dr=("fire",),
     dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks", di=("poison",),
     ci=("charmed", "exhaustion", "poisoned"), senses={"darkvision": 60},
     bio=P("Scrap welded around one of Janella's cheaper cores. Built to guard, not to hate."))

# =========================================================================== CHAPTER II
m = Mon("warder-d")
m.trait("Cracked Control Core", "At initiative count 20 each round, roll 1d6: on a 1 the warder loses its reaction until its "
        "next turn; on a 2 it cannot move; on a 3–6 it acts normally. A character can take an action to attempt a DC 17 "
        "Arcana or tinker's tools check to suspend its aggression for one round.")
m.trait("WARD HOUSE, NEVER WAR HOUSE", "The inscription on its chest. Its original mandate is protective. If restored, replace "
        "this stat block with the <em>Iron Warder, Restored</em>; never stack the two.")
m.util("Roll the Cracked Core", "Initiative 20.", img="ic-core", roll=("1d6", "Cracked Core"), act=LAIR)
m.multi("The warder makes two Guardian Fist attacks.")
m.atk("Guardian Fist", 9, [dmg(2, 10, 5, ["bludgeoning"])])
m.util("Interpose", "<p><strong>Reaction.</strong> If a creature within 5 feet takes damage, reduce that damage by 12; the "
       "warder takes 6 force damage as its chassis stresses.</p>", img="ic-guardian", act=REACT("an adjacent creature takes damage"))
make(F2, "iron-warder-damaged", "Iron Warder Prototype (Damaged)", m, size="lg", ctype="construct", alignment="unaligned",
     cr=7, ac=18, hp=128, hp_formula="15d10+45", speed=25, abilities=(21, 8, 17, 5, 10, 3), dr=("fire",),
     dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks", di=("poison",),
     ci=("charmed", "frightened", "poisoned"), senses={"darkvision": 60}, disposition=0,
     bio=P("A weathered iron giant slumped beside a wall, chest plate open around a missing core. Not a surprise fight: a "
           "CR 7 chassis with an explicit initiative routine and no fire-healing loop."))

m = Mon("warder-r")
m.trait("Autonomous Mandate", "Its first priority is protecting named innocents. An ally cannot override that priority merely "
        "by carrying the control core; changing it requires the construct's informed agreement.")
m.trait("Allied Warder", "As an ally, the warder acts on one designated player's initiative. That player uses a bonus action "
        "to issue a simple command: move and one Guardian Fist, Help, or Dodge. With no command it Dodges and protects the "
        "nearest named civilian. It can't use Boundary Pulse as a free companion feature.")
m.multi("The warder makes two Guardian Fist attacks.")
m.atk("Guardian Fist", 10, [dmg(3, 8, 6, ["bludgeoning"])])
m.sv("Boundary Pulse (Recharge 5–6)", "str", 17, [dmg(4, 8, "", ["thunder"])],
     "Enemies within 15 feet make a [[/save]] saving throw. On a failure a creature takes [[/damage extended]] and is pushed "
     "15 feet; on a success it takes half damage and isn't pushed.", area=("radius", 15), img="ic-shrapnel",
     uses_=R(5), consumption=USE1)
m.util("Interpose", "<p><strong>Reaction.</strong> Reduce damage to an adjacent ally by 16, then take 8 force damage.</p>",
       img="ic-guardian", act=REACT("an adjacent ally takes damage"))
make(F2, "iron-warder-restored", "Iron Warder, Restored", m, size="lg", ctype="construct", alignment="lawful neutral",
     cr=10, ac=19, hp=172, hp_formula="15d10+90", speed=30, abilities=(22, 10, 22, 8, 12, 6), saves=("str", "con"),
     dr=("fire", "force"), dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks", di=("poison",),
     ci=("poisoned",), senses={"darkvision": 60}, langs=("common",), lang_custom="understands Janella's maker-signal",
     disposition=1, bio=P("The prototype with its infernal-glass heart restored: original defensive orders and a perfect "
                          "recording of Kane's sale."))

m = Mon("janella")
m.trait("Spellcasting", "Janella's spellcasting ability is Intelligence (spell save DC 16, +8 to hit). At will: <em>mending, "
        "mage hand, fire bolt</em>. 3/day each: <em>shield, heat metal, web, counterspell</em>. 1/day each: <em>dispel magic, "
        "fabricate</em>.", img="ic-glassheart")
m.trait("Construct Charges", "Three prepared construct charges per day. Bringing a new construct online takes 10 minutes, a "
        "spare core and a valid repair site. No unlimited golem creation in combat.")
m.multi("Janella makes two Dual Coil Bolt attacks.")
m.atk("Dual Coil Bolt", 8, [dmg(2, 8, 5, ["lightning"])], kind="ranged", cls="spell", rng_=90, img="ic-bolt")
m.util("Command Construct", "<p><strong>Bonus Action.</strong> One allied golem within 60 feet that can receive her signal "
       "moves up to half its speed and makes one Slam attack, or takes the Help action. This replaces that golem's own "
       "extra action; she commands at most one golem per round.</p>", img="ic-golem", act=BONUS())
m.util("Emergency Shield (2/Day)", "<p><strong>Reaction.</strong> +4 AC against one attack she can see.</p>",
       img="ic-writshield", act=REACT("she is targeted by an attack"), uses_=day(2), consumption=USE1)
m.util("Smoke Cover (Escalation, once)", "When reduced below 40 hit points she releases smoke in 15 feet, heavily obscuring "
       "the area until the start of her next turn, and retreats toward a defensible position. She fights to protect her "
       "family, not to die proving a point.", img="ic-embers", uses_=per(1), consumption=USE1, act=SPECIAL)
make(F2, "janella-greenbottle", "Janella Greenbottle, Golemancer of Greyhurst", m, size="sm", ctype="humanoid",
     subtype="halfling", alignment="neutral", cr=8, ac=16, ac_calc="flat", hp=96, hp_formula="17d6+34", speed=25,
     abilities=(10, 16, 14, 20, 14, 12), saves=("dex", "int", "wis"), skills={"arc": 11, "inv": 11, "ins": 5},
     dr=("fire",), langs=("common", "halfling", "dwarvish", "infernal"), disposition=0, spellcasting="int", spell_level=8,
     bio=P("A halfling artificer who built Greyhurst's defensive constructs. Her family includes her husband Marus and her "
           "daughter Lila. She can be ally, reluctant rival or antagonist. Her creations are not interchangeable loot."))

m = Mon("lila")
m.trait("Just a Child", "Lila is noncombatant. A good act toward her opens negotiation with Janella without a check.")
make(F6, "lila-greenbottle", "Lila Greenbottle", m, size="sm", ctype="humanoid", subtype="halfling", alignment="neutral good",
     cr=0, ac=11, ac_calc="flat", hp=4, hp_formula="2d4-1", speed=25, abilities=(6, 13, 9, 12, 12, 14),
     langs=("common", "halfling"), disposition=1, bio=P("Janella's daughter. Carries a wind-up bird she says is her father's."))

m = Mon("collector")
m.trait("Warrant of the Unclaimed", "It marches under warrants naming souls as 'unclaimed'. A documented, valid challenge using "
        "Exhibit A forces the accompanying registrar to suspend collection and yields <strong>Exhibit B: The False Service Order</strong>.")
m.multi("The collector makes two Hook Spear attacks.")
m.atk("Hook Spear", 7, [dmg(1, 10, 4, ["piercing"]), dmg(1, 6, "", ["necrotic"])], reach=10, img="ic-glaive")
make(F2, "cadaver-collector", "Armoured Cadaver Collector", m, size="lg", ctype="construct", alignment="lawful evil",
     cr=6, ac=17, hp=105, hp_formula="10d10+50", speed=30, abilities=(19, 10, 20, 5, 11, 3), dr=("fire", "necrotic"),
     di=("poison",), ci=("charmed", "exhaustion", "poisoned"), senses={"darkvision": 60},
     lang_custom="understands Infernal but can't speak")
note("<strong>Armoured Cadaver Collector</strong> and <strong>Brass Registrar</strong> are named in Book I (3D) without stat "
     "blocks; both were built at CR 6 and CR 3 to match the Chapter II budget.")

m = Mon("registrar")
m.trait("Clerical Obedience", "The registrar suspends a collection the moment it is shown a valid written challenge.")
m.atk("Stamp of Default", 5, [dmg(2, 6, 3, ["bludgeoning"])], img="ic-stamp")
m.sv("Notice of Collection (Recharge 5–6)", "wis", 13, [dmg(3, 6, "", ["psychic"])],
     "One creature within 60 feet makes a [[/save]] saving throw, taking [[/damage extended]] on a failure, or half as much "
     "on a success.", rng_=60, img="ic-writ", uses_=R(5), consumption=USE1)
make(F2, "brass-registrar", "Brass Registrar", m, ctype="construct", alignment="lawful evil", cr=3, ac=16, hp=60,
     hp_formula="8d8+24", speed=30, abilities=(14, 12, 16, 14, 12, 10), dr=("fire",), di=("poison",), ci=("poisoned",),
     senses={"darkvision": 60}, langs=("infernal", "common"))

m = Mon("clerk")
m.trait("Testimony for a Question", "Testifies only if the party submits an actual question and discloses its intended use. "
        "Promise to protect its name, or command it by magic and risk the evidence being disputed as coerced.")
m.trait("Incorporeal Movement", "The clerk can move through creatures and objects as difficult terrain.")
m.atk("Withering Ink", 4, [dmg(2, 6, 1, ["necrotic"])], img="ic-pen")
make(F2, "spectral-clerk", "Spectral Mayoral Clerk", m, ctype="undead", alignment="lawful neutral", cr=1, ac=11, ac_calc="flat",
     hp=22, hp_formula="5d8", speed=0, fly=40, hover=True, abilities=(7, 13, 10, 14, 12, 11), di=("poison", "necrotic"),
     dr=("acid", "fire", "lightning", "thunder"), dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks",
     ci=("charmed", "exhaustion", "grappled", "paralyzed", "petrified", "poisoned", "prone", "restrained"),
     senses={"darkvision": 60}, langs=("common",), disposition=0)

m = Mon("kane")
m.trait("Confession Trigger", "Present his signed roster and the inverse rune and he loses Summon Witness for one round; he "
        "must respond to the allegation. He can survive capture and testify instead of dying.")
m.multi("Kane makes two Corrupted Sceptre attacks.")
m.atk("Corrupted Sceptre", 8, [dmg(2, 8, 4, ["bludgeoning"]), dmg(1, 6, "", ["necrotic"])], img="ic-sceptre")
m.util("Summon Witness (1/Day)", "Kane calls two weakened lemure attendants (15 HP, +4 to hit, 1d8 + 2 slashing) that last "
       "3 rounds.", img="ic-portal", uses_=day(1), consumption=USE1)
make(F2, "osric-kane", "Osric Kane, the Lemure King", m, ctype="humanoid", alignment="lawful evil", cr=8, ac=16, ac_calc="flat",
     hp=110, hp_formula="17d8+34", speed=30, abilities=(14, 12, 14, 16, 14, 18), saves=("int", "wis", "cha"),
     skills={"dec": 8, "prf": 8, "his": 7}, langs=("common", "infernal"),
     bio=P("Greyhurst's mayor. He inverted the town's summoning circle to call a devil army and instead registered every "
           "villager's living identity into Avernus. He believed infernal assets would buy permanent protection."))

m = Mon("lemure")
m.trait("Devil's Sight", "Magical darkness doesn't impede the lemure's darkvision.")
m.trait("Hellish Rejuvenation", "A lemure that dies in the Nine Hells comes back to life with all its hit points in 1d10 days "
        "unless it is killed by a good-aligned creature with a <em>bless</em> spell cast on it or its remains are sprinkled with holy water.")
m.atk("Fist", 3, [dmg(1, 4, "", ["bludgeoning"])])
make(F2, "lemure", "Lemure (Weakened Attendant)", m, ctype="fiend", subtype="devil", alignment="lawful evil", cr=0,
     ac=7, ac_calc="flat", hp=13, hp_formula="3d8", speed=15, abilities=(10, 5, 11, 1, 11, 3), dr=("cold",),
     dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks that aren't silvered", di=("fire", "poison"),
     ci=("charmed", "frightened", "poisoned"), senses={"darkvision": 120}, lang_custom="understands Infernal but can't speak")

m = Mon("survivor")
m.trait("Civic Defence Committee", "Survivors who swear voluntary allegiance to an openly organised defence committee count "
        "toward the Proof of Dominion.")
m.atk("Club", 2, [dmg(1, 4, "", ["bludgeoning"])])
make(F6, "greyhurst-survivor", "Greyhurst Survivor", m, ctype="humanoid", subtype="human", alignment="any", cr=0, ac=10,
     ac_calc="flat", hp=4, hp_formula="1d8", speed=30, abilities=(10, 10, 10, 10, 10, 10), langs=("common",), disposition=1)

m = Mon("sable")
m.trait("Declared Truce", "Mother Sable arrives under a declared truce. She gives the full Memorandum of Memory Escrow and "
        "answers direct questions about obligations. If attacked during the truce, the Brass Arbiter records the breach as a "
        "procedural disadvantage. A DC 18 court challenge that proves a concealed annex strikes it.")
m.trait("Spellcasting", "Charisma (save DC 16). At will: <em>detect magic, disguise self, mage hand</em>. 2/day each: "
        "<em>suggestion, counterspell, dimension door</em>.", img="ic-hex")
m.multi("Mother Sable makes two Barrister's Claw attacks.")
m.atk("Barrister's Claw", 7, [dmg(2, 6, 4, ["slashing"]), dmg(1, 6, "", ["psychic"])], img="ic-talon")
make(F4, "mother-sable", "Mother Sable, Coven Barrister", m, ctype="fiend", subtype="hag", alignment="neutral evil", cr=7,
     ac=16, hp=112, hp_formula="15d8+45", speed=30, abilities=(14, 14, 16, 18, 16, 18), saves=("int", "wis", "cha"),
     skills={"dec": 7, "ins": 6, "prf": 7, "arc": 7}, dr=("cold", "fire"), ci=("charmed",), senses={"darkvision": 120},
     langs=("common", "infernal", "abyssal"), disposition=0, spellcasting="cha",
     bio=P("A coven barrister in a velvet lawyer's hood. Misty needs a ruler she can influence, not another fraudulent Red Clause."))
note("<strong>Mother Sable</strong> has no Book I stat block; she is built as a CR 7 social hag so a truce-breach fight "
     "stays survivable at level 12.")

# =========================================================================== CHAPTER III-IV
m = Mon("bailiff")
m.trait("Lawful Stay", "Will obey a valid written stay signed by a recognised court, even if it hates the result.")
m.multi("The bailiff makes two Chain Gavel attacks.")
m.atk("Chain Gavel", 7, [dmg(2, 6, 4, ["bludgeoning"]), dmg(1, 6, "", ["psychic"])], img="ic-hammer")
e_cite = effect("bailiff-cite", "Filed Citation", icon("ic-writ"), duration={"rounds": 1},
                description="<p>You can't take reactions until the end of your next turn.</p>")
m.sv("File Citation (Recharge 4–6)", "wis", 15, [], "<strong>Bonus Action.</strong> One target within 30 feet must succeed "
     "on a [[/save]] saving throw or be unable to take reactions until its next turn.", rng_=30, on_save="none",
     img="ic-writ", act=BONUS(), uses_=R(4), consumption=USE1, effects=[e_cite])
m.util("Obstruct", "<p><strong>Reaction.</strong> When a creature within 5 feet moves away, the bailiff moves 5 feet without "
       "provoking opportunity attacks.</p>", img="ic-chain", act=REACT("a creature within 5 feet moves away"))
make(F3, "writ-bailiff", "Writ Bailiff", m, ctype="fiend", subtype="devil", alignment="lawful evil", cr=5, ac=17, hp=75,
     hp_formula="10d8+30", speed=30, abilities=(18, 12, 16, 10, 12, 12), dr=("fire",), di=("poison",), ci=("poisoned",),
     senses={"darkvision": 60}, langs=("infernal", "common"))

m = Mon("sentinel")
m.trait("Cannot Forbid by Fiat", "The Sentinel cannot prevent an action merely by declaring it illegal.")
m.multi("The Sentinel makes two Writ Hammer attacks.")
m.atk("Writ Hammer", 10, [dmg(2, 10, 6, ["force"])], img="ic-hammer")
e_not = effect("notarise", "Notarised Restraint", icon("ic-chain"), duration={"rounds": 1},
               changes=[("system.attributes.movement.all", 0, "0")],
               description="<p>Speed 0 until the end of your next turn, as long as you can see the Sentinel.</p>")
m.sv("Notarise Restraint (Recharge 5–6)", "wis", 17, [], "Up to two creatures within 30 feet make a [[/save]] saving throw. "
     "On a failure, a creature's speed becomes 0 until the end of its next turn, as long as it can see the Sentinel.",
     rng_=30, count=2, on_save="none", img="ic-chain", uses_=R(5), consumption=USE1, effects=[e_not])
m.util("Clarify Terms (2/Combat)", "<p><strong>Reaction.</strong> When a spell hits the Sentinel, reduce that spell's damage "
       "by 12.</p>", img="ic-proof", act=REACT("a spell hits it"), uses_=per(2, "sr"), consumption=USE1)
make(F3, "contract-sentinel", "Contract Sentinel", m, size="lg", ctype="construct", alignment="lawful evil", cr=10, ac=18,
     hp=158, hp_formula="15d10+75", speed=30, abilities=(22, 10, 20, 8, 12, 8), dr=("fire", "necrotic"), di=("poison",),
     ci=("poisoned",), senses={"darkvision": 60}, lang_custom="understands Infernal and Common")

m = Mon("orro")
m.trait("Vendor of Names", "Offers a regiment of Greyhurst names for thirty soul-coins. Flees if his legal authority to "
        "transfer them is disproven (Exhibits A–C, no roll). Each false entrant bears the red serial "
        "<strong>H-25/RETURN</strong>: Exhibit E, Chain of Title.")
m.multi("Orro makes two Cleaver attacks.")
m.atk("Cleaver", 7, [dmg(2, 6, 4, ["slashing"])], img="ic-glaive")
make(F3, "sergeant-orro", "Sergeant Orro, Merchant of Names", m, ctype="fiend", subtype="devil", alignment="lawful evil",
     cr=5, ac=15, hp=85, hp_formula="10d8+40", speed=30, abilities=(18, 12, 18, 12, 10, 14), skills={"dec": 5, "prf": 5},
     dr=("fire",), di=("poison",), senses={"darkvision": 120}, langs=("infernal", "common"))

m = Mon("hollis")
m.trait("Emergency Authority", "Exhibit E or the original Red Clause ruling invalidates his emergency authority: while held "
        "up within 60 feet, he cannot use False Certification for one round (one use per party per encounter).")
m.trait("Immunity Document", "His immunity document tries to cover future fraud: the words <em>including acts yet to be "
        "discovered</em> are visible to anyone who reads it. Strike the phrase and his testimony can still be taken.")
m.multi("Hollis makes two Pen of Forfeiture attacks.")
m.atk("Pen of Forfeiture", 9, [dmg(3, 10, "", ["psychic"])], kind="ranged", cls="spell", rng_=90, img="ic-pen")
e_cert = effect("false-cert", "False Certification", icon("ic-stamp"), duration={"rounds": 1},
                description="<p>You can't benefit from advantage on your next d20 Test before the end of your next turn.</p>")
m.sv("False Certification (Recharge 5–6)", "int", 17, [], "Each creature in a 20-foot-radius sphere within 90 feet must "
     "succeed on a [[/save]] saving throw or be unable to benefit from advantage on its next d20 Test before the end of its "
     "next turn.", area=("sphere", 20), on_save="none", img="ic-stamp", uses_=R(5), consumption=USE1, effects=[e_cert])
m.util("Stay (3/Day)", "<p><strong>Reaction.</strong> Halve the damage from one attack by sacrificing a prepared counterfeit "
       "document.</p>", img="ic-writ", act=REACT("he is hit by an attack"), uses_=day(3), consumption=USE1)
make(F3, "hollis-valrick", "Hollis Valrick, Deputy Registrar", m, ctype="humanoid", subtype="human", alignment="lawful evil",
     cr=9, ac=17, ac_calc="flat", hp=108, hp_formula="16d8+36", speed=30, abilities=(10, 14, 14, 20, 14, 18),
     saves=("int", "wis", "cha"), skills={"dec": 8, "inv": 9, "his": 9}, langs=("common", "infernal", "draconic"),
     bio=P("The visible bureaucratic antagonist. He secretly harvests paper champions and tests whether an office rather "
           "than an individual can inherit a soul, opening corporate ownership of rulers."))
note("<strong>Hesper Valrick</strong> from the draft is renamed <strong>Hollis Valrick</strong> throughout, so he is never "
     "confused with Hesper Vane from <em>The Night of the Red Clause</em>.")

m = Mon("heir")
m.trait("Forged Sovereignty", "Recovers 15 hit points at the start of its turn while the Championship Stamp remains active. "
        "Destroying the Stamp (AC 17, 40 HP) or winning a witnessed judgment on false entries ends this and stuns the King "
        "until the end of its next turn.")
m.heal("Forged Sovereignty (start of turn)", "15", "While the Stamp stands.", img="ic-stamp", act=activation("turnStart", None))
m.multi("The Vacant King makes three Royal Edict attacks.")
m.atk("Royal Edict", 12, [dmg(2, 8, 7, ["bludgeoning"]), dmg(1, 8, "", ["psychic"])], reach=10, img="ic-edict")
e_seize = effect("seize-name", "Name Seized", icon("ic-edict"), duration={"rounds": 1},
                 description="<p>You can't take reactions until your next turn.</p>")
m.sv("Seize Name (Recharge 5–6)", "cha", 18, [dmg(5, 8, "", ["psychic"])], "One creature within 60 feet makes a [[/save]] "
     "saving throw, taking [[/damage extended]] and losing its reactions until its next turn on a failure, or half damage "
     "on a success.", rng_=60, img="ic-edict", uses_=R(5), consumption=USE1, effects=[e_seize])
m.util("Courtly Counter", "<p><strong>Reaction, once per round.</strong> After being hit, move 10 feet without provoking "
       "opportunity attacks.</p>", img="ic-crownmark", act=REACT("it is hit"))
make(F3, "iron-heir", "The Vacant King (The Iron Heir)", m, size="lg", ctype="construct", alignment="lawful evil", cr=15,
     ac=19, hp=218, hp_formula="19d10+114", speed=35, abilities=(24, 12, 22, 14, 16, 18), saves=("str", "con", "wis", "cha"),
     dr=("fire", "force"), dr_custom="bludgeoning, piercing, and slashing from nonmagical attacks", di=("poison",),
     ci=("charmed", "poisoned"), senses={"darkvision": 120}, langs=("common", "infernal"),
     bio=P("A successor chassis built by corrupting Janella's protect-the-town design: a name given a body of notarised "
           "brass. Its public claim: <em>A machine that can govern flawlessly is more entitled to govern than a mortal who "
           "can break a promise.</em>"))

m = Mon("masked")
m.trait("Who Consented?", "No choice should depend on the creature's type. The question is who genuinely consented to be "
        "represented. Follow the paper trail through Name, Witness, Consideration and Remedy.")
m.multi("The champion makes two Mask-Blade attacks.")
m.atk("Mask-Blade", 7, [dmg(2, 6, 4, ["slashing"])], img="ic-sabre")
for k, nm, ct in (("masked-champion-living", "Masked Champion (the Living Claimant)", "humanoid"),
                  ("masked-champion-construct", "Masked Champion (the Proxy Construct)", "construct"),
                  ("masked-champion-memory", "Masked Champion (the Stitched Memory)", "undead")):
    mm = Mon(k)
    mm.items = [dict(x, _id=fid(f"item:{k}-{i}")) for i, x in enumerate(m.items)]
    make(F3, k, nm, mm, ctype=ct, alignment="neutral", cr=4, ac=15, hp=78, hp_formula="12d8+24", speed=30,
         abilities=(14, 16, 14, 12, 12, 16), langs=("common",), disposition=0)
note("The three <strong>masked champions</strong> share one CR 4 duellist block on purpose: the Trial of False Faces must "
     "never be solved by reading a creature type off a stat block.")

m = Mon("magistrate")
m.trait("Neutral Bench", "The Docket's magistrate states the clause on which each ruling relies. Correct evidence wins a "
        "stage without a check; an improvised case is DC 18.")
make(F6, "magistrate-docket", "Magistrate of the Whispering Docket", m, size="lg", ctype="construct", alignment="lawful neutral",
     cr=0, ac=20, hp=200, speed=0, abilities=(10, 10, 20, 20, 20, 16), di=("poison", "psychic"),
     ci=("charmed", "frightened", "poisoned"), senses={"truesight": 120}, langs=("common", "infernal", "celestial", "abyssal"),
     disposition=0)

m = Mon("claimsclerk")
m.trait("The Circular", "Applies Hollis's unlawful circular interpreting <em>claimant</em> as singular. Cite the Charter's "
        "Article III and the clerk must register a joint slate.")
make(F6, "claims-clerk", "Citadel Claims Clerk", m, size="sm", ctype="fiend", subtype="devil", alignment="lawful evil",
     cr=0.25, ac=12, hp=11, hp_formula="2d6+4", speed=30, abilities=(8, 14, 14, 14, 12, 10), dr=("fire",),
     langs=("infernal", "common"), disposition=0)

m = Mon("arbiter")
m.trait("Independent", "The Brass Arbiter is independent of individual contestants and must state the clause upon which each "
        "ruling relies. An appeal submitted before a scheduled forfeiture stays that forfeiture until the hearing.")
m.trait("Cannot Be Silenced", "No contestant may act to silence the Arbiter. It never steals an unsigned soul.")
make(F6, "brass-arbiter", "The Brass Arbiter", m, size="lg", ctype="construct", alignment="lawful neutral", cr=0, ac=22,
     hp=300, speed=30, abilities=(20, 10, 20, 20, 20, 20), di=("poison", "psychic"), ci=("charmed", "frightened", "poisoned"),
     senses={"truesight": 120}, langs=("common", "infernal", "celestial", "abyssal"), disposition=0)

# =========================================================================== CHAPTER V
m = Mon("advocate")
m.trait("Litigator First", "She retreats if the hearing can be won through litigation.")
m.multi("The advocate makes two Thorn Claw attacks.")
m.atk("Thorn Claw", 9, [dmg(2, 8, 5, ["slashing"]), dmg(1, 8, "", ["psychic"])], img="ic-talon")
e_hex = effect("contract-hex", "Contractual Hex", icon("ic-hex"), duration={"seconds": 60},
               description="<p>Your first attack roll on each turn takes a −1d4 penalty. Repeat the save at the end of each turn.</p>")
m.sv("Contractual Hex (Recharge 5–6)", "cha", 17, [], "One creature within 60 feet must succeed on a [[/save]] saving throw "
     "or be cursed for 1 minute: its first attack roll on each turn takes a −1d4 penalty. It repeats the save at the end of "
     "each of its turns.", rng_=60, on_save="none", uses_=R(5), consumption=USE1, effects=[e_hex])
m.util("Objection (2/Day)", "<p><strong>Reaction.</strong> Give disadvantage to a spell attack targeting her, or advantage to one "
       "of her saves against a spell she can see cast.</p>", img="ic-sp-objection", act=REACT(), uses_=day(2), consumption=USE1)
m.util("Shift Veil (2/Day)", "<p><strong>Bonus Action.</strong> Teleport 20 feet to an unoccupied space she can see.</p>",
       img="ic-portal", act=BONUS(), uses_=day(2), consumption=USE1)
make(F4, "night-hag-advocate", "Night Hag Advocate", m, ctype="fiend", subtype="hag", alignment="lawful evil", cr=11,
     ac=17, hp=138, hp_formula="16d8+64", speed=30, fly=30, hover=True, abilities=(12, 14, 18, 18, 16, 20),
     saves=("con", "wis", "cha"), dr=("fire", "cold", "psychic"), ci=("charmed",), senses={"darkvision": 120},
     langs=("common", "infernal", "abyssal"), bio=P("A coven barrister, not Misty's full power."))

m = Mon("shard")
m.trait("Projection", "Destroying the Oathshard reveals one genuine clue about Misty's covenant but does not injure Misty.")
m.multi("The Oathshard makes two Thorn Lance attacks.")
m.atk("Thorn Lance", 10, [dmg(2, 8, 6, ["piercing"]), dmg(1, 8, "", ["psychic"])], reach=10, img="ic-glaive")
e_fw = effect("false-witness", "False Witness", icon("ic-hex"), statuses=["charmed"], duration={"rounds": 1},
              description="<p>Charmed by the Oathshard until the end of your next turn.</p>")
m.sv("False Witness (Recharge 5–6)", "wis", 18, [], "One creature within 60 feet makes a [[/save]] saving throw or is "
     "charmed by the shard until the end of its next turn; on a success it is immune to this shard's False Witness for "
     "24 hours.", rng_=60, on_save="none", uses_=R(5), consumption=USE1, effects=[e_fw])
m.util("Cut to Shadow (2/Day)", "<p><strong>Bonus Action.</strong> Teleport 30 feet to visible dim light.</p>",
       img="ic-portal", act=BONUS(), uses_=day(2), consumption=USE1)
m.util("Paid Retort", "<p><strong>Reaction, once per round.</strong> Reduce damage from an attack by 10. Not while restrained.</p>",
       img="ic-writshield", act=REACT("it is hit"))
make(F4, "oathshard", "Oathshard of Misty (Limited Projection)", m, ctype="fiend", subtype="hag", alignment="neutral evil",
     cr=13, ac=18, hp=165, hp_formula="22d8+66", speed=30, fly=30, abilities=(16, 16, 16, 18, 18, 22),
     saves=("con", "wis", "cha"), dr=("cold", "fire", "psychic"), di=("poison",), senses={"darkvision": 120},
     langs=("common", "infernal"))

# --- Misty (Appendix A)
MISTY_SPELLS = ("<p><strong>Spellcasting.</strong> Misty uses Charisma (spell save DC 25, +17 to hit). At will: <em>detect "
                "thoughts, disguise self, invisibility</em> (self only), <em>major image</em>. 3/day each: <em>counterspell, "
                "dimension door, greater invisibility, bestow curse</em> (5th level), <em>wall of force</em>. 1/day each: "
                "<em>plane shift</em> (self and willing creatures only), <em>finger of death, power word stun, maze</em>. She "
                "can't use an action spell and her Multiattack in the same action.</p>")


def misty_block(k, phase2=False):
    m = Mon(k)
    m.trait("Magic Resistance", "Advantage on saves against spells and magical effects while the <strong>Seal of Name</strong> "
            "remains intact. Suppressing the Seal removes this for 2 full rounds.", img="ic-reserved")
    m.util("Legendary Resistance (3/Day)", "If she fails a saving throw, she can choose to succeed instead. Suppressing the "
           "<strong>Seal of Jurisdiction</strong> removes one unused use; it never restores a spent one.", img="ic-reserved",
           act=SPECIAL, consumption=consume_legres())
    m.trait("Heartstone Custody", "Her infernal Heartstone sits under three witness-seals: <strong>Name</strong>, "
            "<strong>Consent</strong> and <strong>Jurisdiction</strong>. The stone is an external, knowable object, never an "
            "arbitrary last-second immunity. See the Heartstone object and the Witness objectives.", img="ic-heartstone")
    if not phase2:
        m.trait("Hag Queen's Deception (Mythic, Once)", "The first time Misty drops to 0 hit points she does not die. She "
                "teleports herself and every combatant in the audience chamber to her resting place, restores 144 hit "
                "points and manifests two Children of Hell within 30 feet. Swap this actor for <em>Misty, Unbound</em>. "
                "Legendary Resistances, daily spells and suppressed seals do not reset.", img="ic-portal")
    else:
        m.trait("Second Defeat", "At 0 hit points again, Misty's spirit is pulled into the Heartstone if the tether is intact. "
                "If the tether has been severed and the stone destroyed, the second defeat is permanent.", img="ic-heartstone")
    m._f("Spellcasting", MISTY_SPELLS, "ic-hex")
    m.multi("Misty makes two Thorn Talon attacks, or one Thorn Talon and one Soul Needle attack.")
    m.atk("Thorn Talon", 17, [dmg(3, 8, 8, ["piercing"]), dmg(2, 8, "", ["psychic"])], reach=10, cls="spell", img="ic-talon",
          desc="On a hit, the target knows one specific current fear is being heard by Misty.")
    m.atk("Soul Needle", 17, [dmg(4, 8, 8, ["necrotic"])], kind="ranged", cls="spell", rng_=120, img="ic-needle",
          desc="The target can't regain hit points until the start of Misty's next turn unless it succeeds on a DC 25 "
               "Constitution saving throw.")
    e_fr = effect(k + "-glare", "Death Glare", icon("ic-glare"), statuses=["frightened"], duration={"rounds": 1},
                  description="<p>Frightened of Misty until the end of your next turn. If you were already frightened by her, "
                              "you are also stunned until the end of your next turn.</p>")
    m.sv("Death Glare (Recharge 5–6)", "wis", 25, [dmg(7, 8, "", ["psychic"])], "One creature within 60 feet that can see "
         "Misty makes a [[/save]] saving throw. On a failure it takes [[/damage extended]] and is frightened until the end of "
         "its next turn; a creature already frightened by her is also stunned. On a success it takes half damage and isn't "
         "frightened. A target may close its eyes before being chosen.", rng_=60, img="ic-glare", uses_=R(5),
         consumption=USE1, effects=[e_fr])
    m.sv("Soul Drain (Recharge 5–6)", "cha", 25, [dmg(8, 8, "", ["necrotic"])], "Replaces Death Glare if both are available. "
         "One creature within 60 feet makes a [[/save]] saving throw, taking [[/damage extended]] on a failure, and Misty "
         "gains 15 temporary hit points. On a success it takes half damage and she gains nothing. No soul contract is "
         "created.", rng_=60, img="ic-drain", uses_=R(5), consumption=USE1)
    m.util("Thornstep (3/Day)", "<p><strong>Bonus Action.</strong> Teleport up to 30 feet to a space she can see. The space she "
           "leaves becomes difficult terrain until the end of her next turn.</p>", img="ic-rose", act=BONUS(), uses_=day(3),
           consumption=USE1)
    m.util("Counterclaim (2/Day)", "<p><strong>Reaction.</strong> When an attacker she can see hits her, impose a −1d8 penalty "
           "on that attack roll, possibly turning it into a miss. The attacker is told the exact penalty.</p>",
           img="ic-sp-objection", act=REACT("she is hit"), uses_=day(2), consumption=USE1, roll=("-1d8", "Counterclaim"))
    m.trait("Legendary Actions", "Misty can take 3 legendary actions, one at a time, at the end of another creature's turn. "
            "She regains spent legendary actions at the start of her turn.", img="ic-crownmark")
    m.util("Uncoil (1 Action)", "Move up to 20 feet without provoking opportunity attacks.", img="ic-rose", act=LEG(1),
           consumption=consume_legact(1))
    m.atk("Needle of Doubt (1 Action)", 17, [dmg(4, 8, 8, ["necrotic"])], kind="ranged", cls="spell", rng_=120,
          img="ic-needle", act=LEG(1), consumption=consume_legact(1),
          desc="Made at disadvantage. Not more than once between Misty's turns.")
    e_sil = effect(k + "-silence", "Seal of Silence", icon("ic-chain"), duration={"rounds": 1},
                   description="<p>You can't take reactions until the end of your next turn.</p>")
    m.sv("Seal of Silence (2 Actions)", "wis", 21, [], "One creature within 30 feet makes a [[/save]] saving throw or can't "
         "take reactions until the end of its next turn.", rng_=30, on_save="none", img="ic-chain", act=LEG(2),
         consumption=consume_legact(2), effects=[e_sil])
    m.util("Nightmare Rebuke (3 Actions)", "Misty casts <em>bestow curse</em> at 3rd level against one target within touch "
           "reach without expending a daily use. Unavailable while the Seal of Consent is suppressed.", img="ic-hex",
           act=LEG(3), consumption=consume_legact(3))
    if phase2:
        e_chain = effect(k + "-chainwrit", "Chain Writ", icon("ic-chain"), statuses=["restrained"], duration={"rounds": 1},
                         description="<p>Restrained until the end of your next turn. Action: DC 19 Athletics or Acrobatics to escape.</p>")
        m.sv("Lair: Chain Writ", "dex", 19, [], "One 20-foot square: each creature makes a [[/save]] saving throw or is "
             "restrained until the end of its next turn. Choose one lair action per round, not all three.",
             area=("square", 20), on_save="none", img="ic-chain", act=LAIR, effects=[e_chain])
        m.sv("Lair: Memory Gale", "wis", 19, [dmg(3, 8, "", ["psychic"])], "Creatures in a 20-foot radius make a [[/save]] "
             "saving throw, taking [[/damage extended]] and losing reactions until their next turn on a failure, or half "
             "damage on a success.", area=("radius", 20), img="ic-sp-memory", act=LAIR)
        m.heal("Lair: Heartstone Pulse", "10", "Misty regains 10 hit points. Disabled if the Heartstone's ward has been "
               "disrupted or the Hourglass of True Dawn delays this pulse.", img="ic-heartstone", act=LAIR)
    return m


MIS = dict(ctype="fiend", subtype="hag", alignment="neutral evil", cr=30, ac=20, speed=30, fly=40, hover=True,
           abilities=(14, 18, 18, 22, 22, 26), saves=("con", "int", "wis", "cha"),
           skills={"arc": 15, "dec": 17, "ins": 15, "prc": 15, "per": 17}, dr=("cold", "fire", "necrotic", "psychic"),
           di=("poison",), ci=("charmed", "frightened", "poisoned"), senses={"truesight": 60, "darkvision": 120},
           langs=("common", "infernal", "abyssal"), lang_custom="telepathy 120 ft.", legact=3, legres=3,
           spellcasting="cha", spell_level=20)
make(F4, "misty", "Misty, Hell Hag Queen of the Pyric Triune", misty_block("misty"), hp=244, hp_formula="", **MIS,
     bio=P("Queen of Barbed Chains. A campaign-scale political adversary, not a mid-level miniboss: the true CR 30 fight is "
           "an optional level-17 capstone. <em>'The first lie in every contract is the notion that only one party wants it.'</em>"))
make(F4, "misty-unbound", "Misty, Unbound (Resting Place)", misty_block("misty-unbound", True), hp=144, hp_formula="",
     lair=True, **MIS, bio=P("The mythic second phase in her resting place. <em>'You have mistaken my courtroom for my home. "
                            "Shall I show you the difference?'</em>"))
note("<strong>Misty</strong> keeps her established numbers (CR 30, AC 20, 244 HP, Cha 26, DC 25, +17, 144-HP mythic "
     "restoration). Her attacks, spells and lair actions are the Appendix A campaign adaptation. If you have her original "
     "actor, use it and keep only the scene procedures; do not stack the two.")

m = Mon("child")
m.trait("Shared Initiative", "Both Children act together on initiative 10, attack separately and can't summon. Each vanishes "
        "if Misty reaches 0 HP for the second time.")
m.atk("Hellborn Bite", 9, [dmg(2, 8, 4, ["psychic"])], img="ic-talon")
make(F4, "child-of-hell", "Child of Hell", m, size="sm", ctype="fiend", alignment="neutral evil", cr=5, ac=16, hp=36,
     hp_formula="8d6+8", speed=30, climb=30, abilities=(12, 18, 12, 8, 12, 14), di=("poison",), ci=("poisoned",),
     senses={"darkvision": 120}, lang_custom="understands Infernal")

m = Mon("isolde")
m.trait("Pledged Memories", "Misty's sponsored contestant. She has pledged her future memories, but not her soul. Sympathy, "
        "rivalry or rescue.")
m.multi("Isolde makes two Seven-Mask Dagger attacks.")
m.atk("Seven-Mask Dagger", 9, [dmg(2, 4, 5, ["piercing"]), dmg(2, 6, "", ["psychic"])], img="ic-sabre")
m.util("Change Mask", "<p><strong>Bonus Action.</strong> Isolde changes mask and appearance (<em>disguise self</em>) and moves "
       "10 feet without provoking opportunity attacks.</p>", img="ic-hex", act=BONUS())
make(F5, "isolde", "Isolde of Seven Masks", m, ctype="humanoid", subtype="human", alignment="neutral", cr=8, ac=16,
     ac_calc="flat", hp=104, hp_formula="16d8+32", speed=30, abilities=(10, 20, 14, 14, 14, 18), saves=("dex", "cha"),
     skills={"dec": 8, "ste": 9, "prf": 8, "ins": 6}, langs=("common", "infernal", "elvish"), disposition=0)
note("<strong>Isolde of Seven Masks</strong>, <strong>Corda Kain</strong> and <strong>Magistrate Khel</strong> appear in the "
     "Act III rival cast without stat blocks; each was built at CR 8–10 for level-13 arenas.")

# =========================================================================== RIVALS (Appendix B)
m = Mon("vexa")
m.trait("Public Challenge", "She refuses to harm an uninvolved witness, even if it costs her a Crown Mark. In level-17 arenas "
        "use 190 HP and +1 to attack and damage.")
m.multi("Vexa makes three Sabre attacks.")
m.atk("Sabre", 10, [dmg(1, 8, 6, ["slashing"])], img="ic-sabre")
m.atk("Riposte", 10, [dmg(1, 8, 6, ["slashing"])], img="ic-sabre", act=REACT("missed by a melee attack (once per round)"))
m.util("Duelist's Step (3/Day)", "<p><strong>Bonus Action.</strong> Move 15 feet without provoking opportunity attacks.</p>",
       img="ic-sp-duel", act=BONUS(), uses_=day(3), consumption=USE1)
make(F5, "vexa-corven", "Vexa Corven, Independent Duelist", m, ctype="humanoid", subtype="human", alignment="chaotic good",
     cr=11, ac=18, ac_calc="flat", hp=155, hp_formula="22d8+66", speed=35, abilities=(14, 22, 16, 12, 14, 16),
     saves=("dex", "wis", "cha"), skills={"acr": 10, "ath": 6, "itm": 7, "prf": 7}, langs=("common",), disposition=0,
     bio=P("Leader of the Ashclad Petitioners. Dry, capable, hates pomp. Her dream: rule from a position earned rather than "
           "inherited."))

m = Mon("ashclad")
m.multi("The petitioner makes two Spear attacks.")
m.atk("Spear", 5, [dmg(1, 8, 3, ["piercing"])], img="ic-glaive")
make(F5, "ashclad-petitioner", "Ashclad Petitioner", m, ctype="humanoid", alignment="any", cr=2, ac=15, ac_calc="flat",
     hp=45, hp_formula="7d8+14", speed=30, abilities=(16, 13, 14, 10, 11, 10), langs=("common",), disposition=0)

m = Mon("kordren")
m.trait("Agenda", "Maintain Avernus's war readiness, which can be argued as reasonable Dominion even when the methods are brutal.")
m.multi("Kordren makes two Glaive attacks.")
m.atk("Glaive", 11, [dmg(2, 10, 6, ["slashing"]), dmg(1, 8, "", ["fire"])], reach=10, img="ic-glaive")
m.util("War Decree (Recharge 5–6)", "Allies within 30 feet gain 10 temporary hit points and may move up to 15 feet. It "
       "grants no attacks.", img="ic-battle", uses_=R(5), consumption=USE1)
m.util("Hold the Line", "<p><strong>Reaction.</strong> Reduce an attack's damage against an adjacent ally by 15.</p>",
       img="ic-guardian", act=REACT("an adjacent ally is hit"))
make(F5, "marshal-kordren", "Marshal Kordren, Zariel's War-Host Proxy", m, ctype="fiend", subtype="devil",
     alignment="lawful evil", cr=13, ac=19, hp=185, hp_formula="22d8+88", speed=30, fly=40, abilities=(22, 14, 18, 14, 16, 16),
     saves=("str", "con", "wis"), dr=("fire", "necrotic"), di=("poison",), senses={"darkvision": 120},
     langs=("infernal", "common"))

m = Mon("morn")
m.trait("Agenda", "Bel wants a competent industrial ruler; Morn wants machinery rather than souls to bear the cost of Hell's wars.")
m.multi("Morn makes two Brass Hammer attacks.")
m.atk("Brass Hammer", 10, [dmg(2, 10, 5, ["bludgeoning"])], img="ic-hammer")
m.sv("Contracted Retaliation", "str", 17, [], "<strong>Reaction.</strong> When struck within 5 feet, the attacker must "
     "succeed on a [[/save]] saving throw or be pushed 10 feet.", on_save="none", img="ic-hammer",
     act=REACT("struck by a creature within 5 feet"))
m.util("Overdrive (1/Day)", "For two rounds, gain 10 temporary hit points at the start of each turn; afterwards speed is "
       "reduced by 10 feet for one round.", img="ic-embers", uses_=day(1), consumption=USE1)
make(F5, "brass-factor-morn", "Brass Factor Morn, Bel's Sponsored Champion", m, ctype="humanoid", subtype="dwarf",
     alignment="lawful neutral", cr=12, ac=18, ac_calc="flat", hp=165, hp_formula="22d8+66", speed=30,
     abilities=(20, 10, 18, 16, 12, 10), saves=("con", "int"), langs=("common", "dwarvish", "infernal"), disposition=0)

m = Mon("corda")
m.trait("Narrow Proxy Mandate", "She must obey a narrow proxy mandate from Zariel. She can be defeated by proving she exceeded "
        "her sponsor's authority.")
m.multi("Corda makes three Steel Brief attacks.")
m.atk("Steel Brief", 9, [dmg(1, 10, 5, ["slashing"])], img="ic-sabre")
m.util("Parry", "<p><strong>Reaction.</strong> +3 AC against one melee attack she can see.</p>", img="ic-writshield",
       act=REACT("hit by a melee attack"))
make(F5, "corda-kain", "Corda Kain, Zariel's Steel Advocate", m, ctype="humanoid", subtype="human", alignment="lawful neutral",
     cr=10, ac=19, ac_calc="flat", hp=150, hp_formula="20d8+60", speed=30, abilities=(20, 14, 16, 14, 12, 16),
     saves=("str", "con", "cha"), skills={"ath": 9, "prf": 7}, langs=("common", "infernal"), disposition=0)

m = Mon("khel")
m.trait("Competitive but Practical", "Needs supplies to keep an outpost alive. Capable of compromise.")
m.multi("Khel makes two Calibrated Pistol shots.")
m.atk("Calibrated Pistol", 8, [dmg(2, 6, 4, ["piercing"])], kind="ranged", rng_=60, img="ic-bolt")
m.util("Engineer's Command", "<p><strong>Bonus Action.</strong> One allied construct within 60 feet moves up to half its "
       "speed.</p>", img="ic-golem", act=BONUS())
make(F5, "magistrate-khel", "Magistrate Khel, Bel's Engineer-General", m, ctype="humanoid", subtype="human",
     alignment="lawful neutral", cr=8, ac=17, ac_calc="flat", hp=120, hp_formula="16d8+48", speed=30,
     abilities=(12, 16, 16, 20, 14, 12), saves=("int", "wis"), skills={"arc": 9, "inv": 9}, langs=("common", "infernal", "dwarvish"),
     disposition=0)

# =========================================================================== OBJECTS
def obj(key, name, img, ac, hp, desc, *, di=("poison", "psychic"), threshold=0):
    m = Mon(key)
    m.trait("Object", desc, img=img)
    a = npc(key, name, img=icon(img), token=icon(img), size="med", ctype="", alignment="", cr=0, ac=ac, ac_calc="flat",
            hp=hp, speed=0, abilities=(10, 1, 10, 1, 1, 1), di=di, ci=("blinded", "charmed", "deafened", "frightened",
                                                                       "paralyzed", "petrified", "poisoned", "stunned"),
            items=m.items, disposition=0)
    if threshold:
        a["system"]["attributes"]["hp"]["dt"] = threshold
    a["system"]["details"]["type"]["custom"] = "Object"
    return put(F7, a)


obj("heartstone", "Misty's Heartstone", "ic-heartstone", 20, 70,
    "AC 20, 70 HP, damage threshold 10, immune to poison and psychic. Not targetable until two of the three witness-seals are "
    "suppressed (or a valid superior court order opens the screen). The Blackthorn Shears sever its tether once the two-seal "
    "condition is met. Breaking it while Misty lives prevents later refuge in it; it deals her no damage.", threshold=10)
obj("championship-stamp", "The Championship Stamp", "ic-stamp", 17, 40,
    "Prints counterfeit warrants. Destroying it ends the Vacant King's Forged Sovereignty and stuns the King until the end "
    "of its next turn.")
obj("command-pylon", "Command Pylon", "ic-glassheart", 16, 30,
    "Disable with damage or a DC 17 Arcana or thieves' tools check (action). Two pylons hold Hollis's stolen command seal "
    "over Janella's warders.")
obj("soul-siphon", "The Soul Siphon", "ic-sp-memory", 18, 45,
    "Disable with damage or a DC 19 Arcana check. One of three raid objectives in the Thorn Reliquary.")
note("Battlefield objects (Heartstone, Stamp, Pylons, Siphon) are NPC actors with object immunities so they can be "
     "targeted, damaged and tracked on the scene.")

FOLDERS = {f: FOLDERS[f] for f in (F1, F2, F3, F4, F5, F6, F7)}


# The Redline Run interlude (vehicles, repossession crew, coin broker)
import redline as _RL
_RL.build_actors()
