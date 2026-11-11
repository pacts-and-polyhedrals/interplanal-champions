
import { compilePack } from '@foundryvtt/foundryvtt-cli';
const packs = ["journals", "actors", "pregens", "items", "spells", "options", "tables", "macros"];
for (const p of packs) await compilePack('/home/claude/ic/build/packs/' + p, '/home/claude/ic/module/packs/' + p, { log: false });
console.log('compiled', packs.length);
