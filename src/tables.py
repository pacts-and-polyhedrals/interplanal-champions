"""Rollable tables."""
from lib5e import *

TABLES = []


def table(key, name, formula, rows, desc="", img=None):
    tid = fid("table:" + key)
    results = []
    lo = 1
    for i, r in enumerate(rows):
        weight = 1
        text = r
        if isinstance(r, tuple):
            text, weight = r
        rid = fid(f"tr:{key}:{i}")
        results.append({"_id": rid, "type": "text", "name": "", "description": text, "text": text, "img": icon("ic-arena"),
                        "weight": weight, "range": [lo, lo + weight - 1], "drawn": False,
                        "_key": f"!tables.results!{tid}.{rid}"})
        lo += weight
    TABLES.append({"_id": tid, "name": name, "img": img or icon("ic-arena"), "description": desc, "formula": formula,
                   "replacement": True, "displayRoll": True, "results": results, "folder": None, "sort": len(TABLES) * 100,
                   "flags": {MOD: {"key": key}}, "_key": f"!tables!{tid}", "_stats": STATS})


A = uuid_actor
I = uuid_item

table("arena-environment", "Arena Environmental d6 (initiative count 20)", "1d6", [
    "<strong>Uneventful cycle.</strong> No effect.",
    "<strong>Electric arcs.</strong> Level 15: DC 17 Dex, 3d8 lightning in the marked side lanes. Level 17: DC 19 Dex, 4d8 lightning.",
    "<strong>Blue crystal.</strong> Level 15: DC 17 Con, 3d8 necrotic within 15 ft. Level 17: DC 19 Con, 4d8 necrotic.",
    "<strong>Four lava fissures.</strong> Level 15: DC 17 Dex, 3d10 fire within 10 ft of an active line. Level 17: DC 19 Dex, 4d10 fire.",
    "<strong>Yellow crystal.</strong> Level 15: DC 17 Wis, 3d8 radiant within 15 ft. Level 17: DC 19 Wis, 4d8 radiant.",
    "<strong>Summoning glyph.</strong> Roll the tier-appropriate d100 summons. Only one summon result may be active at once; "
    "on another 6 while summons remain, they move 10 ft instead."],
    "Announce glowing lines and unstable crystal colours before their effect. A creature next to a crystal can suppress it "
    "(action, DC 17 Arcana) or destroy it (AC 16, 25 HP), disabling it for two rounds.", icon("ic-arena"))
table("arena-summons-15", "Arena Summons d100 (Level 15)", "1d100", [
    ("2 lemure mobs (25 HP each, +5 to hit, 2d6 + 2 slashing). Flee when the central glyph breaks.", 15),
    ("2 " + A("writ-bailiff", "Writ Bailiffs") + ". One is visibly contesting a summons warrant.", 15),
    ("1 " + A("ash-scrap-golem", "Ash-Scrap Golem") + ", arriving damaged at 60 HP.", 15),
    ("1 " + A("contract-sentinel", "Contract Sentinel") + ". Targets the current arena control holder.", 15),
    ("3 fire mephits (published blocks). Combative but distractible.", 12),
    ("1 " + A("night-hag-advocate", "Night Hag Advocate") + ". Can be bribed to testify instead of fight.", 10),
    ("2 barbed devils (published blocks). Arrive on opposite sides.", 8),
    ("1 " + A("iron-warder-damaged", "Iron Warder Prototype, Damaged") + ". Unstable orders may be contested.", 6),
    ("Rival audience interference: 2 Writ Bailiffs. The sponsor must identify them publicly.", 3),
    ("An infernal celebrity's shadow passes over the arena; no creature enters. Gain 1 bonus Crown Mark for surviving the spectacle.", 1)],
    "Preliminary pits, level 15.", icon("ic-portal"))
