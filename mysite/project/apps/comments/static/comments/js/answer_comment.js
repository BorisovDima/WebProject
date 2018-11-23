function Answer(id_parent, parent_name) {
      $("html,body").scrollTop($("#form").offset().top - 100)
      $("#id_text").focus()
      $("#id_text").val('')
      $("#id_parent").val(id_parent)
      var html = '<p>Ответить ' + parent_name + '<button onclick="close_comment()" type="button" class="close" aria-label="Close"> <span aria-hidden="true">&times;</span></button></p>'
      $("#answer").html(html)
}
function close_comment() {
      $("#id_parent").val('')
      $("#answer").html('')
}

function scroll_to_parent(parent_id) {
     var location = '#comment-' + parent_id
     $("html,body").scrollTop($(location).offset().top - 100)
}