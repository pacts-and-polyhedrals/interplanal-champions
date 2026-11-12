/**
 * Interplanal Champions: The Throne of Avernus — runtime.
 * Asmo, Pacts & Polyhedrals (Ben Vale).
 *
 * Installs compendium content into labelled world folders, stages every scene (map, walls, doors, lights, journal pins,
 * tokens), and provides the GM tools used at the table: the Championship Board (Proofs, Crown Marks and the three clocks),
 * the arena hazard roller, the tribunal and mass-battle trackers, handouts and more.
 */
const MOD = "interplanal-champions";
const ROOT = "Interplanal Champions";
const PACKS = [
  ["actors", "Actor", `${ROOT} — Actors`],
  ["pregens", "Actor", `${ROOT} — Pregenerated Claimants`],
  ["items", "Item", `${ROOT} — Items`],
  ["spells", "Item", `${ROOT} — Spells`],
  ["options", "Item", `${ROOT} — Player Options`],
  ["journals", "JournalEntry", ROOT],
  ["tables", "RollTable", ROOT],
  ["macros", "Macro", ROOT]
];
const PLAYER_JOURNALS = ["handouts", "book2", "scriptorium"];
const CLOCKS = { war: "Blood War Pressure", lien: "Hag Lien", legit: "Public Legitimacy" };
const SEALS = { name: "Seal of Name", consent: "Seal of Consent", jurisdiction: "Seal of Jurisdiction" };
const SEAL_FX = {
  name: "Misty loses Magic Resistance for 2 full rounds.",
  consent: "Misty's save DC becomes 22 for the rest of this encounter. Nightmare Rebuke is unavailable.",
  jurisdiction: "Misty loses one unspent Legendary Resistance and can't use Counterclaim for 2 rounds."
};

const gen = () => game.release?.generation ?? 13;
const esc = s => foundry.utils.escapeHTML ? foundry.utils.escapeHTML(String(s)) : String(s);
const DialogV2 = () => foundry.applications.api.DialogV2;

/* ------------------------------------------------------------------------ */
/*  Settings                                                                */
/* ------------------------------------------------------------------------ */
Hooks.once("init", () => {
  game.settings.register(MOD, "installedVersion", { scope: "world", config: false, type: String, default: "" });
  game.settings.register(MOD, "promptDismissed", { scope: "world", config: false, type: Boolean, default: false });
  game.settings.register(MOD, "board", {
    scope: "world", config: false, type: Object,
    default: { visible: false, slates: [{ name: "The Party", survival: false, deviousness: false, dominion: false, marks: 0 }],
               clocks: { war: 0, lien: 0, legit: 2 }, seals: { name: false, consent: false, jurisdiction: false } },
    onChange: () => Board.refresh()
  });
  game.settings.register(MOD, "redline", {
    scope: "world", config: false, type: Object,
    default: { visible: false, round: 1, lead: 2, vehicles: [
      { name: "Souljack Hauler", heat: 0, sparks: 0, fuel: 6, echo: "" },
      { name: "Iron Reclaimer (pursuer)", heat: 0, sparks: 0, fuel: 24, echo: "" }] },
    onChange: () => Redline.refresh()
  });
  game.settings.registerMenu(MOD, "manager", {
    name: "Championship Manager", label: "Open Manager", hint: "Set up, update, rebuild scenes, or remove the campaign.",
    icon: "fa-solid fa-crown", type: Manager, restricted: true
  });
  game.modules.get(MOD).api = API;
});

Hooks.once("ready", () => {
  // Never hold up the world: the board, tracker and setup prompt start after the world has finished loading.
  try { Board.refresh(); Redline.refresh(); } catch (e) { console.error(`${MOD} | overlay failed`, e); }
  if (game.user.isGM) setTimeout(() => onReady().catch(e => console.error(`${MOD} | ready failed`, e)), 1500);
});

async function onReady() {
  const ver = game.modules.get(MOD).version, inst = game.settings.get(MOD, "installedVersion");
  if (!inst && !game.settings.get(MOD, "promptDismissed")) {
    const go = await DialogV2().confirm({
      window: { title: ROOT },
      content: `<p>Set up <strong>${ROOT}</strong> now?</p><p>This installs the actors, items, spells, subclasses, journals, roll tables and macros into labelled folders and builds the scenes with walls, lighting, pins and tokens. It takes a few minutes; keep this tab open until it says it's ready. You can do it later from <em>Game Settings → Configure Settings → Championship Manager</em>.</p>`
    });
    // Ask only once: a reload during setup never restarts it automatically.
    await game.settings.set(MOD, "promptDismissed", true);
    if (go) await setupAll();
  } else if (inst && inst !== ver) {
    ui.notifications.info(`${ROOT} updated to ${ver}. Open the Championship Manager and choose "Update Content" to refresh your world copies.`, { permanent: true });
  }
}

async function ensureFolder(name, type, parent = null, color = "#5e0b18") {
  const pid = parent?.id ?? null;
  let f = game.folders.find(x => x.type === type && x.name === name && (x.folder?.id ?? null) === pid);
  if (!f) f = await Folder.create({ name, type, folder: pid, color, sorting: "a", flags: { [MOD]: { managed: true } } });
  return f;
}

function folderDepth(f) { let d = 0; let p = f.folder; while (p) { d++; p = p.folder; } return d; }

