"""Render the DMs Guild PDFs from build/pdf/*.html with WeasyPrint."""
import re, json, sys, os
sys.path.insert(0, "/home/claude/ic/tools")
import sheets as SHEETS
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

W = "/home/claude/ic/build/pdf"
F = "/home/claude/ic/art/fonts"
body = open(f"{W}/body.html").read()
front = open(f"{W}/front.html").read()
back = open(f"{W}/back.html").read()

SINGLE = ("appC", "appE", "appF", "appT", "pheroes", "ptpl", "pho")


def layout(body):
    """Wrap each chapter's flow in two columns, except full-page chapters; split columns at forced page breaks."""
    parts = re.split(r'(<h1 class="chapter" id="[^"]+">.*?</h1>)', body)
    out = [parts[0]]
    for i in range(1, len(parts), 2):
        head, content = parts[i], parts[i + 1]
        cid = re.search(r'id="([^"]+)"', head).group(1)
        if cid in SINGLE:
            out.append(head + f'<div class="single">{content}</div>')
        else:
            content = content.replace('<h2 class="newpage">', '</div><div class="cols newpage-cols"><h2 class="newpage">')
            out.append(head + f'<div class="cols">{content}</div>')
    return "".join(out)


body = layout(body)


def keep_with_next(html):
    """Wrap every heading with the headings/labels right after it and the first block of real content, so a heading
    can never sit alone at the foot of a column or page."""
    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(html, "lxml")
    SKIP = ("cr-wrap", "sheet", "scroll", "scroll-page", "handout-page", "keep", "creature")
    for h in soup.find_all(["h2", "h3", "h4", "h5"]):
        if h.find_parent(class_=lambda c: c and any(k in c.split() for k in SKIP)) or h.parent is None:
            continue
        group = [h]
        nxt = h.next_sibling
        while nxt is not None:
            if isinstance(nxt, NavigableString):
                if nxt.strip():
                    break
                nxt = nxt.next_sibling
                continue
            group.append(nxt)
            label = nxt.name in ("h2", "h3", "h4", "h5") or (nxt.name == "p" and "sp-type" in (nxt.get("class") or [])) \
                or (nxt.name == "p" and len(nxt.get_text()) < 60 and nxt.find(["i", "em"]) is not None and nxt.get_text().strip() == nxt.find(["i", "em"]).get_text().strip())
            if not label:
                break
            nxt = nxt.next_sibling
        if len(group) == 1:
            continue
        w = soup.new_tag("div", attrs={"class": "keep newpage" if "newpage" in (h.get("class") or []) else "keep"})
        h.insert_before(w)
        for g in group:
            w.append(g.extract())
    return str(soup.body)[6:-7]


body = keep_with_next(body)

FONTS = f"""
@font-face {{ font-family: Cinzel; src: url(file://{F}/cinzel-latin-700-normal.ttf); font-weight: 700; }}
@font-face {{ font-family: Cinzel; src: url(file://{F}/cinzel-latin-900-normal.ttf); font-weight: 900; }}
@font-face {{ font-family: Cinzel; src: url(file://{F}/cinzel-latin-400-normal.ttf); font-weight: 400; }}
@font-face {{ font-family: CinzelDeco; src: url(file://{F}/cinzel-decorative-latin-900-normal.ttf); }}
@font-face {{ font-family: Garamond; src: url(file://{F}/eb-garamond-latin-400-normal.ttf); }}
@font-face {{ font-family: Garamond; src: url(file://{F}/eb-garamond-latin-400-italic.ttf); font-style: italic; }}
@font-face {{ font-family: Garamond; src: url(file://{F}/eb-garamond-latin-600-normal.ttf); font-weight: 700; }}
@font-face {{ font-family: Garamond; src: url(file://{F}/eb-garamond-latin-600-italic.ttf); font-weight: 700; font-style: italic; }}
@font-face {{ font-family: Fell; src: url(file://{F}/im-fell-english-latin-400-normal.ttf); }}
@font-face {{ font-family: Fell; src: url(file://{F}/im-fell-english-latin-400-italic.ttf); font-style: italic; }}
"""


