var path = require('path');
var version = require('./package.json').version;

var rules = [
    { test: /\.css$/, use: ['style-loader', 'css-loader']},
    { test: /\.(jpg|png|gif)$/, use: ['url-loader']}
]
var externals = ['@jupyter-widgets/base', '@jupyter-widgets/controls']

module.exports = [
    {// Notebook extension
        entry: './lib/extension.js',
        output: {
            filename: 'extension.js',
            path: path.resolve(__dirname, '..', 'sage_combinat_widgets', 'static'),
            libraryTarget: 'amd'
        }
    },
    {// sage-combinat-widgets bundle for the notebook
        entry: './lib/index.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, '..', 'sage_combinat_widgets', 'static'),
            libraryTarget: 'amd'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: externals
    },
    {// embeddable sage-combinat-widgets bundle
        entry: './lib/embed.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, 'dist'),
            libraryTarget: 'amd',
            publicPath: 'https://unpkg.com/sage-combinat-widgets@' + version + '/dist/'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: externals
    }
];
