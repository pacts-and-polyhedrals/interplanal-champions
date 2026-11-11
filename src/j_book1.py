"""Book I — The Throne of Avernus (the GM's campaign book), built from the manuscript with scene, actor and table links."""
import os
from jhelp import *
import textbook as TB
import tables as TBL

HERE = os.path.dirname(os.path.abspath(__file__))
L = TB.load(os.path.join(HERE, "data", "book1.txt"))
A = uuid_actor
I = uuid_item
T = uuid_table
M = uuid_macro
SC = scene_link
HO = lambda k, n: uuid_journal("handouts", k, n)

# --------------------------------------------------------------------------- hand-built tables (they don't survive the text)
ROADMAP = TABLE(["Act", "Sessions", "Levels", "Core developments", "Milestone"], [
    ["I. Dead Already", "1–3", "12", "Arrival, lava road, initial registration, contenders, first evidence", "Level 13 after the Survival Proof"],
    ["II. The Fallen", "4–7", "13", "Greyhurst, golemancer, inverse circle, soul registry, Misty's first contract", "Level 14 after freeing or ruling Greyhurst"],
    ["III. The War of Claims", "8–11", "14", "Avernus factions, champion sponsorship, rival claimants, contract litigation", "Level 15 after the second public trial"],
    ["IV. Blood and Brass", "12–15", "15", "Citadel politics, progressive arenas, construct war, attempted coup", "Level 16 on securing arena qualification"],
    ["V. The Hag Queen's Due", "16–19", "16–17", "Misty's coven, Heartstone investigation, bargains or raid, optional mythic confrontation", "Level 17 before the true Misty confrontation"],
    ["VI. The Rite of the Nine", "20–24", "17", "Arena of Asmodeus, rival coalitions, legal appeals, governance and investiture", "Sovereign, shared council, proxy or refusal"]])
BRIDGE = TABLE(["Red Clause ending", "Sequel hook and consequence"], [
    ["Unprecedented Verdict", "The Brass Arbiter's judgment is cited as Precedent H-25. The heroes receive standing to inspect the succession charter and one automatic success on a legal petition concerning coerced consent."],
    ["Hostile Takeover", "Salvaged machinery includes a Brass Court summons; the party has proof of fraud but not legal precedent. A Red Clause remnant may appear as a disgraced rival clerk."],
    ["Greatest Gift", "A character who voluntarily pledged a soul receives a separate, optional stay-of-collection offer to enter the tournament. Declining does not rewrite the old bargain; the player can use a new character."],
    ["Ninth Bell", "The tournament advertises a writ of review among its genuine prizes. A contestant may seek title partly to recover prisoners transferred to Nessus."]])
PROOFS = TABLE(["Proof", "How it is earned", "Typical route"], [
    [I("proof-survival", "Survival"), "Live through a published hazard, defeat a ranked foe or protect another qualified claimant while threatened.", "Maps 1–2; or the first arena round."],
    [I("proof-deviousness", "Deviousness"), "Obtain a genuine procedural advantage through investigation, negotiation or a discovered loophole; forgery alone doesn't count unless admitted as a lawful gambit.", "Greyhurst; Misty's challenge; Citadel litigation."],
    [I("proof-dominion", "Dominion"), "Secure the voluntary allegiance of a nontrivial faction, preserve a domain under pressure or demonstrate command in a contest.", "Janella's golems; the Fallen survivors; the final arena."]])
FACTIONS = TABLE(["Faction", "Wants", "Offers", "Hidden fault"], [
    ["Office of the Ninth Crown", "A credible outcome validating Asmodeus's new succession rite", "Enforcement of the published Charter, not personal friendship", "An aide is accepting influence payments from Misty"],
    ["Zariel's War Host", "Preserve military command and win by proxy", "Battlefield intelligence, veteran support", "Will sacrifice civilian assets to improve tactical outcomes"],
    ["Bel's Brass Consortium", "Regain economic and military leverage", "Siege engines, forged metal, logistics", "Has financed both sides of several rival bids"],
    ["Misty's Pyric Triune", "Put soul, memory and curse brokerage under her influence", "Hidden truths, memory escrow, a hag-counsel's legal expertise", "The offered assistance creates future rights in a victor's administration"],
    ["Greyhurst's Remnant", "Release survivors and recover stolen golem work", "Witnesses, protected routes, a construct ally", "The golem core itself contains incriminating recorded commands"]])
