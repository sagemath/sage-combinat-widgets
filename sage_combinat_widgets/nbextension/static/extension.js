// Entry point for the notebook bundle containing custom model definitions.
//
define(function() {
    "use strict";

    window['requirejs'].config({
        map: {
            '*': {
                'sage-combinat-widgets': 'nbextensions/sage-combinat-widgets/index',
            },
        }
    });

    // Export the required load_ipython_extension function
    return {
        load_ipython_extension : function() {}
    };
});
