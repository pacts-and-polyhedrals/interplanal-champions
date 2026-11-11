"""Turn the Book I / Book II manuscripts (plain text, hard-wrapped) into journal HTML.

Paragraphs are re-flowed from the wrapped lines; headings, bullets, numbered lists and read-aloud blocks are recognised;
tables (which do not survive plain text) are replaced by hand-built HTML supplied by the caller.
"""
import re, html

WRAP = 104  # a manuscript line shorter than this ends a paragraph
RENAME = [("Hesper Valrick", "Hollis Valrick"), ("Hesper", "Hollis"), ("Interplanal Champion:", "Interplanal Champions:"),
          ("Original creator credit: Benjamin Vale (as printed on the 2020 Interplanal Champion cover).",
           "Original creator: Asmo, Pacts &amp; Polyhedrals (Ben Vale), as credited on the 2020 Interplanal Champion cover."),
          ("In the finished layout, include the user’s six original maps and original map-key annotations where readable.",
           "The six original maps are rebuilt in this module as full vector battlemaps that follow the 2020 layouts.")]


def esc(s):
    return html.escape(s, quote=False).replace("&amp;amp;", "&amp;")


def load(path):
    t = open(path, encoding="utf-8").read()
    for a, b in RENAME:
        t = t.replace(a, b)
    return [l.rstrip() for l in t.split("\n")]


def slice_lines(lines, start, end=None):
    """Lines from the first line starting with `start` up to (not including) the first later line starting with `end`."""
    a = next(i for i, l in enumerate(lines) if l.startswith(start))
    if end is None:
        return lines[a:]
    b = next(i for i, l in enumerate(lines) if i > a and l.startswith(end))
    return lines[a:b]


def inline(s):
    s = esc(s).replace("\x00", "<strong>").replace("\x01", "</strong>")
    s = re.sub(r"\b(DC \d+)", r"<strong>\1</strong>", s)
    return s


LABEL = re.compile(r"^(Article [IVXL]+\b|[A-Z][A-Za-z0-9’'&/ ()]{1,45}?( - |: |\. ))")
LEAD = re.compile(r"^(Article [IVXL]+ - [^.]{2,60}\.|[A-Z][A-Za-z0-9’'&/ ()-]{1,40}?:)(?= )")
SPLIT = [(r"\. (Our crown|Their crown): ", r".</p><p><strong>\1:</strong> ")]


RUNIN = re.compile(r"(?<=[.!?]) (?=[A-Z][A-Za-z’'-]*(?: [A-Za-z’'-]+){0,4}(?: \([^)]{1,45}\))?: )")
STATLABEL = re.compile(r"^([A-Z][a-z’'-]+(?: [A-Z][a-z’'-]+){0,3}(?: \([^)]{1,30}\))?)\. (?=[A-Z+])")


def runins(txt):
    """Split a paragraph that strings several labelled entries together ("Sessions: ... Place: ... Question: ...") into one
    paragraph per entry, and bold each label. A stat-block line ("Thorn Talon. Melee Spell Attack ...") gets a bold label."""
    parts = RUNIN.split(txt) if len(RUNIN.findall(txt)) >= 2 else [txt]
    out = []
    for k, p in enumerate(parts):
        if k > 0 or len(parts) > 1:
            m = re.match(r"^([^:\x00\x01]{1,60}?:)(?= )", p)
            if m and not p.startswith("\x00"):
                p = "\x00" + m.group(1) + "\x01" + p[len(m.group(1)):]
        if not p.startswith("\x00"):
            m = STATLABEL.match(p)
            if m:
                p = "\x00" + m.group(1) + ".\x01" + p[len(m.group(1)) + 1:]
        out.append(p)
    return out


