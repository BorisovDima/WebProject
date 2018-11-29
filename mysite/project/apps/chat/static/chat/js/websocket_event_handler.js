

var list_dialog = $('#message-list').val()
var Socket = new WebSocket('ws://' + window.location.host + '/event-handler/');


Socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var event = data['event']
    var locate = data['dialog']

    if (Number(locate) != Number($('#message-dispatch').val())) {

        if (event == 'message') {

            var count = Number($('#counter-message').text())
            var new_count = count + 1
            $('#counter-message').text(new_count)
        if (list_dialog) {

        }

    }
}
}

Socket.onclose = function(event) {
    console.error('WebSocket close');
}

Socket.onerror = function(error) {
    console.error(error)

}


