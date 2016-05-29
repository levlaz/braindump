import $ from 'jquery';
import jQuery from 'jquery';
window.$ = $;
window.jQuery = jQuery;

require('bootstrap');
require('bootstrap-tagsinput');

import {ProseMirror} from "prosemirror/dist/edit"
import "prosemirror/dist/inputrules/autoinput"
import "prosemirror/dist/menu/tooltipmenu"
import "prosemirror/dist/menu/menubar"
import "prosemirror/dist/markdown"

let place = document.querySelector("#editor");
let content = document.querySelector("#content")
const noteBody = $('input[id="body"]');
const noteBodyHtml = $('input[id="body_html"]');

let pm = window.pm = new ProseMirror({
  place: place,
  autoInput: true,
  doc: noteBodyHtml.val(),
  docFormat: "html"
});

content.style.display = "none"

setMenuStyle(place.getAttribute("menustyle") || "bar")

function setMenuStyle(type) {
  if (type == "bar") {
    pm.setOption("menuBar", {float: true})
    pm.setOption("tooltipMenu", false)
  } else {
    pm.setOption("menuBar", false)
    pm.setOption("tooltipMenu", {selectedBlockMenu: true})
  }
}

let menuStyle = document.querySelector("#menustyle")
if (menuStyle) menuStyle.addEventListener("change", () => setMenuStyle(menuStyle.value))

pm.on('change', function(){
  noteBody.val(pm.getContent("markdown"));
  noteBodyHtml.val(pm.getContent("html"));
});