def render(lines, *, headings=(), h3=(), tables=None, readaloud=None, skip_first=False):
    """lines -> html. headings/h3: line prefixes to render as h2/h3. tables: {start_prefix: (end_prefix, html)}.
    readaloud: {marker_prefix: end_prefix} — text after the marker line until end_prefix becomes a read-aloud box."""
    tables = tables or {}
    readaloud = readaloud or {}
    out, para, lst = [], [], None
    i = 1 if skip_first else 0

    def flush_para():
        nonlocal para
        if para:
            txt = " ".join(para).replace("- ", "-").replace("  ", " ")
            txt = re.sub(r"(\w)- (\w)", r"\1-\2", " ".join(para))
            if txt.count("; Article ") >= 3:
                head, rest = txt.split(": Article ", 1) if ": Article " in txt else ("", txt)
                items = ("Article " + rest).rstrip(".").split("; ")
                if head:
                    out.append(f"<p>{inline(head)}:</p>")
                out.append("<ul>" + "".join(f"<li>{inline(re.sub(r'^(Article [IVXL]+),', lambda m: chr(0) + m.group(1) + ':' + chr(1), x))}</li>"
                                            for x in items) + "</ul>")
                para = []
                return
            for piece in runins(txt):
                out.append(f"<p>{inline(piece)}</p>")
            para = []

    def flush_list():
        nonlocal lst
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            lst = None

    while i < len(lines):
        l = lines[i].strip()
        if not l:
            if not (para and len(lines[i - 1]) >= WRAP - 14):
                flush_para()
            i += 1; continue
        hit = next((k for k in tables if l.startswith(k)), None)
        if hit:
            flush_para(); flush_list()
            end, h = tables[hit]
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(end):
                j += 1
            out.append(h)
            i = j
            continue
        ra = next((k for k in readaloud if l.startswith(k)), None)
        if ra:
            flush_para(); flush_list()
            title = l.split(":", 1)[1].strip().capitalize() if ":" in l and l.split(":", 1)[1].strip() else "Read Aloud"
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].strip().startswith(readaloud[ra]):
                body.append(lines[j].strip())
                j += 1
            paras, cur = [], []
            for b in body:
                if not b:
                    continue
                cur.append(b)
                if len(b) < WRAP - 14:
                    paras.append(" ".join(cur)); cur = []
            if cur:
                paras.append(" ".join(cur))
            out.append('<blockquote class="rc-readaloud"><h4>' + esc(title) + "</h4>" +
                       "".join(f"<p>{inline(p)}</p>" for p in paras) + "</blockquote>")
            i = j
            continue
        if any(l.startswith(h) for h in headings):
            flush_para(); flush_list()
            out.append(f"<h2>{inline(l)}</h2>"); i += 1; continue
        caps = sum(c.isupper() for c in l) > 0.7 * max(1, sum(c.isalpha() for c in l))
        pref = any(l.startswith(h) for h in h3)
        if pref and len(l) >= 80:
            flush_para(); flush_list()
            m2 = re.match(r"^(.{3,70}?[:.])\s+(.*)$", l)
            if m2:
                lines[i] = "\x00" + m2.group(1) + "\x01 " + m2.group(2)
            pref = False
            l = lines[i].strip()
        if pref or (not caps and len(l) < 70 and not re.search(r"[.:;,?!’'\")]$", l) and l[0].isupper()
                                                 and not para and not l.startswith(("•",)) and not re.match(r"^\d+\.", l)
                                                 and len(l.split()) <= 11):
            flush_para(); flush_list()
            out.append(f"<h3>{inline(l)}</h3>"); i += 1; continue
        m = re.match(r"^•\s*(.*)", l)
        n = re.match(r"^(\d+)\.\s+(.*)", l)
        if m or n:
            flush_para()
            tag = "ul" if m else "ol"
            if lst and lst[0] != tag:
                flush_list()
            if not lst:
                lst = (tag, [])
            item = [m.group(1) if m else n.group(2)]
            j = i + 1
            while (len(lines[j - 1]) >= WRAP - 4 and j < len(lines) and lines[j].strip()
                   and not re.match(r"^(•|\d+\.\s)", lines[j].strip())):
                item.append(lines[j].strip()); j += 1
            lst[1].append(" ".join(item))
            i = j
            continue
        flush_list()
        if para and re.search(r"[.!?)”]$", lines[i - 1].strip()) and LABEL.match(l):
            flush_para()
            continue
        if not para:
            m3 = LEAD.match(l)
            if m3 and not l.startswith("\x00"):
                l = "\x00" + m3.group(1) + "\x01" + l[len(m3.group(1)):]
        para.append(l)
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        ncaps = nxt and sum(c.isupper() for c in nxt) > 0.7 * max(1, sum(c.isalpha() for c in nxt))
        if caps and ncaps:
            i += 1; continue
        if len(lines[i]) < WRAP - 14 or re.search(r"[:]$", l) and len(lines[i]) < WRAP:
            flush_para()
        i += 1
    flush_para(); flush_list()
    h = "".join(out)
    for a, b in SPLIT:
        h = re.sub(a, b, h)
    return h


def link_first(h, pairs):
    """Replace the first plain-text occurrence of each name (outside tags and headings) with a link."""
    for name, link in pairs:
        pat = re.compile(r"(<p>[^<]*?|<li>[^<]*?|</strong>[^<]*?|</em>[^<]*?)\b(" + re.escape(name) + r")\b")
        h, _ = pat.subn(lambda m: m.group(1) + link, h, count=1)
    return h
