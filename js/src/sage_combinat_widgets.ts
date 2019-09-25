import { StyleModel } from '@jupyter-widgets/base';
import { TextView } from '@jupyter-widgets/controls';
import { MODULE_NAME, MODULE_VERSION } from './index';

//export
//const MODULE_VERSION = (require('../package.json') as any).version;

export
class CellStyleModel extends StyleModel {
    defaults() {
        return {...super.defaults(),
            _model_name: 'CellStyleModel',
            _model_module: MODULE_NAME,
            _model_module_version: MODULE_VERSION,
        };
    }

    public static styleProperties = {
        color: {
            selector: '',
            attribute: 'color',
            default: null as any
        },
        background_color: {
            selector: '',
            attribute: 'background-color',
            default: null as any
        },
        background_image: {
            selector: '',
            attribute: 'background-image',
            default: ''
        },
        background_position: {
            selector: '',
            attribute: 'background-position',
            default: ''
        },
        background_repeat: {
            selector: '',
            attribute: 'background-repeat',
            default: ''
        },
        background_size: {
            selector: '',
            attribute: 'background-size',
            default: ''
        },
        background: {
            selector: '',
            attribute: 'background',
            default: ''
        },
    };
}

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
