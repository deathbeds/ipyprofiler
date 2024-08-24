/**
 * Apply transformations to `speedscope` distributions for embedding via sandboxed iframe
 * in e.g. JupyterLab.
 *
 * Many of the approaches below will need to be updated each upstream release.
 *
 * - 1.20.0
 *  - add CSS hacks
 *  - replace references to `localStorage` with empty object
 *  - deploy license
 */
// @ts-check
const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');

const speedscope = path.resolve(__dirname, 'node_modules/speedscope');
const release = path.resolve(speedscope, 'dist/release');

// TODO: find a way to automate this.
const STYLE = `
<style>
  ._1n15n57 { display: none; }
</style>
`;

function transform(/** @type {Buffer} */ content, /** @type {string} */ absoluteFrom) {
  let cString;
  if (absoluteFrom.match(/\.html$/)) {
    /**
     * use of `typestyle` makes it difficult to reason about CSS
     */
    console.warn('... replace CSS in', absoluteFrom);
    cString = content
      .toString('utf-8')
      .replace(/<link[^>]+href="http[^"]+"[^>]+>/, STYLE);
    content = Buffer.from(cString, 'utf8');
  } else if (absoluteFrom.match(/speedscope\.[^.]+?\.js$/)) {
    /**
     * referencing `localStorage` inside a well-sandboxed iframe causes myriad
     * issues.
     *
     * @see https://github.com/jlfwong/speedscope/issues/380
     */
    console.warn('... removing localStorage from', absoluteFrom);
    cString = content.toString('utf-8').replace(/window\.localStorage/g, '{}');
    content = Buffer.from(cString, 'utf8');
  }
  return content;
}

module.exports = /** @type { import('webpack').Configuration } */ {
  output: { clean: true },
  devtool: 'source-map',
  module: { rules: [{ test: /\.js$/, use: 'source-map-loader' }] },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: `${release}/*.{js,css,json,html}`,
          to: 'speedscope/[name][ext]',
          toType: 'template',
          transform,
        },
        { from: `${speedscope}/LICENSE`, to: 'speedscope/' },
      ],
    }),
  ],
};
