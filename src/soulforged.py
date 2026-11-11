"""Artificer: The Soulforged (by Asmo) for Interplanal Champions.

A complete artificer specialist (3rd, 5th, 9th and 15th level) built on the Soul Furnace Codex: two servitor frames,
twelve Construct Imprints, soul generation tables, Forms SF-01 and SF-12, and DM guidance.
The artificer class itself is not in the SRD; the subclass works with any artificer class item whose identifier is
"artificer". Balance decisions are recorded in SUB_NOTE.
"""
from lib5e import *
from scriptorium_v2 import cf, grant, opt_uuid, spell_uuid_by_name, ALWAYS

P = lambda *x: "".join(f"<p>{y}</p>" for y in x)
UL = lambda *x: "<ul>" + "".join(f"<li>{y}</li>" for y in x) + "</ul>"
AR = "Artificer"
SPECIAL = activation("special", None)
LV = "@classes.artificer.levels"
QUOTE = ("“I gave them bodies of iron, hearts of hellfire, and voices that will not shut up. I have created life. "
         "Unfortunately, life has opinions.”")


def T(head, rows):
    return ('<table class="rc-table"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")


def BOX(t, body):
    return f'<div class="rc-box"><h4>{t}</h4>{body}</div>'


# =============================================================================== INTRODUCTION
INTRO = P(
    f"<em>{QUOTE}</em>",
    "Among the infernal manufactories of Avernus, few artificers are as feared, coveted or morally controversial as the "
    "Soulforged. Where ordinary golemancers animate constructs with arcane formulae, a Soulforged artificer gives a mechanical "
    "body a conscious pilot: a mortal soul imprisoned in a soul coin.",
    "These souls keep their memories, personalities, convictions, alignments, ambitions and voices. A once-proud paladin might "
    "inhabit a hulking iron guardian. A cowardly thief could wake inside a spider-legged reconnaissance construct. A bitter "
    "surgeon might discover that their new body has six mechanical arms and a deeply inconvenient number of scalpels.",
    "The artificer builds the body, installs its infernal furnace and engraves a magical <strong>Directive Binding</strong>. The "
    "soul takes control of the machine's movement and senses, and while bound it must obey the artificer's explicit, "
    "achievable instructions. But compulsory obedience is not compulsory agreement. A construct may insult its creator, protest "
    "cruel orders, demand maintenance, argue strategy, or hold long philosophical discussions about the nature of personhood. "
    "Because every soul has a different history, two identical constructs can behave and fight in completely different ways.",
    "Some artificers treat their creations as property. Others treat them as companions, employees, prisoners, or the "
    "beginnings of a new form of life. The question at the heart of the tradition is not whether the artificer <em>can</em> "
    "control a soul. It is whether they should.")
IDENTITY = ('<table class="rc-table"><tbody>' + "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td></tr>" for a, b in [["Primary role", "Construct commander, support and battlefield control"],
                        ["Secondary role", "Crafting, investigation, infernal engineering"],
                        ["Primary ability", "Intelligence"], ["Unique resources", "Soul coins, Resonance Sparks, Engine Heat"],
                        ["Rules", "A specialist for the 2014 artificer; use the same levels with the revised artificer"]]) + "</tbody></table>")
PROGRESSION = T(["Artificer level", "Features"], [
    ["3rd", "Soulforge Engineering, Infernal Servitor, Directive Binding, Soulforged Spells"],
    ["5th", "Soul-Etched Enchantments, Resonant Conduit"],
    ["9th", "Twin-Furnace Architecture, Coordinated Directive, Merciful Disconnect"],
    ["15th", "Dominion of the Forged, Sovereign Overclock"]])
SPELL_ROWS = [(3, ["Command", "Sanctuary"]), (5, ["Heat Metal", "Warding Bond"]), (9, ["Dispel Magic", "Revivify"]),
              (13, ["Fabricate"]), (17, ["Creation", "Wall of Force"])]
SPELLS_HTML = (P("You always have these spells prepared once you reach the listed artificer level. They count as artificer spells "
                 "for you and don't count against the number of artificer spells you prepare.")
               + T(["Artificer level", "Spells"], [["3rd", "<em>command, sanctuary</em>"], ["5th", "<em>heat metal, warding bond</em>"],
                                                  ["9th", "<em>dispel magic, revivify</em>"], ["13th", "<em>fabricate, summon construct</em>"],
                                                  ["17th", "<em>creation, wall of force</em>"]])
               + P("<em>Command</em> represents the tradition's power to impose magical directives. It does not establish legal "
                   "ownership of a creature, and the Directive Binding works separately from it. (<em>Summon construct</em> is "
                   "from <em>Tasha's Cauldron of Everything</em>; the module grants the other nine from the SRD automatically.)"))

# =============================================================================== FEATURES
f_eng = cf("sf-engineering", "Soulforge Engineering", P(
    "You gain proficiency with smith's tools; if you already have it, choose another set of artisan's tools. You learn to "
    "speak, read and write Infernal; if you already know it, learn another language of your choice. You can use smith's tools "
    "or tinker's tools as a spellcasting focus for your artificer spells.",
    "<strong>Creating a construct.</strong> During a long rest you can build or rebuild one Infernal Servitor with smith's or "
    "tinker's tools and 50 gp of metal, components or salvage. Once built, the same frame can be repaired during later rests "
    "without paying again. It may look like any mechanical creature of its size: an armoured golem, a warforged-like assistant, "
    "a quadruped guardian, a skeletal or porcelain automaton, a spider-legged repair unit, a miniature war machine. Appearance "
    "never grants flight, swimming, extra attacks, extra manipulating limbs or other unlisted abilities. A servitor is a "
    "construct creature, not a warforged character, and gains no warforged traits.",
    "<strong>Choosing a chassis.</strong> Each servitor uses one of two frames: the <strong>Enforcer</strong> (melee attacks, "
    "bodyguard duty, labour, area control) or the <strong>Attendant</strong> (healing support, repairs, reconnaissance, tools). "
    "During a long rest you can rebuild a frame into the other configuration at no cost, provided it hasn't been permanently "
    "lost."), img="ic-sf-engineering", cls=AR, level=3,
    activities=[utility("sf-build", 0, name="Build or Rebuild a Servitor (long rest, 50 gp)")])

e_emerg = effect("sf-emergency", "Arcane Emergency Power", icon("ic-sf-enforcer"),
                 description="<p>Running on an expended spell slot: 1 hour per slot level. No soul personality, Echo, Pulse, "
                             "Awakened Inscription, Sparks or Overburn.</p>")
f_serv = cf("sf-servitor", "Infernal Servitor", P(
    "Your servitor has two possible operating states.",
    "<strong>Soulbound.</strong> Its infernal furnace accepts one soul coin at a time. As an action within 5 feet of an inactive "
    "servitor, you insert a coin; the coin is consumed and its soul becomes the machine's conscious pilot. The coin's remaining "
    "charges set its fuel and Resonance Sparks: 1 charge gives 24 hours and 1 Spark, 2 charges 48 hours and 2 Sparks, 3 charges "
    "72 hours and 3 Sparks. The soul keeps its personality, alignment, knowledge and memories, and gives the servitor the "
    "<strong>Construct Imprint</strong> of its Soul Archetype. A servitor houses one soul at a time and can't stack or swap "
    "Echoes. When the fuel runs out the soul is destroyed unless it is liberated first. Replacing a soul means stopping the "
    "furnace and liberating its occupant (or another established extraction method); a removed soul never makes a new coin.",
    "<strong>Arcane Emergency Power.</strong> With no usable coin, you can expend an artificer spell slot as an action while "
    "touching the servitor. It runs for 1 hour per slot level. In this state it follows the normal command and chassis rules "
    "and keeps its frame attacks and support functions, but has no personality and can't use an Echo, Pulse or Awakened "
    "Inscription, gain Sparks or Overburn. Emergency power never creates a soul. It keeps the subclass playable without "
    "destroying anyone.",
    "<strong>Shared limits.</strong> A servitor occupies a space and can be targeted like any creature. It can't attune to magic "
    "items, gains no equipment or infusion slots, and never takes an extra action because it has a soul. At 0 hit points it "
    "becomes inert; its furnace stays available for liberation for 1 hour unless the core is destroyed. Rebuilding a frame never "
    "restores fuel or Sparks, and a soul with no fuel can't animate even an intact body."), img="ic-sf-enforcer", cls=AR, level=3,
    effects=[e_emerg],
    activities=[utility("sf-install", 0, name="Install a Soul Coin (action, within 5 ft.)"),
                utility("sf-emergency", 1, name="Arcane Emergency Power (expend a spell slot)", effects=[e_emerg["_id"]]),
                utility("sf-cool", 2, name="Cool the Furnace (DC 15 tinker's tools: −2 Heat, −1 on failure)",
                        roll=("1d20 + @abilities.int.mod + @prof", "Cooling check")),
                damage_act("sf-overburn", 3, name="Construct Overburn: servitor takes 2d10 fire", parts=[dmg(2, 10, "", ["fire"])],
                           act=SPECIAL)])

