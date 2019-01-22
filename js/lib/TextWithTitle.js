var widgets = require('@jupyter-widgets/base');
var widgetsc = require('@jupyter-widgets/controls');
var _ = require('lodash');

var TextWithTitleModel = widgetsc.TextModel.extend({
    defaults: _.extend(widgets.TextModel.prototype.defaults(), {
        _model_name : 'TextWithTitleModel',
        _view_name : 'TextWithTitleView',
        _model_module : 'sage-combinat-widgets',
        _view_module : 'sage-combinat-widgets',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        title: 'This is a tooltip',
        value : 'Text With Title'
    })
});

var TextWithTitleView = widgets.TextView.extend({
    render: function() {
        widgets.TextView.prototype.render.call(this);
        this.textbox.title = 'ok';
    },
});


// Custom View. Renders the widget model.
/*var TextWithTitleView = widgets.TextView.extend({
    render: function() {
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get('value');
    }
});*/


module.exports = {
    TextWithTitleModel : TextWithTitleModel,
    TextWithTitleView : TextWithTitleView
};
