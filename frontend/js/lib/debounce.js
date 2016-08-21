'use strict';

module.exports = {
    
    debounce: function(fn, delay) {
        let timer = null;
        return function() {
            let context = this, args = arguments;
            clearTimeout(timer);
            timer = setTimeout(function() {
                fn.apply(context, args);
            }, delay);
        };
    }
}