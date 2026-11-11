"""The Asmodeun Scriptorium: Infernal Codex of Contractual Magic (the author's companion text), and the GM toolkit."""
from jhelp import *
import spells as SP, playeroptions as PO, bestiary as B

S_ = []


def sp(key):
    return uuid_spell(key, next(s["name"] for s in SP.SPELLS if s["_id"] == fid("spell:" + key)))


import items as IT
import scriptorium_v2 as V
from blocks import spell_type, spell_lines, item_type, SCRIPTORIUM_ITEMS
section = V.section

_SPN = {n.lower(): k for n, k in V.SPELL_NAMES.items()}
_SPN.update({"seal of the first pact": "seal-first-pact", "contract of the seer's vigil": "contract-seers-vigil"})


def link(h):
    """Link spell names written in bold or italics to the Spells compendium."""
    def rep(m):
        tag, txt = m.group(1), m.group(2)
        k = _SPN.get(re.sub(r"<[^>]+>", "", txt).strip().lower())
        if not k:
            return m.group(0)
        name = next(n for n, kk in V.SPELL_NAMES.items() if kk == k)
        return f"<{tag}>@UUID[Compendium.{MOD}.spells.Item.{fid('spell:' + k)}]{{{name}}}</{tag}>"
    return re.sub(r"<(strong|em)>([^<@]{3,60})</\1>", rep, h)


def MDH(md, **kw):
    return V.md_html(md, link=link, **kw)


import re
S_.append(("intro", "Introduction: The Infernal Scripture of Binding",
           BANNER("Infernal Codex of Contractual Magic", "The Asmodeun Scriptorium",
                  "The Scriptorium holds that every contract bears Hell's sigil, binding souls to Asmodeus's grand design.") +
           MDH(section("## Introduction: The Infernal Scripture", "# **The Oath of the Infernal Lord**")) +
           SECRET("Using the Codex in The Night of the Red Clause",
                  "The Scriptorium is the in-world textbook the Red Clause's lawyers studied, and the source of the "
                  "adventure's contract magic. Share the lore pages with a player who researches the foundation (a clerk at "
                  "the Font of Knowledge keeps a copy under lock). The 26 spells and three subclasses are in the <em>Spells</em> "
                  "and <em>Player Options</em> compendiums.") +
           SECRET("The Hearthlight Irony",
                  "Read these codes beside the Red Clause's conduct. He has broken the first, second and fifth. Hesper Vane "
                  "(pregen) can point this out in court; the Brass Arbiter finds it persuasive.")))

S_.append(("oath", "The Oath of the Infernal Lord (Liturgy)",
           MDH(section("# **The Oath of the Infernal Lord**", "{{partCover}}\n\n# PART II")) +
           P("The playable oath is " + f"@UUID[Compendium.{MOD}.options.Item.{V.OATH['_id']}]{{Oath of the Infernal Lord}}" + ".")))

S_.append(("contracts", "Part II: Infernal Contracts",
           H(2, "Part II: Contracts") + MDH(section("## II. Infernal Contracts", "## Binding Rituals and Soul Contracts"))))

S_.append(("rituals", "Binding Rituals & Soul Contracts",
           MDH(section("## Binding Rituals and Soul Contracts", "# The Ledger")) +
           SECRET("Why the Hearthlight Certificates Fail",
                  "Compare these requirements with Form H-25. There is no soul tether, no collateral clause, no consideration "
                  "beyond a single night of service, and Clause IV expressly conveys <em>no</em> interest in the soul. Under "
                  "the Scriptorium's own doctrine, the foundation's \"unclaimed personal essence\" is a fiction.")))

S_.append(("ledger", "The Ledger: Playable Contracts",
           MDH(section("# The Ledger", "## Theology of Infernal Contracts")) +
           SECRET("The Ledger and the Red Clause",
                  "The Ledger is a campaign tool and isn't needed to run this one-shot; the High Court uses its own Writs. If "
                  "you want it anyway, Form H-25 as Hesper first wrote it is a Draft DC 10 contract with Loophole Rating 3. "
                  "The foundation's holiday revisions add loopholes rather than close them, which is exactly what the party "
                  "argues in Act IV.")))

S_.append(("theology", "Theology of Infernal Contracts",
           MDH(section("## Theology of Infernal Contracts", "{{partCover}}\n\n# PART III")) +
           SECRET("The Red Clause's Fatal Error",
                  "A soul taken by deceit is worth less to Hell than one fairly won, and a precedent built on forgery is "
                  "worthless. The Project Yuletide memorandum says so outright. The Red Clause's theology is sound; his "
                  "paperwork is not.")))

S_.append(("bestiary", "Infernal Bestiary & True Names",
           H(2, "Part III: Infernal Bestiary") + MDH(section("## III. Infernal Bestiary & True Names", "## Hierarchy of Hell"))))
S_.append(("hierarchy", "Hierarchy of Hell & Infernal Agents",
           MDH(section("## Hierarchy of Hell", "## Invoking and Negotiating"))))
S_.append(("invoking", "Guidelines for Invoking & Negotiating",
           MDH(section("## Invoking and Negotiating", "{{partCover}}\n\n# PART IV"))))

S_.append(("templates", "Part IV: Contract Templates",
           H(2, "Part IV: Contract Templates") + MDH(section("## IV. Infernal Contract Templates", "### 1. Contract"))))
