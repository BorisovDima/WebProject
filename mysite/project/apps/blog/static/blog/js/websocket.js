

var Socket = new WebSocket('ws://' + window.location.host + window.location.pathname + 'add-comment/');

Socket.onmessage = function(event) {

    var data = JSON.parse(event.data);
    var comment = data['comment']
    $('#comments-list').prepend(comment)
    $('#id_text').val('')

}


Socket.onclose = function(event) {
    console.error('WebSocket close');
}

Socket.onerror = function(error) {


}


$('#comment-submit').click(function() {
    var text = $("#id_text").val()
    var parent = $("#id_parent").val()

    if (!text) {
        return false
    }
    Socket.send(JSON.stringify({'text': text, 'parent': parent}))
})



