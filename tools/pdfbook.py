"""DMs Guild PDFs: Book I (GM), Book II (Player's Guide) and the claimant sheets."""
import html as html_mod
import sys, os, re, json, math, copy, shutil
sys.path.insert(0, "/home/claude/ic/src")
from lib5e import fid, MOD
import sheets as SHEETS
from blocks import SCRIPTORIUM_ITEMS
import bestiary as B, items as IT, spells as SP, playeroptions as PO, pregens as PG, tables as TB
import j_toolkit, j_book1, j_book2, j_rest, j_scriptorium, jhelp
from PIL import Image

ROOT = "/home/claude/ic"
W = f"{ROOT}/build/pdf"
shutil.rmtree(W, ignore_errors=True)
os.makedirs(f"{W}/img", exist_ok=True)
ASSETS = f"{ROOT}/module/assets"
SKILL = {"acrobatics": ("Dexterity", "Acrobatics"), "animal-handling": ("Wisdom", "Animal Handling"), "arcana": ("Intelligence", "Arcana"),
         "athletics": ("Strength", "Athletics"), "deception": ("Charisma", "Deception"), "history": ("Intelligence", "History"),
         "insight": ("Wisdom", "Insight"), "intimidation": ("Charisma", "Intimidation"), "investigation": ("Intelligence", "Investigation"),
         "medicine": ("Wisdom", "Medicine"), "nature": ("Intelligence", "Nature"), "perception": ("Wisdom", "Perception"),
         "performance": ("Charisma", "Performance"), "persuasion": ("Charisma", "Persuasion"), "religion": ("Intelligence", "Religion"),
         "sleight-of-hand": ("Dexterity", "Sleight of Hand"), "stealth": ("Dexterity", "Stealth"), "survival": ("Wisdom", "Survival")}
SKK = {"acr": "Acrobatics", "ani": "Animal Handling", "arc": "Arcana", "ath": "Athletics", "dec": "Deception", "his": "History",
       "ins": "Insight", "itm": "Intimidation", "inv": "Investigation", "med": "Medicine", "nat": "Nature", "prc": "Perception",
       "prf": "Performance", "per": "Persuasion", "rel": "Religion", "slt": "Sleight of Hand", "ste": "Stealth", "sur": "Survival"}
SKA = {"acr": "dex", "ani": "wis", "arc": "int", "ath": "str", "dec": "cha", "his": "int", "ins": "wis", "itm": "cha", "inv": "int",
       "med": "wis", "nat": "int", "prc": "wis", "prf": "cha", "per": "cha", "rel": "int", "slt": "dex", "ste": "dex", "sur": "wis"}
ABIL = {"strength": "Strength", "dexterity": "Dexterity", "constitution": "Constitution", "intelligence": "Intelligence",
        "wisdom": "Wisdom", "charisma": "Charisma", "str": "Strength", "dex": "Dexterity", "con": "Constitution", "int": "Intelligence",
        "wis": "Wisdom", "cha": "Charisma"}
_SC_ALL = json.load(open("/home/claude/ic/module/data/scenes.json"))["scenes"]
_REUSE = {sc["key"]: sc["src"].rsplit("/", 1)[1].rsplit(".", 1)[0] for sc in _SC_ALL
          if sc["src"].rsplit("/", 1)[1].rsplit(".", 1)[0] != sc["key"]}
_SC = [sc for sc in _SC_ALL if sc["key"] not in _REUSE]
MAPNO = {sc["key"]: i for i, sc in enumerate(_SC, 1)}
MAPNO.update({k: MAPNO[v] for k, v in _REUSE.items()})
MAPTITLE = {sc["key"]: sc["title"].split(" · ", 1)[1] for sc in _SC_ALL}
SCENE_BY_ID = {fid("scene:" + k): k for k in MAPNO}


def img(src_rel, size=600, fmt="JPEG"):
    """Copy a module asset to a print-ready file; returns local path."""
    p = src_rel.split(MOD + "/", 1)[1] if MOD in src_rel else src_rel
    src = f"{ROOT}/module/{p}"
    name = p.replace("/", "_").rsplit(".", 1)[0] + (".jpg" if fmt == "JPEG" else ".png")
    out = f"{W}/img/{name}"
    if not os.path.exists(out):
        im = Image.open(src)
        im = im.convert("RGB") if fmt == "JPEG" else im.convert("RGBA")
        im.thumbnail((size, size))
        im.save(out, fmt, quality=88)
    return out


def avg(formula):
    f = formula.replace(" ", "")
    m = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", f)
    if not m:
        return None
    n, d, b = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    return int(n * (d + 1) / 2 + b)


def dmgtxt(formula, typ=""):
    a = avg(formula)
    f = re.sub(r"\s*([+-])\s*", r" \1 ", formula.strip())
    if a is None:
        return f"{f}{(' ' + typ) if typ else ''} damage"
    return f"{a} ({f}){(' ' + typ) if typ else ''} damage"


def check_txt(cfg):
    toks = cfg.split()
    dc = next((t for t in toks if t.isdigit()), None)
    names = [t for t in toks if not t.isdigit()]
    parts = []
    for t in names:
        if t in SKILL:
            a, s = SKILL[t]
            parts.append(f"{a} ({s})")
        elif t in ABIL:
            parts.append(ABIL[t])
    return f"<b>DC {dc}</b> " + " or ".join(parts) + " check"


