"""Interlude: The Redline Run, the Souljack Yard and the Soul Furnace Codex.

Adapted from the author's Redline Run insert, Soul Furnace Codex and Soul Coin Quick Sheet. The chase runs on the Claw Rift
scrolling map; the Souljack Yard is where the party gets its war machines and the soul coins to power them.
Ordinary soul-coin charges and fuel follow the established Avernus model. Echoes, Sparks, Heat, tuning, the coin
tables and liberation checks are campaign homebrew.
"""
from lib5e import *

MODK = MOD
P = lambda *x: "".join(f"<p>{y}</p>" for y in x)
FOLDER = "Interlude — The Redline Run"
ITEM_FOLDER = "Infernal Machines & Soul Coins"


def T(head, rows, cls="rc-table"):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def BOXH(title, body, cls="rc-box"):
    return f'<div class="{cls}"><h4>{title}</h4>{body}</div>'


def READ(body):
    return f'<div class="rc-readaloud">{body}</div>'


# =============================================================================== SOUL ECHOES
ECHOES = [
    ("01–10", "The Courier", "A runner, messenger or smuggler who died before a final delivery.",
     "Vehicle speed increases by 10 feet. This never adds extra Lead by itself.",
     "Ignore one stretch of difficult terrain this round, and grant +2 to the convoy's end-of-round Lead check (subject to the +4 cap).",
     "Repeats an address, begging for one last message to be delivered."),
    ("11–18", "The Lancer", "A cavalry officer, outrider or chariot champion.",
     "The first ram made by this vehicle each round deals +1d4 damage on a hit.",
     "The next ram before the end of the turn deals +2d8 piercing damage; the target driver makes a DC 16 Strength save or shifts one lane.",
     "Insists the engine be pointed toward a worthy foe."),
    ("19–27", "The Artificer", "A smith, golemancer or enginewright who remembers every broken gear.",
     "Engineers gain +2 on checks to repair this vehicle.",
     "Restore 3d10 vehicle hit points without expending a repair kit. The machine must be above 0 HP.",
     "Knows a maker's mark or a schematic relevant to a campaign construct."),
    ("28–36", "The Scout", "A pathfinder who learned to survive impossible roads.",
     "Crew gain +2 on Perception or Survival checks to spot and navigate road hazards.",
     "Reroll the next road hazard this round and choose either result; gain advantage on one check to avoid it.",
     "Warns of dangers before anyone else can see them."),
    ("37–45", "The Thief", "An infiltrator, escape artist or fugitive.",
     "The driver gains +2 on checks to evade pursuit; riders gain +2 on boarding checks.",
     "Sever one nonmagical snare or harpoon line affecting the vehicle and immediately change one lane without a maneuver check.",
     "Offers the name of someone who sold them out."),
    ("46–54", "The Fire Adept", "A pyromancer, furnace-priest or careless arsonist.",
     "The first hit each round with a vehicle weapon that deals fire damage gains +1d4 fire damage.",
     "A 15-foot cone erupts from the engine: DC 16 Dexterity save, 3d8 fire damage on a failure, half on a success. It can hit allies.",
     "Laughs when the exhaust flames change colour."),
    ("55–63", "The Healer", "A physician, hospice worker or battlefield medic.",
     "Successful vehicle repairs restore 3 additional hit points.",
     "Choose one: a rider regains 3d8 hit points, or the vehicle regains 2d10 hit points. Neither works on the dead or a wreck.",
     "Asks the crew to save someone instead of winning a race."),
    ("64–71", "The Warlord", "A commander whose voice is louder than the engine.",
     "Embarked allies gain +1 on saving throws against being frightened.",
     "An allied vehicle within 60 feet gains 10 temporary hit points and +2 on its next driving check before the end of the next round.",
     "Gives orders even when no one wants to follow."),
    ("72–79", "The Magistrate", "An advocate, judge, clerk or infernal contract drafter.",
     "Crew gain +2 on Investigation, Religion or Persuasion checks made to examine or contest an infernal writ.",
     "Add +2 to one crew member's check to contest a contract; or one legal-enforcement construct within 60 feet makes a DC 16 "
     "Charisma save or suspends one ongoing non-damaging lien effect until the end of its next turn.",
     "Knows which seal, signature or date has been forged."),
    ("80–86", "The Penitent", "A redeemed sinner or faithful martyr who refuses to surrender compassion.",
     "Reduce the first instance of fire damage the vehicle takes each round by 3 (after resistance).",
     "End the frightened condition on all embarked allies; one devil within 30 feet makes a DC 16 Wisdom save or is blinded until the end of its next turn.",
     "Whispers a prayer that the engine cannot drown out."),
    ("87–94", "The Berserker", "A pit fighter whose dying rage still wants motion.",
     "When this vehicle Overburns, reduce its self-inflicted fire damage by 1d6 (minimum 0).",
     "The next ram before the end of the turn deals +2d8 bludgeoning damage; the vehicle takes 1d8 recoil damage that bypasses its damage threshold.",
     "Challenges every driver to go faster."),
    ("95–00", "The Planar Cartographer", "A traveller who saw paths between realities.",
     "The driver gains +2 on Arcana checks to navigate planar anomalies.",
     "Teleport the vehicle and embarked occupants up to 30 feet to visible unoccupied ground, ignoring one immediate terrain hazard. "
     "This does not cross a planar barrier or end a chase automatically.",
     "Knows a dangerous shortcut toward the Brass Citadel."),
]
ECHO_WEIGHTS = [10, 8, 9, 9, 9, 9, 9, 8, 8, 7, 8, 6]
VOICES = ["Terrified, pleading", "Angry, accusatory", "Grief-stricken and distant", "Coldly calculating", "Quietly courageous",
          "Eager to bargain", "Deliriously joyful", "Refuses to speak"]
CLAIMS = [("Valid debt, correctly signed", "The coin can be bought or used; no objection lies."),
          ("Signature forged", "An objection wins outright once the forgery is proved."),
          ("Debt already paid", "Proof of payment wins an objection automatically."),
          ("Captive of a night hag", "Misty's coven holds the original; expect a MIST-113 seal."),
          ("Claim sold twice", "Two creditors; neither holds clean title. A DC 16 check finds the second sale."),
          ("No recorded title", "No one may lawfully sell this coin. It can be confiscated and freed.")]
FURNACE_MISHAPS = ["<strong>Clogged pistons.</strong> Vehicle speed is halved until the end of its next turn.",
                   "<strong>Choir of pain.</strong> The driver makes a DC 15 Wisdom save or has −2 on the next driving check.",
                   "<strong>Fuel-line burst.</strong> The vehicle takes 2d10 fire damage that bypasses its damage threshold.",
                   "<strong>Locked steering.</strong> The next lane change is made at disadvantage.",
                   "<strong>Ghost hands on the controls.</strong> The driver passes DC 15 Dexterity (land vehicles) or shifts one lane.",
                   "<strong>An infernal seal flashes.</strong> One pursuing creditor knows the vehicle's location for 1 hour."]
VEHICLE_MISHAPS = [("Steering pins seize; disadvantage on the next driving check.", "DC 15 Strength or tools action"),
                   ("Flame cough: exposed occupants take 2d6 fire damage.", "Automatic after this pulse"),
                   ("Axle cracks; speed reduced by 30 feet.", "DC 15 tools action and one repair kit"),
                   ("Soul furnace screams; all riders on the machine make a DC 14 Wisdom save or lose their reactions until next turn.", "Automatic at end of round"),
                   ("Weapon jam: one chosen hardpoint cannot fire.", "DC 15 tinker's tools action"),
                   ("Hull breach: the vehicle takes an extra 2d10 fire damage.", "Repair normally")]
HAZARDS = [("The needle field", "Drift around it (DC 15 driving) or ram through. Failure: 3d10 piercing to the vehicle and −1 Lead."),
           ("Soulfire geyser", "Avoid with DC 16 driving or take 2d10 fire to the hull; exposed riders take 2d6 fire (DC 15 Dexterity for half)."),
           ("River Styx runoff", "Detour (−1 Lead) or jump the channel with DC 17 driving. Failure: 3d10 bludgeoning to the hull; riders make DC 14 Wisdom or have disadvantage on their next skill check."),
           ("Living chain web", "One random vehicle is snared (chains AC 16, 20 HP, or DC 16 Strength to break); −1 Lead while snared."),
           ("Sliding claw-teeth", "Choose a lane, then DC 16 driving. Failure: collision, 3d10 bludgeoning plus 2d10 fire to the hull."),
           ("Writstone toll arch", "Pass beneath with DC 17 Arcana to disable the scan, or detour (−1 Lead). On a failure the archive reveals the fake repossession claim, but deals 2d8 psychic damage to one operator.")]
