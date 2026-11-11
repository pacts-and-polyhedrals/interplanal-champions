"""Script macros calling the module API."""
from lib5e import *

MACROS = []


def macro(key, name, call, img, folder):
    mid = fid("macro:" + key)
    cmd = (f'const api = game.modules.get("{MOD}")?.api;\n'
           f'if (!api) return ui.notifications.warn("Enable Interplanal Champions first.");\n'
           f'{call}')
    MACROS.append({"_id": mid, "name": name, "type": "script", "scope": "global", "img": icon(img), "command": cmd,
                   "folder": folder, "sort": len(MACROS) * 100, "ownership": {"default": 0},
                   "flags": {MOD: {"key": key}}, "_key": f"!macros!{mid}", "_stats": STATS})


GM = "GM Setup"
TB = "At the Table"
CT = "Courts & Arenas"
macro("setup", "Championship Manager", "api.openManager();", "ic-title", GM)
macro("board", "Championship Board (Proofs, Marks, Clocks, Seals)", "api.board.toggle();", "ic-tracker", TB)
macro("handout", "Show Handout", "api.showHandout();", "ic-exhibit", TB)
macro("challenge", "Group Challenge", "api.skillChallenge();", "ic-vow", TB)
macro("save", "Request Group Save", "api.requestSave();", "ic-reserved", TB)
macro("arena", "Arena Hazard (initiative count 20)", "api.arenaHazard();", "ic-arena", CT)
macro("tribunal", "Convene a Hearing", "api.tribunal();", "ic-tribunal", CT)
macro("exhibit", "Present an Exhibit", "api.presentExhibit();", "ic-stamp", CT)
macro("battle", "The Ash March (mass battle)", "api.massBattle();", "ic-battle", CT)
macro("mythic", "Hag Queen's Deception (Misty's mythic phase)", "api.mythicPhase();", "ic-heartstone", CT)

RR = "The Redline Run"
macro("redline", "Redline Run: Chase Tracker (Lead, Heat, Sparks)", "api.redline.toggle();", "ic-soul-coin", RR)
macro("redline-round", "Redline Run: Next Round (hazard + enemy plan)", "api.redline.nextRound();", "ic-arena", RR)
macro("soul-coin", "Read a Soul Coin (Echo, voice, claim, charges)", "api.readSoulCoin();", "ic-soul-coin", RR)
macro("generate-soul", "Soulforged: Generate a Soul (archetype, alignment, personality)", "api.generateSoul();", "ic-sf-imprint", RR)