async function importPack(packName, type, rootName, { update = false } = {}) {
  const pack = game.packs.get(`${MOD}.${packName}`);
  if (!pack) { console.warn(`${MOD} | missing pack ${packName}`); return 0; }
  const docs = await pack.getDocuments();
  const root = await ensureFolder(rootName, type);
  const fmap = new Map();
  const pfolders = [...(pack.folders ?? [])].sort((a, b) => folderDepth(a) - folderDepth(b));
  for (const f of pfolders) {
    const parent = f.folder ? fmap.get(f.folder.id) : root;
    fmap.set(f.id, await ensureFolder(f.name, type, parent, f.color ?? "#5e0b18"));
  }
  const coll = game.collections.get(type);
  const cls = getDocumentClass(type);
  const create = [];
  for (const d of docs) {
    const data = coll.fromCompendium(d, { keepId: true, clearFolder: true, clearOwnership: false });
    data.folder = fmap.get(d.folder?.id ?? d.folder)?.id ?? root.id;
    foundry.utils.setProperty(data, `flags.${MOD}.managed`, true);
    if (type === "JournalEntry" && PLAYER_JOURNALS.includes(d.getFlag(MOD, "key"))) {
      data.ownership = { default: CONST.DOCUMENT_OWNERSHIP_LEVELS.OBSERVER };
    }
    const existing = coll.get(d.id);
    if (existing) {
      if (!update) continue;
      await existing.delete();
    }
    create.push(data);
  }
  for (let i = 0; i < create.length; i += 50) await cls.createDocuments(create.slice(i, i + 50), { keepId: true });
  return create.length;
}

async function installContent({ update = false } = {}) {
  let n = 0;
  const note = ui.notifications.info(`${ROOT}: installing content…`, { permanent: true });
  for (const [pack, type, root] of PACKS) n += await importPack(pack, type, root, { update });
  note?.remove?.();
  ui.notifications.info(`${ROOT}: ${update ? "updated" : "installed"} ${n} documents.`);
  return n;
}

/* ------------------------------------------------------------------------ */
/*  Scenes                                                                  */
/* ------------------------------------------------------------------------ */
let SCENES = null;
async function sceneData() {
  if (!SCENES) SCENES = await (await fetch(`modules/${MOD}/data/scenes.json`)).json();
  return SCENES;
}

function managed(d) { return d.getFlag?.(MOD, "managed") === true; }

async function sceneLevel(scene) {
  const levels = scene?.levels?.contents ?? [];
  return scene?.initialLevel ?? levels[0] ?? null;
}

async function setBackground(scene, src, name) {
  if (gen() >= 14) {
    const level = await sceneLevel(scene);
    if (level?.update) await level.update({ "background.src": src });
    else if (scene.createEmbeddedDocuments) await scene.createEmbeddedDocuments("Level", [{ name, background: { src } }]);
  } else {
    await scene.update({ "background.src": src });
  }
}

async function ensureScene(spec, folder) {
  let scene = game.scenes.get(spec.id);
  const base = {
    _id: spec.id, name: spec.title, folder: folder.id, navigation: true, navOrder: spec.order, sort: spec.order * 1000,
    width: spec.width, height: spec.height, padding: 0,
    grid: { size: spec.grid, type: 1, distance: 5, units: "ft", alpha: 0.12, color: "#000000" },
    tokenVision: true, fog: { exploration: true },
    environment: {
      darknessLevel: spec.env.darkness ?? 0,
      globalLight: { enabled: !!spec.env.globalLight, darkness: { max: 1, min: 0 } },
      cycle: true
    },
    journal: spec.journal ?? null, journalEntryPage: spec.journalPage ?? null,
    flags: { [MOD]: { managed: true, key: spec.key, night: spec.env.night ?? null, day: spec.env.darkness ?? 0 } }
  };
  if (gen() < 14) base.background = { src: spec.src };
  else base.levels = [{ name: spec.title, background: { src: spec.src } }];
  if (!scene) {
    [scene] = await Scene.createDocuments([base], { keepId: true });
  } else {
    const { _id, ...upd } = base;
    delete upd.levels;
    delete upd.background;
    await scene.update(upd);
  }
  await setBackground(scene, spec.src, spec.title);
  return scene;
}

async function stageScene(key) {
  const all = await sceneData();
  const spec = all.scenes.find(s => s.key === key);
  if (!spec) throw new Error(`Unknown scene ${key}`);
  const folder = await ensureFolder(ROOT, "Scene");
  const scene = await ensureScene(spec, folder);
  const levelId = gen() >= 14 ? (await sceneLevel(scene))?.id : null;
  const lv = levelId ? { levels: [levelId] } : {};
  // clear previous module placeables only
  for (const [embedded, coll] of [["Wall", scene.walls], ["AmbientLight", scene.lights], ["Note", scene.notes], ["Token", scene.tokens]]) {
    const ids = coll.filter(managed).map(d => d.id);
    if (ids.length) await scene.deleteEmbeddedDocuments(embedded, ids);
  }
  const flag = { [MOD]: { managed: true } };
  const W = CONST.WALL_SENSE_TYPES, M = CONST.WALL_MOVEMENT_TYPES;
  const walls = spec.walls.map(w => {
    const d = { c: w.c, flags: flag, ...lv };
    if (w.kind === "door" || w.kind === "secret") { d.door = w.kind === "secret" ? 2 : 1; d.ds = w.locked ? 2 : 0; }
    if (w.kind === "window") { d.sight = W.NONE; d.light = W.NONE; d.sound = W.LIMITED; }
    if (w.kind === "invisible") { d.sight = W.NONE; d.light = W.NONE; d.sound = W.NONE; }
    if (w.kind === "terrain") { d.sight = W.LIMITED; d.light = W.LIMITED; d.move = M.NORMAL; d.sound = W.LIMITED; }
    if (w.sight === "none" && w.kind === "wall") { d.sight = W.NONE; d.light = W.NONE; }
    return d;
  });
  if (walls.length) await scene.createEmbeddedDocuments("Wall", walls);
  const lights = spec.lights.map(l => ({
    x: l.x, y: l.y, walls: l.walls !== false, flags: flag, ...lv,
    config: {
      dim: l.dim * 5, bright: l.bright * 5, color: l.color, alpha: l.alpha, luminosity: l.luminosity ?? 0.5,
      attenuation: 0.6, coloration: 1,
      animation: { type: l.anim ?? null, speed: l.speed ?? 3, intensity: l.intensity ?? 3, reverse: false },
      darkness: l.darkness ?? { min: 0, max: 1 }
    }
  }));
  if (lights.length) await scene.createEmbeddedDocuments("AmbientLight", lights);
  const notes = spec.notes.filter(n => game.journal.get(n.entryId)).map(n => ({
    x: n.x, y: n.y, entryId: n.entryId, pageId: n.pageId, text: n.label, flags: flag, ...lv,
    texture: { src: `modules/${MOD}/assets/icons/ic-proof.webp` }, iconSize: 48, fontSize: 22, textAnchor: 1,
    global: false
  }));
  if (notes.length) await scene.createEmbeddedDocuments("Note", notes);
  const tokens = [];
  for (const t of spec.tokens) {
    const actor = game.actors.get(t.actorId);
    if (!actor) { console.warn(`${MOD} | token actor missing`, t); continue; }
    const size = actor.prototypeToken.width * spec.grid;
    const td = await actor.getTokenDocument({ x: Math.round(t.x - size / 2), y: Math.round(t.y - size / 2), hidden: !!t.hidden });
    const data = td.toObject();
    if (t.name) data.name = t.name;
    foundry.utils.setProperty(data, `flags.${MOD}.managed`, true);
    Object.assign(data, lv);
    tokens.push(data);
  }
  if (tokens.length) await scene.createEmbeddedDocuments("Token", tokens);
  return scene;
}