ENEMY = [("The plow", "The Reclaimer attempts a ram on the nearest adjacent vehicle."),
         ("The tax hook", "The harpoon targets the machine carrying the heart."),
         ("Sear and scatter", "Flame sluice if available; otherwise a quad's chain flail aims at an exposed rider."),
         ("Official notice", "Kestrel issues a legal objection or tries to verify the heart's seal."),
         ("Flanking riders", "The quads change lanes to make boarding possible next round."),
         ("Forced boarding", "The winch operator launches its hook; Reavers try to board, not to kill.")]
EXAMPLE_SOULS = [
    ("tarnik", "Tarnik Blackspoke", "Lancer", "An Avernian outrider falsely blamed for abandoning his squad. He wants their graves "
     "found. His Pulse is devastating on a Cinderfang Spiker, and his sworn enemy knows the real story.", 3, "Signature forged"),
    ("ysera", "Ysera Quill", "Magistrate", "A clerk who refused to validate Misty's forged chain of title. A MIST-113 stamp covers "
     "her original docket number. If Queried, she can name the crucial missing signature. (If Aurelia Quill is in play, Ysera "
     "is her great-aunt, and Aurelia knows the name.)", 2, "Captive of a night hag"),
    ("merrow", "Merrow Kindhand", "Healer", "A battlefield surgeon who treated enemies as readily as allies. She refuses to help a "
     "crew that attacks refugees, and pleads for her family's release.", 3, "Debt already paid"),
    ("sevrin", "Sevrin Nine-Roads", "Planar Cartographer", "A trader who mapped a way from the Blackspine Narrows to the Brass "
     "Citadel. The route lies in a song he taught his daughter.", 1, "Claim sold twice"),
]

# =============================================================================== RULES TEXT (shared)
QUICK = T(["Step", "Procedure"], [
    ["<strong>1 · Identify</strong>", "Action; DC 14 Intelligence (Arcana or Religion). Reveals the Echo, the soul's emotional tone, "
     "its remaining charges and any visible legal seal. It does not let you question the soul."],
    ["<strong>2 · Feed</strong>", "Driver's bonus action. The whole coin is consumed and its soul enters the furnace. Each "
     "remaining charge gives 24 hours of fuel and 1 Resonance Spark."],
    ["<strong>3 · Tune</strong>", "Only one Echo is active per engine. Engineer's action and DC 15 Intelligence (Arcana or "
     "tinker's tools) switches to another bound soul. Failure wastes the action."],
    ["<strong>4 · Pulse</strong>", "Driver's bonus action or engineer's action. Spend 1 Spark and gain 1 Heat. One Pulse per "
     "vehicle per round."],
    ["<strong>5 · Release</strong>", "Stop the engine, then use a consecrated focus and an action: DC 18 Arcana or Religion, or "
     "suitable curse-removing magic. On a success that soul is freed and its fuel and Echo end."]])
HEAT = T(["Heat", "Effect"], [["0–2", "Stable. No adverse effect."], ["3–4", "Strained. The engine screams; a warning, not a penalty."],
                              ["5", "Critical. Each further Pulse or Overburn triggers a furnace mishap on a d6 roll of 1–2."],
                              ["6", "Rupture. The vehicle takes 3d10 fire damage that bypasses its threshold; roll a vehicle mishap; reset Heat to 3."]])
ENERGY = P(
    "<strong>Resonance Sparks.</strong> A coin contributes Sparks equal to its remaining charges when fed (1–3). Sparks never "
    "recharge. Fuel durations stack; Echo bonuses don't. Track each bound soul by name, with its own Sparks.",
    "<strong>Heat.</strong> Gain 1 Heat for each Pulse or Overburn. An engineer can use an action and DC 15 Intelligence "
    "(tinker's tools) to remove 2 Heat (1 on a failure). At the end of a round with neither a Pulse nor an Overburn, remove 1 Heat.",
    "<strong>Crew.</strong> Weapons need a gunner's action; magic and boarding use the rider's own action. Echoes never give "
    "the vehicle a free turn. All bonuses obey the chase limits: +4 maximum to a check, and Lead moves at most 2 steps a round.")
HANDLING = P(
    "<strong>Before the coin enters an engine.</strong> Holding a coin lets you sense the soul's emotion without a check. "
    "Identify (DC 14) reveals the Echo, attitude, charges and seal. To ask the soul a factual question, use the coin's ordinary "
    "Query, which spends a charge; the soul knows only what it knew in life. Drain Life also spends a charge and grants "
    "temporary hit points. When the last charge is spent the coin crumbles and the soul goes free.",
    "<strong>Charges.</strong> A fresh coin holds 3 charges; a used one 1 or 2. Salvaged coins: roll d6 (1–2 one charge, 3–4 "
    "two, 5–6 three). No coin ever holds more than 3 charges or gives more than 3 Sparks.",
    "<strong>When fuel runs out.</strong> A soul burned as fuel to the end is destroyed. That is what the engines sing about.",
    "<strong>Legal play.</strong> A printed lien does not override the soul's real contract. An action and DC 16 Investigation "
    "or Religion finds an inconsistency in a recorded claim. At an infernal tribunal, DC 18 Persuasion or Religion wins a "
    "temporary stay when evidence is incomplete; authenticated proof of forgery, a paid debt or a missing grant of title wins "
    "the objection outright. A stay blocks seizure but does not by itself free a soul.",
    "<strong>Misty's black seal.</strong> A coin stamped MIST-113 is claimed by the Hell Hag Queen's agents. An invented docket, "
    "stolen maker's mark or voided debt invalidates the claim; the seal gives no special magical ownership. The bound soul may "
    "know who applied it.",
    "<strong>Liberation.</strong> A failed release attempt can be retried after 10 minutes and deals 1d6 psychic damage to the "
    "liberator, never to the soul. Other souls in the furnace keep the engine running. A freed soul may leave one parting gift: "
    "a true secret, a map clue, or advantage on one future check.",
    "<strong>Demon ichor.</strong> A flask runs a machine for 8 hours at −20 feet speed, with a 1-in-6 chance of a mishap "
    "whenever it Overburns. Ichor engines have no Echo. It is unstable, but it burns no one.")
LIMITS = ('<p class="rc-fine"><em>Rules boundary:</em> ordinary soul-coin charges and fuel follow the established Avernus war-machine '
          'model. Echoes, Sparks, Heat, tuning, the coin tables and liberation checks are campaign homebrew for Interplanal Champions.</p>')


def echo_table():
    return T(["d100", "Soul", "Echo (passive while active)", "Pulse (1 Spark, +1 Heat)", "Voice"],
             [[r, f"<strong>{n}</strong><br><em>{w}</em>", e, p, v] for r, n, w, e, p, v in ECHOES])


def origin_tables():
    return (T(["d8", "What the voice sounds like"], [[i + 1, v] for i, v in enumerate(VOICES)])
            + T(["d6", "Claim record", "What it means"], [[i + 1, a, b] for i, (a, b) in enumerate(CLAIMS)]))


