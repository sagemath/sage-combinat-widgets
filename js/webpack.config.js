var path = require('path');
var version = require('./package.json').version;

const rules = [
    { test: /\.ts$/, loader: 'ts-loader' },
    { test: /\.js$/, loader: 'source-map-loader' },
    { test: /\.css$/, use: ['style-loader', 'css-loader']},
    { test: /\.(jpg|png|gif)$/, use: ['url-loader']}
];
// Packages that shouldn't be bundled but loaded at runtime
const externals = ['@jupyter-widgets/base', '@jupyter-widgets/controls'];
const resolve = {
  extensions: [".webpack.js", ".web.js", ".ts", ".js"]
};

module.exports = [
  /**
   * Notebook extension
   *
   * This bundle only contains the part of the JavaScript that is run on load of
   * the notebook.
   */
    {
	mode: 'development',
	entry: './src/extension.ts',
	output: {
	    filename: 'index.js',
            path: path.resolve(__dirname, '..', 'sage_combinat_widgets', 'nbextension', 'static'),
            libraryTarget: 'amd'
	},
	module: {
	    rules: rules
	},
	devtool: 'source-map',
	externals,
	resolve,
    }//,

/*    {
	mode: 'development',
	entry: './src/index.ts',
	output: {
	    filename: 'index.js',
            path: path.resolve(__dirname, '..', 'sage_combinat_widgets', 'nbextension', 'static'),
            libraryTarget: 'amd'
	},
	module: {
	    rules: rules
	},
	devtool: 'source-map',
	externals,
	resolve,
    } */
];
