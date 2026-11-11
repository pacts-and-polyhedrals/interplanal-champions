"""Interplanal Champions: the fourteen relics, the case exhibits, Crown Marks and Proofs, plus the Scriptorium's relics."""
from lib5e import *


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


ITEMS = {}  # folder -> list


def put(folder, doc):
    ITEMS.setdefault(folder, []).append(doc)
    return doc


def wondrous(key, name, desc, *, img, rarity, attune="", activities=None, uses_=None, effects=None, folder="Relics of the Championship",
             itype="equipment", subtype="trinket", extra=None, price=0):
    return put(folder, item(key, name, itype, desc, img=icon(img), rarity=rarity, attune=attune, activities=activities,
                            uses_=uses_, effects=effects, subtype=subtype, extra=extra, price=price, weight=1))


U = consume_item_uses()
SR = "Asmodeun Scriptorium Relics"


# =========================================================================== SCRIPTORIUM RELICS (carried over)
wondrous("infernal-signet", "Infernal Signet of the Red Clause",
         P("A heavy signet ring of black iron set with a ruby that ticks like a clock. Left behind when the Red "
           "Clause's avatar is destroyed.",
           "<strong>Emergency Cancellation.</strong> During the adventure, a creature holding the signet can use an "
           "action to stamp an emergency cancellation on the Master Ledger, ending the soul transfer.",
           "<strong>Afterwards.</strong> While attuned, you know whether any written contract you touch has been "
           "altered since it was signed. Once per dawn you can cast <em>zone of truth</em> (save DC 15) from the ring.",
           "<strong>Curse of the Ninth Court.</strong> Asmodeus's clerks always know where the ring is."),
         img="it-signet", rarity="rare", attune="required", folder=SR, uses_=uses(1, ["dawn"]),
         activities=[utility("signet-cancel", 0, name="Emergency Cancellation"),
                     utility("signet-zot", 1, name="Zone of Truth (1/dawn)", consumption=consume_item_uses())])
wondrous("arbiter-gavel", "Gavel of the Brass Arbiter",
         P("A small brass gavel that the Arbiter strikes once, after a just verdict, and leaves on the lectern for the "
           "party.",
           "<strong>Order!</strong> Once per dawn, as an action, you strike the gavel and cast <em>command</em> (save "
           "DC 15) targeting up to three creatures, giving all of them the same one-word command.",
           "<strong>Precedent.</strong> You have advantage on Charisma (Persuasion) checks made to argue a point of law "
           "before any court that recognises the Pact Primeval."),
         img="it-gavel", rarity="rare", attune="required", folder=SR, uses_=uses(1, ["dawn"]),
         activities=[utility("gavel", 0, name="Order!", consumption=consume_item_uses())])
wondrous("golgorath-quill", "Golgorath's Quill",
         P("The Asmodeun Scriptorium's legendary notary quill: a permanent, more powerful "
           + uuid_spell("quill-of-binding", "Quill of Binding") + ".",
           "While attuned, you can cast <em>quill of binding</em> at will without components, and once per dawn you can "
           "cast " + uuid_spell("binding-clause", "binding clause") + " without material components.",
           "<strong>Sentience (optional).</strong> The quill hums disapprovingly when a contract is badly drafted."),
         img="it-quill", rarity="veryRare", attune="required by a spellcaster", folder=SR, uses_=uses(1, ["dawn"]),
         activities=[utility("golgorath-quill", 0, name="Quill of Binding (at will)"),
                     utility("golgorath-clause", 1, name="Binding Clause (1/dawn)", consumption=consume_item_uses(),
                             act=activation("hour", 1))])