CLOCKS = TABLE(["Clock", "At 4+: visible change", "At 6"], [
    ["Blood War Pressure", "Citadel checkpoints, shortages, army requisitions", "The arena finale includes a siege wave unless the party stabilises supplies"],
    ["Hag Lien", "Witnesses lose memories; hag notaries appear at public proceedings", "Misty gains a free legal opening petition in the final court"],
    ["Public Legitimacy", "Neutral witnesses offer help; recruits volunteer", "The party can nominate a genuine joint regency without persuading a hostile crowd"]]) + \
    P("Track all three on the " + M("board", "Championship Board") + ".")
RIVALS = TABLE(["Name", "Position", "Complication", "Use"], [
    [A("vexa-corven", "Vexa Corven"), "Independent duelist", "Wants honest fame, dislikes being managed", "Ally or honourable rival"],
    [A("corda-kain", "Corda Kain"), "Zariel's steel advocate", "Must obey a narrow proxy mandate", "Can be defeated by exceeding sponsor authority"],
    [A("magistrate-khel", "Magistrate Khel"), "Bel's engineer-general", "Needs supplies to keep an outpost alive", "Competitive but capable of compromise"],
    [A("isolde", "Isolde of Seven Masks"), "Misty's sponsored contestant", "Has pledged her future memories but not her soul", "Sympathy, rivalry or rescue"],
    [A("hollis-valrick", "Hollis Valrick"), "Deputy registrar", "Secretly harvests paper champions", "The visible bureaucratic antagonist"]])
EXHIBITS = TABLE(["Exhibit", "Found", "Proves", "Last-resort duplicate"], [
    [I("exhibit-a", "A, False Entrants"), "Map 2 floating docket", "Stolen contestant identities", "Greyhurst tavern guest list"],
    [I("exhibit-b", "B, False Service Order"), "Greyhurst registrar", "No authority to collect villagers", "Mansion study"],
    [I("exhibit-c", "C, Inverse Circle Transcript"), "Mansion lower level", "Kane's deliberate alteration", "Janella's restored golem core"],
    ["D, Warden Testament", "Restored Warder / Marus", "Construct commands were altered", "Janella's forge ledger"],
    [I("exhibit-e", "E, Chain of Title"), "Market of Claimed Names", "Hollis connected to the Red Clause case", "Citadel registry stamp"],
    ["F, Pyric Trust", "Misty's estate register", "Heartstone held by a named trust", "Witness of Ownership"],
    ["G, Final Charter Public", "Brass Arbiter", "The throne can be held jointly", "Citadel Hall of Registrants"]])
SEALS = TABLE(["Seal", "Evidence", "Effect when suppressed"], [
    [I("witness-name", "Name"), "The first hag witness's authentic birth-name testament", "Misty loses Magic Resistance for 2 full rounds"],
    [I("witness-consent", "Consent"), "The custodian's document proving a soul copy was taken without consent", "Misty's save DC becomes 22 for the rest of this encounter"],
    [I("witness-jurisdiction", "Jurisdiction"), "The Brass Arbiter's order or the third witness's trust registry", "Misty loses one unspent Legendary Resistance and cannot make Counterclaim for 2 rounds"]])
GOLEM_TABLE = TABLE(["Party", "Opening hostile golem setup", "Act IV siege adjustment", "Misty optional fight"], [
    ["Four level-13 PCs", "Janella + 1 Scrap Golem, or 1 damaged Warder", "Remove a Bailiff; allow an early control-pylon success", "Strongly discourage direct confrontation without outside aid"],
    ["Five level-13 PCs", "1 damaged Warder + 2 Bailiffs", "The published five-foe split encounter", "Full warning; three seals and full resources recommended"],
    ["Six level-13 PCs", "Warder + 2 Bailiffs, 1 Scrap Golem arriving later", "Add one Bailiff after round two", "Still extreme; one extra character does not make CR 30 ordinary"]])