def codex_html(players=False):
    """The Soul Furnace Codex: full rules, used in Book II (players) and in Book I's interlude (GM)."""
    return (P("<em>Every soul coin is a person.</em> An infernal engine is not merely a furnace. It is a prison, a fuel tank "
              "and a choir of memories, and who the trapped soul was changes what the war machine can do.")
            + "<h3>Quick Play: Five Steps</h3>" + QUICK
            + "<h3>Energy, Heat and Crew</h3>" + ENERGY + HEAT
            + "<h3>Soul Echoes (d100)</h3>" + P("Roll when a soul coin enters play. The Echo comes from who the soul was in life, "
                                                 "not whether they were good or evil.") + echo_table()
            + "<h3>Handling, Consent and Legal Claims</h3>" + HANDLING + origin_tables()
            + "<h3>Furnace Mishaps (d6)</h3>" + T(["d6", "Mishap"], [[i + 1, x] for i, x in enumerate(FURNACE_MISHAPS)])
            + "<h3>Example Souls</h3>" + "".join(f"<p><strong>{n} ({e}).</strong> {d}</p>" for _, n, e, d, _, _ in EXAMPLE_SOULS)
            + "<h3>Which Soul for Which Machine</h3>"
            + T(["War machine", "Recommended soul", "What it changes"],
                [["Scorchhound Quad", "Courier or Scout", "Faster recon, hazard avoidance, route-breaking escapes."],
                 ["Cinderfang Spiker", "Lancer or Berserker", "Harder rams and high-risk interception."],
                 ["Souljack Hauler", "Artificer or Healer", "Keeps crew and cargo alive; repairs under fire."],
                 ["Iron Reclaimer", "Magistrate or Warlord", "Enforcement authority and control of allied vehicles."]])
            + "<h3>Worked Example</h3>"
            + P("The party feeds a 2-charge Scout coin to its Souljack Hauler: 48 hours of fuel, 2 Sparks, Heat 0.")
            + "<ul><li><strong>Round 1:</strong> the engineer Pulses, rerolling a claw-teeth hazard (Sparks 1, Heat 1).</li>"
              "<li><strong>Round 2:</strong> the driver Overburns for +2 on the Lead check, taking 2d10 fire damage (Heat 2).</li>"
              "<li><strong>Round 3:</strong> no Pulse or Overburn, so Heat falls to 1.</li></ul>"
            + P("The Scout's passive +2 to hazard checks stays on throughout. If the soul is freed at a stopped engine, its Echo "
                "and its remaining fuel vanish together.")
            + LIMITS)


# =============================================================================== ACTORS
def build_actors():
    """Returns a list of actor docs; called by bestiary after its own folders are built."""
    from bestiary import Mon, make, put, BONUS, REACT, SPECIAL, R, USE1, P as BP
    m = Mon("kestrel")
    m.trait("Licensed Bailiff", "Kestrel may confiscate the property named in a writ: never a soul, a passenger or unrelated "
            "cargo. If he ignores a granted stay he loses lawful seizure and can only steal the heart by force, and the breach "
            "becomes evidence (a potential Crown Mark for the party).")
    m.trait("Magic Resistance", "Kestrel has advantage on saving throws against spells and other magical effects.")
    m.multi("Kestrel makes two Iron Clause attacks.")
    m.atk("Iron Clause", 8, [dmg(2, 10, 4, ["slashing"]), dmg(1, 6, "", ["necrotic"])], reach=10, img="ic-chain")
    m.atk("Claimant's Brand", 8, [dmg(3, 8, "", ["force"])], kind="ranged", cls="spell", rng_=90, img="ic-hex")
    m.util("Counterclaim (2/chase)", "<p><em>Reaction.</em> When a character within 60 feet makes an unsupported legal check, "
           "reduce the result by 1d6. This cannot affect a documented automatic legal victory.</p>", act=REACT(),
           uses_=uses(2, ["lr"]), consumption=USE1, roll=("-1d6", "Counterclaim"))
    m.util("Order the Escort", "<p><em>Bonus action.</em> One Cinderfang driver immediately shifts one lane or takes the Help "
           "action. It gains no extra attack.</p>", act=BONUS())
    make(FOLDER, "kestrel-vane", "Marshal Kestrel Vane, Licensed Road Bailiff", m, ctype="fiend", subtype="devil",
         alignment="lawful evil", cr=9, ac=18, hp=112, hp_formula="15d8+45", speed=30, abilities=(18, 16, 18, 16, 14, 18),
         saves=("dex", "wis", "cha"), dr=("fire", "necrotic"), di=("poison",), ci=("poisoned",),
         senses={"darkvision": 120}, langs=("infernal", "common"), lang_custom="telepathy 60 ft.",
         bio=BP("Misty's subcontracted repossession marshal. Kestrel earns a percentage of recovered property. He knows the "
                "writ is questionable, but believes a court will vindicate him if the witnesses die. At half his hit points he "
                "will bargain for immunity and an escort out of the canyon. Suggested CR 9–10 in vehicle play."))
    m = Mon("reaver")
    m.trait("Saddle Grip", "<em>Reaction, once per round.</em> The Reaver has advantage on its next save against being thrown "
            "from a moving machine.")
    m.atk("Chain Lash", 7, [dmg(2, 8, 3, ["slashing"])], reach=10, img="ic-chain")
    m.atk("Scrap Pistol", 7, [dmg(2, 6, 3, ["piercing"])], kind="ranged", rng_="30/90", img="ic-needle")
    make(FOLDER, "ash-road-reaver", "Ash-Road Reaver", m, ctype="fiend", subtype="devil", alignment="lawful evil", cr=3, ac=16,
         hp=52, hp_formula="8d8+16", speed=30, abilities=(14, 16, 14, 10, 11, 10), saves=("dex",), dr=("fire",),
         di=("poison",), ci=("poisoned",), senses={"darkvision": 120}, langs=("infernal",),
         bio=BP("Repossession riders. Each Cinderfang carries a Reaver driver and a Reaver gunner, or a single rider in a short "
                "session. The Reclaimer's devil gunner and winch operator also use this stat block."))
    m = Mon("grisk")
    m.trait("Licensed Broker", "Grisk trades coins under licence from the Ninth Sorting Annex. He must show the claim record of "
            "any coin he sells on request. Proving a defective claim (DC 16 Investigation or Religion) obliges him to surrender "
            "the coin; he grumbles, but the licence matters more to him than one coin.")
    m.trait("Coward's Ledger", "When reduced below half his hit points, Grisk offers his entire stock to whoever stops hurting "
            "him, and means it.")
    m.atk("Ledger Hook", 5, [dmg(2, 6, 3, ["piercing"])], img="ic-chain")
    make(FOLDER, "broker-grisk", "Broker Grisk Tallowmere, Coin-Broker of the Ninth Sorting Annex", m, ctype="fiend",
         subtype="devil", alignment="lawful evil", cr=2, ac=14, hp=45, hp_formula="7d8+14", speed=30,
         abilities=(12, 12, 14, 16, 14, 16), skills={"ins": 6, "per": 7, "inv": 5}, dr=("fire",), di=("poison",),
         ci=("poisoned",), senses={"darkvision": 120}, langs=("infernal", "common", "abyssal"), disposition=0,
         bio=BP("A bearded devil in a merchant's coat, ringed with brass scales and a sack that hums. He runs the coin booth "
                "in the Souljack Yard and sells fuel to anyone with something to trade. He would rather be paid than be right."))

    def veh(key, name, size, ac, hp, dt, mt, speed, abil, crew, pax, stations, bio, feats):
        m = Mon(key)
        for f in feats:
            f(m)
        tsz = {"lg": 2, "huge": 3}[size]
        a = {"_id": fid("actor:" + key), "name": name, "type": "vehicle", "img": portrait(key), "sort": 0, "folder": None,
             "system": {
                 "abilities": {k: {"value": v, "proficient": 0} for k, v in zip(("str", "dex", "con", "int", "wis", "cha"),
                                                                                  abil + (0, 0, 0))},
                 "attributes": {"ac": {"flat": ac, "calc": "flat"}, "hp": {"value": hp, "max": hp, "dt": dt, "mt": mt},
                                "movement": {"walk": speed, "units": "ft"}, "capacity": {"creature": f"{crew} crew, {pax} passengers"},
                                "actions": {"stations": True, "max": 0, "spent": 0}},
                 "details": {"biography": {"value": bio, "public": ""}, "type": "land"},
                 "traits": {"size": size, "di": {"value": ["poison", "psychic"], "bypasses": [], "custom": ""},
                            "ci": {"value": ["blinded", "charmed", "deafened", "frightened", "paralyzed", "petrified",
                                             "poisoned", "stunned", "unconscious"], "custom": ""},
                            "dimensions": stations},
                 "source": SOURCE},
             "prototypeToken": proto_token(name, tok(key), tsz, 0), "items": m.items, "effects": [],
             "flags": {MODK: {"vehicle": True}}, "_stats": STATS}
        return put(FOLDER, a)

    COMMON = ("<p><strong>Infernal war machine.</strong> An object, immune to poison and psychic damage and to the charmed, "
              "frightened and poisoned conditions. The machine never acts on its own; every weapon needs a crew member's action.</p>"
              "<ul><li><strong>Damage threshold:</strong> one instance of damage below it deals 0.</li>"
              "<li><strong>Mishap threshold:</strong> a single hit meeting it triggers a d6 vehicle mishap.</li>"
              "<li><strong>Fuel:</strong> soul coins (Soul Furnace Codex) or demon ichor.</li></ul>")
    veh("scorchhound-quad", "Scorchhound Quad", "lg", 16, 68, 10, 25, 130, (16, 17, 14), 1, 1, "Helm, chain-bow",
        P("Compact and fast, with ragged blades and a twin-piston soul furnace: a warlord's favourite scout bike. It handles tight "
          "lanes with advantage on checks to avoid the claw-teeth. The driver has half cover from the engine cage.") + COMMON,
        [lambda m: m.atk("Chain-Bow (passenger station)", 7, [dmg(2, 10, "", ["piercing"])], kind="ranged", rng_="60/180",
                         desc="Once per round, on a hit against a vehicle, its driver makes a DC 15 Strength save or cannot "
                              "Overburn until the end of its next turn. The line can be cut (AC 16, 15 HP).", img="ic-chain"),
         lambda m: m.util("Spike-Dash (driver, once per chase)", "<p>After a successful DC 16 Dexterity (land vehicles) check, "
                          "increase Lead by 1 and take 1d10 slashing damage from scorching debris. Uses the driver's action and "
                          "counts toward the two Lead changes a round.</p>", roll=("1d10", "Debris damage"))])
    veh("cinderfang-spiker", "Cinderfang Spiker", "lg", 17, 78, 10, 25, 115, (18, 15, 16), 1, 1, "Helm, side blades",
        P("Scarred black iron wheels, hooked blades and a burner tuned to make crowds panic. These are Misty's escort bikes, but "
          "the party may steal one.") + COMMON,
        [lambda m: m.atk("Sideblade (driver, while adjacent, once per round)", 8, [dmg(3, 10, "", ["slashing"])],
                         desc="Against a creature the blade deals 3d6 slashing instead. A hit on a vehicle imposes −2 on that "
                              "driver's next maneuver check. Replaces another driving stunt that turn.", img="ic-glaive"),
         lambda m: m.atk("Chain Flail (passenger station)", 7, [dmg(2, 8, 3, ["bludgeoning"])], kind="ranged", rng_="30/90",
                         desc="An exposed rider hit makes a DC 15 Strength save or is knocked prone on its vehicle; it falls "
                              "only if it then moves recklessly or fails another balance check.", img="ic-chain")])
    veh("souljack-hauler", "Souljack Hauler", "huge", 18, 175, 15, 45, 95, (22, 12, 20), 4, 3,
        "Helm, harpoon, furnace gun, engineer",
        P("A survivor-built armoured mule. Seated riders have half cover; one creature in the armoured cargo locker has "
          "three-quarters cover. Its engine can be detached for maintenance and its central cage can carry the infernal-glass "
          "heart. It carries 3 repair kits and 6 harpoons.") + COMMON,
        [lambda m: m.atk("Chain Harpoon (gunner)", 8, [dmg(3, 10, "", ["piercing"])], kind="ranged", rng_="120/240",
                         desc="The target vehicle makes a DC 16 Strength save or is Snared while the chain holds: −2 on its next "
                              "Lead-related driver check. Remove the chain with an action and DC 16 Strength, or cut it (AC 16, 20 HP).",
                         img="ic-chain"),
         lambda m: m.atk("Furnace Gun (gunner; 4 ash cartridges)", 7, [dmg(4, 8, "", ["fire"])], kind="ranged", rng_="90/180",
                         desc="On a natural 1 the gun jams; clearing it takes an action and DC 15 tinker's tools.", img="ic-embers"),
         lambda m: m.trait("Shield Plating", "The hauler takes half damage from the first ram against it each round (before "
                           "its damage threshold). At the DM's discretion it can shield an allied quad in the same lane instead.")])
    veh("iron-reclaimer", "Iron Reclaimer, the Black Invoice", "huge", 19, 220, 18, 50, 85, (24, 10, 22), 4, 2,
        "Helm, tax harpoon, flame sluice, boarding winch",
        P("Black armour plated like legal books, a furnace of bound souls, and an execution plow hung with forged repossession "
          "certificates. It belongs to Misty's subcontractor, not to her. It carries 2 repair kits.") + COMMON,
        [lambda m: m.atk("Execution Plow (driver, while adjacent)", 9, [dmg(4, 10, 6, ["bludgeoning"])],
                         desc="On a hit the Reclaimer takes 1d10 recoil damage, and the target driver makes a DC 16 Strength "
                              "save or shifts one lane toward the claw-teeth.", img="ic-slam"),
         lambda m: m.atk("Tax Harpoon (gunner)", 8, [dmg(3, 10, "", ["piercing"])], kind="ranged", rng_="120/240",
                         desc="The target vehicle makes a DC 17 Strength save or is Snared: while the chain holds, its convoy "
                              "loses 1 Lead at the end of each round. The chain has AC 17 and 25 HP, or break it with an action "
                              "and DC 17 Strength.", img="ic-chain"),
         lambda m: m.sv("Flame Sluice (gunner)", "dex", 16, [dmg(4, 8, "", ["fire"])],
                        "Each creature and vehicle in a 30-foot cone makes a DC 16 Dexterity save, taking 4d8 fire damage on a "
                        "failure or half on a success. Riders behind full cover are not hit.", area=("cone", 30), img="ic-embers",
                        uses_=R(5)),
         lambda m: m.util("Boarding Winch (operator)", "<p>Grapple check +7 against a vehicle's AC, up to 30 feet. On a hit the "
                          "Reclaimer latches on and the two count as alongside for boarding and melee until the hook is cut "
                          "(DC 16 Athletics, DC 16 tools, or 20 damage to the AC 16 chain).</p>", roll=("1d20 + 7", "Winch grapple"))])


