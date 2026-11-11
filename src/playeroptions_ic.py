"""The three new subclasses of Interplanal Champions (Book II, Sections 2-4) as dnd5e 5.3.3 subclass items."""
from lib5e import *
from scriptorium_v2 import cf, grant, opt_uuid


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


SPECIAL = activation("special", None)
U = consume_item_uses()

# ============================================================== WARLOCK: THE RUBY COURT
W = "Warlock"
e_term = effect("ic-minor-term", "Minor Term", icon("ic-term"), duration={"rounds": 1},
                description="<p>You accepted a Minor Term from a Ruby Court warlock. While you abide by it, once before it "
                            "expires you may add 1d6 to one attack roll, saving throw or ability check after rolling but before "
                            "the outcome is announced. Knowingly break it and the die disappears.</p>")
r1 = cf("rc-mutual", "Clause of Mutual Aid", P(
    "You learn Infernal and gain proficiency in Investigation or Persuasion.",
    "As a bonus action, you may offer one willing creature you can see within 30 feet a <strong>Minor Term</strong>: a feasible, "
    "clearly stated action to perform or avoid before the start of your next turn. The creature knows the entire effect and may "
    "refuse without consequence. While it accepts and abides by the Term, once before it expires the creature may add "
    "[[/r 1d6]] to one attack roll, saving throw or ability check after rolling but before the outcome is announced. If it "
    "knowingly breaks the Term, the unused die disappears; there is no involuntary soul loss or damage.",
    "You may offer terms a number of times equal to your proficiency bonus per long rest; only one of your terms may be active at "
    "a time. This is neither concentration nor a spell."), img="ic-term", cls=W, level=1,
    uses_=uses("@prof", ["lr"]), effects=[e_term],
    activities=[utility("rc-mutual", 0, name="Offer a Minor Term", act=activation("bonus", 1), consumption=U, rng_=rng(30),
                        tgt=target(1, "willing"), effects=[e_term["_id"]], roll=("1d6", "Term die"))])
r6 = cf("rc-consideration", "Consideration Received", P(
    "When a hostile creature that has separately accepted a Minor Term from you knowingly breaks it within 60 feet, you can use a "
    "reaction to deal [[/damage 2d8 type=psychic]] and gain temporary hit points equal to your Charisma modifier plus your "
    "proficiency bonus. You may use this reaction a number of times equal to your Charisma modifier (minimum once) per long "
    "rest, and no creature can trigger it more than once per long rest. Friendly characters never trigger this damage through "
    "playful self-default.",
    "In addition, you have advantage on ability checks to locate a deliberate contradiction in an authentic written agreement "
    "you have been allowed to inspect for 10 minutes; this does not substitute for the evidence needed to win a hearing."),
    img="ic-consideration", cls=W, level=6, uses_=uses("max(1, @abilities.cha.mod)", ["lr"]),
    activities=[damage_act("rc-consideration", 0, name="Breach Penalty", parts=[dmg(2, 8, "", ["psychic"])],
                           act=activation("reaction", 1), consumption=U, rng_=rng(60), tgt=target(1, "creature")),
                heal_act("rc-consideration-t", 1, formula_part=dmg_formula("@abilities.cha.mod + @prof"), temp=True,
                         name="Consideration (temp HP)", act=SPECIAL, tgt=target("", "self"))])
e_res = effect("ic-reserved", "Reserved Rights", icon("ic-reserved"), transfer=True,
               changes=[("system.traits.dr.value", 2, "psychic")],
               description="<p>Resistance to psychic damage; advantage on saves against being charmed or frightened by fiends.</p>")
r10 = cf("rc-reserved", "Reserved Rights", P(
    "You gain resistance to psychic damage and advantage on saves against being charmed or frightened by fiends.",
    "Once per long rest, when you fail a saving throw against a spell or magical effect, you may use your reaction to reroll it. "
    "You must use the second result. The reroll is a timely objection, not retrospective refusal of an already completed "
    "lawful bargain."), img="ic-reserved", cls=W, level=10, uses_=uses(1, ["lr"]), effects=[e_res],
    activities=[utility("rc-reserved", 0, name="Timely Objection (reroll)", act=activation("reaction", 1), consumption=U)])
e_fn = effect("ic-final-notice", "Final Notice", icon("ic-final-notice"), statuses=["restrained"], duration={"seconds": 60},
              description="<p>Restrained in spectral filing chains. Repeat the Charisma save at the end of each turn.</p>")