def enrich(html, ctx=None):
    def rep(m):
        kind, cfg = m.group(1), (m.group(2) or "").strip()
        if kind == "check":
            return check_txt(cfg)
        if kind == "save":
            if not cfg and ctx:
                return ctx.get("save", "saving throw").replace(" saving throw", "")
            toks = cfg.split()
            return f"<b>DC {toks[-1]}</b> {ABIL.get(toks[0], toks[0].title())} saving throw"
        if kind in ("damage", "heal"):
            if cfg.startswith("extended") or not cfg:
                return ctx.get("damage", "damage") if ctx else "damage"
            cfg = cfg.replace("average", "").strip()
            typ = ""
            mt = re.search(r"type=(\w+)", cfg)
            if mt:
                typ = mt.group(1); cfg = cfg.replace(mt.group(0), "").strip()
            else:
                toks = cfg.split()
                if toks and toks[-1].isalpha():
                    typ = toks[-1]; cfg = " ".join(toks[:-1])
            if kind == "heal":
                a = avg(cfg)
                return (f"{a} ({cfg})" if a is not None else cfg) + (" temporary" if typ == "temphp" else "")
            return dmgtxt(cfg, typ)
        if kind == "attack":
            return ctx.get("attack", "") if ctx else ""
        if kind == "roll":
            return cfg
        return cfg
    html = re.sub(r"\[\[/(\w+)([^\]]*)\]\]", rep, html)
    html = re.sub(r"(one target), ((?:reach|range) [^,]{1,20}?, one target)", r"\1", html)
    html = re.sub(r"((?:reach|range) [\d/]+ ft\., one target), (?:reach|range) [\d/]+ ft\., one target", r"\1", html)
    html = re.sub(r"&Reference\[([^\]]+)\]", lambda m: f"<i>{m.group(1)}</i>", html)

    def uu(m):
        u, label = m.group(1), m.group(2) or ""
        if u.startswith("Scene."):
            k = SCENE_BY_ID.get(u.split(".")[1])
            return f"<span class='xref'>{label}</span> <span class='mapref'>(Plate {MAPNO[k]})</span>"
        if ".macros." in u:
            return f"<span class='vtt'>{label}</span>"
        if ".tables." in u:
            return f"<span class='xref'>{label}</span> table (Appendix B)"
        if ".actors." in u:
            return f"<span class='xref'>{label}</span>"
        return f"<span class='xref'>{label}</span>"
    html = re.sub(r"@UUID\[([^\]]+)\](?:\{([^}]*)\})?", uu, html)
    html = html.replace("modules/" + MOD + "/assets/", ASSETS + "/")
    return html


# ---------------------------------------------------------------------------- stat blocks
XP = {0: 10, 0.125: 25, 0.25: 50, 0.5: 100, 1: 200, 2: 450, 3: 700, 4: 1100, 5: 1800, 6: 2300, 7: 2900, 8: 3900,
      9: 5000, 10: 5900, 11: 7200, 12: 8400, 13: 10000, 14: 11500, 15: 13000}


def pb(cr):
    return 2 if cr < 5 else 3 if cr < 9 else 4 if cr < 13 else 5


def mod(v):
    return (v - 10) // 2


def sgn(n):
    return f"+{n}" if n >= 0 else str(n)


def part_txt(p):
    if p.get("custom", {}).get("enabled"):
        f = p["custom"]["formula"]
        return f"{f} {p['types'][0]} damage" if p["types"] else f
    f = f"{p['number']}d{p['denomination']}" + (f" + {p['bonus']}" if str(p['bonus']) not in ("", "0") else "")
    return dmgtxt(f, p["types"][0] if p["types"] else "")


def feat_ctx(it):
    ctx = {}
    acts = list(it["system"]["activities"].values())
    for a in acts:
        if a["type"] == "attack" and "attack" not in ctx:
            rngv = a["range"].get("value", "")
            kind = a["attack"]["type"]["value"]
            cls = a["attack"]["type"]["classification"]
            lab = ("Melee" if kind == "melee" else "Ranged") + (" Spell" if cls == "spell" else " Weapon")
            reach = f"reach {rngv} ft." if kind == "melee" else f"range {rngv} ft."
            ctx["attack"] = f"{sgn(int(a['attack']['bonus']))} to hit, {reach}, one target"
            ctx["damage"] = " plus ".join(part_txt(p) for p in a["damage"]["parts"])
        if a["type"] == "save" and "save" not in ctx:
            ctx["save"] = f"<b>DC {a['save']['dc']['formula']}</b> {ABIL[a['save']['ability'][0]]} saving throw"
            if a["damage"]["parts"] and "damage" not in ctx:
                ctx["damage"] = " plus ".join(part_txt(p) for p in a["damage"]["parts"])
        if a["type"] == "damage" and "damage" not in ctx:
            ctx["damage"] = " plus ".join(part_txt(p) for p in a["damage"]["parts"])
        if a["type"] == "heal":
            ctx["damage"] = part_txt(a["healing"]).replace(" healing damage", "").replace("damage", "")
    return ctx


def feat_section(it):
    acts = list(it["system"]["activities"].values())
    t = acts[0]["activation"]["type"] if acts else ""
    n = it["name"]
    if n == "Legendary Actions":
        return "legintro"
    if n.startswith("Lair Action"):
        return "lair"
    if t == "legendary":
        return "legendary"
    if t == "bonus" or "Bonus Action" in it["system"]["description"]["value"][:60]:
        return "bonus"
    if t == "reaction" or "<strong>Reaction</strong>" in it["system"]["description"]["value"][:40]:
        return "reaction"
    if t == "action":
        return "action"
    return "trait"