f_dir = cf("sf-directive", "Directive Binding", P(
    "To control a servitor you attune to its <strong>Soulforge Control Harness</strong>. This uses one of your ordinary "
    "attunement slots. The harness can't be sold, transferred or used on another artificer's construct without a separate "
    "feature or agreement. It counts toward your attunement limit but isn't a magic item for features that count magic items. "
    "Ending the attunement severs the binding, and the construct becomes inactive.",
    "<strong>The binding.</strong> An attuned, Soulbound construct must obey your explicit, achievable instructions, given aloud "
    "or telepathically within 120 feet. It can't deliberately disobey an unambiguous instruction, sabotage the task, or invent an "
    "unreasonable reading to dodge it. It keeps its own mind, and may freely argue, criticise, complain about its body, ask for "
    "repairs, comfort, new duties or liberation, offer unsolicited advice, keep friendships and rivalries, remember its life, "
    "keep unrelated information to itself, and negotiate further agreements. The binding can compel truthful disclosure of "
    "specifically requested information the soul actually knows; it can't make the soul remember what it has forgotten.",
    "<strong>Rights of an imprisoned soul.</strong> The binding gives mechanical control, not lawful title. You may own a "
    "machine with no legal claim over the person inside it, and a compelled order is never voluntary consent under the "
    "Championship's law. A soul may dispute its imprisonment even while it can't defy an explicit order. This matters when Misty's "
    "repossession men, the Brass Arbiter or the Articles on personhood come calling.",
    "<strong>In combat.</strong> Your servitor shares your initiative and acts immediately after you. It can move and speak "
    "freely; without a command it takes the Dodge action. As a bonus action on your turn you can command one attuned servitor "
    "within 120 feet to take one action on its next turn: Attack, Dash, Disengage, Help, a chassis ability, Construct Overburn or "
    "a Construct Pulse, or an object interaction or tool task. It takes reactions only when its statistics allow. It follows "
    "standing orders outside combat without new commands. While you are incapacitated it can move to safety or continue an "
    "established noncombat task, but can't start commanded attacks or Pulses. A soul never gives you extra actions."),
    img="ic-sf-directive", cls=AR, level=3,
    activities=[utility("sf-command", 0, name="Command a Servitor (bonus action)", act=activation("bonus", 1), rng_=rng(120))])

f_etch = cf("sf-etched", "Soul-Etched Enchantments", P(
    "<strong>Awakened Inscription.</strong> You can dedicate one additional attunement slot to a servitor you already control, so "
    "that construct uses two of your slots. While it does, the servitor gains the <strong>Awakened Inscription</strong> of its "
    "resident soul's archetype. A servitor can never hold more than one inscription. You can end the extra attunement during a "
    "short rest, removing the inscription without affecting the control link. Changing the soul means removing or liberating "
    "the old occupant; the new soul's imprint replaces the old one's."), img="ic-sf-etched", cls=AR, level=5)
f_cond = cf("sf-conduit", "Resonant Conduit", P(
    "Once on each of your turns, when you deal damage with an artificer spell or one of your servitors deals damage, you can "
    "add [[/r 1d8]] force damage to one damage roll. Alternatively, when your artificer spell restores hit points or your "
    "servitor uses Bolster or Field Repair, you can increase one target's healing or temporary hit points by 1d8. You choose "
    "only one of these benefits each turn. The die becomes 2d8 at 15th level. Resonant Conduit works with soul power or "
    "Arcane Emergency Power."), img="ic-sf-conduit", cls=AR, level=5,
    activities=[damage_act("sf-conduit", 0, name="Resonant Conduit (force)", act=SPECIAL,
                           parts=[dmg_formula(f"(1 + floor({LV} / 15))d8", ["force"])]),
                heal_act("sf-conduit-h", 1, formula_part=dmg_formula(f"(1 + floor({LV} / 15))d8"), name="Resonant Conduit (healing)",
                         act=SPECIAL)])
f_twin = cf("sf-twin", "Twin-Furnace Architecture", P(
    "You can maintain two Soulforged constructs. During a long rest you can build an <strong>Auxiliary Servitor</strong> in "
    "addition to your Primary Servitor. Each needs its own Control Harness attunement and its own fuel, and each can be an "
    "Enforcer or an Attendant. The Auxiliary has half the normal maximum hit points of its chassis (rounded up) but otherwise "
    "uses the same statistics, abilities, imprint and scaling. You can swap which is Primary during a long rest; recalculate "
    "their maximum hit points, keeping their current proportion as closely as possible."), img="ic-sf-twin", cls=AR, level=9)
f_coord = cf("sf-coordinated", "Coordinated Directive", P(
    "When you use your bonus action to command your servitors, you can command both with the same bonus action. Each can move "
    "and take one action, but between them they take at most <strong>one offensive action</strong> per round: an Attack, or a "
    "Construct Pulse that deals damage or grants an immediate attack. The other takes a support action (Bolster, Help, Field "
    "Repair, Triage, Dash, Disengage or a non-damaging Pulse), or both can support. One construct never takes two commanded "
    "actions because the other is absent. Each tracks its own Heat and Sparks, and only one servitor may use a reaction in the "
    "same round."), img="ic-sf-directive", cls=AR, level=9,
    activities=[utility("sf-coord", 0, name="Coordinated Directive (bonus action, both servitors)", act=activation("bonus", 1))])
f_mercy = cf("sf-mercy", "Merciful Disconnect", P(
    "Once per long rest, as an action, you can perform an emergency liberation of the soul in a powered-down servitor within 5 "
    "feet: the normal DC 18 liberation check succeeds automatically. The construct becomes inert and loses all remaining fuel "
    "and Sparks. This frees the soul from the furnace but doesn't cancel any independently valid infernal contract that "
    "imprisoned it; the freed soul's fate follows the campaign's rules for liberated souls."), img="ic-sf-mercy", cls=AR, level=9,
    uses_=uses(1, ["lr"]), activities=[utility("sf-mercy", 0, name="Merciful Disconnect", consumption=consume_item_uses())])
e_dom = effect("sf-dominion", "Dominion of the Forged", icon("ic-sf-dominion"), transfer=False,
               changes=[("system.attributes.ac.bonus", 2, "+1"), ("system.attributes.hp.bonuses.overall", 2, "10")],
               description="<p>Apply to each attuned servitor: +1 AC, +10 maximum hit points, telepathy with its artificer across "
                           "1 mile on the same plane.</p>")
f_dom = cf("sf-dominion", "Dominion of the Forged", P(
    "Your attuned servitors, Primary and Auxiliary, gain +1 AC, 10 additional maximum hit points, and telepathic communication "
    "with you across 1 mile while on the same plane. Your Resonant Conduit die becomes 2d8. (In Foundry, drag the "
    "<em>Dominion of the Forged</em> effect from this feature onto each servitor.)"), img="ic-sf-dominion", cls=AR, level=15,
    effects=[e_dom])
f_over = cf("sf-overclock", "Sovereign Overclock", P(
    "Once per long rest, as a bonus action, you activate Sovereign Overclock for 1 minute. While it lasts, when you use "
    "Coordinated Directive both servitors may take offensive actions (an Attack or an offensive Pulse each), though neither takes "
    "more than one commanded action on its own turn. Once per round, when one servitor activates a Pulse, the other can reduce "
    "its own Heat by 1. The Overclock ends early if you are incapacitated or both servitors are inactive. It never creates "
    "Sparks, restores fuel or bypasses attunement."), img="ic-sf-overclock", cls=AR, level=15, uses_=uses(1, ["lr"]),
    activities=[utility("sf-overclock", 0, name="Sovereign Overclock (bonus action, 1 minute)", act=activation("bonus", 1),
                        consumption=consume_item_uses())])
FEATURES = [f_eng, f_serv, f_dir, f_etch, f_cond, f_twin, f_coord, f_mercy, f_dom, f_over]

_adv = [grant(3, [opt_uuid(f_eng), opt_uuid(f_serv), opt_uuid(f_dir)]), grant(5, [opt_uuid(f_etch), opt_uuid(f_cond)]),
        grant(9, [opt_uuid(f_twin), opt_uuid(f_coord), opt_uuid(f_mercy)]), grant(15, [opt_uuid(f_dom), opt_uuid(f_over)])]