def theme(dark):
    bg = "#140709" if dark else "#fbf5e9"
    ink = "#ecdcc4" if dark else "#241312"
    dim = "#b9a88c" if dark else "#6a5040"
    head = "#ff8a6a" if dark else "#8e1424"
    gold = "#d8aa52" if dark else "#8a6418"
    box = "rgba(60,10,16,0.9)" if dark else "#f3e0d6"
    sec = "#1c0a0c" if dark else "#efe6d6"
    sb = "#1e0c0c" if dark else "#fdf1dc"
    sbline = "#b3122a" if dark else "#8e1424"
    return f"""
{FONTS}
@page {{ size: letter; margin: 0.65in 0.6in 0.75in; background: {bg};
  @bottom-center {{ content: counter(page); font-family: Cinzel; font-size: 9pt; color: {gold}; }}
  @bottom-left {{ content: "Interplanal Champions"; font-family: Cinzel; font-size: 7.5pt; color: {dim}; }}
  @bottom-right {{ content: string(chap); font-family: Cinzel; font-size: 7.5pt; color: {dim}; }} }}
@page :first {{ counter-reset: page 0; }}
@page full {{ margin: 0; @bottom-center {{ content: none; }} @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
@page land {{ size: letter landscape; margin: 0.45in; }}
html {{ font-family: Garamond; font-size: 10pt; line-height: 1.38; color: {ink}; }}
p {{ margin: 0 0 0.55em; orphans: 2; widows: 2; text-align: justify; hyphens: auto; }}
.cover, .backcover {{ page: full; break-after: page; }} .cover img, .backcover img {{ width: 8.5in; height: 11in; display: block; }}
.backcover {{ break-before: page; }}
.credits {{ break-after: page; padding-top: 1.2in; text-align: center; }}
.credits h2 {{ font-family: CinzelDeco; font-size: 26pt; color: {head}; border: none; }}
.credits .tag {{ font-family: Fell; font-style: italic; font-size: 13pt; color: {gold}; }}
.credits p {{ text-align: center; }}
.blurb {{ margin: 0.4in 0.8in; font-family: Fell; font-size: 12pt; color: {head}; }}
.legal {{ font-size: 7pt; color: {dim}; margin-top: 1.4in; text-align: justify !important; }}
.toc {{ break-after: page; }} .toc h2 {{ font-family: CinzelDeco; font-size: 24pt; color: {head}; text-align: center; border: none; }}
.toc ul {{ list-style: none; padding: 0; margin: 0.3in 0.5in; }}
.toc li {{ font-family: Cinzel; font-size: 12pt; padding: 6pt 0; border-bottom: 1px dotted {gold}; }}
.toc a {{ color: {ink}; text-decoration: none; }} .toc a::after {{ content: leader(' ') target-counter(attr(href), page); color: {gold}; }}
h1.chapter .ct {{ string-set: chap content(text); }}
h1.chapter {{ break-before: page; font-family: CinzelDeco; font-size: 30pt; color: {head}; text-align: center;
  margin: 0.2in 0 0.25in; padding-bottom: 8pt; border-bottom: 3px double {gold}; }}
h1.chapter .chapart {{ display: block; margin: 8pt 0 0; }} h1.chapter .chapart img {{ display: block; width: 100%; border-radius: 3pt; }}
h1.chapter .kick {{ display: block; font-family: Cinzel; font-size: 10pt; letter-spacing: 4pt; color: {gold}; }}
.cols {{ columns: 2; column-gap: 0.28in; column-fill: auto; }}
h2 {{ font-family: Cinzel; font-weight: 900; font-size: 14pt; color: {head}; border-bottom: 2px solid {sbline}; margin: 0.6em 0 0.35em; break-after: avoid; }}
h3 {{ font-family: Cinzel; font-weight: 700; font-size: 11.5pt; color: {gold}; margin: 0.55em 0 0.25em; break-after: avoid; }}
h4 {{ font-family: Cinzel; font-weight: 700; font-size: 9.5pt; color: {head}; margin: 0.4em 0 0.2em; letter-spacing: 0.5pt; break-after: avoid; }}
h5 {{ break-after: avoid; }} h2 + ul li:first-child, h3 + ul li:first-child, h4 + ul li:first-child {{ break-after: avoid; }} li {{ break-inside: avoid; }}
strong, b {{ color: {"#ffd9a8" if dark else "#5a0a10"}; }}
ul, ol {{ margin: 0 0 0.55em; padding-left: 1.2em; }} li {{ margin-bottom: 0.2em; }}
code {{ font-size: 8.5pt; color: {head}; }}
.rc-banner {{ column-span: all; text-align: center; padding: 10pt; margin: 0 0 10pt; border-top: 2px solid {gold}; border-bottom: 2px solid {gold}; background: {sec}; }}
.rc-banner h1 {{ font-family: CinzelDeco; font-size: 22pt; color: {head}; margin: 2pt 0; }}
.rc-kicker {{ font-family: Cinzel; font-size: 8pt; letter-spacing: 3pt; color: {gold}; }} .rc-sub {{ display: block; font-family: Fell; font-style: italic; font-size: 10.5pt; }}
.rc-tagline {{ font-family: Fell; font-style: italic; font-size: 11pt; text-align: center; color: {head}; }}
.rc-readaloud {{ break-inside: avoid-page; margin: 0.6em 0; padding: 7pt 9pt 3pt; background: {box}; border-left: 4px solid {sbline};
  font-family: Fell; font-size: 10pt; {"box-shadow: 0 0 6pt rgba(179,18,42,0.5);" if dark else ""} }}
.rc-readaloud h4 {{ font-size: 7.5pt; letter-spacing: 2pt; margin: 0 0 3pt; }} .rc-readaloud p {{ text-align: left; margin-bottom: 0.35em; }}
.rc-secret {{ break-inside: avoid; margin: 0.6em 0; padding: 6pt 8pt 2pt; border: 1px dashed {sbline}; background: {sec}; }}
.rc-secret h4::before {{ content: "☩ DM ONLY · "; color: {gold}; }}
.rc-box {{ break-inside: avoid; margin: 0.6em 0; padding: 6pt 8pt 2pt; border: 1px solid {gold}; background: {sec}; }}
.rc-box h4 {{ color: {gold}; }}
table {{ width: 100%; border-collapse: collapse; margin: 0.5em 0 0.8em; font-size: 8.8pt; break-inside: auto; }}
th {{ background: {"#5e0b18" if dark else "#8e1424"}; color: #ffe8c8; font-family: Cinzel; font-size: 7.8pt; text-align: left; padding: 3pt 4pt; }}
td {{ padding: 3pt 4pt; border-bottom: 1px solid {"#3a1418" if dark else "#d8c4a8"}; vertical-align: top; }}
tr:nth-child(even) td {{ background: {"rgba(179,18,42,0.08)" if dark else "#f6e8d8"}; }}
.rc-spec {{ display: block; padding: 5pt 8pt; border-top: 2px solid {sbline}; border-bottom: 2px solid {sbline}; background: {sec}; }}
.rc-spec dt {{ font-family: Cinzel; font-weight: 700; color: {gold}; float: left; clear: left; width: 1.15in; }} .rc-spec dd {{ margin: 0 0 2pt 1.2in; }}
.rc-arc {{ display: flex; gap: 3pt; }} .rc-arc span {{ flex: 1; text-align: center; font-family: Cinzel; font-size: 8pt; color: #fff; padding: 4pt 2pt; }}
.rc-arc span:nth-child(1) {{ background: #2f7a46; }} .rc-arc span:nth-child(2) {{ background: #8a6a2a; }} .rc-arc span:nth-child(3) {{ background: #7a1424; }} .rc-arc span:nth-child(4) {{ background: #2a0408; }}
.rc-portrait {{ float: right; width: 1.25in; margin: 0 0 5pt 7pt; border: 2px solid {gold}; }}
.rc-right {{ float: right; }}
.rc-check {{ list-style: none; padding-left: 0; }} .rc-check li::before {{ content: "☐ "; color: {gold}; }}
.rc-closing {{ text-align: center; font-family: Fell; font-style: italic; font-size: 12pt; color: {head}; }}
.xref {{ font-weight: 700; color: {"#ffcfa8" if dark else "#6a0a14"}; }}
.vtt {{ font-variant: small-caps; color: {gold}; }}
.vtt::before {{ content: "✦"; font-size: 7pt; margin-right: 1pt; }}
/* stat blocks */
.creature {{ break-inside: avoid; margin-top: 0.6em; }} .creature p {{ font-size: 9pt; }}
.sb-portrait {{ float: left; width: 1.05in; margin: 0 7pt 4pt 0; border: 2px solid {gold}; }}
.keep {{ break-inside: avoid; }} .keep > *:last-child {{ margin-bottom: 0.4em; }} h2.newpage, .keep.newpage, .newpage-cols {{ break-before: page; }}
.cr-wrap {{ break-inside: avoid; }} .cr-wrap.long {{ break-inside: auto; }} .cr-wrap.long .creature {{ break-after: avoid; }}
.statblock {{ clear: both; background: {sb}; border-top: 4px solid {sbline}; border-bottom: 4px solid {sbline}; padding: 5pt 7pt; margin: 0.4em 0 1em;
  font-size: 8.8pt; {"box-shadow: 0 0 6pt rgba(0,0,0,0.6);" if dark else "box-shadow: 0 0 4pt #c8a878;"} }}
.statblock p {{ margin: 0 0 3pt; text-align: left; }} .statblock hr {{ border: none; border-top: 2px solid {sbline}; margin: 4pt 0; }}
.sb-name {{ font-family: CinzelDeco; font-size: 12.5pt; color: {head}; margin: 0; letter-spacing: 0; }} .sb-type {{ margin: 0; font-size: 8.5pt; }}
.sb-sec {{ font-family: Cinzel; font-size: 10pt; color: {head}; border-bottom: 1px solid {sbline}; margin: 6pt 0 3pt; }}
.sb-ab {{ margin: 2pt 0; font-size: 8.3pt; text-align: center; }} .sb-ab th {{ text-align: center; background: none; color: {head}; padding: 1pt; }}
.sb-ab td {{ text-align: center; border: none; padding: 1pt; background: none !important; }}
.spell, .item {{ break-inside: avoid; margin-bottom: 0.8em; }} .sp-type {{ margin: -2pt 0 3pt; font-size: 8.8pt; }}
.spell h4, .item h4 {{ font-size: 10.5pt; }}
.rc-spell-classes {{ font-size: 8.5pt; color: {dim}; }}
.subclass h3 {{ font-size: 13pt; }}
.rtable {{ break-inside: avoid; }} .die {{ width: 0.4in; font-family: Cinzel; font-weight: 700; color: {head}; }}
/* pregens */
.pregen {{ break-before: page; border-top: 8px solid var(--pc); padding-top: 6pt; }}
.pregen h2 {{ font-family: CinzelDeco; font-size: 20pt; border: none; margin: 0; }} .pc-sub {{ font-family: Cinzel; font-size: 9pt; color: {gold}; }}
.pregen p {{ font-size: 9pt; line-height: 1.3; margin-bottom: 0.4em; }}
.pc-portrait {{ float: right; width: 1.9in; margin: 0 0 8pt 10pt; border: 3px solid var(--pc); }}
.pc-ab {{ width: 60%; font-size: 10pt; }} .pc-ab td {{ border: 1px solid {gold}; }} .pc-line {{ font-size: 10.5pt; }}
/* handouts */
.handout-page {{ break-after: page; }} .ho-label {{ font-family: Cinzel; font-size: 8pt; color: {dim}; text-align: center; letter-spacing: 2pt; }}
.rc-handout {{ position: relative; color: #2a1408; background: #f1e1bf; border: 3px double #6a3a16; padding: 22pt 28pt 40pt; font-family: Fell; font-size: 11.5pt; min-height: 6in; }}
.rc-handout h2 {{ color: #7a0a14; border-bottom: 2px double #7a0a14; text-align: center; font-size: 16pt; }}
.rc-handout b, .rc-handout strong {{ color: #5a0a10; }} .rc-handout td {{ color: #2a1408; border-color: #b08a5a; }} .rc-handout tr:nth-child(even) td {{ background: #ead6ae; }}
.rc-handout p {{ text-align: left; }}
.rc-form {{ text-align: center !important; font-family: Cinzel; font-size: 8.5pt; letter-spacing: 2pt; }}
.rc-sig {{ font-style: italic; text-align: right !important; }} .rc-sigline {{ font-family: Cinzel; font-size: 9pt; }}
.rc-red {{ color: #a00a14 !important; font-weight: 700; }}
.rc-stamp {{ position: absolute; right: 22pt; bottom: 14pt; transform: rotate(-12deg); font-family: Cinzel; font-weight: 900; font-size: 18pt; color: rgba(160,10,20,0.75); border: 4px double rgba(160,10,20,0.75); padding: 1pt 8pt; }}
.rc-infernal {{ background: #2a0608; color: #f4d8b8; border-color: #b3122a; }} .rc-infernal h2 {{ color: #ffb38a; }} .rc-infernal b, .rc-infernal strong {{ color: #ffd9a8; }}
.rc-blueprint {{ background: #1c3a64; color: #dcefff; }} .rc-blueprint h2 {{ color: #fff; border-color: #9fc6e8; }} .rc-blueprint b, .rc-blueprint strong {{ color: #fff; }}
.rc-invite {{ text-align: center !important; font-family: CinzelDeco; font-size: 20pt; color: #ffd27a; margin: 1in 0 0.4in; }}
.rc-bells {{ text-align: center; margin: 14pt 0; }} .rc-bells span {{ display: inline-block; width: 26pt; height: 26pt; line-height: 26pt; margin: 2pt; border-radius: 13pt; border: 2px solid #d8aa52; color: #d8aa52; font-family: Cinzel; font-weight: 900; text-align: center; }}
.rc-bells span.rung {{ background: #b3122a; color: #fff; }}
.rc-ledger th {{ width: 34%; }}
/* maps */
.map-page {{ break-before: page; text-align: center; }} .map-page.land {{ page: land; }}
.map-page img {{ max-width: 100%; max-height: 7.6in; border: 2px solid {gold}; }} .map-page.land img {{ max-height: 5.55in; }} .map-page.land .map-key {{ columns: 3; font-size: 7.6pt; }}
.map-page h3 {{ font-size: 14pt; margin-top: 0; }} .map-meta {{ text-align: center; font-family: Cinzel; font-size: 8.5pt; color: {dim}; }}
.map-key {{ text-align: left; columns: 2; font-size: 8.5pt; margin-top: 6pt; }}
.single p {{ text-align: left; }}
.rc-npc {{ display: block; }} .rc-thumb {{ width: 0.8in; float: left; margin-right: 6pt; }}
.rc-codex {{ }}
.rc-backcover {{ text-align: center; }} .rc-motto {{ font-family: CinzelDeco; font-size: 13pt; color: {gold}; text-align: center !important; }}
img {{ image-rendering: auto; }}


.rc-stanza {{ margin: 5pt 0; padding: 3pt 8pt; border-left: 3pt solid {gold}; border-radius: 3pt; break-inside: avoid; }}
.rc-stanza h4 {{ margin: 0 0 2pt; }}
.rc-stanza p {{ font-family: Fell; font-style: italic; font-size: 10.5pt; line-height: 1.32; text-align: left; margin: 0 0 4pt; }}
.rc-carol-cue {{ display: block; font-family: Cinzel; font-size: 6.5pt; letter-spacing: 1pt; color: {gold}; margin-bottom: 2pt; }}
.rc-carol-cheer {{ border-color: #2f7a46; background: rgba(47,122,70,0.13); }}
.rc-carol-turn {{ border-color: #b8862e; background: rgba(184,134,46,0.13); }}
.rc-carol-dark {{ border-color: #8e1424; background: rgba(142,20,36,0.15); }}
.rc-carol-hell {{ border-color: #ff4a1a; background: rgba(120,8,12,0.22); }}
.rc-carol-hell p {{ font-style: normal; font-weight: bold; }}
.rc-songbook .rc-carol-sub {{ text-align: center; font-style: italic; }}
.rc-songbook h4 {{ color: #7a0a14 !important; }} .rc-songbook .rc-carol-sub {{ font-size: 9pt; }}
.rc-songbook-full {{ columns: 3; column-gap: 0.18in; }} .rc-songbook-full h2, .rc-songbook-full .rc-carol-sub {{ column-span: all; }}
.rc-songbook-full .rc-stanza {{ padding: 2pt 5pt; margin: 3pt 0; }} .rc-songbook-full .rc-stanza h4 {{ font-size: 7.4pt; }}
.rc-songbook-full .rc-stanza p {{ font-size: 8.6pt; line-height: 1.18; margin-bottom: 2pt; }}

.credits .thanks {{ margin: 0.25in 0.9in 0; font-size: 10pt; text-align: center; font-style: italic; color: {head}; }} .credits .thanks em {{ font-style: normal; }}
@page scroll {{ margin: 0.3in 0.45in 0.45in; }}
.scroll-page {{ page: scroll; break-before: page; }}
.scroll {{ width: 6.9in; margin: 0 auto; }}
.roll {{ height: 0.42in; border-radius: 0.21in; background: linear-gradient(#4a2410, #b07a40 30%, #e8c890 48%, #9a6630 70%, #3a1a08); border: 1.5px solid #2a1206; position: relative; margin: 0 -0.25in; }}
.roll::before, .roll::after {{ content: ""; position: absolute; top: 0.04in; width: 0.34in; height: 0.34in; border-radius: 50%; background: radial-gradient(circle at 40% 35%, #f0d080, #a07020 55%, #4a2a08); border: 1px solid #2a1206; }}
.roll::before {{ left: -0.2in; }} .roll::after {{ right: -0.2in; }}
.scroll-body {{ position: relative; background: linear-gradient(90deg, #d9bf8c, #f3e4c2 8%, #f8ecd2 50%, #f3e4c2 92%, #d9bf8c); border-left: 1px solid #a07a48; border-right: 1px solid #a07a48;
  margin: -0.06in 0; padding: 18pt 30pt 64pt; min-height: 8.2in; color: #2a1408; font-family: Fell; font-size: var(--fs, 12.4pt); line-height: 1.42; }}
.scroll-body h2 {{ font-family: CinzelDeco; color: #7a0a14; text-align: center; font-size: 17pt; border-bottom: 2px double #7a0a14; padding-bottom: 4pt; margin: 0 0 10pt; column-span: none; }}
.scroll-body h3 {{ font-family: Cinzel; color: #7a0a14; font-size: 11pt; margin: 8pt 0 3pt; }}
.scroll-body p, .scroll-body li {{ text-align: justify; color: #2a1408; font-family: Fell; font-size: var(--fs, 12.4pt); margin-bottom: 0.45em; }}
.scroll-body.dense {{ padding: 12pt 24pt 60pt; }} .scroll-body.dense h2 {{ font-size: 14pt; margin-bottom: 6pt; }}
.scroll-cols {{ columns: 2; column-gap: 0.25in; column-rule: 1px solid #c8a878; }} .scroll-cols p, .scroll-cols li {{ text-align: left; }}
.scroll-body ul {{ margin: 0 0 0.4em; padding-left: 1.2em; }} .scroll-body li {{ margin-bottom: 0.15em; }}
.scroll-body b, .scroll-body strong {{ color: #5a0a10; }} .scroll-body em, .scroll-body i {{ color: #3a1a0a; }}
.scroll-body .xref {{ color: #6a0a14 !important; font-weight: 700; border: none; background: none; }}
.scroll-body table {{ width: 100%; }} .scroll-body td {{ color: #2a1408; border-color: #b08a5a; background: none !important; }}
.scroll-body .rc-sigline {{ margin-top: 14pt; font-family: Fell; }}
.seal {{ position: absolute; right: 22pt; bottom: 8pt; width: 0.64in; height: 0.64in; border-radius: 50%; text-align: center; line-height: 0.64in; font-size: 22pt; color: #f0c0a0;
  background: radial-gradient(circle at 38% 32%, #c02030, #7a0a14 60%, #4a0408); box-shadow: 0 0 0 3px #7a0a1466; }}
.rc-handout .xref {{ color: #6a0a14 !important; font-weight: 700; }}
.xref-note {{ column-span: all; }}
"""


