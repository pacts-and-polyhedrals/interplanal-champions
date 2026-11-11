"""Backstories, sheet details and tactics for the six level-12 claimants (Book II, Section 8)."""

PROLOGUE = [
    "Midwinter in Waterdeep. Snow on the courthouse steps, and inside, the Brass Arbiter's verdict fell "
    "like a portcullis. The Hearthlight Foundation's charity had been a harvest of souls from the first "
    'signature. The Red Clause was void. The ruling, <strong>Precedent H-25</strong>, held that Hell may '
    'enforce a true bargain but may never forge consent.',
    'Six strangers stood in that courtroom. Two testified to how the fraud was built. One kept the doors.'
    ' One pressed her seal into the verdict. The last two had crossed the planes to beg help for a '
    'village Hell had swallowed, and were sent away with nothing.',
    'That night each of them found a red envelope sealed with nine black thorns. Asmodeus had opened the '
    'throne of Avernus to any claimant who could prove Survival, Deviousness and Dominion under a Charter'
    ' written for all to read. Six claimants, six reasons to sign, and each of them already knows too '
    'much about the others.',
]

LORE = {
    "aurelia": dict(
        role="<strong>The Advocate.</strong> You read the clauses no one else reads, argue the party's case before"
             " Hell's courts, and unpick enemy magic from the back line.",
        backstory=[
            "For six years Aurelia Quill was the Hearthlight Foundation's compliance attorney in Waterdeep. She "
            'checked the sums, the signatures and the seals, initialled every form, and never asked what the '
            'forms were for. She had been told they were charity. She believed it.',
            'On the second day of the Red Clause hearing, the Brass Arbiter laid three forged default notices '
            'before her. Her initials were on every one. She could have claimed forgery. Instead she testified to'
            ' all of it, lost her licence within the week, and walked out into the snow with nothing but her '
            'notes and her name.',
            'Her patron found her a month later. The <strong>Ruby Court</strong> is neither god nor devil; it is '
            'judgment itself, grown cold and patient enough to bargain. It gave her three powers: to witness a '
            'promise, to suspend it, and to enforce it. Nothing more. She has not forgotten how blind she was, '
            'and she does not mean to be blind again.',
        ],
        tonight="You want the power to say what is true in Avernus. Once Hell's records can be audited, a second Red "
                'Clause becomes impossible. You helped build the last fraud without seeing it. You will see the next '
                'one coming.',
        tie='Tobin Marsh, a Waterdeep baker and once your client, signed a soul bargain that was never part of '
            'the fraud. It is genuine, and Precedent H-25 cannot touch it. You swore to him you would find a way.'
            ' Breaking it will cost someone a real price. And the deeper the Championship drags you, the more you'
            ' want to be the judge no one can overrule. That frightens you more than any devil.',
        knows='<strong>If you rule alone,</strong> you will found a Court of Review that can audit any contract in '
              'Avernus. <strong>If the party shares the crown,</strong> you draft the rules the council votes by. '
              "<strong>If you back someone else,</strong> you stand as advocate for the Brass Arbiter's "
              'independence.',
        others=[
            ('Orren Fenwick',
             'He built the registry your forms ran through. You damned him in open court. He never argued back, '
             'and that was worse.'),
            ('Dame Caldris Vowborne',
             "The Arbiter's bailiff. When Hearthlight's creditors came for you on the courthouse steps, she filled"
             ' the doorway until they left.'),
            ('Sister Nema Copperwrit',
             'She took down your testimony word for word. She knows everything you confessed.'),
            ('Varka Blackseal',
             'You pressed your card into her hand when the court turned her away. She has never used it.'),
            ('Ilyra Ashroot',
             "She asked how long a contract should last. You said, 'As long as it is written.' She looked at you "
             'with pity.'),
        ],
        table='Stay 30–60 feet back, deploy one meaningful control spell per fight, use three <em>eldritch '
              'blast</em> beams as a reliable action, and spend reactions on <em>counterspell</em> or your level-10'
              ' reroll. Use <em>audit the false</em> for investigation rather than treating it as an instant combat'
              ' win.',
        goal='At 14 gain Final Notice; at 15–17 select higher Mystic Arcanum appropriate to a legalist and improve'
             ' defensive invocations. Build as a control-and-evidence specialist rather than a damage-only '
             'blaster.',
    ),
    "varka": dict(
        role='<strong>The Shield.</strong> You stand in the front rank, take the blows meant for others, and keep '
             'the party breathing long enough to win. When the powerful forget the people beneath them, you remind'
             ' them.',
        backstory=[
            'For eleven years Varka Blackseal worked the lip of a planar wound where the Blood War bleeds into '
            'the world. When the rift tore wider, people fell through it: refugees, deserters, children, down '
            'into ash and screaming dark. Varka went after them with a rope, an iron rescue hook and her '
            "grandmother's banner. No one has counted how many she carried out. She has.",
            "Then <strong>Greyhurst</strong> fell. It was a village a day's ride from the wound, with bells, a "
            'ferry and a mill. In a single hour it was gone, every house and every soul dragged down into '
            "Avernus. Varka reached the empty field at dawn. She has carried the list of Greyhurst's missing ever"
            ' since, and it grows each time she passes a notice board.',
            'Her rage is a vow. Before every fight she names aloud what she will protect, and the Blood-Price '
            'makes her bleed if she lets it go. She has never broken a vow by choice. She broke one by failing, '
            'and a devil keeps the paper.',
        ],
        tonight="You took Ilyra to Waterdeep to beg the Brass Arbiter's help for Greyhurst. The court said it had no "
                "jurisdiction over Avernus. Now Avernus offers you that jurisdiction itself. Win, and Greyhurst's "
                'people come home, and no lord of the First Layer will ever again sit safe behind the line.',
        tie="Your broken vow names Edrin Marlowe, the Greyhurst ferry-warden's son. You promised his mother you "
            "would bring him out. You did not. A devil in the Citadel's registry holds that vow, and it can still"
            ' be collected. Someone will offer to burn it, for a price. You are afraid of what you would pay.',
        knows="<strong>If you rule alone,</strong> you will set up a defender's regency, with the ruler on the "
              'walls and not in the palace. <strong>If the party shares the crown,</strong> you marshal its armies.'
              ' <strong>If you back someone else,</strong> you stand for the Greyhurst survivors and make sure the '
              'winner keeps faith with them.',
        others=[
            ('Ilyra Ashroot',
             'Six years at the wound together. You haul out the living and she keeps the names of the dead. You '
             'trust her above anyone alive.'),
            ('Dame Caldris Vowborne',
             'She commanded the relief column at the rift the night Greyhurst fell. You scouted for her. Her '
             'orders were to hold, and she held.'),
            ('Sister Nema Copperwrit',
             'Years ago you carried three of her novices out of a collapsing rift. A letter still comes from her '
             'every winter.'),
            ('Aurelia Quill',
             'A lawyer with a conscience, she claims. You are still deciding.'),
            ('Orren Fenwick',
             'He keeps apologising to you for things he has not yet explained.'),
        ],
        table='Declare a vow with a practical objective, Rage before committing to an enemy, and use Reckless '
              'Attack selectively. Collateral Guardian competes for the same reaction as opportunity attacks. Keep '
              'close to your named Witness during deadly fights.',
        goal='At 14 gain the retaliatory Price Comes Due. Keep improving Constitution, mobility and saves rather '
             'than only damage.',
    ),
    "ilyra": dict(
        role='<strong>The Keeper.</strong> You heal, shield and shape the ground of every battle. In the story you'
             ' remember the people everyone else has written off, and you hold the powerful to one law: every '
             'bargain must end.',
        backstory=[
            "Ilyra Ashroot's grove stands where the Feywild frays against a planar wound, and for two hundred "
            'years its ash has fallen like snow. Her order, the <strong>Circle of Ashen Covenants</strong>, keeps'
            ' what the Blood War devours: names cut into bark, voices sealed in seed-pods, a ledger of souls '
            'whose names were stolen. Its oldest teaching is simple. Every oath is a season, and every season '
            'must end.',
            'For six years she has stood beside Varka Blackseal. Varka drags the living from the rift, and Ilyra '
            'keeps the names of those who never come back. When Greyhurst fell, she planted black trees on the '
            "empty field, one for every name on Varka's list.",
            'She went with Varka to Waterdeep and watched the court turn them away. She came to Avernus with '
            'dried winter roses in her satchel, the bark-ledger of the lost on her back, and one memory that is '
            'not hers to keep.',
        ],
        tonight='You want one law carved above the throne of Avernus: every obligation ends. A soul-debt without a '
                'season of release is not a contract. It is a cage. Win, and the First Crown must answer to the '
                'living, and no debt in Hell will run forever.',
        tie='Among the memories your grove keeps is one torn from a Greyhurst mother on the night the village '
            'fell: a boy at a ferry rail, waving. You are almost certain it belongs to the family Varka failed. '
            "You have not told her. Misty's agents trade in stolen memories, and they may learn whose it is "
            'before you find the courage to speak.',
        knows='<strong>If you rule alone,</strong> you will found an Ash Covenant, a crown that must renew its '
              'consent with the governed every season. <strong>If the party shares the crown,</strong> you are its '
              'conscience and keep the succession records. <strong>If you back someone else,</strong> you sponsor a'
              " free civic council for Avernus's mortal survivors.",
        others=[
            ('Varka Blackseal',
             'Your partner at the wound and your dearest friend. You are keeping a secret from her, and it grows '
             'heavier with every mile.'),
            ('Sister Nema Copperwrit',
             'She knows a contract can be honest and still be cruel. You trust her judgment, but not yet her '
             'monastery.'),
            ('Dame Caldris Vowborne',
             'After Greyhurst she came to your grove and planted a tree with her own hands. She would not say for '
             'whom.'),
            ('Aurelia Quill',
             'She believes the written word is enough. You hope she learns otherwise before it costs her.'),
            ('Orren Fenwick',
             "He asked to copy your bark-ledger 'for indexing'. You refused."),
        ],
        table='Set the Ashen Accord before danger, use bonus-action spirit commands selectively against the value '
              'of <em>healing word</em>, protect allies with reactions, and control terrain with <em>spike '
              "growth</em> or <em>wall of stone</em>. Stay within 60 feet of the Accord's bearer when protection "
              'matters.',
        goal='At 14 gain Court of Returning Ash. Focus on 7th–9th-level renewal and planar defence rather than '
             'summoning many extra combatants.',
    ),
    "orren": dict(
        role="<strong>The Archivist.</strong> You know Hell's paperwork from the inside, because you designed much"
             ' of it. You find the forgery, break the ward, and end the battle with one decisive spell.',
        backstory=[
            'For twenty years Orren Fenwick served the <strong>Asmodeun Scriptorium</strong>, and he was the '
            "finest archivist it had. He built the index that let the Ninth Court's clerks find any soul-contract"
            ' by name, date or default in under a minute. He was proud of it. Order, he believed, was a kindness.',
            'Then someone used his registry to build the Red Clause. His categories, his cross-references and his'
            ' tidy blank fields became the machine that turned charity into harvest. During a Scriptorium audit '
            'he opened a Hearthlight form and found his own handwriting in the template.',
            'He defected the week the Brass Arbiter took the case. He testified, surrendered his notebooks and '
            'was placed on probation, bound to carry a small brass gavel he may never raise in anger. Every night'
            ' since, he has worked to unmake what he made.',
        ],
        tonight='You want false-title registration destroyed: the trick of claiming a soul by inventing a legal '
                'category for it. You built that tool. Only a ruler of Avernus can outlaw it, so you will see that '
                'the next ruler does.',
        tie='Your signature is on the first draft of the registry template, the one the Red Clause copied. No one'
            ' has found it yet. Confess in public and you lose your probation, perhaps your freedom, but you gain'
            ' a legitimacy no rival can buy. Let someone else find it first, and you lose both.',
        knows='<strong>If you rule alone,</strong> you will abolish false-title registration and open every '
              'registry in Avernus to inspection. <strong>If the party shares the crown,</strong> you are its '
              'public legal architect. <strong>If you back someone else,</strong> you present the case of the '
              'surviving Waterdeep debtors.',
        others=[
            ('Aurelia Quill',
             'She damned you in open court, and she was right. You want her forgiveness. You know she should not '
             'give it yet.'),
            ('Dame Caldris Vowborne',
             'She guarded you for nine days during the hearing. She never once asked why you defected.'),
            ('Sister Nema Copperwrit',
             "Her monastery's plague bargain sits in your registry: contract 41-B. It is lawful and valid, and it "
             'is paid by people who never signed. You have not told her you know.'),
            ('Varka Blackseal',
             "Greyhurst's names went into the machinery of Avernus. You suspect you know which index holds them."),
            ('Ilyra Ashroot',
             'Her bark-ledger is the only honest registry you have ever seen. She was right to refuse you.'),
        ],
        table='Use <em>wall of force</em> or <em>globe of invulnerability</em> to control a decisive battlefield, '
              'reserve a reaction for <em>counterspell</em>, and use real evidence during hearings. A ritual '
              "<em>identify</em> is not permission to learn an unknown soul's true name.",
        goal='Expand high-level preparation and choose one strategic project: public registries, anti-forgery '
             'wards or a court that can actually audit devils.',
    ),
    "caldris": dict(
        role='<strong>The Judge.</strong> You hold the line in battle and hold officials to the law. Your aura '
             'shields the party, your word carries weight before any tribunal, and no unlawful seizure happens in '
             'your sight.',
        backstory=[
            'Young and certain, Dame Caldris Vowborne swore the <strong>Oath of the Infernal Lord</strong>, '
            "Asmodeus's own code. She believed the hardest law in the multiverse would forge the truest servant "
            'of justice. Forty years on, she is as hard as that law. She is far less certain it is just.',
            'She has led relief columns along the burning edges of the Blood War. On the night Greyhurst fell she'
            ' stood at the planar wound with two hundred soldiers and orders to hold position. She held. '
            'Afterwards she laid down her command and swore herself to the Brass Arbiter as a bailiff. It was the'
            ' one court in the planes she had seen convict the powerful.',
            'Through the Red Clause hearing she kept the doors. She guarded the defector Orren Fenwick and '
            'shielded the disgraced Aurelia Quill from a mob. She also carries a sealed record of a promise made '
            'under duress, and she has never broken the seal.',
        ],
        tonight='You believe law chains Hell better than any blade, but only if the officials wear the chains too. '
                'For the first time, Asmodeus has bound his own succession to a public Charter. You will see it '
                'honoured to the letter, and then you will rule by it.',
        tie='The sealed record holds the promise you made the night Greyhurst fell. A devil quartermaster offered'
            ' your column safe passage out of the rift in exchange for your word. You gave it without reading the'
            ' terms. Two hundred soldiers walked out alive. You do not know what you agreed to, or whether it '
            'doomed the village. And your Oath may one day demand a loyalty to Asmodeus that no just ruler could '
            'give.',
        knows='<strong>If you rule alone,</strong> you will be a lawful and severe regent who holds every official,'
              ' yourself included, to the Charter. <strong>If the party shares the crown,</strong> you are its '
              'military judge and captain of the watch. <strong>If you back someone else,</strong> you openly '
              'represent Zariel, Bel or an independent order, and say so.',
        others=[
            ('Varka Blackseal',
             'She scouted for you the night Greyhurst fell. She knows nothing of your bargain, and you fear she '
             'would understand it too well.'),
            ('Ilyra Ashroot',
             'You planted a tree in her grove for a soldier who died holding your line. You have never told her '
             'his name.'),
            ('Orren Fenwick',
             'You guarded him for nine days. He talks in his sleep, and every word is an apology.'),
            ('Aurelia Quill',
             'You held a doorway for her once. She thanked you as if signing a receipt, and you liked her for it.'),
            ('Sister Nema Copperwrit',
             'The only other claimant sworn to an oath she cannot break. Her word is iron to you.'),
        ],
        table='Stand close enough for the aura to matter, maintain <em>bless</em> in uncertain encounters, reserve '
              'smites for confirmed priority hits, and use social authority to stop unlawful seizures before battle'
              ' begins.',
        goal='Higher-level auras and oath features can make Caldris a decisive defensive anchor, while forceful '
             'doctrine may become politically divisive.',
    ),
    "nema": dict(
        role='<strong>The Witness.</strong> You keep the party standing with healing and wards, and you are the '
             'one person every faction agrees is honest. When you certify a thing, Avernus believes it.',
        backstory=[
            'Sister Nema Copperwrit is a temple notary of the <strong>Contract Domain</strong>, sworn to the '
            'mountain monastery of Saint Ostra, whose vaults hold six hundred years of records. She can recite '
            'most of them from memory. She has witnessed thousands of marriages, apprenticeships, debts and '
            'deathbed wills, and never once set her seal to a lie. Every court in three kingdoms knows it.',
            'So the Brass Arbiter summoned her to Waterdeep. She took down every word of the Red Clause testimony'
            ' and pressed her seal into the final verdict. Precedent H-25 bears her name in its margin.',
            'She also carries a debt she never signed. Two generations ago, plague climbed the mountain to Saint '
            'Ostra, and the abbot struck an infernal bargain to save the novices. The bargain was honest, and the'
            " novices lived. Their children, and their children's children, still pay a tithe of years from their"
            ' lives every winter. None of them signed. All of them are bound.',
        ],
        tonight='You do not ask Hell to be good. You ask it to stop hiding cruelty behind lawful paper. The throne of'
                ' Avernus is an office, and for once its holder can be called to account. You intend to be in the '
                'room when that account is written.',
        tie="The monastery's bargain is valid. Precedent H-25 cannot void it, because the abbot truly consented. "
            'You seek a way to honour his choice while freeing the descendants who never made it. Such a ruling '
            'would set a precedent that Hell, and perhaps your own order, would find very dangerous.',
        knows='<strong>If you rule alone,</strong> you will proclaim a Charter of Protected Persons: no one bound '
              'by a contract they never signed. <strong>If the party shares the crown,</strong> you are its '
              'independent moral auditor. <strong>If you back someone else,</strong> you sponsor a pact-bound order'
              ' of guardians to watch over the new ruler.',
        others=[
            ('Aurelia Quill',
             'You recorded her confession. She was braver than she knows, and harsher on herself than any law '
             'requires.'),
            ('Varka Blackseal',
             'She carried three of your novices out of a collapsing rift. You owe her a debt you have chosen never'
             ' to settle, so that it always stands.'),
            ('Orren Fenwick',
             'He built a cage and now begs to break it. You will believe him when he confesses all of it.'),
            ('Dame Caldris Vowborne',
             'Her oath is to Asmodeus and yours is to the truth. They have never yet collided. You pray they never'
             ' will.'),
            ('Ilyra Ashroot',
             "She says every bargain must have a season of ending. Your monastery's has none. She may be the "
             'answer you have prayed for.'),
        ],
        table='Prioritise <em>spirit guardians</em> in close fights, <em>bless</em> when saving throws matter more '
              'than area damage, and <em>healing word</em> to rescue fallen allies. In hearings, <em>zone of '
              'truth</em> and authentic records complement direct testimony rather than replacing it.',
        goal="Cleric 17 gains 9th-level magic and the domain's highest feature; focus on lawful restitution and "
             'protection from coercive identity magic.',
    ),
}

