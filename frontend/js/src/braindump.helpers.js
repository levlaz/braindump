(function(window) {
    /**
     * Braindump helpers module
     *
     * Helper functions for other modules
     *
     * @module braindump.helpers
     */
    'use strict';

    /**
     * Wrapper for addEventListener assuming the target exists
     */
    window.$on = function (target, type, callback, useCapture) {
        if (!!target) {
            target.addEventListener(type, callback, !!useCapture)
        }
    };
})(window);