CHAIN = item("clause-chain-whip", "Length of Clause Chain", "weapon", P(
    "A barbed length of the Red Clause's beard, unravelled into chain when the smile disappeared. You have a +1 bonus to "
    "attack and damage rolls made with this magic weapon. On a hit it deals an extra 1d6 psychic damage as the target "
    "hears every clause it has ever broken read aloud."),
    img=icon("it-chainwhip"), rarity="rare", attune="required", subtype="martialM", weight=3,
    props=("fin", "rch", "mgc"),
    extra={"damage": {"base": {"number": 1, "denomination": 4, "bonus": "", "types": ["slashing"],
                               "custom": {"enabled": False, "formula": ""},
                               "scaling": {"mode": "", "number": None, "formula": ""}},
                      "versatile": {"number": None, "denomination": None, "bonus": "", "types": [],
                                    "custom": {"enabled": False, "formula": ""},
                                    "scaling": {"mode": "", "number": None, "formula": ""}}},
           "magicalBonus": 1, "range": {"value": None, "long": None, "reach": 10, "units": "ft"},
           "type": {"value": "martialM", "baseItem": "whip"}, "proficient": None, "mastery": "slow"},
    activities=[attack("clause-chain-whip", 0, ability="", reach=10, classification="weapon",
                       parts=[dmg(1, 6, "", ["psychic"])])])
CHAIN["system"]["activities"][next(iter(CHAIN["system"]["activities"]))]["damage"]["includeBase"] = True
put(SR, CHAIN)

# =========================================================================== THE FOURTEEN RELICS (Book II, Section 6)
R = "Relics of the Championship"
NOTE = ("<p class='rc-fine'><em>Unless a description says otherwise, a charge spent on a spell uses the listed item save DC, "
        "does not consume a spell slot, and recharges at dawn in Avernus.</em></p>")

wondrous("quill-true-notice", "Quill of True Notice", P(
    "A signature written with this quill leaves an indelible, visible timestamp and the signer's chosen disclosed name on the "
    "original sheet; copies show a faint orange line.",
    "The quill has 3 charges, regaining 1d3 at dawn. Expend a charge to learn whether the signature immediately before you was "
    "physically written by the person presenting themselves as its signer (an impostor may have signed sincerely under a false "
    "name). The quill is not a universal lie detector and cannot compel someone to sign.",
    "<em>Recommended acquisition: the Act I registration desk.</em>") + NOTE,
    img="ic-quill", rarity="uncommon", uses_=uses(3, [{"period": "dawn", "type": "formula", "formula": "1d3"}]),
    activities=[utility("quill-true-notice", 0, name="Verify the Previous Signature", consumption=U)])
wondrous("receipt-last-gift", "Receipt of the Last Gift", P(
    "A fragment of Form H-25 from Waterdeep, signed by the independent Brass Arbiter. As an action, display it to create a "
    "10-foot-radius field that grants advantage on saving throws against being charmed or magically compelled by fiends until "
    "the end of your next turn. It then crumbles into red ash.",
    "The receipt is also admissible documentary evidence of the Waterdeep ruling; that legal property is not consumed until the "
    "hearing ends.", "<em>Recommended acquisition: Waterdeep carry-over / Act I.</em>"),
    img="ic-receipt", rarity="uncommon", itype="consumable", subtype="trinket", uses_=uses(1, []),
    activities=[utility("receipt-last-gift", 0, name="Display the Receipt", consumption=U, tgt=target("", "ally", "radius", 10),
                        effects=[])])
e_crown = effect("crownmark-thp", "Crownmark Gauntlets", icon("ic-gauntlets"), transfer=True,
                 description="<p>Advantage on Strength (Athletics) checks made to climb, grapple or hold a contested objective.</p>")
wondrous("crownmark-gauntlets", "Crownmark Gauntlets", P(
    "While wearing them, you have advantage on Strength (Athletics) checks made to climb, grapple or hold a contested objective.",
    "Once per long rest, when you reduce a hostile creature to 0 HP or hold an advertised arena control point for two consecutive "
    "rounds, you may use a reaction to gain 15 temporary hit points. The gauntlets never create extra Crown Marks; they only "
    "reward the underlying action.", "<em>Recommended acquisition: the first Proof of Survival.</em>"),
    img="ic-gauntlets", rarity="rare", attune="required", uses_=uses(1, ["lr"]), effects=[e_crown],
    activities=[heal_act("crownmark", 0, formula_part=dmg_formula("15"), temp=True, name="Hold the Crown",
                         act=activation("reaction", 1), consumption=U, tgt=target("", "self"))])
