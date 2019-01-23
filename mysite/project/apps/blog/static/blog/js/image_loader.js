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
     $('#navbar-create_post_form').val('')
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

$('#send-form-post').on('click', function() {
    var img = $('#image-post-input').prop('files')[0];
    var text = $("textarea[id='navbar-create_post_form']").val();
    var formData = new FormData();
    formData.append("text", text);
    formData.append("image", img);
    formData.append("path", window.location.pathname);
    $('#send-form-post').hide()
    $.ajax({
        url: '/create-post/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.add) {
                $('#add-loader').prepend(data.post)
            }
            $('#content-creation-post').hide()
            $('#post-create-success').html(data.html)
            setTimeout(function () {
                $('#Create-post').modal('hide')
               $('#post-create-success').html('')
                $('#content-creation-post').show()
            }, 1500);
            close_file_choice()
       },
        error: function(data) {
            if (data.status == 400) {
                errors = JSON.parse(data.responseText)
                $("#post-create-error-img").text(errors['image'] || '')
                $("#post-create-error-text").text(errors['text'] || '')
                setTimeout(function () {
                    $("#post-create-error-img").text('')
                    $("#post-create-error-text").text('')
                    }, 2000);
                close_file_choice()
            }
        },
    })

})

