// Documentation parser test only; no game/runtime or physical-device work.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {JSDOM} from 'jsdom';
const window = new JSDOM('<!doctype html><html><body></body></html>').window;
globalThis.window = window;
globalThis.document = window.document;
const mermaid = (await import('mermaid')).default;
mermaid.initialize({startOnLoad:false, securityLevel:'strict'});
const docs = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../docs');
let count=0;
for (const file of fs.readdirSync(docs).filter(f=>f.endsWith('.md'))) {
  const text=fs.readFileSync(path.join(docs,file),'utf8');
  for (const graph of text.matchAll(/```mermaid\n([\s\S]*?)```/g)) {
    try { await mermaid.parse(graph[1]); count++; }
    catch (error) { throw new Error(`Invalid diagram in ${file}`, {cause:error}); }
  }
}
if (count<10) throw new Error(`Required project diagrams missing: ${count}`);
console.log(`Mermaid syntax PASS: ${count} diagrams`);
window.close();
