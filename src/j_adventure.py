"""The adventure book."""
from jhelp import *

A = uuid_actor
I = uuid_item
HO = lambda k, n: uuid_journal("handouts", k, n)
T = uuid_table
M = uuid_macro
SC = scene_link
pg = []


def page(key, title, html):
    pg.append((key, title, html))


# ---------------------------------------------------------------------------
page("overview", "The Adventure at a Glance", BANNER(
    "A Dungeons &amp; Dragons Midwinter One-Shot", "The Night of the Red Clause",
    "Waterdeep · Level 11 · 4–6 Hours · An infernal comedy of errors, obligations, repossessions and eternal damnation") +
    f'<p class="rc-tagline">He\'s watching while you\'re dreaming. He\'s counting while you wake. He knows when you\'ve breached your '
    f'contractual obligations, and your appeal has been rejected.</p>' +
    SPEC(("Party", "4–6 characters of 11th level (six pregenerated heroes included)"), ("Target runtime", "5 hours"),
         ("Setting", "Waterdeep, Midwinter (between Hammer 30 and Alturiak 1)"),
         ("Final encounter", "Combat and infernal arbitration"), ("Rules", "D&amp;D 5e (2014), works with 2024 play")) +
    H(2, "The Premise") +
    P("On Midwinter, Waterdeep becomes a spectacular winter wonderland. A mysterious new charity, the <strong>Hearthlight "
      "Foundation</strong>, has handed enchanted gifts to thousands of citizens. Poverty has briefly been forgotten. The sick "
      "have been healed. The snow-covered streets glow with magical lanterns.",
      "Its eccentric founder, an enormous jolly fellow dressed in crimson, has promised joy to every household. There is "
      "just one condition: everyone who accepts a gift must perform an act of genuine kindness. Those who fail owe the "
      "foundation one night of festive service.",
      "Perfectly reasonable. Until the bells begin to ring.",
      "The foundation is a front for an infernal corporation headquartered in Nessus. Its founder, "
      + A("red-clause", "Nicholas Red Clause") + ", is a specially constructed avatar empowered by Asmodeus. Its cheerful "
      "Christmas workshop is an extradimensional industrial nightmare where souls are processed as commodities, people are "
      "worked beyond the limits of their contracts, and every scream is classified as a voluntary expression of seasonal "
      "enthusiasm.",
      "But the Red Clause is doing more than harvesting souls. He is trying to establish a new infernal <em>legal "
      "precedent</em>: that accepting a freely offered gift can eventually create transferable ownership rights over a "
      "mortal soul. If he succeeds, Asmodeus could roll the model out across Faerûn.",
      "The party has until the <strong>Ninth Bell</strong> to stop the experiment, invalidate the contracts and keep the "
      "citizens of Waterdeep from becoming assets of the Nine Hells.") +
    SECRET("The DM's Central Secret",
           "The original gift contracts are not inherently evil. <strong>The Red Clause's enforcement system is "
           "fraudulent.</strong>",
           "The contracts genuinely grant gifts and promise only limited consequences for breaking the agreement. The horror "
           "comes from the Red Clause secretly altering the accounting records, falsifying the delivery of notices, "
           "manipulating time and reclassifying unwilling mortals as abandoned infernal property.",
           "This matters: the heroes can win using the <em>actual language of the contracts</em>, not a loophole invented "
           "in the last scene. Give players the " + HO("certificate", "Certificate of Festive Entitlement") + " as soon as "
           "anyone receives a gift, and let careful reading pay off.") +
    H(2, "Where Everything Lives") +
    UL("<strong>Scenes:</strong> " + ", ".join([SC("market", "The Market"), SC("pavilion", "Foundation Pavilion"),
                                                  SC("records", "City Records"), SC("depot", "Delivery Depot"),
                                                  SC("rooftops", "Rooftops"), SC("intake", "Intake"),
                                                  SC("assembly", "Assembly Line"), SC("midnight", "Perpetual Midnight"),
                                                  SC("ledger", "Ledger of Abandoned Souls"), SC("court", "High Court")]) +
       " (built by the Red Clause Manager; see the GM Toolkit).",
       "<strong>Handouts:</strong> " + uuid_journal("handouts", None, "The Handouts journal") + ".",
       "<strong>Tools:</strong> the " + M("bells", "Midnight Docket") + " bell tracker, " + M("exhibit", "Present an Exhibit") +
       ", and the rest of the macros in the <em>Night of the Red Clause — Macros</em> compendium.",
       "<strong>Player options:</strong> " + uuid_journal("scriptorium", None, "The Asmodeun Scriptorium") +
       " (contract magic, subclasses and lore)."))

page("structure", "Session Structure & Tone",
     H(2, "Five-Hour Schedule") +
     TABLE(["Time", "Scene", "Intended Feeling"], [
         ["0:00–0:10", "Character hooks and opening", "Festive"],
         ["0:10–0:55", "Act I: The Hearthlight Festival", "Absurd comedy"],
         ["0:55–1:25", "Act II: The First Collections", "Comedy turns sinister"],
         ["1:25–2:15", "Investigation across Waterdeep", "Mystery and dread"],
         ["2:15–3:20", "Act III: Workshop of Good Intentions", "Full horror"],
         ["3:20–4:40", "Act IV: The Final Arbitration", "Combat, legal warfare"],
         ["4:40–5:00", "Epilogue and consequences", "Victory or damnation"]]) +
     BOX("Four Hours", "Shorten the festival to 30 minutes, run two investigation locations, use two workshop chambers and "
                       "keep the final encounter to about 65 minutes.") +
     BOX("Six Hours", "Add the optional " + uuid_journal("adventure", "sleigh-chase", "rooftop sleigh chase") + ", a second "
                      "workshop dilemma and extra time for the tribunal.") +
     H(2, "Tone Direction") +
     '<div class="rc-arc"><span>Festive farce</span><span>Uncertainty</span><span>Industrial horror</span><span>Infernal judgment</span></div>' +
     SECRET("Essential Direction",
            "In the opening act the Red Clause should be <strong>genuinely funny</strong>. By the final act he should be "
            "terrifying precisely <strong>because he has stopped being funny</strong>.") +
     P("The horror should come from stolen identity, coercion, industrialised suffering and cosmic indifference rather than "
       "graphic violence. Before play, confirm the group's boundaries for body horror and threatened civilians.") +
     H(2, "Character Hooks") +
     UL("An invitation to the Hearthlight Festival as honoured guests of the city.",
        "Local reputation: the Watch would like heroes visible at the busiest Midwinter in years.",
        "Investigating unusual magic: a sage has noticed a great deal of infernal-grade enchantment in very cheap presents.",
        "Simply celebrating Midwinter after last year's adventures.",
        "Pregenerated heroes have personal hooks on their sheets; see " + uuid_journal("pregens", None, "Pregenerated Heroes") + "."))

# ---------------------------------------------------------------------------
page("act1-opening", "Act I — Merry Christmas, You Filthy Mortals",
     BANNER("Act I · 45 minutes", "Merry Christmas, You Filthy Mortals", "The Market, Castle Ward · " + SC("market", "Open the scene")) +
     RA("Snow falls gently across the City of Splendors. Waterdeep has endured many strange Midwinter celebrations, but "
        "none quite like this.",
        "The streets shimmer with golden lanterns. Enormous candy canes grow from the cobblestones. A brass reindeer flies "
        "drunkenly above the rooftops, trailing sparks and festive music.",
        "A choir of animated snowmen sings a song about generosity, kindness, and the timely settlement of outstanding "
        "accounts.",
        "Above the marketplace hangs a magnificent crimson banner: <strong>THE HEARTHLIGHT FOUNDATION — HAPPINESS GUARANTEED! "
        "TERMS AND CONDITIONS APPLY.</strong>",
        "Beneath it, a tiny creature in a green hat is arguing with a dwarf. \"Sir! You have exceeded your daily allowance "
        "of grumpiness!\"",
        "The dwarf punches him. A magical bell rings.",
        "\"VIOLENCE AGAINST FESTIVE PERSONNEL! THAT'S ANOTHER FIVE GOLD!\"") +
     P("Give the players freedom to mingle and have fun. The aim is to establish the foundation as funny, generous and "
       "<em>slightly</em> suspicious without revealing the threat.",
       "Roll on " + T("market-moments", "Midwinter Market Moments") + " whenever the scene needs a nudge. The " +
       A("carolling-snowman", "Carolling Snowmen") + " sing all day; the " + A("festive-clerk", "Festive Clerks") +
       " hand out gifts and citations.") +
     H(3, "Running the Market") +
     OL(uuid_journal("adventure", "act1-bureau", "Encounter A: The Bureau of Festive Compliance"),
        uuid_journal("adventure", "act1-gifts", "Encounter B: The Nine Gifts of Midwinter"),
        uuid_journal("adventure", "act1-dasher", "Encounter C: The Runaway Reindeer"),
        uuid_journal("adventure", "act1-arrival", "The Arrival of Nicholas Red Clause")))

