"""Handouts (Charter, forms, exhibits, writs), Dramatis Personae, the claimants and the GM toolkit."""
import os
from jhelp import *
import textbook as TB
import bestiary, spells as SP, playeroptions as PO, pregens as PG

A, I, T, M = uuid_actor, uuid_item, uuid_table, uuid_macro
HERE = os.path.dirname(os.path.abspath(__file__))
L2 = TB.load(os.path.join(HERE, "data", "book2.txt"))
L1 = TB.load(os.path.join(HERE, "data", "book1.txt"))


def DOC(title, body, stamp=None, cls="rc-handout", form=None):
    s = f'<div class="{cls}">' + (f'<p class="rc-form">{form}</p>' if form else "") + f"<h2>{title}</h2>{body}"
    if stamp:
        s += f'<div class="rc-stamp">{stamp}</div>'
    return s + "</div>"


def field_lines(html):
    import re
    return re.sub(r"_{4,}", '<span class="rc-blank"></span>', html)


def form_text(start, end):
    return field_lines(TB.render(TB.slice_lines(L2, start, end), skip_first=True))


# =========================================================================== HANDOUTS
H_ = []
inv = TB.slice_lines(L1, "Read aloud: the invitation", "Lawful premise")
H_.append(("invitation", "Handout 1 — The Invitation", DOC(
    "Official Notice of Conditional Succession",
    "<p><em>A red envelope arrives with no messenger. Its seal is a crown of nine black thorns. The paper smells of ash, cinnamon "
    "and wet iron.</em></p>"
    "<p>Whereas the First Layer requires a sovereign of proven force, ingenuity and contractual competence; whereas the present "
    "administration is subject to audit; and whereas the armies of Hell are weary of appointments made entirely by nepotism—</p>"
    "<p class='rc-big'>THE FIRST INTERPLANAR CHAMPIONSHIP IS HEREBY DECLARED.</p>"
    "<p>You may seek the throne alone. You may nominate partners. You may reject the invitation.</p>"
    "<p>But only those who attend will decide who rules Avernus next.</p>", stamp="OFFICE OF THE NINTH CROWN",
    form="The Office of the Ninth Crown · By Order of the Lord of Nessus")))
H_.append(("charter", "Handout 2 — The Championship Charter", DOC(
    "The Nine Articles of Infernal Succession",
    form_text("1. THE CHAMPIONSHIP CHARTER", "Player’s legal quick start").replace("<h3>The Nine Articles of Infernal Succession</h3>", "")
    + "<h3>Player's Legal Quick Start</h3>" + TB.render(TB.slice_lines(L2, "Player’s legal quick start", "2. NEW SUBCLASS"), skip_first=True),
    stamp="WITNESSED · OFFICE OF THE NINTH CROWN", form="Public Instrument · Binding on All Contestants")))
FORMS = [("ic-01", "Form IC-01 — Covenant of Joint Regency"), ("ic-02", "Form IC-02 — Writ of Safe Passage"),
         ("ic-03", "Form IC-03 — Retainer of Witness Protection"), ("ic-04", "Form IC-04 — Misty’s Memorandum of Memory Escrow"),
         ("ic-05", "Form IC-05 — Warden’s Declaration of Autonomy"), ("ic-06", "Form IC-06 — Covenant of Faction Sponsorship"),
         ("ic-07", "Form IC-07 — Duel of Measured Claims"), ("ic-08", "Form IC-08 — Notice of Withdrawal and Return")]
for n, (k, t) in enumerate(FORMS):
    end = FORMS[n + 1][1] if n + 1 < len(FORMS) else "Blank legal challenge card"
    H_.append((k, f"Handout {n + 3} — {t.split(' — ')[1]}", DOC(t.split(" — ")[1], form_text(t, end),
                                                               stamp="PENDING SIGNATURE", form=t.split(" — ")[0] + " · Championship of the First Crown")))
