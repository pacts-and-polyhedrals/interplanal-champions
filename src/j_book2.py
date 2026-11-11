"""Book II — Claimants of the First Crown (player's guide): text from the manuscript; spells, relics and subclasses
rendered from the compendium documents so the book and the sheets never disagree."""
import os
from jhelp import *
import textbook as TB
import spells as SP
import items as IT
import playeroptions as PO
import pregens as PG
from blocks import spell_type, spell_lines

HERE = os.path.dirname(os.path.abspath(__file__))
L = TB.load(os.path.join(HERE, "data", "book2.txt"))
HO = lambda k, n: uuid_journal("handouts", k, n)


def chunk(a, b=None, **kw):
    return TB.render(TB.slice_lines(L, a, b), skip_first=kw.pop("skip_first", True), **kw)


def _feat_list(feats):
    return "".join(f'<div class="rc-feature"><h4>@UUID[Compendium.{MOD}.options.Item.{f["_id"]}]{{{f["name"]}}} '
                   f'<span class="rc-lvl">({f["system"]["requirements"]})</span></h4>{f["system"]["description"]["value"]}</div>'
                   for f in feats)


def sub_page(doc, kind, feats, icon_):
    return (f'<div class="rc-subclass"><div class="rc-npc">{IMG(icon(icon_), "rc-thumb")}<div><h3>@UUID[Compendium.{MOD}.options.Item.'
            f'{doc["_id"]}]{{{doc["name"]}}}</h3><p class="rc-sptype"><em>{kind}</em></p></div></div>'
            f'{doc["system"]["description"]["value"]}' + _feat_list(feats) + "</div>")


def spell_block(s):
    lines = "<br>".join(f"<strong>{k}:</strong> {v}" for k, v in spell_lines(s))
    return (f'<div class="rc-spell"><h3>@UUID[Compendium.{MOD}.spells.Item.{s["_id"]}]{{{s["name"]}}}</h3>'
            f'<p class="rc-sptype"><em>{spell_type(s)}</em></p><p>{lines}</p>{s["system"]["description"]["value"]}</div>')


def item_block(i):
    y = i["system"]
    rar = {"veryRare": "very rare"}.get(y.get("rarity", ""), y.get("rarity", ""))
    att = f" ({'requires attunement' if y['attunement'] == 'required' else 'requires attunement ' + y['attunement'].replace('required ', '')})" if y.get("attunement") else ""
    kind = {"weapon": "Weapon", "equipment": "Wondrous item" if i["name"] != "Writshield of Personal Sovereignty" else "Armour (shield)",
            "consumable": "Wondrous item"}.get(i["type"], "Item")
    if i["name"] == "Pyric Covenant Ring":
        kind = "Ring"
    return (f'<div class="rc-spell"><h3>@UUID[Compendium.{MOD}.items.Item.{i["_id"]}]{{{i["name"]}}}</h3>'
            f'<p class="rc-sptype"><em>{kind}, {rar}{att}</em></p>{y["description"]["value"]}</div>')