CONNECTIONS = [
    ("Aurelia Quill", "Tobin Marsh's genuine soul bargain; her wish to be the final judge", "Act I registration; Act IV joint-slate fight", "Exhibit E (Chain of Title)"),
    ("Varka Blackseal", "Edrin Marlowe, the boy she failed; a devil holds the vow", "Act II Greyhurst; Act III Ash March", "Proof of Dominion"),
    ("Ilyra Ashroot", "Edrin's mother's stolen memory, kept from Varka", "Act II grove; Act V Custody of Memory", "Witness of Consent"),
    ("Orren Fenwick", "His signature on the first registry template; contract 41-B", "Act III Market of Names; Act IV the circular", "Exhibit C"),
    ("Dame Caldris Vowborne", "The unread promise she made the night Greyhurst fell", "Act III the Legal Duel; Act VI investiture", "Arbiter's order (Jurisdiction)"),
    ("Sister Nema Copperwrit", "Saint Ostra's honest plague bargain, paid by the unsigned", "Act II the spectral clerk; Act V the three witnesses", "Witness of Name"),
]


def bio_paragraphs(key):
    L = LORE[key]
    out = [L["role"]] + list(L["backstory"])
    out.append(f"<strong>Why You Entered.</strong> {L['tonight']}")
    out.append(f"<strong>Private Pressure.</strong> {L['tie']}")
    out.append(f"<strong>Your Claim.</strong> {L['knows']}")
    out.append("<strong>The Other Claimants.</strong> " + " ".join(f"<em>{n}:</em> {t}" for n, t in L["others"]))
    out.append(f"<strong>Tactics.</strong> {L['table']}")
    out.append(f"<strong>Toward Level 17.</strong> {L['goal']}")
    return out


