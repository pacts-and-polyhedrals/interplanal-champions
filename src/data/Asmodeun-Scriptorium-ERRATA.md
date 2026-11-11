# The Asmodeun Scriptorium — Audit & Changelog

Everything found in the draft, and what was done about it in the expanded manuscript.

---

## 1. Rules errors (things that don't work as written)

| # | Issue | Fix |
|---|---|---|
| 1.1 | **Paladin oath spells at illegal levels.** *Fire shield* (4th) listed at paladin 9th, when paladins have only 3rd-level slots. *Dominate person* (5th) listed at 13th, when paladins have only 4th-level slots. | Rebuilt the whole table with level-legal picks that also seed your own spells: 3rd *hellish rebuke* / *seal of the first pact*; 5th *zone of truth* / *quill of binding*; 9th *magic circle* / *devil's due*; 13th *banishment* / *binding clause*; 17th *flame strike* / *soul covenant*. |
| 1.2 | **Infernal Summoning cites a save that doesn't exist.** *Summon Lesser Demons* has no Wisdom save to bypass — you were thinking of *Summon Greater Demon*. It also summons **demons**, which is thematically backwards for a lawful-devil subclass. | Replaced entirely with **Devil's Retainer** (bound imp clerk with an Object reaction) plus **Binding Authority** (fiends you summon obey without a check, and are freed and hostile if you break a term). |
| 1.3 | **Quill of Binding's duration contradicts its own effects.** Duration is 1 hour concentration, but one clause lasts 7 days and another lasts "until the contract is fulfilled." | Duration stays 1 hour concentration for the *writing*; added an explicit line that clauses endure past the spell. |
| 1.4 | **Contract of the Seer's Vigil** — school typo ("Divinbat"), stat block copy-pasted from Infernal Fury (same components, same "Range: Self (summons a tool)" which makes no sense for a telepathic link), and duration says 1 hour concentration while the terms table says 24 hours. | Fully rewritten as a proper 3rd-level divination with its own components, range, and duration. Also reconciled with Contract Template 3, which invokes it as a truth-guarantor — the rewrite now actually does that. |
| 1.5 | **Contract of the Infernal Fury** — labelled Divination, does fire damage. Range "Self (summons a tool)." Duration 1 hour concentration vs. terms saying 1 minute. | Recast as a 2nd-level **evocation**, bonus action, touch, 1 minute concentration, with the Forbidden Term preserved as a real mechanical clause. |
| 1.6 | **True Name Revelation** lists a 1-hour duration but the text references losing concentration. | Now explicitly Concentration, up to 1 hour, with a clause that you keep the *knowledge* after it ends. Added a Charisma save so it isn't a no-save read on any creature in sight. |
| 1.7 | **Contract of the Soulforged Blade** lets souls substitute for spell slots with no ceiling — a level-7 character can potentially fuel their highest-level slots off mooks, and nothing stops recasting the spell with its own souls. | Capped: souls fuel spells of 3rd level or lower from this book's list only, can't fuel the spell itself, capacity = proficiency bonus, souls released on expiry. Higher-level slots raise the ceiling to 5th max. |
| 1.8 | **Grand Infernal Binding** binds "celestials" (plural typo) and has no interaction with true names despite the subclass being about names. | Cleaned up and rebuilt around *contract of infernal servitude* (new 6th-level spell), CR 8, plus a true-name disadvantage rider. |

## 2. Balance problems

| # | Issue | Fix |
|---|---|---|
| 2.1 | **Aura of Contract grants fire immunity to the whole party at 7th level.** Immunity is a capstone-tier effect; this trivialises a third of the fiend bestiary and most of Avernus. | Resistance, not immunity. Range grows to 30 ft at 18th like every other paladin aura. |
| 2.2 | **Contract Sigil: flat d4 to *all* damage rolls for an hour at wizard 2**, with only a 10 gp cost and no use limit. That's better than *bless*, on one target, all day. | Once per turn, on one roll of the bearer's choice, 1 hour, uses = Int mod per long rest. Added a **Term** clause with 2d4 psychic backlash — flavour with teeth. d6 and two sigils at 10th. |
| 2.3 | **Minor Runes gave a permanent free +1 to spell attack rolls or save DCs** on every cantrip, with no cost. A flat DC bump is one of the strongest things you can hand a caster. | Cut. Replaced with the *fine print* cantrip and a spellbook-economy perk. The +1 fire damage flavour survives as the cantrip's cosmetic. |
| 2.4 | **Devil's Due** maximised 36 damage at 3rd level that explicitly ignores resistance. Ignoring resistance is a rare, high-cost design lever. | Kept the 6d6/maximised structure but removed the resistance-piercing clause, added disadvantage on the save for creatures in breach, and gated the soul-claim to contracts that actually pledged a soul. |
| 2.5 | **Binding Clause's geas can't be removed by *remove curse* or anything else.** Unremovable effects at 4th level are a problem in both directions. | Now ends on *dispel magic* at 5th+, *greater restoration*, or fulfilment. Daily damage trimmed 5d10 → 4d10 (it's a 4th-level spell doing a 5th-level spell's job). |
| 2.6 | **Soul Covenant** grants a flat **+5** to Persuasion. 5e doesn't use flat +5s. | Advantage on Charisma checks vs. lawful evil fiends. Also added an explicit "talk to your GM before signing" line, since the breach clause effectively retires a PC. |
| 2.7 | **Avatar of the Infernal Lord lasts 1 hour** and restrains with **no repeated saving throw**. Paladin capstones run 1 minute; permanent-until-aura-ends restraint with no save is harsher than most 9th-level spells. | 1 minute. Restraint lasts until the start of the creature's next turn, re-saving each round. Added Sovereign Authority so it still feels like a capstone. |
| 2.8 | **Fiendish Rebuke: 2d10 no-save reaction damage** and its scaling was pinned to 18th level, which no other paladin feature uses. | Dexterity save for half; scales at 9th and 15th. |

