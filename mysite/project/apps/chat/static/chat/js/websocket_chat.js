$(document).ready(function(){
        $('body, html').scrollTop($(document).height())

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
    Socket.send(JSON.stringify({'text': "TEST"}))
    console.error('WebSocket close');
}

Socket.onerror = function(error) {


}

$('#send-message').click(function() {
    var text = $("#id_text_dialog").val()
    if (!text) {
        return false
    }
    Socket.send(JSON.stringify({'text': text}))
})