for _lvl, _names in SPELL_ROWS:
    _adv.append(grant(_lvl, [spell_uuid_by_name(n) for n in _names], "Soulforged Spells", spell=ALWAYS("int")))
SOULFORGED = {"_id": fid("sub:soulforged"), "name": "The Soulforged", "type": "subclass", "img": icon("ic-soulforged"),
              "sort": 0, "folder": None, "effects": [], "flags": {}, "_stats": STATS,
              "system": {"description": {"value": "<p><em>Artificer Specialist (3rd, 5th, 9th and 15th level).</em></p>" + INTRO
                                         + IDENTITY, "chat": ""},
                         "source": SOURCE, "identifier": "the-soulforged", "classIdentifier": "artificer",
                         "advancement": _adv, "spellcasting": {"progression": "none", "ability": ""}}}

# =============================================================================== SERVITOR ACTORS (12th-level artificer, Int 20)
def build_actors():
    from bestiary import Mon, REACT
    out = []
    note = ("<p><em>Shown for a 12th-level artificer with Intelligence 20 (proficiency bonus +4, spell attack +9, save DC 17). "
            "Rescale with your own numbers: {f}. Its challenge rating only sets proficiency +4; a servitor is worth no XP.</em></p>")
    m = Mon("sf-enf")
    m.trait("Industrial Strength", "The Enforcer counts as one size larger when calculating carrying capacity and the weight it "
            "can push, drag or lift.")
    m.trait("Magical Construction", "Its attacks count as magical.")
    m.atk("Force Fist", 9, [dmg(1, 8, 4, ["force"])], cls="spell", img="ic-gauntlets")
    m.util("Interpose", "<p><em>Reaction.</em> When a creature within 5 feet of the Enforcer is targeted by an attack, the "
           "Enforcer imposes disadvantage on that attack roll before it is made.</p>", act=REACT(), img="ic-guardian")
    a = npc("soulforged-enforcer", "Soulforged Enforcer", img=portrait("soulforged-enforcer"), token=tok("soulforged-enforcer"),
            items=m.items, ctype="construct", alignment="as its soul", cr=9, ac=17, hp=70, hp_formula="5 + 5 × artificer level + Int",
            speed=30, abilities=(16, 12, 16, 10, 12, 10), saves=("dex", "con"), di=("poison",), ci=("exhaustion", "poisoned"),
            senses={"darkvision": 60}, langs=("infernal",), lang_custom="and any languages its soul knew in life", disposition=1,
            bio=P("A combat frame built to intercept enemies, withstand punishment and protect its creator.")
            + note.format(f="AC 13 + PB; HP 5 + 5 × artificer level + Int modifier; Force Fist uses your spell attack, 1d8 + PB force"))
    a["flags"][MOD] = {"servitor": True}
    out.append(a)
    m = Mon("sf-att")
    m.trait("Magical Construction", "Its attacks count as magical.")
    m.atk("Arc Needle", 9, [dmg(1, 6, 4, ["lightning"])], kind="ranged", cls="spell", rng_=60, img="ic-glassheart")
    m.heal("Bolster", "1d6 + 4", "One creature within 10 feet gains 1d6 + your proficiency bonus temporary hit points. Temporary "
           "hit points from repeated uses don't stack.", temp=True, img="ic-sf-attendant")
    m.heal("Field Repair", "2d8 + 5", "One construct, object or vehicle within 5 feet regains 2d8 + your Intelligence modifier hit "
           "points. Your servitors share a pool of uses equal to your proficiency bonus per long rest. A target destroyed at 0 hit "
           "points (rather than merely incapacitated) can't be repaired this way alone.", uses_=uses(4, ["lr"]),
           consumption=consume_item_uses(), img="ic-hammer")
    m.trait("Triage", "As an action, the Attendant stabilises a living creature within 5 feet without an ability check.")
    a = npc("soulforged-attendant", "Soulforged Attendant", img=portrait("soulforged-attendant"), token=tok("soulforged-attendant"),
            items=m.items, ctype="construct", alignment="as its soul", cr=9, ac=16, hp=58, hp_formula="5 + 4 × artificer level + Int",
            speed=30, climb=20, abilities=(10, 14, 14, 12, 14, 10), saves=("dex", "wis"), di=("poison",),
            ci=("exhaustion", "poisoned"), senses={"darkvision": 60}, langs=("infernal",),
            lang_custom="and any languages its soul knew in life", disposition=1,
            bio=P("A support frame with repair tools, stabilisation mechanisms, defensive magic and precision instruments.")
            + note.format(f="AC 12 + PB; HP 5 + 4 × artificer level + Int modifier; Arc Needle uses your spell attack, 1d6 + PB "
                            "lightning; Bolster 1d6 + PB; Field Repair 2d8 + Int"))
    a["flags"][MOD] = {"servitor": True}
    out.append(a)
    return out


