'use strict';

/*
 * This modules adds helper functions to the notebooks view
 * which allows users to add, edit, and delete notebooks.
 */
let self = module.exports = {

        init: function() {

                let notebooks = $(".notebook-card");

                notebooks.each(function() {
                        let notebook = self.getNotebook(this);
                        let deleteButton = $(this).find('.delete-notebook');
                        deleteButton.on('click', notebook, self.deleteNotebook);
                });
        },

        getNotebook: function(e) {
                let notebookId = e.getAttribute("notebook_id");
                let noteCountString = $(e).find("span").text();
                let noteCount = noteCountString.match(/\d+/)[0];

                let notebook = {
                        self: e,
                        id: notebookId,
                        noteCount: noteCount
                }

                return notebook;
        },

        deleteNotebook: function(e) {
                $.ajax({
                        url: `/notebook/${e.data.id}`,
                        contentType: 'application/json',
                        type: 'DELETE',
                        success: function (response) {
                                e.data.self.remove();
                                console.log(response);
                        },
                        error: function (error) {
                                console.log(error);
                        }
                });
        }
}
