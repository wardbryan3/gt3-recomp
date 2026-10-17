module.exports = {
  title: 'GT3 Recomp',
  tagline: 'Recover first. Modify second.',
  url: 'http://localhost:3100',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {format: 'detect', mermaid: true, hooks: {onBrokenMarkdownLinks: 'throw'}},
  themes: ['@docusaurus/theme-mermaid'],
  presets: [['classic', {
    docs: {
      sidebarPath: require.resolve('./sidebars.js'),
      routeBasePath: 'docs',
      // Retired publication only: source remains for historical context and the
      // migration map. Durable knowledge lives in the retained domain/guides.
      exclude: [
        'development/BUILD.md', 'development/DEVELOPMENT.md',
        'reference/recovery.md',
        'registry/current-validation.md', 'registry/pedal-validation.md',
        'registry/pedal-profiles.md', 'registry/pedal-closure.md',
        'registry/virtual-pedals.md', 'registry/handbrake.md',
        'registry/virtual-handbrake.md',
        'steering.md', 'synthetic.md', 'pedals.md', 'pedal-join-contract.md',
        'pedal-profiles.md', 'transmission.md', 'transmission-reverse-v1.md',
        'virtual-transmission-v1-boundary.md',
        'checkpoint1.md', 'checkpoint2.md', 'presentation.md', 'unknowns.md',
        'history/legacy/README.md',
        'history/legacy/resolution-workflow/README.md'
      ]
    },
    blog: false
  }]],
  themeConfig: {
    navbar: {title: 'GT3 Recomp', items: [{to: '/docs/intro', label: 'Knowledge base', position: 'left'}, {to: '/docs/testing', label: 'Evidence and limits', position: 'left'}]},
    footer: {style: 'dark', copyright: 'Source-only selective decompilation. No game assets are distributed. Not affiliated with Sony or Polyphony Digital.'},
    mermaid: {theme: {light: 'neutral', dark: 'dark'}}
  }
};
