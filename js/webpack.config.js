var path = require('path');
var version = require('./package.json').version;

var rules = [
    { test: /\.css$/, use: ['style-loader', 'css-loader']},
    { test: /\.(jpg|png|gif)$/, use: ['url-loader']}
]
var externals = ['@jupyter-widgets/base', '@jupyter-widgets/controls']

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
	    filename: 'extension.js',
            path: path.resolve(__dirname, '..', 'sage_combinat_widgets', 'static'),
            libraryTarget: 'amd'
	},
	module: {
	    rules: rules
	},
	devtool: 'none',
	externals,
	resolve,
    },
    
    {
	mode: 'development',
	entry: './src/index.ts',
	output: {
	    filename: 'index.js',
            path: path.resolve(__dirname, '..', 'sage_combinat_widgets', 'static'),
            libraryTarget: 'amd'
	},
	module: {
	    rules: rules
	}
    ];
