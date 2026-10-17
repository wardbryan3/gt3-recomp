// Static old-URL compatibility, with no additional runtime/dependency package.
// Relative Markdown links point directly to the new docs. Redirects preserve
// query strings and section fragments for existing external bookmarks.
const fs = require('node:fs/promises');
const path = require('node:path');
const {redirects} = require('../doc-routes');
module.exports = function docRedirects() {
  return {
    name: 'gt3-doc-redirects',
    async postBuild({outDir}) {
      for (const {from, to} of redirects) {
        const target = path.join(outDir, to, 'index.html');
        await fs.access(target); // Never emit a redirect to an unpublished page.
        const output = path.join(outDir, from, 'index.html');
        try {
          await fs.access(output);
          throw new Error(`Redirect would overwrite a published page: ${from}`);
        } catch (error) {
          if (error.code !== 'ENOENT') throw error;
        }
        await fs.mkdir(path.dirname(output), {recursive: true});
        await fs.writeFile(output, `<!doctype html><html lang="en"><head>
<meta charset="utf-8"><title>Documentation moved</title>
<link rel="canonical" href="${to}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0;url=${to}">
<script>location.replace(${JSON.stringify(to)} + location.search + location.hash);</script>
</head><body><p>This documentation moved to <a href="${to}">${to}</a>.</p></body></html>\n`);
      }
      console.log(`Documentation redirects PASS: ${redirects.length} old routes`);
    }
  };
};