wondrous("mistletoe-manacles", "Mistletoe Manacles", P(
    "<em>Three pairs.</em> Reusable restraints for Medium or smaller creatures. A willing creature can be bound automatically; an "
    "unwilling, grappled creature is bound only after an action and a successful DC 17 Strength (Athletics) or Dexterity "
    "(Sleight of Hand) check contested by its Athletics or Acrobatics. A restrained wearer can use its action to attempt DC 17 "
    "Athletics or Acrobatics to escape.",
    "The manacles prevent nonmagical use of hands but do not suppress spellcasting by themselves. Once per long rest, the wielder "
    "can activate them to prevent the wearer from teleporting until the end of its next turn on a failed DC 17 Charisma save. "
    "They contain no soul-ownership clause.", "<em>Recommended acquisition: citation enforcement stores.</em>"),
    img="ic-manacles", rarity="rare", uses_=uses(1, ["lr"]),
    activities=[save("manacles-tp", 0, ability="cha", dc=17, on_save="none", name="Seal Against Teleportation", consumption=U,
                     tgt=target(1, "creature"), rng_=rng("", "touch"))])
wondrous("marshals-chain", "Marshal's Chain of Allegiance", P(
    "When a willing creature within 30 feet explicitly accepts your command for a specific task of no more than 1 minute, you "
    "may link a spectral brass strand to it; you can have only one such link active.",
    "Once per short rest, when the linked creature fails a saving throw, you can use your reaction to add [[/r 1d6]] to the failed "
    "roll, potentially turning it into a success. Either participant can end the link instantly without cost. This is teamwork, "
    "not domination.", "<em>Recommended acquisition: the Greyhurst coalition.</em>"),
    img="ic-chain", rarity="rare", attune="required", uses_=uses(1, ["sr"]),
    activities=[utility("marshals-chain", 0, name="Steady the Linked Ally (+1d6)", act=activation("reaction", 1), consumption=U,
                        roll=("1d6", "Allegiance"))])
wondrous("ashen-seed", "Ashen Seed of Remembrance", P(
    "Planting this dark-red seed over 1 minute creates a 20-foot-radius thicket lasting 1 hour. Willing creatures resting within "
    "it have advantage on checks and saving throws against magical memory alteration for the duration.",
    "Once per long rest, one creature completing a short rest in the thicket may restore one expended Hit Die and can remember one "
    "event from its own life that had been altered by a spell of 5th level or lower, subject to the spell's original saving "
    "throw. It cannot recreate another person's experiences or restore a soul already lawfully sold.",
    "<em>Recommended acquisition: the Greyhurst grove.</em>"),
    img="ic-seed", rarity="rare", attune="required by a spellcaster", uses_=uses(1, ["lr"]),
    activities=[utility("ashen-seed", 0, name="Plant the Thicket", act=activation("minute", 1),
                        tgt=target("", "", "radius", 20)),
                utility("ashen-seed-r", 1, name="Remembrance (short rest)", consumption=U)])
wondrous("glassheart-interpreter", "Glassheart Interpreter", P(
    "A palm-sized receiver keyed to Janella Greenbottle's maker-mark. Holding it within 30 feet of one of her golems allows a "
    "creature proficient in Arcana or tinker's tools to hear the construct's current orders and detect whether they were altered "
    "after leaving her workshop.",
    "Once per long rest, the operator can use an action to give a construct another saving throw against a magical command "
    "effect, or force an uncontrolled construct to make a DC 17 Wisdom save or lose reactions until its next turn. The device "
    "never grants permanent ownership or control of an unwilling autonomous construct.",
    "<em>Recommended acquisition: Janella's forge.</em>"),
    img="ic-glassheart", rarity="rare", uses_=uses(1, ["lr"]),
    activities=[save("glassheart", 0, ability="wis", dc=17, on_save="none", name="Jam an Uncontrolled Construct", consumption=U,
                     tgt=target(1, "creature"), rng_=rng(30)),
                utility("glassheart-free", 1, name="Grant a New Save Against Command", consumption=U, rng_=rng(30))])
