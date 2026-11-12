// Headless smoke test: stub just enough Foundry to run setupAll, stageScene, docket and writs.
import fs from "fs";
const MOD = "interplanal-champions";
const log = []; let idc = 0;
const mkColl = (name) => { const m = new Map(); const c = {
  get: id => m.get(id), find: f => [...m.values()].find(f), filter: f => [...m.values()].filter(f), map: f => [...m.values()].map(f),
  get contents() { return [...m.values()]; }, [Symbol.iterator]: () => m.values(), _m: m, documentName: name,
  fromCompendium: (d, o) => JSON.parse(JSON.stringify({ ...d._data, _id: o.keepId ? d.id : undefined })),
  documentClass: { deleteDocuments: async ids => ids.forEach(i => m.delete(i)) } }; return c; };
const doc = (data, coll) => { const d = { ...data, id: data._id ?? `gen${idc++}`, flags: data.flags ?? {},
  getFlag(s, k) { return this.flags?.[s]?.[k]; }, async update(u) { for (const [k, v] of Object.entries(u)) setP(this, k, v); return this; },
  async delete() { coll?._m.delete(this.id); }, toObject() { return JSON.parse(JSON.stringify(this)); } }; return d; };
const setP = (o, path, v) => { const ps = path.split("."); let c = o; for (const p of ps.slice(0, -1)) c = c[p] ??= {}; c[ps.at(-1)] = v; };
const colls = { Actor: mkColl("Actor"), Item: mkColl("Item"), JournalEntry: mkColl("JournalEntry"), RollTable: mkColl("RollTable"), Macro: mkColl("Macro"), Scene: mkColl("Scene"), Folder: mkColl("Folder") };
const createIn = (type) => async (arr) => arr.map(a => { const d = doc(a, colls[type]); if (type === "Actor") { d.prototypeToken = a.prototypeToken ?? { width: 1 }; d.getTokenDocument = async (o) => ({ toObject: () => ({ actorId: d.id, name: d.name, ...o }) }); d.toggleStatusEffect = async () => log.push("status"); } colls[type]._m.set(d.id, d); return d; });
const embedded = () => { const m = new Map(); return { _m: m, filter: f => [...m.values()].filter(f), find: f => [...m.values()].find(f), [Symbol.iterator]: () => m.values() }; };
globalThis.Hooks = { _h: {}, once(n, f) { this._h[n] = f; }, on() {} };
globalThis.CONST = { WALL_SENSE_TYPES: { NONE: 0, LIMITED: 10, NORMAL: 20, PROXIMITY: 30 }, WALL_MOVEMENT_TYPES: { NONE: 0, NORMAL: 20 }, DOCUMENT_OWNERSHIP_LEVELS: { OBSERVER: 2 } };
const settings = {};
const packs = new Map();
for (const p of JSON.parse(fs.readFileSync("module/module.json")).packs) {
  const dir = `build/extract/${p.name}`; const files = fs.readdirSync(dir, { recursive: true }).filter(f => f.endsWith(".json"));
  const all = files.map(f => JSON.parse(fs.readFileSync(`${dir}/${f}`)));
  const folders = all.filter(d => d._key.startsWith("!folders")).map(f => ({ ...f, id: f._id, folder: null, _parent: f.folder }));
  folders.forEach(f => f.folder = folders.find(x => x.id === f._parent) ?? null);
  const docs = all.filter(d => !d._key.startsWith("!folders")).map(d => ({ id: d._id, name: d.name, folder: folders.find(f => f.id === d.folder) ?? null, _data: d, getFlag: (s, k) => d.flags?.[s]?.[k] }));
  packs.set(`${MOD}.${p.name}`, { getDocuments: async () => docs, folders, getIndex: async () => docs.map(d => ({ _id: d.id, name: d.name, flags: d._data.flags })), getDocument: async id => docs.find(d => d.id === id) });
}
globalThis.game = { release: { generation: Number(process.argv[2] ?? 13) }, user: { isGM: true }, ready: true,
  modules: new Map([[MOD, { version: "1.0.0" }]]),
  settings: { register: (m, k, o) => settings[k] = o.default, registerMenu() {}, get: (m, k) => settings[k], set: async (m, k, v) => { settings[k] = v; } },
  packs, collections: new Map(Object.entries(colls)), folders: colls.Folder, actors: colls.Actor, items: colls.Item, journal: colls.JournalEntry, tables: colls.RollTable, macros: colls.Macro, scenes: colls.Scene };