r14 = cf("rc-final", "Final Notice", P(
    "As an action, choose a creature within 60 feet that can hear or see you. It makes a Charisma saving throw against your "
    "warlock spell save DC. On a failure, it takes [[/damage 6d10 type=psychic]] and is &Reference[restrained] in spectral filing "
    "chains for up to 1 minute. It repeats the save at the end of each turn, ending the restraint on a success. On a success, it "
    "takes half damage and is not restrained.",
    "If the target is currently bound by a genuinely accepted Minor Term from you and knowingly breached it, the initial damage "
    "increases by 2d10. Once used, this feature cannot be used again until a long rest. This is a magical attack, not a contract "
    "granting your patron title to a soul."), img="ic-final-notice", cls=W, level=14, uses_=uses(1, ["lr"]), effects=[e_fn],
    activities=[save("rc-final", 0, ability="cha", spell=True, parts=[dmg(6, 10, "", ["psychic"])], rng_=rng(60),
                     tgt=target(1, "creature"), consumption=U, effects=[e_fn["_id"]], name="Final Notice"),
                damage_act("rc-final-b", 1, name="Breached Term (+2d10)", parts=[dmg(2, 10, "", ["psychic"])], act=SPECIAL)])
RUBY_FEATURES = [r1, r6, r10, r14]
RUBY = {"_id": fid("sub:ruby-court"), "name": "The Ruby Court", "type": "subclass", "img": icon("ic-ruby"), "sort": 0,
        "folder": None, "effects": [], "flags": {}, "_stats": STATS,
        "system": {"description": {"value": P(
            "<em>Otherworldly Patron.</em> Warlocks of the Ruby Court bargain for the authority to witness, suspend and enforce "
            "specific promises. They may work for Asmodeus, copy his methods without loyalty, or use Hell's law against Hell "
            "itself. Their magic cannot conjure soul ownership from an enemy who has not agreed to it.",
            "<strong>Expanded Spell List.</strong> 1st <em>command, sanctuary</em>; 2nd <em>zone of truth, hold person</em>; 3rd "
            "<em>counterspell, sending</em>; 4th <em>banishment, freedom of movement</em>; 5th <em>geas, wall of force</em>. These "
            "are options on the warlock spell list, not extra known spells (2024 tables may treat them as always prepared).",
            "<strong>2024 play.</strong> Grant the 1st-level feature at level 3 with the expanded spells; later levels unchanged.",
            "<strong>Design ceiling.</strong> Short-lived attack/save support, one optional control ultimate, no automatic mind "
            "control, no extra spell slots and no involuntary soul transfer."), "chat": ""},
            "source": SOURCE, "identifier": "the-ruby-court", "classIdentifier": "warlock",
            "advancement": [grant(1, [opt_uuid(r1)]), grant(6, [opt_uuid(r6)]), grant(10, [opt_uuid(r10)]),
                            grant(14, [opt_uuid(r14)])], "spellcasting": {"progression": "none", "ability": ""}}}

# ============================================================== BARBARIAN: PATH OF THE BLOOD-PRICE
B = "Barbarian"
b3 = cf("bp-covenant", "Rage Covenant", P(
    "When you enter a Rage, speak one <strong>Battle Vow</strong> whose condition you can reasonably fulfil: protect a named "
    "willing ally within 30 feet, hold a location you can see, or engage a declared enemy without deliberately fleeing. The vow "
    "lasts until your Rage ends.",
    "On each of your turns while raging, if you have not knowingly broken it, the first creature you hit with a Strength-based "
    "melee weapon attack takes an extra 1d6 necrotic or fire damage (your choice when you vow). This increases to 1d8 at "
    "barbarian level 10. If you knowingly break the vow, you lose this extra damage until you start a new Rage; your Rage itself "
    "does not end. The vow does not magically force your actions or bind any ally's soul."), img="ic-vow", cls=B, level=3,
    activities=[damage_act("bp-covenant", 0, name="Vow Damage (necrotic)", act=SPECIAL,
                           parts=[dmg_formula("1d(6 + 2 * floor(@classes.barbarian.levels / 10))", ["necrotic"])]),
                damage_act("bp-covenant-f", 1, name="Vow Damage (fire)", act=SPECIAL,
                           parts=[dmg_formula("1d(6 + 2 * floor(@classes.barbarian.levels / 10))", ["fire"])])])