# =============================================================================== ITEMS
def build_items(item_put):
    U = consume_item_uses()

    def coin(key, name, desc, img="ic-soul-coin", charges=3, price=0):
        return item_put(ITEM_FOLDER, item(key, name, "consumable", desc, img=icon(img), subtype="trinket", price=price,
                                          weight=0, uses_=uses(charges, []),
                                          activities=[heal_act(f"{key}-drain", 0, formula_part=dmg_formula("1d10"), temp=True,
                                                               name="Drain Life (1 charge)", consumption=U,
                                                               tgt=target("", "self")),
                                                      utility(f"{key}-query", 1, name="Query (1 charge)", consumption=U),
                                                      utility(f"{key}-identify", 2, name="Identify the Echo (DC 14 Arcana or Religion)"),
                                                      utility(f"{key}-feed", 3, name="Feed to a Furnace (driver's bonus action)",
                                                              act=activation("bonus", 1))]))
    base = ("<p>A heavy iron coin, warm to the touch, with a face in its centre that is not quite a stamp. It holds a trapped "
            "soul and up to 3 charges. <strong>Drain Life</strong> spends a charge for 1d10 temporary hit points. "
            "<strong>Query</strong> spends a charge to ask the soul one question; it knows only what it knew in life. When "
            "the last charge is spent the coin crumbles and the soul goes free.</p>"
            "<p><strong>As fuel.</strong> Fed to an infernal engine (driver's bonus action), the whole coin is consumed: each "
            "remaining charge gives 24 hours of fuel and 1 Resonance Spark. Roll its Echo (d100), voice (d8) and claim record "
            "(d6) on the Soul Furnace tables. A soul burned to the end is destroyed.</p>")
    coin("soul-coin", "Soul Coin", base + "<p class='rc-fine'>Salvaged coins: roll d6 for charges (1–2 one, 3–4 two, 5–6 three).</p>")
    for k, n, e, d, ch, claim in EXAMPLE_SOULS:
        coin(f"soul-coin-{k}", f"Soul Coin: {n} ({e})", base + f"<p><strong>The soul.</strong> {d}</p>"
             f"<p><strong>Charges</strong> {ch}. <strong>Claim record:</strong> {claim}.</p>",
             img="ic-soul-coin-mist" if k == "ysera" else "ic-soul-coin", charges=ch)
    item_put(ITEM_FOLDER, item("demon-ichor", "Flask of Demon Ichor", "consumable", P(
        "A stoppered flask of black, faintly warm blood. Poured into an infernal furnace it runs the machine for 8 hours at −20 "
        "feet speed. Whenever the machine Overburns on ichor, roll a d6: on a 1, roll a furnace mishap. An ichor engine has no "
        "Echo and burns no soul."), img=icon("ic-drain"), subtype="potion", price=100, weight=1,
        uses_=uses(1, []), activities=[utility("ichor-fuel", 0, name="Fuel a Furnace (8 hours)", act=activation("bonus", 1),
                                                consumption=U)]))
    item_put(ITEM_FOLDER, item("repair-kit", "War-Machine Repair Kit", "consumable", P(
        "Scrap iron, rivets and a pot of hellforge flux. An engineer with smith's or tinker's tools uses an action and makes a "
        "DC 15 Intelligence check to restore 2d10 + 5 hit points to a vehicle. The kit is spent even on a failure."),
        img=icon("ic-hammer"), subtype="trinket", price=50, weight=10, uses_=uses(1, []),
        activities=[check_act("rk-check", 0, ability="int", dc=15, name="Repair check (DC 15)"),
                    heal_act("rk-heal", 1, formula_part=dmg_formula("2d10 + 5"), name="Restore vehicle HP", consumption=U)]))
    item_put(ITEM_FOLDER, item("writ-seal", "Brass Writ-Seal", "consumable", P(
        "Kestrel Vane's seal of office. Once, before rolling, you can press it to a document to gain advantage on a genuine "
        "contract-jurisdiction check. Then it cracks."), img=icon("ic-stamp"), subtype="trinket", weight=0, uses_=uses(1, []),
        activities=[utility("ws-use", 0, name="Press the seal (advantage on one jurisdiction check)", consumption=U)]))
    item_put(ITEM_FOLDER, item("writ-m9r", "Exhibit: Provisional Writ M-9-R", "loot", P(
        "Misty's writ of contested salvage over the infernal-glass heart JG-09. It is knowingly defective: Janella never "
        "abandoned her property, the 'abandonment' affidavit was signed by someone who never lived in Greyhurst, and notice was "
        "served at an address that was never hers. Presented with Janella's maker-mark it wins an emergency stay outright.")
        + f"<p class='rc-fine'>Handout: {uuid_journal('handouts', 'writ-m9r', 'read the writ')}</p>", img=icon("ic-exhibit"), weight=0))
    item_put(ITEM_FOLDER, item("loan-g12", "Greyhurst Reclamation Loan (Form G-12)", "loot", P(
        "The vehicle loan. Its security is the vehicles and installed equipment only; cargo, liberty, memories, names and souls "
        "are expressly excluded.") + f"<p class='rc-fine'>Handout: {uuid_journal('handouts', 'loan-g12', 'read the loan')}</p>",
        img=icon("ic-exhibit"), weight=0))