page("act1-bureau", "Encounter A: The Bureau of Festive Compliance",
     IMG(portrait("sprocket-jingles"), "rc-portrait rc-right") +
     P("The foundation employs small green-clad clerks who look like traditional Christmas elves. They are minor devils "
       "operating under contractual disguises (" + A("festive-clerk", "Festive Clerk") + "). Their supervisor is " +
       A("sprocket-jingles", "Sprocket Jingles") + ", a bespectacled imp with a tiny brass clipboard.") +
     SPEC(("Disposition", "Cheerfully officious, utterly terrified of his employer."),
          ("Voice", "Nasal, fast, constantly correcting himself."),
          ("Public secret", "Employees receive a commission for every citizen who accepts a gift."),
          ("Private secret", "Sprocket has been falsifying his own employee happiness reports for three centuries.")) +
     P("He approaches the party and begins his inspection. Use the fines as quick roleplay prompts, or roll on " +
       T("festive-fines", "Festive Compliance Fines") + " (the " + M("fine", "Issue a Festive Fine") + " macro targets a "
       "selected token).") +
     TABLE(["Accusation", "Fine"], [["Insufficiently festive expression", "5 gp"], ["Unauthorised humbuggery", "10 gp"],
                                    ["Failure to reciprocate a seasonal greeting", "15 gp"],
                                    ["Excessive use of sarcasm", "20 gp"],
                                    ["Premeditated carolling without a licence", "50 gp"],
                                    ["Displaying an unregistered magical beard", "100 gp"]]) +
     P("The fines are ridiculous and <strong>unenforceable</strong>: Sprocket cannot confiscate anyone's property for "
       "refusing to pay. Players can argue, intimidate him, make him laugh or turn his own regulations against him. Reward "
       "inventive play with a free confection, a silly " + I("sprocket-citation", "citation") + " or a small prize.") +
     UL(chk("insight", 14) + " reveals that Sprocket's enthusiasm is partly genuine and partly terror.",
        chk("arcana religion", 15) + " identifies a faint infernal signature on his clipboard.") +
     SECRET("Keep Sprocket Alive", "Don't turn this into combat. Sprocket is far more useful alive: he knows the "
                                   "service-elevator code <code>GOODWILL-999</code> and can turn up again in the workshop "
                                   "and the epilogue."))

page("act1-gifts", "Encounter B: The Nine Gifts of Midwinter",
     P("The foundation distributes nine kinds of magical gift. Let interested characters choose one, or roll on " +
       T("nine-gifts", "The Nine Gifts of Midwinter") + ". Each is genuinely useful and carries the same separate contractual "
       "obligation. <strong>The gift itself has no secretly imposed mechanical drawback.</strong> Drag the item onto the "
       "character's sheet from the compendium, or use the " + M("gift", "Hand Out a Gift") + " macro.") +
     TABLE(["Gift", "Benefit", "Later Revelation"], [
         [I("everwarm-scarf", "The Everwarm Scarf"), "Resistance to cold damage for 1 hour", "Woven by debtors trapped in an endless winter"],
         [I("candy-cane-mercy", "The Candy Cane of Mercy"), "Action: restore 5d8 + 5 HP to a creature; once", "Manufactured using confiscated healing magic"],
         [I("bell-perfect-timing", "The Bell of Perfect Timing"), "Add 1d8 to one failed ability check or saving throw", "Its recorded ring can be used as evidence"],
         [I("jolly-soldier", "The Jolly Soldier"), "Summon a toy soldier that follows simple commands for 1 hour", "Other soldiers serve as enforcement units"],
         [I("stocking-holding", "The Stocking of Holding"), "Store up to 50 lb. in a miniature extradimensional space", "Uses the workshop's storage network"],
         [I("gingerbread-champion", "The Gingerbread Champion"), "Gain 15 temporary HP for 1 hour", "Originally designed as a workforce stimulant"],
         [I("star-good-fortune", "The Star of Good Fortune"), "Reroll one d20; once", "Its serial number identifies the legal issuer"],
         [I("mirror-merriment", "The Mirror of Merriment"), "Cast <em>disguise self</em> once without a slot", "Stores a record of its original owner"],
         [I("hearthlight-candle", "The Hearthlight Candle"), "Once, <em>see invisibility</em> for 10 minutes", "Reveals hidden infernal lettering on documents"]]) +
     P("All consumable benefits expire at the end of the adventure. The soldier uses the " + A("toy-soldier", "Festive Toy Soldier") +
       " statistics and won't attack its recipient unless someone independently uses a command override.",
       "The point isn't to punish players for accepting gifts. It's to tempt them into the same system that is exploiting "
       "Waterdeep.") +
     H(3, "Player Handout 1: The Actual Gift Contract") +
     P("Show the " + HO("certificate", "Certificate of Festive Entitlement") + " (or use the " + M("handout", "Show Handout") +
       " macro) the moment anyone receives a gift.") +
     SECRET("DM-Only Contract Ruling",
            "The certificate is binding when voluntarily accepted, but grants only the precise rights stated. A character "
            "who completes a genuine act of kindness has fulfilled it. Someone who doesn't accept a gift has no obligation. "
            "<strong>Even genuine defaulters cannot have their souls repossessed under this document.</strong>",
            "The foundation's later enforcement rests on falsified records and unauthorised supplemental notices.",
            "If a character reads the contract carefully now and spots its protections, reward them. That knowledge is "
            "meant to matter in the High Court."))

page("act1-dasher", "Encounter C: The Runaway Reindeer",
     IMG(portrait("dash-er"), "rc-portrait rc-right") +
     P("As the players explore, a clockwork reindeer named " + A("dash-er", "DASH-ER 3000") + " breaks free from a delivery "
       "sleigh. It has eight legs, two flaming antlers and a malfunctioning navigation system. It races through the market "
       "shouting <em>\"DELIVERY ATTEMPT FAILED! RECIPIENT NOT AT ADDRESS!\"</em>, crashes through a pastry stall and tries to "
       "deliver sixteen barrels of enchanted eggnog to the same terrified merchant, " + A("harl-bramble", "Old Harl Bramble") + ".") +
     BOX("Skill Challenge: Three Successes Before Two Failures",
         "DC 15. Suitable checks: " + chk("athletics", 15) + ", " + chk("acrobatics", 15) + ", " +
         chk("animal-handling", 15) + ", " + chk("arcana", 15) + ", or creative spellcasting. Track it with the " +
         M("challenge", "Skill Challenge") + " macro.",
         "<strong>Success:</strong> the machine stops without being destroyed, and the party earns public applause.",
         "<strong>Failure:</strong> a spectacular, nonlethal explosion of pastries and eggnog. DASH-ER eventually shuts "
         "itself down.") +
     P("Examining its " + I("dasher-manifest", "delivery manifest") + " reveals its true destination: <strong>Workshop Nine, "
       "Nessus Distribution Network.</strong> Right now it sounds like another bureaucratic joke. Later it becomes an "
       "important lead."))

page("act1-arrival", "The Arrival of Nicholas Red Clause",
     IMG(portrait("red-clause"), "rc-portrait rc-right") +
     P("After the players have enjoyed some festive nonsense, the Red Clause's sleigh descends through a magical snowstorm "
       "onto the Sleigh Landing, pulled by nine " + A("hellforged-reindeer", "mechanical nightmare reindeer") + " whose "
       "flaming eyes are hidden beneath ridiculous decorative antlers.",
       "He is about nine feet tall, with curling black horns, an enormous white beard, polished spectacles, a crimson coat "
       "and a sack larger than a carriage. His body creaks like a clockwork machine. He smells faintly of cinnamon and "
       "brimstone.") +
     RA("\"HO! HO! HO!\"", "\"WATERDEEP! WHAT A MAGNIFICENT COLLECTION OF POTENTIAL CUSTOMERS!\"",
        "\"I COME BEARING GIFTS, GOODWILL, AND A LIMITED-TIME OPPORTUNITY TO IMPROVE YOUR OVERALL MORAL CREDIT RATING!\"",
        "\"Remember, my little sugarplums: a promise made is a promise paid!\"",
        "He looks directly at the adventurers. \"And you lot look like you have VERY expensive souls!\"",
        "He throws back his head and laughs. \"HA! HA! HA! Just a little joke from your old pal Nicholas!\"") +
     P("Allow brief interactions. He compliments heroic reputations, guesses oddly personal details and offers absurd "
       "presents. Use the " + T("red-dialogue", "Red Clause's Dialogue") + " table freely.") +
     SECRET("He Must Not Be Defeated in Act I",
            "He won't attack unless attacked. If the party attacks, his festive projection shatters into wrapping paper, "
            "leaving a note: <em>Please present all complaints to the Workshop Nine arbitration desk.</em> His token on the "
            "Market scene is hidden; reveal it for the arrival and delete it when he leaves.") +
     P("<strong>Transition:</strong> as his sleigh disappears, a single deep bell begins to sound. Run the " +
       M("nightfall", "Nightfall") + " macro to bring sunset over the Market (the street lamps light themselves)."))

