"""The Asmodeun Scriptorium, expanded edition (v2 manuscript by Asmo).

Everything rules-bearing (26 spells, three subclasses) and every lore page is generated from
data/Asmodeun-Scriptorium-v2.md, so the Foundry compendiums, the journal and the PDF all read the same text.
"""
import re, os
from lib5e import *

HERE = os.path.dirname(os.path.abspath(__file__))
MD = open(os.path.join(HERE, "data", "Asmodeun-Scriptorium-v2.md"), encoding="utf-8").read()

# The manuscript was renumbered I–VI but a few cross-references still use the draft's part numbers.
PART_FIX = [("Parts VIII and IX", "Parts V and VI"), ("Parts II through VII", "Parts II through IV"),
            ("Part VIII", "Part V"), ("Part IX", "Part VI"), ("Part VII", "Part IV")]
for a, b in PART_FIX:
    MD = MD.replace(a, b)

DTYPES = "fire|psychic|necrotic|radiant|cold|lightning|force|acid|poison|thunder|bludgeoning|piercing|slashing"


# --------------------------------------------------------------------------------------------- markdown → HTML
def inline(t):
    t = t.replace("\\[", "[").replace("\\]", "]").replace("\\_", "_").replace("\\*", "&#42;")
    t = t.replace("&", "&amp;").replace("&amp;#42;", "&#42;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = t.replace("—", "—")
    return t


def enrich_damage(h):
    """Turn '2d10 psychic damage' into a rollable enricher (skips text already inside an enricher)."""
    def rep(m):
        return f"[[/damage {m.group(1)} type={m.group(2)}]]"
    h = re.sub(r"(?<![\[/=\w])(\d+d\d+)\s+(" + DTYPES + r")\s+damage", rep, h)
    h = re.sub(r"<strong>\[\[/damage ([^\]]+)\]\]</strong>", r"[[/damage \1]]", h)
    return h


def strip_layout(md):
    out, skip = [], 0
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if re.match(r"^\{\{(imageMask|banner|frontCover|partCover|backCover|footnote)", s):
            if s.endswith("}}") and s.count("{{") == s.count("}}"):
                i += 1
                continue
            depth = 1
            i += 1
            while i < len(lines) and depth:
                depth += lines[i].count("{{") - lines[i].count("}}")
                i += 1
            continue
        if s.startswith("![") or s == "\\page" or s.startswith("<!--") or s.startswith("Use --") or s.endswith("-->"):
            i += 1
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def md_html(md, *, link=None, hshift=0, enrich=True):
    """Small markdown converter for the manuscript's Homebrewery flavour."""
    md = strip_layout(md)
    lines = md.split("\n")
    out, para, lst, ltype = [], [], [], None
    box = []  # stack of open boxes

    def flush_para():
        nonlocal para
        if para:
            txt = para[0].strip()
            for x in para[1:]:
                x = x.strip()
                txt += ("<br>" if x.startswith("**") else " ") + x
            out.append("<p>" + inline(txt).replace("&lt;br&gt;", "<br>") + "</p>")
            para = []

    def flush_list():
        nonlocal lst, ltype
        if lst:
            out.append(f"<{ltype}>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + f"</{ltype}>")
            lst, ltype = [], None

    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if s.startswith("{{wide") or s == "{{":
            flush_para(); flush_list()
            box.append("")
            i += 1
            continue
        m = re.match(r"^\{\{(note|descriptive)", s)
        if m:
            flush_para(); flush_list()
            out.append(f'<div class="rc-box rc-{m.group(1)}">')
            box.append("</div>")
            i += 1
            continue
        if s == "}}":
            flush_para(); flush_list()
            if box:
                out.append(box.pop())
            i += 1
            continue
        if not s or re.fullmatch(r":+", s):
            flush_para(); flush_list()
            i += 1
            continue
        if s in ("---", "___"):
            flush_para(); flush_list()
            i += 1
            continue
        hm = re.match(r"^(#{1,6})\s+(.*)$", s)
        if hm:
            flush_para(); flush_list()
            n = len(hm.group(1))
            text = hm.group(2).strip().strip("*").strip()
            lvl = min(6, max(2, n + hshift)) if n < 5 else 4
            out.append(f"<h{lvl}>{inline(text)}</h{lvl}>")
            i += 1
            continue
        if s.startswith("|"):
            flush_para(); flush_list()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not re.fullmatch(r"[:\- ]+", "".join(r))]
            out.append('<table class="rc-table"><thead><tr>' + "".join(f"<th>{inline(h)}</th>" for h in head)
                       + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                                                          for r in body) + "</tbody></table>")
            continue
        if s.startswith(">"):
            flush_para(); flush_list()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            out.append('<p class="rc-flavour">' + inline(" ".join(q)) + "</p>")
            continue
        lm = re.match(r"^(\*|-|\d+\.)\s+(.*)$", s)
        if lm and not s.startswith("**"):
            flush_para()
            t = "ol" if lm.group(1)[0].isdigit() else "ul"
            if ltype and ltype != t:
                flush_list()
            ltype = t
            lst.append(lm.group(2))
            i += 1
            continue
        if lst and raw.startswith("   "):
            lst[-1] += " " + s
            i += 1
            continue
        flush_list()
        para.append(s)
        i += 1
    flush_para(); flush_list()
    while box:
        out.append(box.pop())
    h = "".join(out)
    h = re.sub(r"</(ul|ol)>\s*<\1>", "", h)
    if enrich:
        h = enrich_damage(h)
    if link:
        h = link(h)
    return h


