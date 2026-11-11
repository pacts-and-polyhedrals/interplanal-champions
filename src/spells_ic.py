"""The seventeen contractual spells of Interplanal Champions (Book II, Section 5)."""
from lib5e import *


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def D(value, units):
    return {"value": str(value) if value != "" else "", "units": units}


SELF = rng("", "self")
TOUCH = rng("", "touch")
SPELL_ACT = activation


def build(add):
    out = []
    A = out.append
    e_wm = effect("ic-witness-mark", "Witness Mark", icon("ic-sp-witness"), duration={"seconds": 3600},
                  description="<p>A faint sigil. Once, reveal it to gain advantage on a check to verify your own statement or "
                              "a signature you made.</p>")
    A(add("witness-mark", name="Witness Mark", img="ic-sp-witness", level=0, school="div",
          classes="Bard, Cleric, Druid, Warlock, Wizard", rng_=TOUCH, duration=D(1, "hour"), effects=[e_wm],
          desc=P("You mark a willing creature or a document with a faint sigil. While the mark lasts, you can recognise the "
                 "marked target if you see it within 60 feet, even if superficially disguised. The mark gives no truesight "
                 "and does not defeat invisibility.",
                 "Once before the spell ends, the bearer can choose to reveal the sigil to gain advantage on an ability check "
                 "to verify the authenticity of its own statement or a signature it personally made. The sigil then vanishes. "
                 "You can have only one Witness Mark active."),
          activities=[utility("witness-mark", 0, name="Mark", effects=[e_wm["_id"]], tgt=target(1, "willing"), rng_=TOUCH)]))
    A(add("ember-receipt", name="Ember Receipt", img="ic-sp-ember", level=0, school="evo",
          classes="Druid, Sorcerer, Warlock, Wizard", rng_=rng(60), duration=D("", "inst"),
          desc=P("Make a ranged spell attack against a creature. On a hit it takes [[/damage 1d8 type=fire]]; if it knowingly "
                 "broke a clearly stated promise to you during the previous round, it takes an additional "
                 "[[/damage 1d4 type=fire]] (no additional damage from merely signing a contract).",
                 "The base damage becomes 2d8 at character level 5, 3d8 at 11 and 4d8 at 17; the bonus stays 1d4."),
          activities=[attack("ember-receipt", 0, kind="ranged", classification="spell", range_=60, ability="",
                             parts=[dmg(1, 8, "", ["fire"], "whole", 1)], name="Ember Receipt"),
                      damage_act("ember-receipt-b", 1, name="Broken Promise (+1d4)", parts=[dmg(1, 4, "", ["fire"])],
                                 act=activation("special", None))]))
    for _a in out[-1]["system"]["activities"].values():
        if _a["type"] == "attack":
            _a["attack"]["ability"] = ""
            _a["damage"]["parts"][0]["scaling"] = {"mode": "", "number": None, "formula": ""}
    out[-1]["system"]["activities"][next(iter(out[-1]["system"]["activities"]))]["damage"]["parts"] = [
        dmg_formula("(1 + floor((@details.level + 1) / 6))d8", ["fire"])]
    A(add("formal-objection", name="Formal Objection", img="ic-sp-objection", level=1, school="abj",
          classes="Bard, Cleric, Paladin, Warlock, Wizard", comps=("vocal",), rng_=rng(60), duration=D("", "inst"),
          act=activation("reaction", 1, "when a creature within range makes a saving throw against being charmed or frightened"),
          desc=P("Before the DM announces the outcome of the save, add 1d4 to the roll. The spell cannot retroactively undo an "
                 "event.", "<strong>At Higher Levels.</strong> Add another 1d4 at slot levels 3, 5 and 7, to a maximum of 4d4."),
          activities=[utility("formal-objection", 0, name="Object", roll=("(1 + floor((@item.level - 1) / 2))d4", "Objection"),
                              act=activation("reaction", 1), tgt=target(1, "creature"))]))
    A(add("promissory-ward", name="Promissory Ward", img="ic-sp-promissory", level=1, school="abj",
          classes="Cleric, Druid, Paladin, Warlock", rng_=rng(30), duration=D("", "inst"),
          act=activation("reaction", 1, "when a willing creature within range is damaged by an attack"),
          desc=P("Reduce the triggering damage by 1d10 + your spellcasting ability modifier. The protected creature may "
                 "freely promise to aid you later, but this promise has no automatic magical penalty.",
                 "<strong>At Higher Levels.</strong> Add 1d10 reduction per slot level above 1st."),
          activities=[utility("promissory-ward", 0, name="Ward", roll=("(@item.level)d10 + @mod", "Damage reduced"),
                              act=activation("reaction", 1), tgt=target(1, "willing"))]))
    A(add("registry-of-names", name="Registry of Names", img="ic-sp-registry", level=2, school="div", ritual=True,
          classes="Bard, Cleric, Druid, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="a quill and indexed paper worth 10 gp, not consumed", act=activation("minute", 10), rng_=TOUCH,
          duration=D("", "inst"),
          desc=P("Touch a named document. Learn whether up to six listed signatures were made by the people they purport to "
                 "represent, whether the writing has been magically altered since signing, and whether any named signatory "
                 "appears twice under mutually incompatible identities.",
                 "You do not learn true names, a hidden signatory's location, or what a lawful contract means. The spell "
                 "examines the document, not every copy in the universe."),
          activities=[utility("registry-of-names", 0, name="Examine")]))
    e_ch = effect("ic-collateral", "Collateral Chains", icon("ic-sp-chains"), statuses=["restrained"], duration={"seconds": 60},
                  description="<p>Restrained by spectral brass chains. Repeat the Strength save at the end of each of your turns.</p>")
    A(add("collateral-chains", name="Collateral Chains", img="ic-sp-chains", level=2, school="con", concentration=True,
          classes="Sorcerer, Warlock, Wizard", rng_=rng(60), duration=D(1, "minute"), effects=[e_ch],
          desc=P("One creature you see must make a Strength saving throw. On a failure, spectral brass chains "
                 "&Reference[restrained]{restrain} it. It may repeat the save at the end of each of its turns, ending the spell "
                 "on a success. The chains end early if you lose concentration. A creature restrained by this spell is not "
                 "legally indebted to you."),
          activities=[save("collateral-chains", 0, ability="str", spell=True, on_save="none", tgt=target(1, "creature"),
                           rng_=rng(60), effects=[e_ch["_id"]])]))
    e_sp = effect("ic-safe-passage", "Writ of Safe Passage", icon("ic-sp-passage"), duration={"seconds": 3600},
                  description="<p>Advantage on your first saving throw against an environmental hazard caused by heat, extreme "
                              "cold, acidic rain or planar instability. You know the shortest nonmagical path back to the "
                              "casting location within 1 mile.</p>")
    A(add("writ-of-safe-passage", name="Writ of Safe Passage", img="ic-sp-passage", level=3, school="abj", ritual=True,
          classes="Cleric, Druid, Paladin, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="a brass token worth 25 gp, not consumed", act=activation("minute", 10), rng_=TOUCH, duration=D(1, "hour"),
          effects=[e_sp],
          desc=P("Up to six willing creatures who touch the token when you cast gain advantage on their first saving throw "
                 "each against an environmental hazard caused by heat, extreme cold, acidic rain or planar instability during "
                 "the duration. Each creature also knows the shortest nonmagical path back to the casting location while "
                 "within 1 mile.",
                 "The spell neither protects from weapon attacks nor compels a planar authority to grant entry."),
          activities=[utility("writ-of-safe-passage", 0, name="Issue the Writ", effects=[e_sp["_id"]], tgt=target(6, "willing"))]))
    e_du = effect("ic-duel", "Duel by Covenant", icon("ic-sp-duel"), duration={"seconds": 60},
                  changes=[("system.attributes.ac.bonus", 2, "+1")],
                  description="<p>+1 AC against attacks by creatures other than the other duellist. Once, use a reaction to "
                              "move 10 feet without provoking opportunity attacks from outsiders.</p>")
    A(add("duel-by-covenant", name="Duel by Covenant", img="ic-sp-duel", level=3, school="abj", concentration=True,
          classes="Bard, Cleric, Paladin, Warlock", rng_=rng(60), duration=D(1, "minute"), effects=[e_du],
          desc=P("Name two willing creatures within range (one may be you) who can communicate their agreement. For the "
                 "duration, each duellist gains +1 AC against attacks made by creatures other than the other duellist, and "
                 "each can once use a reaction to move 10 feet without provoking opportunity attacks from outsiders.",
                 "The spell ends for both if either duellist withdraws consent (no action), if they move more than 120 feet "
                 "apart, or if concentration ends. It does not force them to fight and does not cancel legal duels already "
                 "established."),
          activities=[utility("duel-by-covenant", 0, name="Witness the Duel", effects=[e_du["_id"]], tgt=target(2, "willing"))]))
    e_cm = effect("ic-custody", "Custody of Memory", icon("ic-sp-memory"), duration={"seconds": 3600},
                  description="<p>Advantage on Intelligence and Wisdom saves against effects that erase, modify or extract your "
                              "memories. Once, turn a failed save into a success (ends the spell).</p>")
    A(add("custody-of-memory", name="Custody of Memory", img="ic-sp-memory", level=4, school="abj", concentration=True,
          classes="Bard, Cleric, Druid, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="a clear glass bead worth 50 gp, not consumed", rng_=TOUCH, duration=D(1, "hour"), effects=[e_cm],
          desc=P("One willing creature gains advantage on Intelligence and Wisdom saving throws against spells and effects that "
                 "erase, modify or extract its memories. Once during the duration, when it would fail such a save, it may "
                 "choose to succeed instead; doing so ends the spell.",
                 "The spell has no effect on a memory already voluntarily transferred by a valid signed contract."),
          activities=[utility("custody-of-memory", 0, name="Take Custody", effects=[e_cm["_id"]], tgt=target(1, "willing"),
                              rng_=TOUCH)]))
    e_bd = effect("ic-breach", "Breach of Dominion", icon("ic-sp-breach"), duration={"rounds": 1},
                  description="<p>You can't take reactions until the end of your next turn.</p>")
    A(add("breach-of-dominion", name="Breach of Dominion", img="ic-sp-breach", level=4, school="trs",
          classes="Druid, Sorcerer, Warlock, Wizard", rng_=rng(90), duration=D("", "inst"), effects=[e_bd],
          desc=P("A construct or fiend within range makes a Constitution saving throw. On a failure, it takes "
                 "[[/damage 5d8 type=force]] and cannot take reactions until the end of its next turn; on a success, half "
                 "damage and no other effect.",
                 "A construct currently being compelled by a magical command can immediately make an additional saving throw "
                 "against that command if one was initially allowed.",
                 "<strong>At Higher Levels.</strong> +1d8 damage per slot level above 4th."),
          activities=[save("breach-of-dominion", 0, ability="con", spell=True, parts=[dmg(5, 8, "", ["force"], "whole", 1)],
                           tgt=target(1, "creature"), rng_=rng(90), effects=[e_bd["_id"]])]))
    e_ti = effect("ic-injunction", "Temporary Injunction", icon("ic-sp-injunction"), duration={"seconds": 60},
                  description="<p>While within 60 feet of the caster, you can't teleport or use a feature to summon another "
                              "creature. Repeat the Charisma save at the end of each turn.</p>")
    A(add("temporary-injunction", name="Temporary Injunction", img="ic-sp-injunction", level=5, school="abj",
          concentration=True, classes="Cleric, Paladin, Warlock, Wizard", rng_=rng(60), duration=D(1, "minute"), effects=[e_ti],
          desc=P("One creature you can see makes a Charisma saving throw. On a failure, while within 60 feet of you it cannot "
                 "teleport or use a feature to summon another creature. It repeats the save at the end of each turn, ending "
                 "the spell on a success. On an initial success, nothing happens.",
                 "This does not prohibit ordinary movement, existing companions or the creature leaving on foot. Teleportation "
                 "that is part of a mythic death-and-rebirth feature is suppressed only if the creature fails the save and "
                 "the feature does not explicitly override spells."),
          activities=[save("temporary-injunction", 0, ability="cha", spell=True, on_save="none", tgt=target(1, "creature"),
                           rng_=rng(60), effects=[e_ti["_id"]])]))
    A(add("audit-the-false", name="Audit the False", img="ic-sp-audit", level=5, school="div", ritual=True,
          classes="Bard, Cleric, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="ink dusted with platinum worth 100 gp, which the spell consumes", mat_cost=100, mat_consumed=True,
          act=activation("minute", 10), rng_=TOUCH, duration=D("", "inst"),
          desc=P("Touch one signed document or active magical record. You learn which of up to ten named signatures are forged "
                 "or produced under magical impersonation; the date and general kind of magical alteration; and whether any "
                 "cited authority belongs to the purported issuer.",
                 "You do not automatically learn the true perpetrator, and the spell cannot declare a genuinely voluntary but "
                 "harmful agreement invalid. A creature capable of concealing its identity from divination may oppose you with "
                 "a Charisma save against your spell save DC; on a success, the spell reveals that this entry is obscured, not "
                 "that it is authentic."),
          activities=[utility("audit-the-false", 0, name="Audit")]))
    A(add("sever-assigned-name", name="Sever Assigned Name", img="ic-sp-sever", level=6, school="abj",
          classes="Cleric, Druid, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="a seal of genuine testimony worth 250 gp, which the spell consumes", mat_cost=250, mat_consumed=True,
          rng_=rng(60), duration=D("", "inst"),
          desc=P("Choose a willing creature whose identity or name has been assigned to a magical claimant without their "
                 "permission. One spell or magical effect of 6th level or lower sustaining that false assignment ends. For a "
                 "higher-level effect, make a spellcasting ability check against DC 10 + the effect's level.",
                 "If a creature is actively sustaining the assignment, it may make a Charisma save; on a success, only the "
                 "assignment's control is suppressed until the end of your next turn. This does not erase a legitimate name, "
                 "make a true soul bargain disappear, or kill a person sustained by magic."),
          activities=[utility("sever-assigned-name", 0, name="Sever", roll=("1d20 + @mod", "Severing check"),
                              tgt=target(1, "willing"), rng_=rng(60))]))
    A(add("planar-reprieve", name="Planar Reprieve", img="ic-sp-reprieve", level=6, school="con",
          classes="Cleric, Druid, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="a consecrated home-key worth 500 gp, not consumed", act=activation("minute", 1), rng_=TOUCH,
          duration=D("", "inst"),
          desc=P("You and up to five willing creatures touching you teleport to a circle that you personally registered earlier "
                 "on the same plane and within 10 miles. You must have spent 1 hour preparing that circle.",
                 "This spell cannot escape a sealed plane and is blocked by effects that prevent teleportation. It is "
                 "deliberately slower and shorter-range than a universal emergency escape."),
          activities=[utility("planar-reprieve", 0, name="Return", tgt=target(5, "willing"))]))
    e_si = effect("ic-sovereign", "Sovereign Injunction", icon("ic-sp-sovereign"), duration={"seconds": 60},
                  description="<p>Enjoined: you can't make opportunity attacks, or can't use legendary actions, or can't teleport "
                              "(as chosen). Repeat the Charisma save at the end of each of your turns.</p>")
    A(add("sovereign-injunction", name="Sovereign Injunction", img="ic-sp-sovereign", level=7, school="enc",
          concentration=True, classes="Bard, Cleric, Warlock, Wizard", rng_=rng(60), duration=D(1, "minute"), effects=[e_si],
          desc=P("One creature that can understand any language you speak makes a Charisma saving throw. On a failure, choose "
                 "one: it cannot make opportunity attacks; it cannot use legendary actions; or it cannot teleport. At the end "
                 "of each of its turns it may repeat the save, ending the injunction on a success.",
                 "A target with Legendary Resistance may use it normally. The spell does not prevent ordinary actions, remove "
                 "legendary resistances or compel a contract. It may fail against an especially potent sovereign creature even "
                 "when a weaker foe would be bound."),
          activities=[save("sovereign-injunction", 0, ability="cha", spell=True, on_save="none", tgt=target(1, "creature"),
                           rng_=rng(60), effects=[e_si["_id"]])]))
    A(add("writ-of-provisional-dawn", name="Writ of Provisional Dawn", img="ic-sp-dawn", level=7, school="trs",
          concentration=True, classes="Cleric, Druid, Warlock, Wizard", comps=("vocal", "somatic", "material"),
          materials="a sun-marked hourglass worth 500 gp, not consumed", rng_=rng(120), duration=D(10, "minute"),
          tgt=target("", "space", "sphere", 60),
          desc=P("Within a 60-foot-radius sphere, magical effects that rely on a false or frozen local time instead use the "
                 "actual passing time at the effect's original place of jurisdiction, if that place is known to you.",
                 "This cannot accelerate time, force true sunlight, end a legitimate contract before its term, or negate the "
                 "passage of a real night. Any creature sustaining a false-time effect may make a Charisma save; on a success, "
                 "its effect is unaffected until the start of your next turn, at which point the sphere attempts again."),
          activities=[utility("writ-of-provisional-dawn", 0, name="Restore True Time")]))
    A(add("statute-of-the-first-crown", name="Statute of the First Crown", img="ic-sp-statute", level=8, school="abj",
          concentration=True, classes="Cleric, Warlock (8th-level Mystic Arcanum), Wizard",
          comps=("vocal", "somatic", "material"), materials="a bronze crown replica worth 1,000 gp, not consumed",
          act=activation("minute", 1), rng_=rng("", "self", "100-foot-radius sphere"), duration=D(1, "hour"),
          tgt=target("", "", "sphere", 100),
          desc=P("Declare a single procedural protection that applies equally to all creatures within the sphere: (a) no "
                 "magical effect may use a forged signature as a source of authority; (b) no unwilling creature can be "
                 "compelled to testify by magical effects of 5th level or lower; or (c) contracts of 5th level or lower cannot "
                 "be magically altered while within the sphere.",
                 "A hostile magical creature whose effect would be stopped may make a Charisma save against your spell save "
                 "DC when first affected, allowing its effect to continue for one round on a success. The protection does not "
                 "invalidate truthful testimony, a genuine signed contract, or a superior divine law. The sphere is "
                 "stationary. Casting this spell does not itself make you ruler of Avernus."),
          activities=[utility("statute-of-the-first-crown", 0, name="Declare the Statute")]))
    for sp in out:
        sp["flags"][MOD] = {"group": "Interplanal Champions"}
    return out
