"""Read the dnd5e 5.3.3 SRD pack sources so pregens embed real compendium documents."""
import glob, os, copy, yaml

SRD = "/home/claude/ref/dnd5e/packs/_source"
PACKS = ["classes", "subclasses", "classfeatures", "races", "items", "spells", "backgrounds", "tradegoods"]
BY_ID = {}
BY_NAME = {}


def _load():
    if BY_ID:
        return
    for pack in PACKS:
        for f in glob.glob(f"{SRD}/{pack}/**/*.yml", recursive=True):
            if os.path.basename(f) == "_folder.yml":
                continue
            d = yaml.safe_load(open(f))
            if not isinstance(d, dict) or "_id" not in d or d.get("_key", "").startswith("!folders"):
                continue
            d["__pack"] = pack
            BY_ID[d["_id"]] = d
            BY_NAME.setdefault((pack, d["name"]), d)


def uuid(doc):
    return f"Compendium.dnd5e.{doc['__pack']}.Item.{doc['_id']}"


def get(pack, name):
    _load()
    d = BY_NAME.get((pack, name))
    if d is None:
        raise KeyError(f"SRD {pack}: {name!r} not found")
    return d


def by_uuid(u):
    _load()
    return BY_ID[u.split(".")[-1]]


def embed(doc, **system_updates):
    """A clean embedded copy of an SRD item."""
    d = copy.deepcopy(doc)
    src = uuid(d)
    for k in ("__pack", "_key", "folder", "sort", "ownership"):
        d.pop(k, None)
    d["_stats"] = {"compendiumSource": src, "systemId": "dnd5e", "systemVersion": "5.3.3", "coreVersion": "13.351",
                   "duplicateSource": None, "exportSource": None}
    d.setdefault("flags", {})
    for e in d.get("effects", []):
        e.pop("_key", None)
    for k, v in system_updates.items():
        cur = d["system"]
        parts = k.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return d


def grants_upto(doc, level, skip_titles=()):
    """UUIDs from ItemGrant advancements at or below `level`."""
    out = []
    for adv in doc["system"].get("advancement", []):
        if adv.get("type") == "ItemGrant" and (adv.get("level") or 0) <= level and adv.get("title") not in skip_titles:
            for it in adv["configuration"]["items"]:
                out.append((adv, it["uuid"]))
    return out