game.journal.get = id => colls.JournalEntry._m.get(id);
globalThis.getDocumentClass = t => ({ createDocuments: createIn(t) });
globalThis.Folder = { create: async d => (await createIn("Folder")([d]))[0], deleteDocuments: async ids => ids.forEach(i => colls.Folder._m.delete(i)) };
globalThis.Scene = { createDocuments: async (arr) => (await createIn("Scene")(arr)).map(s => {
  for (const k of ["walls", "lights", "notes", "tokens"]) s[k] = embedded();
  s.levels = { contents: [] };
  s.createEmbeddedDocuments = async (type, arr) => { const key = { Wall: "walls", AmbientLight: "lights", Note: "notes", Token: "tokens", Level: "levels" }[type];
    if (type === "Level") { const l = doc(arr[0]); l.update = async u => { setP(l, Object.keys(u)[0], Object.values(u)[0]); }; s.levels.contents.push(l); return [l]; }
    return arr.map(a => { const d = doc(a); s[key]._m.set(d.id, d); return d; }); };
  s.deleteEmbeddedDocuments = async (type, ids) => { const key = { Wall: "walls", AmbientLight: "lights", Note: "notes", Token: "tokens" }[type]; ids.forEach(i => s[key]._m.delete(i)); };
  s.updateEmbeddedDocuments = async () => {}; s.createThumbnail = async () => ({ thumb: "x" }); return s; }) };
globalThis.ui = { notifications: { info: m => (log.push(m), { remove() {} }), warn: m => log.push("WARN " + m) } };
globalThis.foundry = { utils: { deepClone: o => JSON.parse(JSON.stringify(o)), setProperty: setP, escapeHTML: s => s },
  applications: { api: { ApplicationV2: class {}, DialogV2: { confirm: async () => true, prompt: async () => null, wait: async () => null } } } };
globalThis.fetch = async (p) => ({ json: async () => JSON.parse(fs.readFileSync(p.replace(`modules/${MOD}/`, "module/"))) });
globalThis.ChatMessage = { create: async m => log.push("CHAT " + m.content.replace(/<[^>]+>/g, " ").slice(0, 90)) };
globalThis.canvas = { scene: null };
globalThis.document = { createElement: () => ({ addEventListener() {}, remove() {} }), body: { appendChild() {} } };
await import("../module/scripts/main.mjs");
Hooks._h.init(); await Hooks._h.ready(); await new Promise(r => setTimeout(r, 100)); await game.modules.get(MOD).api.setupAll?.() ?? null;
const api = game.modules.get(MOD).api;
const scenes = colls.Scene.contents;
console.log("gen", game.release.generation, "| scenes", scenes.length, "| actors", colls.Actor.contents.length, "| items", colls.Item.contents.length,
  "| journals", colls.JournalEntry.contents.length, "| tables", colls.RollTable.contents.length, "| macros", colls.Macro.contents.length, "| folders", colls.Folder.contents.length);
const rel = scenes.find(s => s.getFlag(MOD, "key") === "reliquary");
console.log("reliquary walls", rel.walls._m.size, "lights", rel.lights._m.size, "notes", rel.notes._m.size, "tokens", rel.tokens._m.size, "| bg", rel.background?.src ?? rel.levels?.contents?.[0]?.background?.src);
let tot = 0; for (const s of scenes) tot += s.tokens?._m?.size ?? 0; console.log("tokens placed across scenes", tot);
await api.stageScene("greenbottle"); const gb = scenes.find(s => s.getFlag(MOD, "key") === "greenbottle");
console.log("greenbottle restaged tokens", gb.tokens._m.size, "hidden", [...gb.tokens._m.values()].filter(t => t.hidden).length);
await api.board.toggle(true); await api.board.act("survival", 0); await api.board.act("mark+", 0); await api.board.act("clock:lien:1");
await api.board.act("seal:name"); await api.board.act("seal:consent");
console.log("board", JSON.stringify(settings.board));
// Redline Run tracker and soul coins
for (const t of colls.RollTable.contents) {
  t.draw = async () => { const rs = [...(t.results?.contents ?? t.results ?? t._source?.results ?? [])]; const r = rs[Math.floor(Math.random() * rs.length)];
    return { roll: { total: 1 + Math.floor(Math.random() * 6) }, results: [r] }; };
}
globalThis.Roll ??= class { constructor(f) { this.f = f; } async evaluate() { this.total = 1 + Math.floor(Math.random() * 6); return this; } };
await api.redline.toggle(true); await api.redline.reset(); await api.redline.act("lead+"); await api.redline.act("spark+", 0);
await api.redline.act("spark-", 0); for (let i = 0; i < 6; i++) await api.redline.act("heat+", 0);
await api.redline.nextRound(); await api.readSoulCoin(); await api.generateSoul();
console.log("redline", JSON.stringify(settings.redline));
console.log(log.filter(l => l.includes("REDLINE") || l.includes("SOUL COIN") || l.includes("RUPTURE")).join("\n"));
const hand = colls.JournalEntry.find(j => j.getFlag(MOD, "key") === "handouts"); console.log("handouts ownership", JSON.stringify(hand.ownership));
const b2 = colls.JournalEntry.find(j => j.getFlag(MOD, "key") === "book2"); console.log("book2 ownership", JSON.stringify(b2.ownership));
console.log(log.filter(l => l.startsWith("WARN") || l.startsWith("CHAT")).slice(-6).join("\n"));