e_pyric = effect("pyric-ring", "Pyric Covenant Ring", icon("ic-pyric-ring"), transfer=True,
                 changes=[("system.traits.dr.value", 2, "necrotic")], description="<p>Resistance to necrotic damage.</p>")
wondrous("pyric-ring", "Pyric Covenant Ring", P(
    "You gain resistance to necrotic damage. Once per long rest, when a creature within 30 feet willingly tells you a truthful "
    "fact that would place it at risk, you can use a reaction to grant it [[/r 2d8]] temporary hit points and advantage on its next "
    "saving throw before the start of your next turn.",
    "The inscription reads: <em>A secret given freely is worth more than a secret stolen.</em> A rival who sees the ring may "
    "assume you work for Misty; the ring itself does not bind you to her.", "<em>Recommended acquisition: Misty's embassy.</em>"),
    img="ic-pyric-ring", rarity="rare", attune="required", itype="equipment", subtype="ring", uses_=uses(1, ["lr"]),
    effects=[e_pyric],
    activities=[heal_act("pyric-ring", 0, formula_part=dmg(2, 8, ""), temp=True, name="Reward a Freely Given Secret",
                         act=activation("reaction", 1), consumption=U, tgt=target(1, "creature"), rng_=rng(30))])
_dmgbase = {"number": 1, "denomination": 8, "bonus": "", "types": ["slashing"], "custom": {"enabled": False, "formula": ""},
            "scaling": {"mode": "", "number": None, "formula": ""}}
SPLIT = item("contract-splitter", "Contract-Splitter Blade", "weapon", P(
    "<em>Weapon (any sword), very rare (requires attunement).</em> A +2 magic sword (statted here as a longsword).",
    "Once on each of your turns when you hit a creature maintaining a magical contract effect, you can deal "
    "[[/damage 1d6 type=force]] additional damage.",
    "Once per long rest, after hitting a target, you may choose one magical effect of 5th level or lower currently imposing a "
    "penalty or compulsion on that target; make a DC 17 ability check using your spellcasting ability, or Intelligence if you "
    "have none. On a success, end that effect. This cannot cancel a valid written agreement itself; it severs one active magical "
    "enforcement effect.", "<em>Recommended acquisition: the Citadel preliminary prize.</em>"),
    img=icon("ic-splitter"), rarity="veryRare", attune="required", weight=3, props=("mgc", "ver"), uses_=uses(1, ["lr"]),
    extra={"damage": {"base": _dmgbase, "versatile": dict(_dmgbase, denomination=10)}, "magicalBonus": 2,
           "type": {"value": "martialM", "baseItem": "longsword"}, "proficient": None, "mastery": "sap"},
    activities=[attack("contract-splitter", 0, ability="", classification="weapon", parts=[]),
                damage_act("splitter-force", 1, name="Split the Contract (+1d6 force)", parts=[dmg(1, 6, "", ["force"])],
                           act=activation("special", None)),
                utility("splitter-sever", 2, name="Sever an Enforcement Effect (DC 17)", act=activation("special", None),
                        consumption=U, roll=("1d20 + @mod", "Severing check"))])
