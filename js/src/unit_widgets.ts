import { TextModel, TextView, ComboboxView, TextareaView } from '@jupyter-widgets/controls';
import { MODULE_NAME, MODULE_VERSION } from './version';

export
class TextUnitModel extends TextModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'TextUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'TextUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        focuspos: null,
        };
    }
}

export
class TextUnitView extends TextView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
        this.model.on('change:focus', this.update_focus, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }

    update_focus() {
        console.log("HERE");
	this.model.set('value', 'wip', {updated_view: this});
        let focus = this.model.get('focuspos');
	if (!focus) return;
	if (focus == 'on') { this.textbox.focus(); this.model.set('value', 'focused', {updated_view: this}); }
	else if (focus == 'off') { this.textbox.blur(); this.model.set('value', 'blurred', {updated_view: this}); }
    }
};

export
class ComboboxUnitView extends ComboboxView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};

export
class TextareaUnitView extends TextareaView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};