table("arena-summons-17", "Arena Summons d100 (Level 17)", "1d100", [
    ("2 " + A("writ-bailiff", "Writ Bailiffs") + ". A distraction rather than a decisive threat.", 12),
    ("1 " + A("contract-sentinel", "Contract Sentinel") + ". No extra reinforcement.", 13),
    ("1 " + A("night-hag-advocate", "Night Hag Advocate") + ". Will bargain with clever contestants.", 13),
    ("2 " + A("ash-scrap-golem", "Ash-Scrap Golems") + " on opposing sides.", 12),
    ("1 " + A("iron-warder-restored", "Iron Warder, Restored") + ". Fights only for 3 rounds.", 13),
    ("2 barbed devils (published blocks). Use normal initiative.", 11),
    ("1 horned devil (published block). Leaves when the summoning glyph is disabled.", 9),
    ("The Vacant King's scrap echo: 100 HP, one attack, does not regenerate.", 8),
    ("A hostile claimant's champion: substitute a prepared rival (" + A("vexa-corven", "Vexa") + ", " +
     A("marshal-kordren", "Kordren") + ", " + A("brass-factor-morn", "Morn") + "), never an unbuilt ancient dragon.", 6),
    ("Tiamat's silhouette crosses the sky; DC 18 Wis or frightened until your next turn. A cameo only, no forced fight.", 2),
    ("The arena offers a true negotiation: release the current summoned enemy and win a Crown Mark if both sides agree. Consent counts.", 1)],
    "The Rite of the Nine, level 17.", icon("ic-portal"))
table("travel", "Travel Incidents (d12)", "1d12", [
    "Imps demand a nonexistent toll; a written exemption works.",
    "A caravan seeks protection from a war machine.",
    "A living witness has forgotten their own name.",
    "Unstable lava crust: two DC 16 checks or [[/damage 3d8 fire]].",
    "An abandoned golem contains Janella's maker mark.",
    "A lawyer offers safe passage with an explicit memory price.",
    "A devil tries to deliver a letter to a dead claimant.",
    "A rival offers a legitimate joint-slate negotiation.",
    "A regiment asks whether a machine can be a person.",
    "A hag-eye follows the party; DC 18 Perception to notice.",
    "The Styx touches the bank; travellers risk memories if they bathe in it.",
    "An old Red Clause toy sings a carol and spits out an appeal notice."], "Roads of Avernus.", icon("ic-key"))
table("temptations", "Infernal Temptations (d10)", "1d10", [
    "<strong>Offer:</strong> restore one spent Hit Die to each party member. <strong>Honest price:</strong> publicly sponsor one infernal witness.",
    "<strong>Offer:</strong> passage past a dangerous garrison. <strong>Price:</strong> disclose the party's destination to a named rival.",
    "<strong>Offer:</strong> a one-use rare wand. <strong>Price:</strong> one week of explicitly defined service after the contest.",
    "<strong>Offer:</strong> a map of a sealed court. <strong>Price:</strong> share a copy with Misty's notary.",
    "<strong>Offer:</strong> undo one recent memory loss. <strong>Price:</strong> permit one recorded interview about the restored memory.",
    "<strong>Offer:</strong> restore one deceased NPC to life if rules permit. <strong>Price:</strong> return a stolen personal artifact, not a soul.",
    "<strong>Offer:</strong> a legal precedent against soul repossession. <strong>Price:</strong> read the citation publicly at the next trial.",
    "<strong>Offer:</strong> a golem core repair kit. <strong>Price:</strong> assist Janella's civil-rights hearing.",
    "<strong>Offer:</strong> a dragon's treasure location. <strong>Price:</strong> give the source a first look at any recovered cache.",
    "<strong>Offer:</strong> one automatic success in a minor hearing. <strong>Price:</strong> recuse a named character from that hearing."],
    "Every temptation states its honest price.", icon("ic-pyric-ring"))
table("rewards-low", "Rewards by Tier (Levels 12–14)", "1d10", [
    ("250–700 gp in infernal coin and 1 potion of superior healing.", 2),
    ("2 spell scrolls of levels 2–3.", 2),
    ("1 uncommon or rare relic from Book II (" + I("quill-true-notice", "Quill of True Notice") + ", "
     + I("mistletoe-manacles", "Mistletoe Manacles") + ", " + I("marshals-chain", "Marshal's Chain") + ").", 2),
    ("1 detailed document or favourable witness.", 2),
    ("One partial Crown Mark lead.", 1), ("A golem repair component worth 500 gp.", 1)],
    "Treasure markers on Maps 1–5. Loot policy: no random +3 items at level 12, no permanent spell-restoring loops, "
    "no automatic dragon attached to a chest.", icon("ic-crownmark"))
