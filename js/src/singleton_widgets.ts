import { ButtonModel,  ButtonView,
       ComboboxModel, ComboboxView,
       DropdownModel, DropdownView,
       HTMLModel, HTMLView,
       HTMLMathModel, HTMLMathView,
       TextModel, TextView,
       TextareaModel, TextareaView,
       ToggleButtonModel, ToggleButtonView } from '@jupyter-widgets/controls';
import { MODULE_NAME, MODULE_VERSION } from './version';

export
class ButtonSingletonModel extends ButtonModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'ButtonSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'ButtonSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class ComboboxSingletonModel extends ComboboxModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'ComboboxSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'ComboboxSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class DropdownSingletonModel extends DropdownModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'DropdownSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'DropdownSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class HTMLSingletonModel extends HTMLModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'HTMLSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'HTMLSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class HTMLMathSingletonModel extends HTMLMathModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'HTMLMathSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'HTMLMathSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class TextSingletonModel extends TextModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'TextSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'TextSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class TextareaSingletonModel extends TextareaModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'TextareaSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'TextareaSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class ToggleButtonSingletonModel extends ToggleButtonModel {
    defaults() {
        return {...super.defaults(),
	_model_name: 'ToggleButtonSingletonModel',
	_model_module: MODULE_NAME,
	_model_module_version: MODULE_VERSION,
	_view_name: 'ToggleButtonSingletonView',
	_view_module: MODULE_NAME,
	_view_module_version: MODULE_VERSION,
        _focus: null,
	_tooltip: null,
	tabindex: null,
        };
    }
}

export
class ButtonSingletonView extends ButtonView {
    render() {
        super.render();
        this.update_tabindex();
        this.update_tooltip();
        this.update_title();
        this.update_focus();
        this.model.on('change:tabindex', this.update_tabindex, this);
        this.model.on('change:_tooltip', this.update_title, this);
        this.model.on('change:tooltip', this.update_tooltip, this);
        this.model.on('change:_focus', this.update_focus, this);
    }

    update_tabindex() {
        let tabindex = this.model.get('tabindex')
        if (tabindex) this.el.setAttribute('tabindex', tabindex);
	else this.el.removeAttribute('tabindex');
    }

    update_tooltip() {
        if (this.model.get('tooltip')) this.model.set('_tooltip', this.model.get('tooltip'));
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

export
class ComboboxSingletonView extends ComboboxView {
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
	if (this.model.get('description_tooltip')) {
	    this.model.set('_tooltip', this.model.get('description_tooltip'));
	}
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
class DropdownSingletonView extends DropdownView {
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
	if (this.model.get('description_tooltip')) {
	    this.model.set('_tooltip', this.model.get('description_tooltip'));
	}
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
class HTMLSingletonView extends HTMLView {
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
        if (tabindex) this.content.setAttribute('tabindex', tabindex);
	else this.content.removeAttribute('tabindex');
    }

    update_tooltip() {
	if (this.model.get('description_tooltip')) {
            this.model.set('_tooltip', this.model.get('description_tooltip'));
	}
    }

    update_title() {
        let title = this.model.get('_tooltip');
        if (title) this.content.setAttribute('title', title);
	else this.content.removeAttribute('title');
    }

    update_focus() {
        let focus = this.model.get('_focus');
	if (!focus) return;
	if (focus == 'on') { this.content.focus(); }
	else if (focus == 'off') { this.content.blur(); }
    }
};

export
class HTMLMathSingletonView extends HTMLSingletonView {
    render() {
        super.render();
    }
};

export
class TextSingletonView extends TextView {
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
	if (this.model.get('description_tooltip')) {
	   this.model.set('_tooltip', this.model.get('description_tooltip'));
	}
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
class TextareaSingletonView extends TextareaView {
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
        if (this.model.get('description_tooltip')) {
	    this.model.set('_tooltip', this.model.get('description_tooltip'));
	}
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
class ToggleButtonSingletonView extends ToggleButtonView {
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
        let tabindex = this.model.get('tabindex');
        if (tabindex) this.el.setAttribute('tabindex', tabindex);
	else this.el.removeAttribute('tabindex');
    }

    update_tooltip() {
        if (this.model.get('tooltip')) {
	    this.model.set('_tooltip', this.model.get('tooltip'));
	}
	else if (this.model.get('description_tooltip')) {
	    this.model.set('_tooltip', this.model.get('description_tooltip'));
	}
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