async function buildScenes() {
  const all = await sceneData();
  const note = ui.notifications.info(`${ROOT}: building scenes…`, { permanent: true });
  // landing scene
  const folder = await ensureFolder(ROOT, "Scene");
  await ensureScene(all.landing, folder);
  for (const s of all.scenes) {
    try { await stageScene(s.key); } catch (e) { console.error(`${MOD} | scene ${s.key} failed`, e); }
  }
  note?.remove?.();
  ui.notifications.info(`${ROOT}: ${all.scenes.length} scenes built.`);
}

async function setupAll() {
  try {
    await installContent({ update: false });
    await buildScenes();
  } catch (e) {
    console.error(`${MOD} | setup failed`, e);
    ui.notifications.error(`${ROOT}: setup stopped (${e.message}). Open the Championship Manager to try again; press F12 for details.`, { permanent: true });
    return null;
  }
  await game.settings.set(MOD, "installedVersion", game.modules.get(MOD).version);
  const landing = game.scenes.get((await sceneData()).landing.id);
  ui.notifications.info(`${ROOT} is ready. Open Book I to begin.`);
  const book = game.journal.find(j => j.getFlag(MOD, "key") === "book1");
  book?.sheet?.render(true);
  return landing;
}

async function updateContent() {
  await installContent({ update: true });
  await game.settings.set(MOD, "installedVersion", game.modules.get(MOD).version);
}

async function removeAll() {
  const ok = await DialogV2().confirm({ window: { title: `Remove ${ROOT}` },
    content: "<p>Delete every world document and folder this module created (scenes, actors, items, journals, tables, macros)? Anything you created yourself is kept.</p>" });
  if (!ok) return;
  for (const coll of [game.scenes, game.actors, game.items, game.journal, game.tables, game.macros]) {
    const ids = coll.filter(managed).map(d => d.id);
    if (ids.length) await coll.documentClass.deleteDocuments(ids);
  }
  const fids = game.folders.filter(managed).map(f => f.id);
  if (fids.length) await Folder.deleteDocuments(fids);
  await game.settings.set(MOD, "installedVersion", "");
  ui.notifications.info(`${ROOT} removed.`);
}