page("act2", "Act II — The First Collections",
     BANNER("Act II · 30 minutes", "The First Collections", "The Festival, shortly after sunset") +
     P("The transformation begins with <strong>one small incident</strong>, not a citywide explosion.") +
     H(3, "The Woman Who Gave Away Her Bread") +
     IMG(portrait("edda-hearth"), "rc-portrait rc-right") +
     P(A("edda-hearth", "Edda Hearth") + " is an elderly halfling baker who has spent the day giving free bread to people "
       "struggling through winter. Warm, generous and entirely unremarkable. She accepted an Everwarm Scarf, and in return "
       "gave a loaf to a grieving widow, " + A("agna-vell", "Agna Vell") + ". Several people saw it. Her kindness was "
       "recorded.",
       "But the system rejected it: the widow was still unhappy afterwards, so the auditor ruled that no measurable "
       "happiness had been created. This is legally irrelevant. <strong>The contract requires kindness, not demonstrable "
       "happiness.</strong>") +
     RA("The bell sounds again. Every enchanted decoration in the market stops moving. The singing snowmen fall silent.",
        "A tiny mechanical soldier turns its painted face towards an old halfling woman carrying a basket of bread.",
        "\"CITIZEN EDDA HEARTH. ACT OF RECIPROCITY NOT VERIFIED.\"",
        "Edda blinks. \"But I gave away all my bread.\"", "\"INSUFFICIENT POSITIVE EMOTIONAL OUTCOME.\"",
        "\"The poor woman's husband died yesterday!\"", "\"GRIEF IS NOT A RECOGNISED EXEMPTION.\"",
        "Three enormous ribbons of red wrapping paper unwind from a nearby present. They wrap themselves around Edda's wrists.",
        "For the first time that evening, the mechanical soldier stops smiling.", "\"PLEASE DO NOT RESIST YOUR GIFT.\"") +
     H(3, "Encounter: Festive Enforcement (15–20 minutes)") +
     P("For five 11th-level characters, reveal two " + A("jingle-bailiff", "Jingle Bailiffs") + " and two " +
       A("toy-soldier", "Festive Toy Soldiers") + " (they're hidden on the Market scene). The bailiffs have three objectives: "
       "secure Edda, confiscate her gift receipt, and deliver her to a waiting collection sack. They don't attack the crowd "
       "at first.") +
     H(4, "Ways to Resolve the Scene") +
     UL("Defeat or restrain the bailiffs, freeing Edda.",
        "Present testimony proving Edda fulfilled her promise (Agna will testify).",
        "File an immediate appeal on Edda's behalf. A bailiff receiving a valid appeal must suspend collection (its "
        "<em>Appeal Protocol</em>), though it may insist on a stamp or form.",
        "Hack, dispel or sabotage the bailiffs' command network.") +
     SECRET("If They Find the Legal Solution, Let It Work",
            "The devices are programmed to respect a properly filed appeal; the system has merely been hiding the procedure.",
            "If Edda is taken, she can be rescued in the workshop (her token waits hidden in the Assembly Line pens). Her "
            "basket and receipt stay behind with the same information.") +
     H(3, "The First Evidence") +
     P("Edda's receipt (" + HO("receipt", "handout") + ", item: " + I("edda-receipt", "Edda's Reciprocity Record") + ") shows "
       "two separate irregularities: her deed was recorded as <strong>fulfilled</strong> before being changed, and the "
       "notice went to an <strong>impossible address</strong> in Nessus. The heroes now have reason to suspect the whole "
       "celebration is a fraudulent collection scheme."))

page("act2-marta", "Sergeant Marta Quill Arrives",
     IMG(portrait("marta-quill"), "rc-portrait rc-right") +
     P(A("marta-quill", "Sergeant Marta Quill") + " is a veteran officer of the City Watch, overseeing festival safety. "
       "Tired, efficient and deeply irritated by magically binding bureaucracy.") +
     RA("\"First somebody turns the city's gutters into peppermint, and now we've got arrest warrants from Hell. I "
        "should've taken that bloody promotion.\"", title="Marta Quill") +
     P("She tells the party that several people have vanished across the city. The Watch cannot locate the foundation's "
       "headquarters, and formal requests for information get automated denials.",
       "She can give the party temporary authority to investigate on the Watch's behalf. <strong>This gives them standing to "
       "challenge the contracts even if none of them accepted a gift.</strong>",
       "She also confirms that Waterdeep's residential records list nobody as living in Nessus.") +
     RA("\"Find the people they've taken. Bring them home.\"", title="Her Request"))

# ---------------------------------------------------------------------------
page("investigation", "Investigation — Follow the Paperwork",
     BANNER("Investigation · 50 minutes", "Follow the Paperwork", "Run two of the three leads") +
     P("The players need to discover the nature of the workshop and gather evidence for the final confrontation.") +
     SECRET("No Single Point of Failure",
            "Don't make any essential clue depend on a single successful check. Spells, clever reasoning, intimidation, "
            "negotiation, theft and force should all work.") +
     TABLE(["Lead", "Where", "Evidence"], [
         [uuid_journal("adventure", "lead-a", "Lead A"), SC("pavilion", "The Foundation Pavilion"), I("exhibit-a", "Exhibit A: Falsified Defaults")],
         [uuid_journal("adventure", "lead-b", "Lead B"), SC("records", "City Records (Font of Knowledge)"), I("exhibit-b", "Exhibit B: Falsified Service Addresses")],
         [uuid_journal("adventure", "lead-c", "Lead C"), SC("depot", "The Hidden Delivery Depot"), I("exhibit-c", "Exhibit C: The Endless-Night Mechanism")]]) +
     H(3, "What the Players Should Understand") +
     UL("The foundation is falsifying defaults and notices.",
        "Its extradimensional workshop is central to the operation.",
        "The Red Clause acts under Asmodeus's authority, but is trying to stretch that authority beyond the original contracts.",
        "<strong>Most importantly:</strong> the Brass Arbiter is required by the foundation's own agreement to consider valid "
        "evidence.") +
     P("<em>Even devils must obey the machinery of their bargains when properly invoked.</em>"))

page("lead-a", "Lead A: The Foundation Pavilion",
     P(SC("pavilion", "Open the Pavilion scene") + ". The festival's administrative tent holds a public ledger and a hidden "
       "enchanted verification register behind the clerk's desk.",
       chk("investigation arcana", 15) + " reveals that thousands of fulfilled kindness obligations were changed to defaults "
       "by an automated command: <code>HOLIDAY_OVERRIDE</code>. A " + I("hearthlight-candle", "Hearthlight Candle") + " or " +
       uuid_spell("read-the-fine-print", "read the fine print") + " shows the revisions at a glance.",
       "Characters can obtain a certified copy of the original ledger, marked with the foundation's own magical seal: " +
       I("exhibit-a", "Exhibit A: Evidence of Falsified Defaults") + " (" + HO("exhibit-a", "handout") + ").") +
     BOX("The Service Elevator", "A curtained alcove at the back hides the concealed service elevator to Workshop Nine "
                                 "(a secret door on the scene). Code: <code>GOODWILL-999</code>. See " +
         uuid_journal("adventure", "finding-workshop", "Finding the Workshop") + "."))

page("lead-b", "Lead B: City Records",
     IMG(portrait("ossian-pell"), "rc-portrait rc-right") +
     P(SC("records", "Open the City Records scene") + ". The City Watch or the Font of Knowledge, a temple of Oghma, can help "
       "identify the legal discrepancy. " + A("ossian-pell", "Ossian Pell") + ", a fussy clerk, keeps the residence rolls.",
       "Comparing foundation notice records with actual addresses shows every seized recipient listed as residing "
       "somewhere in Nessus, despite living in Waterdeep. Pell discovers the addresses were changed immediately before the "
       "notices were issued (" + chk("investigation history", 14) + " to spot it first; otherwise Pell finds it in ten minutes).",
       "Characters obtain certified Waterdeep residence records: " + I("exhibit-b", "Exhibit B: Evidence of Falsified Service "
                                                                                    "Addresses") + " (" + HO("exhibit-b", "handout") + ")."))

page("lead-c", "Lead C: The Delivery Depot",
     IMG(portrait("mizzle"), "rc-portrait rc-right") +
     P(SC("depot", "Open the Delivery Depot scene") + ". A hidden depot on the edge of the Castle Ward is processing "
       "enchanted parcels. A frightened imp called " + A("mizzle", "Mizzle") + " manages the shipping manifests. He will talk "
       "if offered protection, a credible escape plan or immunity from ordinary prosecution (" + chk("persuasion", 13) +
       ", or automatic with a sincere offer).",
       "Mizzle explains that the workshop is a pocket dimension linked to Waterdeep through magical deliveries. Its entire "
       "purpose is to keep workers from reaching the end of their contractual night.",
       "He can provide a " + I("access-token", "Service Access Token") + " and a " + I("maintenance-schematic", "Maintenance "
                                                                                                                "Schematic") +
       ": " + I("exhibit-c", "Exhibit C: The Endless-Night Mechanism") + " (" + HO("exhibit-c", "handout") + ").") +
     SECRET("Guards", "Two Festive Clerks and two Toy Soldiers work the floor. A Brass Supervisor (hidden) arrives if the "
                      "alarm is raised. The sleigh in the bay is the party's ride for the Sleigh Route."))

page("carol-callback", "The Christmas Carol Callback",
     IMG(portrait("midwinter-ghost"), "rc-portrait rc-right") +
     P("If you ran a Christmas Carol adventure in Waterdeep last year, there is room for a small callback without assuming "
       "how that story ended. An NPC, location or supernatural presence from it can return during the investigation: "
       "perhaps the " + A("midwinter-ghost", "Ghost of Midwinters Past") + ", hidden at the Shrine of Oghma in City Records.") +
     RA("\"Last year, you showed a man what became of a life without generosity.\"",
        "\"This year, something has learned to put a price upon it.\"", title="The Visitor") +
     P("Keep it to a few minutes. It makes the two one-shots feel like a growing Midwinter tradition. The ghost can grant "
       "one <em>Glimpse of Midwinters Past</em>: healing and one true fact about the foundation."))

