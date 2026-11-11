"""HTML helpers for crimson-infernal journal pages."""
from lib5e import *

JOURNALS = []  # list of (jkey, name, folder, pages[(pkey, title, html)])


def scene_link(key, label):
    return f"@UUID[Scene.{fid('scene:' + key)}]{{{label}}}"


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def H(level, s):
    return f"<h{level}>{s}</h{level}>"


def RA(*lines, title="Read Aloud"):
    body = "".join(f"<p>{l}</p>" for l in lines)
    return f'<blockquote class="rc-readaloud"><h4>{title}</h4>{body}</blockquote>'


def SECRET(title, *paras):
    return f'<section class="rc-secret"><h4>{title}</h4>{"".join(f"<p>{x}</p>" for x in paras)}</section>'


def BOX(title, *paras, cls="rc-box"):
    return f'<div class="{cls}"><h4>{title}</h4>{"".join(f"<p>{x}</p>" for x in paras)}</div>'


def UL(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def OL(*items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def TABLE(head, rows, cls="rc-table"):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def SPEC(*pairs):
    return '<dl class="rc-spec">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in pairs) + "</dl>"


def IMG(src, cls="rc-portrait", alt=""):
    return f'<img class="{cls}" src="{src}" alt="{alt}">'


def BANNER(kicker, title, sub=""):
    return (f'<header class="rc-banner"><span class="rc-kicker">{kicker}</span><h1>{title}</h1>'
            + (f'<span class="rc-sub">{sub}</span>' if sub else "") + "</header>")


def wrap(html, cls="rc-journal"):
    return f'<div class="{cls}">{html}</div>'


def chk(skills, dc):
    return f"[[/check {skills} {dc}]]"


def sv(ability, dc):
    return f"[[/save {ability} {dc}]]"


def journal(jkey, name, folder, pages, sort=0, cls="rc-journal"):
    JOURNALS.append((jkey, name, folder, pages, sort, cls))


CHAPTER_ART = {("book1", "overview"): "intro", ("book1", "running"): "run", ("book1", "ch1"): "ch1", ("book1", "ch2"): "ch2",
               ("book1", "ch3"): "ch3", ("book1", "ch4"): "ch4", ("book1", "ch5"): "ch5", ("book1", "ch6"): "ch6",
               ("book1", "procedure"): "ref", ("book1", "npcs"): "appA", ("book1", "arena-engine"): "appB",
               ("book1", "app-c"): "appC", ("book1", "app-d"): "appF", ("book1", "design-audit"): "appH",
               ("book2", "cover"): "pintro", ("book2", "claimants"): "pheroes", ("book2", "ruby-court"): "popts",
               ("book2", "spells"): "pspells", ("book2", "relics"): "prelics", ("book2", "contracts"): "pho",
               ("book2", "rules"): "prules", ("handouts", "invitation"): "appC", ("pregens", "intro"): "pheroes",
               ("toolkit", "toolkit"): "appF", ("book1", "souljack-yard"): "interlude",
               ("book2", "soul-furnace"): "pfurnace"}


def chapter_art(jkey, pkey):
    k = CHAPTER_ART.get((jkey, pkey))
    return (f'<p class="ipc-chapart"><img src="modules/{MOD}/assets/art/chapters/{k}.webp" width="1600" height="520" '
            f'alt=""></p>') if k else ""


def build_docs():
    docs = []
    for jkey, name, folder, pages, sort, cls in JOURNALS:
        jid = fid("journal:" + jkey)
        ps = []
        for i, (pkey, title, html) in enumerate(pages):
            pid = fid("page:" + jkey + ":" + pkey)
            if html.startswith("@@PDF:"):
                ps.append({"_id": pid, "name": title, "type": "pdf", "sort": (i + 1) * 100000,
                           "title": {"show": True, "level": 1}, "src": html[6:], "ownership": {"default": -1},
                           "flags": {MOD: {"key": pkey}}, "_key": f"!journal.pages!{jid}.{pid}", "_stats": STATS})
                continue
            ps.append({"_id": pid, "name": title, "type": "text", "sort": (i + 1) * 100000,
                       "title": {"show": False, "level": 1},
                       "text": {"format": 1, "content": wrap(chapter_art(jkey, pkey) + html, cls)},
                       "ownership": {"default": -1}, "flags": {MOD: {"key": pkey}},
                       "_key": f"!journal.pages!{jid}.{pid}", "_stats": STATS})
        docs.append({"_id": jid, "name": name, "pages": ps, "folder": folder, "sort": sort,
                     "ownership": {"default": 0}, "flags": {MOD: {"key": jkey}},
                     "_key": f"!journal!{jid}", "_stats": STATS})
    return docs
