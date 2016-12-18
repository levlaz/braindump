(function () {
    'use strict';

    /**
     * Braindump Settings Module
     *
     * Scripts that run on the settings view of the app
     *
     * @module braindump.settings
     */

    var defaultNotebookSelector = document.getElementById('defaultNotebook');

    /**
     * Update default notebook
     *
     * When default notebook selection is changed on the settings page,
     * send a request to update the default notebook for the user.
     */
    function updateDefaultNotebook() {

        var r = new XMLHttpRequest();
        var csrftoken = $('meta[name=csrf-token]').attr('content');
        var data = JSON.stringify({
            'default_notebook': this.value
        });

        r.open('PUT', '/users');

        r.onreadystatechange = function() {
            if (r.readyState != 4 || r.status != 200) return;
            console.log(r.responseText);
        }

        r.setRequestHeader("X-CSRFToken", csrftoken);
        r.setRequestHeader("Content-Type", "application/json");
        r.send(data);
    }

    $on(defaultNotebookSelector, 'change', updateDefaultNotebook);
})();