page("finding-workshop", "Finding the Workshop",
     P("The party should reach the workshop whichever leads they followed. If they missed a critical clue, place a duplicate "
       "in the workshop itself.") +
     TABLE(["Route", "How", "Arrives At"], [
         ["<strong>The Service Elevator</strong>", "Concealed behind the Foundation Pavilion. Code <code>GOODWILL-999</code> "
                                                   "(Sprocket or Mizzle can give it), or " + chk("arcana", 17) +
          ", appropriate magic, or breaking the lock.", SC("intake", "Intake Department")],
         ["<strong>The Parcel Route</strong>", "Hide inside oversized enchanted presents and let the delivery system carry "
                                               "you to the workshop's intake.", SC("intake", "Intake chute")],
         ["<strong>The Sleigh Route</strong>", "Hijack a delivery sleigh and fly through the planar loading entrance. Use "
                                               "this for the optional chase.", SC("rooftops", "Rooftops") + ", then " +
          SC("assembly", "a maintenance balcony")]]))

page("sleigh-chase", "Optional: The Rooftop Sleigh Chase",
     P(SC("rooftops", "Open the Rooftops scene") + ". Run this between the investigation and the infiltration. The party "
       "hijacks a delivery sleigh and is pursued by " + A("hellforged-reindeer", "mechanical reindeer") + " and a " +
       A("yule-engine", "Yule Enforcement Engine") + ".") +
     BOX("Group Challenge: Five Successes Before Three Failures",
         "DC 16–18 depending on the action. Encourage Acrobatics for leaping between rooftops, Arcana for disrupting the "
         "sleigh's engines, Athletics for wrestling the controls, and ranged attacks or spells for neutralising pursuers. "
         "Roll complications on " + T("sleigh-complications", "Sleigh Chase Complications") + ".",
         "<strong>On a failure:</strong> [[/damage 3d10 bludgeoning]] or [[/damage 3d10 fire]] to an exposed character, "
         "lost equipment, or a damaged sleigh component, never instant elimination.",
         "<strong>On success:</strong> the party arrives through a maintenance balcony, bypassing the Intake security "
         "checkpoint."))

# ---------------------------------------------------------------------------
page("act3", "Act III — The Workshop of Good Intentions",
     BANNER("Act III · 65 minutes", "The Workshop of Good Intentions", "An extradimensional factory above Waterdeep") +
     P("This is where the adventure becomes full horror.") +
     RA("You emerge from the delivery passage into an enormous industrial complex.",
        "Hundreds of mechanical elves work at endless conveyor belts. Mountains of presents pass through enormous brass "
        "machines. Golden chains descend from the ceiling, and colossal clocks tick above every workstation.",
        "There is music. Cheerful, repetitive, maddening music.", "Every worker is smiling. Every single one.",
        "Above the factory floor, in beautiful golden lettering: A HAPPY WORKER IS A PRODUCTIVE WORKER.",
        "Then you notice something. One of the workers is crying. His smile doesn't change.",
        "A brass supervisor approaches him. \"EMPLOYEE 447. NEGATIVE EMOTIONAL OUTPUT DETECTED.\"",
        "It turns a small wheel on the worker's collar. He straightens, and the tears stop.",
        "\"Thank you,\" he whispers. \"I love my job.\"", "The music starts again.") +
     SECRET("Don't Start Combat Yet",
            "Let the characters observe what the foundation has become. The \"elves\" are a mix of actual devils, enchanted "
            "constructs and former mortal gift recipients, many of whom have long since completed the service their "
            "contracts allowed.",
            "Their smiles are held by enchanted " + I("collar-cheer", "Collars of Compulsory Cheer") + ". Removing or "
            "dispelling one lets a worker speak freely. Roll on " + T("workshop-horrors", "Workshop Horrors") + " for detail.") +
     H(3, "Workshop Layout") +
     P("Conceptual flow, not to scale. Players may move between the lower chambers freely. Run three areas in depth; the "
       "party should reach the hearing with at least two pieces of evidence or an equivalent way to challenge the scheme.") +
     TABLE(["Area", "Scene", "Focus"], [
         [uuid_journal("adventure", "area-a", "A: The Intake Department"), SC("intake", "Intake"), "Investigation and puzzle, 10–15 min"],
         [uuid_journal("adventure", "area-b", "B: The Assembly Line"), SC("assembly", "Assembly Line"), "Roleplay, dilemma, optional combat, 20–25 min"],
         [uuid_journal("adventure", "area-c", "C: Perpetual Midnight"), SC("midnight", "Perpetual Midnight"), "Environmental puzzle, 10–15 min"],
         [uuid_journal("adventure", "area-d", "D: The Ledger of Abandoned Souls"), SC("ledger", "Ledger Vault"), "Optional, 10 min"]]))

page("area-a", "Area A: The Intake Department",
     P(SC("intake", "Open the Intake scene") + ". Hundreds of gift certificates float through a forest of mechanical arms. "
       "Every certificate moves through three stamping stations: <strong>ACCEPTED</strong>, <strong>DEFAULTED</strong>, "
       "<strong>REPOSSESSED</strong>.",
       "A display shows the process: a citizen's record first reads FULFILLED; then a supervisor's override changes it to "
       "DEFAULTED; then collection proceeds despite the original verified act.",
       "The party can examine the system and retrieve an authenticated, unaltered register. If they missed " +
       I("exhibit-a", "Exhibit A") + " in the city, they can obtain it here.") +
     BOX("The Restricted Door",
         "Characters can demonstrate that a specific record was improperly processed; override the machinery with two "
         "successful " + chk("arcana investigation", 16) + " checks; or destroy the " + A("intake-lock", "locking mechanism") +
         " (AC 17, 30 HP).",
         "A failed attempt sounds an alarm, alerting the next chamber. It doesn't destroy the evidence or close the route.") +
     SECRET("Horror Detail",
            "The registry includes an entry titled <strong>UNASSIGNED MATERNAL AFFECTION</strong>, valued at 14,000 soul-coins. "
            "Someone has found a way to treat a person's capacity to love as a recoverable asset."))

page("area-b", "Area B: The Assembly Line of Eternal Gratitude",
     IMG(portrait("tilda-marr"), "rc-portrait rc-right") +
     P(SC("assembly", "Open the Assembly Line scene") + ". The line manufactures toys, clothing, enchanted food and magical "
       "gifts, each made with resources confiscated from workers. A toy that makes someone laugh might contain the memory of "
       "a loved one's voice (" + I("laughing-toy", "example") + "); a music box might be powered by a debtor's final happy "
       "thought (" + I("memory-music-box", "example") + "). Roll on " + T("confiscated-joys", "Confiscated Joys") + ".",
       "The party meets " + A("tilda-marr", "Tilda Marr") + ", an elven artisan. She accepted a gift to feed her neighbours, "
       "genuinely failed to complete her kindness in time, and owed a single night of service. That was ninety-three years "
       "ago by her own experience. It is still Midwinter night in the workshop.") +
     RA("\"I thought it was a fair exchange.\"", "\"One night. He said one night.\"", "\"Sometimes I dream of the sun.\"",
        "\"Then the bell rings, and I remember I'm not allowed to leave until morning.\"",
        "\"Please. Do you know if the sun is still there?\"", title="Tilda Marr") +
     P("Tilda explains that the factory has a perpetual-midnight mechanism and never registers a sunrise. She can give "
       "evidence of the altered working conditions, knows how to reach the clock mechanism, and knows that <strong>no one on "
       "the line signed a separate soul-transfer agreement</strong>: " + I("exhibit-d", "Exhibit D") + " (" +
       HO("exhibit-d", "handout") + ")."))

page("area-b-dilemma", "The Dilemma: Save the Workers or Secure the Records?",
     P("A " + A("brass-supervisor", "Brass Supervisor") + " arrives to destroy the intake records and move twenty prisoners "
       "to the next processing stage. Present two simultaneous urgent objectives: <strong>halt the conveyor</strong> and "
       "<strong>copy the evidence</strong>. Both can be done, but they need coordination.") +
     BOX("Three-Round Encounter",
         "Each character can attack the enforcement units, rescue prisoners, copy records or sabotage the line.",
         "The conveyor advances at initiative count 20. Two actions spent on the machinery (or a creative equivalent) "
         "disable it. Emergency stop levers are marked STOP on the map.",
         "Copying the records takes an action and a " + chk("investigation arcana", 16) + " check; a suitable spell can also "
         "secure them.") +
     P("Opponents: two " + A("jingle-bailiff", "Jingle Bailiffs") + ", plus two " + A("toy-soldier", "Toy Soldiers") +
       " (hidden) for a larger party. If the earlier fight ran long, use only the supervisor, who can be persuaded, tricked "
       "or disabled (its <em>Quota Logic</em> trait).") +
     SECRET("Consequences, Not Dead Ends",
            "If the players can't do both, they choose. The missed objective has consequences but never ends the adventure. "
            "Freed, Tilda and the prisoners help with the final escape."))