/* ------------------------------------------------------------------------ */
/*  Championship Board: Proofs, Crown Marks, the three clocks, the seals    */
/* ------------------------------------------------------------------------ */
const Board = {
  el: null,
  state() { return foundry.utils.deepClone(game.settings.get(MOD, "board")); },
  async set(s) { if (!game.user.isGM) return; await game.settings.set(MOD, "board", s); },
  async toggle(v) { const s = this.state(); s.visible = v ?? !s.visible; await this.set(s); },
  async addSlate() {
    const name = await DialogV2().prompt({ window: { title: "Register a Claimant or Slate" },
      content: `<div class="ipc-form"><label>Name <input type="text" name="n" value="Rival Slate"></label></div>`,
      ok: { label: "Register", callback: (e, b) => b.form.elements.n.value }, rejectClose: false });
    if (!name) return;
    const s = this.state(); s.slates.push({ name, survival: false, deviousness: false, dominion: false, marks: 0 }); await this.set(s);
  },
  async act(a, i) {
    const s = this.state();
    const sl = s.slates[i];
    if (a === "remove") s.slates.splice(i, 1);
    else if (a === "mark+") sl.marks++;
    else if (a === "mark-") sl.marks = Math.max(0, sl.marks - 1);
    else if (["survival", "deviousness", "dominion"].includes(a)) {
      sl[a] = !sl[a];
      if (sl[a]) chat(`<p class="ipc-ruling">PROOF OF ${a.toUpperCase()} CERTIFIED</p><p><strong>${esc(sl.name)}</strong> has proved ${a}.</p>`);
    } else if (a.startsWith("clock")) {
      const [, k, d] = a.split(":"); s.clocks[k] = Math.max(0, Math.min(6, s.clocks[k] + Number(d)));
      if (s.clocks[k] === 6) chat(`<p class="ipc-ruling">${CLOCKS[k].toUpperCase()} IS FULL</p>`);
    } else if (a.startsWith("seal")) {
      const k = a.split(":")[1]; s.seals[k] = !s.seals[k];
      if (s.seals[k]) chat(`<p class="ipc-ruling">${SEALS[k].toUpperCase()} SUPPRESSED</p><p>${SEAL_FX[k]}</p>` +
        (Object.values(s.seals).filter(Boolean).length >= 2 ? `<p><strong>Two seals are down. The Heartstone's screen can now be targeted.</strong></p>` : ""));
    }
    await this.set(s);
  },
  refresh() {
    const s = this.state();
    if (!s.visible) { this.el?.remove(); this.el = null; return; }
    if (!this.el) {
      this.el = document.createElement("div"); this.el.id = "ipc-board";
      document.body.appendChild(this.el);
      this.el.addEventListener("click", ev => {
        const b = ev.target.closest("[data-act]"); if (!b || !game.user.isGM) return;
        const a = b.dataset.act;
        if (a === "add") return this.addSlate();
        if (a === "close") return this.toggle(false);
        this.act(a, Number(b.dataset.i ?? 0));
      });
    }
    const gm = game.user.isGM;
    const pip = (on, act, i, label) => `<span class="ipc-proof ${on ? "on" : ""}" ${gm ? `data-act="${act}" data-i="${i}"` : ""} title="${label}">${label[0]}</span>`;
    const rows = s.slates.map((sl, i) => `<div class="ipc-slate"><span class="nm">${esc(sl.name)}</span>
      ${pip(sl.survival, "survival", i, "Survival")}${pip(sl.deviousness, "deviousness", i, "Deviousness")}${pip(sl.dominion, "dominion", i, "Dominion")}
      <span class="ipc-marks">${gm ? `<a data-act="mark-" data-i="${i}">−</a>` : ""}<b>${sl.marks}</b> ♛${gm ? `<a data-act="mark+" data-i="${i}">+</a>` : ""}</span>
      ${gm && i > 0 ? `<a class="x" data-act="remove" data-i="${i}">✕</a>` : ""}</div>`).join("");
    const clocks = Object.entries(CLOCKS).map(([k, n]) => `<div class="ipc-clock"><span>${n}</span><span class="seg">${[1, 2, 3, 4, 5, 6].map(j => `<i class="${j <= s.clocks[k] ? "on" : ""} ${k}"></i>`).join("")}</span>
      ${gm ? `<a data-act="clock:${k}:-1">−</a><a data-act="clock:${k}:1">+</a>` : ""}</div>`).join("");
    const seals = Object.entries(SEALS).map(([k, n]) => `<span class="ipc-seal ${s.seals[k] ? "down" : ""}" ${gm ? `data-act="seal:${k}"` : ""}>${n.replace("Seal of ", "")}</span>`).join("");
    this.el.innerHTML = `<header>The Championship of the First Crown ${gm ? `<a data-act="close">✕</a>` : ""}</header>
      <div class="ipc-slates">${rows}</div>${gm ? `<a class="ipc-add" data-act="add">+ register a claimant or slate</a>` : ""}
      <div class="ipc-clocks">${clocks}</div><div class="ipc-seals"><span>Heartstone seals</span>${seals}</div>`;
  }
};

function chat(content, alias = "The Brass Arbiter") {
  return ChatMessage.create({ content: `<div class="ipc-chat">${content}</div>`, speaker: { alias } });
}

/* ------------------------------------------------------------------------ */
/*  Arena engine: initiative count 20                                       */
/* ------------------------------------------------------------------------ */
const ARENA = {
  15: { 1: ["Uneventful cycle", ""], 2: ["Electric arcs", "DC 17 Dex, [[/damage 3d8 lightning]] in the marked side lanes"],
        3: ["Blue crystal", "DC 17 Con, [[/damage 3d8 necrotic]] within 15 ft of the blue crystals"],
        4: ["Four lava fissures", "DC 17 Dex, [[/damage 3d10 fire]] within 10 ft of an active line"],
        5: ["Yellow crystal", "DC 17 Wis, [[/damage 3d8 radiant]] within 15 ft of the yellow crystals"],
        6: ["Summoning glyph", "Roll the level-15 summons table"] },
  17: { 1: ["Uneventful cycle", ""], 2: ["Electric arcs", "DC 19 Dex, [[/damage 4d8 lightning]] in the marked side lanes"],
        3: ["Blue crystal", "DC 19 Con, [[/damage 4d8 necrotic]] within 15 ft of the blue crystals"],
        4: ["Four lava fissures", "DC 19 Dex, [[/damage 4d10 fire]] within 10 ft of an active line"],
        5: ["Yellow crystal", "DC 19 Wis, [[/damage 4d8 radiant]] within 15 ft of the yellow crystals"],
        6: ["Summoning glyph", "Roll the final-tier summons table"] }
};
async function arenaHazard(tier = null) {
  tier ??= await DialogV2().wait({ window: { title: "Arena Hazard" }, content: "<p>Which tier?</p>",
    buttons: [{ action: "15", label: "Level 15 preliminary" }, { action: "17", label: "Level 17 final" }] });
  if (!tier) return;
  const r = await new Roll("1d6").evaluate();
  const [name, fx] = ARENA[tier][r.total];
  await r.toMessage({ flavor: `<div class="ipc-chat"><p class="ipc-ruling">ARENA CYCLE: ${name.toUpperCase()}</p><p>${fx || "The arena holds its breath."}</p><p class="hint">Telegraphed now; resolves at initiative count 20. A creature next to a crystal can suppress it (action, DC 17 Arcana) or destroy it (AC 16, 25 HP) for two rounds.</p></div>` });
  if (r.total === 6) {
    const key = tier === "15" || tier === 15 ? "arena-summons-15" : "arena-summons-17";
    const t = game.tables.find(x => x.getFlag(MOD, "key") === key);
    if (t) await t.draw(); else ui.notifications.warn("Install the roll tables first.");
  }
}

