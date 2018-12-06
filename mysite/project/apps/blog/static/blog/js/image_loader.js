function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#image-load-post')
        .attr('src', e.target.result)
      show_submit()
    };

    $('#wrapper-image-load-post').show()
    show_submit()
    reader.readAsDataURL(input.files[0]);

  }
};



$(function() {
    $("textarea[id='navbar-create_post_form']").keyup(function count(){
    number = $("textarea[id='navbar-create_post_form']").val().length;
    $("#count_message").html(+number);
    show_submit()

  });
});

function close_file_choice(input) {
    $('#image-post-input').val('')
    $('#image-load-post')
        .attr('src', '')
     $('#wrapper-image-load-post').hide()
    show_submit()
}


function show_submit() {
    count = $("textarea[id='navbar-create_post_form']").val()
    if (count){
    count = count.length
    }
    img = $('#image-post-input').val()
    if (count > 0 || img) {
        $('#send-form-post').show()
    }
    else {
         $('#send-form-post').hide()
    }
}

