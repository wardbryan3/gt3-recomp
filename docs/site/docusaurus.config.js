module.exports = {
  title: 'GT3 Recomp',
  tagline: 'Recover first. Modify second.',
  url: 'http://localhost:3000',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {format: 'detect', mermaid: true, hooks: {onBrokenMarkdownLinks: 'throw'}},
  themes: ['@docusaurus/theme-mermaid'],
  presets: [['classic', {
    docs: {sidebarPath: require.resolve('./sidebars.js'), routeBasePath: 'docs'},
    blog: false
  }]],
  themeConfig: {
    navbar: {title: 'GT3 Recomp', items: [{to: '/docs/intro', label: 'Knowledge base', position: 'left'}, {to: '/docs/queue', label: 'Next cycles', position: 'left'}]},
    footer: {style: 'dark', copyright: 'Source-only selective decompilation. No game assets are distributed. Not affiliated with Sony or Polyphony Digital.'},
    mermaid: {theme: {light: 'neutral', dark: 'dark'}}
  }
};