/* ------------------------------------------------------------------------ */
/*  Tribunal and mass battle                                                */
/* ------------------------------------------------------------------------ */
async function tribunal() {
  const res = await DialogV2().prompt({ window: { title: "Convene a Hearing" },
    content: `<div class="ipc-form"><label>Matter <input type="text" name="m" value="Petition M-9"></label>
      <label>Format <select name="f"><option value="stages">Three stages: Admissibility, Authority, Remedy</option>
      <option value="2v2">Two successes before two failures</option><option value="3v2">Three successes before two failures</option></select></label>
      <label>Disputed DC <input type="number" name="dc" value="18"></label></div>`,
    ok: { label: "Open the Hearing", callback: (e, b) => ({ m: b.form.elements.m.value, f: b.form.elements.f.value, dc: Number(b.form.elements.dc.value) || 18 }) },
    rejectClose: false });
  if (!res) return;
  const stages = res.f === "stages" ? ["Admissibility", "Authority", "Remedy"] : null;
  const need = res.f === "3v2" ? 3 : 2;
  let s = 0, f = 0, i = 0;
  await chat(`<p class="ipc-ruling">THE BRASS ARBITER IS SEATED</p><p><strong>${esc(res.m)}</strong>. Identify the instrument, the clause, who owns the right, the evidence of consent or default, and the remedy. Correct evidence wins without a roll; an improvised argument is DC ${res.dc}.</p>`);
  while (true) {
    const label = stages ? `Stage ${i + 1}: ${stages[i]}` : `Argument ${s + f + 1} (${s}/${need} successes, ${f}/2 failures)`;
    const r = await DialogV2().wait({ window: { title: esc(res.m) }, content: `<p><strong>${label}</strong></p>`,
      buttons: [{ action: "ev", label: "Correct evidence (no roll)" }, { action: "win", label: "Argued: success" },
                { action: "lose", label: "Argued: failure" }, { action: "end", label: "Close the hearing" }] });
    if (!r || r === "end") break;
    if (r === "ev" || r === "win") s++; else f++;
    await chat(`<p><strong>${label}.</strong> ${r === "ev" ? "Authentic evidence: the point is won without a roll." : r === "win" ? "The argument is sustained." : "The argument is not sustained."}</p>`);
    i++;
    if (stages && i >= 3) {
      const out = s >= 3 ? "Full relief: universal first-refusal denied and a two-session injunction imposed." :
        s === 2 ? "Universal first-refusal is denied." : "A limited thirty-day concession is permitted unless the claim is withdrawn.";
      await chat(`<p class="ipc-ruling">JUDGMENT: ${s} OF 3 STAGES</p><p>${out}</p>`); break;
    }
    if (!stages && s >= need) { await chat(`<p class="ipc-ruling">PETITION DECIDED FOR THE CLAIMANT</p>`); break; }
    if (!stages && f >= 2) { await chat(`<p class="ipc-ruling">PETITION FAILS</p><p>The adventure continues. Misty gains one interference token and offers a lawful settlement.</p>`); break; }
  }
}

async function massBattle() {
  let adv = 0, cost = 0;
  await chat(`<p class="ipc-ruling">THE ASH MARCH</p><p>Three exchanges. Each needs a group plan, then two relevant checks against DC 17 (one character can't make both). Success scores an Advantage; failure scores a Cost.</p>`, "The Convoy");
  for (let x = 1; x <= 3; x++) {
    for (let c = 1; c <= 2; c++) {
      const r = await DialogV2().wait({ window: { title: `Exchange ${x}, check ${c}` }, content: `<p>Advantages ${adv} · Costs ${cost}</p>`,
        buttons: [{ action: "a", label: "Success (Advantage)" }, { action: "c", label: "Failure (Cost)" }, { action: "end", label: "Stop" }] });
      if (!r || r === "end") { x = 4; break; }
      if (r === "a") adv++; else cost++;
    }
  }
  const lines = [];
  lines.push(adv >= 3 ? "The convoy survives and the survivors publicly support the claimants (Public Legitimacy +1)." :
    adv >= 2 ? "The convoy survives." : "The convoy is badly mauled.");
  if (cost >= 3) lines.push("The outpost survives but loses half its supplies. Blood War Pressure rises.");
  else if (cost >= 2) lines.push("Run a short fight: two winged Writ Bailiffs and one Ash-Scrap Golem.");
  await chat(`<p class="ipc-ruling">${adv} ADVANTAGES · ${cost} COSTS</p>${lines.map(l => `<p>${l}</p>`).join("")}`, "The Convoy");
  if (cost >= 3) await Board.act("clock:war:1");
  if (adv >= 3) await Board.act("clock:legit:1");
}

async function presentExhibit() {
  const ex = game.items.filter(i => i.getFlag(MOD, "managed") && i.name.startsWith("Exhibit"));
  if (!ex.length) return ui.notifications.warn("Install the content first.");
  const opts = ex.map(i => `<option value="${i.id}">${esc(i.name)}</option>`).join("");
  const res = await DialogV2().prompt({ window: { title: "Present an Exhibit" },
    content: `<div class="ipc-form"><label>Exhibit <select name="e">${opts}</select></label><label>Offered against <input type="text" name="t" value=""></label></div>`,
    ok: { label: "Present", callback: (e, b) => ({ e: b.form.elements.e.value, t: b.form.elements.t.value }) }, rejectClose: false });
  if (!res) return;
  const it = game.items.get(res.e);
  await chat(`<p>The Arbiter receives <em>${esc(it.name)}</em>${res.t ? ` against <strong>${esc(res.t)}</strong>` : ""}.</p>${it.system.description.value}<p class="ipc-ruling">"EVIDENCE RECEIVED. STATE THE CLAUSE."</p>`);
}