# Names for the closing "With Thanks" art page (added only when a book needs one more page to reach an even count).
PLAYTESTERS = ["Tim", "Alex", "Heather", "Kai"]


def _thanks_img():
    out = f"{W}/img/thanks.jpg"
    sys.path.insert(0, "/home/claude/ic/art")
    import chapterart
    chapterart.thanks_page(out, PLAYTESTERS)
    return out


import glob
import tablefit as TF
PICTURES = [("art", f) for f in sorted(glob.glob(f"{W}/img/assets_art_chapters_*.jpg"))]


def render(name, html, dark, even=True):
    """Render a book. Print rule: every book has an even number of pages. If it comes out odd, a full-page
    'With Thanks' art piece is inserted before the back cover (or at the end, if there is no back cover)."""
    fc = FontConfiguration()
    sheets = [CSS(string=theme(dark), font_config=fc), CSS(string=SHEETS.CSS, font_config=fc), CSS(string=TF.CSS, font_config=fc)]
    html = TF.prepare(html)

    def build(h):
        doc = f"<html><head><meta charset='utf-8'><title>Interplanal Champions</title></head><body>{h}</body></html>"
        return HTML(string=doc, base_url=W).render(stylesheets=sheets, font_config=fc, optimize_images=True, jpeg_quality=85)
    d = build(html)
    for _ in range(3):                      # fill the space a moved table leaves, then check again
        html, n = TF.fill(html, d, PICTURES)
        if not n:
            break
        d = build(html)
    if even and len(d.pages) % 2:
        page = f'<section class="backcover thanks"><img src="{_thanks_img()}"></section>'
        i = html.rfind('<section class="backcover">')
        html = html[:i] + page + html[i:] if i >= 0 else html + page
        d = build(html)
    sp = TF.report(html, d)
    print(f"    tables running across a break (between rows, header repeated): {[(r, pg) for r, pg, _ in sp]}")
    d.write_pdf(name)
    print(f"  {os.path.basename(name)}: {len(d.pages)} pages")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = "/home/claude/ic/dist/dmsguild"
    import os
    os.makedirs(out, exist_ok=True)
    full = front + body + back
    if which in ("all", "screen"):
        render(f"{out}/Interplanal Champions - Book I (GM).pdf", full, True)
    if which in ("all", "print"):
        render(f"{out}/Interplanal Champions - Book I (GM, Printer Friendly).pdf", full.replace(f'<section class="cover"><img src="{W}/img/cover.jpg"></section>', f'<section class="cover"><img src="{W}/img/cover.jpg"></section>'), False)
    if which in ("all", "player"):
        pb = keep_with_next(layout(open(f"{W}/player_body.html").read()))
        render(f"{out}/Interplanal Champions - Book II (Player's Guide).pdf",
               open(f"{W}/player_front.html").read() + pb + open(f"{W}/player_back.html").read(), True)
    if which in ("all", "sheets"):
        sh = SHEETS.all_sheets(lambda k: f"/home/claude/ic/module/assets/portraits/pc-{k}.webp")
        render(f"{out}/Interplanal Champions - Claimant Character Sheets.pdf", sh, False)
    print("done")