def vehicle_block(a):
    s = a["system"]
    at, tr, ab = s["attributes"], s["traits"], s["abilities"]
    size = {"lg": "Large", "huge": "Huge", "grg": "Gargantuan"}[tr["size"]]
    out = [f'<div class="statblock"><h4 class="sb-name">{a["name"]}</h4><p class="sb-type"><i>{size} vehicle (land)</i></p><hr>',
           f"<p><b>Armor Class</b> {at['ac']['flat']}</p>",
           f"<p><b>Hit Points</b> {at['hp']['max']} (damage threshold {at['hp']['dt']}, mishap threshold {at['hp']['mt']})</p>",
           f"<p><b>Speed</b> {at['movement']['walk']} ft.</p><hr>",
           '<table class="sb-ab"><tr>' + "".join(f"<th>{k.upper()}</th>" for k in ("str", "dex", "con", "int", "wis", "cha")) + "</tr><tr>"
           + "".join(f"<td>{ab[k]['value']} ({sgn(mod(ab[k]['value']))})</td>" if ab[k]["value"] else "<td>0 (−5)</td>"
                     for k in ("str", "dex", "con", "int", "wis", "cha")) + "</tr></table><hr>",
           f"<p><b>Damage Immunities</b> {', '.join(tr['di']['value'])}</p>",
           f"<p><b>Condition Immunities</b> {', '.join(tr['ci']['value'])}</p>",
           f"<p><b>Capacity</b> {at['capacity']['creature']}</p><p><b>Stations</b> {tr['dimensions']}</p><hr>"]
    for it in a["items"]:
        d = enrich(it["system"]["description"]["value"], feat_ctx(it))
        out.append(re.sub(r"^<p>", f"<p><b><i>{it['name']}.</i></b> ", d, count=1))
    out.append("</div>")
    return "".join(out)


def statblock(a):
    if a["type"] == "vehicle":
        return vehicle_block(a)
    s = a["system"]
    cr = s["details"]["cr"]
    p = pb(cr)
    ab = s["abilities"]
    crs = {0.125: "1/8", 0.25: "1/4", 0.5: "1/2"}.get(cr, str(int(cr)) if cr == int(cr) else str(cr))
    size = {"tiny": "Tiny", "sm": "Small", "med": "Medium", "lg": "Large", "huge": "Huge", "grg": "Gargantuan"}[s["traits"]["size"]]
    typ = s["details"]["type"]["value"] + (f" ({s['details']['type']['subtype']})" if s["details"]["type"]["subtype"] else "")
    mv = s["attributes"]["movement"]
    spd = [f"{mv['walk']} ft."] + [f"{k} {mv[k]} ft." + (" (hover)" if k == "fly" and mv.get("hover") else "") for k in ("fly", "climb", "swim") if mv.get(k)]
    saves = ", ".join(f"{k.title()} {sgn(mod(ab[k]['value']) + p)}" for k in ("str", "dex", "con", "int", "wis", "cha") if ab[k].get("proficient"))
    skills = ", ".join(f"{SKK[k]} {sgn(mod(ab[SKA[k]]['value']) + p * v['value'])}" for k, v in sorted(s.get("skills", {}).items(), key=lambda x: SKK[x[0]]))
    tr = s["traits"]
    se = s["attributes"]["senses"]
    senses = [f"{k} {se[k]} ft." for k in ("blindsight", "darkvision", "truesight") if se.get(k)]
    pp = 10 + mod(ab["wis"]["value"]) + (p * s.get("skills", {}).get("prc", {}).get("value", 0))
    senses.append(f"passive Perception {pp}")
    langs = ", ".join([l.title() for l in tr["languages"]["value"]] + ([tr["languages"]["custom"]] if tr["languages"]["custom"] else [])) or "—"
    hp = s["attributes"]["hp"]
    rows = [("Armor Class", f"{s['attributes']['ac']['flat'] or 10}"), ("Hit Points", f"{hp['max']}" + (f" ({hp['formula']})" if hp.get("formula") else "")),
            ("Speed", ", ".join(spd))]
    long_ = len(a["items"]) > 9
    out = [f'<div class="statblock{" long" if long_ else ""}"><h4 class="sb-name">{a["name"]}</h4><p class="sb-type"><i>{size} {typ}, {s["details"]["alignment"].lower()}</i></p><hr>']
    out += [f"<p><b>{k}</b> {v}</p>" for k, v in rows] + ["<hr>"]
    out.append('<table class="sb-ab"><tr>' + "".join(f"<th>{k.upper()}</th>" for k in ab) + "</tr><tr>" +
               "".join(f"<td>{v['value']} ({sgn(mod(v['value']))})</td>" for v in ab.values()) + "</tr></table><hr>")
    for k, v in [("Saving Throws", saves), ("Skills", skills),
                 ("Damage Vulnerabilities", ", ".join(tr["dv"]["value"])),
                 ("Damage Resistances", ", ".join(tr["dr"]["value"]) + (f" {tr['dr']['custom']}" if tr["dr"].get("custom") else "")),
                 ("Damage Immunities", ", ".join(tr["di"]["value"])), ("Condition Immunities", ", ".join(tr["ci"]["value"])),
                 ("Senses", ", ".join(senses)), ("Languages", langs)]:
        if v.strip():
            out.append(f"<p><b>{k}</b> {v}</p>")
    out.append(f"<p><b>Challenge</b> {crs} ({XP.get(cr, 0):,} XP) &nbsp; <b>Proficiency Bonus</b> +{p}</p><hr>")
    secs = {k: [] for k in ("trait", "action", "bonus", "reaction", "legintro", "legendary", "lair")}
    for it in a["items"]:
        secs[feat_section(it)].append(it)
    head = {"action": "Actions", "bonus": "Bonus Actions", "reaction": "Reactions", "legendary": "Legendary Actions", "lair": "Lair Actions"}

    def body(it):
        d = enrich(it["system"]["description"]["value"], feat_ctx(it))
        d = re.sub(r"^<p>(?:<strong>|<b>)" + re.escape(it["name"]) + r"\.?(?:</strong>|</b>)\.?\s*", "<p>", d, count=1)
        d = re.sub(r"^<p>", f"<p><b><i>{it['name']}.</i></b> ", d, count=1)
        return d
    out += [body(i) for i in secs["trait"]]
    for k in ("action", "bonus", "reaction", "legendary", "lair"):
        if secs[k] or (k == "legendary" and secs["legintro"]):
            out.append(f'<h5 class="sb-sec">{head[k]}</h5>')
            if k == "legendary":
                out += [enrich(i["system"]["description"]["value"]) for i in secs["legintro"]]
            if k == "lair":
                out.append("<p>On initiative count 20 (losing initiative ties), choose one of these, not all of them.</p>")
            out += [body(i) for i in secs[k]]
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------------------- spells / items
SCHOOL = {"abj": "abjuration", "con": "conjuration", "div": "divination", "enc": "enchantment", "evo": "evocation",
          "ill": "illusion", "nec": "necromancy", "trs": "transmutation"}
ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}
ORD_ = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th", 8: "8th", 9: "9th"}


