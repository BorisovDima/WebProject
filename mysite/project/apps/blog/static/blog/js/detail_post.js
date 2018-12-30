
$(document).ready(function(){

autosize($('[data-type="data-form"]'));
var path = ''
var since = ''
var Socket = ''
var inProgress = ''

$(document).on('click', '[data-action="detail-post"]', function(){
    var post = $(this)
    inProgress = true
    var body = post.find('[data-type="detail-post-body"]')
    var footer = post.parent().find('[data-type="post-footer-body"]')
    body_c = body.clone()
    body_c.find('[data-type="text-post-body"]').css('font-size', '20px')
    $('#detail-post-container-body').html(body_c)
    $('#footer-post-container-body').html(footer.clone())
    var id = post.data('id')
    path = '/api/post/comments/'  + id + '/'
    Socket = new WebSocket('ws://' + window.location.host + '/ws/post/' + id + '/add-comment/');
    Socket.onopen = function(event) { console.log('Socket Connect!', path)}
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
    $('#detail-post-container').modal('show')
    $.ajax({
        url: '/api/post/' + id + '/view/',
        method: 'POST',
     })
    $.ajax({
        url: path,
        method: 'GET',
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
})

$('#detail-post-container').on('hide.bs.modal', function(){
    $('#container-comments').html('')
    $('#button-comments-loader').hide()
    Socket.onclose = function(event) { console.log('WebSocket close', path) }
    Socket.close()
    history.pushState('', document.title, window.location.pathname);
})

$(document).on('click', '[data-action="comment-send"]', function(e) {
        var event = $(this).parent().find('[data-type="data-form"]')
        var data = event.val()
        var id_parent = $(this).parent().find('input[type="hidden"]').val()
        if (data) {
            console.log(data.length)
            }
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

})