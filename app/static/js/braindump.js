$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function checkUncheck (checkbox) {
  // body...
  var property;
  if ($(checkbox).is(':checked') == false){
    $(checkbox).removeAttr("checked");
    property = "uncheck";
  }
  else{
    $(checkbox).attr("checked","");
    property="check";
  }
  
  var notediv = $(checkbox).parents(".tab-pane");

  var note_id = ($(notediv).attr('id'));// note id
  var todo_item = ($(checkbox).parent().text()); // todo item text
  var content_div = $(checkbox).parents(".note-content"); 
  var body_html = content_div.html();// body_html of the note
  var todo_item_id = $(checkbox).parent().attr("id");
  console.log("id is "+ todo_item_id);
  $.ajax({
    url: "/checkuncheck/",
    cache: false,
    type: "POST",
    data: {note_id : note_id, property: property, body_html: body_html, todo_item: todo_item,todo_item_id:todo_item_id},
    success: function(result){
      console.log(result);
    },
    error: function(result){
      console.log(result);
    }
  });
}


