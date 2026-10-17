module.exports = {knowledge: [
  {type: 'category', label: 'Start Here', link: {type: 'doc', id: 'start-here/index'}, items: [
    'start-here/quick-start', 'start-here/goals', 'start-here/terminology', 'start-here/current-status', 'start-here/continuation'
  ]},
  {type: 'category', label: 'Developer Guide', collapsed: false, link: {type: 'doc', id: 'developer-guide/index'}, items: [
    'developer-guide/environment', 'developer-guide/build-and-run', 'developer-guide/workflow',
    'developer-guide/recovery-method', 'developer-guide/representations', 'developer-guide/validation',
    {type: 'category', label: 'Worked example: MT selector', link: {type: 'doc', id: 'developer-guide/worked-example-mt-selector/index'}, items: [
      'developer-guide/worked-example-mt-selector/identify-and-bound',
      'developer-guide/worked-example-mt-selector/trace-and-contract',
      'developer-guide/worked-example-mt-selector/implementation',
      'developer-guide/worked-example-mt-selector/differential-validation',
      'developer-guide/worked-example-mt-selector/live-validation-and-lessons'
    ]},
    'developer-guide/troubleshooting', 'developer-guide/contributing', 'developer-guide/publication', 'developer-guide/continuation'
  ]},
  {type: 'category', label: 'Architecture', link: {type: 'doc', id: 'architecture/index'}, items: [
    'architecture/execution', 'architecture/products-and-bindings', 'architecture/controls',
    'architecture/transmission', 'architecture/enhancements', 'architecture/playable-and-headless'
  ]},
  {type: 'category', label: 'Reference', link: {type: 'doc', id: 'reference/index'}, items: [
    'reference/commands', 'reference/supported-profile', 'reference/repository-layout',
    'reference/authorization', 'reference/authorities', 'reference/historical-knowledge-schema',
    'reference/generated/current-products', 'reference/generated/status', 'reference/generated/symbols', 'reference/generated/types'
  ]},
  {type: 'category', label: 'Research & Evidence', collapsed: true, link: {type: 'doc', id: 'research/index'}, items: [
    {type: 'category', label: 'Controls and steering', link: {type: 'doc', id: 'research/controls/index'}, items: [
      'research/controls/mapped-actions', 'research/controls/pad-steering-trace', 'research/controls/wheel-steering-trace',
      'research/controls/steering-recovery', 'research/controls/synthetic-wheel'
    ]},
    {type: 'category', label: 'Pedals', link: {type: 'doc', id: 'research/pedals/index'}, items: [
      'research/pedals/stopped-prerequisite-audit', 'research/pedals/recovery-v1', 'research/pedals/profile-survey',
      'research/pedals/admission-49af40', 'research/pedals/closure', 'research/pedals/virtual-input-v1'
    ]},
    {type: 'category', label: 'Handbrake', link: {type: 'doc', id: 'research/handbrake/index'}, items: [
      'research/handbrake/recovery-v1', 'research/handbrake/virtual-input-v1'
    ]},
    {type: 'category', label: 'Transmission', link: {type: 'doc', id: 'research/transmission/index'}, items: [
      'research/transmission/producer-consumer-map', 'research/transmission/reverse-investigation',
      'research/transmission/power-transfer', 'research/transmission/mt-selector-v1',
      'research/transmission/speed-search-v1', 'research/transmission/state-transitions-v1'
    ]},
    {type: 'category', label: 'Enhancement experiments', link: {type: 'doc', id: 'research/enhancements/index'}, items: [
      'research/enhancements/architecture-proposal', 'research/enhancements/stopped-boundary-audit', 'research/enhancements/virtual-transmission-v1'
    ]},
    {type: 'category', label: 'Platform and presentation', link: {type: 'doc', id: 'research/platform/index'}, items: [
      'research/platform/resolution', 'research/platform/presentation', 'research/platform/lan-streaming'
    ]},
    {type: 'category', label: 'Provenance', link: {type: 'doc', id: 'research/provenance/index'}, items: [
      'research/provenance/upstream-contributions'
    ]},
    {type: 'category', label: 'Evaluated checkpoints', link: {type: 'doc', id: 'research/checkpoints/index'}, items: [
      'research/checkpoints/native-v3-baseline', 'research/checkpoints/consolidation', 'research/checkpoints/status-history',
      'research/checkpoints/restructuring', 'research/checkpoints/historical-queue'
    ]},
    {type: 'category', label: 'Unresolved reconnaissance', link: {type: 'doc', id: 'research/reconnaissance/index'}, items: [
      'research/reconnaissance/force-feedback', 'research/reconnaissance/telemetry', 'research/reconnaissance/reset-step'
    ]},
    'research/retained-summaries/index'
  ]}
]};