def spellblock(s):
    from blocks import spell_type, spell_lines
    y = s["system"]
    lvl = spell_type(s)
    if s["flags"][MOD]["group"] == "Asmodeun Scriptorium":
        lvl = lvl.replace(" (ritual)", " (ritual, infernal)") if "(ritual)" in lvl else lvl + " (infernal)"
    lines = "<br>".join(f"<b>{k}:</b> {v}" for k, v in spell_lines(s))
    return (f'<div class="spell"><h4>{s["name"]}</h4><p class="sp-type"><i>{lvl}</i></p>'
            f"<p>{lines}</p>{enrich(y['description']['value'])}</div>")


def itemblock(i):
    y = i["system"]
    kind = {"consumable": "Wondrous item (consumable)", "equipment": "Wondrous item", "loot": "Document / curio",
            "container": "Wondrous item", "weapon": "Weapon (whip)"}[i["type"]]
    rar = y.get("rarity", "")
    att = f" (requires attunement{' ' + y['attunement'].replace('required', '').strip() if y.get('attunement') not in ('', 'required') else ''})" if y.get("attunement") else ""
    meta = f"{kind}{', ' + rar if rar else ''}{att}"
    return f'<div class="item"><h4>{i["name"]}</h4><p class="sp-type"><i>{meta}</i></p>{enrich(y["description"]["value"])}</div>'


# ---------------------------------------------------------------------------- pregens
AC = {"marigold": (21, "plate, +1 shield"), "hesper": (16, "mage armor, cloak of protection"), "bramwell": (21, "plate, shield, Defense"),
      "dorn": (19, "plate, Defense"), "pip": (18, "+1 studded leather"), "fennick": (15, "studded leather")}
SLOTS = {"Cleric": "4 / 3 / 3 / 3 / 2 / 1", "Wizard": "4 / 3 / 3 / 3 / 2 / 1", "Bard": "4 / 3 / 3 / 3 / 2 / 1", "Paladin": "4 / 3 / 3"}
CAST = {"Cleric": "wis", "Wizard": "int", "Paladin": "cha", "Bard": "cha"}


def pregen_sheet(p, a):
    sv = PG.SAVES[p["cls"]]
    ab = dict(zip(("str", "dex", "con", "int", "wis", "cha"), p["abilities"]))
    jack = p["cls"] == "Bard"
    sk = []
    for k in sorted(SKK, key=lambda k: SKK[k]):
        v = p["skills"].get(k, 0)
        bonus = mod(ab[SKA[k]]) + (4 * v if v else (2 if jack else 0))
        if v:
            sk.append(f"{SKK[k]} {sgn(bonus)}{'*' if v == 2 else ''}")
    feats = [i["name"] for i in a["items"] if i["type"] == "feat"]
    spells = {}
    for i in a["items"]:
        if i["type"] == "spell":
            spells.setdefault(i["system"]["level"], []).append(i["name"] + (" †" if i["system"].get("prepared") == 2 else ""))
    hp = a["flags"][MOD]["expectedHp"]
    speed = 25 if p["race"] in ("Hill Dwarf", "Lightfoot Halfling") else 30
    out = [f'<section class="pregen" style="--pc:{p["color"]}"><img class="pc-portrait" src="{img("assets/portraits/pc-" + p["key"] + ".webp")}">'
           f'<h2>{p["name"]}</h2><p class="pc-sub">{p["title"]} · {p["race"]} {p["cls"]} 11 ({p["sub"]}) · {p["align"]}</p>'
           '<table class="sb-ab pc-ab"><tr>' + "".join(f"<th>{k.upper()}</th>" for k in ab) + "</tr><tr>" +
           "".join(f"<td>{v}<br><b>{sgn(mod(v))}</b></td>" for v in ab.values()) + "</tr></table>"
           f'<p class="pc-line"><b>AC</b> {AC[p["key"]][0]} ({AC[p["key"]][1]}) · <b>HP</b> {hp} · <b>Speed</b> {speed} ft. · <b>Proficiency</b> +4 · <b>Initiative</b> {sgn(mod(ab["dex"]))}</p>'
           f'<p><b>Saving Throws</b> ' + ", ".join(f"{ABIL[k]} {sgn(mod(ab[k]) + (4 if k in sv else 0))}" for k in ab) + "</p>"
           f'<p><b>Skills</b> {", ".join(sk)}{" (* expertise)" if any("*" in s for s in sk) else ""}</p>']
    if p["cls"] in CAST:
        cm = mod(ab[CAST[p["cls"]]])
        out.append(f'<p><b>Spellcasting</b> save DC {8 + 4 + cm}, spell attack {sgn(4 + cm)} · slots {SLOTS[p["cls"]]}</p>')
    out.append(f'<p><b>Features</b> {", ".join(feats)}</p>')
    if spells:
        out.append("<p><b>Spells</b> " + " ".join(f"<i>{'Cantrips' if l == 0 else ORD.get(l, str(l))}:</i> {', '.join(sorted(n))}." for l, n in sorted(spells.items())) + " († always prepared)</p>")
    out.append(f'<p><b>Gear</b> {", ".join(g[0] for g in p["gear"])}; 250 gp.</p>')
    out += [f"<p>{b}</p>" for b in p["bio"]]
    out.append("</section>")
    return "".join(out)


