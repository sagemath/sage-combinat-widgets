import { TextModel, TextView, ComboboxModel, ComboboxView, TextareaModel, TextareaView } from '@jupyter-widgets/controls';
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
        _focus: null,
        };
    }
}

export
class ComboboxUnitModel extends ComboboxModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'TextUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'TextUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
        };
    }
}

export
class TextareaUnitModel extends TextareaModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'TextUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'TextUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
        };
    }
}

export
class TextUnitView extends TextView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.textbox.focus(); }
	else if (focus == 'off') { this.textbox.blur(); }
    }
};

export
class ComboboxUnitView extends ComboboxView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.textbox.focus(); }
	else if (focus == 'off') { this.textbox.blur(); }
    }
};

export
class TextareaUnitView extends TextareaView {
    render() {
        super.render();
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.textbox.focus(); }
	else if (focus == 'off') { this.textbox.blur(); }
    }
};