def section(start, end=None, src=None):
    """Text between a heading line `start` (inclusive) and `end` (exclusive)."""
    src = src or MD
    a = src.index(start)
    b = src.index(end, a + len(start)) if end else len(src)
    return src[a:b]


# --------------------------------------------------------------------------------------------- spells
SPELL_KEY = {"Seal of the First Pact": "seal-first-pact", "Seer's Vigil": "contract-seers-vigil",
             "Contract of the Infernal Fury": "contract-infernal-fury", "Contract of the Soulforged Blade": "soulforged-blade",
             "Devil's Due": "devils-due"}
SPELL_ICON = {"Fine Print": "sp-fine", "Sulfurous Seal": "sp-sulfur", "Brand of Arrears": "sp-arrears", "Objection": "sp-objection",
              "Seal of the First Pact": "sp-seal", "True Name Revelation": "sp-truename", "Retainer's Fee": "sp-retainer",
              "Quill of Binding": "sp-quill", "Summons and Complaint": "sp-summons", "Contract of the Infernal Fury": "sp-fury",
              "Devil's Due": "sp-due", "Seer's Vigil": "sp-vigil", "Injunction": "sp-injunction", "Binding Clause": "sp-clause",
              "Contract of the Soulforged Blade": "sp-blade", "Writ of Repossession": "sp-repossess", "Soul Covenant": "sp-covenant",
              "Infernal Class Action": "sp-classaction", "Contract of Infernal Servitude": "sp-servitude",
              "Amend the Record": "sp-amend", "Foreclosure": "sp-foreclosure", "Writ of Cessation": "sp-cessation",
              "Charter of the Iron Tower": "sp-charter", "Devil's Advocate": "sp-advocate", "Pact Primeval": "sp-primeval",
              "Writ of Damnation": "sp-damnation"}
SCHOOLS = {"abjuration": "abj", "conjuration": "con", "divination": "div", "enchantment": "enc", "evocation": "evo",
           "illusion": "ill", "necromancy": "nec", "transmutation": "trs"}


def skey(name):
    return SPELL_KEY.get(name) or slug(name.replace("'", ""))


def _activation(ct):
    ct0 = ct.split(",")[0].strip().lower()
    m = re.match(r"(\d+)\s+(action|bonus action|reaction|minute|minutes|hour|hours)", ct0)
    n, kind = int(m.group(1)), m.group(2)
    if kind == "bonus action":
        return activation("bonus", 1)
    if kind == "reaction":
        cond = ct.split("which you take", 1)[1].strip() if "which you take" in ct else ""
        return activation("reaction", 1, cond)
    if kind.startswith("minute"):
        return activation("minute", n)
    if kind.startswith("hour"):
        return activation("hour", n)
    return activation("action", 1)


def _range(r):
    r = r.strip()
    if r.lower().startswith("touch"):
        return rng("", "touch")
    if r.lower().startswith("self"):
        sp = re.search(r"\((.*)\)", r)
        return rng("", "self", sp.group(1) if sp else "")
    m = re.match(r"(\d[\d,]*)\s*(feet|foot|miles?)", r)
    return rng(int(m.group(1).replace(",", "")), "ft" if m.group(2).startswith("f") else "mi")


def _duration(d):
    d = d.strip()
    conc = d.lower().startswith("concentration")
    core = re.sub(r"^Concentration,\s*up to\s*", "", d, flags=re.I)
    if core.lower().startswith("instant"):
        return {"value": "", "units": "inst"}, conc
    if core.lower().startswith("until dispelled"):
        return {"value": "", "units": "disp"}, conc
    if core.lower().startswith("until fulfilled"):
        return {"value": "", "units": "perm"}, conc
    m = re.match(r"(\d+)\s+(round|minute|hour|day)", core)
    return {"value": m.group(1), "units": m.group(2)}, conc


