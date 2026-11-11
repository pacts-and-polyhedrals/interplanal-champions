"""Flag headings stranded at the foot of a column or page in a rendered PDF.

A heading is stranded when, in its own column, fewer than MIN_CHARS of text follow it before the footer.
Usage: python3 check_orphans.py file.pdf [file.pdf ...]
"""
import re, sys, html
import pypdfium2 as P
import pypdfium2.raw as R
from bs4 import BeautifulSoup

W = "/home/claude/ic/build/pdf"
MIN_CHARS = 60
FOOTER_TOP = 46  # pt above the page bottom: everything below is running footer


def headings():
    src = "".join(open(f"{W}/{n}.html").read() for n in ("front", "body", "back", "player_front", "player_body", "player_back"))
    soup = BeautifulSoup(src, "lxml")
    out = set()
    for h in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
        t = re.sub(r"\s+", " ", h.get_text()).strip()
        if len(t) >= 4:
            out.add(t)
    return sorted(out, key=len, reverse=True)


def fontname(tp, idx):
    import ctypes
    buf = ctypes.create_string_buffer(256)
    flags = ctypes.c_int()
    R.FPDFText_GetFontInfo(tp.raw, idx, buf, 256, ctypes.byref(flags))
    return buf.value.decode("latin-1", "ignore")


def check(path, heads):
    doc = P.PdfDocument(path)
    bad = []
    for pi in range(len(doc)):
        page = doc[pi]
        pw, ph = page.get_size()
        tp = page.get_textpage()
        full = tp.get_text_range()
        if not full.strip():
            continue
        seen = set()
        for h in heads:
            key = h[:40]
            if key.lower() not in full.lower():
                continue
            s = tp.search(key, match_case=False)
            hit = s.get_next()
            while hit:
                idx, cnt = hit
                l, b, r, t = tp.get_charbox(idx)
                l2, b2, r2, t2 = tp.get_charbox(idx + cnt - 1)
                if (round(l), round(b)) in seen:
                    hit = s.get_next()
                    continue
                seen.add((round(l), round(b)))
                bottom = min(b, b2)
                mid = pw / 2
                if r2 - l > pw * 0.55 or (l < mid - 20 and r2 > mid + 20):
                    x0, x1 = 20, pw - 20
                elif l < mid:
                    x0, x1 = 20, mid - 4
                else:
                    x0, x1 = mid + 4, pw - 20
                if "cinzel" not in fontname(tp, idx).lower() or bottom < FOOTER_TOP + 14:
                    hit = s.get_next()
                    continue
                norm = lambda z: re.sub(r"[^a-z0-9]", "", z.lower())
                line = norm(tp.get_text_bounded(left=x0, bottom=bottom + 1, right=x1, top=max(t, t2) - 1))
                if not line or not (line in norm(h) or norm(h) in line and len(line) <= len(norm(h)) + 4):
                    hit = s.get_next()
                    continue
                below = tp.get_text_bounded(left=x0, bottom=FOOTER_TOP, right=x1, top=bottom - 1).strip()
                if len(re.sub(r"\s+", "", below)) < MIN_CHARS and bottom < FOOTER_TOP + 90:
                    bad.append((pi + 1, h, len(below)))
                hit = s.get_next()
    return bad


if __name__ == "__main__":
    heads = headings()
    total = 0
    for f in sys.argv[1:]:
        bad = check(f, heads)
        total += len(bad)
        print(f"{f}: {len(bad)} stranded heading(s)")
        for p, h, n in bad:
            print(f"   p{p}: {h!r} ({n} chars after)")
    sys.exit(1 if total else 0)