# =============================================================================== TABLES
def build_tables(table):
    table("soul-echo", "Soul Echo (d100)", "1d100",
          [(f"<strong>{n}.</strong> {w} <em>Echo:</em> {e} <em>Pulse:</em> {p} <em>Voice:</em> {v}", wgt)
           for (r, n, w, e, p, v), wgt in zip(ECHOES, ECHO_WEIGHTS)],
          "Roll when a soul coin enters play. Pulse costs 1 Spark and adds 1 Heat; one Pulse per engine per round.", icon("ic-soul-coin"))
    table("soul-voice", "Soul Coin: What the Voice Sounds Like (d8)", "1d8", VOICES, "", icon("ic-soul-coin"))
    table("soul-claim", "Soul Coin: Claim Record (d6)", "1d6", [f"<strong>{a}.</strong> {b}" for a, b in CLAIMS],
          "A printed lien does not override the soul's real contract.", icon("ic-soul-coin-mist"))
    table("soul-charges", "Salvaged Soul Coin: Charges (d6)", "1d6", ["1 charge", "1 charge", "2 charges", "2 charges",
                                                                    "3 charges", "3 charges"], "", icon("ic-soul-coin"))
    table("furnace-mishap", "Furnace Mishap (d6)", "1d6", FURNACE_MISHAPS, "Heat 5: each Pulse or Overburn mishaps on a 1–2.",
          icon("ic-embers"))
    table("vehicle-mishap", "Vehicle Mishap (d6)", "1d6", [f"{a} <em>Remedy:</em> {b}" for a, b in VEHICLE_MISHAPS],
          "Whenever a single hit meets a vehicle's mishap threshold.", icon("ic-embers"))
    table("road-hazard", "Redline Run: Road Hazard (d6)", "1d6", [f"<strong>{a}.</strong> {b}" for a, b in HAZARDS],
          "Roll at the start of each round after round 1 and announce it before anyone acts.", icon("ic-arena"))
    table("enemy-plan", "Redline Run: Enemy Plan (d6)", "1d6", [f"<strong>{a}.</strong> {b}" for a, b in ENEMY],
          "Roll openly before the characters act, and follow it unless a creature becomes unable to.", icon("ic-arena"))


TABLE_KEYS = ["soul-echo", "soul-voice", "soul-claim", "soul-charges", "furnace-mishap", "vehicle-mishap", "road-hazard", "enemy-plan"]


# =============================================================================== HANDOUTS
def handouts(DOC, field_lines):
    loan = DOC("GREYHURST RECLAMATION LOAN · FORM G-12", P(
        "<strong>Lender:</strong> Janella Greenbottle, Vexa Corven or Broker Grisk Tallowmere, as signed. "
        "<strong>Borrower:</strong> the undersigned crew.",
        "<strong>Subject:</strong> one Souljack Hauler and up to three Scorchhound Quads.",
        "<strong>Term:</strong> until arrival at the Brass Citadel, or 72 hours by the Brass Registry chronometer, whichever "
        "comes first.",
        "<strong>Security:</strong> the loaned vehicles and installed equipment ONLY. Cargo, bodily liberty, memories, names and "
        "souls are expressly excluded.",
        "<strong>Use:</strong> the crew may repair, modify or exchange the vehicles with the lender's consent.",
        "<strong>Loss:</strong> if equipment is lost, the lender may seek its fair market value after an opportunity to contest "
        "the loss before a neutral Brass Registry clerk. No summary seizure is authorised.",
        "Both parties affirm voluntary agreement.") + field_lines("<p>Lender: ____________ Crew: ____________ Witness: ____________</p>"),
        stamp="FAIR TERMS", form="Form G-12")
    writ = DOC("COURT OF THE BARBED CHAIN · PROVISIONAL WRIT M-9-R", P(
        "<strong>Claimant:</strong> Misty, Queen of Barbed Chains.",
        "<strong>Respondent:</strong> Custodian of Infernal-Glass Golem Heart JG-09.",
        "<strong>Alleged basis:</strong> abandonment following the destruction of Greyhurst.",
        "<strong>Notice of pending seizure:</strong> served at the Ninth Sorting Annex, Avernus.",
        "<strong>Scope:</strong> one named mechanical heart and directly attached frame; not the bearer or the bearer's soul.",
        "<strong>Conditions:</strong> this claim is stayed by competent evidence of continued custody, the original maker's "
        "identification, or proof of defective notice. Appeal may be spoken before a licensed bailiff or entered with the Brass "
        "Registry.",
        "Signed under conditional seal, <em>Marshal K. Vane</em>."), stamp="REPOSSESSION", form="Writ M-9-R")
    quick = DOC("THE SOUL FURNACE · QUICK SHEET", QUICK + HEAT + P(
        "<strong>Overburn:</strong> +2 to the Lead check; 2d10 fire to the vehicle, bypassing its threshold; +1 Heat.",
        "<strong>Cool:</strong> engineer's action, DC 15, removes 2 Heat (1 on a failure); a quiet round removes 1.",
        "<strong>Identify</strong> DC 14 Arcana or Religion. <strong>Liberate</strong> at a stopped engine, DC 18 Arcana or "
        "Religion with a consecrated focus. A factual Query spends a normal coin charge."), form="Players' reference")
    row = "<tr><td>________________</td><td>________________</td><td>______ hours</td><td>___ / ___</td></tr>"
    tracker = DOC("SOUL FURNACE TRACKER", P("One line per trapped soul. Fill it in as you play.")
                  + field_lines('<table class="rc-table"><thead><tr><th>Name / Echo</th><th>Legal claim / seal</th><th>Fuel</th>'
                                '<th>Sparks</th></tr></thead><tbody>' + row * 4 + "</tbody></table>"
                                "<p>Vehicle: ____________ Active Echo: ____________</p>"
                                "<p>Heat: [0] [1] [2] [3] [4] [5] [6] · Lead: [0] [1] [2] [3] [4] [5] [6] · Round: 1 2 3 4 5 6 7 8</p>")
                  + P("<em>One Pulse per vehicle per round. +1 Heat for a Pulse or Overburn. Heat 5 risks mishaps; Heat 6 ruptures.</em>"),
                  form="Record sheet")
    dispute = DOC("INFERNAL SERVICE DISPUTE RECORD", field_lines(P(
        "Claimant: ________________ Docket: ________________",
        "Soul or engine at issue: ________________________________",
        "Clause cited by creditor: ________________________________",
        "Evidence of defect (signature, title, deadline, jurisdiction): ________________________________",
        "Remedy demanded: ☐ Stay ☐ Return of coin ☐ End of lien ☐ Release ☐ Other ____________")), form="Brass Registry")
    return [("loan-g12", "Handout 17 — Greyhurst Reclamation Loan (Form G-12)", loan),
            ("writ-m9r", "Handout 18 — Provisional Writ M-9-R", writ),
            ("furnace-quick", "Handout 19 — The Soul Furnace Quick Sheet", quick),
            ("furnace-tracker", "Handout 20 — Soul Furnace Tracker", tracker),
            ("dispute-record", "Handout 21 — Infernal Service Dispute Record", dispute)]


