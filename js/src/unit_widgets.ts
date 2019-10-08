import { ComboboxModel, ComboboxView,
       DropdownModel, DropdownView,
       TextModel, TextView,
       TextareaModel, TextareaView,
       ToggleButtonModel, ToggleButtonView } from '@jupyter-widgets/controls';
import { MODULE_NAME, MODULE_VERSION } from './version';

export
class ComboboxUnitModel extends ComboboxModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'ComboboxUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'ComboboxUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class DropdownUnitModel extends DropdownModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'DropdownUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'DropdownUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

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
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class TextareaUnitModel extends TextareaModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'TextareaUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'TextareaUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class ToggleButtonUnitModel extends ToggleButtonModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'ToggleButtonUnitModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'ToggleButtonUnitView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class ComboboxUnitView extends ComboboxView {
    render() {
        super.render();
        this.update_tabindex();
        this.update_tooltip();
        this.update_title();
        this.update_focus();
        this.model.on('change:tabindex', this.update_tabindex, this);
        this.model.on('change:_tooltip', this.update_title, this);
        this.model.on('change:description_tooltip', this.update_tooltip, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_tabindex() {
        let tabindex = this.model.get('tabindex')
        if (tabindex) this.textbox.setAttribute('tabindex', tabindex);
	else this.textbox.removeAttribute('tabindex');
    }

    update_tooltip() {
	this.model.set('_tooltip', this.model.get('description_tooltip'));
    }

    update_title() {
        let title = this.model.get('_tooltip');
        if (title) this.textbox.setAttribute('title', title);
	else this.textbox.removeAttribute('title');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.textbox.focus(); }
	else if (focus == 'off') { this.textbox.blur(); }
    }
};

export
class DropdownUnitView extends DropdownView {
    render() {
        super.render();
        this.update_tabindex();
        this.update_tooltip();
        this.update_title();
        this.update_focus();
        this.model.on('change:tabindex', this.update_tabindex, this);
        this.model.on('change:_tooltip', this.update_title, this);
        this.model.on('change:description_tooltip', this.update_tooltip, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_tabindex() {
        let tabindex = this.model.get('tabindex')
        if (tabindex) this.listbox.setAttribute('tabindex', tabindex);
	else this.listbox.removeAttribute('tabindex');
    }

    update_tooltip() {
	this.model.set('_tooltip', this.model.get('description_tooltip'));
    }

    update_title() {
        var title = this.model.get('description_tooltip');
        if (!title) this.listbox.removeAttribute('title');
	else this.listbox.setAttribute('title', title);
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.listbox.focus(); }
	else if (focus == 'off') { this.listbox.blur(); }
    }
};

export
class TextUnitView extends TextView {
    render() {
        super.render();
        this.update_tabindex();
        this.update_tooltip();
        this.update_title();
        this.update_focus();
        this.model.on('change:tabindex', this.update_tabindex, this);
        this.model.on('change:_tooltip', this.update_title, this);
        this.model.on('change:description_tooltip', this.update_tooltip, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_tabindex() {
        let tabindex = this.model.get('tabindex')
        if (tabindex) this.textbox.setAttribute('tabindex', tabindex);
	else this.textbox.removeAttribute('tabindex');
    }

    update_tooltip() {
	this.model.set('_tooltip', this.model.get('description_tooltip'));
    }

    update_title() {
        let title = this.model.get('_tooltip');
        if (title) this.textbox.setAttribute('title', title);
	else this.textbox.removeAttribute('title');
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
        this.update_tabindex();
        this.update_tooltip();
        this.update_title();
        this.update_focus();
        this.model.on('change:tabindex', this.update_tabindex, this);
        this.model.on('change:_tooltip', this.update_title, this);
        this.model.on('change:description_tooltip', this.update_tooltip, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_tabindex() {
        let tabindex = this.model.get('tabindex')
        if (tabindex) this.textbox.setAttribute('tabindex', tabindex);
	else this.textbox.removeAttribute('tabindex');
    }

    update_tooltip() {
	this.model.set('_tooltip', this.model.get('description_tooltip'));
    }

    update_title() {
        let title = this.model.get('_tooltip');
        if (title) this.textbox.setAttribute('title', title);
	else this.textbox.removeAttribute('title');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.textbox.focus(); }
	else if (focus == 'off') { this.textbox.blur(); }
    }
};

export
class ToggleButtonUnitView extends ToggleButtonView {
    render() {
        super.render();
        this.update_tabindex();
        this.update_tooltip();
        this.update_title();
        this.update_focus();
        this.model.on('change:tabindex', this.update_tabindex, this);
        this.model.on('change:_tooltip', this.update_title, this);
        this.model.on('change:tooltip', this.update_tooltip, this);
        this.model.on('change:description_tooltip', this.update_tooltip, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_tabindex() {
        let tabindex = this.model.get('tabindex')
        if (tabindex) this.el.setAttribute('tabindex', tabindex);
	else this.el.removeAttribute('tabindex');
    }

    update_tooltip() {
        if (this.model.get('tooltip')) this.model.set('_tooltip', this.model.get('description_tooltip'));
	else this.model.set('_tooltip', this.model.get('description_tooltip'));
    }

    update_title() {
        let title = this.model.get('_tooltip');
        if (title) this.el.setAttribute('title', title);
	else this.el.removeAttribute('title');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.el.focus(); }
	else if (focus == 'off') { this.el.blur(); }
    }
};