def parse_spells():
    sec = section("# Cantrips", "# Appendix A")
    blocks = re.split(r"\n(?=### )", sec)
    out = []
    for b in blocks:
        if not b.startswith("### "):
            continue
        lines = b.split("\n")
        name = lines[0][4:].strip()
        meta, body = {}, []
        typ = ""
        for ln in lines[1:]:
            s = ln.strip()
            if s.startswith("###### "):
                t = s[7:].strip()
                fm = re.match(r"\*\*(.+?):\*\*\s*(.*)", t)
                if fm:
                    meta[fm.group(1)] = fm.group(2).strip()
                else:
                    typ = t.strip("*")
                continue
            if re.match(r"^# ", s):  # level dividers
                break
            body.append(ln)
        tl = typ.lower()
        level = 0 if "cantrip" in tl else int(re.match(r"(\d)", tl).group(1))
        school = SCHOOLS[next(w for w in SCHOOLS if w in tl)]
        ritual = "ritual" in tl or "as a ritual" in meta["Casting Time"]
        comp = meta["Components"]
        comps = [c for c, k in (("vocal", "V"), ("somatic", "S"), ("material", "M")) if re.search(rf"(^|[ ,]){k}([ ,(]|$)", comp)]
        mat = re.search(r"M \((.*)\)\s*$", comp)
        materials = mat.group(1) if mat else ""
        cost = re.search(r"([\d,]+)\s*gp", materials)
        dur, conc = _duration(meta["Duration"])
        out.append(dict(name=name, key=skey(name), level=level, school=school, ritual=ritual, comps=comps,
                        materials=materials, cost=int(cost.group(1).replace(",", "")) if cost else 0,
                        consumed="consume" in materials, act=_activation(meta["Casting Time"]),
                        rng=_range(meta["Range"]), dur=dur, conc=conc, classes=meta["Classes"],
                        body="\n".join(body).strip(), meta=meta))
    return out


SPELL_SPECS = parse_spells()
SPELL_NAMES = {s["name"]: s["key"] for s in SPELL_SPECS}


def _sp(d):
    return d  # placeholder for readability


def spell_activities(s):
    k, L = s["key"], s["level"]
    sc1 = lambda n, die, t: dmg(n, die, "", [t], "whole", 1)  # +1 die per slot level / cantrip tier
    spec = {
        "fine-print": [utility(k, 0, name="Read the Fine Print")],
        "sulfurous-seal": [utility(k, 0, name="Press the Seal"),
                           damage_act(k + "-b", 1, name="Seal Broken", parts=[dmg_formula("1", ["fire"])], act=activation("special", None))],
        "brand-of-arrears": [attack(k, 0, kind="ranged", classification="spell", parts=[sc1(1, 8, "psychic")], range_=60,
                                    name="Read the Account", ability="")],
        "objection": [utility(k, 0, name="Object!", act=s["act"])],
        "seal-first-pact": [utility(k, 0, name="Affix the Seal"),
                            damage_act(k + "-break", 1, name="The Seal Shatters", parts=[sc1(2, 10, "psychic")],
                                       act=activation("special", None))],
        "true-name-revelation": [save(k, 0, ability="cha", spell=True, on_save="none", name="Reveal the Name",
                                      duration={"concentration": True, "value": "1", "units": "hour", "special": "", "override": False})],
        "retainers-fee": [heal_act(k, 0, formula_part=dmg(2, 8, "@mod", ["temphp"], "whole", 2), name="Pay the Retainer",
                                   temp=True, act=activation("bonus", 1)),
                          damage_act(k + "-b", 1, name="Duty Abandoned (lost temp HP)", parts=[dmg_formula("2d8 + @mod", ["psychic"])],
                                     act=activation("special", None))],
        "quill-of-binding": [utility(k, 0, name="Conjure the Quill"),
                             damage_act("quill-accountability", 1, name="Clause of Arcane Accountability",
                                        parts=[dmg(1, 6, "", ["psychic"])], act=activation("special", None))],
        "summons-and-complaint": [utility(k, 0, name="Conjure the Clerk"),
                                  save(k + "-writ", 1, ability="cha", spell=True, on_save="none", name="Serve the Writ",
                                       act=activation("special", None))],
        "contract-infernal-fury": [utility(k, 0, name="Strike the Bargain"),
                                   damage_act(k + "-b", 1, name="Forbidden Term Broken", parts=[dmg(2, 6, "", ["fire"])],
                                              act=activation("special", None))],
        "devils-due": [save(k, 0, ability="cha", spell=True, parts=[sc1(6, 6, "necrotic")], name="Collect the Debt"),
                       damage_act(k + "-max", 1, name="Willful Breach (failed save, maximised)",
                                  parts=[dmg_formula("36", ["necrotic"])], act=activation("special", None))],
        "contract-seers-vigil": [utility(k, 0, name="Join Minds")],
        "injunction": [save(k, 0, ability="wis", spell=True, on_save="none", name="Issue the Injunction"),
                       damage_act(k + "-b", 1, name="Forbidden Action Attempted", parts=[dmg(4, 8, "", ["psychic"])],
                                  act=activation("special", None))],
        "binding-clause": [utility(k, 0, name="Inscribe the Clause"),
                           damage_act(k + "-geas", 1, name="Geas Enforcement (daily)", parts=[dmg(4, 10, "", ["psychic"])],
                                      act=activation("special", None))],
        "soulforged-blade": [utility(k, 0, name="Forge the Compact"),
                             damage_act(k + "-combust", 1, name="Souls Combust (per soul)", parts=[dmg(2, 8, "", ["psychic"])],
                                        act=activation("special", None))],
        "writ-of-repossession": [save(k, 0, ability="str", spell=True, on_save="none", name="Repossess")],
        "soul-covenant": [utility(k, 0, name="Speak the Covenant"),
                          damage_act(k + "-defy", 1, name="Defiance (daily)", parts=[dmg(5, 10, "", ["psychic"])], act=activation("special", None)),
                          damage_act(k + "-warn", 2, name="Betrayal Warning", parts=[dmg(8, 6, "", ["fire"])], act=activation("special", None)),
                          damage_act(k + "-fate", 3, name="Shared Fate", parts=[dmg(10, 6, "", ["necrotic"])], act=activation("special", None)),
                          damage_act(k + "-breach", 4, name="Breach: Hell's Judgment",
                                     parts=[dmg(6, 6, "", ["fire"]), dmg(6, 6, "", ["radiant"])], act=activation("special", None))],
        "infernal-class-action": [save(k, 0, ability="dex", spell=True, parts=[sc1(8, 6, "fire")], name="Read Judgment",
                                       tgt=target(6, "creature"))],
        "contract-of-infernal-servitude": [save(k, 0, ability="cha", spell=True, on_save="none", name="Bind into Service")],
        "amend-the-record": [save(k, 0, ability="cha", spell=True, on_save="none", name="Amend an Article"),
                             damage_act(k + "-b", 1, name="The Ledger Rejects Your Hand", parts=[dmg(6, 10, "", ["psychic"])],
                                        act=activation("special", None))],
        "foreclosure": [save(k, 0, ability="cha", spell=True, parts=[dmg(12, 10, "", ["necrotic"])], name="Call Every Debt")],
        "writ-of-cessation": [utility(k, 0, name="Declare Jurisdiction"),
                              save(k + "-b", 1, ability="wis", spell=True, on_save="none", parts=[dmg(6, 10, "", ["psychic"])],
                                   name="Hostile Action Within", act=activation("special", None))],
        "charter-of-the-iron-tower": [utility(k, 0, name="Charter the Demesne"),
                                      damage_act(k + "-b", 1, name="Chastisement", parts=[dmg(8, 10, "", ["psychic"])],
                                                 act=activation("special", None))],
        "devils-advocate": [utility(k, 0, name="Retain the Advocate")],
        "pact-primeval": [utility(k, 0, name="Forge the Covenant"),
                          damage_act(k + "-b", 1, name="Breach of the First Contract", parts=[dmg(20, 10, "", ["psychic"])],
                                     act=activation("special", None))],
        "writ-of-damnation": [save(k, 0, ability="cha", spell=True, parts=[dmg(15, 12, "", ["necrotic"])], name="Execute Judgment")],
    }
    return spec[k]


