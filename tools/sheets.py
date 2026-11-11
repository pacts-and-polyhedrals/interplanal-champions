"""Five-page character sheets for the pregenerated heroes: Core, Features & Equipment, Spells or Tactics, Backstory, Claim & Connections."""
import re, html as H, sys
sys.path.insert(0, "/home/claude/ic/src")
from lib5e import MOD
import pregens as PG
from pregen_lore import LORE, SHEET, TACTICS, PROLOGUE

ABBR = ("str", "dex", "con", "int", "wis", "cha")
ANAME = {"str": "Strength", "dex": "Dexterity", "con": "Constitution", "int": "Intelligence", "wis": "Wisdom", "cha": "Charisma"}
SKILLS = [("acr", "Acrobatics", "dex"), ("ani", "Animal Handling", "wis"), ("arc", "Arcana", "int"), ("ath", "Athletics", "str"),
          ("dec", "Deception", "cha"), ("his", "History", "int"), ("ins", "Insight", "wis"), ("itm", "Intimidation", "cha"),
          ("inv", "Investigation", "int"), ("med", "Medicine", "wis"), ("nat", "Nature", "int"), ("prc", "Perception", "wis"),
          ("prf", "Performance", "cha"), ("per", "Persuasion", "cha"), ("rel", "Religion", "int"), ("slt", "Sleight of Hand", "dex"),
          ("ste", "Stealth", "dex"), ("sur", "Survival", "wis")]
PB = 4
HD = {"Cleric": "d8", "Wizard": "d6", "Paladin": "d10", "Warlock": "d8", "Barbarian": "d12", "Druid": "d8"}
CASTER = {"Cleric": "wis", "Wizard": "int", "Paladin": "cha", "Warlock": "cha", "Druid": "wis"}
SLOTS = {"Cleric": [4, 3, 3, 3, 2, 1], "Wizard": [4, 3, 3, 3, 2, 1], "Druid": [4, 3, 3, 3, 2, 1], "Paladin": [4, 3, 3],
         "Warlock": [0, 0, 0, 0, 3]}
AC = {"aurelia": (15, "Studded leather +1 (13) + Dex 2"), "varka": (16, "Unarmoured: 10 + Dex 2 + Con 4"),
      "ilyra": (17, "Hide 12 + Dex 2 + Shield +1 (3)"), "orren": (16, "Mage armour 13 + Dex 2 + Cloak 1 (13 without mage armour)"),
      "caldris": (22, "Plate 18 + Shield +1 (3) + Defence 1"), "nema": (18, "Scale mail 14 + Dex 1 + Shield +1 (3)")}
SAVE_MISC = {"orren": 1, "caldris": 4}
CHECK_MISC = {}
SAVE_NOTE = {"aurelia": "Advantage vs charm/fright by fiends (Reserved Rights, from 10th); one reroll vs a spell per long rest.",
             "varka": "Advantage on Dex saves you can see coming (Danger Sense).",
             "ilyra": "Advantage vs charm; can't be magically put to sleep (Fey Ancestry).",
             "orren": "+1 Cloak of Protection.", "caldris": "+4 Aura of Protection (you and allies within 10 ft.).",
             "nema": "Advantage vs poison (Dwarven Resilience)."}
DEFENSES = {"aurelia": "Resistance: fire, psychic", "varka": "Raging: resist bludgeoning, piercing, slashing; Relentless Rage",
            "ilyra": "Resistance: fire (Covenant of Embers, 10th)", "orren": "—",
            "caldris": "Resistance: fire (Draconic Ancestry); immune to disease; allies within 10 ft. can't be frightened",
            "nema": "Resistance: poison"}
SENSES = {"aurelia": "Darkvision 60 ft.; Devil's Sight 120 ft.", "varka": "Darkvision 60 ft.", "ilyra": "Darkvision 60 ft.",
          "orren": "—", "caldris": "Divine Sense", "nema": "Darkvision 60 ft."}
SPEED = {"aurelia": "30 ft.", "varka": "40 ft. (Fast Movement)", "ilyra": "35 ft. (wood elf)", "orren": "30 ft.",
         "caldris": "30 ft.", "nema": "25 ft. (not reduced by heavy armour)"}
PROFS = {"aurelia": ("Light armour", "Simple weapons", "—"), "varka": ("Light and medium armour, shields", "Simple and martial weapons", "—"),
         "ilyra": ("Light and medium armour, shields (no metal)", "Clubs, daggers, darts, javelins, maces, quarterstaffs, scimitars, sickles, slings, spears", "Herbalism kit"),
         "orren": ("—", "Daggers, darts, slings, quarterstaffs, light crossbows", "Calligrapher's supplies"),
         "caldris": ("All armour, shields", "Simple and martial weapons", "—"),
         "nema": ("Light, medium and heavy armour, shields", "Simple weapons, battleaxe, handaxe, light hammer, warhammer", "Calligrapher's supplies")}