# =============================================================================== CONSTRUCT IMPRINTS
# key, archetype, d100, role, example soul, Echo, Pulse (kind, text), Inscription, personality, quest, activity spec
IMPRINTS = [
    ("courier", "Courier", "01–10", "Rapid support and spell delivery", "Quillip Swiftpost, the Undelivered Messenger",
     ("Living Delivery Conduit", "When you cast an artificer spell with a range of touch, your Courier servitor can deliver it as "
      "though it were the caster, provided it is within 60 feet of you and the target is within 5 feet of it. The spell uses your "
      "action, slot and other requirements."),
     ("Emergency Dispatch", "Support", "Choose one willing creature within 30 feet of the servitor. It can use its reaction to "
      "move up to 15 feet without provoking opportunity attacks."),
     ("Priority Delivery", "Once per turn, immediately after the servitor delivers one of your touch spells, it can move 10 feet "
      "without provoking opportunity attacks. This doesn't use its movement."),
     "Impatient, sarcastic, constantly asks whether the party knows the meaning of the word <em>urgent</em>. Deeply distressed "
     "by unopened letters.", "Deliver the final letter Quillip was carrying when captured.", None),
    ("lancer", "Lancer", "11–18", "Duelling and enemy control", "Tarnik Blackspoke, the Betrayed Cavalryman",
     ("Duelist's Interdiction", "Once per turn when the servitor hits a creature with a melee attack, that creature can't make "
      "opportunity attacks against anyone but the servitor until the start of your next turn."),
     ("Oathpin", "Offensive", "The servitor makes one melee attack. On a hit, the target takes the attack's normal damage and "
      "must succeed on a Strength saving throw or have its speed reduced to 0 until the start of your next turn."),
     ("Challenge of Iron", "Once per round, when a creature the servitor struck on its previous turn attacks an ally within 5 "
      "feet of the servitor, the servitor can use its reaction to impose disadvantage on that attack."),
     "Proud, formal, deeply protective of weaker companions. Horrified that a sworn knight's soul might be used for dishonourable "
     "acts.", "Find evidence that Tarnik did not abandon his squad.", ("save", "str", None)),
    ("artificer", "Artificer", "19–27", "Mechanical adaptation", "Gilda Copperhand, the Disgraced Master Engineer",
     ("Artisan's Memory", "The servitor can use smith's tools, tinker's tools and one other set of artisan's tools you're "
      "proficient with, making those checks with your Intelligence modifier and proficiency bonus."),
     ("Emergency Reconfiguration", "Support", "The servitor switches between Enforcer and Attendant configuration for 1 minute, "
      "gaining the other frame's movement, AC and chassis abilities. Its current and maximum hit points stay as they are until "
      "the effect ends; it keeps its fuel, Heat, Sparks and imprint."),
     ("Redundant Soul Housing", "Once per long rest, when the servitor would drop to 0 hit points, it drops to 1 hit point "
      "instead and its Heat resets to 0."),
     "Obsessive about maintenance, meticulously critical of the artificer's workmanship, unable to accept that a working "
     "mechanism might still be badly designed.", "Recover Gilda's stolen master schematic, which may have shaped the Iron Heir.",
     None),
    ("scout", "Scout", "28–36", "Detection and battlefield intelligence", "Nera Ash-Eye, the Last Pathfinder",
     ("Spectral Detection Lattice", "The servitor can perceive invisible creatures and objects within 10 feet that aren't behind "
      "total cover."),
     ("Weakness Revelation", "Support", "Choose one creature within 60 feet. Until the start of your next turn it gains no benefit "
      "from invisibility or from half or three-quarters cover against attacks by you or your servitors. Other concealment still "
      "applies."),
     ("Perimeter Intelligence", "While the servitor is conscious, you and friendly creatures within 10 feet of it can't be "
      "surprised and gain +2 to initiative rolls."),
     "Suspicious, terse, watchful. Routinely predicts disasters and becomes insufferably smug when right.",
     "Discover what happened to the companions Nera guided into Avernus.", None),
    ("thief", "Thief", "37–45", "Infiltration and disarming", "Pex Lockwhisper, the Impossible Burglar",
     ("Thieving Fingers", "The servitor can use thieves' tools and make precise Dexterity (Sleight of Hand) checks, adding your "
      "proficiency bonus, with the fine motor control to do so whatever its chassis looks like."),
     ("Filch the Weapon", "Support", "One creature within 5 feet makes a Dexterity saving throw or drops one Small or smaller "
      "object it's holding (your choice) into an adjacent space. Objects magically secured to their owner are unaffected."),
     ("Cloaked Mechanism", "Once per short or long rest, after the servitor succeeds on a Sleight of Hand check or Helps a "
      "creature's Stealth check, it becomes invisible until the start of your next turn, or until it attacks, deals damage or "
      "casts a spell."),
     "Cheeky, opportunistic, naturally suspicious of authority. Insists every locked door is an invitation.",
     "Retrieve the fortune Pex hid shortly before he was murdered.", ("save", "dex", None)),
    ("fire-adept", "Fire Adept", "46–54", "Area denial", "Mother Cinder, the Ashen Pyromancer",
     ("Punishing Furnace", "Once per turn, when a creature starts grappling the servitor or hits it with an unarmed strike, that "
      "creature takes [[/damage 1d6 type=fire]]."),
     ("Molten Inscription", "Offensive", "Choose a 10-foot square of ground within 30 feet. Until the start of your next turn it "
      "is difficult terrain, and a creature that enters it for the first time on a turn or starts its turn there takes 2d8 fire "
      "damage (once per turn)."),
     ("Tempered Inferno", "Fire damage from the servitor's own features ignores fire resistance (not immunity). The servitor "
      "chooses whether its fire ignites unattended combustibles."),
     "Dramatic, enthusiastic, and disturbingly appreciative of a beautiful explosion. An evil arsonist, an idealistic purifier "
     "or a devoted forge-worker, depending on alignment.", "Discover who deliberately set the fire that ended Mother Cinder's life.",
     ("damage", None, (2, 8, "fire"))),
    ("healer", "Healer", "55–63", "Emergency healing and preservation", "Merrow Kindhand, the Battlefield Physician",
     ("Deathwatch Instruments", "Friendly creatures within 10 feet of the active, unincapacitated servitor have advantage on death "
      "saving throws."),
     ("Borrowed Heartbeat", "Support", "One willing creature within 5 feet can immediately spend up to two of its Hit Dice and "
      "regain hit points equal to the dice rolled plus your Intelligence modifier. If it is conscious and prone, it can also stand "
      "without spending movement."),
     ("The Last Breath", "Once per long rest, when a creature within 10 feet would drop to 0 hit points without being killed "
      "outright, the servitor can use its reaction to leave it at 1 hit point instead. The servitor then takes 2d8 necrotic "
      "damage that can't be reduced."),
     "Compassionate but impatient, especially with reckless adventurers. Calls everyone by their most recent injury.",
     "Find the surviving patients Merrow was protecting when she was captured.", None),
    ("warlord", "Warlord", "64–71", "Tactical coordination", "General Varnek, the Conqueror of Seven Banners",
     ("Tactical Formation", "Once per turn, one friendly creature within 5 feet of the servitor gains +1 on its first weapon "
      "attack roll that turn."),
     ("General's Command", "Offensive", "One willing ally within 30 feet who can hear the servitor can use its reaction to make "
      "one weapon attack against a target within its weapon's range."),
     ("Coordinated Assault", "When one of your servitors Helps the other servitor's attack, that attack gains an extra +2 to hit "
      "(once per round)."),
     "Authoritative, loud, arrogant, and certain that everyone else is disastrously incompetent at war.",
     "Learn which subordinate betrayed Varnek for an infernal promotion.", None),
    ("magistrate", "Magistrate", "72–79", "Evidence, investigation and legal control", "Ysera Quill, the Defiant Infernal Magistrate",
     ("Witness Plate", "While active, the servitor perfectly records conversations, visible writing and signatures within 30 feet, "
      "and can play them back in its voice or as projected script. Magical concealment can prevent a particular recording."),
     ("Identify the Controller", "Support", "One construct or fiend within 30 feet makes a Charisma saving throw. On a failure, "
      "the servitor learns who is currently issuing its magical commands (if the target knows), and the target has disadvantage "
      "on its next attack roll before the start of your next turn."),
     ("Chain of Custody", "After examining a document or magical contract for 1 minute, the servitor identifies altered passages "
      "and counterfeit seals. This is authenticated evidence of alteration; it can't by itself decide whether the whole agreement "
      "is lawful."),
     "Formal, pedantic, exacting, relentlessly concerned with the wording of instructions. Constantly reminds the artificer that "
     "owning a machine is not owning its occupant.", "Expose the fraudulent transaction by which Misty obtained Ysera's soul coin.",
     ("save", "cha", None)),
    ("penitent", "Penitent", "80–86", "Protective intervention", "Brother Halven, the Repentant Executioner",
     ("Shield of Remorse", "While the servitor is taking the Dodge action, friendly creatures within 5 feet of it gain +1 AC "
      "against the first attack made against each of them that round."),
     ("Intercession Writ", "Support", "Choose one ally within 30 feet. The next time it takes damage before the start of your next "
      "turn, reduce the damage by 2d8 + your Intelligence modifier; any unused protection then vanishes."),
     ("Burden of Mercy", "Once per short or long rest, when the servitor uses Interpose or Intercession Writ to protect an ally, "
      "that ally can immediately repeat a saving throw against one effect making it charmed or frightened, ending it on a success."),
     "Quiet, remorseful, deeply uncomfortable with coercion. Speaks most when the artificer faces a hard moral choice.",
     "Find someone harmed by Halven's former deeds and offer restitution.", None),
    ("berserker", "Berserker", "87–94", "Destructive area disruption", "Skritch Mawbreaker, the Pit Champion",
     ("Grudge Engine", "While the servitor is at or below half its maximum hit points, the first damaging attack it makes on each "
      "of its turns deals an extra 1d4 bludgeoning damage."),
     ("Scrapstorm", "Offensive", "The servitor spins violently. Each enemy within 5 feet makes a Strength saving throw, taking 2d8 "
      "bludgeoning damage and being pushed 10 feet on a failure, or half damage and no push on a success."),
     ("Wrecking Pressure", "Once per turn, when the servitor hits with a melee attack while below half its hit points, it can take "
      "1d6 fire damage (ignoring resistance and immunity) to deal an extra 1d8 force damage with that attack."),
     "Excitable, belligerent, quick to laugh, eager to fight enormous enemies. May regard the artificer as an inadequate but "
     "entertaining battle commander.", "Defeat the pit master who sold Skritch's soul rather than honour his promised freedom.",
     ("save", "str", (2, 8, "bludgeoning"))),
    ("cartographer", "Planar Cartographer", "95–00", "Spatial engineering and planar defence", "Sevrin Nine-Roads, the Lost Navigator",
     ("Planar Surveyor", "The servitor senses the presence and rough direction of planar portals, extradimensional entrances and "
      "unstable planar boundaries within 60 feet, unless a powerful ward blocks it. It doesn't learn destinations."),
     ("Phase Bridge", "Support", "Create a solid bridge of translucent force up to 15 feet long and 5 feet wide between two points "
      "the servitor can see within 30 feet. It lasts until the start of your next turn; anyone on it when it vanishes falls."),
     ("Dimensional Anchor", "Once per long rest, when unwilling teleportation or planar displacement would affect you, the "
      "servitor or a willing ally within 10 feet of it, the servitor can use its reaction to prevent it. It can't undo a "
      "displacement that has already happened."),
     "Curious, philosophical, often distracted by impossible geometry. Describes places that no longer exist.",
     "Discover where an expedition that vanished between the planes finally went.", None),
]
ARCH_WEIGHTS = [10, 8, 9, 9, 9, 9, 9, 8, 8, 7, 8, 6]