# =============================================================================== BOOK I PAGES
def yard_page(A, I, TBL, HOUT):
    return (
        "<h2>The Souljack Yard</h2>"
        + P("<em>Greyhurst's ruined smithy yard, behind the Greenbottle alley. Run it as soon as the party has the "
            "infernal-glass heart and needs to reach the Brass Citadel before Misty's writ catches up with it.</em>")
        + READ(P("Behind the alley the old smithy yard is a graveyard of iron. Wrecked war machines lie on their sides, wheels "
                 "turned to the red sky, their furnaces cold. Something in the rubble is still glowing a sick blue-green, and "
                 "when the wind drops you can hear it: voices, very small, counting.",
                 "By the gate a bearded devil in a merchant's coat polishes a coin on his sleeve. \"Fuel,\" he says, without "
                 "looking up. \"Everyone needs fuel. Nobody likes to ask what it's made of.\""))
        + "<h3>Y1. Janella's Lift</h3>"
        + P(f"{A('janella-greenbottle', 'Janella Greenbottle')} can restore the abandoned {A('souljack-hauler', 'Souljack Hauler')} "
            "from spare iron and her golem tools. It takes 2 hours. Characters who help make a group check, three successes "
            "before two failures (DC 15; smith's or tinker's tools, Athletics to lift plates, Arcana to wake the furnace). Each "
            "failure costs another hour. Success, or no help at all, returns the hauler with 6 hours of soul fuel still in its "
            "tank, so no one has to burn a new soul to play the chase.")
        + "<h3>Y2. The Wreck Field</h3>"
        + P("Each hour of searching (DC 15 Investigation or Perception; at most three searches) turns up one "
            f"{I('soul-coin', 'soul coin')} still lodged in a dead furnace. Roll its charges, Echo, voice and claim record "
            "(Appendix B, or the ✦ Read a Soul Coin tool). On a roll of 1–2 on a d6, the coin carries Misty's MIST-113 seal and "
            "her agents learn where it is. A failed search finds 1d4 repair-kit scraps instead.")
        + "<h3>Y3. Broker Grisk's Coin Booth</h3>"
        + P(f"{A('broker-grisk', 'Broker Grisk Tallowmere')} sells coins under licence from the Ninth Sorting Annex. Prices: 300 "
            "gp in trade-scrip per charge, one Crown Mark for a 3-charge coin, or a favour named in writing. He keeps the four "
            f"example souls in a velvet tray: {I('soul-coin-tarnik', 'Tarnik Blackspoke')}, {I('soul-coin-ysera', 'Ysera Quill')}, "
            f"{I('soul-coin-merrow', 'Merrow Kindhand')} and {I('soul-coin-sevrin', 'Sevrin Nine-Roads')}.",
            "<strong>The claim ledger.</strong> Grisk must show any coin's claim record on request. A character who proves a "
            "defect (action, DC 16 Investigation or Religion) obliges him to surrender that coin. Ysera's MIST-113 stamp, "
            "Merrow's paid debt and Sevrin's double sale can all be proved this way; Tarnik's forgery needs Tarnik himself "
            "(a Query) or Janella's records.",
            "<strong>Freeing a soul.</strong> Releasing a coin whose claim the party has proved false advances the "
            "Legitimacy clock by 1 (once per session) and earns the soul's parting gift. Burning it as fuel earns nothing "
            "but the miles.")
        + "<h3>Y4. The Fuel Shed</h3>"
        + P(f"Two flasks of {I('demon-ichor', 'demon ichor')} (100 gp each from Grisk, or a DC 16 Sleight of Hand to lift them). "
            "This is the fuel for a party that refuses to burn souls: slower, unstable, and clean.")
        + "<h3>Y5. The Loan Table</h3>"
        + P(f"{A('vexa-corven', 'Vexa Corven')} (or Grisk, if Vexa is a rival) fronts up to three "
            f"{A('scorchhound-quad', 'Scorchhound Quads')} against {HOUT('loan-g12', 'Form G-12')}. Put the printed loan on "
            "the table before anyone signs. A cautious player should find it fair: the lender may negotiate a fee, but may "
            "not turn the security into a secret soul lien. It is a deliberate contrast to the sham writ Misty is about to serve.")
        + "<h3>Crewing the Machines</h3>"
        + P("For five characters use one hauler (driver, gunner, engineer and two passengers) and optionally one quad crewed by "
            "two. If the party wants all quads, put the heart in a lockable armoured saddle-box on one of them. Every machine "
            "stays vulnerable, so teamwork matters.")
        + BOXH("Soul Coins at the Table", P("The full Soul Furnace rules are in Book II, so players can read them. The short "
                                            "version: feed a coin (bonus action) for 24 hours of fuel and 1 Spark per charge; "
                                            "Pulse a Spark for the soul's power; watch the Heat; and remember every coin is a "
                                            "person. " + TBL("soul-echo", "Soul Echo table") + ".")))


