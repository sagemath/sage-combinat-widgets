var widgets = require('@jupyter-widgets/base');
var widgets = require('@jupyter-widgets/controls');
var _ = require('lodash');

var TextWithTooltipModel = widgets.TextModel.extend({
    defaults: _.extend(widgets.TextModel.prototype.defaults(), {
        _model_name : 'TextWithTooltipModel',
        _view_name : 'TextWithTooltipView',
        _model_module : 'sage-combinat-widgets',
        _view_module : 'sage-combinat-widgets',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        tooltip: 'This is a tooltip',
        value : 'Text With Tooltip'
    })
});

var TextWithTooltipView = widgets.TextView.extend({
    render: function() {
        widgets.TextView.prototype.render.call(this);
        this.tooltip_changed();
        this.model.on('change:tooltip', this.tooltip_changed, this);
    },
    tooltip_changed: function() {
        this.textbox.title = this.model.get('tooltip');
    }
});

module.exports = {
    TextWithTooltipModel : TextWithTooltipModel,
    TextWithTooltipView : TextWithTooltipView
};