def imprint_items():
    out = []
    for key, arch, rng_, role, soul, echo, pulse, insc, pers, quest, spec in IMPRINTS:
        desc = (f"<p><em>Construct Imprint · d100 {rng_} · {role}</em></p>"
                f"<p><strong>Construct Echo: {echo[0]}.</strong> {echo[1]}</p>"
                f"<p><strong>Construct Pulse: {pulse[0]} ({pulse[1]}).</strong> {pulse[2]} <em>(Commanded action, 1 Spark, +1 "
                f"Heat; one Pulse per servitor per round; saves use your artificer spell save DC.)</em></p>"
                f"<p><strong>Awakened Inscription: {insc[0]}.</strong> {insc[1]} <em>(Requires the second attunement slot, 5th "
                f"level.)</em></p><p><strong>Example soul:</strong> {soul}. {pers} <em>Personal quest:</em> {quest}</p>")
        acts_ = []
        if spec and spec[0] == "save":
            parts = [dmg(spec[2][0], spec[2][1], "", [spec[2][2]])] if spec[2] else []
            acts_.append(save(f"sf-imp-{key}", 0, ability=spec[1], dc=17, parts=parts, name=f"{pulse[0]} (Pulse)",
                              on_save="half" if parts else "none", tgt=target(1, "creature")))
        elif spec and spec[0] == "damage":
            acts_.append(damage_act(f"sf-imp-{key}", 0, name=f"{pulse[0]} (Pulse)", parts=[dmg(spec[2][0], spec[2][1], "", [spec[2][2]])]))
        else:
            acts_.append(utility(f"sf-imp-{key}", 0, name=f"{pulse[0]} (Pulse)"))
        f = feat(f"sf-imprint-{key}", f"Construct Imprint: {arch}", desc, img=icon("ic-sf-imprint"), activities=acts_,
                 ftype="monster")
        f["flags"][MOD] = {"imprint": key, "level": 3}
        out.append(f)
    return out


IMPRINT_ITEMS = imprint_items()


def imprint_html():
    return "".join(f"<h4>{i[1]} <span class='rc-fine'>(d100 {i[2]} · {i[3]})</span></h4>"
                   f"<p><strong>Echo: {i[5][0]}.</strong> {i[5][1]}</p>"
                   f"<p><strong>Pulse: {i[6][0]} ({i[6][1]}).</strong> {i[6][2]}</p>"
                   f"<p><strong>Awakened Inscription: {i[7][0]}.</strong> {i[7][1]}</p>"
                   f"<p class='rc-fine'><em>Example soul: {i[4]}. {i[8]} Quest: {i[9]}</em></p>" for i in IMPRINTS)


# =============================================================================== SOUL GENERATION
ALIGN = [("Lawful Good", "The Principled Protector", "Duty, compassion, justice, honour, responsibility.",
          "They obey the binding while protesting the injustice and seeking lawful ways to prevent similar harm.",
          "Keeping promises, protecting the vulnerable, admitting mistakes, allowing eventual liberation.",
          "I will do what you command. I shall not, however, call it honourable.",
          "Their need to fulfil an oath may conflict with their desire to escape servitude."),
         ("Neutral Good", "The Compassionate Soul", "Kindness, healing, empathy, reducing suffering.",
          "Distressed, worried about consequences, eager to find merciful alternatives.",
          "Compassion, mercy, helping strangers, treating souls as individuals.",
          "There must be another way. There is nearly always another way.",
          "They may willingly stay in a painful situation to protect someone they care about."),
         ("Chaotic Good", "The Defiant Liberator", "Freedom, justice, individuality, resisting oppression.",
          "Outspoken condemnation, even when mechanically compelled to comply.",
          "Freeing captives, opposing tyrants, allowing personal expression.",
          "I spent my life fighting slavers, and now I'm a bloody iron kettle with legs!",
          "They might enjoy their powerful body while despising how they got it."),
         ("Lawful Neutral", "The Keeper of Order", "Procedure, discipline, structure, responsibility, consistency.",
          "May comply without emotional protest but still question whether the order is procedurally justified.",
          "Clarity, consistency, adherence to formal agreements.",
          "Instruction received. I advise you that the command violates three provisions of our existing agreement.",
          "Their loyalty to a system is tested when that system is demonstrably corrupt."),
         ("True Neutral", "The Practical Observer", "Practicality, balance, survival, knowledge, personal responsibilities.",
          "More likely to discuss consequences than morality, though some object for personal reasons.",
          "Competence, balanced decisions, respect for personal goals.",
          "Not what I would have chosen. But considering the alternatives, it may work.",
          "Their wish to stay uninvolved may become impossible as the Championship escalates."),
         ("Chaotic Neutral", "The Unpredictable Individualist", "Personal freedom, curiosity, originality, autonomy.",
          "Anything from disgust to detached cynicism, depending on the soul's interests.",
          "Room to improvise, serious attention to their opinions, freedom where possible.",
          "We could use the door. Or the wall. Or hear me out: the ceiling.",
          "They may form strong attachments while insisting they need nobody."),
         ("Lawful Evil", "The Ambitious Tyrant", "Hierarchy, ambition, power, discipline, control.",
          "May ridicule generosity as inefficient, yet obey fully and sometimes take an interest in the results.",
          "Credible deals, status, influence, mutually beneficial arrangements.",
          "You have commanded my obedience. You have not earned my respect.",
          "A devotee of hierarchy forcibly placed at its bottom."),
         ("Neutral Evil", "The Calculating Opportunist", "Personal advancement, survival, advantage, self-interest.",
          "Generally complies, but asks why the artificer is spending resources for nothing.",
          "Clear incentives and bargains that consistently benefit both sides.",
          "There's the profitable option, the merciful option, and the stupid option. Which would you like first?",
          "They may find that attachment has become worth more to them than gain."),
         ("Chaotic Evil", "The Malicious Destroyer", "Domination, cruelty, impulsive desire, personal gratification.",
          "Obeys, but complains loudly or mocks the people being helped.",
          "Personal incentives, chances to reach their goals, consistent treatment. Trust doesn't guarantee kindness.",
          "WHAT DO YOU MEAN WE'RE SAVING HIM? I ALREADY PICKED WHICH ARM I WAS GOING TO BREAK!",
          "A soul that wants absolute freedom may find it now depends on the artificer to exist at all.")]
MOTIVATION = ["Recover someone they loved", "Take revenge on whoever caused their death", "Restore their reputation or prove their innocence",
              "Complete unfinished work", "Escape an outstanding obligation or punishment", "Gain power, influence or a second chance at life"]
MANNER = ["Formal and precise", "Sarcastic and irreverent", "Emotional and passionate", "Quiet and contemplative",
          "Confrontational and argumentative", "Warm and talkative"]
CONTRADICTION = ["Their convictions conflict with something terrible they once did", "They want freedom but fear the afterlife",
                 "They hate imprisonment but enjoy their new mechanical abilities", "They stay loyal to someone who betrayed them",
                 "They claim to want revenge but secretly want forgiveness",
                 "They believe they deserve punishment but can't accept its consequences"]
GRIEVANCE = ["Despises the design of their mechanical body", "Resents compulsory obedience but is glad to move again",
             "Recognises someone involved in their imprisonment",
             "Believes their imprisonment was lawful and thinks liberation dishonourable",
             "Wants revenge before their fuel runs out", "Wants freedom but is terrified of what comes after"]
CMISHAP = [("Servo Seizure", "The servitor's speed becomes 0 until the end of its next turn."),
           ("Screaming Feedback", "The artificer makes a DC 15 Wisdom save or takes −2 on their next attack roll or ability check."),
           ("Soulfire Leakage", "The construct takes 2d10 fire damage, ignoring resistance and immunity."),
           ("Directive Jam", "The construct can't Attack or activate Pulses until the end of its next turn."),
           ("Ghost Hands", "The construct makes a DC 15 Dexterity save or moves up to half its speed toward something significant in "
                           "the soul's memories, avoiding obviously lethal terrain."),
           ("Creditor's Beacon", "A creditor registered against that soul learns the machine's location for 1 hour.")]
SOULS = [("Tarnik Blackspoke", "Lancer", "Lawful Good", "An honourable knight determined to prove his innocence"),
         ("Merrow Kindhand", "Healer", "Neutral Good", "A compassionate physician who believes no patient is beyond saving"),
         ("Quillip Swiftpost", "Courier", "Chaotic Good", "A reckless messenger who smuggled food to oppressed communities"),
         ("Ysera Quill", "Magistrate", "Lawful Neutral", "A precise advocate who values truth and procedural fairness"),
         ("Gilda Copperhand", "Artificer", "True Neutral", "A brilliant engineer who values invention above ideology"),
         ("Sevrin Nine-Roads", "Planar Cartographer", "Chaotic Neutral", "A traveller obsessed with freedom and exploration"),
         ("Mother Cinder", "Fire Adept", "Lawful Evil", "A pyromancer who believes destruction should follow strict principles"),
         ("General Varnek", "Warlord", "Neutral Evil", "A mercenary commander who values personal advancement"),
         ("Pex Lockwhisper", "Thief", "Chaotic Evil", "A malicious burglar who treats theft and humiliation as entertainment")]