ACTIONS = {
    "aurelia": [("Action", "<i>Eldritch blast</i> (three beams, +9, 1d10 + 5 force each, push 10 ft.), cast a spell"),
                ("Bonus", "Offer a Minor Term (Clause of Mutual Aid, 4/long rest): a willing ally adds a d6 once"),
                ("Reaction", "<i>Counterspell</i>, <i>hellish rebuke</i>; Consideration Received when a hostile breaks a Term; Reserved Rights reroll")],
    "varka": [("Action", "Attack ×2 (greataxe +10, 1d12 + 6; +3 raging; first hit each turn +1d8 vow damage)"),
              ("Bonus", "Rage (5/long rest) and speak a Battle Vow; Reckless Attack is free"),
              ("Reaction", "Collateral Guardian (soak a hit for an adjacent ally, 4/long rest) or opportunity attack")],
    "ilyra": [("Action", "Cast a spell, Wild Shape (beast, or Ashen fiend up to CR 4), or manifest the Ash Warden Spirit (bonus action, costs a Wild Shape use)"),
              ("Bonus", "Command the Ash Warden (Ashen Touch +9, 2d8 + 4 fire), <i>healing word</i>, <i>shillelagh</i>"),
              ("Reaction", "Witness of the Grove (reduce damage to the Accord bearer by 1d8 + 5) or Remedy of the Root (−1d6 to an attacker)")],
    "orren": [("Action", "Cast a spell; Devil's Retainer takes Dash, Hide, Help or scribes"),
              ("Bonus", "Contract Sigil: a bearer adds a d6 to one damage roll or save per turn (5/long rest)"),
              ("Reaction", "<i>Shield</i>, <i>counterspell</i>; retainer's Object! (disadvantage on a save, 1/long rest)")],
    "caldris": [("Action", "Attack ×2 (longsword +10, 1d8 + 6 + 1d8 radiant), cast a spell, Lay on Hands (60 HP), breath weapon (fire)"),
                ("Bonus", "—"), ("Reaction", "Channel Divinity: Fiendish Rebuke; opportunity attack")],
    "nema": [("Action", "Cast a spell, Channel Divinity (Writ of Compulsion, Infernal Audit, Turn Undead; 2/rest)"),
             ("Bonus", "<i>Healing word</i>, <i>spiritual weapon</i>; Notary of the Nine: offer a Minor Term for temp HP"),
             ("Reaction", "Opportunity attack")],
}
SKIP_FEATS = {"Spellcasting", "Otherworldly Patron", "Primal Path", "Druid Circle", "Pact Magic", "Eldritch Invocations", "Pact Boon", "Divine Domain", "Sacred Oath", "Roguish Archetype", "Bard College", "Martial Archetype",
              "Arcane Tradition", "Fighting Style", "Channel Divinity", "Additional Fighting Style", "Bonus Proficiencies",
              "Bonus Proficiency", "Expertise"}


def mod(v):
    return (v - 10) // 2


def sg(n):
    return f"+{n}" if n >= 0 else f"−{abs(n)}"


def plain(htmltext, n=280):
    t = re.sub(r"<[^>]+>", " ", htmltext or "")
    t = re.sub(r"\[\[/[^\]]*\]\]|@UUID\[[^\]]*\](\{([^}]*)\})?|&Reference\[([^\]]+)\]", lambda m: m.group(2) or m.group(3) or "", t)
    t = H.unescape(re.sub(r"\s+", " ", t)).strip()
    t = re.sub(r"^(Wondrous item,?\s*)?\(\s*requires attunement[^)]*\)\s*", "", t, flags=re.I)
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind(". "), cut.rfind("; "))
    return (cut[:k + 1] if k > 120 else cut.rsplit(" ", 1)[0] + "…")


def box(title, inner, cls=""):
    return f'<div class="bx {cls}"><div class="bx-t">{title}</div><div class="bx-b">{inner}</div></div>'


def header(p, title):
    return (f'<header class="sh-head" style="--pc:{p["color"]}"><div class="sh-port" style="background-image:url(__PORT__{p["key"]})"></div><div class="sh-name"><span class="lbl">Character Name</span>{p["name"]}</div>'
            f'<div class="sh-info"><div><span class="lbl">Class &amp; Level</span>{p["cls"]} 12</div><div><span class="lbl">Subclass</span>{p["sub"]}</div>'
            f'<div><span class="lbl">Species</span>{p["race"]}</div><div><span class="lbl">Background</span>{p.get("bg_text") or p["title"]}</div>'
            f'<div><span class="lbl">Alignment</span>{p["align"]}</div><div><span class="lbl">Player</span>&nbsp;</div></div>'
            f'<div class="sh-page">{title}</div></header>')


def weapons(p, a, ab):
    rows = []
    for it in a["items"]:
        if it["type"] != "weapon":
            continue
        s = it["system"]
        base = s["damage"]["base"]
        props = s.get("properties", [])
        rngd = s["type"]["value"].endswith("R")
        if "fin" in props:
            m = max(mod(ab["str"]), mod(ab["dex"]))
        elif rngd:
            m = mod(ab["dex"])
        else:
            m = mod(ab["str"])
        mb = int(s.get("magicalBonus") or 0)
        hit = m + PB + mb
        dmg = f'{base["number"]}d{base["denomination"]} {sg(m + mb)}' + f' {base["types"][0]}'
        r = s.get("range", {})
        notes = []
        if r.get("value") and (rngd or "thr" in props):
            notes.append(f'range {r["value"]}' + (f'/{r["long"]}' if r.get("long") else ""))
        if "ver" in props and s["damage"].get("versatile", {}).get("denomination"):
            notes.append(f'versatile d{s["damage"]["versatile"]["denomination"]}')
        for k, lab in (("fin", "finesse"), ("lgt", "light"), ("two", "two-handed"), ("hvy", "heavy")):
            if k in props:
                notes.append(lab)
        q = s.get("quantity", 1)
        extra = {"Greataxe +1": "+3 raging; vow +1d8 first hit/turn; Brutal Critical", "Longsword +1": "+1d8 radiant (Improved Smite)",
                 "Contract-Splitter Blade": "+1d6 force vs contract effects"}.get(it["name"], "")
        if extra:
            notes.append(extra)
        rows.append((it["name"] + (f" ×{q}" if q > 1 else ""), sg(hit), dmg, ", ".join(n for n in notes if n)))
    cantrips = {"aurelia": [("Eldritch Blast ×3", "+9", "1d10 + 5 force each", "120 ft.; Repelling Blast pushes 10 ft.")],
                "ilyra": [("Produce Flame", "+9", "3d8 fire", "30 ft."), ("Ash Warden: Ashen Touch", "+9", "2d8 + 4 fire", "bonus action command")],
                "orren": [("Fire Bolt", "+9", "3d10 fire", "120 ft."), ("Ember Receipt", "+9", "3d8 fire (+1d4 if a promise was broken)", "60 ft.")],
                "nema": [("Sacred Flame", "DC 17 Dex", "3d8 radiant", "60 ft., no cover bonus")]}
    rows += cantrips.get(p["key"], [])
    body = "".join(f"<tr><td class='nm'>{n}</td><td class='c'>{h}</td><td>{d}</td><td class='nt'>{x}</td></tr>" for n, h, d, x in rows)
    return f'<table class="atk"><tr><th>Name</th><th>Hit / DC</th><th>Damage / Type</th><th>Notes</th></tr>{body}</table>'