async function showHandout() {
  const j = game.journal.find(x => x.getFlag(MOD, "key") === "handouts");
  if (!j) return ui.notifications.warn("Install the content first.");
  const opts = j.pages.contents.sort((a, b) => a.sort - b.sort).map(p => `<option value="${p.id}">${esc(p.name)}</option>`).join("");
  const id = await DialogV2().prompt({ window: { title: "Show a Handout" }, content: `<div class="ipc-form"><select name="p">${opts}</select></div>`,
    ok: { label: "Show to Players", callback: (e, b) => b.form.elements.p.value }, rejectClose: false });
  if (!id) return;
  const page = j.pages.get(id);
  await j.update({ "ownership.default": CONST.DOCUMENT_OWNERSHIP_LEVELS.OBSERVER });
  Journal.showDialog ? Journal.showDialog(page) : game.socket.emit("showEntry", page.uuid, { force: true });
  page.sheet?.render(true);
}

const Challenge = { s: 0, f: 0, need: 3, fail: 2, name: "" };
async function skillChallenge() {
  const res = await DialogV2().prompt({ window: { title: "Group Challenge" },
    content: `<div class="ipc-form"><label>Name <input type="text" name="n" value="The Ash Bridge"></label>
      <label>Successes needed <input type="number" name="s" value="3"></label><label>Failures allowed <input type="number" name="f" value="2"></label>
      <label>DC <input type="number" name="dc" value="16"></label></div>`,
    ok: { label: "Start", callback: (e, b) => ({ n: b.form.elements.n.value, s: Number(b.form.elements.s.value), f: Number(b.form.elements.f.value), dc: Number(b.form.elements.dc.value) }) },
    rejectClose: false });
  if (!res) return;
  let s = 0, f = 0;
  await chat(`<p class="ipc-ruling">${esc(res.n).toUpperCase()}</p><p>${res.s} successes before ${res.f} failures, DC ${res.dc}. Any skill, spell or clever support can contribute.</p>`, "Group Challenge");
  while (s < res.s && f < res.f) {
    const r = await DialogV2().wait({ window: { title: esc(res.n) }, content: `<p>${s} successes · ${f} failures</p>`,
      buttons: [{ action: "s", label: "Success" }, { action: "f", label: "Failure" }, { action: "x", label: "Stop" }] });
    if (!r || r === "x") return;
    if (r === "s") s++; else f++;
  }
  await chat(s >= res.s ? `<p class="ipc-ruling">SUCCESS</p>` : `<p class="ipc-ruling">FAILURE</p><p>On the Ash Bridge: one exposed character takes [[/damage 3d8 fire]], or a resource is spent to prevent it. No instant death from lava at a procedural entry point.</p>`, "Group Challenge");
}

async function requestSave() {
  const abil = ["str", "dex", "con", "int", "wis", "cha"].map(a => `<option value="${a}">${CONFIG.DND5E?.abilities?.[a]?.label ?? a}</option>`).join("");
  const res = await DialogV2().prompt({ window: { title: "Request a Group Save" },
    content: `<div class="ipc-form"><label>Ability <select name="a">${abil}</select></label><label>DC <input type="number" name="dc" value="17"></label><label>Reason <input type="text" name="why" value=""></label></div>`,
    ok: { label: "Post", callback: (e, b) => ({ a: b.form.elements.a.value, dc: b.form.elements.dc.value, why: b.form.elements.why.value }) }, rejectClose: false });
  if (!res) return;
  chat(`<p>${esc(res.why || "Make a saving throw.")}</p><p>[[/save ${res.a} ${Number(res.dc) || 10}]]</p>`, ROOT);
}

async function mythicPhase() {
  await chat(`<p><em>Misty does not fall. The audience chamber folds like a letter, and every combatant stands in her resting place: a sleeping dais, two bridges over fire, four hanging iron roses, and somewhere behind a prismatic screen, a heartbeat that is not hers.</em></p>
    <p class="ipc-ruling">"You have mistaken my courtroom for my home. Shall I show you the difference?"</p>
    <p>Hag Queen's Deception: Misty restores 144 HP and two Children of Hell appear within 30 ft. Swap to the <strong>Misty, Unbound</strong> actor on the Thorn Reliquary scene. Legendary Resistances, daily spells and suppressed seals do not reset.</p>`, "Misty");
  const r = game.scenes.find(s => s.getFlag(MOD, "key") === "reliquary");
  if (r) r.view();
}

/* ------------------------------------------------------------------------ */
/*  Manager                                                                 */
/* ------------------------------------------------------------------------ */
class Manager extends foundry.applications.api.ApplicationV2 {
  static DEFAULT_OPTIONS = {
    id: "ipc-manager", tag: "div", classes: ["ipc-app"],
    window: { title: "Interplanal Champions — Manager", icon: "fa-solid fa-crown", resizable: true },
    position: { width: 520, height: "auto" },
    actions: {
      setupAll: async function () { await setupAll(); this.render(); },
      install: async function () { await installContent(); this.render(); },
      update: async function () { await updateContent(); this.render(); },
      scenes: async function () { await buildScenes(); this.render(); },
      stage: async function (e, t) { await stageScene(t.dataset.key); ui.notifications.info("Scene rebuilt."); },
      board: async function () { await Board.toggle(true); },
      redline: async function () { await Redline.toggle(true); },
      remove: async function () { await removeAll(); this.render(); }
    }
  };
  async _renderHTML() {
    const ver = game.modules.get(MOD).version, inst = game.settings.get(MOD, "installedVersion");
    const all = await sceneData();
    const rows = all.scenes.map(s => `<li><span>${esc(s.title)}</span><button type="button" data-action="stage" data-key="${s.key}" title="Rebuild walls, lights, pins and tokens"><i class="fa-solid fa-rotate"></i></button></li>`).join("");
    return `<div class="ipc-manager">
      <header class="ipc-mhead"><img src="modules/${MOD}/assets/art/banner.webp" alt=""><p>Module ${ver} · World content ${inst || "not installed"}</p></header>
      <section><button type="button" class="ipc-big" data-action="setupAll"><i class="fa-solid fa-wand-magic-sparkles"></i> Set Up Everything</button>
        <div class="ipc-row"><button type="button" data-action="install"><i class="fa-solid fa-download"></i> Install Content</button>
        <button type="button" data-action="update"><i class="fa-solid fa-arrows-rotate"></i> Update Content</button>
        <button type="button" data-action="scenes"><i class="fa-solid fa-map"></i> Rebuild All Scenes</button></div></section>
      <section><h3>Scenes</h3><ul class="ipc-scenes">${rows}</ul></section>
      <section><h3>At the Table</h3><div class="ipc-row"><button type="button" data-action="board"><i class="fa-solid fa-crown"></i> Show the Championship Board</button>
        <button type="button" data-action="redline"><i class="fa-solid fa-truck-monster"></i> Redline Run Tracker</button></div></section>
      <section class="ipc-danger"><button type="button" data-action="remove"><i class="fa-solid fa-trash"></i> Remove Module Content</button></section>
    </div>`;
  }
  _replaceHTML(result, content) { content.innerHTML = result; }
}

