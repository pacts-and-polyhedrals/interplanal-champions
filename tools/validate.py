"""Validate the compiled module: links, images, effects, dnd5e keys, scenes."""
import json, os, re, glob, subprocess, shutil, sys
sys.path.insert(0, "/home/claude/ic/src")
import srd

ROOT = "/home/claude/ic"
MOD = "interplanal-champions"
MODDIR = f"{ROOT}/module"
OUT = f"{ROOT}/build/extract"
shutil.rmtree(OUT, ignore_errors=True)
mod = json.load(open(f"{MODDIR}/module.json"))
js = "import {extractPack} from '@foundryvtt/foundryvtt-cli';\n" + "".join(
    f"await extractPack('{MODDIR}/packs/{p['name']}', '{OUT}/{p['name']}', {{log:false}});\n" for p in mod["packs"])
open(f"{ROOT}/tools/extract.mjs", "w").write(js)
r = subprocess.run(["node", f"{ROOT}/tools/extract.mjs"], cwd=ROOT, capture_output=True, text=True)
assert r.returncode == 0, r.stderr

problems = []
SRD_IDS = set()
for f in glob.glob("/home/claude/ref/dnd5e/packs/_source/**/*.yml", recursive=True):
    for m in re.finditer(r"^_id: (\S+)", open(f).read(), re.M):
        SRD_IDS.add(m.group(1).strip("'"))
docs = {}
for p in mod["packs"]:
    for f in glob.glob(f"{OUT}/{p['name']}/**/*.json", recursive=True):
        d = json.load(open(f))
        docs.setdefault(p["name"], []).append(d)

ids = {}
for pack, ds in docs.items():
    for d in ds:
        if d.get("_key", "").startswith("!folders"):
            continue
        ids[(pack, d["_id"])] = d
        for pg in d.get("pages", []):
            ids[(pack, d["_id"] + "." + pg["_id"])] = pg

scenes = json.load(open(f"{MODDIR}/data/scenes.json"))
scene_ids = {s["id"] for s in scenes["scenes"]} | {scenes["landing"]["id"]}

# dnd5e config keys
cfg = open("/home/claude/ref/dnd5e/module/config.mjs").read()


def cfg_keys(name):
    m = re.search(rf"DND5E\.{name} = \{{(.*?)\n\}};", cfg, re.S)
    return set(re.findall(r"^  ([a-zA-Z0-9]+):", m.group(1), re.M)) if m else set()


DMG = cfg_keys("damageTypes") | cfg_keys("healingTypes")
COND = cfg_keys("conditionTypes")
SKILLS = cfg_keys("skills")
ACTTYPES = {"action", "bonus", "reaction", "minute", "hour", "day", "longRest", "shortRest", "encounter", "turnStart",
            "turnEnd", "legendary", "mythic", "lair", "crew", "special", ""}
ACTIVITY = {"attack", "cast", "check", "damage", "enchant", "forward", "heal", "order", "save", "summon", "transform", "utility"}
print("dnd5e keys:", len(DMG), "damage,", len(COND), "conditions,", len(SKILLS), "skills")

link_re = re.compile(r"@UUID\[([^\]]+)\]")
img_re = re.compile(r'(modules/interplanal-champions/[^"\'\)\s]+)')


def check_text(where, text):
    for u in link_re.findall(text):
        parts = u.split(".")
        if parts[0] == "Compendium" and parts[1] == MOD:
            pack = parts[2]
            key = parts[4] if len(parts) == 5 else parts[4] + "." + parts[6]
            if (pack, key) not in ids:
                problems.append(f"{where}: broken link {u}")
        elif parts[0] == "Compendium" and parts[1] == "dnd5e":
            if parts[4] not in SRD_IDS:
                problems.append(f"{where}: broken SRD link {u}")
        elif parts[0] == "Scene":
            if parts[1] not in scene_ids:
                problems.append(f"{where}: broken scene link {u}")
        else:
            problems.append(f"{where}: unexpected link {u}")
    for path in img_re.findall(text):
        if not os.path.exists(f"{MODDIR}/{path.split(MOD + '/', 1)[1]}"):
            problems.append(f"{where}: missing file {path}")