page("area-c", "Area C: The Department of Perpetual Midnight",
     P(SC("midnight", "Open the Perpetual Midnight scene") + ". An enormous clock dominates the room, its hands frozen at "
       "11:59 p.m. Above it hangs a miniature artificial sun trapped inside a glass sphere. Every time the sun tries to rise, "
       "mechanical claws drag it back below the horizon.") +
     RA("SERVICE CONCLUDES AT DAWN. DAWN IS CURRENTLY UNAVAILABLE.", title="The Inscription") +
     P("The players can establish that the clock artificially overrides Waterdeep's real sunrise. This is crucial: "
       "<strong>Clause III measures service by Waterdeep's sunrise, not the workshop's.</strong>") +
     TABLE(["Approach", "Resolution"], [
         ["Smash the " + A("midnight-engine", "clock mechanism"), "AC 17, 45 HP"],
         ["Reverse the gears", chk("arcana", 17) + " or tinker's tools"],
         ["Break the trapped sunlight free", "Appropriate magic (e.g. " + uuid_spell("midwinter-dawn", "midwinter dawn") + ") or " + chk("athletics", 18)],
         ["Use the maintenance manual", "Automatic success with Mizzle's schematic"],
         ["Copy the calibration settings", "Gain Exhibit C without disabling the engine"]]) +
     P("Disabling the mechanism releases a shaft of actual sunlight into the chamber. Workers begin remembering what morning "
       "feels like. It also suspends the endless-service process. If the players already hold Exhibit C, use this room for "
       "a dramatic sabotage scene instead of more investigation."))

page("area-d", "Area D: The Ledger of Abandoned Souls",
     P(SC("ledger", "Open the Ledger scene") + ". The darkest part of the workshop: a vast library of jars, filing cabinets "
       "and scrolls recording the ownership status of thousands of souls. The ledgers list living people as abandoned "
       "property because their notices were supposedly delivered to Nessus and went unanswered.",
       "The system has invented a category: <strong>unclaimed personal essence</strong>. Asmodeus's representatives are "
       "trying to establish that a soul can be seized without an explicit soul bargain, simply by collecting a supposedly "
       "unpaid service debt. Nothing in the gift contract authorises this.",
       "The party can obtain " + I("exhibit-d", "Exhibit D") + " here if Tilda didn't provide it.") +
     SECRET("A Genuine Soul Bargain",
            "In the vault is a real contract: someone voluntarily signed away their soul in exchange for a miracle (" +
            I("valid-soul-bargain", "item") + "). It is valid under infernal law. Use it to show the legal difference "
            "between a true soul bargain and the foundation's attempted theft.") +
     P("The characters can release souls held by the local sorting mechanism, but freeing everyone requires stopping the "
       "master transfer in the final chamber. Roll on " + T("ledger-categories", "Ledger Categories") + " for entries."))

page("reveal", "The Reveal: An Infernal Business Experiment",
     P("Any investigation of the private executive records turns up a memorandum from Asmodeus's court: " +
       HO("memo", "the Project Yuletide memorandum") + " (" + I("nessus-memo", "item") + ").") +
     SECRET("Why It Matters",
            "Asmodeus needs the ruling to be <strong>legally defensible</strong>. Simply abducting citizens won't create a "
            "precedent that can be replicated elsewhere.",
            "Nicholas has falsified records because he is trying to deliver the enormous soul harvest his master expects, "
            "and he knows a legitimate appeal could ruin the entire project.",
            "For the first time the players understand how frightened he may be of his own employer."))

# ---------------------------------------------------------------------------
page("act4", "Act IV — The Final Arbitration",
     BANNER("Act IV · 80 minutes", "The Final Arbitration", "The High Court of Seasonal Obligations · " + SC("court", "Open the scene")) +
     P("The centrepiece of the adventure. The players aren't simply fighting a monster: they're fighting an avatar of "
       "Asmodeus who has weaponised legal procedure, while a giant clock counts down the transfer of thousands of souls.") +
     H(3, "The Chamber (80 × 60 ft)") +
     UL("A raised northern dais holding the Red Clause's throne.",
        "An ornate witness lectern on the west side, attended by the " + A("brass-arbiter", "Brass Arbiter") + ".",
        "Three floating Infernal Writs in golden frames: " + A("writ-1", "Writ I") + " (northwest), " + A("writ-2", "Writ II") +
        " (northeast), " + A("writ-3", "Writ III") + " (south).",
        "An enormous bell mechanism along the east wall: the Midnight Docket.",
        "A central pit holding the " + A("master-ledger", "master ledger") + ", an immense book chained above a furnace.",
        "Catwalks and conveyor belts crossing the floor for movement, cover and environmental sabotage.") +
     P("The machinery runs continuously, even if the Red Clause is distracted or incapacitated.") +
     RA("A great iron door swings open. Beyond it stands a courtroom of impossible proportions.",
        "Thousands of parchment contracts hang suspended in the air, connected by golden threads to an enormous, beating "
        "furnace. High above, a clock with nine hands ticks towards midnight.",
        "At the far end of the chamber sits Nicholas Red Clause. He is no longer laughing.",
        "His spectacles rest neatly on the arm of his throne. His enormous sack hangs behind him, and from within it come "
        "the faint, overlapping voices of thousands of people.",
        "He studies you for several seconds. \"Well.\" He rises, slowly.",
        "\"I had hoped you would accept the terms of the festival. But here you are. Interfering with the lawful operations "
        "of a duly registered infernal enterprise.\"",
        "He straightens his crimson coat. \"I suppose you would like to speak to the manager.\"",
        "His smile becomes very, very wide. \"Unfortunately, I am the manager. And my manager...\"",
        "He points downwards. \"...is unavailable for comment.\"") +
     H(3, "The Final Offer") +
     P("Before initiative, the Red Clause offers to release every prisoner and close the current collection operation in "
       "exchange for <strong>one adventurer voluntarily signing over their soul to Asmodeus</strong>. This is a genuine, "
       "separate infernal bargain, not another falsified certificate. He cannot force anyone to accept it and explains its "
       "terms if asked: the character's soul becomes Asmodeus's property, with consequences for their afterlife and "
       "resurrection. One freely given heroic soul, won in public arbitration, could be worth more than thousands of "
       "disputed contracts.") +
     RA("\"How disappointing.\"", "\"You seek to save thousands of souls, yet none of you will surrender one.\"",
        "\"Such an extraordinary example of collective self-interest.\"", "\"The Naughty List grows longer by the moment.\"",
        title="If They Refuse") +
     P("If the players demand arbitration, he must permit it. The Brass Arbiter announces: <em>\"PETITION ACCEPTED. ALL "
       "PARTIES SHALL REMAIN PRESENT UNTIL FINAL JUDGMENT.\"</em> At that moment the Red Clause summons his bailiffs and "
       "tries to disrupt the proceedings. <strong>Roll initiative.</strong> Open the " + M("bells", "Midnight Docket") +
       " tracker at Bell III."))

page("legal-warfare", "The Legal Warfare System",
     P("A custom encounter mechanic using ordinary D&amp;D actions. It works with 2014 or 2024 play.") +
     TABLE(["Writ", "Legal Counter", "While It Stands", "When Broken"], [
         [A("writ-1", "Writ I — The Presumption of Default") + "<br><em>Kindness falsely marked as unfulfilled.</em>",
          I("exhibit-a", "Exhibit A"), "Red Clause can use Default Notice; Jingle Bailiffs remain under central command.",
          "Bailiffs are stunned until the end of their next turn; Red Clause loses Default Notice."],
         [A("writ-2", "Writ II — The Perpetuity of Service") + "<br><em>One night's service extended forever.</em>",
          I("exhibit-c", "Exhibit C"), "Red Clause regains 15 HP at the start of his turn.",
          "Regeneration ends; the next advancing bell is delayed by one round."],
         [A("writ-3", "Writ III — The Doctrine of Abandoned Souls") + "<br><em>Undelivered notices let souls be taken as "
                                                                       "unclaimed property.</em>",
          I("exhibit-b", "Exhibit B") + " or " + I("exhibit-d", "Exhibit D"), "Red Clause has two uses of Legendary Resistance.",
          "He loses any unused Legendary Resistance; the Arbiter warns the soul transfer lacks legal title."]]) +
     H(3, "How to Challenge a Writ") +
     P("A character at the witness lectern can use an action to present a relevant exhibit (use the " +
       M("exhibit", "Present an Exhibit") + " macro).") +
     UL("<strong>Clear, authenticated evidence matching a Writ succeeds automatically.</strong> Don't make the players gamble "
        "away their evidence on one Persuasion roll.",
        "With incomplete evidence, allow a " + chk("investigation arcana religion insight persuasion", 18) +
        " check backed by an actual argument. Success suspends that Writ for one round. Two separate successful provisional "
        "challenges invalidate it permanently.",
        "<strong>Only one petition can receive a full ruling per round.</strong>") +
     H(3, "Or Just Smash It") +
     P("The Writs physically exist as hovering constructs (AC 17, 35 HP, immune to poison and psychic damage) and can be "
       "attacked normally. Reducing one to 0 HP destroys it and suppresses its power (use the " + M("writ", "Break a Writ") +
       " macro). The Arbiter records the destruction, but destroying a Writ doesn't establish the same binding precedent as "
       "winning the hearing.") +
     SECRET("Victory Conditions",
            "<strong>All three Writs invalidated through evidence:</strong> the Arbiter declares the entire collection "
            "programme unlawful. The Red Clause's authority is revoked, the prisoners are released, and his avatar is "
            "forcibly recalled to Nessus. A complete victory without reducing his HP to zero.",
            "<strong>All three Writs physically destroyed:</strong> the machinery stops, but the infernal legal precedent "
            "remains unresolved.",
            "A mix of legal objections and physical sabotage works equally well for saving the prisoners."))

