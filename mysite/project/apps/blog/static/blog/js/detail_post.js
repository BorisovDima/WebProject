
$(document).ready(function(){

autosize($('textarea'));
var path = ''
var since = ''
var Socket = ''
var inProgress = ''
var location = ''


console.log($("input").is('#init-post'))

if ($("input").is('#init-post')) {
    var init_post_id = $('#init-post').data('id')
    show_post(init_post_id)
}




$(document).on('click', '[data-action="detail-post"]', function (event){
    if (event.target.nodeName == 'A') {
        window.location.replace(event.target.href);
        return false
    }
    var id = $(this).data('id')
    show_post(id)

})


function show_post(id) {
    location = $('#location').val()
    inProgress = true
/////////////// post  /////////////////
        $.ajax({
        url: '/api/post/detail-post/'  + id + '/',
        method: 'POST',
        success: function(data) {
            $('#detail-post-container-body').html(data.html)
            window.history.pushState("", document.title, data.url);
        }

    })
/////////////// socket  /////////////////
    path = '/api/load/comment/post-comment/'
    Socket = new WebSocket('ws://' + window.location.host + '/ws/post/' + id + '/add-comment/');
    Socket.onopen = function(event) { console.log('Socket Connect!', 'ws://' + window.location.host + '/ws/post/' + id + '/add-comment/')}
    Socket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        if (data['status'] == 'ok'){
            var comment = data['comment']
            if (data['add'] == 'child') {
                $('#comment-new-' + data['initial']).append(comment)
            }
            else {
                $('#container-comments').prepend(comment)
            }
            $('[data-type="data-form"]').val('')
        }
        else {
            console.log('INVALID')
        }
    }
/////////////// comments  /////////////////
    $('#detail-post-container').modal('show')
    $.ajax({
        url: path,
        method: 'GET',
        data: {'f': id},
        success: function(data) {
            if (data.status == 'ok') {
                $('#container-comments').append(data.html)
                since = data.since
                if (data.button) {
                    inProgress = false
                    $('#button-comments-loader').show()
                }
            }
        }
    })
}



$('#detail-post-container').on('hide.bs.modal', function(){
    $('#container-comments').html('')
    $('#button-comments-loader').hide()
    Socket.onclose = function(event) { console.log('WebSocket close', path) }
    Socket.close()
    history.pushState('', document.title, '/' + $('#location').data('start') + '/');
    $('#detail-post-container-body').html('')
})




$(document).on('click', '[data-action="comment-send"]', function(e) {
        var event = $(this).parent().find('[data-type="data-form"]')
        var data = event.val()
        var id_parent = $(this).parent().find('input[type="hidden"]').val()
        if (data) {
            Socket.send(JSON.stringify({'text': data, 'id_parent':id_parent}))
        }
})


$('#button-comments-loader').on('click', function(){
    if (!inProgress) {
        $.ajax({
            url: path,
            method: 'GET',
            data: {'since': since},
            beforeSend: function() { inProgress = true },
            success: function(data) {
                $('#container-comments').append(data.html)
                since = data.since      // c какого id делать выборку
                inProgress = false
                if (!data.button) {
                    inProgress = true
                    $('#button-comments-loader').hide()
                }
            },
        })
    }
})





////////////////////////////////////////////////////////////////////////////////////


var redactor = false
var del = false
var id_post_update = ''
$(document).on('click', '[data-action="update_object"]', function(){
        del = false
        id_post_update = $(this).data('id')
        $.ajax({
            url: '/update-post/' + id_post_update +'/',
            method: 'GET',
            success: function(data) {
                $('#update-post-container').html(data.html)
                autosize($('#update-post-text'));
                $('#update-modal').modal('show')
                redactor = false
            },
            error: function(data) {
                 if (data.status == 400) {
                    console.log('Invalid')
                 }
            },
       })


 })



    $(document).on('change', '#update_post_input_file', function(e) {
         del = false
         input = $(this)[0]
        if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#user_update_img').attr('src', e.target.result)
        };
        reader.readAsDataURL(input.files[0]);
        $('[data-type="error-update-image"]').text('')
        }
    })

    $(document).on('click', '[data-action="save_update"]', function(e) {
     if (!redactor) {
        redactor = true
        var image = $('#update_post_input_file').prop('files')[0] || ''
        var text = $('#update-post-text').val()
        if (!image && !text) {
            return false
        }
        var formData = new FormData();
        formData.append("image", image);
        formData.append("text", text);
        if (del) {
            formData.append("delete", del);
        }
        $.ajax({
            url: '/update-post/' + id_post_update +'/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            complete: function() {
                redactor = false
             },
            success: function(data) {
                $('#wrapper_post-' + id_post_update).replaceWith(data.html)
                $('#update-modal').modal('hide')

            },
            error: function(data) {
                console.log('INVALID')
                if (data.status == 400) {
                    errors = JSON.parse(data.responseText)
                    $('[data-type="error-update-image"]').text(errors['image'] || '')
                    $('[data-type="error-update-text"]').text(errors['text'] || '')
                }
            }
        })
       }
    })

    $(document).on('click', '[data-action="delete_update_img" ]', function() {
        del = true
        $('#user_update_img').attr('src', '')
        $('#update_post_input_file').val('')
        $('[data-type="error-update-image"]').text('')
    })

})