def build_spells(classes_note=True):
    docs, lists = [], {}
    e_fury = effect("sp-fury", "Infernal Fury", icon("sp-fury"), duration={"seconds": 60},
                    changes=[("system.bonuses.mwak.damage", 2, "1d6[fire]"), ("system.bonuses.rwak.damage", 2, "1d6[fire]")],
                    description="<p>Your weapon attacks deal an extra 1d6 fire damage on a hit. Breaking the Forbidden Term "
                                "ends the spell and deals 2d6 fire damage to you.</p>")
    for s in SPELL_SPECS:
        lists[s["key"]] = s["classes"]
        desc = md_html(s["body"], hshift=0)
        desc += f"<p class='rc-spell-classes'><strong>Spell Lists.</strong> {s['classes']}</p>"
        d = spell(s["key"], s["name"], desc, img=icon(SPELL_ICON[s["name"]]), level=s["level"], school=s["school"],
                  activities=spell_activities(s), comps=tuple(s["comps"]), materials=s["materials"], mat_cost=s["cost"],
                  mat_consumed=s["consumed"], act=s["act"], duration=s["dur"], rng_=s["rng"], ritual=s["ritual"],
                  concentration=s["conc"], effects=[e_fury] if s["key"] == "contract-infernal-fury" else None)
        if s["key"] == "contract-infernal-fury":
            a0 = next(iter(d["system"]["activities"].values()))
            a0["effects"] = [{"_id": e_fury["_id"]}]
        for a in d["system"]["activities"].values():
            if a["type"] in ("save", "utility") and s["conc"] and a["activation"]["type"] != "special":
                a["duration"] = {"concentration": True, "value": s["dur"]["value"], "units": s["dur"]["units"],
                                 "special": "", "override": False}
        d["flags"][MOD] = {"group": "Asmodeun Scriptorium", "book": "v2", "castingTime": s["meta"]["Casting Time"]}
        d["system"]["identifier"] = s["key"]
        docs.append(d)
    return docs, lists