H_.append(("challenge-card", "Handout 11 — Blank Legal Challenge Card", DOC(
    "Legal Challenge Card", form_text("Blank legal challenge card", "Remember the Scriptorium"),
    form="Filed before the Brass Arbiter")))
H_.append(("circular", "Handout 12 — Hollis Valrick's Circular", DOC(
    "Circular No. 9-C: On the Meaning of 'Claimant'",
    "<p><strong>From:</strong> The Deputy Registrar, Hall of Registrants, Brass Citadel.<br><strong>To:</strong> All claims desks.</p>"
    "<p>Effective immediately, desks shall interpret the word <em>claimant</em> in the Charter as <strong>singular</strong>. Each "
    "contestant shall be registered as a separate claimant and assigned a separate account for Crown Marks, liabilities and "
    "successor rights. Applications styled as 'joint slates' are to be divided into their component persons for the "
    "convenience of the Registry.</p>"
    "<p>Desks are reminded that individual accounts permit the orderly transfer of unspent Marks to qualified successors.</p>"
    "<p>— <em>H. Valrick, Deputy Registrar</em></p>"
    "<p class='rc-fine'><em>GM note: the circular is unlawful. Charter Article III expressly permits joint slates. Cite it and the "
    "clerk must register the slate. A DC 18 Insight check reveals why Hollis opposes it: joint claims reduce the number of isolated "
    "souls that can be bought, blackmailed or harvested.</em></p>", stamp="FILED — UNDER REVIEW")))
H_.append(("petition-m9", "Handout 13 — Petition M-9 and Its Annex", DOC(
    "Petition M-9: Evidence Royalty of the Pyric Triune",
    "<p><strong>Petitioner:</strong> Misty, Queen of Barbed Chains, by her counsel the Pyric Triune.</p>"
    "<p><strong>Prayer:</strong> That any crown candidate using <em>borrowed memory, replicated identity, or construct testimony</em> "
    "be declared to owe the Pyric Triune a perpetual evidence royalty of one memory per instance of use, payable on investiture.</p>"
    "<p><strong>Grounds:</strong> The memories, identities and testimonies of Greyhurst were lawfully conveyed to the Petitioner by "
    "the sole competent authority of that town, as evidenced by the Annex.</p>"
    "<h3>Annex A</h3>"
    "<p>I, <strong>Osric Kane</strong>, Mayor of Greyhurst, for good and valuable consideration (namely, the protection of the town "
    "by a host of devils), do hereby consent on behalf of the citizens of Greyhurst to the transfer of their names, memories and "
    "testimonies to the custody of the Pyric Triune.</p><p>— <em>O. Kane</em> (seal of the Pyric Triune affixed)</p>"
    "<p class='rc-fine'><em>GM note: a character can defeat the claim by proving (i) Kane lacked authority over individual names, "
    "(ii) the transferred memories were not his to sell, or (iii) the annex misidentifies the contracting party. Each separate, "
    "persuasive argument plus appropriate evidence is a success in a two-successes-before-two-failures hearing (DC 18 when "
    "disputed). A document establishing lack of authority is one automatic success.</em></p>", stamp="RECEIVED")))
