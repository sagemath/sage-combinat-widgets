import { TextView } from '@jupyter-widgets/controls';

export
class TextWithTooltipView extends TextView {
    /**
     * Called when view is rendered.
     */
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};
