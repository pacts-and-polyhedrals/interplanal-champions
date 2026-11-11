"""Keep tables legible across page and column breaks, and fill the space a moved table leaves behind.

Rules:
* A table row is never split across a page or column.
* A table of up to KEEP_ROWS rows is kept whole; it moves to the next column or page if it doesn't fit.
* A longer table may run on, but only between rows, and its header row repeats.
* When a table moves and leaves an empty space at the foot of a column, the space gets a picture
  (or, if it's small, an ornament) instead of staying blank.
"""
import itertools
import re

from bs4 import BeautifulSoup

KEEP_ROWS = 18
PAGE_H, BOTTOM = 1056, 72          # letter, 0.75in bottom margin (CSS px)
MID_X = 408
MIN_ORN, MIN_ART = 70, 230         # gap sizes (px) for an ornament / a picture
SKIP = ("sheet", "scroll", "scroll-page", "handout-page", "creature", "cr-wrap", "statblock", "sb", "map-page", "rtable-wrap")

CSS = """
tr, li { break-inside: avoid; }
thead { display: table-header-group; }
table.keep-tbl { break-inside: avoid; }
.gapmark, .gapend { height: 0; margin: 0; padding: 0; }
.gapfill { box-sizing: border-box; break-inside: avoid; margin: 0; padding: 8px 0 10px; overflow: hidden; }
.gapfill.art div { box-sizing: border-box; width: 100%; height: 100%; border: 1.5px solid #b8862e; border-radius: 4px;
  background-size: cover; background-position: center; }
.gapfill.portrait div { box-sizing: border-box; width: 100%; height: 100%; border: 1.5px solid #b8862e; border-radius: 4px;
  background-color: rgba(120, 20, 30, 0.12); background-repeat: no-repeat; background-position: center;
  background-size: contain; }
.gapfill.orn { display: flex; align-items: center; justify-content: center; text-align: center; color: #b8862e;
  font-size: 15pt; letter-spacing: 6pt; }
"""


def prepare(html):
    """Mark every flowing table: keep short ones whole and drop an invisible marker before each."""
    soup = BeautifulSoup(html, "lxml")
    n = 0
    for t in soup.find_all("table"):
        if t.find_parent(class_=lambda c: c and any(k in c.split() for k in SKIP)):
            continue
        rows = len(t.find_all("tr"))
        if rows <= KEEP_ROWS:
            t["class"] = t.get("class", []) + ["keep-tbl"]
        prev = t.find_previous_sibling()
        if rows <= KEEP_ROWS and prev is not None and prev.name in ("h2", "h3", "h4", "h5") and "keep" not in (t.parent.get("class") or []):
            wrap = soup.new_tag("div", attrs={"class": "keep"})
            prev.insert_before(wrap)
            wrap.append(prev.extract())
            wrap.append(t.extract())
        anchor = t
        par = t.parent
        # a heading kept with its table: the marker goes before the whole group
        while par is not None and "keep" in (par.get("class") or []):
            anchor = par
            par = par.parent
        if anchor.find_previous_sibling() is not None and "gapmark" in (anchor.find_previous_sibling().get("class") or []):
            continue
        n += 1
        if not t.get("id"):
            t["id"] = f"gt{n}"
        m = soup.new_tag("div", attrs={"class": "gapmark", "id": f"gm{n}", "data-t": t["id"]})
        anchor.insert_before(m)
        e = soup.new_tag("div", attrs={"class": "gapend", "id": f"ge{n}", "data-rows": str(rows)})
        t.insert_after(e)
    body = soup.body
    return "".join(str(c) for c in body.children) if body else str(soup)


def _where(doc):
    pos = {}
    for i, p in enumerate(doc.pages):
        for k, v in p.anchors.items():
            x, y = v[0], v[1]
            if k not in pos:
                pos[k] = (i, 0 if x < MID_X else 1, y)
    return pos


def fill(html, doc, pictures):
    """Return (html, number_of_gaps_filled). pictures: list of (kind, path) with kind 'art' or 'portrait'."""
    pos = _where(doc)
    pool = itertools.cycle(pictures) if pictures else None
    filled = 0

    def rep(m):
        nonlocal filled
        gid, tid = m.group(1), m.group(2)
        if gid not in pos or tid not in pos:
            return m.group(0)
        p1, c1, y1 = pos[gid]
        p2, c2, y2 = pos[tid]
        if (p1, c1) == (p2, c2):
            return m.group(0)
        gap = PAGE_H - BOTTOM - y1 - 6
        if gap < MIN_ORN or gap > 860:
            return m.group(0)
        filled += 1
        if gap >= MIN_ART and pool:
            kind, src = next(pool)
            return (f'<div class="gapfill {kind}" id="f{gid}" style="height:{int(gap)}px"><div style="background-image:url(\'{src}\')">'
                    f'</div></div>')
        return f'<div class="gapfill orn" id="f{gid}" style="height:{int(gap)}px">✦ ✦ ✦</div>'
    out = re.sub(r'<div class="gapmark" data-t="([^"]+)" id="([^"]+)"></div>', lambda m: rep(_swap(m)), html)
    out = re.sub(r'<div class="gapmark" id="([^"]+)" data-t="([^"]+)"></div>', rep, out)
    return out, filled


class _swap:
    def __init__(self, m):
        self.m = m

    def group(self, i):
        return {0: self.m.group(0), 1: self.m.group(2), 2: self.m.group(1)}[i]


def report(html, doc):
    """List tables that still run across a column or page: (rows, start page, kept?)."""
    pos = _where(doc)
    out = []
    for m in re.finditer(r'<div class="gapend" data-rows="(\d+)" id="ge(\d+)"></div>|<div class="gapend" id="ge(\d+)" data-rows="(\d+)"></div>', html):
        rows, n = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
        t = re.search(r'<table[^>]*id="gt%s"' % n, html)
        a, b = pos.get(f"gt{n}"), pos.get(f"ge{n}")
        if a and b and (a[0], a[1]) != (b[0], b[1]):
            out.append((int(rows), a[0] + 1, "keep-tbl" in (t.group(0) if t else "")))
    return out
