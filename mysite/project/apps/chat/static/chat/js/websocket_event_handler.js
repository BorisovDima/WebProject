


var Socket = new WebSocket('ws://' + window.location.host + '/event-handler/');


Socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var event = data['event']
    if (event == 'message') {

       var count = Number($('#counter-message').text())
       var new_count = count + 1
       Number($('#counter-message').text(new_count))

    }

}


Socket.onclose = function(event) {
    console.error('WebSocket close');
}

Socket.onerror = function(error) {
    console.error(error)

}