page("nine-bells", "The Nine Bells (The Midnight Docket)",
     P("Put a visible nine-space countdown in front of your players. The " + M("bells", "Midnight Docket") + " macro opens a "
       "shared tracker that every player can see; only the GM can change it.") +
     UL("The first three bells have already sounded during the collections and the journey into the workshop. At the start "
        "of the final encounter the docket stands at <strong>Bell III</strong>.",
        "At initiative count 20 each round, advance one bell, starting with Bell IV. The party ordinarily has six rounds "
        "before Bell IX.",
        "Breaking Writ II delays one bell. A particularly clever action directly disrupting the clock may also delay a bell, "
        "to a maximum of two additional rounds (the tracker's <em>Stay</em> button counts these). " +
        uuid_spell("stay-of-execution", "Stay of Execution") + " counts as a clever action.") +
     SECRET("Bell IX",
            "If Bell IX is reached while the collection machinery remains active, the soul transfer begins. At each "
            "subsequent initiative count 20, about one-third of the remaining captive souls are transferred to Nessus.",
            "Stopping the process after it begins still saves those not yet transferred, so the characters always have a "
            "meaningful chance to avert complete disaster."))

page("red-clause-tactics", "The Red Clause: Statistics & Tactics",
     IMG(portrait("red-clause"), "rc-portrait rc-right") +
     P(A("red-clause", "Nicholas Red Clause") + " — Huge fiend (devil), lawful evil. AC 19, HP 250, speed 40 ft. Encounter-"
       "specific homebrew statistics; CR 15 is listed for the XP tracker only.") +
     UL("<strong>Multiattack:</strong> two Clause Chain attacks (+11, reach 15 ft., 2d8 + 6 slashing + 1d8 psychic).",
        "<strong>Breach Notice (Recharge 5–6):</strong> 30-ft cone, " + sv("wisdom", 18) + ", 5d8 psychic and no reactions.",
        "<strong>Sack of Repossession (Recharge 6):</strong> " + sv("strength", 18) + " or swallowed; 3d6 cold per turn; "
        "escape DC 17 or break the " + A("sack-seam", "seam") + " (AC 15, 25 HP).",
        "<strong>Default Notice (bonus action, Writ I):</strong> " + sv("wisdom", 18) + " or crimson citation.",
        "<strong>Legendary Actions (2):</strong> Staple of Judgment, Relocate Assets, Order Enforcement.",
        "<strong>Lair actions (initiative 20, after the bell):</strong> rotate Furnace Discharge, Gift-Wrapped Restraints and "
        "Blizzard of Fine Print. Roll " + T("lair-actions", "Lair Actions") + " if you like.") +
     H(3, "Phase II — The Smile Disappears") +
     P("Trigger once, when two Writs are destroyed or he falls below half HP, whichever comes first (the " +
       M("phase2", "The Smile Disappears") + " macro posts the narration and prompts the saves).") +
     RA("The Red Clause stops moving. His smile remains for a moment, as though painted onto his face. Then it slowly folds "
        "inwards.", "You hear metal tearing.",
        "His crimson coat splits open, revealing an enormous furnace of black iron and white-hot chains. Inside it, thousands "
        "of names burn across the walls.",
        "The beard of silver bells unravels into barbed lengths of chain. His spectacles shatter. And when he speaks again, "
        "the warmth has vanished from his voice.",
        "\"I have been exceedingly patient.\"", "He removes his white gloves, revealing hands of polished bone and brass.",
        "\"You have exhausted the limits of my goodwill.\"", "His eyes flare. \"Your account is now payable in full.\"") +
     P("Creatures within 15 feet make a " + sv("wisdom", 18) + " saving throw, taking [[/damage 4d8 psychic]] on a failure, or "
       "half on a success. Afterwards his manner is cold, legalistic and absolutely serious. His statistics stay the same; "
       "<strong>don't add a second health bar.</strong>") +
     H(3, "Scaling the Fight") +
     TABLE(["Party", "Red Clause HP", "Bailiffs", "Legendary Actions"], [
         ["4 characters", "200", "1", "2"], ["5 characters", "250", "2", "2"], ["6 characters", "300", "2–3", "3"]]) +
     P("The " + M("setup", "Red Clause Manager") + " can apply these numbers to the boss for you. A highly optimised party "
       "may overwhelm the avatar fast. Let their strength matter, but keep the bell and the legal objectives demanding "
       "attention. The 2024 guidance gives a high-difficulty benchmark of 4,100 XP per 11th-level character, but the extra "
       "objectives here need live DM judgement more than XP arithmetic."))

page("kill-red-clause", "If the Players Kill the Red Clause",
     P("His avatar disintegrates into fragments of red paper, broken gears and burning ash. <strong>But the central ledger is "
       "still running.</strong> His " + I("infernal-signet", "Infernal Signet") + " remains behind, carrying the authority to "
       "terminate the transfer.",
       "Give the party two rounds to destroy the " + A("master-ledger", "master ledger") + " (AC 17, 40 HP), stamp an "
       "emergency cancellation with the signet, or secure a final ruling from the Brass Arbiter.",
       "A successful intervention stops the harvest and releases the captives. Characters who concentrate on direct combat "
       "can still earn a complete rescue without the legal challenge, though they may not establish a binding infernal "
       "precedent."))

page("legal-arguments", "The Legal Arguments That Should Work",
     P("Your quick reference when players start acting like infernal attorneys.") +
     TABLE(["Player's Argument", "Correct Consequence"], [
         ["\"Edda performed a genuine act of kindness.\"", "Writ I is invalid if authenticated records are presented."],
         ["\"The notices were delivered to Hell, not Waterdeep.\"", "The collection notice is invalid, supporting the challenge to Writ III."],
         ["\"One night ends at sunrise in Waterdeep.\"", "Writ II is invalid."],
         ["\"The contracts don't transfer ownership of souls.\"", "Writ III is invalid."],
         ["\"I'm filing an appeal on behalf of the victims.\"", "The Arbiter must hear a properly supported petition."],
         ["\"We never agreed to these terms.\"", "Characters who refused the gift can't be held under it."],
         ["\"We can simply kill you.\"", "The avatar can be destroyed, but the machinery must also be stopped."]]) +
     P("Use the wording the players actually received. If they find another genuine contradiction, let it matter even if it "
       "isn't on this list.") +
     SECRET("The Real Conflict",
            "This isn't about tricking players with hidden rules. It's about uncovering how a powerful institution has "
            "deliberately violated its own enforceable promises."))

page("dialogue", "The Red Clause's Dialogue Sheet",
     P("Designed to follow the tonal progression. Also available as the " + T("red-dialogue", "Red Clause's Dialogue") + " table.") +
     TABLE(["Situation", "Dialogue"], [
         ["A character refuses a gift", "\"Oh, a cautious one! How terribly unprofitable!\""],
         ["Someone asks whether he's a devil", "\"A devil? My dear, I'm an executive!\""],
         ["Someone questions the fine print", "\"We believe in transparency. That's why our terms are printed in such wonderfully translucent ink.\""],
         ["A player tries to bribe him", "\"Bribery? Please! We call those expedited relationship fees.\""],
         ["The players first find the workshop", "\"We prefer the term mandatory volunteer experience.\""],
         ["Someone mentions the trapped workers", "\"They were given a wonderful opportunity to contribute. Some have been contributing for generations.\""],
         ["The party invokes the original contract", "\"You'll find that generosity is a remarkably expensive principle.\""],
         ["A legal objection succeeds", "\"Objection acknowledged. How delightfully inconvenient.\""],
         ["Two Writs are destroyed", "\"Enough. The festivities are over.\""],
         ["A character offers their soul", "\"Now THAT is the spirit of giving.\""],
         ["The Brass Arbiter rules against him", "\"No. No, that cannot be correct. Read it again.\""],
         ["He is defeated", "\"You have no idea what my employer is going to do to me.\""]]) +
     SECRET("The Most Important Roleplaying Beat",
            "Don't have Asmodeus appear in person or rescue the Red Clause. Asmodeus authorised an experiment; he didn't "
            "guarantee his subordinate's success. Once the avatar loses, the Lord of the Nine Hells may even accept the "
            "verdict with chilling composure. That makes the world feel bigger than the adventure."))