def interlude_page(A, I, TBL, HOUT, SCN):
    rows8 = [["The Writ arrives", "1–2", "Two quads flank; the loudspeaker demands the heart.", "Study the writ; choose lanes; sabotage escorts."],
             ["The claw-teeth", "3–5", "The Reclaimer closes, chains lash, lava cuts the road.", "Jump vehicles; disable the winch; win a stay of collection."],
             ["The Last Cut", "6–8", "The rift closes into a burning gate; the rig prepares its final seizure.", "Outrun, ram, break the legal claim, or fight for the heart."]]
    man = [["Hold the line", "Drive; no extra check", "The vehicle moves as desired; normal end-of-round Lead check."],
           ["Thread the needles", "DC 16 Dex (land vehicles)", "Avoid a telegraphed hazard and grant +2 to the convoy's Lead check; on a failure take the hazard."],
           ["Swerve and screen", "DC 15 Dex (land vehicles)", "Allies behind this vehicle have half cover until the driver's next turn; success also gives one ally +2 on its next chase check."],
           ["Ram", "Adjacent target; vehicle attack", "Use the machine's ram attack. A ram replaces evasive driving that turn."],
           ["Board alongside", "DC 16 Dex (land vehicles)", "Bring the vehicle alongside another for the round, enabling grapples, melee or a jump between them; on a failure the jump is at disadvantage."],
           ["Overburn", "Bonus action, once per round", "+2 on this round's Lead check; the vehicle takes 2d10 fire damage that bypasses its threshold; +1 Heat."]]
    veh = [["Scorchhound Quad", "Large / 16 / 68", "10 / 25", "130 ft / 2", "Helm, chain-bow"],
           ["Cinderfang Spiker", "Large / 17 / 78", "10 / 25", "115 ft / 2", "Helm, side blades"],
           ["Souljack Hauler", "Huge / 18 / 175", "15 / 45", "95 ft / 7", "Helm, harpoon, furnace gun, engineer"],
           ["Iron Reclaimer", "Huge / 19 / 220", "18 / 50", "85 ft / 6", "Helm, tax harpoon, flame sluice, boarding winch"]]
    outcomes = [["Lawful victory", "The writ is stayed; Kestrel withdraws or becomes a fugitive.", "A legal exhibit for the Trial of Scales; 1 Crown Mark if not already earned for that proof."],
                ["Escape by speed", "The heart is kept and the pursuers lost.", "Misty files a fresh petition later; damaged machines need repairs."],
                ["Destroy or commandeer the rig", "The Reclaimer is a wreck or a prize.", "Salvage worth 3,000 gp, one working harpoon station, and at most 1 intact soul coin (if found)."],
                ["Surrender or escrow the heart", "The party survives; the heart is impounded.", "Janella asks the party to recover it at the Brass Registry: a hearing quest."],
                ["Interception", "The Reclaimer boards and takes or seals the cargo.", "A short recovery mission. No arbitrary TPK, no automatic soul loss."]]
    return (
        P("<em>Repossession at the Blackspine Narrows. Five level-12/13 characters, 60–90 minutes: a road pursuit with sabotage, "
          "vehicle combat and infernal arbitration. Run it straight after Chapter II, when the party has the infernal-glass core "
          "from Kane's mansion and has visited the Souljack Yard, and before Chapter III. It still works at level 14 with the "
          "scaling notes.</em>")
        + "<h3>Who Actually Owns the Heart?</h3>"
        + P("Janella Greenbottle built the Iron Warder to defend her community. Osric Kane stole its infernal-glass heart, but her "
            "engraved maker-mark survives on its inner ring, and the party may hold her forge records. Misty now claims that "
            "because Greyhurst fell its artifacts were abandoned, and are hers by a provisional salvage writ.",
            "Misty does not want the adventurers. She wants the heart, its testimony about the Iron Heir, and the chance to erase "
            "the traces of her agents in Kane's identity theft. Her repossession marshal may confiscate property, but not souls, "
            "characters or unrelated cargo, and he cares more about being paid than about dying for her.",
            f"The writ ({HOUT('writ-m9r', 'Writ M-9-R')}) looks plausible but is invalid. Janella never abandoned her property, "
            "the village had no right to transfer it, and notice was served at an invented address. The players have a genuine "
            "contract case while a metal apocalypse tries to run them off the road.")
        + "<h3>The Claw Rift as a Moving Road</h3>"
        + P(f"The chase runs on the {SCN("redline-run", "Claw Rift")}. The Blackspine Narrows are the road that "
            "threads it. The map is built to scroll: its left and right edges join, so the same strip serves all eight rounds.",
            "The open middle is the drivable corridor; the red claw-teeth above and below are lethal shoulders. Divide the "
            "corridor into three 20-foot lanes (north, centre, south) and place vehicles where their relative positions make "
            "sense. Keep the quads toward the edges and give the huge rig room to force a centre-lane dilemma. At the end of each "
            "round, recentre the convoy on the strip but keep its distances, lanes and ongoing effects: the land is rushing past.")
        + "<ul><li>Ranges use real token distances. A creature on a vehicle moves with it and spends no movement to stay aboard.</li>"
          "<li>The Lead score measures progress toward the far end of the Narrows, not the gap between tokens. Vehicles can "
          "still fire on each other at any Lead.</li>"
          "<li>A creature thrown from a machine lands on the moving road. It is left behind unless an ally rescues it with a "
          "reaction or an action; never instant death.</li>"
          "<li>Hitting the claw-teeth deals 3d10 bludgeoning plus 2d10 fire to a vehicle; exposed riders make DC 16 Dexterity "
          "saves (2d8 fire, half on a success). A driver avoids the collision with DC 16 Dexterity (land vehicles).</li></ul>"
        + READ(P("The Claw Rift yawns ahead, a scorched road between two jaws of red stone teeth. Trapped crystal glitters in the "
                 "walls. The road is black with ash and the bones of machines that didn't make it.",
                 "Then a low mechanical growl rises behind you. Four points of orange light become six. The dust splits around "
                 "a monstrous iron road-train, its prow a row of cutting blades, its furnace a cage of screaming gold. Quads run "
                 "ahead of it, their riders whipping chains over horned helmets. A brass loudspeaker barks: <strong>UNREGISTERED "
                 "CLAIMANTS, YOU ARE IN POSSESSION OF PROPERTY SUBJECT TO REPOSSESSION. PULL OVER. COMPLIANCE WILL REDUCE YOUR "
                 "PENALTY BY ONE THIRD.</strong>",
                 "A harpoon strikes the road beside your wheels. Roll initiative."))
        + "<h3>The Eight-Round Chase</h3>"
        + P("Begin at <strong>Lead 2</strong>. The party wins at once at Lead 6, if the Reclaimer is disabled, or if its lawful "
            "authority is suspended and the surviving crew obeys the ruling. At the end of each round the lead driver makes a DC "
            "16 Dexterity check (adding land-vehicle proficiency): success raises Lead by 1, failure lowers it by 1 (minimum 0). "
            "Scouting, distraction or a terrain maneuver can add +2, and speed or teamwork another +2, for a maximum of +4.",
            "Once each round, disabling a hostile harpoon, dropping an escort to 0 HP or forcing the pursuers into a severe "
            "obstacle also raises Lead by 1. Lead moves at most 2 steps a round, except for a ruling that ends the chase. Lead 0 "
            "is danger, not defeat. If no one has won by the end of round 8, resolve the final choke point: Lead 4–5 is a clean "
            "escape; Lead 2–3 escapes at a cost (a wreck, a lost cache, an injury or a bargain); Lead 0–1 means the Reclaimer "
            "locks onto the cargo for a short boarding showdown or negotiation. Losing the chase need not lose the campaign.")
        + T(["Phase", "Rounds", "Pressure", "Player opportunity"], rows8)
        + BOXH("✦ The Redline Run tracker", P("In Foundry, open the Championship Board and start the Redline Run: it tracks the round, "
                                               "Lead, and each machine's Heat and Sparks, and rolls the hazard and the enemy plan at "
                                               "the top of each round."), "rc-box rc-tools")
        + "<h3>Initiative and the Crew's Actions</h3>"
        + P("Roll initiative normally. Every machine has a helm and optional stations. The driver spends its action to drive, "
            "change lanes, attempt a stunt or ram; with no one driving, the vehicle runs straight until it hits something or the "
            "engine stops. Gunner and engineer actions belong to those creatures, not the machine, so a vehicle never multiplies "
            "the party's actions. Riders can cast spells and attack normally. A driver may use a bonus action to start or stop the "
            "engine, make a brief evasive juke, Overburn, feed a soul coin or Pulse.")
        + T(["Driver maneuver", "Action and check", "Effect"], man)
        + "<h3>Passengers, Boarding and Wrecks</h3>"
        + P("A passenger can Scout (action; DC 15 Perception, Survival or Investigation) to give the driver +2 on the next Lead "
            "check, or Help to steady a weapon, protect cargo, contest a writ or support a boarding. Jumping between adjacent "
            "vehicles is DC 15 Acrobatics or Athletics; on a failure the creature hangs off the target and can haul itself aboard "
            "with half its movement next turn. A passenger with a free hand can catch a falling ally as a reaction (DC 15 Athletics).",
            "At 0 HP a vehicle is a wreck: its engine stops and it drops out. Exposed riders make DC 16 Dexterity saves (4d6 "
            "bludgeoning plus 2d6 fire, half on a success); riders in enclosed compartments take half of that. An ally can attempt "
            "an immediate rescue with an action or a spell. Teleportation, flight and wall spells work as their targeting rules allow.")
        + "<h3>Soul Fuel, Engine Ethics and Repairs</h3>"
        + P("Each machine begins with 6 hours of soul fuel. Make the horror audible: the engines sing in voices. The Soul Furnace "
            "rules (Book II, and below) let the party feed new coins, Pulse a soul's Echo and risk the Heat. A party that refuses "
            f"to burn souls can run on {I('demon-ichor', 'demon ichor')} instead.",
            f"An engineer with smith's or tinker's tools and a {I('repair-kit', 'repair kit')} uses an action and DC 15 "
            "Intelligence to restore 2d10 + 5 vehicle HP; the kit is spent even on a failure. The hauler carries 3 kits, each quad "
            "1 and the Reclaimer 2. A character can instead remove a wheel lock (DC 16 Strength) or cut an attached grapnel chain "
            "(AC 16, 20 HP).")
        + "<h3>The Machines</h3>" + T(["Vehicle", "Size / AC / HP", "Threshold / mishap", "Speed / seats", "Stations"], veh)
        + P(f"Full stat blocks: {A('scorchhound-quad', 'Scorchhound Quad')}, {A('cinderfang-spiker', 'Cinderfang Spiker')}, "
            f"{A('souljack-hauler', 'Souljack Hauler')} and {A('iron-reclaimer', 'Iron Reclaimer, the Black Invoice')} (Appendix A). "
            f"Vehicle mishaps: {TBL('vehicle-mishap', 'd6 table')}.")
        + "<h3>The Repossession Crew</h3>"
        + P(f"{A('kestrel-vane', 'Marshal Kestrel Vane')} drives the Black Invoice, with a devil gunner and a winch operator "
            f"(both {A('ash-road-reaver', 'Ash-Road Reavers')}), plus two Cinderfang Spikers with a Reaver each. For four "
            "characters use one quad and 180 Reclaimer HP. For six optimised characters use three quads or 250 Reclaimer HP; "
            "don't add more attacks on the same initiative until you have seen the party play.")
        + "<h3>Legal Warfare During the Chase</h3>"
        + P("A character can use an action to object over the loudspeaker, display a verified document or force Kestrel to "
            "acknowledge a defect: one objection per character per round, and no repeating the same argument. Adjudicate the "
            "actual text of the writ before any roll.",
            "<strong>Full evidence.</strong> Janella's maker-mark AND the writ (or the village custody ledger) wins an emergency "
            "stay automatically. The crew withdraws for two rounds, the convoy gains +2 Lead at once, and any continued seizure "
            "is recorded as criminal contempt for the later tribunal.",
            "<strong>Partial evidence.</strong> Two separate DC 17 checks (Investigation, Persuasion, Arcana or a relevant tool) "
            "showing defective notice or continued custody. Each success stops a Tax Harpoon shot for a round while Kestrel argues; "
            "the second wins the stay. A failure gives Kestrel +2 on his next driving check or harpoon attack. Spells that reveal a "
            "forged signature, compel truthful testimony or produce genuine records can replace a check. No verbal trick alone "
            "ever transfers a soul.",
            "Kestrel can ignore the stay. If he does he loses lawful seizure and can only take the heart by force, and the party "
            "gains concrete evidence for the Trial of Scales and a possible Crown Mark.")
        + "<h3>The Oracles</h3>"
        + P(f"At the start of each round after the first, roll the {TBL('road-hazard', 'road hazard')} and announce it before "
            "anyone acts. Only one hazard applies each round, and it can catch the pursuers too; when unsure, target the most "
            f"exposed machine, not the weakest player. Then roll the {TBL('enemy-plan', 'enemy plan')} openly and follow it "
            "unless a creature can't.")
        + T(["d6", "Road hazard", "Choices and consequence"], [[i + 1, a, b] for i, (a, b) in enumerate(HAZARDS)])
        + T(["d6", "Enemy plan", "Declared behaviour"], [[i + 1, a, b] for i, (a, b) in enumerate(ENEMY)])
        + "<h3>Three Turning Points</h3>"
        + P("<strong>Round 2: The First Notice.</strong> Kestrel broadcasts the writ and reads its narrow scope. Reward the first "
            "player to ask for a copy: it arrives magically, service-address defect and all. If they object at once, the crew "
            "starts arguing instead of shooting.",
            "<strong>Round 4: The Crystal Maw.</strong> The south claws burst and block one lane. The nearest driver chooses: DC 17 "
            "driving through falling crystal, or steer into the Reclaimer's range so it can try its hook. A spell or gunfire can "
            "clear the rocks instead (AC 16, 35 HP).",
            "<strong>Round 7: The Blackspine Gate.</strong> Red blades rise from both shoulders, closing the road to the centre "
            "lane. A convoy at Lead 4 or more can try a DC 16 drive to escape at once; on a failure round 8 still happens. The "
            "Reclaimer fires a last harpoon and offers surrender: Kestrel will accept an escrow bond limited to the heart, never a soul.")
        + "<h3>Outcomes and Rewards</h3>" + T(["Outcome", "Consequences", "Campaign follow-through"], outcomes)
        + P(f"Kestrel carries 320 gp in infernal trade-scrip, a {I('writ-seal', 'Brass Writ-Seal')}, two repair kits and a spare "
            "flame-sluice canister. An intact Cinderfang becomes a durable vehicle if repaired. Never award a living prisoner's soul "
            "as a free collectible without an explicit moral consequence.")
        + "<h3>Pacing and Scaling</h3>"
        + "<ul><li><strong>45 minutes:</strong> start at Lead 3; one enemy quad, one hazard, six rounds, the maker-mark "
          "automatically available; no enemy oracle.</li>"
          "<li><strong>90 minutes:</strong> both quads, eight rounds, the Crystal Maw boarding and a short hearing at the Brass "
          "Registry afterwards.</li>"
          "<li><strong>Levels 14–15:</strong> add one quad and 30 Reclaimer HP; +1 to one enemy gunner's attack. Legal DCs stay the same.</li>"
          "<li><strong>Levels 16–17:</strong> make it a political ambush, not a lethal fight. Replace the marshal with a Scales "
          "Advocate, and give the heart's cage an anti-teleport field only if its limits are disclosed before play.</li>"
          "<li><strong>Afterwards:</strong> Kestrel can become a recurring rival; Janella can use the rescued heart to restore "
          "the Iron Warder; Misty can sue over her crew's misconduct while pretending she never authorised the forged notice.</li></ul>"
        + BOXH("DM-as-player fairness", P("Write down or publicly roll the hazard and the enemy plan before resolving your own "
                                          "character's declared action. The marshal's orders are fixed by the oracle; he bargains "
                                          "only when a real legal opening exists. Never change the writ's wording after the party "
                                          "finds a loophole.")))