H_.append(("first-refusal", "Handout 14 — Misty's Perpetual First Refusal Writ", DOC(
    "The Perpetual First Refusal Writ",
    "<p><strong>Grantor:</strong> the claimant or slate named below, upon investiture as Sovereign of the First Layer.<br>"
    "<strong>Grantee:</strong> Misty, Queen of Barbed Chains, and the Pyric Triune.</p>"
    "<p><strong>Clause 1 — The Right.</strong> Whenever the Sovereign's courts, treasury or officers come to hold a debt, memory or "
    "secret by forfeit, default, confiscation or lawful judgment, the Grantee shall have the first right to purchase it at the "
    "Registry's appraised value before it is sold, released or destroyed.</p>"
    "<p><strong>Clause 2 — Disputes of Memory.</strong> In any dispute over a memory held by the Crown, the Grantee shall receive "
    "one-tenth of the memory's appraised value as a custodial fee, regardless of outcome.</p>"
    "<p><strong>Clause 3 — Term.</strong> This right is perpetual and passes to the Sovereign's successors in office.</p>"
    "<p><strong>Clause 4 — Consideration.</strong> In exchange, the Grantee withdraws her own claim to the First Crown, places the "
    "Pyric Triune's counsel at the Sovereign's disposal and discloses the true location of every Greyhurst name held in her "
    "registers.</p>"
    "<p><strong>Clause 5 — Exclusions.</strong> Nothing in this Writ conveys a soul. Nothing in this Writ obliges any citizen who "
    "has not personally signed. There is no appendix.</p>"
    "<p><strong>Clause 6 — Amendment.</strong> This Writ may be amended only by a written instrument signed by both parties.</p>"
    "<p>Claimant: <span class='rc-blank'></span> Pyric Witness: <span class='rc-blank'></span></p>"
    "<p class='rc-fine'><em>GM note: Misty conceals nothing; her trap is economic. Even small percentages of future memory "
    "disputes give her influence. Players may negotiate a sunset clause, an independent audit, a prohibition on children's "
    "memories, or personal liability borne by the ruler instead of citizens. Each material concession requires something "
    "meaningful in return; a single DC 20 Persuasion check never erases the contract.</em></p>", stamp="THE PYRIC TRIUNE",
    form="Offered in Audience · The Chamber of Iron Roses")))
H_.append(("welcome-sign", "Handout 15 — The Welcome Sign", DOC(
    "WELCOME, PROSPECTIVE SOVEREIGN",
    "<p class='rc-big'>ALL COMPLAINTS MUST BE FILED IN TRIPLICATE.</p>"
    "<p><em>A sign leaning sideways on the far bank of the burning river, Map 1.</em></p>")))
H_.append(("iron-warning", "Handout 16 — The Warning Written in Iron", DOC(
    "THE DEAD ARE ELIGIBLE. THE LIVING ARE EXPENDABLE. THE UNCLAIMED ARE PROPERTY OF THE HOST.",
    "<p>Beneath the inscription someone has carved:</p><p class='rc-big'>THERE IS NO SUCH THING AS UNCLAIMED.</p>")))