TRIALS = TABLE(["Trial", "Session", "Clear win condition", "Recorded output"], [
    ["I Claim", "1", "Register with a disclosed claim type", "Charter signature / absence"],
    ["II Ember", "2–3", "Cross Avernus alive or protect a rival", "Survival Proof"],
    ["III Witness", "4–7", "Recover the authentic Greyhurst registry", "Witness and Deviousness Proof"],
    ["IV Dominion", "9", "Secure a voluntary or witnessed command", "Dominion Proof"],
    ["V Scales", "10", "Win a pleaded case on real evidence", "Legal precedent or standing"],
    ["VI Deception", "11", "Unmask a forged contestant without forging consent", "Recorded counterevidence"],
    ["VII Siege", "13", "Preserve civilians and the forge under attack", "Construct alliance or military command"],
    ["VIII Resolve", "14", "Survive multi-objective Brass Arena preliminaries", "Qualification to the final Rite"],
    ["IX Crown", "20–24", "Survive the arena, answer claims and accept office", "Sole, joint, proxy or no crown"]])
TRACKSHEET = TABLE(["Contestant or slate", "Survival", "Deviousness", "Dominion", "Bonus Crown Marks", "Public Legitimacy", "Hag Lien", "Current claim"],
                   [["&nbsp;", "☐", "☐", "☐", "", "", "", "Sole / Joint / Proxy"] for _ in range(4)]) + \
    P("In Foundry, the " + M("board", "Championship Board") + " keeps this sheet live for the whole table.")


def table_html(key):
    t = next(x for x in TBL.TABLES if x["flags"][MOD]["key"] == key)
    rows = [[f"{r['range'][0]}" + (f"–{r['range'][1]}" if r['range'][1] != r['range'][0] else ""), r["description"]] for r in t["results"]]
    return H(3, T(key, t["name"])) + (P(t["description"]) if t["description"] else "") + TABLE([t["formula"].replace("1", "", 1), "Result"], rows)


ARENA = (TABLE(["Original map", "New purpose", "Original element retained", "Scene"], [
    ["Map 1, Welcome to Hell", "Act I entry", "Lava-cut arrival, markers, treasure", SC("welcome", "Map 1")],
    ["Map 2, Unexpected Findings", "Act I ash road", "Wide lava river, risky shortcuts", SC("findings", "Map 2")],
    ["Map 3, The Fallen", "Act II Greyhurst", "Town blocks, old mayor, silent golem", SC("greyhurst", "Map 3")],
    ["Map 4, Sorcerous Implications", "Act II mansion lower", "Inverse summoning circle, infernal script", SC("mansion-lower", "Map 4")],
    ["Map 5, Sorcerous Implications II", "Act II mansion upper", "Warded room, golem core, escape routes", SC("mansion-upper", "Map 5")],
    ["Map 6, Brass Arena", "Acts IV and VI", "Two glyphs, two crystals, four lava channels, two chests, central pad", SC("arena", "Map 6")]]) +
    P("<strong>Map naming:</strong> the original Map 6 image is headed <em>Brass Arena – Map 4</em> on its own page; this campaign "
      "calls it Map 6 to avoid confusing it with the mansion.",
      "<strong>At the table:</strong> the " + M("arena", "Arena Hazard") + " macro rolls the d6 at initiative count 20, posts the "
      "telegraphed effect and draws on the right summons table on a 6.") +
    "".join(table_html(k) for k in ("arena-environment", "arena-summons-15", "arena-summons-17", "travel", "temptations",
                                    "rewards-low", "rewards-high", "wilds-encounters", "greyhurst-encounters")))

TABLES = {
    "Act Sessions Levels Core developments Milestone": ("Pacing:", ROADMAP),
    "Red Clause ending Sequel hook and consequence": ("The party need not have played", BRIDGE),
    "Proof How it is earned Typical route": ("Use open Crown Marks", PROOFS),
    "Faction Wants Offers Hidden fault": ("Primary adversary:", FACTIONS),
    "Clock at 4+ Visible change At 6": ("Fail-forward:", CLOCKS),
    "Name Position Complication Use": ("Side quests", RIVALS),
    "Exhibit Found Proves Last resort duplicate": ("Safety and consequences", EXHIBITS),
    "Seal Evidence Effect when suppressed": ("Heartstone object:", SEALS),
    "d6 Consequence Mechanical effect": ("Golemancer action-economy", table_html("mansion-consequences")),
    "Party Opening hostile golem setup": ("APPENDIX C", GOLEM_TABLE),
    "Six original map locations, preserved": ("Loot policy:", ARENA),
    "Trial Default session Clear win condition": ("For a faster 18-session season", TRIALS),
    "Contestant or": ("Open encounter record", TRACKSHEET),
}
READ = {"Read aloud: the invitation": "Lawful premise", "Read aloud:": "Preserve the existing Misty", "Read aloud": "Keyed encounter locations"}