# --------------------------------------------------------------------------------------------- subclasses
def features_from(md_block):
    """Split a subclass block into (preamble_md, [(level, name, body_md)], trailing_boxes_md)."""
    parts = re.split(r"\n(?=#### )", md_block)
    pre = parts[0]
    feats, tail = [], ""
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        m = re.match(r"#### (\d+)\w\w Level:\s*(.*)", head)
        # boxes ({{note …}}) at the end of the last feature belong to the subclass description
        bm = re.search(r"\n\{\{(note|descriptive)", body)
        if bm:
            tail += body[bm.start():]
            body = body[:bm.start()]
        feats.append((int(m.group(1)), m.group(2).strip(), body.strip()))
    return pre, feats, tail


WIZ_MD = section("# Wizard: School of Infernal Contracts", "# Paladin: Oath of the Infernal Lord")
PAL_MD = section("# Paladin: Oath of the Infernal Lord", "# Cleric: Contract Domain")
CLE_MD = section("# Cleric: Contract Domain", "{{partCover}}\n\n# PART VI")
SUB_INTRO_MD = section("## V. Infernal Subclasses", "# Wizard: School of Infernal Contracts")


SRD = "/home/claude/ref/dnd5e/packs/_source"
_SRD_CACHE = {}


def srd_spell_uuid(name):
    import glob, yaml
    if not _SRD_CACHE:
        for f in glob.glob(f"{SRD}/spells/**/*.yml", recursive=True):
            d = yaml.safe_load(open(f))
            _SRD_CACHE[d.get("name")] = f"Compendium.dnd5e.spells.Item.{d['_id']}"
    return _SRD_CACHE[name]


def mod_spell_uuid(key):
    return f"Compendium.{MOD}.spells.Item.{fid('spell:' + key)}"


def spell_uuid_by_name(n):
    """Spell names in subclass tables: module spells first, SRD otherwise."""
    for nm, k in SPELL_NAMES.items():
        if nm.lower() == n.lower():
            return mod_spell_uuid(k)
    return srd_spell_uuid(n.title().replace(" Of ", " of ").replace(" The ", " the "))


def cf(key, name, desc, *, img, cls, level, activities=None, uses_=None, effects=None, subtype=""):
    f = feat(key, name, desc, img=icon(img), activities=activities, uses_=uses_, ftype="class", subtype=subtype,
             effects=effects, req=f"{cls} {level}")
    f["flags"][MOD] = {"level": level}
    return f


def grant(level, items, title="Features", spell=None):
    return {"_id": fid(f"adv:{level}:{title}:{items[0]}")[:16], "type": "ItemGrant", "level": level, "title": title,
            "configuration": {"items": [{"uuid": u, "optional": False} for u in items], "optional": False,
                              "spell": spell or {"ability": [], "method": "", "prepared": 0,
                                                 "uses": {"max": "", "per": "", "requireSlot": False}}},
            "value": {}}


def opt_uuid(doc):
    return f"Compendium.{MOD}.options.Item.{doc['_id']}"


def ALWAYS(ab):
    return {"ability": [ab], "method": "spell", "prepared": 2, "uses": {"max": "", "per": "", "requireSlot": False}}


def spell_table(md_block, heading):
    """Rows (level, [spell names]) from a '### … Spells' table."""
    t = section(heading, "\n#", md_block)
    rows = []
    for ln in t.split("\n"):
        m = re.match(r"\|\s*(\d+)\w\w\s*\|\s*(.+?)\s*\|", ln.strip())
        if m:
            rows.append((int(m.group(1)), [x.strip().strip("*").strip() for x in m.group(2).split(",")]))
    return rows


def fbody(feats, name):
    return next(b for l, n, b in feats if n.startswith(name))


# ---- Wizard
W = "Wizard"
w_pre, w_feats, w_tail = features_from(WIZ_MD)
e_sigil = effect("sigil", "Contract Sigil", icon("sub-sigil"), duration={"seconds": 3600},
                 description="<p>Once on each of your turns, add the Contract Sigil die (d4, or d6 from a 10th-level binder) to "
                             "one damage roll or one saving throw. Knowingly violate the Term and the sigil shatters for 2d4 "
                             "psychic damage.</p>")
e_ward = effect("ward-cov", "Warding Covenant", icon("sub-ward"), duration={"seconds": 3600},
                changes=[("system.traits.dr.value", 2, "fire"), ("system.traits.dr.value", 2, "psychic")],
                description="<p>Resistance to fire and psychic damage while you bear the Contract Sigil.</p>")
w_runic = cf("w-runic", "Runic Drafting", md_html(fbody(w_feats, "Runic Drafting")), img="sub-rune", cls=W, level=2)
w_sigil = cf("w-sigil", "Contract Sigil", md_html(fbody(w_feats, "Contract Sigil")), img="sub-sigil", cls=W, level=2,
             effects=[e_sigil], uses_=uses("max(1, @abilities.int.mod)", ["lr"]),
             activities=[utility("w-sigil", 0, name="Place the Sigil", act=activation("bonus", 1),
                                 consumption=consume_item_uses(), roll=("1d(4 + 2 * floor(@classes.wizard.levels / 10))", "Sigil Die"),
                                 effects=[e_sigil["_id"]], tgt=target(1, "willing"), rng_=rng("", "touch")),
                         damage_act("w-sigil-shatter", 1, name="Sigil Shatters", parts=[dmg(2, 4, "", ["psychic"])],
                                    act=activation("special", None))])