# ---------------------------------------------------------------------------- assemble
docs = {j["flags"][MOD]["key"]: j for j in jhelp.build_docs()}


def pages(jkey, skip=()):
    return [(p["flags"][MOD]["key"], p["name"], re.sub(r'<p class="ipc-chapart">.*?</p>', "", p["text"]["content"])) for p in docs[jkey]["pages"] if p["flags"][MOD]["key"] not in skip]


def strip_wrapper(h):
    return re.sub(r'^<div class="rc-journal[^"]*">|</div>$', "", h)



def drop_dup_titles(h):
    """The chapter opener already prints the chapter's title; drop a manuscript heading that only repeats it."""
    out, pos = [], 0
    for m in re.finditer(r'<h1 class="chapter"[^>]*>.*?<span class="ct">(.*?)</span>.*?</h1>', h, flags=re.S):
        title = html_mod.unescape(re.sub("<[^>]+>", "", m.group(1))).strip()
        out.append(h[pos:m.end()]); pos = m.end()
        nxt = re.compile(r'<h2[^>]*>(?:\d+\. )?([^<]*)</h2>').search(h, pos, pos + 3000)
        if nxt and html_mod.unescape(nxt.group(1)).strip().lower() == title.lower():
            out.append(h[pos:nxt.start()]); pos = nxt.end()
    out.append(h[pos:])
    return "".join(out)


def chapter(cid, title, kicker=""):
    art = f"{ROOT}/module/assets/art/chapters/{cid}.webp"
    pic = (f'<span class="chapart"><img src="{img(f"modules/{MOD}/assets/art/chapters/{cid}.webp", 1600)}"></span>'
           if os.path.exists(art) else "")
    return f'<h1 class="chapter" id="{cid}"><span class="kick">{kicker}</span><span class="ct">{title}</span>{pic}</h1>'


TOC = []
H = []


def jp(jkey):
    return {k: (t, h) for k, t, h in pages(jkey)}


B1 = jp("book1")


def sect(h, title):
    h = strip_wrapper(h)
    h = re.sub(r'<div class="rc-box rc-box rc-(scenes|tools)">.*?</div>', "", h, flags=re.S)
    h = re.sub(r'<div class="rc-box rc-(scenes|tools)">.*?</div>', "", h, flags=re.S)
    if not h.lstrip().startswith(("<header", "<h2")):
        h = f"<h2>{title}</h2>" + h
    return f'<section class="sect">{enrich(h)}</section>'


book_sections = [("intro", "Introduction", ["overview"]),
                 ("run", "Running the Championship", ["running", "bridge", "audit"]),
                 ("ch1", "Chapter I — Dead Already", ["ch1", "map1", "map2"]),
                 ("ch2", "Chapter II — The Fallen", ["ch2", "map3", "map4", "map5"]),
                 ("interlude", "Interlude — The Redline Run", ["souljack-yard", "redline", "soulforged-gm"]),
                 ("ch3", "Chapter III — The War of Claims", ["ch3", "s8", "s9", "s10", "s11"]),
                 ("ch4", "Chapter IV — Blood and Brass", ["ch4", "s12", "s13", "s14", "s15"]),
                 ("ch5", "Chapter V — The Hag Queen's Due", ["ch5", "s16", "s17", "s18", "s19"]),
                 ("ch6", "Chapter VI — The Rite of the Nine", ["ch6", "s20", "s21", "s23", "s24"]),
                 ("ref", "Running the Table", ["procedure", "charter-ref", "design-audit"])]
for cid, title, keys in book_sections:
    TOC.append((cid, title))
    H.append(chapter(cid, title, "Chapter" if cid.startswith("ch") else ("Interlude" if cid == "interlude" else "")))
    for k in keys:
        t, h = B1[k]
        if k == "overview":
            h = re.sub(r"<h2>Contents</h2>.*?</table>", "", h, flags=re.S)
            h = re.sub(r"<h2>Getting Started</h2>.*$", "", h, flags=re.S)
            h += ('<div class="rc-box"><h4>Using This Book</h4><p>Read-aloud text appears in crimson boxes. Creature statistics are in '
                  'Appendix A, the arena engine and roll tables in Appendix B, handouts and contract forms in Appendix C, the '
                  'twenty-two maps in Appendix D, record sheets in Appendix E, and the design audit in Appendix F. The six '
                  'pregenerated claimants, the subclasses, spells and relics are in Book II. Names in <span class="vtt">this '
                  'style</span> are tools automated in the free Foundry VTT companion module; at any other table, run them by hand.</p></div></div>')
        H.append(sect(h, t))