b6 = cf("bp-guardian", "Collateral Guardian", P(
    "While raging, when a willing ally within 5 feet is damaged by an attack, you can use your reaction to reduce the damage by "
    "1d10 + your Constitution modifier + your Rage Damage bonus. You take psychic damage equal to half the damage prevented, "
    "rounded down; Rage resistance can't reduce it. You may use this feature a number of times equal to your proficiency bonus "
    "per long rest. The ally knows you are assuming the cost and may decline."), img="ic-guardian", cls=B, level=6,
    uses_=uses("@prof", ["lr"]),
    activities=[utility("bp-guardian", 0, name="Take the Blow", act=activation("reaction", 1), consumption=U,
                        roll=("1d10 + @abilities.con.mod + @scale.barbarian.rage-damage", "Damage prevented"),
                        tgt=target(1, "ally"), rng_=rng(5))])
b10 = cf("bp-witness", "Witness to the Oath", P(
    "When you begin Rage Covenant, you may designate one willing ally within 30 feet as a <strong>Witness</strong>. While your "
    "Rage lasts and you are conscious, that ally has advantage on saving throws against being frightened.",
    "Once during each Rage, when the Witness misses an attack against the foe named by your Battle Vow, the Witness may add your "
    "Rage Damage bonus to the attack roll, potentially turning the miss into a hit. The Witness can't gain this benefit while "
    "incapacitated, and may withdraw at any time."), img="ic-witness", cls=B, level=10)
b14 = cf("bp-price", "The Price Comes Due", P(
    "While raging, when a hostile creature within 30 feet damages your designated Witness or an ally named by your Battle Vow, "
    "you may use your reaction to move up to half your speed toward that enemy without provoking opportunity attacks and make one "
    "melee weapon attack against it, provided it comes within reach. On a hit, deal an extra [[/damage 2d8 type=necrotic]].",
    "You may use this feature a number of times equal to your proficiency bonus per long rest. You cannot use it during the same "
    "reaction as Collateral Guardian."), img="ic-pricedue", cls=B, level=14, uses_=uses("@prof", ["lr"]),
    activities=[damage_act("bp-price", 0, name="The Price (extra damage)", act=activation("reaction", 1), consumption=U,
                           parts=[dmg(2, 8, "", ["necrotic"])])])
BLOOD_FEATURES = [b3, b6, b10, b14]
BLOOD = {"_id": fid("sub:blood-price"), "name": "Path of the Blood-Price", "type": "subclass", "img": icon("ic-bloodprice"),
         "sort": 0, "folder": None, "effects": [], "flags": {}, "_stats": STATS,
         "system": {"description": {"value": P(
             "<em>Primal Path (3rd, 6th, 10th and 14th level, for 2014 and 2024 timing).</em> These warriors swear measurable "
             "combat vows and draw power from the peril of keeping them. A Blood-Price barbarian might defend innocent people "
             "out of fierce devotion or serve Asmodeus as an honour-bound executioner.",
             "<strong>Design ceiling.</strong> Rage Covenant's extra damage resembles established barbarian bonus-damage "
             "subclasses; reaction defence trades personal hit points and an action-economy slot for protection. The oath's "
             "penalty is limited and disclosed."), "chat": ""},
             "source": SOURCE, "identifier": "path-of-the-blood-price", "classIdentifier": "barbarian",
             "advancement": [grant(3, [opt_uuid(b3)]), grant(6, [opt_uuid(b6)]), grant(10, [opt_uuid(b10)]),
                             grant(14, [opt_uuid(b14)])], "spellcasting": {"progression": "none", "ability": ""}}}

# ============================================================== DRUID: CIRCLE OF ASHEN COVENANTS
DR = "Druid"
e_acc = effect("ic-ashen-accord", "Ashen Accord", icon("ic-accord"), duration={"seconds": 86400},
               description="<p>Bearer of an Ashen Accord. Within 60 feet of the druid, they can use their reaction to reduce "
                           "damage you take and grant temporary hit points.</p>")
d2a = cf("ac-grove", "Witness of the Grove", P(
    "You gain proficiency in Insight or Nature, and learn Infernal or Sylvan.",
    "As a 1-minute rite, you may place an <strong>Ashen Accord</strong> on one willing creature you touch. It lasts until your "
    "next long rest, until dismissed by either party (no action), or until another Ashen Accord replaces it. While within 60 "
    "feet of you, when the bearer takes damage you may use your reaction to reduce the damage by 1d8 + your Wisdom modifier and "
    "grant the bearer temporary hit points equal to your proficiency bonus. You may use the reduction a number of times equal to "
    "your proficiency bonus per long rest; no creature is compelled to accept it."), img="ic-accord", cls=DR, level=2,
    uses_=uses("@prof", ["lr"]), effects=[e_acc],
    activities=[utility("ac-rite", 0, name="Ashen Accord (1-minute rite)", act=activation("minute", 1), rng_=rng("", "touch"),
                        tgt=target(1, "willing"), effects=[e_acc["_id"]]),
                utility("ac-reduce", 1, name="Shield the Bearer", act=activation("reaction", 1), consumption=U, rng_=rng(60),
                        roll=("1d8 + @abilities.wis.mod", "Damage reduced")),
                heal_act("ac-temp", 2, formula_part=dmg_formula("@prof"), temp=True, name="Bearer's Temp HP", act=SPECIAL)])
