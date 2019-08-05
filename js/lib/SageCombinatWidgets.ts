import StyleModel from '@jupyter-widgets/base';
import TextView from '@jupyter-widgets/controls';

export
class CellStyleModel extends StyleModel {
    defaults() {
        return {...super.defaults(),
            _model_name: 'CellStyleModel',
            _model_module: '@jupyter-widgets/controls',
            _model_module_version: JUPYTER_CONTROLS_VERSION,
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

/*export
class TextWithTooltipView extends TextView {
    render() {
        widgets.TextView.prototype.render.call(this);
        this.update_title();
        this.model.on('change:description_tooltip', this.update_title, this);
    },
    update_title() {
        this.textbox.title = this.model.get('description_tooltip');
    }
};
}*/