_TPL = re.findall(r"^### (\d)\. (.+)$", section("## IV. Infernal Contract Templates", "{{partCover}}\n\n# PART V"), re.M)
for i, (n, title) in enumerate(_TPL):
    start = f"### {n}. {title}"
    end = f"### {_TPL[i + 1][0]}. {_TPL[i + 1][1]}" if i + 1 < len(_TPL) else "{{partCover}}\n\n# PART V"
    body = MDH(section(start, end), hshift=-1)
    body = body.replace(f"<h2>{n}. {title}</h2>", f"<h2>IV.{n}: {title}</h2>", 1)
    S_.append((f"template-{n}", f"Contract Template {n}: {title}", '<div class="rc-handout">' + body + "</div>"))


def _feature_list(feats):
    return "".join(f'<div class="rc-feature"><h4>{f["name"]}</h4><p class="rc-sptype"><em>{f["system"]["requirements"]}</em></p>'
                   f'{f["system"]["description"]["value"]}</div>' for f in feats)


def _sub(doc, kind, feats, icon_):
    return (f'<div class="rc-subclass"><div class="rc-npc">{IMG(icon(icon_), "rc-thumb")}<div><h3>@UUID[Compendium.{MOD}.options.Item.'
            f'{doc["_id"]}]{{{doc["name"]}}}</h3><p class="rc-sptype"><em>{kind}</em></p></div></div>'
            f'{link(doc["system"]["description"]["value"])}' + _feature_list(feats) + "</div>")


S_.append(("subclasses", "Part V: Infernal Subclasses",
           H(2, "Part V: Infernal Subclasses") +
           MDH(section("## V. Infernal Subclasses", "---\n\n# Wizard:")).replace("<h2>V. Infernal Subclasses</h2>", "") +
           P("Each subclass is in the <em>Player Options</em> compendium. Drop it on a character of the matching class and its "
             "features, oath spells and domain spells arrive by advancement at the right levels.") +
           _sub(V.SCHOOL, "Arcane Tradition (Wizard)", V.WIZ_FEATURES, "sub-school") +
           _sub(V.OATH, "Sacred Oath (Paladin)", V.PAL_FEATURES, "sub-oath") +
           _sub(V.DOMAIN, "Divine Domain (Cleric)", V.CLE_FEATURES, "sub-domain")))

_SSP = sorted([s for s in SP.SPELLS if s["flags"][MOD]["group"] == "Asmodeun Scriptorium"], key=lambda s: (s["system"]["level"], s["name"]))


def _spell(s):
    lines = "<br>".join(f"<strong>{k}:</strong> {v}" for k, v in spell_lines(s))
    return (f'<div class="rc-spell"><h3>@UUID[Compendium.{MOD}.spells.Item.{s["_id"]}]{{{s["name"]}}}</h3>'
            f'<p class="rc-sptype"><em>{spell_type(s)} (infernal)</em></p><p>{lines}</p>'
            f'{s["system"]["description"]["value"]}</div>')


S_.append(("spells", "Part VI: Infernal Contract Spells",
           H(2, "Part VI: Infernal Contract Spells") +
           MDH(section("## VI. The Infernal Contract Spells", "# Cantrips")).replace("<h2>VI. The Infernal Contract Spells</h2>", "") +
           "".join(_spell(s) for s in _SSP)))

S_.append(("spell-lists", "Appendix A: Spell Lists by Class",
           MDH(section("# Appendix A: Spell Lists by Class", "# Appendix B: Running the Church"))))

_REL = [i for its in IT.ITEMS.values() for i in its if i["name"] in SCRIPTORIUM_ITEMS]
S_.append(("relics", "Relics of the Scriptorium",
           H(2, "Relics of the Scriptorium") +
           P("Instruments of infernal law that a Scriptorium notary might carry, forge or confiscate. All four appear in "
             "<em>The Night of the Red Clause</em> and are in the <em>Items</em> compendium. <em>Golgorath's Quill</em> is the "
             "artifact the Scriptorium uses to notarize deals too large to trust to <em>quill of binding</em>.") +
           "".join(f'<div class="rc-spell"><h3>@UUID[Compendium.{MOD}.items.Item.{i["_id"]}]{{{i["name"]}}}</h3>'
                   f'<p class="rc-sptype"><em>{item_type(i)}</em></p>{i["system"]["description"]["value"]}</div>' for i in _REL)))

S_.append(("running", "Appendix B: Running the Church",
           MDH(section("# Appendix B: Running the Church", "{{backCover}}"))))

_back = section("##### The Ruby Lord's Oath")
_back_html = MDH(_back).replace("<h4>The Ruby Lord's Oath</h4>", "<h2>The Ruby Lord's Oath</h2>")
_back_html = _back_html.replace("<p>BIND POWER. SEAL FATE. SERVE THE RUBY LORD.</p>",
                                '<p class="rc-motto">BIND POWER. SEAL FATE. SERVE THE RUBY LORD.</p>')
S_.append(("back", "The Ruby Lord's Oath", '<div class="rc-backcover">' + _back_html + "</div>"))
journal("scriptorium", "The Asmodeun Scriptorium — Infernal Codex of Contractual Magic", "Books", S_, sort=500000,
        cls="rc-journal rc-codex")