def check_item(where, it):
    sysd = it.get("system", {})
    eff_ids = {e["_id"] for e in it.get("effects", [])}
    for aid, a in (sysd.get("activities") or {}).items():
        if a["type"] not in ACTIVITY:
            problems.append(f"{where}/{it['name']}: activity type {a['type']}")
        if a.get("activation", {}).get("type", "") not in ACTTYPES:
            problems.append(f"{where}/{it['name']}: activation {a['activation']['type']}")
        for e in a.get("effects", []):
            if e["_id"] not in eff_ids:
                problems.append(f"{where}/{it['name']}: activity effect {e['_id']} missing")
        parts = (a.get("damage", {}) or {}).get("parts", []) + ([a["healing"]] if a.get("healing") else [])
        for p_ in parts:
            for t in p_.get("types", []):
                if t not in DMG:
                    problems.append(f"{where}/{it['name']}: damage type {t}")
        if a["type"] == "save" and not a["save"]["ability"]:
            problems.append(f"{where}/{it['name']}: save without ability")
        if a["type"] == "save" and a["save"]["dc"]["calculation"] == "" and not str(a["save"]["dc"]["formula"]).strip().isdigit():
            problems.append(f"{where}/{it['name']}: save DC formula {a['save']['dc']['formula']!r}")
        if a["_id"] != aid or len(aid) != 16:
            problems.append(f"{where}/{it['name']}: activity id {aid}")
    for e in it.get("effects", []):
        for s in e.get("statuses", []):
            if s not in COND:
                problems.append(f"{where}/{it['name']}: status {s}")
    check_text(f"{where}/{it['name']}", json.dumps(it))


for pack, ds in docs.items():
    for d in ds:
        if d.get("_key", "").startswith("!folders"):
            continue
        if pack in ("actors", "pregens"):
            for it in d["items"]:
                check_item(f"{pack}/{d['name']}", it)
            for k in d["system"].get("skills", {}):
                if k not in SKILLS:
                    problems.append(f"{d['name']}: skill {k}")
            for c in d["system"]["traits"].get("ci", {}).get("value", []):
                if c not in COND:
                    problems.append(f"{d['name']}: ci {c}")
            for fld in ("di", "dr", "dv"):
                for t in d["system"]["traits"].get(fld, {}).get("value", []):
                    if t not in DMG:
                        problems.append(f"{d['name']}: {fld} {t}")
            check_text(f"{pack}/{d['name']}", json.dumps({k: v for k, v in d.items() if k != "items"}))
            ids_ = [i["_id"] for i in d["items"]]
            if len(ids_) != len(set(ids_)):
                problems.append(f"{d['name']}: duplicate embedded ids")
        elif pack in ("items", "spells", "options"):
            check_item(pack, d)
        elif pack == "journals":
            for pg in d["pages"]:
                if pg["type"] == "pdf":
                    if not os.path.exists(os.path.join(ROOT, "module", pg["src"].split(MOD + "/", 1)[1])):
                        problems.append(f"journal {d['name']}/{pg['name']}: missing PDF {pg['src']}")
                    continue
                check_text(f"journal {d['name']}/{pg['name']}", pg["text"]["content"])
        else:
            check_text(f"{pack}/{d['name']}", json.dumps(d))
        if d.get("folder") and not any(x["_id"] == d["folder"] for x in ds if x.get("_key", "").startswith("!folders")):
            problems.append(f"{pack}/{d['name']}: folder missing")

# scenes
actor_ids = {d["_id"] for d in docs["actors"] if not d.get("_key", "").startswith("!folders")}
for s in scenes["scenes"] + [scenes["landing"]]:
    if not os.path.exists(f"{MODDIR}/{s['src'].split(MOD + '/', 1)[1]}"):
        problems.append(f"scene {s['key']}: missing map")
    for t in s.get("tokens", []):
        if t["actorId"] not in actor_ids:
            problems.append(f"scene {s['key']}: token actor {t['actorId']}")
    for n in s.get("notes", []):
        if ("journals", n["entryId"] + "." + n["pageId"]) not in ids:
            problems.append(f"scene {s['key']}: note page missing {n['label']}")
    for w in s.get("walls", []):
        x1, y1, x2, y2 = w["c"]
        if not (0 <= min(x1, x2) and max(x1, x2) <= s["width"] and 0 <= min(y1, y2) and max(y1, y2) <= s["height"]):
            problems.append(f"scene {s['key']}: wall outside map {w['c']}")
        if (x1, y1) == (x2, y2):
            problems.append(f"scene {s['key']}: zero-length wall")
# token/portrait images for actors
for pack in ("actors", "pregens"):
    for d in docs[pack]:
        if d.get("_key", "").startswith("!folders"):
            continue
        for path in (d["img"], d["prototypeToken"]["texture"]["src"]):
            if path.startswith("systems/dnd5e/tokens/"):
                if not os.path.exists("/home/claude/ref/dnd5e/" + path.split("systems/dnd5e/", 1)[1]):
                    problems.append(f"{d['name']}: missing system token {path}")
                continue
            if not os.path.exists(f"{MODDIR}/{path.split(MOD + '/', 1)[1]}"):
                problems.append(f"{d['name']}: missing image {path}")
print("documents:", {k: len(v) for k, v in docs.items()})
print("scenes:", len(scenes["scenes"]), "walls:", sum(len(s["walls"]) for s in scenes["scenes"]),
      "lights:", sum(len(s["lights"]) for s in scenes["scenes"]), "notes:", sum(len(s["notes"]) for s in scenes["scenes"]),
      "tokens:", sum(len(s["tokens"]) for s in scenes["scenes"]))
print(f"{len(problems)} problems")
for p in problems[:60]:
    print(" -", p)
sys.exit(1 if problems else 0)
