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

    var initialize = function () {
        // update params with any specified in the server's config file.
        // the "thisextension" value of the Jupyter notebook config's
        // data may be undefined, but that's ok when using JQuery's extend
        $.extend(true, params, Jupyter.notebook.config.thisextension);

        // add our extension's css to the page
        $('<link/>')
            .attr({
                rel: 'stylesheet',
                type: 'text/css',
                href: requirejs.toUrl('./sage-combinat-widgets.css')
            })
            .appendTo('head');
    };

    // Export the required load_ipython_extension function
    return {
        load_ipython_extension : function() {}
    };
});
