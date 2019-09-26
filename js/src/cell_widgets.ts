//import { TextView, ComboboxView, TextareaView } from '@jupyter-widgets/controls';
import { TextView, TextareaView } from '@jupyter-widgets/controls';

export
class TextWithTooltipView extends TextView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};

/*
export
class ComboboxWithTooltipView extends ComboboxView {
    render() {
        super.render();
        this.update_title();
        //this.model.on('change:description_tooltip', this.update_title, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};*/

export
class TextareaWithTooltipView extends TextareaView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};