/* ------------------------------------------------------------------------ */
/*  The Redline Run: chase tracker (round, Lead, Heat, Sparks) and soul coins */
/* ------------------------------------------------------------------------ */
async function drawKey(key) {
  const t = game.tables.find(x => x.getFlag(MOD, "key") === key);
  if (!t) { ui.notifications.warn("Install the roll tables first."); return null; }
  const d = await t.draw({ displayChat: false });
  const r = d.results[0];
  return { total: d.roll.total, text: r?.description || r?.text || r?.name || "" };
}

const HEAT_FX = ["Stable", "Stable", "Stable", "Strained (warning)", "Strained (warning)", "CRITICAL: Pulse/Overburn mishaps on 1–2", "RUPTURE"];
const Redline = {
  el: null,
  state() { return foundry.utils.deepClone(game.settings.get(MOD, "redline")); },
  async set(s) { if (!game.user.isGM) return; await game.settings.set(MOD, "redline", s); },
  async toggle(v) { const s = this.state(); s.visible = v ?? !s.visible; await this.set(s); },
  async reset() {
    const s = this.state(); s.round = 1; s.lead = 2; s.vehicles.forEach(v => { v.heat = 0; }); await this.set(s);
    chat(`<p class="ipc-ruling">THE REDLINE RUN BEGINS</p><p>Round 1 · Lead 2. The loudspeaker demands the heart.</p>`, "Marshal Kestrel Vane");
  },
  async addVehicle() {
    const name = await DialogV2().prompt({ window: { title: "Add a Machine" },
      content: `<div class="ipc-form"><label>Name <input type="text" name="n" value="Scorchhound Quad"></label>
        <label>Sparks <input type="number" name="sp" value="0"></label><label>Fuel (hours) <input type="number" name="f" value="6"></label></div>`,
      ok: { label: "Add", callback: (e, b) => ({ n: b.form.elements.n.value, sp: Number(b.form.elements.sp.value), f: Number(b.form.elements.f.value) }) },
      rejectClose: false });
    if (!name) return;
    const s = this.state(); s.vehicles.push({ name: name.n, heat: 0, sparks: name.sp, fuel: name.f, echo: "" }); await this.set(s);
  },
  async act(a, i) {
    const s = this.state(); const v = s.vehicles[i];
    if (a === "lead+") s.lead = Math.min(6, s.lead + 1);
    else if (a === "lead-") s.lead = Math.max(0, s.lead - 1);
    else if (a === "heat+") {
      v.heat = Math.min(6, v.heat + 1);
      if (v.heat === 6) {
        chat(`<p class="ipc-ruling">FURNACE RUPTURE: ${esc(v.name)}</p><p>[[/damage 3d10 fire]] that bypasses the damage threshold. Roll a vehicle mishap. Heat resets to 3.</p>`);
        await drawKey("vehicle-mishap").then(r => r && chat(`<p><strong>Vehicle mishap (${r.total}).</strong> ${r.text}</p>`));
        v.heat = 3;
      } else if (v.heat === 5) chat(`<p class="ipc-ruling">${esc(v.name)} IS CRITICAL</p><p>Each further Pulse or Overburn triggers a furnace mishap on a d6 roll of 1–2.</p>`);
    }
    else if (a === "heat-") v.heat = Math.max(0, v.heat - 1);
    else if (a === "spark-") {
      if (v.sparks <= 0) return ui.notifications.warn("No Sparks left in that furnace.");
      v.sparks--; v.heat = Math.min(6, v.heat + 1);
      chat(`<p class="ipc-ruling">PULSE: ${esc(v.name)}</p><p>${esc(v.echo || "The bound soul")} answers. Sparks ${v.sparks}, Heat ${v.heat}.</p>`);
      if (v.heat >= 6) { await this.set(s); return this.act("heat+", i); }
    }
    else if (a === "spark+") v.sparks = Math.min(9, v.sparks + 1);
    else if (a === "remove") s.vehicles.splice(i, 1);
    await this.set(s);
  },
  async nextRound() {
    const s = this.state();
    s.round = Math.min(9, s.round + 1);
    await this.set(s);
    if (s.round > 8) return chat(`<p class="ipc-ruling">THE LAST CUT</p><p>Round 8 is over at Lead ${s.lead}. Lead 4–5: clean escape. Lead 2–3: escape at a cost. Lead 0–1: the Reclaimer locks on.</p>`);
    const turning = { 2: "<strong>The First Notice.</strong> Kestrel broadcasts the writ. Reward the first player to ask for a copy.",
                      4: "<strong>The Crystal Maw.</strong> The south claws burst and block one lane (DC 17 driving, or clear AC 16, 35 HP).",
                      7: "<strong>The Blackspine Gate.</strong> Only the centre lane remains. At Lead 4+, a DC 16 drive escapes at once." };
    const hz = await drawKey("road-hazard"), en = await drawKey("enemy-plan");
    chat(`<p class="ipc-ruling">REDLINE RUN · ROUND ${s.round} · LEAD ${s.lead}</p>` + (turning[s.round] ? `<p>${turning[s.round]}</p>` : "")
      + (hz ? `<p><strong>Road hazard (${hz.total}).</strong> ${hz.text}</p>` : "") + (en ? `<p><strong>Enemy plan (${en.total}).</strong> ${en.text}</p>` : "")
      + `<p class="hint">Announce both before anyone acts. End of round: lead driver DC 16 Dex (land vehicles); quiet furnaces cool by 1 Heat.</p>`, "The Blackspine Narrows");
  },
  refresh() {
    const s = this.state();
    if (!s.visible) { this.el?.remove(); this.el = null; return; }
    if (!this.el) {
      this.el = document.createElement("div"); this.el.id = "ipc-redline";
      document.body.appendChild(this.el);
      this.el.addEventListener("click", ev => {
        const b = ev.target.closest("[data-act]"); if (!b || !game.user.isGM) return;
        const a = b.dataset.act;
        if (a === "close") return this.toggle(false);
        if (a === "round") return this.nextRound();
        if (a === "reset") return this.reset();
        if (a === "add") return this.addVehicle();
        if (a === "coin") return readSoulCoin();
        this.act(a, Number(b.dataset.i ?? 0));
      });
    }
    const gm = game.user.isGM;
    const seg = (n, on, cls) => [...Array(n).keys()].map(j => `<i class="${j < on ? "on" : ""} ${cls}"></i>`).join("");
    const rows = s.vehicles.map((v, i) => `<div class="ipc-veh"><span class="nm">${esc(v.name)}</span>
      <span class="ipc-heat" title="${HEAT_FX[v.heat]}">Heat ${gm ? `<a data-act="heat-" data-i="${i}">−</a>` : ""}<span class="seg">${seg(6, v.heat, "heat")}</span>${gm ? `<a data-act="heat+" data-i="${i}">+</a>` : ""}</span>
      <span class="ipc-sparks">Sparks <b>${v.sparks}</b>${gm ? ` <a data-act="spark+" data-i="${i}">+</a><a data-act="spark-" data-i="${i}" title="Pulse: spend 1 Spark, +1 Heat">Pulse</a>` : ""}</span>
      ${gm ? `<a class="x" data-act="remove" data-i="${i}">✕</a>` : ""}</div>`).join("");
    this.el.innerHTML = `<header>The Redline Run · Round ${Math.min(8, s.round)} of 8 ${gm ? `<a data-act="close">✕</a>` : ""}</header>
      <div class="ipc-lead"><span>Lead</span>${gm ? `<a data-act="lead-">−</a>` : ""}<span class="seg">${seg(6, s.lead, "lead")}</span>${gm ? `<a data-act="lead+">+</a>` : ""}<b>${s.lead}</b></div>
      <div class="ipc-vehs">${rows}</div>
      ${gm ? `<div class="ipc-rl-btns"><a data-act="round">Next round ▸</a><a data-act="add">+ machine</a><a data-act="coin">Read a soul coin</a><a data-act="reset">Reset</a></div>` : ""}`;
  }
};

