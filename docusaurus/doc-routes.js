// Runtime routing configuration for the physical documentation move, not an
// evidence registry. Existing exclusions retain their identity at the new paths.
const moves = require('./doc-paths.json');
const excluded = [
  'development/BUILD.md', 'development/DEVELOPMENT.md', 'reference/recovery.md',
  'registry/current-validation.md', 'registry/pedal-validation.md',
  'registry/pedal-profiles.md', 'registry/pedal-closure.md',
  'registry/virtual-pedals.md', 'registry/handbrake.md', 'registry/virtual-handbrake.md',
  'steering.md', 'synthetic.md', 'pedals.md', 'pedal-join-contract.md',
  'transmission.md', 'checkpoint1.md', 'checkpoint2.md', 'presentation.md',
  'unknowns.md', 'history/legacy/README.md', 'history/legacy/resolution-workflow/README.md'
].map(old => moves[old]);
function route(file) {
  return '/docs/' + file.replace(/\.md$/, '').replace(/\/index$/, '');
}
const redirects = Object.entries(moves)
  .filter(([, next]) => !excluded.includes(next))
  .map(([old, next]) => ({from: route(old), to: route(next)}))
  .filter(({from, to}) => from !== to);
module.exports = {moves, excluded, route, redirects};