SPLIT["system"]["activities"][next(iter(SPLIT["system"]["activities"]))]["damage"]["includeBase"] = True
SPLIT["system"]["rarity"] = "veryRare"
put(R, SPLIT)
wondrous("gavel-of-appeal", "Gavel of Appeal", P(
    "This blackwood gavel has 3 charges, regaining 1d3 daily. As an action expend one charge to cast "
    "<em>dispel magic</em> at 4th level.",
    "When resolving a public, contested hearing with documents that the relevant adjudicator can inspect, you can expend one "
    "charge to grant advantage on one Investigation, Religion or Persuasion check concerning admissibility or interpretation. No "
    "more than one charge may be spent this way per hearing, and the gavel cannot turn a lie into a true exhibit.",
    "<em>Recommended acquisition: a Brass Arbiter special commendation.</em>"),
    img="ic-gavel", rarity="veryRare", attune="required by a spellcaster",
    uses_=uses(3, [{"period": "dawn", "type": "formula", "formula": "1d3"}]),
    activities=[utility("gavel-dispel", 0, name="Dispel Magic (4th level)", consumption=U),
                utility("gavel-hearing", 1, name="Grant Advantage in a Hearing", consumption=U,
                        act=activation("special", None))])
WS = item("writshield", "Writshield of Personal Sovereignty", "equipment", P(
    "<em>Shield, very rare (requires attunement).</em> A +1 shield.",
    "When you or a creature within 10 feet fails a Charisma saving throw against a magical attempt to alter identity, bind a "
    "soul or compel a personal oath, you can use your reaction to allow a reroll. The second result stands. This can be done "
    "twice per long rest.",
    "During the Heartstone confrontation, the shield can serve as one authentic protection against the queen's identity-seizure "
    "effects, but gives no automatic immunity to her spells.", "<em>Recommended acquisition: the hag's first witness.</em>"),
    img=icon("ic-writshield"), rarity="veryRare", attune="required", weight=6, props=("mgc",), uses_=uses(2, ["lr"]),
    extra={"armor": {"value": 2, "magicalBonus": 1, "dex": None}, "type": {"value": "shield", "baseItem": "shield"},
           "strength": 0, "proficient": None},
    activities=[utility("writshield", 0, name="Sovereign Reroll", act=activation("reaction", 1), consumption=U, rng_=rng(10))])
put(R, WS)
wondrous("hourglass-true-dawn", "Hourglass of True Dawn", P(
    "Sand inside the glass flows according to time on the plane and jurisdiction named when the hourglass is activated. Once per "
    "long rest, as an action, create a 30-foot-radius sphere centred on the glass for 1 minute. Magical environmental effects "
    "relying solely on fabricated or frozen time are suppressed within the sphere.",
    "A hostile source may make a DC 18 Charisma save when the field appears; on a success, its effect is delayed rather than "
    "suppressed for one round. The sphere does not create daylight, erase legitimate service, or halt natural time. In Misty's "
    "lair, activating it can delay one lair-action pulse or the Heartstone recovery pulse, not both.",
    "<em>Recommended acquisition: the time registrar's vault.</em>"),
    img="ic-hourglass", rarity="veryRare", attune="required", uses_=uses(1, ["lr"]),
    activities=[save("hourglass", 0, ability="cha", dc=18, on_save="none", name="True Dawn Field", consumption=U,
                     tgt=target("", "", "sphere", 30))])
wondrous("lantern-three-witnesses", "Lantern of the Three Witnesses", P(
    "Three oil reservoirs are inscribed <strong>Name</strong>, <strong>Consent</strong> and <strong>Jurisdiction</strong>. The "
    "lantern has three charges and cannot be recharged until the campaign's current Heartstone rite ends.",
    "One charge makes a hidden true-name inscription visible for 10 minutes; another grants advantage on one saving throw against "
    "a hag's enchantment or illusion (declare before rolling); the third illuminates a hidden soul-anchor or its nearest ward "
    "within 60 feet.",
    "A bearer who has gathered all three Heartstone witness statements may use all remaining charges as an action to deactivate "
    "one of the queen's three witness-seals. It does not deal damage to Misty.",
    "<em>Recommended acquisition: the Heartstone investigation.</em>"),
    img="ic-lantern", rarity="veryRare", attune="required", uses_=uses(3, []),
    activities=[utility("lantern-name", 0, name="Reveal a True-Name Inscription", consumption=U),
                utility("lantern-save", 1, name="Ward Against a Hag (advantage)", consumption=U, act=activation("special", None)),
                utility("lantern-anchor", 2, name="Find a Soul-Anchor", consumption=U),
                utility("lantern-seal", 3, name="Deactivate a Witness-Seal (all charges)",
                        consumption={"targets": [{"type": "itemUses", "target": "", "value": "@item.uses.value",
                                                  "scaling": {"mode": "", "formula": ""}}],
                                     "scaling": {"allowed": False, "max": ""}, "spellSlot": True})])