d2b = cf("ac-warden", "Ash Warden Spirit", P(
    "As a bonus action you can expend one use of Wild Shape to manifest an <strong>Ash Warden Spirit</strong> in an unoccupied "
    "space within 30 feet for 10 minutes.",
    "<strong>Ash Warden Spirit.</strong> Small Elemental; AC 13 + your proficiency bonus; HP 5 + five times your druid level; "
    "speed 30 ft., fly 20 ft. (hover); resistance to fire; immune to the poisoned condition; attack bonus equal to your spell "
    "attack modifier. It acts on your initiative immediately after your turn. It can move and Dodge freely; if you spend a bonus "
    "action to command it, it instead moves and makes one <strong>Ashen Touch</strong> attack (1d8 + your proficiency bonus fire "
    "damage; 2d8 + PB from druid level 10), Helps, or Dashes. It can't cast spells, carry large objects or make opportunity "
    "attacks. It vanishes at 0 HP, when dismissed, or when the duration expires. You can't have more than one."),
    img="ic-warden", cls=DR, level=2,
    activities=[utility("ac-summon", 0, name="Manifest the Spirit", act=activation("bonus", 1), rng_=rng(30),
                        consumption={"targets": [{"type": "itemUses", "target": "", "value": "1",
                                                  "scaling": {"mode": "", "formula": ""}}],
                                     "scaling": {"allowed": False, "max": ""}, "spellSlot": True}),
                attack("ac-touch", 1, kind="melee", classification="spell", ability="", reach=5, name="Ashen Touch (commanded)",
                       act=activation("bonus", 1),
                       parts=[dmg_formula("(1 + floor(@classes.druid.levels / 10))d8 + @prof", ["fire"])])])
_t = d2b["system"]["activities"]
_k = [k for k, v in _t.items() if v["type"] == "attack"][0]
_t[_k]["attack"]["ability"] = "spellcasting"
d2b["system"]["activities"][[k for k, v in _t.items() if v["type"] == "utility"][0]]["consumption"]["targets"] = []
d6 = cf("ac-remedy", "Remedy of the Root", P(
    "When a creature you can see within 60 feet harms the bearer of your Ashen Accord, you can use your reaction to impose a "
    "−1d6 penalty on one attack roll that creature makes before the end of its next turn; the penalty must be declared before "
    "that roll. If you use this reaction, the Accord bearer may immediately move 5 feet without provoking opportunity attacks. "
    "You may use the reaction a number of times equal to your Wisdom modifier (minimum once) per long rest. It competes with "
    "Witness of the Grove for your reaction."), img="ic-remedy", cls=DR, level=6, uses_=uses("max(1, @abilities.wis.mod)", ["lr"]),
    activities=[utility("ac-remedy", 0, name="Remedy of the Root", act=activation("reaction", 1), consumption=U, rng_=rng(60),
                        roll=("-1d6", "Penalty"))])
e_emb = effect("ic-embers", "Covenant of Embers", icon("ic-embers"), transfer=True, changes=[("system.traits.dr.value", 2, "fire")],
               description="<p>Resistance to fire damage.</p>")
d10 = cf("ac-embers", "Covenant of Embers", P(
    "You gain resistance to fire damage. When your Ash Warden Spirit is within 30 feet of the bearer of your Ashen Accord, the "
    "bearer has advantage on saving throws against being frightened. When the spirit scores a critical hit, its target can't "
    "make opportunity attacks until the end of the target's next turn. Duplicate spirit bonuses don't stack."),
    img="ic-embers", cls=DR, level=10, effects=[e_emb])
e_court = effect("ic-court-ash", "Court of Returning Ash", icon("ic-court-ash"), duration={"seconds": 60},
                 description="<p>A 30-foot-radius grove of black trees (concentration). Included creatures reduce the first "
                             "damage they take each round in the area by 2d8. Enemies starting their turn inside make a Wisdom "
                             "save or have their speed halved; the grove is difficult terrain for enemies.</p>")