SHEET = {
    "aurelia": dict(age="34", height="5'8\"", weight="140 lb.", eyes="Gold, slit-pupiled", hair="Black, long", skin="Ruby red",
        gender="Female", faith="The Ruby Court (a patron, not a god)",
        traits=["I keep a physical card for every Minor Term I offer, and I make the recipient initial it.",
                "I cannot hear the word 'standard' attached to a contract without asking which standard."],
        ideal="Truth. A government is only as honest as the records it certifies.",
        bond="I signed off on the Red Clause's forms. Every honest ruling I win pays a little of that back.",
        flaw="I want to be the final judge of what is true, and I do not trust anyone else with the job.",
        allies="The Brass Arbiter's clerks; former Hearthlight auditors; a former client whose soul is still owed.",
        appearance="A tiefling in a severe black coat with ruby lining and gold spectacles, a quill always behind one horn.",
        play=["You are the party's advocate: read every clause aloud and file the right objection.",
              "Three <em>eldritch blast</em> beams a turn, pushing with Repelling Blast. Hold one control spell per fight.",
              "Offer Minor Terms to willing allies as a bonus action; they get a d6 to add when it matters."]),
    "varka": dict(age="38", height="6'4\"", weight="260 lb.", eyes="Red-brown", hair="Black, shaved at the sides", skin="Grey-green, scarred",
        gender="Female", faith="Her own vows",
        traits=["I name what I will protect out loud before every fight.", "I eat standing up, in case someone needs carrying."],
        ideal="Protection. Power is only worth having if you stand in front of the people beneath it.",
        bond="The list of Greyhurst's missing is in my coat. I mean to cross every name off by finding them.",
        flaw="I failed one vow. I am afraid of what I will agree to pay to make up for it.",
        allies="Refugees and deserters she has carried out of the ash; the Greyhurst survivors.",
        appearance="A towering half-orc in scarred leathers and a crimson sash, a greataxe on her back and an iron rescue hook at her hip.",
        play=["Rage, then speak a Battle Vow: protect, hold, or engage. Keep it and your first hit each turn burns for +1d8.",
              "Collateral Guardian: soak a hit for an adjacent ally (your reaction, and you take half as psychic).",
              "Name a Witness at 10th level: they get advantage against fear and a once-per-rage boost against your foe."]),
    "ilyra": dict(age="212", height="5'6\"", weight="110 lb.", eyes="Green", hair="Ash-white", skin="Copper-brown",
        gender="Female", faith="The Ash Covenant (the turning of seasons)",
        traits=["I press a dried rose into the hand of anyone I comfort.", "I count the seasons of every promise I hear."],
        ideal="Renewal. Every obligation needs a season in which it ends.",
        bond="My ledger holds the names of people the war swallowed. I will not let anyone sell them.",
        flaw="I am keeping a memory that is not mine, and I tell myself it is for the owner's good.",
        allies="The Ashroot grove; Blood War refugees; any druid who keeps a record of the lost.",
        appearance="A wood elf in moss-green hide armour with a crown of dried winter roses and a moonstone sickle at her belt.",
        play=["Place the Ashen Accord on your frontliner before the fight (a 1-minute rite).",
              "Spend Wild Shape to manifest your Ash Warden Spirit; command it with a bonus action for 2d8 + 4 fire.",
              "Or Wild Shape into an Ashen fiend up to CR 4 (a Writ Hound or Barbed Toll-Warden), or spend both uses on a CR 5 Infernal Form.",
              "Use your reaction to shield the Accord's bearer, or to curse an attacker's next roll (Remedy of the Root)."]),
    "orren": dict(age="47", height="5'10\"", weight="150 lb.", eyes="Blue", hair="Brown, untidy, with a short beard", skin="Pale, ink-stained",
        gender="Male", faith="None he will admit to",
        traits=["I index everything, including my friends' grievances.", "I apologise to documents when I tear them."],
        ideal="Accountability. A system is only as good as the archivist willing to burn the bad parts.",
        bond="My registry made the Red Clause possible. I will see it unmade.",
        flaw="I would rather be right in private than useful in public.",
        allies="The Brass Arbiter (on probation); defectors from the Asmodeun Scriptorium; Waterdeep's surviving debtors.",
        appearance="A rumpled human wizard in a deep-blue archivist's coat, spectacles on a chain and a blackwood gavel at his belt.",
        play=["Control the field: <em>wall of force</em>, <em>globe of invulnerability</em>, <em>counterspell</em>.",
              "Place a Contract Sigil on an ally (bonus action) for a once-per-turn boost to damage or a save.",
              "Your Gavel of Appeal grants advantage in a hearing once per hearing."]),
    "caldris": dict(age="58", height="6'6\"", weight="300 lb.", eyes="Amber", hair="None (blue scales)", skin="Blue-grey scales",
        gender="Female", faith="The Oath of the Infernal Lord",
        traits=["I recite the clause I am enforcing before I draw my sword.", "I refuse any reward I did not earn under the rules."],
        ideal="Order. The strictest code is the only one that can bind the strong.",
        bond="A sealed promise I made under pressure. I have never opened it.",
        flaw="I may obey Asmodeus even when obedience and justice part ways.",
        allies="Old comrades of the Ninth Court's honour guard; any court that keeps its own rules.",
        appearance="A towering blue dragonborn in plate with a crimson tabard, a +1 longsword and a scorched oath-scroll on her shield.",
        play=["Your Aura of Protection adds +4 to everyone's saves within 10 feet. Stay close.",
              "Every hit adds 1d8 radiant; smite on confirmed priority hits.",
              "Channel Divinity: Fiendish Rebuke (reaction) or Fiendish Binding (restrain a foe)."]),
    "nema": dict(age="96", height="4'5\"", weight="160 lb.", eyes="Hazel", hair="Copper, braided into a bun, with a beard to match",
        skin="Ruddy", gender="Female", faith="The Contract Domain (the god of witnessed promises)",
        traits=["I can recite any contract I have witnessed.", "I stamp my seal on my own lunch."],
        ideal="Restitution. Honour the signer, free those who never consented.",
        bond="My monastery's bargain saved the novices and binds their children. I will settle it fairly.",
        flaw="I believe a properly witnessed document can fix anything, and it cannot.",
        allies="The Monastery of the Copper Seal; temple notaries across the realms.",
        appearance="A stout hill dwarf priest in scale mail with a notary's seal on a chain, a copper-red braid and beard.",
        play=["<em>Spirit guardians</em> in close fights; <em>healing word</em> to bring the fallen back up.",
              "Notary of the Nine: offer a Minor Term for temporary hit points (bonus action).",
              "Channel Divinity: Writ of Compulsion forbids one action; Infernal Audit declares a foe In Arrears."]),
}

TACTICS = {
    "varka": [("Every Turn", "Two greataxe attacks: +10 to hit, 1d12 + 6 slashing (+3 while raging). Brutal Critical adds one extra die on a crit."),
              ("Rage Covenant", "When you Rage, speak a Battle Vow. Keep it and the first creature you hit each turn takes +1d8 necrotic or fire."),
              ("Reckless Attack", "Advantage on your Strength attacks this turn; attacks against you have advantage until your next turn. Pick your moments."),
              ("Collateral Guardian", "Reaction: reduce damage to a willing adjacent ally by 1d10 + 7. You take half the prevented damage as psychic. 4/long rest."),
              ("Witness to the Oath", "Name a Witness when you Rage: advantage on saves against fear, and once per Rage they add +3 to a missed attack against your vow's foe."),
              ("Staying Up", "Relentless Rage and Relentless Endurance both keep you standing. Rage resistance to bludgeoning, piercing and slashing."),
              ("Crownmark Gauntlets", "Advantage to climb, grapple or hold an objective. Once per long rest, gain 15 temp HP when you drop a foe or hold a control point two rounds.")],
}