## 3. Structure and consistency

- **Part numbering was broken.** Three separate parts were all labelled "PART X," and the inline headings (II, III, IV, V) didn't match the part covers. Renumbered I–VI end to end.
- **The cleric subclass didn't exist.** The book referenced the "Infernal (Contract) Domain" four separate times — in the spells intro, in *True Name Revelation*'s class line, and in the spell descriptions — but never wrote it. Now written in full (1st/2nd/6th/8th/17th).
- **Spells were listed as "Levels 1–5"** but the section header promised the full range; three spells also lacked *At Higher Levels* entries. All 26 spells now carry upcasting where appropriate.
- **Contract templates cited spells by name and level inconsistently** (e.g. "Sanctified Escort Sign, 2nd-level enchantment" appears nowhere else in the book). Templates now cite only spells that exist in Part VI.
- **The bestiary and the hierarchy section listed different devils.** Merged: the bestiary table now covers all ten, including the contract devil (Phistophilus), which the summoning section referenced but never described.

## 4. Typos and text errors

- `https://imgur.com/Lcqq9aP,png` — **comma instead of a period**, so that image was silently failing to load on the theology page. Fixed.
- "Patrón" (Spanish accent) throughout Template 1 → "Patron."
- "Divinbat" → "divination." "Alkirat doctrine" — appears to be a leftover from another project; cut.
- "an infernal contract **gain** legitimacy" → gains. "**a** almost sacramental act" → an. "**streaming** cauldron of brimstone" → steaming.
- **Emergency Invocation Clause was ungrammatical** — "...the when the standard soul-tithe rate of three percent (3%) was not enacted before the journey shall, for that journey alone, escalate..." has no subject. Rewritten so it parses (and so a player can actually read it aloud at the table).
- Title mismatch: front cover says *Infernal Codex of Contractual Magic*, intro said *The codex of Contractual Magics*. Unified.
- Cross-reference to "Article IV, Subsection 4.2" in Template 7 — there is no subsection 4.2. Simplified to "per Article IV."
- Every image alt text was `![cat warrior]`, including on devils and contracts. Retitled descriptively (harmless in output, but it makes the source searchable).

## 5. What was added

- **Part III: The Ledger** — the contract subsystem. Draft DCs, Loophole Ratings, a Scrutiny/argument procedure for escaping contracts, and a 0–100% soul-tithe track with mechanical consequences at each band. This is what turns "the GM decides what the devil does" into a game.
- **Contract Domain (cleric)**, complete.
- **Rebuilt wizard and paladin subclasses**, complete.
- **26 spells, cantrip through 9th**, up from 8. Four cantrips, three each at 1st–4th, two each at 5th–9th.
- **Class spell lists** (Appendix A) including bard and warlock access.
- **Six adventure seeds** built on the templates and the Ledger (Appendix B).
- **2024-rules conversion sidebar** at the head of Part V.
- Loophole Ratings and Draft DCs added to all seven contract templates.

## 6. Open questions for you

1. **Edition.** Written at 2014 levels since that's what the draft used, with a conversion sidebar. Your *Delinquency & Debauchery* was SRD 5.2.1 — say the word and I'll flip the whole thing to 2024 native.
2. **Warlock subclass.** The draft mentions warlocks on the back cover and lists Warlock (The Fiend) in a spell's class line, but there's no patron subclass. An "Advocate" patron would slot in naturally, and it's arguably the most obvious class for this book.
3. **Stat blocks.** Contract devil, infernal auditor, and a Chartered Protector NPC would round out Part III. Not written yet.
4. **Magic items.** *Golgorath's Quill* is referenced twice as an artifact but never statted.
5. **Foundry packaging.** Same treatment as D&D — compendiums with folders for the three subclasses, 26 spells, and the seven contracts as journal entries.