def preview():
    raw = open(f"{W}/body.html").read()
    act = raw[:raw.index('<h1 class="chapter" id="ch2"')]
    cr = re.search(r'<div class="cr-wrap[^"]*">.*?</div></div>(?=<div class="cr-wrap)', raw[raw.index("Janella Greenbottle, Golemancer") - 3000:], re.S)
    cr = cr.group(0) if cr else ""
    mp = re.search(r'<section class="map-page[^"]*"><h3>Plate 1:.*?</section>', raw, re.S).group(0)
    ho = re.search(r'<section class="handout-page">.*?</section>', raw, re.S).group(0)
    teaser = ('<h1 class="chapter" id="more"><span class="kick">Preview</span><span class="ct">And Much More…</span></h1>'
              '<div class="cols"><p>The full campaign continues through Greyhurst and the mansion of the Lemure King, the War of Claims, '
              'the Brass Citadel and the coup of the Vacant King, the Hag Queen\'s Due and the optional mythic battle against Misty, '
              'and the Rite of the Nine, plus the Redline Run: a soul-fuelled vehicle chase through the Claw Rift. 45 creatures, four '
              'infernal war machines, 23 battlemaps, roll tables, the Championship Charter and eight contract forms. Book II adds six level-12 claimants, three subclasses, seventeen spells, fourteen relics and the Soul Furnace rules.</p></div>'
              + f'<div class="cols">{cr}</div><div style="break-before: page"></div>' + ho)
    body_ = act + teaser + mp
    parts = re.split(r'(<h1 class="chapter" id="[^"]+">.*?</h1>)', body_)
    o = [parts[0]]
    for i in range(1, len(parts), 2):
        cid = re.search(r'id="([^"]+)"', parts[i]).group(1)
        o.append(parts[i] + (parts[i + 1] if cid == "more" else f'<div class="cols">{parts[i + 1]}</div>'))
    fr = re.sub(r'<section class="toc">.*?</section>', "", front, flags=re.S)
    render("/home/claude/ic/dist/dmsguild/Interplanal Champions - Preview.pdf", fr + "".join(o) + back, True)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "preview":
    preview()