table("rewards-high", "Rewards by Tier (Levels 15–17)", "1d10", [
    ("700–1,500 gp and 2 potions of superior healing.", 2), ("2 spell scrolls of levels 4–5.", 2),
    ("1 rare relic from Book II.", 2), ("1 very rare relic or a strong faction favour (choose).", 2),
    ("A completed one-use legal stay.", 1), ("A Heartstone witness-seal or an equivalent unique story asset.", 1)],
    "Arena chests and Chapter IV–VI rewards.", icon("ic-crownmark"))
table("mansion-consequences", "Mansion Consequences (d6)", "1d6", [
    "<strong>Infernal dust.</strong> DC 16 Con save or blinded until the end of the next turn.",
    "<strong>Name echo.</strong> A nearby mirror repeats an authentic witness's name; gain an additional clue.",
    "<strong>Bound ember.</strong> DC 16 Dex save or [[/damage 3d8 fire]]; half on a success.",
    "<strong>Errant summons.</strong> One " + A("ash-scrap-golem", "Ash-Scrap Golem") + " arrives at half HP, guarding its assigned door.",
    "<strong>Paper swarm.</strong> Squares within 15 ft become difficult terrain for one round.",
    "<strong>Contradiction revealed.</strong> The false rune glows; one step in the sequence is made certain."],
    "Roll once for each incorrect inverse-circle configuration (Map 4). After the second mistake, reveal which term was "
    "misplaced. All effects are reversible or avoidable.", icon("ic-hex"))
table("rival-oracle", "Rival Oracle (d6)", "1d6", [
    A("vexa-corven", "Vexa Corven") + " offers an honest alliance against a sponsored champion.",
    A("corda-kain", "Corda Kain") + " exceeds Zariel's proxy mandate; it can be proved.",
    A("magistrate-khel", "Magistrate Khel") + " trades supplies for a public hearing.",
    A("isolde", "Isolde of Seven Masks") + " asks, quietly, whether pledged memories can be bought back.",
    A("hollis-valrick", "Hollis Valrick") + " issues a new circular that misreads the Charter.",
    "A sponsor's agent offers a Covenant of Faction Sponsorship (Form IC-06)."], "What the rivals do this session.", icon("ic-battle"))
table("wilds-encounters", "Avernus Wilds Encounters (d100, Maps 1–2)", "1d100", [
    ("2 " + A("imp-tollkeeper", "imps") + " with a forged toll schedule. Talkable.", 15),
    ("1 " + A("ash-scrap-golem", "Ash-Scrap Golem") + " guarding a stranded courier.", 15),
    ("Lava crust gives way: group challenge, 3 successes before 2 failures, DC 16.", 15),
    ("3 " + A("skull-notary", "skull notaries") + " offering to certify a deed, for a fee.", 10),
    ("2 " + A("writ-bailiff", "Writ Bailiffs") + " serving a warrant on the wrong contestant.", 15),
    ("The " + A("ashclad-petitioner", "Ashclad Petitioners") + " (3), arguing about where to go next.", 10),
    ("A dragon's bones; a chest beneath (roll Rewards, Levels 12–14).", 10),
    ("A hag-eye watches from a rock; DC 18 Perception to notice.", 7),
    ("Nothing: the red sand blows, and somewhere a bell rings that nobody pulls.", 3)],
    "Roll once per original encounter marker; do not reroll if characters circle the same spot. No ancient dragons, no Tiamat.",
    icon("ic-embers"))
table("greyhurst-encounters", "Greyhurst Encounters (d100, Maps 3–5)", "1d100", [
    ("2 " + A("cadaver-collector", "cadaver collectors") + " and a " + A("brass-registrar", "brass registrar") + " with warrants (3D).", 20),
    ("A " + A("greyhurst-survivor", "survivor") + " family hiding in a cellar. They know where the bell is.", 15),
    ("3 " + A("lemure", "lemures") + " that were villagers yesterday. Can they be saved?", 15),
    ("An " + A("ash-scrap-golem", "Ash-Scrap Golem") + " guarding a door it no longer remembers.", 15),
    ("A " + A("spectral-clerk", "spectral clerk") + " filing the same form forever.", 10),
    ("A burning house: DC 15 Athletics to reach the child inside.", 10),
    ("A forge-ledger page in Janella's hand (clue 1 of 3).", 10),
    ("Silence. The inverted circle overhead turns a quarter-turn.", 5)],
    "Roll once per marker. Every Greyhurst encounter has someone in it who can be saved or questioned.", icon("ic-core"))


import redline as _RL
_RL.build_tables(table)
import soulforged as _SF
_SF.build_tables(table)