d14 = cf("ac-court", "Court of Returning Ash", P(
    "As an action, you raise a 30-foot-radius grove of black trees centred on yourself for up to 1 minute, as if concentrating on "
    "a spell. You may include or exclude any willing creatures you can see when you activate it.",
    "For the duration, the first time each round that an included creature takes damage within the area, reduce that damage by "
    "2d8. An enemy that starts its turn within the grove must make a Wisdom save against your spell save DC or have its speed "
    "halved until the start of its next turn. The grove is stationary and counts as difficult terrain for enemies; it ends if "
    "your concentration ends. Once used, you can't use this feature again until a long rest. It does not nullify valid signed "
    "agreements or compel an enemy to contract."), img="ic-court-ash", cls=DR, level=14, uses_=uses(1, ["lr"]), effects=[e_court],
    activities=[utility("ac-court", 0, name="Raise the Grove", consumption=U, effects=[e_court["_id"]],
                        tgt=target("", "", "radius", 30), duration={"concentration": True, "value": "1", "units": "minute",
                                                                    "special": "", "override": False}),
                utility("ac-court-r", 1, name="Grove Reduction (2d8)", act=SPECIAL, roll=("2d8", "Damage reduced")),
                save("ac-court-s", 2, ability="wis", spell=True, on_save="none", act=SPECIAL, name="Slowing Grove",
                     tgt=target(1, "creature"))])
import ashen_forms as AF
d2c = cf("ac-forms", "Ashen Forms", AF.RULES + "<h4>The Ashen Forms</h4>" + AF.table_html(), img="ic-ashen", cls=DR, level=2)
d10b = cf("ac-infernal", "Infernal Form", AF.INFERNAL, img="ic-ashen", cls=DR, level=10,
          activities=[utility("ac-infernal", 0, name="Infernal Form (2 Wild Shape uses)")])
ASH_FEATURES = [d2a, d2b, d2c, d6, d10, d10b, d14]
ASHEN = {"_id": fid("sub:ashen-covenants"), "name": "Circle of Ashen Covenants", "type": "subclass", "img": icon("ic-ashen"),
         "sort": 0, "folder": None, "effects": [], "flags": {}, "_stats": STATS,
         "system": {"description": {"value": P(
             "<em>Druid Circle (2nd, 6th, 10th and 14th level; 2024 druids gain the 2nd-level features at 3rd).</em> The Circle "
             "teaches that every harvest carries a debt, every flame nourishes ash, and every oath must have a season in which "
             "it ends. Some druids venerate Asmodeus as an embodiment of cosmic exchange. Others study his contracts precisely to "
             "keep natural communities out of them.",
             "<strong>Design ceiling.</strong> The spirit's attack requires a bonus action and does not combine with repeated "
             "Wild Shape strikes; the reactive mitigation competes for the same reaction; the capstone uses concentration."),
             "chat": ""},
             "source": SOURCE, "identifier": "circle-of-ashen-covenants", "classIdentifier": "druid",
             "advancement": [grant(2, [opt_uuid(d2a), opt_uuid(d2b), opt_uuid(d2c)]), grant(6, [opt_uuid(d6)]), grant(10, [opt_uuid(d10), opt_uuid(d10b)]),
                             grant(14, [opt_uuid(d14)])], "spellcasting": {"progression": "none", "ability": ""}}}

import soulforged as SF
SUBCLASSES = [RUBY, BLOOD, ASHEN, SF.SOULFORGED]
FEATURES = {"The Ruby Court — Features": RUBY_FEATURES, "Path of the Blood-Price — Features": BLOOD_FEATURES,
            "Circle of Ashen Covenants — Features": ASH_FEATURES,
            "The Soulforged — Features": SF.FEATURES, "The Soulforged — Construct Imprints": SF.IMPRINT_ITEMS}
SUB_NOTES = [
    "<strong>The Ruby Court, Path of the Blood-Price, Circle of Ashen Covenants</strong> follow Book II exactly; each feature is "
    "an item granted by advancement at its listed level, with activities for the dice it rolls. Rage Covenant's die scales by "
    "formula (d6, then d8 at barbarian 10); the Ash Warden's touch scales at druid 10.",
    "The Ash Warden Spirit is run as a feature activity rather than a summoned actor, matching the Book II rule that it acts "
    "only on a bonus-action command and can't make opportunity attacks.",
    "Ashen Forms: the Circle wild-shapes into fiends on the Circle of the Moon's challenge-rating scale, with a CR 5 "
    "Infernal Form at 10th level. The seven SRD fiends (Lemure, Dretch, Imp, Quasit, Hell Hound, Bearded Devil, Barbed Devil) "
    "and seven original fiends of Avernus are actors in the folder Ashen Forms (Wild Shape), visible to players so a druid "
    "can drag one onto their token to transform. Fiends from other official books are listed by book and page only.",
    SF.SUB_NOTE]
