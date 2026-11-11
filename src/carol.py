"""'The Red Clause Is Coming to Town' — the Hearthlight Foundation's Midwinter jingle (lyrics by Asmo).

In the world it is the foundation's new words set to Fennick Holloway's stolen Lantern-Light Carol. At the table it is
sung to the tune of a familiar Christmas standard. It starts cheerful and curdles as the bells toll, verse by verse.
"""

# The chorus opening is written fresh so the lyric sheet carries none of the original song's words.
OPEN = ["He's watching while you're dreaming,", "He's counting while you wake,"]

SONG = [
    dict(key="v1", title="Verse 1 — A Very Merry Midwinter", mood="cheer", cue="Act I: the Carolling Snowmen, all day in the Market",
         lines=["The snow's falling down,", "The bells ring with cheer,", "There's presents for all,", "And nothing to fear!",
                "The Red Clause is coming to town!", "", "He's bringing you toys,", "He's bringing you treats,",
                "With magical gifts", "For everyone he meets!", "The Red Clause is coming to town!"]),
    dict(key="c1", title="Chorus — The Naughty List", mood="cheer", cue="Act I, after each verse (a clerk winces at line three)",
         lines=OPEN + ["He knows which deals you've signed in blood,", "And which souls he gets to take!"]),
    dict(key="v2", title="Verse 2 — Terms and Conditions", mood="cheer", cue="Act I: as the Nine Gifts are handed out",
         lines=["So open your gifts,", "And sign on the line,", "Just one little promise,", "And everything's fine!",
                "The Red Clause is coming to town!", "", "His elves are so sweet,", "His reindeer can fly,",
                "His contracts are binding,", "But don't ask him why!", "The Red Clause is coming to town!"]),
    dict(key="v3", title="Verse 3 — The First Bell", mood="turn", cue="Act II: Nightfall and the first collections (Bell IV)",
         lines=["The bells start to toll,", "The laughter runs dry,", "The toys turn their heads,", "As the children ask why…",
                "The Red Clause is coming to town.", "", "He's checking his books,", "He's counting each debt,",
                "And every small promise", "You'd rather forget…", "The Red Clause is coming to town."]),
    dict(key="c2", title="Chorus — The Infernal Collection", mood="turn", cue="Act II: hummed by everyone who accepted a gift",
         lines=OPEN + ["He knows every promise you've broken,", "And the price that you'll now pay!"]),
    dict(key="v4", title="Verse 4 — The Workshop", mood="dark", cue="Act III: the work song of the Assembly Line",
         lines=["The furnaces roar,", "The chains drag below,", "You'll work through the night,", "Where the sun cannot show!",
                "The Red Clause is coming to town!", "", "The workers all smile,", "Though tears fill their eyes,",
                "Their freedom was lost", "In a parcel of lies!", "The Red Clause is coming to town!"]),
    dict(key="bridge", title="Bridge — The Devil's in the Details", mood="dark", cue="Act III: the jars of the Ledger of Abandoned Souls",
         lines=["Your kindness is counted,", "Your goodness appraised,", "Your name's in the ledger,", "Your debt has been raised!",
                "", "You gave from your heart,", "But the contract was sealed,", "And now that you've questioned,",
                "The horrors are revealed!"]),
    dict(key="v5", title="Verse 5 — Final Arbitration", mood="hell", cue="Act IV: as the High Court opens its session",
         lines=["The ninth bell is near,", "The verdict draws nigh,", "Your soul's on the table,", "And Hell's standing by!",
                "The Red Clause is coming to town!", "", "So challenge his claims,", "And tear up his lies,",
                "Or sign on the line", "For your own soul's demise!", "The Red Clause is coming to town!"]),
    dict(key="c3", title="Final Chorus — The Last Collection", mood="hell", cue="Act IV: the whole court sings, the Red Clause conducting",
         lines=OPEN + ["He knows which deals you've signed in blood,", "And which souls he gets to take!"]),
    dict(key="outro", title="Outro — slower, whispered, then one booming laugh", mood="hell",
         cue="Phase II: The Smile Disappears",
         lines=["The presents were free…", "The paperwork's signed…", "Your appeal has been denied…", "And your soul is now mine…",
                "", "HO… HO… HO…", "THE RED CLAUSE IS COMING…", "TO TOWN!"]),
]

MOOD_STYLE = {"cheer": "rc-carol-cheer", "turn": "rc-carol-turn", "dark": "rc-carol-dark", "hell": "rc-carol-hell"}


def stanza_html(s, cue=False):
    body = "<br>".join(l if l else "" for l in s["lines"]).replace("<br><br>", "</p><p>")
    c = f'<span class="rc-carol-cue">{s["cue"]}</span>' if cue else ""
    return f'<div class="rc-stanza {MOOD_STYLE[s["mood"]]}"><h4>{s["title"]}</h4>{c}<p>{body}</p></div>'


def song_html(keys=None, cue=False):
    return "".join(stanza_html(s, cue) for s in SONG if keys is None or s["key"] in keys)


def by_key(k):
    return next(s for s in SONG if s["key"] == k)