w_ret = cf("w-retainer", "Devil's Retainer", md_html(fbody(w_feats, "Devil's Retainer")), img="sub-retainer", cls=W, level=6,
           uses_=uses(1, ["lr"]),
           activities=[utility("w-retainer", 0, name="Bind the Retainer (10 min)", act=activation("minute", 10)),
                       utility("w-retainer-obj", 1, name="Object! (disadvantage on the save)", act=activation("special", None),
                               consumption=consume_item_uses())])
w_auth = cf("w-authority", "Binding Authority", md_html(fbody(w_feats, "Binding Authority")), img="sub-authority", cls=W, level=6)
w_cov = cf("w-covenants", "Master of Covenants", md_html(fbody(w_feats, "Master of Covenants")), img="sub-ward", cls=W, level=10,
           effects=[e_ward],
           activities=[utility("w-ward", 0, name="Warding Covenant", effects=[e_ward["_id"]], act=activation("special", None)),
                       heal_act("w-consideration", 1, formula_part=dmg_formula("2 * @classes.wizard.levels", ["temphp"]),
                                name="Consideration (sigil shattered)", temp=True, act=activation("special", None))])
w_grand = cf("w-grand", "Grand Infernal Binding", md_html(fbody(w_feats, "Grand Infernal Binding")), img="sub-binding", cls=W,
             level=14, uses_=uses(1, ["lr"]),
             activities=[utility("w-grand", 0, name="Contract of Infernal Servitude (no slot)", consumption=consume_item_uses(),
                                 act=activation("hour", 1))])
WIZ_FEATURES = [w_runic, w_sigil, w_ret, w_auth, w_cov, w_grand]

SCHOOL = {"_id": fid("sub:school-infernal-contracts"), "name": "School of Infernal Contracts", "type": "subclass",
          "img": icon("sub-school"), "sort": 0, "folder": None, "effects": [], "flags": {}, "_stats": STATS,
          "system": {"description": {"value": md_html(section("*Wizards of this tradition", "#### ", WIZ_MD)), "chat": ""},
                     "source": SOURCE, "identifier": "school-of-infernal-contracts", "classIdentifier": "wizard",
                     "advancement": [grant(2, [opt_uuid(w_runic), opt_uuid(w_sigil)]),
                                     grant(2, [mod_spell_uuid("fine-print")], "Runic Drafting", spell=ALWAYS("int")),
                                     grant(6, [opt_uuid(w_ret), opt_uuid(w_auth)]), grant(10, [opt_uuid(w_cov)]),
                                     grant(14, [opt_uuid(w_grand)]),
                                     grant(14, [mod_spell_uuid("contract-of-infernal-servitude")], "Grand Infernal Binding",
                                           spell=ALWAYS("int"))],
                     "spellcasting": {"progression": "none", "ability": ""}}}

# ---- Paladin
PA = "Paladin"
p_pre, p_feats, p_tail = features_from(PAL_MD)
OATH_SPELLS = spell_table(PAL_MD, "### Oath Spells")
cd_body = fbody(p_feats, "Channel Divinity")
rebuke_md = re.search(r"\*\*Fiendish Rebuke\.\*\*.*?(?=\n:\n\*\*Fiendish Binding)", cd_body, re.S).group(0)
binding_md = re.search(r"\*\*Fiendish Binding\.\*\*.*", cd_body, re.S).group(0)
e_bound = effect("fiendish-binding", "Fiendish Binding", icon("sub-chains"), statuses=["restrained"], duration={"seconds": 60},
                 description="<p>Restrained by crackling infernal chains. Repeat the Wisdom save at the end of each of your turns. "
                             "From the paladin's 7th level you can't teleport, be teleported, or be returned to your home plane "
                             "while restrained this way.</p>")
e_aura = effect("aura-contract", "Aura of Contract", icon("sub-aura"), transfer=True, changes=[("system.traits.dr.value", 2, "fire")],
                description="<p>You and friendly creatures within 10 feet (30 feet at 18th level) have resistance to fire damage.</p>")
e_avatar = effect("avatar-lord", "Avatar of the Infernal Lord", icon("sub-avatar"), duration={"seconds": 60},
                  changes=[("system.attributes.movement.fly", 4, "@attributes.movement.walk")],
                  description="<p>Horns, blazing eyes and a 30-foot aura of hellfire for 1 minute. Flying speed equal to your walking "
                              "speed; fiends have disadvantage on saves against your spells and Channel Divinity; you can't be "
                              "charmed or frightened.</p>")