# scene callouts and links, by page
SCENE_BOX = {
    "map1": [("welcome", "Map 1: Welcome to Hell"), ("counting-gate", "1A: The Counting Gate"), ("ash-bridge", "1B–1D: The Ash Bridge"), ("breach", "The Breach at Hollow Barrow (optional arrival)")],
    "map2": [("findings", "Map 2: Unexpected Findings"), ("styx-ferry", "2A–2C: The Ferryman's Landing"), ("ashen-caverns", "The Ashen Caverns (optional)")],
    "map3": [("greyhurst", "Map 3: The Fallen"), ("greyhurst-district", "Greyhurst: The Burgher's Row (street level)"), ("tavern", "3A: The Drowned Tavern"), ("greenbottle", "3B–3E: The Greenbottle Alley")],
    "map4": [("mansion-lower", "Map 4: The Mansion (Ground Floor)")],
    "map5": [("mansion-upper", "Map 5: The Mansion (Upper Floor)")],
    "s8": [("market-names", "The Market of Names")], "s10": [("docket", "The Whispering Docket")],
    "s11": [("masquerade", "The Trial of False Faces")], "s12": [("citadel", "The Hall of Registrants")],
    "s13": [("iron-quarter", "The Iron Quarter")], "s14": [("arena", "Map 6: The Brass Arena")], "s15": [("claw-rift", "The Claw Rift (Hollis's escape)")],
    "s16": [("audience", "The Chamber of Iron Roses")], "s18": [("reliquary", "The Thorn Reliquary")],
    "s19": [("audience", "Phase 1: The Chamber of Iron Roses"), ("reliquary", "Phase 2: The Thorn Reliquary")],
    "s20": [("arena", "Map 6: The Arena of Asmodeus")],
}
TOOLS = {
    "map1": "Ash Bridge: run the " + M("challenge", "Group Challenge") + " macro (3 successes before 2 failures, DC 16). Random encounters: " + T("wilds-encounters", "Avernus Wilds") + ".",
    "map2": "Random encounters: " + T("wilds-encounters", "Avernus Wilds") + ". Travel: " + T("travel", "Travel Incidents") + ".",
    "map3": "Random encounters: " + T("greyhurst-encounters", "Greyhurst Encounters") + ".",
    "map4": "Wrong circle sequence: roll " + T("mansion-consequences", "Mansion Consequences") + ".",
    "s9": "Run the " + M("battle", "Ash March") + " macro for the three exchanges.",
    "s10": "Run the " + M("tribunal", "Convene a Hearing") + " macro (three stages).",
    "s14": "Each round: " + M("arena", "Arena Hazard") + " at initiative count 20.",
    "s19": "When Misty first drops to 0 HP, run " + M("mythic", "Hag Queen's Deception") + ". Track the seals on the " + M("board", "Championship Board") + ".",
    "s21": "Each round: " + M("arena", "Arena Hazard") + " (level 17).",
    "ch2": "After the Proofs, Petition M-9 is heard with the " + M("tribunal", "Convene a Hearing") + " macro (two successes before two failures, DC 18).",
}
ACTOR_LINKS = [("Janella Greenbottle", A("janella-greenbottle", "Janella Greenbottle")), ("Osric Kane", A("osric-kane", "Osric Kane")),
               ("Hollis Valrick", A("hollis-valrick", "Hollis Valrick")), ("Vexa Corven", A("vexa-corven", "Vexa Corven")),
               ("Mother Sable", A("mother-sable", "Mother Sable")), ("Iron Warder", A("iron-warder-damaged", "Iron Warder")),
               ("Ash-Scrap Golem", A("ash-scrap-golem", "Ash-Scrap Golem")), ("Writ Bailiff", A("writ-bailiff", "Writ Bailiff")),
               ("Contract Sentinel", A("contract-sentinel", "Contract Sentinel")), ("Night Hag Advocate", A("night-hag-advocate", "Night Hag Advocate")),
               ("Vacant King", A("iron-heir", "Vacant King")), ("Brass Arbiter", A("brass-arbiter", "Brass Arbiter")),
               ("Oathshard", A("oathshard", "Oathshard")), ("Sergeant Orro", A("sergeant-orro", "Sergeant Orro")),
               ("Marshal Kordren", A("marshal-kordren", "Marshal Kordren")), ("Brass Factor Morn", A("brass-factor-morn", "Brass Factor Morn")),
               ("Isolde", A("isolde", "Isolde")), ("Lila", A("lila-greenbottle", "Lila")), ("Children of Hell", A("child-of-hell", "Children of Hell")),
               ("Heartstone", A("heartstone", "Heartstone")), ("Championship Stamp", A("championship-stamp", "Championship Stamp")),
               ("Blackthorn Shears", I("blackthorn-shears", "Blackthorn Shears")), ("Hourglass of True Dawn", I("hourglass-true-dawn", "Hourglass of True Dawn")),
               ("Lantern of Three Witnesses", I("lantern-three-witnesses", "Lantern of Three Witnesses")),
               ("Covenant of Joint Regency", HO("ic-01", "Covenant of Joint Regency")), ("Petition M-9", HO("petition-m9", "Petition M-9")),
               ("Perpetual First Refusal Writ", HO("first-refusal", "Perpetual First Refusal Writ")),
               ("Memorandum of Memory Escrow", HO("ic-04", "Memorandum of Memory Escrow")),
               ("Exhibit A", I("exhibit-a", "Exhibit A")), ("Exhibit B", I("exhibit-b", "Exhibit B")), ("Exhibit C", I("exhibit-c", "Exhibit C")),
               ("Exhibit E", I("exhibit-e", "Exhibit E")), ("Proof of Survival", I("proof-survival", "Proof of Survival")),
               ("Proof of Deviousness", I("proof-deviousness", "Proof of Deviousness")), ("Proof of Dominion", I("proof-dominion", "Proof of Dominion"))]