EXTRA_SOULS = [("Nera Ash-Eye", "Scout"), ("Brother Halven", "Penitent"), ("Skritch Mawbreaker", "Berserker")]

GENERATION = (P("Every alignment is equally likely, whatever the archetype. A Lawful Good Berserker, a Chaotic Evil Healer, a Lawful "
                "Evil Courier and a Chaotic Good Magistrate are all equally possible. Alignment shapes the soul's morals, "
                "worldview, reading of orders, relationships and personality. It never changes the imprint's mechanics.",
                "<strong>Random alignment (2d6).</strong> Roll two separate d6. The first sets order (1–2 Lawful, 3–4 Neutral, 5–6 "
                "Chaotic), the second morality (1–2 Good, 3–4 Neutral, 5–6 Evil). Neutral and Neutral is True Neutral. Each of the "
                "nine results has exactly a 1 in 9 chance.",
                "<strong>The Nine-Soul Deck.</strong> For a whole collection of coins, make nine cards, one per alignment. Shuffle, "
                "draw without replacement until all nine are used, then reshuffle. Every completed group of nine souls then has "
                "exactly one of each alignment.")
              + "<h3>The Nine Alignments</h3>"
              + "".join(f"<h4>{a}: {t}</h4><ul><li><strong>Values:</strong> {v}</li>"
                        f"<li><strong>To cruel or merciful orders:</strong> {o}</li><li><strong>Trust is earned through:</strong> {tr}</li>"
                        f"<li><strong>Voice:</strong> “{voice}”</li><li><strong>Contradiction:</strong> {c}</li></ul>"
                        for a, t, v, o, tr, voice, c in ALIGN)
              + "<h3>Creating a Soul</h3>"
              + UL("Roll the <strong>Soul Archetype</strong> (d100).", "Roll <strong>alignment</strong> (2d6) or draw from the "
                   "Nine-Soul Deck.", "Roll the <strong>initial attitude</strong> (d8) and the <strong>legal origin</strong> (d6), "
                   "using the Soul Furnace tables.", "Roll a <strong>core motivation</strong>, <strong>speaking manner</strong>, "
                   "<strong>personal contradiction</strong> and <strong>grievance</strong> (d6 each).",
                   "Give the soul a name, former species, homeland and one meaningful memory, and choose how its relationship "
                   "with the artificer begins.")
              + T(["d6", "Core motivation", "Speaking manner", "Personal contradiction", "Grievance"],
                  [[i + 1, MOTIVATION[i], MANNER[i], CONTRADICTION[i], GRIEVANCE[i]] for i in range(6)])
              + P("<em>Alignment has no bearing on the legal origin. An evil soul can be the victim of a fraudulent imprisonment, "
                  "and a good soul may have made a genuinely terrible bargain.</em> The individual soul is a persistent character, "
                  "not a disposable table result: its alignment, personality and legal history survive any change of body.")
              + "<h3>A Balanced Collection: Nine Souls</h3>"
              + T(["Soul", "Archetype", "Alignment", "Defining trait"], [list(s) for s in SOULS])
              + P("Nera Ash-Eye (Scout), Brother Halven (Penitent) and Skritch Mawbreaker (Berserker) roll their alignments the same "
                  "way when introduced. The named examples never fix an archetype to an alignment."))

FURNACE = (P("Every Soulbound construct uses the Soul Furnace's three resources: <strong>fuel</strong> (how long the soul can "
             "animate the body, set by the coin's charges), <strong>Resonance Sparks</strong> (power drawn from the soul's "
             "memories, spent on Pulses, never recharged by rest), and <strong>Engine Heat</strong> (instability from Pulses and "
             "Overburn).",
             "<strong>Pulses.</strong> A Pulse needs the servitor's commanded action, spends 1 Spark and adds 1 Heat; one Pulse per "
             "servitor per round. With no Sparks left, the soul still pilots the body and gives its passive Echo until its fuel "
             "runs out or it is freed.",
             "<strong>Heat.</strong> 0–2 stable. 3–4 strained: the flames change colour, gears shudder, and the soul complains. At 5, "
             "each Pulse or Overburn causes a construct mishap on a d6 roll of 1–2. At 6 the furnace ruptures: the servitor takes "
             "3d10 fire damage that ignores resistance and immunity, suffers one construct mishap, and resets to Heat 3.",
             "<strong>Cooling.</strong> A construct loses 1 Heat at the end of its turn if it neither Pulsed nor Overburned that "
             "round. A character within 5 feet can use an action and make a DC 15 Intelligence check with tinker's tools: success "
             "removes 2 Heat, failure 1.",
             "<strong>Construct Overburn.</strong> When commanded, once on its turn, a servitor can gain 20 extra feet of movement "
             "or advantage on its next attack roll that turn. It takes 2d10 fire damage (ignoring resistance and immunity) and "
             "gains 1 Heat. Overburn needs no Sparks.")
           + T(["d6", "Construct mishap", "Effect"], [[i + 1, a, b] for i, (a, b) in enumerate(CMISHAP)])
           + P("<em>A mishap is an involuntary malfunction, not deliberate disobedience.</em>",
               "<strong>Handling coins.</strong> Identify Soul (action, DC 14 Intelligence (Arcana or Religion)) reveals the "
               "archetype, charges, attitude and any infernal seal. Questioning a soul uses the coin's normal Query and spends a "
               "charge; merely holding it gives an emotional impression for free. To liberate a soul from a furnace, stop the "
               "engine and make a DC 18 Intelligence (Arcana) or Wisdom (Religion) check as an action with a consecrated focus or "
               "suitable magic. Success frees the soul and ends its fuel, Echo, Pulses and Awakened Inscription; failure costs the "
               "action but no Spark or fuel.",
               "<strong>Vehicles.</strong> A Soulforged artificer can't make a quad, hauler or Reclaimer into an extra autonomous "
               "companion, but can identify, repair and manipulate their Soul Furnace systems. In a vehicle a soul gives its "
               "vehicle Echo and Pulse from the Codex; in a servitor it gives its Construct Imprint. One soul never gives both at "
               "once."))

EXAMPLE = (P("<strong>Veyra Brassheart</strong>, a 12th-level Soulforged with Intelligence 20 (proficiency +4), travels with two "
             "independently conscious constructs.")
           + T(["Construct", "Soul", "Stats", "Fuel / Sparks", "Inscription"],
               [["<strong>Iron Oath</strong> (Primary Enforcer, 70 HP)", "Tarnik Blackspoke, LG Lancer",
                 "AC 17; Force Fist +9, 1d8 + 4 force", "72 hours / 3", "Challenge of Iron"],
                ["<strong>Mercy-7</strong> (Auxiliary Attendant, 29 HP)", "Merrow Kindhand, NG Healer",
                 "AC 16; Arc Needle +9, 1d6 + 4 lightning", "48 hours / 2", "None"]])
           + P("<strong>Attunement.</strong> Slot 1 Iron Oath's harness; slot 2 Mercy-7's harness; slot 3 Iron Oath's Awakened "
               "Inscription; slot 4 a personal magic item. At 14th level her fifth slot adds flexibility.",
               "<strong>A turn.</strong> Facing three infernal soldiers and a wounded ally, Veyra casts <em>heat metal</em> on the "
               "captain's armour, then issues a Coordinated Directive with her bonus action. Iron Oath advances and punches a "
               "soldier; Mercy-7 reaches the wounded ally and Bolsters them for 1d6 + 4. Veyra adds Resonant Conduit's 1d8 to "
               "the punch <em>or</em> the temporary hit points, not both. The souls immediately start arguing.")
           + BOX("“Advance!”", P("<strong>Tarnik:</strong> The enemy's flank is exposed! Strike while they're disorganised!<br>"
                                 "<strong>Merrow:</strong> I have three bleeding patients behind us, you oversized suit of cutlery!<br>"
                                 "<strong>Tarnik:</strong> I was commander of the King's Fifth Cavalry!<br>"
                                 "<strong>Merrow:</strong> Wonderful. And now you're a wardrobe with fists.<br>"
                                 "<em>Both carry out their instructions anyway.</em>"))
           + T(["Level", "How the Soulforged plays"],
               [["3–4", "One companion with a unique personality and limited soul abilities"],
                ["5–8", "A specialised companion, enhanced through extra attunement"],
                ["9–11", "Two constructs with coordinated combat and support actions"],
                ["12–14", "A customisable mechanical team working alongside the artificer's spells"],
                ["15–17", "A formidable commander able to field two offensive units"],
                ["18–20", "More attunement flexibility from the artificer's own progression"]]))

