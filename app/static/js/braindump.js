// Ace Editor Loading
var editor = ace.edit("editor");
editor.setTheme("ace/theme/tomorrow");
editor.session.setMode("ace/mode/markdown");
editor.getSession().setUseWrapMode(true);
editor.setAutoScrollEditorIntoView(true);
editor.setOption("minLines", 10);
editor.setOption("maxLines", 100);

var textarea = $('textarea[id="body"]').hide();
var textarea_html_label = $('label[for="body_html"]').hide();
var textarea_html = $('textarea[id="body_html"]').hide();
editor.getSession().setValue(textarea.val());
editor.getSession().on('change', function(){
  textarea_html.val(marked(editor.getSession().getValue()));
  textarea.val(editor.getSession().getValue());
});

// Hot Keys
editor.commands.addCommand({
    name: 'insert text',
    bindKey: {win: 'Ctrl-1',  mac: 'Ctrl-1'},
    exec: function(editor) {
        editor.insert("*TODO ")
    },
    readOnly: true // false if this command should not apply in readOnly mode
});

editor.commands.addCommand({
    name: 'Insert TimeStamp',
    bindKey: {win: 'Ctrl-d',  mac: 'Ctrl-d'},
    exec: function(editor) {
        editor.insert(moment().format('MMMM Do YYYY, h:mm:ss a') + "\n");
    },
    readOnly: true // false if this command should not apply in readOnly mode
});
