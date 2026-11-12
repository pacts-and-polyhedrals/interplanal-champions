"""Build Interplanal Champions: pack sources, scenes.json, module.json; compile with @foundryvtt/foundryvtt-cli."""
import json, os, shutil, subprocess, sys, copy, re
sys.path.insert(0, "/home/claude/ic/src")
from lib5e import *
import bestiary, items, spells, playeroptions, pregens, tables, macros
import j_toolkit, j_book1, j_book2, j_rest, j_scriptorium, jhelp

ROOT = "/home/claude/ic"
MODDIR = f"{ROOT}/module"
SRC = f"{ROOT}/build/packs"
VERSION = "1.0.1"
REPO = "https://github.com/pacts-and-polyhedrals/interplanal-champions"

shutil.rmtree(SRC, ignore_errors=True)
os.makedirs(SRC)
PACKDOCS = {}


def folder(pack, name, ftype, parent=None, color="#5e0b18", sort=0):
    fidv = fid(f"folder:{pack}:{name}:{parent}")
    PACKDOCS.setdefault(pack, []).append({"_id": fidv, "name": name, "type": ftype, "folder": parent, "sorting": "m",
                                          "sort": sort, "color": color, "description": "", "flags": {},
                                          "_key": f"!folders!{fidv}", "_stats": STATS})
    return fidv


def add(pack, doc, fold=None):
    d = copy.deepcopy(doc)
    d["folder"] = fold
    PACKDOCS.setdefault(pack, []).append(d)


# ---- actors
for i, (fname, actors) in enumerate(bestiary.FOLDERS.items()):
    f = folder("actors", fname, "Actor", sort=i * 1000, color=["#a3182a", "#2f7a46", "#5a3214", "#3a1a1a", "#b8862e",
                                                                 "#3a3640", "#2c4f8a", "#4a4a52"][i % 8])
    for j, a in enumerate(actors):
        a["sort"] = j * 100
        add("actors", key_items(a), f)
import ashen_forms
fa = folder("actors", ashen_forms.FOLDER, "Actor", sort=len(bestiary.FOLDERS) * 1000, color="#c2410c")
for j, a in enumerate(ashen_forms.ACTORS):
    a["sort"] = j * 100
    add("actors", key_items(a), fa)
import soulforged
fs = folder("actors", "Soulforged Servitors", "Actor", sort=(len(bestiary.FOLDERS) + 1) * 1000, color="#b8862e")
for j, a in enumerate(soulforged.build_actors()):
    a["sort"] = j * 100
    add("actors", key_items(a), fs)
fp = folder("pregens", "Pregenerated Claimants (Level 12)", "Actor", color="#c0183a")
for j, a in enumerate(pregens.ACTORS):
    a["sort"] = j * 100
    add("pregens", key_items(a), fp)
# ---- items
for i, (fname, docs) in enumerate(items.ITEMS.items()):
    f = folder("items", fname, "Item", sort=i * 1000, color=["#2f7a46", "#8e1424", "#b8862e", "#3a3640"][i % 4])
    for j, d in enumerate(docs):
        d["sort"] = j * 100
        add("items", key_item(d), f)
# ---- spells, by group then level
LEVELN = {0: "Cantrips", 1: "1st Level", 2: "2nd Level", 3: "3rd Level", 4: "4th Level", 5: "5th Level", 6: "6th Level",
          7: "7th Level", 8: "8th Level", 9: "9th Level"}
groups = {}
for s in spells.SPELLS:
    g = s["flags"][MOD]["group"]
    if g not in groups:
        groups[g] = folder("spells", g, "Item", sort=len(groups) * 1000, color="#8e1424" if "Script" in g else "#2c4f8a")
    lvf = folder("spells", LEVELN[s["system"]["level"]], "Item", parent=groups[g], sort=s["system"]["level"] * 100)
    add("spells", key_item(s), lvf)
PACKDOCS["spells"] = list({d["_id"]: d for d in PACKDOCS["spells"]}.values())
# ---- player options
fsub = folder("options", "Subclasses", "Item", sort=0, color="#8e1424")
for sdoc in playeroptions.SUBCLASSES:
    add("options", key_item(sdoc), fsub)
for i, (fname, feats) in enumerate(playeroptions.FEATURE_FOLDERS.items(), 1):
    ff = folder("options", fname, "Item", sort=i * 1000, color=["#5a0a1a", "#3a0a0a", "#2a3a14", "#3a1a3a", "#3a0a0a", "#3a2a0a"][(i - 1) % 6])
    for f_ in feats:
        f_["sort"] = f_["flags"][MOD]["level"] * 100
        add("options", key_item(f_), ff)