def page_core(p, a):
    ab = dict(zip(ABBR, p["abilities"]))
    saves = PG.SAVES[p["cls"]]
    k = p["key"]
    abil = "".join(f'<div class="ab"><div class="ab-n">{ANAME[x]}</div><div class="ab-m">{sg(mod(ab[x]))}</div><div class="ab-s">{ab[x]}</div></div>' for x in ABBR)
    sv = "".join(f'<li><span class="dot {"on" if x in saves else ""}"></span><b>{sg(mod(ab[x]) + (PB if x in saves else 0) + SAVE_MISC.get(k, 0))}</b> {ANAME[x]}</li>' for x in ABBR)
    jack = p["cls"] == "Bard"
    sk = []
    for key, name, at in SKILLS:
        v = p["skills"].get(key, 0)
        bonus = mod(ab[at]) + (PB * v if v else (PB // 2 if jack else 0)) + CHECK_MISC.get(k, 0)
        mark = "exp" if v == 2 else "on" if v == 1 else ""
        sk.append(f'<li><span class="dot {mark}"></span><b>{sg(bonus)}</b> {name} <i>{at.upper()}</i></li>')

    def passive(key, at):
        v = p["skills"].get(key, 0)
        return 10 + mod(ab[at]) + (PB * v if v else (PB // 2 if jack else 0)) + CHECK_MISC.get(k, 0)
    hp = a["flags"][MOD]["expectedHp"]
    init = mod(ab["dex"]) + (PB // 2 if jack else 0) + CHECK_MISC.get(k, 0)
    pr = PROFS[k]
    langs = ", ".join(l.title() for l in a["system"]["traits"]["languages"]["value"]) + (", Thieves' Cant" if k == "pip" else "")
    col1 = (f'<div class="abcol">{abil}</div>')
    col2 = (f'<div class="pill"><span class="pv">+{PB}</span>Proficiency Bonus</div><div class="pill"><span class="pv">☐</span>Heroic Inspiration</div>'
            + box("Saving Throws", f'<ul class="ls">{sv}</ul><p class="note">{SAVE_NOTE[k]}</p>')
            + box("Skills", f'<ul class="ls sk">{"".join(sk)}</ul><p class="note">● proficient &nbsp; ◆ expertise{" &nbsp; Jack of All Trades: +2 to the rest" if jack else ""}</p>')
            + box("Passive Senses", f'<ul class="ls ps"><li><b>{passive("prc","wis")}</b> Perception</li><li><b>{passive("ins","wis")}</b> Insight</li><li><b>{passive("inv","int")}</b> Investigation</li></ul><p class="note">{SENSES[k]}</p>'))
    combat = (f'<div class="cbt"><div class="shield"><span class="big">{AC[k][0]}</span><span>Armor Class</span></div>'
              f'<div class="stat"><span class="big">{sg(init)}</span><span>Initiative</span></div>'
              f'<div class="stat"><span class="big sm">{SPEED[k].split(" (")[0]}</span><span>Speed</span></div></div>'
              f'<p class="note c">{AC[k][1]}{(" · " + SPEED[k].split("(")[1].rstrip(")")) if "(" in SPEED[k] else ""}</p>'
              f'<div class="hp"><div><span class="lbl">Max HP</span><span class="big">{hp}</span></div><div><span class="lbl">Current HP</span>&nbsp;</div><div><span class="lbl">Temp HP</span>&nbsp;</div></div>'
              f'<div class="row2"><div class="mini"><span class="lbl">Hit Dice</span><b>12{HD[p["cls"]]}</b></div>'
              f'<div class="mini"><span class="lbl">Death Saves</span>Successes ○○○<br>Failures ○○○</div></div>'
              + box("Defenses", f'<p>{DEFENSES[k]}</p>', "tight")
              + box("Weapon Attacks &amp; Cantrips", weapons(p, a, ab))
              + box("On Your Turn", "".join(f'<p><b class="tag">{t}</b> {d}</p>' for t, d in ACTIONS[k]))
              + box("Proficiencies &amp; Languages", f'<p><b>Armor</b> {pr[0]}</p><p><b>Weapons</b> {pr[1]}</p><p><b>Tools</b> {pr[2]}</p><p><b>Languages</b> {langs}</p>')
              + box("Conditions &amp; Notes", '<div class="lines">' + '<div></div>' * 6 + '</div>'))
    return (f'<section class="sheet">{header(p, "I · Core")}<div class="core">{col1}<div class="c2">{col2}</div><div class="c3">{combat}</div></div></section>')


def uses_txt(it, ab, p):
    u = it["system"].get("uses") or {}
    mx = str(u.get("max") or "")
    if not mx:
        return ""
    f = mx.replace("@prof", str(PB))
    for x in ABBR:
        f = f.replace(f"@abilities.{x}.mod", str(mod(ab[x])))
    f = re.sub(r"@classes\.\w+\.levels", "12", f)
    try:
        n = int(eval(f, {"__builtins__": {}}, {"floor": lambda v: int(v // 1), "max": max, "min": min}))
    except Exception:
        return ""
    rec = (u.get("recovery") or [{}])[0].get("period", "")
    per = {"lr": "long rest", "sr": "short rest", "dawn": "dawn", "day": "day"}.get(rec, "")
    return f'<span class="uses">{n}/{per or "use"} {"☐" * min(n, 8)}</span>'


def page_features(p, a):
    ab = dict(zip(ABBR, p["abilities"]))
    groups = {"Class &amp; Subclass": [], "Species": [], "Background": []}
    for it in a["items"]:
        if it["type"] != "feat" or it["name"] in SKIP_FEATS:
            continue
        src = (it.get("_stats") or {}).get("compendiumSource", "") or ""
        g = "Species" if ".races." in src else "Background" if ".backgrounds." in src else "Class &amp; Subclass"
        groups[g].append(it)
    feats = ""
    for g, its in groups.items():
        if not its:
            continue
        feats += f'<h4 class="fg">{g} Features</h4>' + "".join(
            f'<div class="ft"><b>{i["name"]}</b>{uses_txt(i, ab, p)}<span>{plain(i["system"]["description"]["value"], 230)}</span></div>' for i in its)
    eq = [i for i in a["items"] if i["type"] in ("weapon", "equipment", "consumable", "loot", "tool", "container")]
    att = [i for i in eq if i["system"].get("attuned")]
    magic = [i for i in eq if (i["system"].get("rarity") or "") not in ("", "common") and not i["system"].get("attuned")]
    mundane = [i for i in eq if i not in att and i not in magic]

    def rows(lst):
        return "".join(f'<tr><td>{i["name"]}{" <i>(equipped)</i>" if i["system"].get("equipped") and i["type"] in ("weapon","equipment") else ""}</td><td class="c">{i["system"].get("quantity",1)}</td>'
                       f'<td class="c">{(i["system"].get("weight") or {}).get("value", 0) * i["system"].get("quantity",1):g} lb.</td></tr>' for i in lst)
    wt = sum((i["system"].get("weight") or {}).get("value", 0) * i["system"].get("quantity", 1) for i in eq)
    strs = p["abilities"][0]
    cap = strs * 15 // (2 if "Halfling" in p["race"] else 1)
    def idesc(i, n):
        mb = i["system"].get("magicalBonus")
        if mb and i["type"] == "weapon" and i["name"].endswith(f"+{mb}"):
            return f"You have a +{mb} bonus to attack and damage rolls made with this magic weapon."
        if mb and i["type"] == "equipment" and i["name"].endswith(f"+{mb}"):
            return f"You have a +{mb} bonus to AC while wearing or wielding this magic item."
        return plain(i["system"]["description"]["value"], n)
    att_html = "".join(f'<div class="att"><span class="dot on"></span><div><b>{i["name"]}</b><br><span>{idesc(i, 200)}</span></div></div>' for i in att)
    att_html += "".join('<div class="att"><span class="dot"></span><div>&nbsp;</div></div>' for _ in range(3 - len(att)))
    mag_html = "".join(f'<div class="att"><span class="dot"></span><div><b>{i["name"]}</b>{(" ×" + str(i["system"].get("quantity",1))) if i["system"].get("quantity",1) > 1 else ""}<br><span>{idesc(i, 170)}</span></div></div>' for i in magic)
    right = (box("Attuned Magic Items (3 slots)", att_html)
             + (box("Other Magic Items &amp; Potions", mag_html) if magic else "")
             + box("Equipment", f'<table class="eq"><tr><th>Item</th><th>Qty</th><th>Weight</th></tr>{rows(mundane)}</table>'
                   f'<p class="note">Carried: {wt:g} lb. · Capacity {cap} lb.</p>')
             + box("Coins", '<div class="coins"><span>CP<b>0</b></span><span>SP<b>30</b></span><span>EP<b>0</b></span><span>GP<b>250</b></span><span>PP<b>5</b></span></div>'))
    return f'<section class="sheet">{header(p, "II · Features &amp; Equipment")}<div class="two"><div>{box("Features &amp; Traits", feats, "feats")}</div><div>{right}</div></div></section>'


SCH = {"abj": "Abj", "con": "Conj", "div": "Div", "enc": "Ench", "evo": "Evoc", "ill": "Illu", "nec": "Necr", "trs": "Trans"}


def spell_row(it, dc, atk):
    s = it["system"]
    act = s.get("activation") or {}
    t = {"action": "1A", "bonus": "1BA", "reaction": "1R", "minute": f'{act.get("value") or 1} min', "hour": f'{act.get("value") or 1} hr'}.get(act.get("type"), "—")
    r = s.get("range") or {}
    rng = {"self": "Self", "touch": "Touch"}.get(r.get("units"), f'{r.get("value")} ft.' if r.get("value") else "—")
    props = s.get("properties") or []
    comp = "".join(c for c, k in (("V", "vocal"), ("S", "somatic"), ("M", "material")) if k in props)
    d = s.get("duration") or {}
    du = {"inst": "Inst.", "perm": "Perm.", "disp": "Until dispelled", "round": f'{d.get("value")} rnd', "minute": f'{d.get("value")} min',
          "hour": f'{d.get("value")} hr', "day": f'{d.get("value")} day', "spec": "Special"}.get(d.get("units"), "—")
    if "concentration" in props:
        du = "Ⓒ " + du
    eff = "—"
    for a in (s.get("activities") or {}).values():
        if a["type"] == "save":
            ab_ = a["save"]["ability"][0] if isinstance(a["save"]["ability"], list) and a["save"]["ability"] else a["save"].get("ability", "")
            eff = f"{(ab_ or '').upper()} save"
            break
        if a["type"] == "attack":
            eff = f"{sg(atk)} atk"
            break
        if a["type"] == "heal":
            eff = "Heal"
            break
    prep = s.get("prepared", 0)
    mark = "◆" if prep == 2 else ("●" if prep == 1 or s.get("level") == 0 else "○")
    rit = " ®" if "ritual" in props else ""
    return f'<tr><td class="c">{mark}</td><td class="nm">{it["name"]}{rit}</td><td>{SCH.get(s.get("school"),"")}</td><td>{t}</td><td>{rng}</td><td>{comp}</td><td>{du}</td><td>{eff}</td></tr>'


def page_spells(p, a):
    ab = dict(zip(ABBR, p["abilities"]))
    cm = mod(ab[CASTER[p["cls"]]])
    dc, atk = 8 + PB + cm, PB + cm
    spells = sorted([i for i in a["items"] if i["type"] == "spell"], key=lambda i: (i["system"]["level"], i["name"]))
    slots = SLOTS[p["cls"]]
    slot_html = "".join(f'<div class="slot"><span class="lv">{["1st","2nd","3rd","4th","5th","6th"][i]}</span><span>{"○" * n}</span></div>' for i, n in enumerate(slots) if n)
    if p["cls"] == "Warlock":
        slot_html += '<div class="slot"><span class="lv">6th (Arcanum)</span><span>○</span></div>'

    by = {}
    for s in spells:
        by.setdefault(s["system"]["level"], []).append(s)
    tables = ""
    for lv, ss in by.items():
        tables += (f'<tr class="lvh"><td colspan="8">{"Cantrips (at will)" if lv == 0 else ["", "1st", "2nd", "3rd", "4th", "5th", "6th"][lv] + " Level"}</td></tr>'
                   + "".join(spell_row(s, dc, atk) for s in ss))
    head = (f'<div class="spellhead"><div class="stat"><span class="big sm">{ANAME[CASTER[p["cls"]]]}</span><span>Spellcasting Ability</span></div>'
            f'<div class="stat"><span class="big">{dc}</span><span>Spell Save DC</span></div>'
            f'<div class="stat"><span class="big">{sg(atk)}</span><span>Spell Attack</span></div>'
            f'<div class="slots">{slot_html}<span class="lbl">Spell Slots (tick when spent)</span></div></div>')
    key = '<p class="note">◆ always prepared &nbsp; ● prepared &nbsp; ○ in spellbook / known, not prepared &nbsp; ® ritual &nbsp; Ⓒ concentration · 1A action, 1BA bonus action, 1R reaction</p>'
    extra = {"aurelia": '<p class="note">Pact Magic: three 5th-level slots, back on a short rest. Mystic Arcanum: <i>mass suggestion</i> once per long rest. Book of Ancient Secrets rituals: <i>detect magic</i>, <i>identify</i>. Hex and armor of Agathys (not SRD) are replaced by <i>hellish rebuke</i> and <i>protection from evil and good</i>.</p>',
             "ilyra": '<p class="note">Prepare 17 spells after a long rest. Wild Shape 2/short rest: a beast or an Ashen fiend up to CR 4 (Book II); both uses for a CR 5 Infernal Form; or one use for the Ash Warden Spirit. Ashen Accord: a 1-minute rite on one willing ally.</p>',
             "orren": '<p class="note">Arcane Recovery: once per day after a short rest, recover slots totalling 6 levels (none 6th+). Fine Print (◆) is always prepared by Runic Drafting. Prepare 17 spells after a long rest.</p>',
             "caldris": '<p class="note">Oath spells (◆) are always prepared. Prepare 10 more. Divine Smite: expend a slot on a hit for 2d8 radiant (+1d8 per slot above 1st, +1d8 vs fiends and undead).</p>',
             "nema": '<p class="note">Domain spells (◆) are always prepared. Prepare 17 more after a long rest. Divine Intervention: 12%.</p>'}.get(p["key"], "")
    return (f'<section class="sheet">{header(p, "III · Spells")}{head}'
            + box("Spells", f'<table class="sp{" dense" if len(spells) > 34 else ""}"><tr><th></th><th>Spell</th><th>School</th><th>Time</th><th>Range</th><th>Comp.</th><th>Duration</th><th>Save / Atk</th></tr>{tables}</table>{(key[:-4] + " " + re.sub(r"^<p class=.note.>", "", extra)) if (extra and len(spells) > 34) else key + extra}', "flow")
            + "</section>")


TRACK = {"varka": [("Rage", 5, "long rest"), ("Collateral Guardian", 4, "long rest"), ("Crownmark Gauntlets (15 temp HP)", 1, "long rest"),
                   ("Potion of Greater Healing", 2, "single use"), ("Handaxe", 2, "thrown"), ("Hit Dice (d12)", 12, "long rest, regain half")]}


def page_tactics(p, a, public=False):
    ab = dict(zip(ABBR, p["abilities"]))
    items = "".join(box(t, f"<p>{d}</p>", "tac") for t, d in TACTICS[p["key"]] if not (public and spoils(t + d)))
    tr = "".join(f'<tr><td class="nm">{n}</td><td>{"☐" * min(q, 20)}</td><td class="nt">{w}</td></tr>' for n, q, w in TRACK[p["key"]])
    return (f'<section class="sheet">{header(p, "III · Tactics &amp; Tricks")}'
            + box("Attack Reference", weapons(p, a, ab))
            + f'<div class="tacgrid">{items}</div>'
            + box("Resource Tracker", f'<table class="eq"><tr><th>Resource</th><th>Uses (tick when spent)</th><th>Recovers</th></tr>{tr}</table>')
            + box("Notes", '<div class="lines">' + '<div></div>' * 13 + '</div>') + "</section>")


PLOT = ("Hollis", "Heartstone", "Vacant King", "Iron Heir", "Greyhurst's names", "Petition M-9", "Pyric Trust")


PUBLIC_BOND = {}


PNAME = {"aurelia": "Aurelia", "varka": "Varka", "ilyra": "Ilyra", "orren": "Orren", "caldris": "Caldris", "nema": "Nema"}


def spoils(t):
    return any(w in t for w in PLOT)


def page_backstory(p, a, public=False):
    S, L = SHEET[p["key"]], LORE[p["key"]]
    port = f'modules/{MOD}/assets/portraits/pc-{p["key"]}.webp'
    det = "".join(f'<div><span class="lbl">{k}</span>{v}</div>' for k, v in [("Age", S["age"]), ("Height", S["height"]), ("Weight", S["weight"]),
                                                                            ("Eyes", S["eyes"]), ("Hair", S["hair"]), ("Skin", S["skin"]),
                                                                            ("Gender", S["gender"]), ("Faith", S["faith"])])
    left = (f'<div class="portrait"><img src="__PORT__{p["key"]}"></div>'
            + box("Appearance", f'<div class="det">{det}</div><p>{S["appearance"]}</p>')
            + box("Personality Traits", "".join(f"<p>{t}</p>" for t in S["traits"]))
            + box("Ideal", f"<p>{S['ideal']}</p>") + box("Bond", f"<p>{PUBLIC_BOND.get(p['key'], S['bond']) if public else S['bond']}</p>") + box("Flaw", f"<p>{S['flaw']}</p>")
            + box("Allies &amp; Organizations", f"<p>{S['allies']}</p>"))
    right = (box("Your Role", f"<p>{L['role']}</p>", "hl")
             + box("Backstory", "".join(f"<p>{b}</p>" for b in L["backstory"]))
             + box("Why You Entered", f"<p>{L['tonight']}</p>", "hl"))
    return f'<section class="sheet">{header(p, "IV · Backstory")}<div class="bs"><div>{left}</div><div>{right}</div></div></section>'


def page_story(p, a, public=False):
    S, L = SHEET[p["key"]], LORE[p["key"]]
    began = box("How It Began", "".join(f"<p>{x}</p>" for x in PROLOGUE))
    others = box("The Other Claimants", "".join(f"<p><b>{n}.</b> {t}</p>" for n, t in L["others"]))
    claim = box("Your Claim", f"<p>{L['knows']}</p><p class='fine'>Under the Charter you may claim alone, as one of a "
                              f"declared joint slate, or as the open representative of a patron.</p>")
    if public:
        press = box("Your Private Pressure", "<p>Your DM has one more note for you: the private pressure that will test your "
                                             "claim. Keep it to yourself until it matters.</p>", "hl")
        play = box("Playing " + PNAME[p["key"]], "<ul>" + "".join(f"<li>{x}</li>" for x in S["play"] if not spoils(x)) + "</ul>")
        left, right = began + claim, others + press + play
    else:
        press = box("Private Pressure", f"<p>{L['tie']}</p>", "hl")
        play = box("Playing " + PNAME[p["key"]], "<ul>" + "".join(f"<li>{x}</li>" for x in S["play"]) + "</ul>")
        left = began + claim + box("Toward Level 17", f"<p>{L['goal']}</p>")
        right = others + press + box("Tactics", f"<p>{L['table']}</p>", "hl") + play
    return f'<section class="sheet">{header(p, "V · Claim &amp; Connections")}<div class="bs"><div>{left}</div><div>{right}</div></div></section>'


def split_labels(h):
    """Put each labelled rule in a sheet note on its own line ("Pact Magic: ... <br>Mystic Arcanum: ...")."""
    lab = r"(?<=[.)]) ([A-Z][A-Za-z'’ ]{2,40}?:)(?= )"
    def fix(m):
        body = re.sub(lab, r"<br><b>\1</b>", m.group(2))
        body = re.sub(r"^([A-Z][A-Za-z'’ ]{2,40}?:)(?= )", r"<b>\1</b>", body) if "<br>" in body else body
        return m.group(1) + body + "</p>"
    h = re.sub(r'(<p class="note">)(.*?)</p>', fix, h, flags=re.S)
    return re.sub(r'(<div class="bx tac"><div class="bx-t">[^<]*</div><div class="bx-b"><p>)(.*?)</p>', fix, h, flags=re.S)


def all_sheets(portrait_resolver, public=False):
    out = []
    for p, a in zip(PG.PREGENS, PG.ACTORS):
        pages = [page_core(p, a), page_features(p, a),
                 page_spells(p, a) if p["cls"] in CASTER else page_tactics(p, a, public), page_backstory(p, a, public), page_story(p, a, public)]
        out.append("".join(pages).replace(f"__PORT__{p['key']}", portrait_resolver(p["key"])))
    return split_labels("".join(out))


CSS = """
@page sheet { size: letter; margin: 0.32in 0.35in 0.35in; background: #f4ead2;
  @bottom-center { content: none; } @bottom-left { content: none; } @bottom-right { content: none; } }
.sheet { page: sheet; break-before: page; color: #241312; font-family: Garamond; font-size: 8.6pt; line-height: 1.22; }
.sheet p { margin: 0 0 2.5pt; text-align: left; }
.sheet b { color: #3a0a10; }
.lbl { display: block; font-family: Cinzel; font-size: 5.6pt; letter-spacing: 0.6pt; color: #8a6418; text-transform: uppercase; }
.sh-head { display: flex; gap: 6pt; align-items: stretch; margin-bottom: 6pt; border-bottom: 3px solid var(--pc); padding-bottom: 4pt; }
.sh-port { flex: 0 0 1.05in; height: 1.05in; border: 3px solid var(--pc); border-radius: 8pt; background-color: #1a0a0c; background-size: 135%; background-position: 50% 28%; background-repeat: no-repeat; box-shadow: 0 0 0 1.5px #7a0a14; }
.sh-name { flex: 0 0 2.05in; font-family: CinzelDeco; font-size: 13.5pt; color: #7a0a14; background: #fffaf0; border: 2px solid #7a0a14; border-radius: 6pt; padding: 3pt 7pt; line-height: 1.05; }
.sh-info { flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 2pt 8pt; background: #fffaf0; border: 1.5px solid #8a6418; border-radius: 6pt; padding: 3pt 7pt; font-size: 8.4pt; }
.sh-info > div { border-bottom: 1px solid #d8c4a0; }
.sh-page { flex: 0 0 0.95in; display: flex; align-items: center; justify-content: center; text-align: center; font-family: Cinzel; font-weight: 900; font-size: 9pt; color: #fff; background: var(--pc); border-radius: 6pt; padding: 3pt; }
.bx { border: 1.5px solid #7a0a14; border-radius: 5pt; background: #fffaf0; margin-bottom: 5pt; break-inside: avoid; }
.bx-t { background: linear-gradient(#8e1424, #5e0b18); color: #ffe8c8; font-family: Cinzel; font-weight: 700; font-size: 7.2pt; letter-spacing: 0.6pt; padding: 1.5pt 6pt; border-radius: 3.5pt 3.5pt 0 0; text-transform: uppercase; }
.bx-b { padding: 3pt 6pt 2pt; }

.bx.flow { break-inside: auto; }
.bx.hl { border-color: #8a6418; } .bx.hl .bx-t { background: linear-gradient(#b88a2e, #7a5410); }
.note { font-size: 6.8pt; color: #6a5040; font-style: italic; }
.c { text-align: center !important; }
.core { display: grid; grid-template-columns: 1.05in 2.2in 1fr; gap: 6pt; }
.abcol .ab { border: 2px solid #7a0a14; border-radius: 8pt; background: #fffaf0; text-align: center; margin-bottom: 5pt; padding: 2pt 0 3pt; }
.ab-n { font-family: Cinzel; font-weight: 700; font-size: 6.4pt; color: #7a0a14; letter-spacing: 0.5pt; text-transform: uppercase; }
.ab-m { font-family: Cinzel; font-weight: 900; font-size: 19pt; color: #241312; line-height: 1.1; }
.ab-s { display: inline-block; min-width: 0.36in; border: 1.5px solid #8a6418; border-radius: 9pt; font-family: Cinzel; font-weight: 700; font-size: 9pt; background: #f4ead2; }
.pill { display: flex; align-items: center; gap: 6pt; border: 1.5px solid #7a0a14; border-radius: 12pt; background: #fffaf0; margin-bottom: 4pt; font-family: Cinzel; font-size: 7pt; font-weight: 700; color: #7a0a14; text-transform: uppercase; }
.pv { display: inline-block; width: 0.32in; text-align: center; font-size: 11pt; color: #241312; border-right: 1.5px solid #7a0a14; padding: 1pt 0; }
ul.ls { list-style: none; padding: 0; margin: 0; } ul.ls li { padding: 1pt 0; border-bottom: 1px dotted #d8c4a0; font-size: 8.3pt; }
ul.ls li b { display: inline-block; width: 0.28in; text-align: center; color: #241312; font-family: Cinzel; font-size: 8.2pt; }
ul.ls li i { font-size: 6pt; color: #8a6418; font-style: normal; }
ul.sk li { padding: 0.6pt 0; font-size: 8pt; }
ul.ps li b { width: 0.3in; border: 1px solid #8a6418; border-radius: 3pt; margin-right: 3pt; }
.dot { display: inline-block; width: 6pt; height: 6pt; border-radius: 3pt; border: 1px solid #7a0a14; vertical-align: middle; }
.dot.on { background: #7a0a14; } .dot.exp { background: #b88a2e; border-color: #7a5410; border-radius: 0; transform: rotate(45deg); width: 5pt; height: 5pt; }
.cbt { display: flex; gap: 5pt; margin-bottom: 2pt; }
.shield, .stat { flex: 1; text-align: center; border: 2px solid #7a0a14; background: #fffaf0; padding: 3pt 2pt; font-family: Cinzel; font-size: 6.3pt; font-weight: 700; color: #7a0a14; text-transform: uppercase; }
.shield { border-radius: 4pt 4pt 22pt 22pt; } .stat { border-radius: 6pt; }
.big { display: block; font-family: Cinzel; font-weight: 900; font-size: 18pt; color: #241312; line-height: 1.1; } .big.sm { font-size: 11pt; padding: 3pt 0; }
.hp { display: grid; grid-template-columns: 1fr 1fr 1fr; border: 2px solid #7a0a14; border-radius: 6pt; background: #fffaf0; margin: 4pt 0; }
.hp > div { padding: 2pt 5pt; min-height: 0.45in; border-right: 1px solid #d8c4a0; } .hp > div:last-child { border: none; }
.row2 { display: flex; gap: 5pt; margin-bottom: 5pt; } .mini { flex: 1; border: 1.5px solid #8a6418; border-radius: 5pt; background: #fffaf0; padding: 2pt 5pt; font-size: 8pt; }
.mini b { font-family: Cinzel; font-size: 11pt; }
.tight .bx-b p { margin: 0; }
table.atk, table.eq, table.sp { width: 100%; border-collapse: collapse; margin: 0; font-size: 7.8pt; }
table.atk th, table.eq th, table.sp th { background: #efe0c0; color: #7a0a14; font-family: Cinzel; font-size: 6pt; padding: 1.5pt 3pt; text-align: left; border: none; }
table.atk td, table.eq td, table.sp td { padding: 1.6pt 3pt; border-bottom: 1px solid #e2d2b0; background: none !important; color: #241312; vertical-align: top; }
td.nm { font-weight: 700; color: #3a0a10; } td.nt { font-size: 6.8pt; color: #5a4030; }
.tag { display: inline-block; min-width: 0.55in; font-family: Cinzel; font-size: 6.5pt; color: #fff !important; background: #7a0a14; border-radius: 3pt; padding: 0 3pt; margin-right: 3pt; text-align: center; }
.two { display: grid; grid-template-columns: 1.15fr 1fr; gap: 7pt; }
.feats .bx-b { columns: 1; }
h4.fg { font-family: Cinzel; font-size: 7.4pt; color: #8a6418; border-bottom: 1px solid #b88a2e; margin: 3pt 0 2pt; letter-spacing: 0.5pt; text-transform: uppercase; }
.ft { margin-bottom: 3pt; font-size: 7.6pt; line-height: 1.18; } .ft b { display: block; font-family: Cinzel; font-size: 7.6pt; color: #7a0a14; }
.ft span { display: block; } .uses { float: right; font-family: Cinzel; font-size: 6.2pt; color: #8a6418; }
.att { display: flex; gap: 5pt; align-items: flex-start; padding: 2pt 0; border-bottom: 1px dotted #d8c4a0; font-size: 7.6pt; } .att span { font-size: 7pt; color: #5a4030; }
.att .dot { margin-top: 2pt; flex: 0 0 auto; }
.coins { display: flex; gap: 4pt; } .coins span { flex: 1; text-align: center; border: 1.5px solid #8a6418; border-radius: 10pt; font-family: Cinzel; font-size: 6pt; color: #8a6418; padding: 1pt; }
.coins b { display: block; font-size: 10pt; color: #241312; }
.spellhead { display: flex; gap: 6pt; margin-bottom: 6pt; } .spellhead .stat { flex: 0 0 1.05in; }
.slots { flex: 1; display: flex; flex-wrap: wrap; gap: 3pt; align-items: center; border: 2px solid #7a0a14; border-radius: 6pt; background: #fffaf0; padding: 3pt 6pt; font-size: 10pt; }
.slot { border: 1px solid #d8c4a0; border-radius: 4pt; padding: 1pt 4pt; } .slot .lv { font-family: Cinzel; font-size: 6.5pt; color: #7a0a14; margin-right: 3pt; }
.slots .lbl { flex-basis: 100%; }
table.sp tr.lvh td { background: #7a0a14 !important; color: #ffe8c8; font-family: Cinzel; font-size: 7pt; font-weight: 700; padding: 1.5pt 4pt; }
table.sp td { font-size: 7.6pt; padding: 1.2pt 3pt; }
table.sp.dense td { font-size: 6.9pt; padding: 0.2pt 3pt; line-height: 1.12; } table.sp.dense tr.lvh td { padding: 0.5pt 4pt; }
.tacgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 6pt; } .tac .bx-b p { font-size: 9.5pt; line-height: 1.32; }
.bs { display: grid; grid-template-columns: 2.6in 1fr; gap: 7pt; }
.portrait img { width: 100%; border: 3px solid #7a0a14; border-radius: 6pt; margin-bottom: 4pt; }
.det { display: grid; grid-template-columns: 1fr 1fr; gap: 1pt 6pt; margin-bottom: 3pt; font-size: 7.6pt; } .det > div { border-bottom: 1px solid #e2d2b0; }
.bs .bx-b p, .bs .bx-b li { font-size: 8.4pt; line-height: 1.25; }
.bs ul { margin: 0; padding-left: 10pt; }
.lines > div { height: 15pt; border-bottom: 1px solid #d8c4a0; }
.sheet strong { color: #5a0a10; } .sheet em { color: #3a1a0a; }
"""
