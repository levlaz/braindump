'use strict';

import {ProseMirror} from "prosemirror/dist/edit"
import "prosemirror/dist/inputrules/autoinput"
import "prosemirror/dist/menu/tooltipmenu"
import "prosemirror/dist/menu/menubar"
import "prosemirror/dist/markdown"
const debounce = require('./lib/debounce');

let self = module.exports = {
    
    initEditor: function() {
        let place = $(".editor");

        place.each(function() {
            self.createEditor(this, this.getAttribute("note_id"));
        });
    },
    
    createEditor: function(place, noteId) {
        var input = "";

        if (typeof place.children[0] !== 'undefined') {
            var input = place.children[0].value;
        }
        
        let noteBody = $('input[id="body"]');
        let pm = window.pm = new ProseMirror({
            place: place,
            autoInput: true,
            doc: input,
            docFormat: "markdown"
        });
        
        self.setMenuStyle(place.getAttribute("menustyle") || "bar");
        
        let menuStyle = document.querySelector("#menustyle")
        if (menuStyle) menuStyle.addEventListener("change", () => setMenuStyle(menuStyle.value))

        pm.on('change', (debounce.debounce(function(event){
            noteBody.val(pm.getContent("markdown"));
            self.saveNote(noteId, noteBody.val());
        }, 500)));
    }, 
    
    setMenuStyle: function(type) {
        if (type == "bar") {
            pm.setOption("menuBar", {float: true})
            pm.setOption("tooltipMenu", false)
        } else {
            pm.setOption("menuBar", false)
            pm.setOption("tooltipMenu", {selectedBlockMenu: true})
        }        
    }, 
    
    saveNote: function(id, content) {
        $.ajax({
            url: `/edit/${id}`,
            data: JSON.stringify({
                'body': content,
            }),
            contentType: 'application/json',
            type: 'PUT',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
    
}