# ---- journals
jfolders = {}
for j in jhelp.build_docs():
    fn = j["folder"]
    if fn not in jfolders:
        jfolders[fn] = folder("journals", fn, "JournalEntry", sort={"Books": 0, "Handouts": 1000}[fn],
                              color={"Books": "#8e1424", "Handouts": "#b8862e"}[fn])
    add("journals", j, jfolders[fn])
# ---- tables
TF = {"Arena of Asmodeus": ["arena-environment", "arena-summons-15", "arena-summons-17"],
      "The Road and the Wilds": ["travel", "wilds-encounters", "greyhurst-encounters", "temptations"],
      "Rewards & Consequences": ["rewards-low", "rewards-high", "mansion-consequences"],
      "Rivals": ["rival-oracle"],
      "The Redline Run & Soul Furnace": __import__("redline").TABLE_KEYS,
      "The Soulforged": __import__("soulforged").TABLE_KEYS}
for i, (fname, keys) in enumerate(TF.items()):
    f = folder("tables", fname, "RollTable", sort=i * 1000)
    for t in tables.TABLES:
        if t["flags"][MOD]["key"] in keys:
            add("tables", t, f)
assert sum(len(v) for v in TF.values()) == len(tables.TABLES)
# ---- macros
mf = {}
for m in macros.MACROS:
    if m["folder"] not in mf:
        mf[m["folder"]] = folder("macros", m["folder"], "Macro", sort=len(mf) * 1000)
    add("macros", m, mf[m["folder"]])

for pack, docs in PACKDOCS.items():
    os.makedirs(f"{SRC}/{pack}", exist_ok=True)
    for d in docs:
        name = re.sub(r"[^A-Za-z0-9]+", "_", d["name"])[:50] + "_" + d["_id"]
        json.dump(d, open(f"{SRC}/{pack}/{name}.json", "w"), ensure_ascii=False)

# ---- scenes.json
raw = json.load(open(f"{ROOT}/src/scenes.json"))
ORDER = ["welcome", "counting-gate", "ash-bridge", "breach", "findings", "styx-ferry", "ashen-caverns", "greyhurst",
         "greyhurst-district", "tavern", "greenbottle", "mansion-lower", "mansion-upper", "souljack-yard", "redline-run", "market-names", "docket", "masquerade",
         "citadel", "iron-quarter", "arena", "claw-rift", "audience", "reliquary"]
TITLES = {k: raw[k]["name"] for k in ORDER}
SCENE_PAGE = {"welcome": "map1", "counting-gate": "map1", "ash-bridge": "map1", "breach": "map1", "findings": "map2",
              "styx-ferry": "map2", "ashen-caverns": "map2", "greyhurst": "map3", "greyhurst-district": "map3", "tavern": "map3",
              "greenbottle": "map3", "mansion-lower": "map4", "mansion-upper": "map5", "market-names": "s8", "docket": "s10",
              "masquerade": "s11", "citadel": "s12", "iron-quarter": "s13", "arena": "s14", "claw-rift": "s15", "audience": "s16",
              "reliquary": "s18", "souljack-yard": "souljack-yard", "redline-run": "redline"}
adv = fid("journal:book1")
actor_ids = {}
for a in [x for v in bestiary.FOLDERS.values() for x in v]:
    k = a["img"].split("/")[-1].replace(".webp", "")
    actor_ids[k] = a["_id"]
out = {"landing": {"key": "title", "id": fid("scene:title"), "title": "Interplanal Champions", "order": 0,
                   "src": f"modules/{MOD}/assets/art/title.webp", "width": 1920, "height": 1080, "grid": 100,
                   "env": {"darkness": 0, "globalLight": True}, "journal": adv,
                   "journalPage": fid("page:book1:overview")},
       "scenes": []}
page_keys = {p[0] for j in jhelp.JOURNALS if j[0] == "book1" for p in j[3]}
for i, k in enumerate(ORDER, 1):
    s = raw[k]
    notes = []
    for n in s["notes"]:
        pk = SCENE_PAGE[k]
        assert pk in page_keys, (k, pk)
        notes.append({"x": n["x"], "y": n["y"], "label": n["label"], "entryId": adv, "pageId": fid(f"page:book1:{pk}")})
    toks = []
    for t in s["tokens"]:
        assert t["actor"] in actor_ids, t["actor"]
        toks.append({"actorId": actor_ids[t["actor"]], "x": t["x"], "y": t["y"], "hidden": t["hidden"], "name": t["name"]})
    W_, H_ = s["width"], s["height"]
    walls_ = []
    for w in s["walls"]:
        c = [min(max(v, 0), W_ if j % 2 == 0 else H_) for j, v in enumerate(w["c"])]
        if abs(c[0] - c[2]) + abs(c[1] - c[3]) < 1:
            continue
        walls_.append(dict(w, c=c))
    s["walls"] = walls_
    out["scenes"].append({"key": k, "id": fid("scene:" + k), "title": f"{i:02d} · {TITLES[k]}", "order": i,
                          "src": f"modules/{MOD}/assets/maps/{s.get('image', k)}.webp", "width": s["width"], "height": s["height"],
                          "grid": s["grid"], "walls": s["walls"], "lights": s["lights"], "notes": notes, "tokens": toks,
                          "env": s["env"], "journal": adv, "journalPage": fid(f"page:book1:{SCENE_PAGE[k]}")})
