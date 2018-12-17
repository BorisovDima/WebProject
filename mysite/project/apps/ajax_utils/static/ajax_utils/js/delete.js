$(document).on('click', '[data-action="delete_object"]', function() {
    type = $(this).data('type')
    id = $(this).data('id')
    console.log(type, id)
    $.ajax({
        url: '/api/' + type +  '/delete/' + id + '/',
        method: 'POST',
    }).success( function(data) {
        if (data.status == 'ok') {
            if (data.event == 'comment'){
                $('#comment-' + id).html(data.html)
                $('#comment-' + id).on('click', '[data-action="return_object"]', comeback)
            }
            else {
                $('#wrapper_post-' + id).html(data.html)
                $('#wrapper_post-' + id).on('click', '[data-action="return_object"]', comeback)
            }
        }
        else {
            console.log('INVALID')
        }
    })
})


function comeback() {
    type = $(this).data('type')
    id = $(this).data('id')
    console.log(type, id)
    $.ajax({
        url: '/api/' + type +  '/return/' + id + '/',
        method: 'POST',
    }).success( function(data) {
          if (data.status == 'ok') {
            if (data.event == 'comment'){
                $('#comment-' + id).replaceWith(data.html)
            }
            else {
                $('#wrapper_post-' + id).replaceWith(data.html)
            }
        }
        else {
            console.log('INVALID')
        }
    })
}





