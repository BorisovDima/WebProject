

var Socket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname + 'add-comment/');

Socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data['status'] == 'ok'){
        var comment = data['comment']
        $('#comments-list').prepend(comment)
        $('#id_text').val('')
    }

    else if (data['status'] == 'del_post'){
        alert(10)
    }

    else {
        console.log('INVALID')
    }
}


Socket.onclose = function(event) {
    console.error('WebSocket close');
}

Socket.onerror = function(error) {


}


$('#comment-submit').click(function() {
    var text = $("#id_text").val()
    var id_parent = $("#id_parent").val()
    var name_parent = $("#name_parent").val()
    if (!text) {
        return false
    }
    Socket.send(JSON.stringify({'text': text, 'id_parent':id_parent, 'name_parent' : name_parent}))
})