EXH = [
    ("exhibit-a", "Exhibit A — The False Entrants", "An Obsolete Tournament Bracket",
     "<p><em>Recovered from a sealed brass casket drifting on the Styx-touched current.</em></p>"
     "<table class='rc-table'><thead><tr><th>Entrant</th><th>Origin</th><th>Registered</th><th>Status</th></tr></thead><tbody>"
     "<tr><td>Aldous Pell</td><td>Greyhurst</td><td>This year</td><td>Died forty-one years ago</td></tr>"
     "<tr><td>Marrow Teague</td><td>Greyhurst</td><td>This year</td><td>Died twenty-nine years ago</td></tr>"
     "<tr><td><strong>Marus Greenbottle</strong></td><td>Greyhurst</td><td>This year</td><td><em>Living</em> (recorded 'unclaimed')</td></tr>"
     "<tr><td>Wenna Rook</td><td>Greyhurst</td><td>This year</td><td>Died fifty-six years ago</td></tr></tbody></table>"
     "<p>Every entry is in the same hand. The registrar's mark is <strong>H-25/RETURN</strong>.</p>"),
    ("exhibit-b", "Exhibit B — The False Service Order", "Warrant of Collection: Unclaimed Souls of Greyhurst",
     "<p>By order of the Registry, the bearers are authorised to collect all <em>unclaimed</em> souls of Greyhurst and deliver them "
     "to the tournament's asset pool.</p><p class='rc-fine'>Authority cited: <em>Annex A to Petition M-9</em> (the mayor's consent). "
     "No individual citizen's signature is attached. <strong>Collection suspended pending challenge.</strong></p>"),
    ("exhibit-c", "Exhibit C — The Unmodified Command Transcript", "Recorded at the Inverse Circle",
     "<p><em>The circle's own record, released when Name → Consent → Witness → Jurisdiction is set in order.</em></p>"
     "<p>KANE: <em>Invert the third ring. Yes, the registration line. They'll never read it; they'll only see devils arriving to "
     "protect them.</em></p><p>CLERK: <em>Mayor, the inverted line registers the villagers. It sends them, not the devils.</em></p>"
     "<p>KANE: <em>Then they'll be registered somewhere safe. Do it.</em></p>"),
    ("exhibit-e", "Exhibit E — Chain of Title", "Serial Ledger, Orro's Stall",
     "<p>Every 'regiment' of names on sale bears the same red serialization: <strong>H-25/RETURN</strong>, the docket number of the "
     "Red Clause's Waterdeep collection programme. The Registry certificate is countersigned <em>H. Valrick, Deputy Registrar</em>.</p>"),
    ("exhibit-f", "Exhibit F — Hollis's Immunity Document", "Grant of Immunity in Exchange for Testimony",
     "<p>The witness Hollis Valrick shall be immune from prosecution for all acts of registration fraud disclosed in his testimony, "
     "<strong>including acts yet to be discovered</strong>.</p><p class='rc-fine'><em>Strike the bolded phrase and his testimony can "
     "still be taken.</em></p>"),
    ("exhibit-g", "Exhibit G — The True Roster", "Roster of Validly Registered Claimants",
     "<p>The roster Hollis carried toward the administrative elevator. None of the Vacant King's entrants appears on it. A "
     "witnessed judgment on these false entries ends the King's Forged Sovereignty.</p>"),
]
for k, t, title, body in EXH:
    H_.append((k, t, DOC(title, body, stamp="ADMITTED IN EVIDENCE", form=t.split(" — ")[0])))
import redline as _RL
H_.extend(_RL.handouts(DOC, field_lines))
H_.extend(__import__("soulforged").handouts(DOC, field_lines))
journal("handouts", "Handouts — Interplanal Champions", "Handouts", H_, sort=200000, cls="rc-journal rc-handouts")

# =========================================================================== DRAMATIS PERSONAE
N_ = [("intro", "Dramatis Personae", BANNER("Interplanal Champions", "Dramatis Personae", "Who's who in the war for Avernus") +
       P("Every creature here is in the <em>Interplanal Champions — Actors</em> compendium and is installed into labelled actor "
         "folders by the Championship Manager."))]
for folder, actors in bestiary.FOLDERS.items():
    body = H(2, folder)
    for a in actors:
        if a["type"] == "vehicle":
            hp_ = a["system"]["attributes"]["hp"]
            body += (f'<div class="rc-npc">{IMG(a["img"], "rc-thumb")}<div><h3>@UUID[Compendium.{MOD}.actors.Actor.{a["_id"]}]{{{a["name"]}}}</h3>'
                     f'<p class="rc-meta">{a["system"]["traits"]["size"].replace("lg", "Large").replace("huge", "Huge")} vehicle · AC {a["system"]["attributes"]["ac"]["flat"]} · '
                     f'HP {hp_["max"]} · threshold {hp_["dt"]} / mishap {hp_["mt"]} · speed {a["system"]["attributes"]["movement"]["walk"]} ft.</p>'
                     f'{a["system"]["details"]["biography"]["value"]}</div></div>')
            continue
        cr = a["system"]["details"]["cr"]
        crs = {0.125: "1/8", 0.25: "1/4", 0.5: "1/2"}.get(cr, str(cr))
        ty = a["system"]["details"]["type"]["value"] or "object"
        body += (f'<div class="rc-npc">{IMG(a["img"], "rc-thumb")}<div><h3>@UUID[Compendium.{MOD}.actors.Actor.{a["_id"]}]{{{a["name"]}}}</h3>'
                 f'<p class="rc-meta">{ty.title()} · CR {crs} · AC {a["system"]["attributes"]["ac"]["flat"]} · '
                 f'HP {a["system"]["attributes"]["hp"]["max"]}</p>{a["system"]["details"]["biography"]["value"]}</div></div>')
    N_.append((slug(folder), folder, body))