wondrous("blackthorn-shears", "Blackthorn Shears", P(
    "A single-use ritual implement shaped from living infernal blackthorn. With an action while adjacent to a properly exposed "
    "soul-anchor, cut the magical tether connecting the anchor to its owner.",
    "This succeeds only if the party has already disabled two witness-seals or obtained a valid independent court order "
    "establishing unlawful ownership. If used on Misty's Heartstone after her second defeat, the shears destroy the tether and "
    "render the stone vulnerable to physical destruction. They cannot permanently kill a creature while its living body is "
    "elsewhere or erase a consented mortal contract as an incidental benefit.", "<em>Recommended acquisition: the Pyric Reliquary.</em>"),
    img="ic-shears", rarity="veryRare", itype="consumable", subtype="trinket", uses_=uses(1, []),
    activities=[utility("blackthorn", 0, name="Sever the Tether", consumption=U)])

# =========================================================================== EVIDENCE, PROOFS & TOKENS
E = "Exhibits & Evidence"
T = "Proofs, Crown Marks & Tokens"


def evidence(key, name, desc, *, img="ic-exhibit", folder=E, handout=""):
    h = (f"<p class='rc-fine'>Handout: {uuid_journal('handouts', handout, 'read the document')}</p>" if handout else "")
    return put(folder, item(key, name, "loot", desc + h, img=icon(img), subtype="", weight=0))


evidence("exhibit-a", "Exhibit A: The False Entrants", P(
    "An obsolete tournament bracket recovered from the sealed brass casket (Scene 2A). It lists contestants who have been dead "
    "for decades but have somehow been entered this year. One name belongs to Janella's family. A duplicate can be found in the "
    "Drowned Tavern's guest list (DC 15 Investigation)."), handout="exhibit-a")
evidence("exhibit-b", "Exhibit B: The False Service Order", P(
    "The cadaver collectors' warrant naming Greyhurst souls 'unclaimed', suspended by the registrar after a documented, valid "
    "challenge (Scene 3D)."), handout="exhibit-b")
evidence("exhibit-c", "Exhibit C: The Unmodified Command Transcript", P(
    "Released when the inverse summoning circle is activated correctly (Name → Consent → Witness → Jurisdiction). It shows Osric "
    "Kane deliberately concealing the soul transfer from the villagers."), handout="exhibit-c")
evidence("exhibit-d", "Exhibit D: The Annex That Isn't", P(
    "Misty's stamped annex to Petition M-9, showing 'consent' from Osric Kane on behalf of villagers he had no authority to bind. "
    "Proof of its defect is an automatic success in the M-9 hearing."), handout="petition-m9")
evidence("exhibit-e", "Exhibit E: Chain of Title", P(
    "The red serialization <strong>H-25/RETURN</strong> on every false entrant at Orro's stall, linking the tournament's "
    "fraudulent registry to the Red Clause case. Held up within 60 feet of Hollis Valrick, it suspends his False Certification "
    "for one round (once per encounter)."), handout="exhibit-e")
evidence("exhibit-f", "Exhibit F: Hollis's Immunity Document", P(
    "Hollis Valrick's immunity grant. The words <em>including acts yet to be discovered</em> are visible to anyone who reads it. "
    "Strike the phrase and his testimony can still be taken."), handout="exhibit-f")
evidence("exhibit-g", "Exhibit G: The True Roster", P(
    "The roster Hollis tries to carry away on the administrative elevator. It proves the Vacant King's entrants were never validly "
    "registered."), handout="exhibit-g")
