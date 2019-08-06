import { StyleModel } from '@jupyter-widgets/base';
import { TextView } from '@jupyter-widgets/controls';

export
const SAGE_COMBINAT_WIDGETS_VERSION = (require('../package.json') as any).version;

export
class CellStyleModel extends StyleModel {
    defaults() {
        return {...super.defaults(),
            _model_name: 'CellStyleModel',
            _model_module: '@jupyter-widgets/controls',
            _model_module_version: SAGE_COMBINAT_WIDGETS_VERSION,
        };
    }

    public static styleProperties = {
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