NEW = sorted([s for s in SP.SPELLS if s["flags"][MOD]["group"] == "Interplanal Champions"], key=lambda s: (s["system"]["level"], s["name"]))
ORD = {0: "Cantrip", 1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th", 8: "8th"}
spell_list = TABLE(["Level", "Spells"], [[ORD[l], ", ".join(uuid_spell(s["flags"][MOD].get("key", "") or "", "") and
                                                         f"@UUID[Compendium.{MOD}.spells.Item.{s['_id']}]{{{s['name']}}}"
                                                         for s in NEW if s["system"]["level"] == l)] for l in range(9)])

RELICS = IT.ITEMS["Relics of the Championship"]
relic_table = TABLE(["Item", "Rarity", "Attunement", "Recommended acquisition"], [
    [f"@UUID[Compendium.{MOD}.items.Item.{i['_id']}]{{{i['name']}}}", {"veryRare": "Very rare"}.get(i["system"]["rarity"], i["system"]["rarity"].capitalize()),
     "Yes" if i["system"]["attunement"] else "No",
     __import__("re").search(r"Recommended acquisition: ([^<]*)\.</em>", i["system"]["description"]["value"]).group(1)] for i in RELICS])


from pregen_lore import LORE as _LORE, PROLOGUE as _PROLOGUE


def _public_bio(k):
    L = _LORE[k]
    return (f"<p>{L['role']}</p>" + "".join(f"<p>{b}</p>" for b in L["backstory"])
            + BOX("Why You Entered", L["tonight"]) + f"<p><strong>Your Claim.</strong> {L['knows']}</p>"
            + "<h4>The Other Claimants</h4><ul>" + "".join(f"<li><strong>{n}.</strong> {t}</li>" for n, t in L["others"]) + "</ul>"
            + "<p><em>Your DM has one more private note for you: the pressure that will test your claim.</em></p>")


def claimant(p, a):
    y = a["system"]
    return (f'<div class="rc-pregen"><div class="rc-npc">{IMG(portrait("pc-" + p["key"]), "rc-portrait")}<div>'
            f'<h3>@UUID[Compendium.{MOD}.pregens.Actor.{a["_id"]}]{{{p["name"]}}}</h3>'
            f'<p class="rc-sptype"><em>{p["title"]} · {p["race"]} {p["cls"]} 12 ({p["sub"]}) · {p["align"]}</em></p>'
            f'<p><strong>Hit Points</strong> {a["flags"][MOD]["expectedHp"]} · <strong>Background</strong> {p.get("bg_text", "")}</p></div></div>'
            + _public_bio(p["key"])
            + (f'<p class="rc-fine"><em>{p["subst"]}</em></p>' if p.get("subst") else "") + "</div>")


B2 = [
    ("cover", "Claimants of the First Crown",
     BANNER("Book II · Player's Guide &amp; Character Options", "Claimants of the First Crown",
            "Interplanal Champions · A sequel to The Night of the Red Clause") +
     '<p class="rc-tagline">EVERY CROWN IS A CONTRACT. READ YOURS.</p>' +
     P("Three Asmodean subclasses. Seventeen contractual spells. Fourteen relics. Eight handout contracts. Six level-12 claimants "
       "ready for the First Crown. Designed to accompany the Asmodeun Scriptorium.") +
     chunk("What kind of campaign is this?", "1. THE CHAMPIONSHIP CHARTER", skip_first=False)),
    ("charter", "1. The Championship Charter",
     H(2, "1. The Championship Charter") + BOX("Handout", "Give every player the " + HO("charter", "Nine Articles of Infernal Succession")
                                               + " before anyone signs anything.", cls="rc-box rc-tools") +
     chunk("1. THE CHAMPIONSHIP CHARTER", "2. NEW SUBCLASS")),
    ("ruby-court", "2. Warlock: The Ruby Court", H(2, "2. Warlock: The Ruby Court") +
     sub_page(PO.IC.RUBY, "Otherworldly Patron (Warlock)", PO.IC.RUBY_FEATURES, "ic-ruby")),
    ("blood-price", "3. Barbarian: Path of the Blood-Price", H(2, "3. Barbarian: Path of the Blood-Price") +
     sub_page(PO.IC.BLOOD, "Primal Path (Barbarian)", PO.IC.BLOOD_FEATURES, "ic-bloodprice")),
    ("ashen", "4. Druid: Circle of Ashen Covenants", H(2, "4. Druid: Circle of Ashen Covenants") +
     sub_page(PO.IC.ASHEN, "Druid Circle", PO.IC.ASH_FEATURES, "ic-ashen")),
    ("soulforged", "4A. Artificer: The Soulforged", H(2, "4A. Artificer: The Soulforged") +
     BOX("In Foundry", "Subclass, features and the twelve Construct Imprints are in <em>Player Options</em>; the two servitor "
         "frames are actors in <em>Soulforged Servitors</em>; the soul tables are in <em>The Soulforged</em>; Forms SF-01 and "
         "SF-12 are handouts. The <em>Generate a Soul</em> macro rolls a complete soul.", cls="rc-box rc-tools") +
     __import__("soulforged").player_page()),
    ("spells", "5. Contractual Spellcasting", H(2, "5. Contractual Spellcasting") +
     P("These are 17 original new spells for this campaign, designed to extend rather than duplicate the Asmodeun Scriptorium's "
       "existing 26-spell ladder in <em>The Night of the Red Clause</em>. Spells do not forge genuine consent: a magical combat "
       "restraint is not a soul bargain. Every spell is in the <em>Spells</em> compendium.") + spell_list +
     "".join(spell_block(s) for s in NEW) + chunk("Spell use and stacking", "6. RELICS", skip_first=False)),
    ("relics", "6. Relics, Rewards and Championship Equipment", H(2, "6. Relics, Rewards and Championship Equipment") +
     P("The following fourteen items are unique to this campaign. Normal attunement limits apply. The items are rewards for an "
       "entire party, not fourteen things one claimant is expected to acquire. A particularly important tool can also be "
       "obtained by contract, loan, purchase from a faction, or restitution.") + relic_table +
     "".join(item_block(i) for i in RELICS) + chunk("Equipment balance and attunement", "7. EIGHT CONTRACTS", skip_first=False)),
    ("contracts", "7. Eight Contracts for Players", H(2, "7. Eight Contracts for Players") +
     P("All eight forms are complete player-facing offers. A document only becomes effective when the appropriate signer freely "
       "accepts. There are no invisible additional paragraphs. The public Charter takes precedence over narrower private "
       "agreements when they conflict about eligibility or consent.") +
     UL(*[HO(k, n) for k, n in (("ic-01", "Form IC-01 — Covenant of Joint Regency"), ("ic-02", "Form IC-02 — Writ of Safe Passage"),
                               ("ic-03", "Form IC-03 — Retainer of Witness Protection"), ("ic-04", "Form IC-04 — Misty's Memorandum of Memory Escrow"),
                               ("ic-05", "Form IC-05 — Warden's Declaration of Autonomy"), ("ic-06", "Form IC-06 — Covenant of Faction Sponsorship"),
                               ("ic-07", "Form IC-07 — Duel of Measured Claims"), ("ic-08", "Form IC-08 — Notice of Withdrawal and Return"),
                               ("challenge-card", "Blank Legal Challenge Card"))]) +
     P("Remember the Scriptorium's existing Ledger rules remain available for voluntarily negotiated bargains. Official "
       "Championship Charter petitions do not automatically exact the Scriptorium's default 5% soul-fee on a failed argument; "
       "hearings under this Charter waive that fee and impose disclosed procedural delay or limited Crown Mark risks instead.")),
    ("claimants", "8. Six Pregenerated Level-12 Claimants", H(2, "8. Six Pregenerated Level-12 Claimants") +
     chunk("8. SIX PREGENERATED LEVEL-12 CLAIMANTS", "1. Aurelia Quill") +
     H(3, "How It Began") + "".join(f"<p>{x}</p>" for x in _PROLOGUE) +
     "".join(claimant(p, a) for p, a in zip(PG.PREGENS, PG.ACTORS)) +
     H(3, "Shared party introductions") +
     P("Start the campaign by having each player answer two questions: <em>What would you change about Avernus if you "
       "actually held the First Crown?</em> and <em>Which personal principle would you refuse to trade, even to win?</em> "
       "The six claimants already know one another from the Brass Arbiter's courtroom. Read your <em>Other Claimants</em> "
       "notes aloud to each other, or keep them to yourself and let the table discover them. No one begins required to "
       "betray another player. If the claimants prefer separate claims, they can still travel as an alliance until final "
       "registration.")),
    ("soul-furnace", "Infernal Machines and Soul Coins", H(2, "Infernal Machines and Soul Coins") +
     P("In Avernus, war machines run on souls. Before the road to the Brass Citadel you may borrow, restore or steal one, and "
       "you will have to decide what to burn in it. These are the rules your table uses; the GM has the same pages.") +
     __import__("redline").codex_html(players=True)),
    ("rules", "9. Player Rules, Advancement and 2024 Conversion", H(2, "9. Player Rules, Advancement and 2024 Conversion") +
     chunk("9. PLAYER RULES", None).replace("Player’s Draft", "Player's Guide")),
]
journal("book2", "Book II — Claimants of the First Crown (Players)", "Books", B2, sort=1000)