journal("npcs", "Dramatis Personae — Interplanal Champions", "Books", N_, sort=300000)

# =========================================================================== CLAIMANTS
P_ = [("intro", "Pregenerated Claimants", BANNER("Level 12", "Pregenerated Claimants", "Six claimants for the First Crown") +
       P("Each claimant is a complete 12th-level character built from the dnd5e SRD and this module's subclasses, spells and "
         "relics. Assign them from the actor folder <em>Interplanal Champions — Pregenerated Claimants</em>.") +
       H(2, "Connections") + TABLE(["Claimant", "Personal stake", "Where it matters", "Evidence they can bring"],
                                   [list(c) for c in __import__("pregen_lore").CONNECTIONS]))]
from pregen_lore import LORE, SHEET, PROLOGUE
P_[0] = (P_[0][0], P_[0][1], P_[0][2] + H(2, "How It Began") + "".join(P(x) for x in PROLOGUE))
for p, a in zip(PG.PREGENS, PG.ACTORS):
    L_, S2 = LORE[p["key"]], SHEET[p["key"]]
    ab = " · ".join(f"{k.upper()} {v}" for k, v in zip(("str", "dex", "con", "int", "wis", "cha"), p["abilities"]))
    det = " · ".join(f"<strong>{k}</strong> {S2[k.lower()]}" for k in ("Age", "Height", "Weight", "Eyes", "Hair", "Skin", "Faith"))
    body = (f'<div class="rc-pc" style="--pc:{p["color"]}">{IMG(portrait("pc-" + p["key"]), "rc-portrait rc-right")}'
            f'<h2>@UUID[Compendium.{MOD}.pregens.Actor.{a["_id"]}]{{{p["name"]}}}</h2>'
            f'<p class="rc-meta">{p["title"]} · {p["race"]} {p["cls"]} 12 ({p["sub"]}) · {p["align"]}</p>'
            f'<p class="rc-meta">{ab} · HP {a["flags"][MOD]["expectedHp"]}</p>'
            f'<p class="rc-meta">{det}</p><p><em>{S2["appearance"]}</em></p>'
            + P(L_["role"]) + H(3, "Backstory") + "".join(f"<p>{b}</p>" for b in L_["backstory"])
            + BOX("Why You Entered", L_["tonight"]) + H(4, "Private Pressure (DM, and this player only)") + P(L_["tie"])
            + H(4, "Your Claim") + P(L_["knows"])
            + H(4, "The Other Claimants") + UL(*[f"<strong>{n}.</strong> {t}" for n, t in L_["others"]])
            + BOX("Tactics", L_["table"]) + H(4, "Toward Level 17") + P(L_["goal"])
            + H(3, "Personality") + TABLE(["", ""], [["Traits", "<br>".join(S2["traits"])], ["Ideal", S2["ideal"]], ["Bond", S2["bond"]],
                                                    ["Flaw", S2["flaw"]], ["Allies", S2["allies"]]])
            + H(4, "Playing " + p["name"].split()[-1 if p["key"] == "caldris" else (1 if p["key"] == "nema" else 0)]) + UL(*S2["play"])
            + (f'<p class="rc-fine"><em>{p["subst"]}</em></p>' if p.get("subst") else "") + "</div>")
    P_.append((p["key"], p["name"], body))
P_.append(("sheets", "Printable Character Sheets (PDF)", f"@@PDF:modules/{MOD}/assets/docs/claimant-character-sheets.pdf"))
P_.append(("players-guide", "Player's Guide (PDF)", f"@@PDF:modules/{MOD}/assets/docs/players-guide.pdf"))
journal("pregens", "Pregenerated Claimants — Interplanal Champions", "Books", P_, sort=400000)
