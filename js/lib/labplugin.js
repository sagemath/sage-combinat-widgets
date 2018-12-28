var sage-combinat-widgets = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'sage-combinat-widgets',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'sage-combinat-widgets',
          version: sage-combinat-widgets.version,
          exports: sage-combinat-widgets
      });
  },
  autoStart: true
};