page("endings", "Endings & Epilogues",
     P("The result should reflect <em>how</em> the party won, not just whether the boss's HP reached zero.") +
     BOX("Ending A — The Unprecedented Verdict (complete legal victory)",
         "All three Writs are invalidated through arbitration. The Arbiter pronounces the experiment unlawful and terminates "
         "the Red Clause's licence. Every illegally held soul is released. The precedent fails, and Asmodeus's model can't be "
         "expanded on the strength of this case. Nicholas is dragged back to Nessus by his own chains.",
         "As he disappears, an elegant document appears before the party: " + HO("invitation", "the invitation") +
         ". The Arbiter leaves its " + I("arbiter-gavel", "gavel") + " on the lectern.") +
     BOX("Ending B — Hostile Takeover (victory by combat and sabotage)",
         "The avatar is destroyed, the ledger disabled and the captives escape. Waterdeep celebrates its heroes. But the legal "
         "question remains unresolved: no binding ruling was issued on the broader doctrine.",
         "Somewhere in Nessus, another infernal executive opens a new file: " + HO("revised", "Project Yuletide: Revised "
                                                                                              "Commercial Model") + ".") +
     BOX("Ending C — The Greatest Gift (a character accepts the sacrifice)",
         "One adventurer voluntarily signs a genuine soul bargain in return for the prisoners' freedom. The Red Clause honours "
         "it exactly. Thousands are saved. Their friend becomes the subject of a valid infernal contract, perhaps allowed to "
         "live out their mortal life first, depending on the terms they negotiated. A poignant standalone ending, or the "
         "beginning of a rescue campaign.") +
     BOX("Ending D — The Ninth Bell (partial failure or complete defeat)",
         "The party can't stop the transfer in time. Thousands of souls begin disappearing from the ledger. Waterdeep wakes to "
         "an eerie quiet, its streets full of unclaimed gifts. Survivors may still be saved, and a later adventure could "
         "pursue the transferred souls into the Nine Hells.") +
     H(3, "Final Read-Aloud for the Best Ending") +
     RA("For a long moment, the factory is silent. Then the great clock begins to turn.",
        "Slowly, impossibly, its hands advance past midnight. The suspended sun breaks free. Golden light floods the workshop.",
        "The workers look up. Some begin to cry. Others simply stare. The smiles finally disappear from their faces.",
        "Tilda Marr falls to her knees as the first light of dawn touches her skin.",
        "\"Oh,\" she whispers. \"I'd forgotten. I'd forgotten how beautiful it was.\"",
        "Across Waterdeep, bells ring. Not the cruel, mechanical chimes of the foundation. Real bells. Bells calling the city "
        "to morning.", "For the first time in a very long while, the people of the workshop are free.") +
     P("Then finish with one last absurd detail. A tiny imp approaches the heroes carrying a clipboard.") +
     RA("\"Erm. Excuse me. Terribly sorry.\"", "He clears his throat.",
        "\"Before you leave, would you mind completing our customer satisfaction survey?\"", title="Sprocket Jingles") +
     P("Hand over the " + HO("survey", "Customer Satisfaction Survey") + ". Rewards: " + I("dawnglass", "Tilda's Dawnglass") +
       ", " + I("sprocket-clipboard", "Sprocket's Clipboard of Citations") + ", " + I("bell-ninth-hour", "Bell of the Ninth "
                                                                                                         "Hour") + ", and "
       "anything else in the <em>Rewards &amp; Relics</em> folder that suits your table."))

page("contingencies", "Magical Solutions & Level 11 Contingencies",
     P("11th-level adventurers can bypass ordinary investigation and dungeon design. Let them.") +
     TABLE(["Ability or Strategy", "Suggested Ruling"], [
         ["<em>Detect magic</em>", "Reveals infernal enchantment on gifts and constructs, not the legal truth of every contract."],
         ["<em>Identify</em>", "Reveals an item's function and magical properties, not every secret in the records."],
         ["<em>Zone of truth</em>", "Exposes inconsistencies in testimony but doesn't automatically invalidate signed documents."],
         ["<em>Dispel magic</em>", "Suppresses collars or smaller enchantments; the night engine needs a high-level dispel or physical sabotage."],
         ["<em>Dimension door</em>", "Works inside the workshop and can bypass individual chambers."],
         ["<em>Banishment</em>", "Can temporarily remove the avatar; the independent contractual machinery keeps running."],
         ["<em>Legend lore</em> or divine investigation", "Can reveal the significance of the Brass Arbiter or a governing infernal principle."],
         ["<em>Speak with dead</em>", "May provide testimony, but can't retrieve a living person from the soul ledger."],
         ["Destroying all records", "Disrupts collection but risks losing proof for binding arbitration."],
         ["Teleporting prisoners away", "Saves individual captives but doesn't remove their names from the central ledger."]]) +
     P("Don't blanket-ban spells to protect the story. Reward clever use of powerful abilities; a group that spends its "
       "limited resources dismantling the operation should progress faster."))

page("checklist", "DM Preparation & Quick Reference",
     H(3, "Session Setup") +
     '<ul class="rc-check">' + "".join(f"<li>{x}</li>" for x in [
         "Run <strong>Set Up Everything</strong> from the " + M("setup", "Red Clause Manager") + " (Game Settings → Module "
                                                                                                "Settings).",
         "Prepare the " + HO("certificate", "Hearthlight contract") + " as a player handout.",
         "Check the Red Clause and supporting actors (installed into the <em>Night of the Red Clause</em> actor folders).",
         "Check the Market, Workshop and Court scenes (all built and staged).",
         "Writ tokens are on the Court scene.",
         "Evidence cards A–D are in the Evidence &amp; Documents item folder.",
         "Put the " + M("bells", "Midnight Docket") + " where everyone can see it.",
         "Decide whether to include the sleigh chase.",
         "Decide which NPC or location to bring back from last year's one-shot.",
         "Confirm the group's boundaries for horror and coercion."]) + "</ul>" +
     H(3, "Quick Reference") +
     TABLE(["Situation", "What to Remember"], [
         ["Players distrust everything immediately", "Good. Let their suspicion uncover real clues."],
         ["Nobody accepts a gift", "The City Watch still gives them standing to intervene."],
         ["They solve Edda's case instantly", "Reward it; the larger conspiracy remains."],
         ["They kill Sprocket", "Mizzle and the documents provide alternative routes."],
         ["They miss evidence", "Duplicate the essential information in the workshop."],
         ["They want to negotiate", "The Red Clause must honour legitimate arbitration."],
         ["They ignore legal arguments", "Combat and sabotage can still stop the harvest."],
         ["They split up in the factory", "Let separate groups pursue evidence and rescue at once."],
         ["The session is running long", "Skip Area D; go from the night engine to the court."],
         ["The boss is falling too easily", "Keep the independent soul-transfer clock active instead of adding a second health bar."]]))

page("creative-direction", "Final Creative Direction",
     P("Preserve three principles when running this.") +
     OL("<strong>The comedy must feel sincere.</strong> The players need to enjoy the absurd citations, ridiculous presents "
        "and homicidally cheerful mechanical Santa. Don't make every cheerful NPC immediately sinister.",
        "<strong>The contract must be fair to the players even though the villain isn't.</strong> Let them inspect terms, "
        "refuse gifts, satisfy obligations and present valid objections. The horror lands harder when they realise ordinary "
        "citizens were manipulated by a system pretending to follow rules.",
        "<strong>The final encounter must reward the whole party.</strong> A charismatic character can argue a case, a wizard "
        "can disrupt the machinery, a rogue can steal the signet, and a fighter can smash a Writ of Infernal Authority to "
        "pieces.") +
     P("For Forgotten Realms placement: Midwinter falls between Hammer 30 and Alturiak 1, and Waterdeep's Castle Ward holds "
       "the Market and the major civic landmarks. The Hearthlight Foundation, the workshop, the contracts and the Red Clause "
       "are original to this adventure.") +
     '<p class="rc-closing">The greatest gift the heroes gave Waterdeep wasn\'t money, magic, or even their swords.<br>'
     'It was proving that kindness cannot be owned.</p>')

# ---------------------------------------------------------------------------
# Pregenerated hero connections: overview page + in-scene callouts
from pregen_lore import LORE, CONNECTIONS


def HOOK(title, *paras):
    return BOX("Hero Hook · " + title, *paras)


_conn = (P("Each pregenerated hero has a personal reason to be in the Market tonight and a stake in someone the "
           "foundation has taken. Their full backstories are on their character sheets and in " +
           uuid_journal("pregens", None, "Pregenerated Heroes") + ". The callout boxes marked <strong>Hero Hook</strong> in "
           "each scene tell you when to cue them.") +
         TABLE(["Hero", "Connected To", "When It Pays Off", "Helps Break"], [list(r) for r in CONNECTIONS]) +
         SECRET("The Shape of It",
                "The hooks are built so that every hero walks into the High Court carrying something only they can offer: "
                "an eyewitness (Bramwell), an author (Hesper), a priest who knows the true dawn (Marigold), a founder who "
                "knows where the bell will break (Dorn), a thief within reach of the signet (Pip), and a singer who can wake "
                "the workers (Fennick).",
                "If players bring their own characters, borrow these hooks: give a PC a friend among the vanished, a hand "
                "in making the foundation's tools, or a debt to Edda Hearth.") +
         "".join(f"<h3>{n}</h3><p>{LORE[k]['tonight']}</p><p><em>At the table:</em> {LORE[k]['table']}</p>"
                 for k, n in [("marigold", "Sister Marigold Ashby"), ("hesper", "Hesper Vane"), ("bramwell", "Ser Bramwell Thistlegown"),
                              ("dorn", "Dorn Ironhollow"), ("pip", "Pip Nettlewick"), ("fennick", "Fennick Holloway")]))