SPLIT = [  # key, title, start-line prefix
    ("running", "1. Running the Championship", "1. RUNNING THE CHAMPIONSHIP"),
    ("bridge", "Bridge from The Night of the Red Clause", "Bridge from The Night of the Red Clause"),
    ("audit", "2. The Succession Audit", "2. THE SUCCESSION AUDIT"),
    ("ch1", "3. Chapter I — Dead Already", "3. CHAPTER I — DEAD ALREADY"),
    ("map1", "Map 1: Welcome to Hell", "Map 1: Welcome to Hell"),
    ("map2", "Map 2: Unexpected Findings", "Map 2: Unexpected Findings"),
    ("ch2", "4. Chapter II — The Fallen", "4. CHAPTER II — THE FALLEN"),
    ("map3", "Map 3: The Fallen", "Map 3: The Fallen"),
    ("map4", "Map 4: The Mansion Below", "Map 4: Sorcerous Implications"),
    ("map5", "Map 5: The Mayor's Upper Floor", "Map 5: Sorcerous Implications II"),
    ("ch3", "5. Chapter III — The War of Claims", "5. CHAPTER III - THE WAR OF CLAIMS"),
    ("s8", "Session 8: The Market of Claimed Names", "Session 8:"),
    ("s9", "Session 9: Trial of the Ash March", "Session 9:"),
    ("s10", "Session 10: The Whispering Docket", "Session 10:"),
    ("s11", "Session 11: The Trial of False Faces", "Session 11:"),
    ("ch4", "6. Chapter IV — Blood and Brass", "6. CHAPTER IV - BLOOD AND BRASS"),
    ("s12", "Session 12: Arrival and Registration", "Session 12:"),
    ("s13", "Session 13: The Golemancer's War", "Session 13:"),
    ("s14", "Session 14: The Preliminary Pits", "Session 14:"),
    ("s15", "Session 15: The Coup That Cannot Be Filed", "Session 15:"),
    ("ch5", "7. Chapter V — The Hag Queen's Due", "7. CHAPTER V - THE HAG QUEEN"),
    ("s16", "Session 16: The Queen's Due", "Session 16:"),
    ("s17", "Session 17: The Three Witnesses of the Heartstone", "Session 17:"),
    ("s18", "Session 18: Raid on the Thorn Reliquary", "Session 18:"),
    ("s19", "Session 19: Misty Unbound", "Session 19:"),
    ("ch6", "8. Chapter VI — The Rite of the Nine", "8. CHAPTER VI - THE RITE OF THE NINE"),
    ("s20", "Session 20: Opening Ceremony", "Session 20:"),
    ("s21", "Sessions 21–22: Arena Rounds", "Sessions 21-22:"),
    ("s23", "Session 23: The Last Appeal", "Session 23:"),
    ("s24", "Session 24: Crown, Council or Catastrophe", "Session 24:"),
    ("npcs", "9. NPC Dossiers and Balanced Bestiary", "9. NPC DOSSIERS AND BALANCED BESTIARY"),
    ("arena-engine", "10. Arena Engine and Random Tables", "10. ARENA ENGINE AND RANDOM TABLES"),
    ("procedure", "11. Open-Procedure DM-as-Player Rules", "11. OPEN-PROCEDURE DM-AS-PLAYER RULES"),
    ("charter-ref", "12. Campaign Charter — DM Reference", "12. CAMPAIGN CHARTER - DM REFERENCE"),
    ("design-audit", "13. Design and Playtest Audit", "13. DESIGN AND PLAYTEST AUDIT"),
    ("app-a", "Appendix A: Misty — The Full Optional Mythic Encounter", "APPENDIX A."),
    ("app-b", "Appendix B: Additional Foes, Claimants and Golem Warfare", "APPENDIX B."),
    ("app-c", "Appendix C: Open Procedure and Record Sheets", "APPENDIX C."),
    ("app-d", "Appendix D: The Six Original Maps", "APPENDIX D."),
]
HEADS = tuple(s[2] for s in SPLIT)