# Appendix A: creatures
TOC.append(("appA", "Appendix A: Creatures &amp; NPCs"))
H.append(chapter("appA", "Creatures &amp; NPCs", "Appendix A"))
for folder, actors in B.FOLDERS.items():
    for n_, a in enumerate(actors):
        sb = statblock(a)
        H.append(f'<div class="cr-wrap{" long" if "statblock long" in sb else ""}">{("<h2>" + folder + "</h2>") if n_ == 0 else ""}<div class="creature"><img class="sb-portrait" src="{img(a["img"], 360)}">{enrich(a["system"]["details"]["biography"]["value"])}</div>{sb}</div>')
H.append('<h2 class="newpage">Encounter Notes</h2>')
for k in ("app-a", "app-b"):
    t, h = B1[k]
    h = re.sub(r'<div class="rc-npc">.*?</div></div>', "", strip_wrapper(h), flags=re.S)
    H.append(sect(h, t))
# Appendix B: arena engine & tables
TOC.append(("appB", "Appendix B: Arena Engine &amp; Roll Tables"))
H.append(chapter("appB", "Arena Engine &amp; Roll Tables", "Appendix B"))
H.append(sect(B1["arena-engine"][1], B1["arena-engine"][0]))
done = set(re.findall(r"RollTable\.([A-Za-z0-9]{16})", B1["arena-engine"][1]) + re.findall(r"RollTable\.([A-Za-z0-9]{16})", B1["app-b"][1]))
for t in TB.TABLES:
    if t["_id"] in done:
        continue
    rows = "".join(f"<tr><td class='die'>{r['range'][0]}{'–' + str(r['range'][1]) if r['range'][1] != r['range'][0] else ''}</td><td>{enrich(r['description'])}</td></tr>" for r in t["results"])
    H.append(f'<div class="rtable"><h3>{t["name"]}</h3>{("<p><i>" + enrich(t["description"]) + "</i></p>") if t["description"] else ""}'
             f'<table class="rc-table"><thead><tr><th>{t["formula"]}</th><th>Result</th></tr></thead><tbody>{rows}</tbody></table></div>')
# Appendix C: handouts
TOC.append(("appC", "Appendix C: Handouts &amp; Contract Forms"))
H.append(chapter("appC", "Handouts &amp; Contract Forms", "Appendix C"))
for k, t, h in pages("handouts"):
    H.append(f'<section class="handout-page"><p class="ho-label">{t}</p>{enrich(strip_wrapper(h))}</section>')
# Appendix D: maps
TOC.append(("appF", "Appendix D: Maps"))
H.append(chapter("appF", "Maps", "Appendix D"))
H.append("<p>Every map is 5 feet per square. The six original 2020 maps are rebuilt as Plates 1–6 of their chapters; the keyed "
         "locations inside them follow. Full-resolution gridded, gridless and Universal VTT versions (with walls, doors and "
         "lights) are in the companion Map Pack.</p>")
scenes = json.load(open(f"{ROOT}/module/data/scenes.json"))
for s_ in scenes["scenes"]:
    k = s_["key"]
    if k in _REUSE:
        continue
    im = Image.open(f"{ROOT}/module/assets/maps/{k}.webp").convert("RGB")
    im.thumbnail((2200, 2200))
    p = f"{W}/img/map-{k}.jpg"
    im.save(p, "JPEG", quality=84)
    land = im.width > im.height * 1.15
    keyed = "".join(f"<li>{n['label']}</li>" for n in s_["notes"])
    H.append(f'<section class="map-page {"land" if land else ""}"><h3>Plate {MAPNO[k]}: {MAPTITLE[k]}</h3>'
             f'<p class="map-meta">{s_["width"] // 100} × {s_["height"] // 100} squares ({s_["width"] // 20} × {s_["height"] // 20} ft.)</p>'
             f'<img src="{p}"><ul class="map-key">{keyed}</ul></section>')
# Appendix E: record sheets
TOC.append(("appE", "Appendix E: Record Sheets"))
H.append(chapter("appE", "Record Sheets", "Appendix E"))
H.append(sect(B1["app-c"][1], B1["app-c"][0]))
# Appendix F: design notes
TOC.append(("appH", "Appendix F: Design Notes &amp; Rules Audit"))
H.append(chapter("appH", "Design Notes &amp; Rules Audit", "Appendix F"))
H.append(enrich(strip_wrapper(pages("toolkit")[1][2])).replace("<h2>Design Notes &amp; Rules Audit</h2>", "").replace("<h2>Design Notes & Rules Audit</h2>", ""))

LEGAL = ("DUNGEONS &amp; DRAGONS, D&amp;D, Wizards of the Coast, Forgotten Realms, the dragon ampersand, Player's Handbook, "
         "Monster Manual, Dungeon Master's Guide, D&amp;D Adventurers League, all other Wizards of the Coast product names, and "
         "their respective logos are trademarks of Wizards of the Coast in the USA and other countries. All characters and their "
         "distinctive likenesses are property of Wizards of the Coast. This material is protected under the copyright laws of "
         "the United States of America. Any reproduction or unauthorized use of the material or artwork contained herein is "
         "prohibited without the express written permission of Wizards of the Coast.<br><br>©2026 Wizards of the Coast LLC, PO Box "
         "707, Renton, WA 98057-0707, USA. Manufactured by Wizards of the Coast LLC, PO Box 707, Renton, WA 98057-0707, USA.<br><br>"
         "All other original material in this work is copyright 2026 by Asmo, Pacts &amp; Polyhedrals (Ben Vale) and published "
         "under the Community Content Agreement for Dungeon Masters Guild.")