async function readSoulCoin() {
  const echo = await drawKey("soul-echo"); if (!echo) return;
  const voice = await drawKey("soul-voice"), claim = await drawKey("soul-claim"), ch = await drawKey("soul-charges");
  const mist = (await new Roll("1d6").evaluate()).total <= 2;
  chat(`<p class="ipc-ruling">A SOUL COIN SPEAKS</p><p><strong>Echo (${echo.total}).</strong> ${echo.text}</p>`
    + `<p><strong>Voice.</strong> ${voice?.text ?? ""}</p><p><strong>Claim record.</strong> ${claim?.text ?? ""}</p>`
    + `<p><strong>Charges.</strong> ${ch?.text ?? ""} (each = 24 hours of fuel and 1 Spark)</p>`
    + (mist ? `<p><strong>Salvage only:</strong> this coin bears Misty's <strong>MIST-113</strong> seal. Her agents learn where it is.</p>` : "")
    + `<p class="hint">Identify (DC 14 Arcana or Religion) reveals this to the players. Every soul coin is a person.</p>`, "The Soul Furnace");
}

async function generateSoul() {
  const arch = await drawKey("sf-archetype"); if (!arch) return;
  const o = await drawKey("sf-order"), m = await drawKey("sf-morality");
  const ord = o?.text?.replace(/<[^>]+>/g, "") ?? "", mor = m?.text?.replace(/<[^>]+>/g, "") ?? "";
  const al = ord === "Neutral" && mor === "Neutral" ? "True Neutral" : `${ord} ${mor}`;
  const parts = [];
  for (const [k, n] of [["sf-motivation", "Core motivation"], ["sf-manner", "Speaking manner"], ["sf-contradiction", "Contradiction"], ["sf-grievance", "Grievance"], ["soul-voice", "Voice"], ["soul-claim", "Claim record"]]) {
    const r = await drawKey(k); if (r) parts.push(`<p><strong>${n}.</strong> ${r.text}</p>`);
  }
  chat(`<p class="ipc-ruling">A SOUL WAKES IN THE FURNACE</p><p><strong>Archetype (${arch.total}).</strong> ${arch.text}</p>`
    + `<p><strong>Alignment.</strong> ${al}</p>` + parts.join("")
    + `<p class="hint">Give it a name, a former species and homeland, and one meaningful memory. Record it on Form SF-01.</p>`, "The Soulforged");
}

const API = {
  openManager: () => new Manager().render(true), setupAll, installContent, updateContent, buildScenes, stageScene, removeAll,
  board: Board, arenaHazard, tribunal, massBattle, presentExhibit, showHandout, skillChallenge, requestSave, mythicPhase, chat,
  redline: Redline, readSoulCoin, generateSoul
};