os.makedirs(f"{MODDIR}/data", exist_ok=True)
json.dump(out, open(f"{MODDIR}/data/scenes.json", "w"))

# ---- module.json
PERM_PLAYER = {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}
PERM_GM = {"PLAYER": "NONE", "ASSISTANT": "OWNER"}
packs = [
    ("journals", "JournalEntry", "Books, Handouts & Journals", PERM_GM),
    ("actors", "Actor", "Actors (Bestiary & NPCs)", PERM_GM),
    ("pregens", "Actor", "Pregenerated Claimants", PERM_PLAYER),
    ("items", "Item", "Relics, Exhibits & Tokens", PERM_PLAYER),
    ("spells", "Item", "Spells", PERM_PLAYER),
    ("options", "Item", "Player Options (Subclasses)", PERM_PLAYER),
    ("tables", "RollTable", "Roll Tables", PERM_GM),
    ("macros", "Macro", "Macros", PERM_GM),
]
module = {
    "id": MOD, "title": "Interplanal Champions: The Throne of Avernus",
    "description": "<p>A level 12–17 D&amp;D 5e campaign of infernal succession, the sequel to <em>The Night of the Red Clause</em>. "
                   "Asmodeus opens the throne of Avernus to challengers who can prove Survival, Deviousness and Dominion, and "
                   "every crown is a contract. Twenty-two vector battlemaps (the six 2020 originals rebuilt, plus their keyed "
                   "locations), a full bestiary with automation including Misty, Hell Hag Queen, six level-12 claimants, three new "
                   "subclasses, seventeen contractual spells, fourteen relics, the Championship Charter and eight contract forms, "
                   "roll tables, the Championship Board and arena, tribunal and mass-battle tools. One-click setup.</p>",
    "version": VERSION,
    "authors": [{"name": "Asmo, Pacts & Polyhedrals (Ben Vale)", "url": "https://www.patreon.com/pactsandpolyhedrals"}],
    "compatibility": {"minimum": "13", "verified": "14"},
    "relationships": {"systems": [{"id": "dnd5e", "type": "system", "compatibility": {"minimum": "5.0.0", "verified": "5.3.3"}}]},
    "esmodules": ["scripts/main.mjs"], "styles": ["styles/interplanal.css"],
    "languages": [{"lang": "en", "name": "English", "path": "lang/en.json"}],
    "packs": [{"name": n, "label": l, "path": f"packs/{n}", "type": t, "system": "dnd5e", "ownership": o, "flags": {}}
              for n, t, l, o in packs],
    "packFolders": [{"name": "Interplanal Champions", "sorting": "m", "color": "#5e0b18",
                     "packs": [p[0] for p in packs], "folders": []}],
    # The Forge Bazaar and the setup screen read media from the manifest before the module is installed: absolute URLs.
    "media": [{"type": "cover", "url": REPO.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/module/assets/art/title.webp"},
              {"type": "icon", "url": REPO.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/module/assets/icons/ic-title.webp"}],
    "url": REPO, "manifest": f"{REPO}/releases/latest/download/module.json",
    "download": f"{REPO}/releases/download/v{VERSION}/{MOD}.zip",
    "readme": f"{REPO}/blob/main/README.md", "changelog": f"{REPO}/blob/main/CHANGELOG.md",
    "bugs": f"{REPO}/issues", "license": f"{REPO}/blob/main/LICENSE", "flags": {}
}
json.dump(module, open(f"{MODDIR}/module.json", "w"), indent=2, ensure_ascii=False)
os.makedirs(f"{MODDIR}/lang", exist_ok=True)
json.dump({"IPC.Title": "Interplanal Champions", "IPC.Manager": "Championship Manager"}, open(f"{MODDIR}/lang/en.json", "w"), indent=2)

# ---- compile
shutil.rmtree(f"{MODDIR}/packs", ignore_errors=True)
js = f"""
import {{ compilePack }} from '@foundryvtt/foundryvtt-cli';
const packs = {json.dumps([p[0] for p in packs])};
for (const p of packs) await compilePack('{SRC}/' + p, '{MODDIR}/packs/' + p, {{ log: false }});
console.log('compiled', packs.length);
"""
open(f"{ROOT}/tools/compile.mjs", "w").write(js)
r = subprocess.run(["node", f"{ROOT}/tools/compile.mjs"], cwd=ROOT, capture_output=True, text=True)
print(r.stdout, r.stderr[-2000:])
print({k: len(v) for k, v in PACKDOCS.items()})
