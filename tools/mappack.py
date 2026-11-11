"""DMs Guild map pack: gridless + gridded JPGs (100 px/square), Universal VTT (.dd2vtt) with walls, doors and lights."""
import sys, os, json, base64, io, math, shutil
sys.path.insert(0, "/home/claude/ic/art")
import maps as MP
from PIL import Image, ImageDraw

OUT = "/home/claude/ic/dist/mappack/Interplanal Champions - Map Pack"
shutil.rmtree(os.path.dirname(OUT), ignore_errors=True)
for d in ("Gridless", "Gridded", "Universal VTT (dd2vtt)"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)
import re as _re
def NAME(i, m):
    return f"{i + 1:02d} " + _re.sub(r"[:/]", " -", m.name).replace("  ", " ")
rows = []
for i_, k in enumerate([k for k in MP.ORDER if k != "redline-run"]):
    m = MP.MAPS[k]()
    im = m.render("/tmp/_m.webp", quality=95)
    w, h = m.w, m.h
    base = NAME(i_, m)
    im.save(f"{OUT}/Gridless/{base} ({w}x{h}).jpg", "JPEG", quality=92, optimize=True)
    g = im.copy()
    dr = ImageDraw.Draw(g, "RGBA")
    for x in range(0, m.W + 1, 100):
        dr.line([(x, 0), (x, m.H)], fill=(10, 4, 6, 110), width=2)
    for y in range(0, m.H + 1, 100):
        dr.line([(0, y), (m.W, y)], fill=(10, 4, 6, 110), width=2)
    g.save(f"{OUT}/Gridded/{base} ({w}x{h}).jpg", "JPEG", quality=92, optimize=True)
    # Universal VTT at 70 px per square
    ppg = 70
    small = im.resize((w * ppg, h * ppg), Image.LANCZOS)
    buf = io.BytesIO()
    small.save(buf, "PNG", optimize=True)
    los, objs, portals = [], [], []
    for wl in m.walls:
        x1, y1, x2, y2 = [c / 100 for c in wl["c"]]
        seg = [{"x": x1, "y": y1}, {"x": x2, "y": y2}]
        if wl["kind"] in ("door", "secret"):
            portals.append({"position": {"x": (x1 + x2) / 2, "y": (y1 + y2) / 2}, "bounds": seg,
                            "rotation": math.atan2(y2 - y1, x2 - x1), "closed": True, "freestanding": False})
        elif wl["kind"] == "terrain":
            objs.append(seg)
        elif wl["kind"] == "window":
            portals.append({"position": {"x": (x1 + x2) / 2, "y": (y1 + y2) / 2}, "bounds": seg,
                            "rotation": math.atan2(y2 - y1, x2 - x1), "closed": False, "freestanding": False})
        else:
            los.append(seg)
    lights = [{"position": {"x": l["x"] / 100, "y": l["y"] / 100}, "range": l["dim"], "intensity": 1.0,
               "color": "ff" + l["color"].lstrip("#"), "shadows": True} for l in m.lights]
    dd = {"format": 0.3, "resolution": {"map_origin": {"x": 0, "y": 0}, "map_size": {"x": w, "y": h}, "pixels_per_grid": ppg},
          "line_of_sight": los, "objects_line_of_sight": objs, "portals": portals,
          "environment": {"baked_lighting": False, "ambient_light": "ff" + ("ffffff" if m.env.get("globalLight") else "3a3040")},
          "lights": lights, "image": base64.b64encode(buf.getvalue()).decode()}
    json.dump(dd, open(f"{OUT}/Universal VTT (dd2vtt)/{base}.dd2vtt", "w"))
    rows.append((base, w, h, w * 5, h * 5, len(m.walls), sum(1 for x in m.walls if x["kind"] in ("door", "secret")), len(m.lights)))
    print(k, "ok")

lines = ["INTERPLANAL CHAMPIONS: THE THRONE OF AVERNUS — MAP PACK", "Asmo, Pacts & Polyhedrals (Ben Vale)", "",
         "Twenty-three vector battlemaps for Interplanal Champions (D&D 5e, levels 12-17, Avernus): the six great maps",
         "of the 2020 original, rebuilt, plus seventeen location maps within them.", "",
         "FOLDERS", "  Gridless/   JPG, 100 pixels per 5-ft square. Use in any VTT; set the grid to 100 px.",
         "  Gridded/    The same maps with a printed grid, for print or theatre-of-the-mind reference.",
         "  Universal VTT (dd2vtt)/   Maps at 70 px per square with walls, doors and lights already placed.",
         "               Import with Foundry's 'Universal Battlemap Importer', Fantasy Grounds Unity, Arkenforge,",
         "               Owlbear Rodeo extensions and other Universal VTT readers.", "",
         "Foundry VTT users: the companion module 'Interplanal Champions' builds every scene for you, with",
         "walls, doors, lighting, journal pins and tokens. Install from:",
         "  https://github.com/pacts-and-polyhedrals/interplanal-champions/releases/latest/download/module.json", "",
         "MAP                                              SQUARES   FEET        WALLS DOORS LIGHTS"]
for b, w, h, fw, fh, nw, nd, nl in rows:
    lines.append(f"{b:<48} {w:>2}x{h:<3}   {fw:>3}x{fh:<4}   {nw:>4} {nd:>4} {nl:>5}")
lines += ["", "The Claw Rift is built to scroll: its left and right edges match, so two copies placed side by side",
          "join seamlessly for a chase that never ends.", "",
          "Licence: for personal use at your own table, including streamed games with credit. Do not redistribute.",
          "© 2026 Asmo, Pacts & Polyhedrals (Ben Vale)."]
open(f"{OUT}/READ ME.txt", "w").write("\n".join(lines))
