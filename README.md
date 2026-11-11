# Interplanal Champions: The Throne of Avernus

*A campaign of infernal succession for D&D 5e · Avernus · Levels 12–17 · 18–24 sessions · A sequel to The Night of the Red Clause*

> In Hell, the strongest take the throne. The devious keep it. The wise read what they have signed.

Asmodeus has opened a new Rite of Succession for the First Layer of Hell, and challengers from across the planes are competing for the throne of Avernus. To win, a claimant has to prove Survival, Deviousness and Dominion, because in Hell every crown is a contract. Behind the pageantry, a deputy registrar is entering paper champions made from stolen names, a drowned town has been registered as "unclaimed", and Misty, Queen of Barbed Chains, wants one clause written into the winner's charter.

## Requirements
- Foundry VTT v13 or v14
- dnd5e system 5.0.0 or later (verified 5.3.3)

## Install
Paste this manifest URL into **Install Module**:
```
https://github.com/pacts-and-polyhedrals/interplanal-champions/releases/latest/download/module.json
```
Enable the module and reload as GM. You'll be asked once whether to set the campaign up. Choose **Set Up Everything**. You can also do it later from **Game Settings → Configure Settings → Interplanal Champions → Championship Manager**.

## What Set Up Everything does
1. Imports every actor, item, spell, subclass, journal, roll table and macro into labelled world folders.
2. Builds 22 vector battlemap scenes. Each has walls, doors, per-scene lighting, journal pins on every keyed location and the cast placed (ambushers and late arrivals hidden).
3. Creates a title landing scene and opens Book I.

Rebuilding a scene is safe: it replaces only what the module placed. **Update Content** refreshes world copies after a module update. It keeps IDs, so tokens and links still work.

## Contents
| | |
|---|---|
| **Book I (GM)** | A vector headpiece for every chapter. Running the Championship, the Succession Audit, six chapters (Dead Already, The Fallen, The War of Claims, Blood and Brass, The Hag Queen's Due, The Rite of the Nine), NPCs, the arena engine, open procedure, Charter reference, appendices |
| **Book II (Player's Guide)** | The Championship Charter, the four new subclasses, the 17 new spells, relics, contracts, claimants and player rules |
| **Handouts** | 21: the invitation, the Charter, the Nine Articles, eight contract forms, the challenge card, Circular No. 9-C, Petition M-9, Misty's writ of first refusal, Exhibits A–G… |
| **Interlude** | The Redline Run: a soul-fuelled vehicle chase on the scrolling Claw Rift, with the Souljack Yard (where the party gets its war machines and soul coins), the Soul Furnace Codex, four vehicle actors, a chase tracker and a soul-coin reader |
| **Scenes** | The six original great maps (Welcome to Hell, Unexpected Findings, Greyhurst, the Mansion's two floors, the Brass Arena), plus 17 locations within them (24 scenes, including the Redline Run staging of the Claw Rift). The Claw Rift tiles edge to edge for a scrolling chase |
| **Actors** | 45 creatures, NPCs and objects, 4 infernal war machines, with dnd5e 5.x activities, legendary, lair and mythic actions; Ashen Forms: 14 fiend Wild Shape actors (7 SRD fiends, 7 original fiends of Avernus); 6 level-12 pregenerated claimants with five-page sheets and connected backstories |
| **Items** | Relics of the Championship, Exhibits & Evidence, Proofs, Crown Marks & Tokens, and Asmodeun Scriptorium relics (38) |
| **Player Options** | *The Ruby Court* (warlock), *Path of the Blood-Price* (barbarian) *Circle of Ashen Covenants* (druid) and *The Soulforged* (artificer, with 12 Construct Imprints and 2 servitor actors); 17 new spells from cantrip to 8th; the Asmodeun Scriptorium's 26 contract spells and three subclasses |
| **Tools** | Championship Board (proofs, Crown Marks, War, Lien and Legitimacy clocks, seals), Arena Hazard, Convene a Hearing, Present an Exhibit, The Ash March (mass battle), Misty's mythic phase, Show Handout, Group Challenge, Request Group Save |
| **Roll Tables** | 19 tables, including soul Echoes, coin origins, furnace and vehicle mishaps, road hazards and the enemy-plan oracle; including arena environment and summons, travel, temptations, rewards, Mansion consequences, the Rival Oracle, and Wilds and Greyhurst encounters |

## Credits
*Interplanal Champions* began as *Interplanal Champion: Interest of Asmodeus*, first run in 2020. My thanks to everyone who played it on the **Blown Away** server. You were my first playtest group, it was the first D&D server I ran, and every claim, betrayal and ruling in this book is better because of you. Special thanks to the playtesters, **Tim, Alex, Heather and Kai**, and to the **Pacts & Polyhedrals**, **Blown Away** and **Imagi-Nations** Discord servers.

Written and designed by **Asmo**, Pacts & Polyhedrals (Ben Vale). The Asmodeun Scriptorium by Asmo.
[Patreon](https://www.patreon.com/pactsandpolyhedrals) · [StartPlaying](https://startplaying.games/gm/dmasmo)

*Not affiliated with Wizards of the Coast. Pregenerated claimants embed D&D 5e SRD 5.1 content (CC-BY-4.0) from the Foundry dnd5e system.*

## Building from source
```
npm install
python3 art/maps.py; python3 art/cast.py; python3 art/icons.py; python3 art/keyart.py
python3 tools/build.py; python3 tools/validate.py; node tools/smoke.mjs
python3 tools/pdfbook.py; python3 tools/render_pdf.py all; python3 tools/mappack.py
```
