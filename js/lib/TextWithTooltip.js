var widgets = require('@jupyter-widgets/base');
var widgets = require('@jupyter-widgets/controls');
var _ = require('lodash');

var TextWithTooltipView = widgets.TextView.extend({
    render: function() {
        widgets.TextView.prototype.render.call(this);
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    },
    update_title: function() {
        this.textbox.title = this.model.get('description_tooltip');
    }
});

module.exports = {
    TextWithTooltipView : TextWithTooltipView
};