evidence("exempt-receipt", "Receipt: EXEMPT FROM FRAUDULENT FEES", P(
    "A tiny brass receipt from the Counting Gate imps. One use: present it to void a fraudulent fee or surcharge."), img="ic-receipt")
evidence("janella-core", "Janella's Infernal-Glass Core", P(
    "The Iron Warder's stolen heart. Inserted into the Warder it wakes the construct with its original defensive orders and a "
    "perfect recording of Kane's sale. Giving it to Misty or Bel earns a different faction promise and may make Janella an "
    "enemy."), img="ic-core")
evidence("forge-ledger", "Janella's Forge Ledger", P(
    "Clue 1 of 3: identifies the Warder's controller as a removable infernal-glass heart with maker initials J.G."), img="ic-roster")
evidence("inverted-rune", "The Inverted Rune", P(
    "Clue 2 of 3: found beneath the mayor's study table; it matches the core's command socket."), img="ic-stamp")
evidence("custody-deed", "Misty's Custody Deed", P(
    "Clue 3 of 3: Misty's counsellor offers to return the core in exchange for 'the first authority exercised by the future "
    "regent'. A plainly disclosed bargain the players can reject."), img="ic-writ")
evidence("witness-name", "Witness Statement: Name", P(
    "The first hag witness's authentic birth-name testament. Suppresses the Seal of Name (Misty loses Magic Resistance for 2 full "
    "rounds)."), img="ic-lantern", folder=T)
evidence("witness-consent", "Witness Statement: Consent", P(
    "The custodian's document proving a soul copy was taken without consent. Suppresses the Seal of Consent (Misty's save DC "
    "becomes 22 for the rest of the encounter)."), img="ic-lantern", folder=T)
evidence("witness-jurisdiction", "Witness Statement: Jurisdiction", P(
    "The Brass Arbiter's order or the third witness's trust registry. Suppresses the Seal of Jurisdiction (Misty loses one unspent "
    "Legendary Resistance and cannot use Counterclaim for 2 rounds)."), img="ic-lantern", folder=T)
for k, n, d in (("proof-survival", "Proof of Survival", "Certified by the Three Witnesses at the Ash Bridge, or any witnessed "
                 "act of endurance the Arbiter accepts."),
                ("proof-deviousness", "Proof of Deviousness", "Earned by activating the inverse circle correctly, or by honourable "
                 "ingenuity the Arbiter witnesses."),
                ("proof-dominion", "Proof of Dominion", "Earned by the voluntary sworn support of a meaningful group, a protective "
                 "mandate honestly secured, or a legitimate defence won.")):
    evidence(k, n, P(d, "Qualification for final investiture requires valid proof of Survival, Deviousness and Dominion "
                     "(Charter, Article II)."), img="ic-proof", folder=T)
CM = item("crown-mark", "Crown Mark", "loot", P(
    "A brass token stamped with the First Crown. Crown Marks are the Championship's scoring currency: earned in arenas, trials "
    "and witnessed deeds, spent on arena boons, and forfeited (if unspent) on withdrawal."),
    img=icon("ic-crownmark"), quantity=1, weight=0)
put(T, CM)
put(T, item("soul-coin-currency", "Soul-Coin of Avernus (currency)", "loot", P(
    "Hell's hard currency, minted from a trapped soul. Orro prices a regiment of names at thirty of them. Spending one is "
    "never morally neutral. For fuel, charges and the Soul Furnace rules, see the Soul Coin in <em>Infernal Machines &amp; Soul Coins</em>."), img=icon("ic-soulcoin"), weight=0))
import redline as _RL
_RL.build_items(put)
import soulforged as _SF
_SF.build_coins(item, put, _RL.ITEM_FOLDER, ITEMS[_RL.ITEM_FOLDER])
ITEMS = {k: ITEMS[k] for k in (R, E, T, _RL.ITEM_FOLDER, SR)}