QUICKREF = ('<table class="rc-table"><tbody>' + "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td></tr>" for a, b in [["Build a frame", "Long rest, tools, 50 gp of materials"], ["Attune", "One attunement slot per servitor"],
                        ["Install a coin", "Action within 5 ft.; the coin is consumed"], ["Fuel", "24 hours per remaining charge"],
                        ["Sparks", "1–3; never recharge"], ["Pulse", "Commanded action, 1 Spark, +1 Heat"],
                        ["Overburn", "+20 ft. or advantage on an attack; +1 Heat; 2d10 fire to itself"],
                        ["Command", "Your bonus action"], ["Two constructs", "9th level; one offensive action between them"],
                        ["Both attack", "15th level, Sovereign Overclock"], ["Awakening", "A second attunement slot on that frame"],
                        ["Alignment", "Two d6 or the Nine-Soul Deck"], ["Liberation", "Stopped furnace, DC 18 with a consecrated focus"]]) + "</tbody></table>")


def player_page():
    return (INTRO + IDENTITY + "<h3>Progression</h3>" + PROGRESSION + "<h3>Soulforged Spells</h3>" + SPELLS_HTML
            + "<h3>Features</h3>" + "".join(f"<h4>{f['name']} <span class='rc-fine'>({f['system']['requirements']})</span></h4>"
                                            f"{f['system']['description']['value']}" for f in FEATURES)
            + "<h3>Infernal Servitors</h3>"
            + P("Both frames are Small or Medium constructs, immune to poison damage, exhaustion and the poisoned condition, with "
                "darkvision 60 feet, Infernal and the languages their soul knew in life. Their attacks count as magical.")
            + T(["", "Enforcer", "Attendant"],
                [["AC", "13 + PB", "12 + PB"], ["Hit points", "5 + 5 × artificer level + Int mod", "5 + 4 × artificer level + Int mod"],
                 ["Speed", "30 ft.", "30 ft., climb 20 ft."], ["Str/Dex/Con/Int/Wis/Cha", "16/12/16/10/12/10", "10/14/14/12/14/10"],
                 ["Saves", "Dex +1 + PB, Con +3 + PB", "Dex +2 + PB, Wis +2 + PB"],
                 ["Abilities", "<strong>Force Fist</strong> (spell attack, reach 5 ft., 1d8 + PB force); <strong>Interpose</strong> "
                  "(reaction: disadvantage on an attack against a creature within 5 ft.); <strong>Industrial Strength</strong>",
                  "<strong>Arc Needle</strong> (spell attack, 60 ft., 1d6 + PB lightning); <strong>Bolster</strong> (1d6 + PB temp "
                  "HP, 10 ft.); <strong>Field Repair</strong> (2d8 + Int, PB uses per long rest across all servitors); "
                  "<strong>Triage</strong>"]])
            + "<h3>The Soul Furnace in a Servitor</h3>" + FURNACE
            + "<h3>The Twelve Construct Imprints</h3>"
            + T(["d100", "Archetype", "Construct role"], [[i[2], i[1], i[3]] for i in IMPRINTS])
            + P("This table sets abilities, not alignment; a soul's profession, morals and personality are rolled separately. In "
                "Foundry, each imprint is an item in Player Options: drag it onto the servitor.")
            + imprint_html()
            + "<h3>Souls and Alignment</h3>" + GENERATION
            + "<h3>Example: A 12th-Level Soulforged</h3>" + EXAMPLE
            + "<h3>The Voluntary Maintenance Covenant</h3>"
            + P("A Soulforged artificer may offer a separate contract to the soul in the machine, Form SF-12. It isn't needed to run "
                "the servitor. It sets out treatment, working conditions, disclosure, liberation and the soul's rights. Acceptance "
                "must be voluntary: the Directive Binding can't substitute for consent. A breach creates a legal dispute and "
                "remedies, but never transfers a soul, creates a power or overrides the Championship's higher rules.")
            + "<h3>Quick Reference</h3>" + QUICKREF
            + P("<em>The most interesting Soulforged won't necessarily be the one who builds the strongest golem. It may be the one "
                "who builds a body for a soul, offers that soul its freedom, and discovers that the soul chooses to stay. Not "
                "because it must.</em>"))


SUB_NOTE = P(
    "<strong>The Soulforged (balance review).</strong> The design was marked as a playable draft. What I checked and what changed:",
    UL("<strong>Servitor numbers</strong> sit beside the Battle Smith's Steel Defender: similar AC, a little more hit points "
       "(5 + 5 × level + Int against 2 + Int + 5 × level), the same 1d8 + PB attack. Paying an attunement slot per servitor, and "
       "a second for each Awakened Inscription, is the intended trade.",
       "<strong>Resonant Conduit</strong> (1d8 once per turn, 2d8 at 15th) matches the Artillerist's Arcane Firearm, which also "
       "adds 1d8 once per turn with no limit on uses. Left as written.",
       "<strong>Coordinated Directive</strong> keeps one offensive action between two bodies until 15th level, and only one "
       "servitor reaction per round. Left as written; it is the main thing to watch in play.",
       "<strong>Summon construct</strong> (13th) isn't in the SRD, so the module can't grant it automatically. The other nine "
       "Soulforged spells are granted by advancement.",
       "<strong>Servitor actors</strong> are shown at 12th level with Intelligence 20 (the campaign's starting level). Their "
       "statistics are written as formulas in the text and biography so tables can rescale them.",
       "<strong>Imprint Pulses in Foundry</strong> use a flat DC 17 (12th level, Intelligence 20). Change it to your own artificer "
       "spell save DC."),
    "<strong>Class.</strong> The artificer class isn't in the SRD. The subclass item attaches to any artificer class with the "
    "identifier <em>artificer</em>, such as the one from your own copy of Tasha's Cauldron of Everything or Eberron.")


def gm_page():
    rows = [["More than two servitors?", "Not through this subclass"], ["Several souls in one servitor?", "No; one active soul per frame"],
            ["One soul powering a vehicle and a construct?", "Not at the same time"], ["Does alignment change powers?", "No"],
            ["Can a good soul refuse an evil order?", "It can protest, but must obey an explicit, achievable command while bound"],
            ["Can a soul talk without orders?", "Yes, freely"], ["Can it sabotage its machine?", "Not against an explicit, achievable instruction"],
            ["Independent attacks?", "No; it needs a command"], ["Can a construct attune items?", "No"],
            ["Do rests restore Sparks?", "No"], ["Does a new chassis restore fuel?", "No"],
            ["Can a soul be freed safely?", "Yes, by liberation or suitable magic"],
            ["Does liberation cancel every contract?", "No; independent agreements are settled separately"],
            ["Can a construct claim the Crown of Avernus?", "Potentially, if its personhood, eligibility and consent are "
             "established under the Charter"]]
    return (P("<em>For the GM: running a Soulforged artificer in the Championship. The player's rules are in Book II.</em>")
            + "<h3>Misty and Disputed Ownership</h3>"
            + P("Misty is the ideal recurring adversary for a Soulforged. Some coins in Avernus carry the designation MIST-113: her "
                "court claims them. The seal is not proof of title. The artificer may discover that a companion was imprisoned by "
                "forgery, a repaid debt or an unlawful transfer.",
                "<strong>Challenging a coin.</strong> A DC 16 Investigation or Religion check on the markings and papers may find "
                "irregularities. With incomplete evidence, DC 18 Persuasion or Religion wins a temporary stay. Authentic proof of "
                "forgery or missing title defeats the claim before a competent arbiter. A successful challenge prevents improper "
                "repossession, but it doesn't free the occupant by itself.",
                "<strong>The personal stakes.</strong> Imagine the artificer travelling with Ysera Quill, an argumentative Lawful "
                "Neutral magistrate, for twelve sessions. She has prosecuted devils, exposed forgeries and protected the party. Then "
                "Misty reveals that Ysera's coin was taken from one of her own prisoners, and demands it back. The artificer must "
                "fight a legal battle for a companion whose body they built, whose mind they can't replace, and whose existence "
                "may depend on the machinery that imprisons her. Misty isn't demanding a magic item. She is demanding a person.")
            + "<h3>The Iron Heir and Janella Greenbottle</h3>"
            + P("Tie the tradition to the golemancer story. Janella may have studied an early version of the Directive Binding "
                "while building Greyhurst's golems, and the Iron Heir may be its most advanced form. Unlike an ordinary servitor, it "
                "might have a permanent consciousness instead of a coin's tenant, act without a control harness, hold its own legal "
                "identity, carry memories inherited from several souls, and know secrets of the original succession trials. These "
                "are story properties of the Iron Heir alone, never subclass abilities.",
                "It sets up a strong revelation: what if the ultimate achievement of Soulforging is not a machine that obeys "
                "perfectly, but one that can finally <em>choose</em>? That discovery could change the relationship between "
                "artificers, constructs and the whole soul-fuel economy of Avernus.")
            + "<h3>Rulings</h3>" + T(["Question", "Ruling"], rows)
            + "<h3>Attunement</h3>"
            + P("The 2014 artificer attunes to 3 items at 3rd–9th level, 4 at 10th–13th, 5 at 14th–17th and 6 at 18th–20th. Each "
                "active servitor takes one slot and each Awakened Inscription another, so at 12th level an artificer can run two "
                "fully awakened servitors with no slots left for personal items. That is intentional: the subclass trades personal "
                "magic for mechanical versatility.")
            + "<h3>What to Watch in Play</h3>"
            + UL("<strong>Action economy.</strong> Coordinated Directive is flexible but limits offence until 15th level; Sovereign "
                 "Overclock should feel powerful without giving two full independent turns.",
                 "<strong>Attunement.</strong> Servitors and inscriptions should feel worth the personal items given up.",
                 "<strong>Support.</strong> Compare Bolster and Resonant Conduit with an Artillerist's Protector cannon.",
                 "<strong>Soul scarcity.</strong> Sparks don't recharge, so three-charge coins should feel valuable without making "
                 "the subclass miserable when fuel runs short.",
                 "<strong>Personality.</strong> Let disagreement and moral conflict drive roleplay, but never use a soul's "
                 "personality to deny a clear mechanical command.",
                 "<strong>Agency.</strong> The artificer is the player's character. You voice the soul's thoughts and feelings; "
                 "resolve its mechanical instructions consistently.")
            + SUB_NOTE)


