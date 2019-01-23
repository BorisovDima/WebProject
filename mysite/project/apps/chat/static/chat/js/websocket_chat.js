$(document).ready(function(){
        autosize($('#id_text_dialog'));
})


var id_dialog = $("#id_dialog").val()
var status = $("#status_dialog").val()
$('#message-dispatch').val(id_dialog)

var Socket = new WebSocket('ws://' + window.location.host + '/ws/dialog/' + id_dialog + '/?status=' + status);


Socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data['status'] == 'ok') {
        var message = data['message']
        $('#message-list').append(message)
        $('#id_text_dialog').val('')
        $("html,body").scrollTop($(document).height())
    }
    else {
        console.log("INVALID")
    }
}


Socket.onclose = function(event) {
    console.error('WebSocket close', event);
}

Socket.onerror = function(error) {
     console.error('WebSocket error ', error);

}

$('#send-message').click(function() {
    var text = $("#id_text_dialog").val()
    if (!text) {
        return false
    }
    Socket.send(JSON.stringify({'text': text}))
})



