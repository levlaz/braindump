'use strict';

const moment = require('moment');

let self = module.exports = {

        initDates: function() {
                self.setUpdatedDates();
                self.setCreatedDates();
        },

        setUpdatedDates: function() {
                let dateField = $(".note-updated-date");

                dateField.each(function() {
                        let updatedDate = this.getAttribute('value');
                        this.innerHTML = `Updated at: ${moment(updatedDate).format('MMMM DD, YYYY h:mm a')}`;
                });

                let dateListField = $(".note-updated-date-list");

                dateListField.each(function() {
                        let updatedDate = this.getAttribute('value');
                        this.innerHTML = moment(updatedDate).fromNow();
                });
        },

        setCreatedDates: function() {
                let dateField = $(".note-created-date");

                dateField.each(function() {
                        let createdDate = this.getAttribute('value');
                        this.innerHTML = `Created on: ${moment(createdDate).format('MMMM DD, YYYY')}`;
                })
        }
}
