// Ace Editor Loading
var editor = ace.edit("editor");
editor.setTheme("ace/theme/tomorrow");
editor.session.setMode("ace/mode/markdown");
editor.getSession().setUseWrapMode(true);
editor.setAutoScrollEditorIntoView(true);
editor.setOption("minLines", 10);
editor.setOption("maxLines", 100);

var textarea = $('textarea[id="body"]').hide();
editor.getSession().setValue(textarea.val());
editor.getSession().on('change', function(){
  textarea.val(marked(editor.getSession().getValue()));
});