def driving_html():
    """Player-facing chase basics for Book II."""
    man = [["Hold the line", "Drive; no extra check", "Move as you like; the normal end-of-round Lead check applies."],
           ["Thread the needles", "DC 16 Dex (land vehicles)", "Avoid a telegraphed hazard and give the convoy +2 on its Lead check; on a failure, take the hazard."],
           ["Swerve and screen", "DC 15 Dex (land vehicles)", "Allies behind you have half cover until your next turn; success also gives one ally +2 on its next chase check."],
           ["Ram", "Adjacent target; vehicle attack", "Use the machine's ram attack instead of evasive driving."],
           ["Board alongside", "DC 16 Dex (land vehicles)", "Pull alongside another vehicle for the round so allies can grapple, fight or jump across."],
           ["Overburn", "Bonus action, once per round", "+2 on this round's Lead check; your vehicle takes 2d10 fire damage that bypasses its threshold; +1 Heat."]]
    return (P("<strong>Who does what.</strong> The driver spends their action to drive, change lanes, attempt a stunt or ram; "
              "their bonus action can start or stop the engine, juke, Overburn, feed a soul coin or Pulse. Gunners fire stations "
              "with their own actions, and the engineer repairs and cools the furnace. A vehicle never takes actions of its own, "
              "and riders cast and attack normally.",
              "<strong>Lead.</strong> In a chase your convoy has a Lead score from 0 to 6. At the end of each round the lead driver "
              "makes a DC 16 Dexterity check (with land-vehicle proficiency): success raises Lead, failure lowers it. Scouting, "
              "maneuvers and teamwork add up to +4. Reach Lead 6 and you're clear.",
              "<strong>Passengers.</strong> Scout (action; DC 15 Perception, Survival or Investigation) to give the driver +2; jump "
              "between adjacent vehicles with DC 15 Acrobatics or Athletics; catch a falling ally as a reaction (DC 15 Athletics). "
              "Anyone thrown off lands on the road and needs rescuing, not a funeral.",
              "<strong>Repairs.</strong> With a repair kit and smith's or tinker's tools, an action and DC 15 Intelligence restores "
              "2d10 + 5 vehicle hit points.")
            + T(["Driver maneuver", "Action and check", "Effect"], man))