# statblock pages: replace the plain-text stat blocks with linked actor panels
NPC_PANEL_KEYS = ["janella-greenbottle", "ash-scrap-golem", "iron-warder-damaged", "iron-warder-restored", "contract-sentinel",
                  "writ-bailiff", "night-hag-advocate", "osric-kane", "hollis-valrick", "iron-heir"]
APPB_KEYS = ["vexa-corven", "marshal-kordren", "brass-factor-morn", "oathshard"]


def npc_panel(key):
    import bestiary as B
    a = next(x for v in B.FOLDERS.values() for x in v if x["_id"] == fid("actor:" + key))
    y = a["system"]
    hp = y["attributes"]["hp"]["max"]
    return (f'<div class="rc-npc">{IMG(a["img"], "rc-thumb")}<div><h4>{A(key, a["name"])}</h4>'
            f'<p class="rc-sptype"><em>CR {y["details"]["cr"]} · AC {y["attributes"]["ac"]["flat"]} · HP {hp}</em></p>'
            f'{y["details"]["biography"]["value"]}</div></div>')


def pages():
    idx = [next(i for i, l in enumerate(L) if l.startswith(h)) for h in HEADS]
    idx.append(len(L))
    out = []
    for n, (key, title, head) in enumerate(SPLIT):
        chunk = L[idx[n]:idx[n + 1]]
        if key == "app-d":
            chunk = chunk[:6]
        body = TB.render(chunk, tables=TABLES, readaloud=READ, skip_first=True,
                         h3=("Map ", "Scene ", "Phase ", "Round ", "Session ", "Conditions for entry", "Four conclusions",
                             "Keyed encounter locations", "Map 1 roll points", "Missing core", "Proof of Dominion",
                             "Misty’s second legal maneuver", "Transition to", "The three agendas", "Rival cast",
                             "Side quests", "The Citadel", "Three ways through", "Heartstone", "Lair:", "Actions",
                             "Bonus Actions", "Legendary Actions", "Mythic Trait", "Three Witness objectives",
                             "Escape and a genuine", "Misty’s battle voice", "The Iron Heir", "Mansion Consequences",
                             "Golemancer action-economy", "Legal verdict rubric", "Mansion Consequences", "Legal exhibits by chapter",
                             "Safety and consequences", "d6 rival-behaviour oracle", "Rulings to write", "Three table procedures",
                             "The cleanest mode", "No extra referee", "Status of this stat block", "Misty, Hell Hag Queen"))
        body = TB.link_first(body, ACTOR_LINKS)
        top = H(2, title)
        if key in SCENE_BOX:
            top += BOX("Scenes", " · ".join(SC(k, t) for k, t in SCENE_BOX[key]), cls="rc-box rc-scenes")
        if key in TOOLS:
            top += BOX("At the Table", TOOLS[key], cls="rc-box rc-tools")
        if key == "npcs":
            top += BOX("In the Actors compendium", "Every creature below is a finished actor with automated attacks, saves and "
                       "recharges. The book text follows for reference.", cls="rc-box")
            top += "".join(npc_panel(k) for k in NPC_PANEL_KEYS)
        if key == "app-b":
            top += "".join(npc_panel(k) for k in APPB_KEYS)
        if key == "app-a":
            top += npc_panel("misty") + npc_panel("misty-unbound") + npc_panel("child-of-hell") + npc_panel("heartstone")
        if key == "app-d":
            plates = [("welcome", "Plate I — Welcome to Hell (Map 1)"), ("findings", "Plate II — Unexpected Findings (Map 2)"),
                      ("greyhurst", "Plate III — The Fallen / Greyhurst (Map 3)"), ("mansion-lower", "Plate IV — Sorcerous Implications (Map 4)"),
                      ("mansion-upper", "Plate V — Sorcerous Implications II (Map 5)"), ("arena", "Plate VI — Brass Arena (Map 6)")]
            body += P("Each plate is rebuilt here as a full-resolution vector battlemap following the 2020 original's layout, "
                      "with walls, doors, lighting and keyed journal pins. The original coloured encounter markers are journal "
                      "notes on the scene, not printed on the art.") + "".join(
                f'<figure class="rc-plate">{IMG(f"modules/{MOD}/assets/maps/{k}.webp", "rc-mapplate")}<figcaption>{SC(k, t)}</figcaption></figure>'
                for k, t in plates)
            body += P("<em>End of Book I. The tournament's Charter, subclasses, seventeen new contractual spells, fourteen magic "
                      "items, eight forms and six level-12 claimants are in Book II, " + uuid_journal("book2", None, "Claimants of the First Crown") + ".</em>")
        out.append((key, title, top + body))
    return out