_i = next(i for i, x in enumerate(pg) if x[0] == "structure")
pg.insert(_i + 1, ("hero-connections", "Hero Connections (Pregenerated Heroes)", _conn))

CALLOUTS = {
    "act1-bureau": HOOK("Fennick", "Sprocket has a thick file on Fennick Holloway: the foundation bought his carol last summer, "
                        "and Sprocket fined him this morning for singing it. Let Sprocket greet him by name, nervously."),
    "act1-gifts": HOOK("Hesper", "The moment Hesper Vane reads Form H-25 she recognises her own drafting, clause for clause. "
                       "Tell her player that every protection in it is genuine, and that she wrote the Arbiter clause herself."),
    "act1-arrival": HOOK("Hesper &amp; Dorn", "The Red Clause singles Hesper out: <em>“Miss Vane! Still drafting for paupers?”</em> "
                         "When his sleigh leaves and the first bell tolls, Dorn Ironhollow knows the bronze: he cast it."),
    "act2": HOOK("Bramwell &amp; Pip", "Bramwell watched Edda give Agna the bread this morning: his sworn testimony is a properly "
                 "filed appeal, and the bailiffs must suspend collection. Pip has been watching Edda all day; give his player "
                 "the first chance to act when the ribbons wrap her wrists."),
    "act2-marta": HOOK("Bramwell", "Marta Quill patrolled with Corin Vell. She knows Bramwell and deputises the party on his word."),
    "lead-b": HOOK("Marigold &amp; Dorn", "The residence rolls show Tilda Marr (Cloak Alley) and Tam Gorm (Sails Street) "
                   "re-addressed to Nessus. Marigold and Dorn each recognise a name."),
    "lead-c": HOOK("Pip", "The Depot is Pip's own fencing drop, and Mizzle owes him. With Pip present, Mizzle talks without any "
                   "check and hands over the Service Access Token and the Maintenance Schematic."),
    "area-b": HOOK("Marigold, Dorn &amp; Fennick", "Tilda knows Marigold at once and asks her about the sun. Tam Gorm is on the "
                   "line too, smiling, and calls Dorn “master”. The factory music is Fennick's carol, slowed and looped: if he "
                   "sings the true words, collared workers within 60 feet can speak freely for a minute."),
    "area-c": HOOK("Marigold", "Marigold can feel the real sunrise beyond the false clock: advantage on checks to free the "
                   "trapped sun, and her sworn word about the true dawn can stand in for Exhibit C."),
    "act4": HOOK("Hesper", "The Final Offer is made to Hesper by name: her disputed account settled and every prisoner freed for "
                 "her soul. It is a genuine bargain. Let her player decide."),
    "legal-warfare": HOOK("Hesper &amp; Bramwell", "Once per hearing, Hesper's argument as the template's author turns a "
                          "provisional challenge into a full ruling. Bramwell's and Agna's eyewitness testimony counts as "
                          "authenticated evidence against Writ I."),
    "nine-bells": HOOK("Dorn", "Dorn can strike the ninth bell at the flaw he hid: one strike delays the next toll, a second "
                       "cracks it so Bell IX cannot sound for one more round. This may exceed the two-stay limit."),
    "kill-red-clause": HOOK("Pip", "If the Red Clause falls, Pip can snatch the Infernal Signet as a bonus action from within 5 feet."),
}
pg[:] = [(k, t, h + CALLOUTS[k]) if k in CALLOUTS else (k, t, h) for k, t, h in pg]

# ---------------------------------------------------------------------------------------------- the jingle
import carol as CAROL


def CUE(stanza_key, *paras):
    st = CAROL.by_key(stanza_key)
    return (f'<div class="rc-box rc-carol-box"><h4>♪ The Jingle · {st["title"]}</h4>' + "".join(f"<p>{p}</p>" for p in paras)
            + CAROL.stanza_html(st) + "</div>")


_carol_page = (
    BANNER("The Foundation's Midwinter Jingle", "The Red Clause Is Coming to Town",
           "A cheerful carol that curdles, one verse per act") +
    P("The Hearthlight Foundation has a jingle. The " + A("carolling-snowman", "Carolling Snowmen") + " sing it all day, the clerks "
      "hum it while they fine people, and by midnight the whole city has it stuck in its head. It is the single best tool you "
      "have for showing the players that the night is getting worse: <strong>every act, the song gets one verse darker.</strong>",
      "Sing it to the tune of the best-known Christmas song about a jolly man checking a list. Badly is fine. Badly is better.") +
    SECRET("Whose Song Is It?",
           "In the world, the melody is <em>The Lantern-Light Carol</em>, the song Fennick Holloway sold to a polite clerk in a green "
           "hat last summer. The foundation kept the tune and wrote new words. Anyone who knew the old carol (Fennick, Edda, half "
           "the Market) hears the theft at once. In Act III, the Assembly Line plays the same tune slowed into a dirge.") +
    H(2, "When Each Verse Plays") +
    TABLE(["Moment", "Verse", "What it shows"], [
        ["Act I, the Market", "Verse 1, Chorus, Verse 2", "Cheer. One line in the chorus is wrong, and a clerk winces every time."],
        ["Act II, Nightfall (Bell IV)", "Verse 3, second Chorus", "The snowmen slow down. Gift-takers hum it without meaning to."],
        ["Act III, Assembly Line", "Verse 4", "The collared workers' work song, sung through smiles."],
        ["Act III, Area D", "Bridge", "The jars in the Ledger whisper it, each in a different voice."],
        ["Act IV, the High Court", "Verse 5, Final Chorus", "The court's opening hymn; the Red Clause conducts."],
        ["Phase II", "Outro", "Whispered as the smile disappears, then one booming laugh."]]) +
    P("The " + M("carol", "Sing the Next Verse") + " macro posts any verse to chat, styled for the act it belongs to, and the "
      "players get the Act I verses as a handout: the " + HO("songbook", "Hearthlight Songbook") + ". The complete lyrics are "
      "the " + HO("carol-full", "The Red Clause Is Coming to Town") + " handout, best saved for the epilogue.") +
    H(2, "The Jingle at the Table") +
    BOX("The Wrong Line (Act I)",
        "The chorus admits the foundation is collecting souls. A character who listens properly notices it with a DC 13 Wisdom "
        "(Insight) check, or automatically if they read the Songbook. Ask a clerk about it and the clerk insists the lyric is "
        "<em>\u201c…which <strong>shoes</strong> he gets to make\u201d</em>, and fines whoever asked 10 gp for unauthorised humbuggery.") +
    BOX("The Humming (Act II)",
        "After nightfall, every creature that accepted one of the Nine Gifts hums the second chorus under its breath without "
        "noticing. It does no harm. It is a reliable way to tell who has signed, and it is horrible to watch a child do it.") +
    BOX("The Jingle as Evidence (Act IV)",
        "Form H-25 says it conveys <em>no interest whatsoever</em> in the soul. The foundation's own jingle says it knows "
        "<em>which souls he gets to take</em>. A hero who presents the Songbook, a recording (the Bell of Perfect Timing can hold "
        "one), or a live performance argues intent: treat it as a provisional exhibit against <strong>Writ III, the Doctrine of "
        "Abandoned Souls</strong>, made with advantage on the DC 18 check. It works once per hearing. Fennick, as the composer, "
        "can testify to the melody's theft at the same time.") +
    BOX("Countersong (optional, Act IV)",
        "When Verse 5 begins, one hero can lead the Market in the real words of the Lantern-Light Carol with a DC 16 Charisma "
        "(Performance) check; Fennick has advantage. On a success, the court falters: each hero has advantage on its first "
        "saving throw against the Red Clause's Breach Notice. On a failure, the snowmen sing louder.") +
    H(2, "The Complete Lyrics") + P("Lyrics by Asmo. Each verse below shows when it plays.") + CAROL.song_html(cue=True))
_ci = next(i for i, (k, _, _) in enumerate(pg) if k == "hero-connections")
pg.insert(_ci + 1, ("carol", "The Red Clause Is Coming to Town", _carol_page))

_CUES = {
    "act1-opening": CUE("v1", "The snowmen are singing this as the players arrive. Sing it; the clerks join in on the last line."),
    "act1-gifts": CUE("v2", "The choir switches to the second verse as the gifts are handed out. Hand over the "
                      + HO("songbook", "Hearthlight Songbook") + " with the certificate."),
    "act2": CUE("v3", "At nightfall the snowmen's carrot noses droop and the tempo drops. Then everyone with a gift starts humming."),
    "area-b": CUE("v4", "The workers sing this as they work, smiling. Fennick's true words (see his sheet) stop it."),
    "area-d": CUE("bridge", "Every jar on the shelves whispers one line of it, out of time with the others."),
    "act4": CUE("v5", "The court's opening hymn. Offer the Countersong (see " +
                uuid_journal("adventure", "carol", "The Red Clause Is Coming to Town") + ")."),
    "red-clause-tactics": CUE("outro", "Use this when the smile disappears (Phase II): whisper it, slowly, then laugh as loudly "
                              "as you can manage. The players will not forget it."),
}
pg[:] = [(k, t, h + _CUES[k]) if k in _CUES else (k, t, h) for k, t, h in pg]

journal("adventure", "The Night of the Red Clause — Adventure Book", "Adventure", pg, sort=100000)
