"""GM Toolkit: setup, scenes, macros, tables, credits and the design audit."""
from jhelp import *
import bestiary as B, spells as SP, playeroptions as PO, tables as TBL, macros as MC

SCENES = [  # key, title, used in, lighting
    ("welcome", "Map 1: Welcome to Hell", "Chapter I", "Hellish daylight; lava glow"),
    ("counting-gate", "1A: The Counting Gate", "Chapter I", "Hellish daylight, braziers"),
    ("ash-bridge", "1B–1D: The Ash Bridge", "Chapter I", "Lava glow, notary light"),
    ("breach", "The Breach at Hollow Barrow", "Chapter I (optional arrival)", "Daylight bleeding into Hell"),
    ("findings", "Map 2: Unexpected Findings", "Chapter I", "Lava gorge"),
    ("styx-ferry", "2A–2C: The Ferryman's Landing", "Chapter I", "Dim; ferry lantern"),
    ("ashen-caverns", "The Ashen Caverns", "Chapter I–II (optional)", "Dark; lava vein and vents"),
    ("greyhurst", "Map 3: The Fallen (Greyhurst)", "Chapter II", "Ash-dark; braziers"),
    ("greyhurst-district", "Greyhurst: The Burgher's Row", "Chapter II", "Ash-dark; burning wreck"),
    ("tavern", "3A: The Drowned Tavern", "Chapter II", "Dark, braziers"),
    ("greenbottle", "3B–3E: The Greenbottle Alley", "Chapter II", "Dark; forge glow"),
    ("mansion-lower", "Map 4: The Mansion (Ground Floor)", "Chapter II", "Dim; altar and circle light"),
    ("mansion-upper", "Map 5: The Mansion (Upper Floor)", "Chapter II", "Dim; braziers"),
    ("market-names", "The Market of Names", "Chapter III, Session 8", "Bone-pale, torchlit"),
    ("docket", "The Whispering Docket", "Chapter III, Session 10", "Courtroom braziers"),
    ("masquerade", "The Trial of False Faces", "Chapter III, Session 11", "Dark; four coloured circles"),
    ("citadel", "The Hall of Registrants", "Chapter IV, Session 12", "Brass hall; practice-floor braziers"),
    ("iron-quarter", "The Iron Quarter", "Chapter IV, Session 13", "Dark; forge and pylons"),
    ("arena", "Map 6: The Brass Arena", "Chapters IV and VI", "Lava cross, crystals, dais"),
    ("claw-rift", "The Claw Rift (scrolling)", "Chapter IV, Session 15 chase", "Fire bands; loops east–west"),
    ("audience", "The Chamber of Iron Roses", "Chapter V, Sessions 16 and 19", "Very dark; rose-red"),
    ("reliquary", "The Thorn Reliquary", "Chapter V, Sessions 18–19", "Very dark; Heartstone pulse"),
]