OVERVIEW = (BANNER("Interest of Asmodeus · A sequel to The Night of the Red Clause", "Interplanal Champions",
                   "Book I: The Throne of Avernus · Levels 12–17 · A campaign of infernal succession for D&amp;D 5e") +
            '<p class="rc-tagline">In Hell, the strongest take the throne. The devious keep it. The wise read what they have signed.</p>' +
            SPEC(("Party", "4–6 characters of 12th level, ending around 17th (six pregenerated claimants included)"),
                 ("Length", "18–24 sessions across six chapters"), ("Setting", "Avernus, the First Layer of the Nine Hells"),
                 ("Rules", "D&amp;D 5e (2014), with 2024 conversion notes"),
                 ("Original", "Based on <em>Interplanal Champion: Interest of Asmodeus</em> (2020)")) +
            H(2, "The Premise") +
            P("Asmodeus has opened a new Rite of Succession for the First Layer of Hell. Challengers from many planes may compete "
              "for the throne of Avernus. Victory requires more than violence: contestants must prove <strong>Survival</strong>, "
              "<strong>Deviousness</strong> and <strong>Dominion</strong>, and every crown is a contract. A sole regent may rule; "
              "a declared allied slate may share power; a contestant may represent a patron; anyone may withdraw on the terms "
              "they signed.",
              "Behind the pageantry, a deputy registrar named " + A("hollis-valrick", "Hollis Valrick") + " is seeding the "
              "tournament with paper champions built from stolen names, the drowned town of Greyhurst has been registered as "
              "'unclaimed', and " + A("misty", "Misty, Queen of Barbed Chains") + " wants a clause giving her hags perpetual "
              "first refusal on every debt, memory and secret the winner collects.") +
            H(2, "Contents") +
            TABLE(["Chapter", "Sessions", "Levels", "Pages"], [
                ["Running the Championship", "", "", uuid_journal("book1", "running", "1. Running") + " · " + uuid_journal("book1", "bridge", "Bridge") + " · " + uuid_journal("book1", "audit", "2. The Succession Audit")],
                ["I. Dead Already", "1–3", "12", uuid_journal("book1", "ch1", "Chapter I") + " · " + uuid_journal("book1", "map1", "Map 1") + " · " + uuid_journal("book1", "map2", "Map 2")],
                ["II. The Fallen", "4–7", "13", uuid_journal("book1", "ch2", "Chapter II") + " · " + uuid_journal("book1", "map3", "Map 3") + " · " + uuid_journal("book1", "map4", "Map 4") + " · " + uuid_journal("book1", "map5", "Map 5")],
                ["Interlude: The Redline Run", "7–8", "13", uuid_journal("book1", "souljack-yard", "The Souljack Yard") + " · " + uuid_journal("book1", "redline", "The Redline Run")],
                ["III. The War of Claims", "8–11", "14", " · ".join(uuid_journal("book1", k, t) for k, t in (("ch3", "Chapter III"), ("s8", "8"), ("s9", "9"), ("s10", "10"), ("s11", "11")))],
                ["IV. Blood and Brass", "12–15", "15", " · ".join(uuid_journal("book1", k, t) for k, t in (("ch4", "Chapter IV"), ("s12", "12"), ("s13", "13"), ("s14", "14"), ("s15", "15")))],
                ["V. The Hag Queen's Due", "16–19", "16–17", " · ".join(uuid_journal("book1", k, t) for k, t in (("ch5", "Chapter V"), ("s16", "16"), ("s17", "17"), ("s18", "18"), ("s19", "19")))],
                ["VI. The Rite of the Nine", "20–24", "17", " · ".join(uuid_journal("book1", k, t) for k, t in (("ch6", "Chapter VI"), ("s20", "20"), ("s21", "21–22"), ("s23", "23"), ("s24", "24")))],
                ["Reference", "", "", " · ".join(uuid_journal("book1", k, t) for k, t in (("npcs", "NPCs"), ("arena-engine", "Arena & Tables"), ("procedure", "Open Procedure"), ("charter-ref", "Charter"), ("design-audit", "Design Audit"), ("app-a", "App. A"), ("app-b", "App. B"), ("app-c", "App. C"), ("app-d", "App. D")))]]) +
            H(2, "Getting Started") +
            P("Run the " + M("setup", "Championship Manager") + " and choose <strong>Set Up Everything</strong>. Hand each player the "
              + uuid_journal("handouts", "charter", "Championship Charter") + " and the " + uuid_journal("handouts", "invitation", "invitation")
              + ", let them choose a claimant from the pregens or bring their own, and open " + SC("welcome", "Map 1: Welcome to Hell") + "."))

