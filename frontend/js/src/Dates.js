'use strict';

const moment = require('moment');

let self = module.exports = {

        initDates: function() {
                self.setListUpdatedDates();
                self.setUpdatedDates();
                self.setCreatedDates();
        },

        setListUpdatedDates: function() {
                let dateListField = $(".note-updated-date-list");

                dateListField.each(function() {
                        let updatedDate = this.getAttribute('value');
                        this.innerHTML = moment.utc(updatedDate).local().fromNow();
                });
        },

        setUpdatedDates: function() {
                let dateField = $(".note-updated-date");

                dateField.each(function() {
                        let updatedDate = this.getAttribute('value');
                        this.innerHTML = `Updated on: ${moment.utc(updatedDate).local().format('MMMM DD, YYYY h:mm a zz')}`;
                });
        },

        setCreatedDates: function() {
                let dateField = $(".note-created-date");

                dateField.each(function() {
                        let createdDate = this.getAttribute('value');
                        this.innerHTML = `Created on: ${moment.utc(createdDate).local().format('MMMM DD, YYYY h:mm a zz')}`;
                })
        }
}
