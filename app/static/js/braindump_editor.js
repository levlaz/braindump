// Ace Editor Loading
var editor = ace.edit("editor");
editor.setTheme("ace/theme/tomorrow");
editor.session.setMode("ace/mode/markdown");
editor.getSession().setUseWrapMode(true);
editor.setAutoScrollEditorIntoView(true);
editor.setOption("minLines", 10);
editor.setOption("maxLines", 25);

// marked.js table renderer
var renderer = new marked.Renderer();
renderer.table = function (header, body) {
    return '<table class="table table-bordered"><thead>' + header + '</thead><tbody>' + body + '</tbody></table>';
};
renderer.listitem = function(text, checked) {
  if (checked === undefined) {
    return '<li>' + text + '</li>\n';
  }

  return '<li class="task-list-item">'
    + '<input type="checkbox" class="task-list-item-checkbox" onchange = "checkUncheck(this)"'
    + (checked ? ' checked' : '')
    + '> '
    + text
    + '</li>\n';
};

marked.setOptions({ renderer: renderer });

var textarea = $('textarea[id="body"]').hide();
var textarea_html_label = $('label[for="body_html"]').hide();
var textarea_html = $('textarea[id="body_html"]').hide();
textarea_html.val(marked(textarea.val()));
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
        editor.insert("- [ ] TODO")
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

function showHTML() {
  $('#preview').html(marked(editor.getSession().getValue()));
}

editor.getSession().on('change', showHTML)