tenets_md = section("### Tenets of the Infernal Lord", "#### ", PAL_MD)
p_ten = cf("p-tenets", "Tenets of the Infernal Lord", md_html(tenets_md), img="sub-oath", cls=PA, level=3)
p_reb = cf("p-rebuke", "Channel Divinity: Fiendish Rebuke", md_html(rebuke_md), img="sub-rebuke", cls=PA, level=3,
           subtype="channelDivinity",
           activities=[save("p-rebuke", 0, ability="dex", spell=True, act=activation("reaction", 1), rng_=rng(60),
                            tgt=target(1, "creature"),
                            parts=[dmg_formula("(1 + floor((@classes.paladin.levels + 3) / 6))d10", ["fire"])],
                            name="Fiendish Rebuke")])
p_bin = cf("p-binding", "Channel Divinity: Fiendish Binding", md_html(binding_md), img="sub-chains", cls=PA, level=3,
           subtype="channelDivinity", effects=[e_bound],
           activities=[save("p-binding", 0, ability="wis", spell=True, on_save="none", rng_=rng(30), tgt=target(1, "creature"),
                            effects=[e_bound["_id"]], name="Fiendish Binding")])
p_aura = cf("p-aura", "Aura of Contract", md_html(fbody(p_feats, "Aura of Contract")), img="sub-aura", cls=PA, level=7,
            effects=[e_aura])
p_unb = cf("p-unbreakable", "Unbreakable Pact", md_html(fbody(p_feats, "Unbreakable Pact")), img="sub-pact", cls=PA, level=15,
           uses_=uses("@prof", ["lr"]),
           activities=[utility("p-unbreak", 0, name="Impose Disadvantage", act=activation("reaction", 1),
                               consumption=consume_item_uses())])
p_ava = cf("p-avatar", "Avatar of the Infernal Lord", md_html(fbody(p_feats, "Avatar")), img="sub-avatar", cls=PA, level=20,
           uses_=uses(1, ["lr"]), effects=[e_avatar],
           activities=[utility("p-avatar", 0, name="Assume the Aspect", consumption=consume_item_uses(), effects=[e_avatar["_id"]]),
                       save("p-avatar-chains", 1, ability="wis", spell=True, on_save="none", act=activation("special", None),
                            name="Infernal Chains", tgt=target(1, "creature")),
                       damage_act("p-avatar-fire", 2, name="Hellfire Blast", parts=[dmg(4, 6, "", ["fire"])],
                                  act=activation("special", None))])
PAL_FEATURES = [p_ten, p_reb, p_bin, p_aura, p_unb, p_ava]
oath_adv = [grant(3, [opt_uuid(p_ten), opt_uuid(p_reb), opt_uuid(p_bin)]), grant(7, [opt_uuid(p_aura)]),
            grant(15, [opt_uuid(p_unb)]), grant(20, [opt_uuid(p_ava)])]
for lvl, names in OATH_SPELLS:
    oath_adv.append(grant(lvl, [spell_uuid_by_name(n) for n in names], "Oath Spells", spell=ALWAYS("cha")))
OATH = {"_id": fid("sub:oath-infernal-lord"), "name": "Oath of the Infernal Lord", "type": "subclass",
        "img": icon("sub-oath"), "sort": 0, "folder": None, "effects": [], "flags": {}, "_stats": STATS,
        "system": {"description": {"value": md_html(section('*"By iron and flame', "#### ", PAL_MD)) + md_html(p_tail)
                                   + "<p><em>In The Night of the Red Clause this oath belongs to the Red Clause's enforcers and to "
                                     "anyone the party meets who signed the Ninth Court's terms. With DM approval it suits an "
                                     "antihero who means to beat Hell at its own law.</em></p>", "chat": ""},
                   "source": SOURCE, "identifier": "oath-of-the-infernal-lord", "classIdentifier": "paladin",
                   "advancement": oath_adv, "spellcasting": {"progression": "none", "ability": ""}}}

# ---- Cleric
CL = "Cleric"
c_pre, c_feats, c_tail = features_from(CLE_MD)
DOMAIN_SPELLS = spell_table(CLE_MD, "### Contract Domain Spells")
e_arrears = effect("in-arrears", "In Arrears", icon("sub-audit"), duration={"seconds": 60},
                   description="<p>Declared In Arrears by an Infernal Audit: you can't regain hit points, and the first time on "
                               "each of the cleric's turns that the cleric or an ally damages you, you take an extra 1d8 necrotic "
                               "damage.</p>")
e_writ = effect("writ-compulsion", "Writ of Compulsion", icon("sub-writ"), duration={"seconds": 60},
                description="<p>Bound by a writ: one named action is forbidden. Attempting it fails, wastes the action and deals "
                            "psychic damage (2d10, 3d10 from 8th level, 4d10 from 14th). Repeat the Wisdom save at the end of each "
                            "of your turns.</p>")
c_prof = cf("c-prof", "Bonus Proficiencies", md_html(fbody(c_feats, "Bonus Proficiencies")), img="sub-domain", cls=CL, level=1,
            effects=[effect("c-prof", "Contract Domain Proficiencies", icon("sub-domain"), transfer=True,
                            changes=[("system.traits.armorProf.value", 2, "hvy"), ("system.traits.languages.value", 2, "infernal")],
                            description="<p>Heavy armour proficiency and the Infernal language.</p>")])