K_ = [("toolkit", "Using This Module",
       BANNER("GM Toolkit", "Using This Module", "Setup, scenes, macros and tables") +
       H(2, "One-Click Setup") +
       P("Open <strong>Game Settings → Configure Settings → Interplanal Champions → Championship Manager</strong> (or run the "
         + uuid_macro("setup", "Championship Manager") + " macro) and choose <strong>Set Up Everything</strong>. It will:") +
       OL("Import every actor, claimant, item, spell, subclass, journal, roll table and macro into labelled world folders under "
          "<em>Interplanal Champions</em>.",
          f"Build all {len(SCENES)} scenes: maps, walls, doors, lighting, journal pins on every keyed location (pins open the "
          "matching page of Book I), and the cast already standing where they belong. Ambushers and late arrivals are hidden.",
          "Create a landing scene with the title art and open Book I.") +
       P("You can also install content only, rebuild a single scene, or remove everything. <strong>Rebuilding a scene is "
         "safe</strong>: it replaces only the walls, lights, notes and tokens the module created and keeps anything you placed "
         "yourself. Use <em>Update Content</em> after a module update.") +
       H(2, "Scenes") +
       TABLE(["#", "Scene", "Used in", "Lighting"], [[str(i + 1), scene_link(k, t), u, l] for i, (k, t, u, l) in enumerate(SCENES)]) +
       H(2, "The Championship Board") +
       P("The " + uuid_macro("board", "Championship Board") + " is a small shared panel for the whole table: each registered "
         "claimant or slate with its three Proofs and Crown Marks, the three public clocks (Blood War Pressure, Hag Lien, Public "
         "Legitimacy, 0–6), and the three Heartstone witness-seals. The GM clicks to change it; players see it update live. "
         "Certifying a Proof, filling a clock or suppressing a seal posts the Brass Arbiter's ruling to chat.") +
       H(2, "Macros") +
       TABLE(["Macro", "What it does"], [
           [uuid_macro("setup", "Championship Manager"), "Install, update, rebuild scenes, remove."],
           [uuid_macro("board", "Championship Board"), "Show or hide the Proofs, Marks, clocks and seals panel."],
           [uuid_macro("handout", "Show Handout"), "Show any handout page to the players."],
           [uuid_macro("challenge", "Group Challenge"), "Successes-before-failures tracker (the Ash Bridge is 3 before 2, DC 16)."],
           [uuid_macro("save", "Request Group Save"), "Posts a save request card."],
           [uuid_macro("arena", "Arena Hazard"), "Rolls the arena d6 at initiative count 20 and draws summons on a 6."],
           [uuid_macro("tribunal", "Convene a Hearing"), "Three-stage hearing (Admissibility, Authority, Remedy) or a 2-before-2 petition."],
           [uuid_macro("exhibit", "Present an Exhibit"), "Posts an exhibit's text with the Arbiter's acknowledgement."],
           [uuid_macro("battle", "The Ash March"), "The three-exchange mass battle; moves the clocks for you."],
           [uuid_macro("mythic", "Hag Queen's Deception"), "Misty's mythic phase: posts the transition and opens the Thorn Reliquary."]]) +
       H(2, "Roll Tables") +
       P(", ".join(uuid_table(t["flags"][MOD]["key"], t["name"]) for t in TBL.TABLES) + ".") +
       H(2, "Credits") +
       H(3, "With Thanks") +
       P("<em>Interplanal Champions</em> grew out of <em>Interplanal Champion: Interest of Asmodeus</em>, first run at the table in "
         "2020 as the follow-on to <em>The Night of the Red Clause</em>. My thanks to everyone who played the original versions on the "
         "<strong>Blown Away</strong> server, my first playtest group and the first D&amp;D server I ran. You crossed the first lava "
         "river, argued with the first imps and walked into the first arena, and every page of this campaign is better for it.",
         "Special thanks to the playtesters, <strong>Tim, Alex, Heather and Kai</strong>, and to the <strong>Pacts &amp; "
         "Polyhedrals</strong>, <strong>Blown Away</strong> and <strong>Imagi-Nations</strong> Discord servers.") +
       P("Written and designed by <strong>Asmo</strong>, Pacts &amp; Polyhedrals (Ben Vale). The Asmodeun Scriptorium by Asmo. Vector "
         "battlemaps (after the 2020 originals), portraits, tokens and icons made for this module.",
         "Support the work on <a href=\"https://www.patreon.com/pactsandpolyhedrals\">Patreon</a> · play with Asmo on "
         "<a href=\"https://startplaying.games/gm/dmasmo\">StartPlaying</a>.",
         "<em>Not affiliated with Wizards of the Coast. Uses the D&amp;D 5e SRD (CC-BY-4.0) via the Foundry dnd5e system. Barbed "
         "devils, horned devils and fire mephits referenced in the arena tables use their published SRD blocks.</em>"))]

dn = H(2, "Design Notes & Rules Audit") + P(
    "Everything below was checked against the 2014 rules and the dnd5e 5.3.3 system data. Where a number or rule had to be "
    "supplied or changed, it is listed here so you can revert anything you prefer as written.")
dn += H(3, "Creatures") + UL(*B.DESIGN_NOTES)
dn += H(3, "Spells") + UL(*SP.SPELL_NOTES)
dn += H(3, "Subclasses") + UL(*PO.SUB_NOTES)
dn += H(3, "Maps") + UL(
    "The six original maps are rebuilt as vector battlemaps following the 2020 layouts, at larger grid sizes so every original "
    "feature has room: Map 1 44×44, Map 2 64×46, Map 3 48×36, Maps 4–5 48×32, Map 6 40×40 squares.",
    "The original coloured encounter dots (spawn, E1–E4, boss, treasure) are journal pins, not baked into the art, so the maps "
    "stay clean for players.",
    "Sixteen further maps cover the keyed locations inside those maps (the Counting Gate, Ash Bridge, Styx landing, Drowned "
    "Tavern, Greenbottle alley, the Market of Names, the Docket, the masquerade, the Hall of Registrants, the Iron Quarter, the "
    "Chamber of Iron Roses and the Thorn Reliquary) and four locations supplied later (the Breach, Greyhurst's Burgher's Row, "
    "the Ashen Caverns and the Claw Rift).",
    "The Claw Rift is mirror-symmetric top to bottom and tiles seamlessly left to right (a 50-ft module), so it can be used as a "
    "looping chase map.")
dn += H(3, "Naming") + UL(
    "The draft's deputy registrar <em>Hesper Valrick</em> is <strong>Hollis Valrick</strong> throughout, so he is never confused "
    "with Hesper Vane from <em>The Night of the Red Clause</em>.",
    "The campaign keeps the original spelling <em>Interplanal</em>.")
K_.append(("design-notes", "Design Notes & Rules Audit", dn))
journal("toolkit", "GM Toolkit — Interplanal Champions", "Books", K_, sort=50000)