THANKS = ('<p class="thanks"><em>Interplanal Champions</em> grew out of <em>Interplanal Champion: Interest of Asmodeus</em>, first run at the table '
          'in 2020 as the follow-on to <em>The Night of the Red Clause</em>. My thanks to everyone who played the original versions on the '
          '<strong>Blown Away</strong> server, my first playtest group and the first D&amp;D server I ran. You crossed the first lava river, '
          'argued with the first imps and walked into the first arena, and every page of this campaign is better for it. Special thanks to the playtesters, <strong>Tim, Alex, Heather and Kai</strong>, and to the <strong>Pacts &amp; Polyhedrals</strong>, <strong>Blown Away</strong> and <strong>Imagi-Nations</strong> Discord servers.</p>')
COVER = f"{W}/img/cover.jpg"
BACK = f"{W}/img/back.jpg"
shutil.copy(f"{ROOT}/dist/dmsguild-cover.jpg", COVER)
shutil.copy(f"{ROOT}/dist/dmsguild-back.jpg", BACK)


def front():
    toc = "".join(f'<li><a href="#{c}">{t}</a></li>' for c, t in TOC)
    return (f'<section class="cover"><img src="{COVER}"></section>'
            '<section class="credits"><h2>Interplanal Champions</h2><p class="tag">Book I: The Throne of Avernus · a campaign of infernal succession for characters of 12th to 17th level</p>'
            "<p><b>Design &amp; Writing:</b> Asmo, Pacts &amp; Polyhedrals (Ben Vale)<br><b>The Asmodeun Scriptorium:</b> Asmo<br>"
            "<b>Cartography, Portraits &amp; Layout:</b> Pacts &amp; Polyhedrals<br>"
            "<b>Play with us:</b> patreon.com/pactsandpolyhedrals · startplaying.games/gm/dmasmo</p>"
            + THANKS +
            '<div class="blurb"><p><i>In Hell, the strongest take the throne. The devious keep it. The wise read what they have signed.</i></p></div>'
            f'<p class="legal">{LEGAL}</p></section>'
            f'<section class="toc"><h2>Contents</h2><ul>{toc}</ul></section>')


def back():
    return f'<section class="backcover"><img src="{BACK}"></section>'