# =============================================================================== HANDOUTS
def handouts(DOC, field_lines):
    record = DOC("REGISTRY OF BOUND CONSCIOUSNESS", field_lines(P(
        "Name: ____________________________ Former species / homeland: ____________________",
        "Soul archetype: ________________ Alignment: ________________ Initial attitude: ________________",
        "Core motivation: ____________________ Speaking manner: ____________________",
        "Personal contradiction: ____________________________________________",
        "Greatest grievance: ____________________________________________",
        "Legal origin: ____________________ Current registered creditor: ____________________",
        "Personal memory: ____________________________________________",
        "Relationship with artificer: ____________________________________________",
        "Fuel: ______ hours · Sparks: ____ / ____ · Engine Heat: ____ / 6",
        "Chassis: ☐ Enforcer ☐ Attendant · Control Harness: ☐ Attuned ☐ Unattuned · Awakened Inscription: ☐ Active ☐ Inactive",
        "Outstanding personal promise: ____________________________________________"))
        + P("<em>The soul is a persistent character, not a disposable result. Its alignment, personality and legal history survive "
            "any change of body.</em>"), form="Soulforge Record · Form SF-01")
    covenant = DOC("SUPPLEMENTAL AGREEMENT OF MECHANICAL RESIDENCE", P(
        "<strong>Parties:</strong> the Artificer (the Constructor) and the resident consciousness (the Occupant).",
        "<strong>Article I — Mechanical Housing.</strong> The Constructor provides the Occupant with a functioning mechanical body, "
        "maintained to reasonable operational standards.",
        "<strong>Article II — Expression.</strong> The Occupant keeps the right to speak, express opinions, criticise instructions "
        "and petition for changes in treatment without further contractual penalty.",
        "<strong>Article III — Preservation.</strong> The Constructor will not knowingly expend the Occupant's final fuel interval "
        "without first offering an opportunity for safe liberation.",
        "<strong>Article IV — Memory and Identity.</strong> The Occupant's memories, identity, former property and pre-existing "
        "legal rights are not transferred to the Constructor by this agreement.",
        "<strong>Article V — Liberation.</strong> The conditions under which the Occupant may seek liberation are recorded "
        "separately and open to inspection.",
        "<strong>Article VI — Disputes.</strong> Disputes may be heard by an authorised arbiter under the laws governing infernal "
        "contracts and the Championship of Succession.",
        "<em>Acceptance must be voluntary. The Directive Binding cannot substitute for consent.</em>")
        + field_lines("<p>Constructor: ____________ Occupant: ____________ Witness: ____________</p>"),
        stamp="VOLUNTARY", form="Soulforge Covenant · Form SF-12")
    return [("sf-record", "Handout 22 — Soulforge Record (Form SF-01)", record),
            ("sf-covenant", "Handout 23 — Soulforge Covenant (Form SF-12)", covenant)]


# =============================================================================== TABLES
def build_tables(table):
    table("sf-archetype", "Soul Archetype (d100, Soulforged)", "1d100",
          [(f"<strong>{i[1]}.</strong> {i[3]}. Echo: {i[5][0]}; Pulse: {i[6][0]}; Inscription: {i[7][0]}.", w)
           for i, w in zip(IMPRINTS, ARCH_WEIGHTS)], "The soul's Construct Imprint. Abilities, not alignment.", icon("ic-sf-imprint"))
    table("sf-order", "Soul Alignment: Order (d6)", "1d6", ["Lawful", "Lawful", "Neutral", "Neutral", "Chaotic", "Chaotic"],
          "Roll with Morality. Neutral and Neutral is True Neutral.", icon("ic-sf-imprint"))
    table("sf-morality", "Soul Alignment: Morality (d6)", "1d6", ["Good", "Good", "Neutral", "Neutral", "Evil", "Evil"],
          "", icon("ic-sf-imprint"))
    table("sf-motivation", "Soul: Core Motivation (d6)", "1d6", MOTIVATION, "", icon("ic-sf-imprint"))
    table("sf-manner", "Soul: Speaking Manner (d6)", "1d6", MANNER, "", icon("ic-sf-imprint"))
    table("sf-contradiction", "Soul: Personal Contradiction (d6)", "1d6", CONTRADICTION, "", icon("ic-sf-imprint"))
    table("sf-grievance", "Soul: Grievance (d6)", "1d6", GRIEVANCE, "", icon("ic-sf-imprint"))
    table("sf-mishap", "Construct Furnace Mishap (d6)", "1d6", [f"<strong>{a}.</strong> {b}" for a, b in CMISHAP],
          "At Heat 5, each Pulse or Overburn mishaps on a 1–2.", icon("ic-sf-overclock"))


TABLE_KEYS = ["sf-archetype", "sf-order", "sf-morality", "sf-motivation", "sf-manner", "sf-contradiction", "sf-grievance",
              "sf-mishap"]


# =============================================================================== SOUL COINS (named souls)
def build_coins(item_fn, put_fn, folder, existing):
    """Add the remaining named souls as coins, and give the four existing example coins their alignment."""
    align = {n: (a, al) for n, a, al, _ in SOULS}
    for it in existing:
        for n, (a, al) in align.items():
            if n in it["name"]:
                it["system"]["description"]["value"] += (f"<p><strong>Soulforged.</strong> {al}. In a servitor this soul gives the "
                                                         f"<em>{a}</em> Construct Imprint.</p>")
    have = {n for n in align if any(n in it["name"] for it in existing)}
    U = consume_item_uses()
    base = ("<p>A soul coin (see <em>Soul Coin</em>). In a Soulforged servitor this soul gives the <em>{a}</em> Construct "
            "Imprint; in a war machine, the matching Soul Furnace Echo.</p>")
    for i in IMPRINTS:
        n = i[4].split(",")[0]
        if n in have:
            continue
        al = align.get(n, (None, "Alignment: roll 2d6 when introduced"))[1]
        key = "soul-coin-" + slug(n)
        put_fn(folder, item_fn(key, f"Soul Coin: {n} ({i[1]})", "consumable",
                               base.format(a=i[1]) + f"<p><strong>{i[4]}.</strong> {al}. {i[8]} <em>Quest:</em> {i[9]}</p>",
                               img=icon("ic-soul-coin"), subtype="trinket", weight=0, uses_=uses(3, []),
                               activities=[heal_act(f"{key}-drain", 0, formula_part=dmg_formula("1d10"), temp=True,
                                                    name="Drain Life (1 charge)", consumption=U, tgt=target("", "self")),
                                           utility(f"{key}-query", 1, name="Query (1 charge)", consumption=U),
                                           utility(f"{key}-install", 2, name="Install in a Servitor (action)")]))