c_not = cf("c-notary", "Notary of the Nine", md_html(fbody(c_feats, "Notary of the Nine")), img="sub-notary", cls=CL, level=1,
           uses_=uses("max(1, @abilities.wis.mod)", ["lr"]),
           activities=[heal_act("c-notary", 0, formula_part=dmg_formula("@classes.cleric.levels", ["temphp"]), name="Offer a Minor Term",
                                temp=True, act=activation("bonus", 1), consumption=consume_item_uses(), rng_=rng(30),
                                tgt=target(1, "creature")),
                       damage_act("c-notary-break", 1, name="Term Broken", parts=[dmg(1, 8, "@abilities.wis.mod", ["psychic"])],
                                  act=activation("special", None))])
c_writ = cf("c-writ", "Channel Divinity: Writ of Compulsion", md_html(fbody(c_feats, "Channel Divinity — Writ")), img="sub-writ",
            cls=CL, level=2, subtype="channelDivinity", effects=[e_writ],
            activities=[save("c-writ", 0, ability="wis", spell=True, on_save="none", rng_=rng(30), tgt=target(1, "creature"),
                             effects=[e_writ["_id"]], name="Read the Writ"),
                        damage_act("c-writ-b", 1, name="Forbidden Action Attempted", act=activation("special", None),
                                   parts=[dmg_formula("(1 + floor((@classes.cleric.levels + 4) / 6))d10", ["psychic"])])])
c_aud = cf("c-audit", "Channel Divinity: Infernal Audit", md_html(fbody(c_feats, "Channel Divinity — Infernal")), img="sub-audit",
           cls=CL, level=6, subtype="channelDivinity", effects=[e_arrears],
           activities=[utility("c-audit", 0, name="Open Hell's Books (1 minute)"),
                       utility("c-arrears", 1, name="Declare In Arrears", act=activation("bonus", 1), effects=[e_arrears["_id"]],
                               rng_=rng(60), tgt=target(1, "creature")),
                       damage_act("c-arrears-d", 2, name="In Arrears (extra damage)", parts=[dmg(1, 8, "", ["necrotic"])],
                                  act=activation("special", None))])
c_lien = cf("c-lien", "Divine Strike: Hellfire Lien", md_html(fbody(c_feats, "Divine Strike")), img="sub-lien", cls=CL, level=8,
            activities=[damage_act("c-lien", 0, name="Hellfire Lien", act=activation("special", None),
                                   parts=[dmg_formula("(1 + floor(@classes.cleric.levels / 14))d8", ["fire"])]),
                        damage_act("c-lien-n", 1, name="Hellfire Lien (bound target)", act=activation("special", None),
                                   parts=[dmg_formula("(1 + floor(@classes.cleric.levels / 14))d8", ["necrotic"])])])
c_mas = cf("c-master", "Master of the Ledger", md_html(fbody(c_feats, "Master of the Ledger")), img="sub-ledgermaster", cls=CL,
           level=17, uses_=uses(1, ["lr"]),
           activities=[save("c-foreclose", 0, ability="cha", spell=True, act=activation("reaction", 1), rng_=rng(60),
                            tgt=target(1, "creature"), parts=[dmg(8, 10, "", ["psychic"])], name="Foreclosure",
                            consumption=consume_item_uses()),
                       utility("c-sealed", 1, name="Sealed Covenant (soul covenant, no slot)", act=activation("minute", 1))])
CLE_FEATURES = [c_prof, c_not, c_writ, c_aud, c_lien, c_mas]
dom_adv = [grant(1, [opt_uuid(c_prof), opt_uuid(c_not)]), grant(2, [opt_uuid(c_writ)]), grant(6, [opt_uuid(c_aud)]),
           grant(8, [opt_uuid(c_lien)]), grant(17, [opt_uuid(c_mas)])]
for lvl, names in DOMAIN_SPELLS:
    dom_adv.append(grant(lvl, [spell_uuid_by_name(n) for n in names], "Domain Spells", spell=ALWAYS("wis")))
DOMAIN = {"_id": fid("sub:contract-domain"), "name": "Contract Domain", "type": "subclass",
          "img": icon("sub-domain"), "sort": 0, "folder": None, "effects": [], "flags": {}, "_stats": STATS,
          "system": {"description": {"value": md_html(section("*The Contract Domain serves", "#### ", CLE_MD)) + md_html(c_tail),
                                     "chat": ""},
                     "source": SOURCE, "identifier": "contract-domain", "classIdentifier": "cleric",
                     "advancement": dom_adv, "spellcasting": {"progression": "none", "ability": ""}}}

FEATURES = WIZ_FEATURES + PAL_FEATURES + CLE_FEATURES
SUBCLASSES = [SCHOOL, OATH, DOMAIN]
