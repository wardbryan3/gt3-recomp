const {excluded} = require('./doc-routes');
module.exports = {
  title: 'GT3 Recomp',
  tagline: 'Recover first. Modify second.',
  url: 'http://localhost:3100',
  baseUrl: '/',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {format: 'detect', mermaid: true, hooks: {onBrokenMarkdownLinks: 'throw'}},
  themes: ['@docusaurus/theme-mermaid'],
  plugins: [require.resolve('./plugins/doc-redirects')],
  presets: [['classic', {
    docs: {
      sidebarPath: require.resolve('./sidebars.js'),
      routeBasePath: 'docs',
      // No additional exclusions: retained summaries remain source files. The
      // stopped profile, Reverse and extension-boundary reports are now published.
      exclude: excluded
    },
    blog: false
  }]],
  themeConfig: {
    navbar: {title: 'GT3 Recomp', items: [
      {to: '/docs/start-here', label: 'Start Here', position: 'left'},
      {to: '/docs/developer-guide', label: 'Developer Guide', position: 'left'},
      {to: '/docs/architecture', label: 'Architecture', position: 'left'},
      {to: '/docs/reference', label: 'Reference', position: 'left'},
      {to: '/docs/research', label: 'Research & Evidence', position: 'left'}
    ]},
    footer: {style: 'dark', copyright: 'Source-only selective decompilation. No game assets are distributed. Not affiliated with Sony or Polyphony Digital.'},
    mermaid: {theme: {light: 'neutral', dark: 'dark'}}
  }
};