import redline as _RL
_P1 = pages()
_i = next(i for i, p in enumerate(_P1) if p[0] == "map5") + 1
_RL_PAGES = [
    ("souljack-yard", "Interlude — The Souljack Yard", H(2, "Interlude — The Souljack Yard")
     + BOX("Scenes", SC("souljack-yard", "The Souljack Yard (Greyhurst)"), cls="rc-box rc-scenes")
     + BOX("At the Table", "Roll a coin: " + M("soul-coin", "Read a Soul Coin") + ". Hand out "
           + HO("furnace-quick", "the Soul Furnace Quick Sheet") + " and " + HO("loan-g12", "Form G-12") + ".", cls="rc-box rc-tools")
     + _RL.yard_page(A, I, T, HO).replace("<h2>The Souljack Yard</h2>", "")),
    ("redline", "Interlude — The Redline Run", H(2, "Interlude — The Redline Run")
     + BOX("Scenes", SC("redline-run", "The Redline Run (Claw Rift)"), cls="rc-box rc-scenes")
     + BOX("At the Table", M("redline", "Chase Tracker") + " · " + M("redline-round", "Next Round") + " · "
           + T("road-hazard", "Road Hazard") + " · " + T("enemy-plan", "Enemy Plan") + " · " + HO("writ-m9r", "Writ M-9-R")
           + " · " + HO("furnace-tracker", "Soul Furnace Tracker"), cls="rc-box rc-tools")
     + _RL.interlude_page(A, I, T, HO, SC)
     + H(3, "The Soul Furnace Codex (GM copy)") + _RL.codex_html()),
    ("soulforged-gm", "Running a Soulforged Artificer", H(2, "Running a Soulforged Artificer")
     + BOX("At the Table", M("generate-soul", "Generate a Soul") + " · " + HO("sf-record", "Form SF-01") + " · "
           + HO("sf-covenant", "Form SF-12") + " · " + T("sf-mishap", "Construct Mishap"), cls="rc-box rc-tools")
     + __import__("soulforged").gm_page())]
_P1[_i:_i] = _RL_PAGES
journal("book1", "Book I — The Throne of Avernus (GM)", "Books", [("overview", "Interplanal Champions", OVERVIEW)] + _P1, sort=0)