BODY = "".join(H)
open(f"{W}/body.html", "w").write(drop_dup_titles(BODY))
json.dump({"toc": TOC}, open(f"{W}/meta.json", "w"))
open(f"{W}/front.html", "w").write(front())
open(f"{W}/back.html", "w").write(back())
print("html", len(BODY) // 1000, "KB")


# =====================================================================================================================
# BOOK II — PLAYER'S GUIDE
# =====================================================================================================================
SPOILERS = ("Hollis", "Heartstone", "Vacant King", "Iron Heir", "Pyric Trust")


def player_safe(h):
    h = re.sub(r'<section class="rc-secret">.*?</section>', "", h, flags=re.S)
    return h


PTOC, PH = [], []


def pchapter(cid, title, kicker):
    PTOC.append((cid, title))
    PH.append(chapter(cid, title, kicker))


B2 = jp("book2")
pchapter("pintro", "Claimants of the First Crown", "Chapter 1")
PH.append(sect(B2["cover"][1], "Claimants of the First Crown"))
PH.append(sect(B2["charter"][1], B2["charter"][0]))
pchapter("pheroes", "Pregenerated Claimants", "Chapter 2")
PH.append("<p>Six complete 12th-level claimants, each on five pages: <b>I · Core</b>, <b>II · Features &amp; Equipment</b>, "
          "<b>III · Spells</b> or <b>Tactics</b>, <b>IV · Backstory</b> and <b>V · Claim &amp; Connections</b>. Built from the 2014 SRD and this book's subclasses. "
          "These versions keep each claimant's private pressure for the DM to share.</p>")
PH.append(SHEETS.all_sheets(lambda k: img(f"modules/{MOD}/assets/portraits/pc-{k}.webp", 700), public=True))
_cl = strip_wrapper(B2["claimants"][1])
_cl = re.sub(r'<div class="rc-pregen">.*?</div></div>.*?(?=<div class="rc-pregen">|<h3>Shared|$)', "", _cl, flags=re.S)
PH.append(f'<section class="sect">{enrich(_cl)}</section>')
pchapter("popts", "Character Options", "Chapter 3")
for k in ("ruby-court", "blood-price", "ashen", "soulforged"):
    t, h = B2[k]
    PH.append(f'<h2 class="newpage">{t}</h2>' + f'<section class="sect">{enrich(strip_wrapper(h).replace(f"<h2>{t}</h2>", ""))}</section>')
import soulforged as SFM
PH.append('<h2 class="newpage">Soulforged Servitors</h2><p>Both frames at 12th level with Intelligence 20. Rescale with the '
          'formulas in each biography.</p>' + "".join(
    f'<div class="cr-wrap"><div class="creature"><img class="sb-portrait" src="{img(a["img"], 360)}">'
    f'{enrich(a["system"]["details"]["biography"]["value"])}</div>{statblock(a)}</div>' for a in SFM.build_actors()))
import ashen_forms as AFM
PH.append('<h2 class="newpage">Ashen Forms: Fiends of Avernus</h2>'
          '<p>Seven original fiends for the Circle of Ashen Covenants\' Wild Shape. The Ashen Hellwarden is an Infernal Form '
          '(10th level, two uses of Wild Shape). SRD fiends use the standard stat blocks; the forms from other books use those books.</p>'
          + "".join(f'<div class="cr-wrap"><div class="creature">{enrich(a["system"]["details"]["biography"]["value"])}</div>{statblock(a)}</div>'
                    for a in AFM.HOMEBREW))
for sub, feats, kind in ((PO.SCHOOL, PO.WIZ_FEATURES, "Arcane Tradition (Wizard) · from the Asmodeun Scriptorium"),
                         (PO.OATH, PO.PAL_FEATURES, "Sacred Oath (Paladin) · from the Asmodeun Scriptorium"),
                         (PO.DOMAIN, PO.CLE_FEATURES, "Divine Domain (Cleric) · from the Asmodeun Scriptorium")):
    PH.append(f'<h2 class="newpage">{sub["name"]}</h2><div class="subclass"><p class="sp-type"><i>{kind}</i></p>'
              f'{enrich(sub["system"]["description"]["value"])}' +
              "".join(f'<h4>{f["name"]}</h4><p class="sp-type"><i>{f["system"]["requirements"]}</i></p>{enrich(f["system"]["description"]["value"])}'
                      for f in feats) + "</div>")
pchapter("pspells", "Spells", "Chapter 4")
PH.append(sect(B2["spells"][1], B2["spells"][0]))
PH.append('<h2 class="newpage">The Asmodeun Scriptorium\'s Contract Spells</h2><p>The twenty-six spells of the Scriptorium, carried '
          'over from <em>The Night of the Red Clause</em>. Orren, Caldris and Nema draw on them.</p>' +
          "".join(spellblock(s) for s in sorted(SP.SPELLS, key=lambda s: (s["system"]["level"], s["name"]))
                  if s["flags"][MOD]["group"] == "Asmodeun Scriptorium"))
pchapter("prelics", "Relics of the Championship", "Chapter 5")
PH.append(sect(B2["relics"][1], B2["relics"][0]))
pchapter("pho", "The Charter and Eight Contracts", "Chapter 6")
PH.append(sect(B2["contracts"][1], B2["contracts"][0]))
_hd = {k: (t, h) for k, t, h in pages("handouts")}
for k in ("invitation", "charter", "ic-01", "ic-02", "ic-03", "ic-04", "ic-05", "ic-06", "ic-07", "ic-08", "challenge-card"):
    t, h = _hd[k]
    PH.append(f'<section class="handout-page"><p class="ho-label">{t.split(" — ")[-1]}</p>{enrich(strip_wrapper(h))}</section>')
pchapter("pfurnace", "Infernal Machines and Soul Coins", "Chapter 7")
import redline as RL
PH.append(sect(B2["soul-furnace"][1], B2["soul-furnace"][0]))
PH.append('<h2 class="newpage">Driving in Avernus</h2>' + f'<section class="sect">{enrich(RL.driving_html())}</section>')
PH.append('<h2>The Machines You Can Crew</h2>' + "".join(
    f'<div class="cr-wrap"><div class="creature"><img class="sb-portrait" src="{img(a["img"], 360)}">'
    f'{enrich(a["system"]["details"]["biography"]["value"])}</div>{statblock(a)}</div>'
    for a in [x for v in B.FOLDERS.values() for x in v if x["_id"] in (fid("actor:scorchhound-quad"), fid("actor:cinderfang-spiker"), fid("actor:souljack-hauler"))]))
pchapter("prules", "Player Rules, Advancement and 2024 Conversion", "Chapter 8")
PH.append(sect(B2["rules"][1], B2["rules"][0]))

PCOVER, PBACK = f"{W}/img/player-cover.jpg", f"{W}/img/player-back.jpg"
shutil.copy(f"{ROOT}/dist/dmsguild-player-cover.jpg", PCOVER)
shutil.copy(f"{ROOT}/dist/dmsguild-player-back.jpg", PBACK)
_ptoc = "".join(f'<li><a href="#{c}">{t}</a></li>' for c, t in PTOC)
PFRONT = (f'<section class="cover"><img src="{PCOVER}"></section>'
          '<section class="credits"><h2>Interplanal Champions</h2><p class="tag">Book II: Claimants of the First Crown · Player\'s Guide '
          '&amp; Character Options</p>'
          "<p><b>Design &amp; Writing:</b> Asmo, Pacts &amp; Polyhedrals (Ben Vale)<br><b>The Asmodeun Scriptorium:</b> Asmo<br>"
          "<b>Cartography, Portraits &amp; Layout:</b> Pacts &amp; Polyhedrals<br>"
          "<b>Play with us:</b> patreon.com/pactsandpolyhedrals · startplaying.games/gm/dmasmo</p>" + THANKS +
          '<div class="blurb"><p><i>Every crown is a contract. Read yours.</i></p></div>'
          f'<p class="legal">{LEGAL}</p></section><section class="toc"><h2>Contents</h2><ul>{_ptoc}</ul></section>')
open(f"{W}/player_body.html", "w").write(drop_dup_titles("".join(PH)))
open(f"{W}/player_front.html", "w").write(PFRONT)
open(f"{W}/player_back.html", "w").write(f'<section class="backcover"><img src="{PBACK}"></section>')
print("player html", len("".join(PH)) // 1000, "KB")
