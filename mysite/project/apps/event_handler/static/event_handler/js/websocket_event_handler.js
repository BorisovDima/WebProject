

function close_modal() {
    $('#wrapper-show-message').hide(100)
}



var event_choice = $('#message-window-n').val()

var Socket = new WebSocket('ws://' + window.location.host + '/ws/event-handler/');
//alert($('#wrapper-dialog').length)

Socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var event = data['event']
    var locate = data['dialog']
    if (Number(locate) != Number($('#message-dispatch').val())) {
        if (event == 'message') {

            var count = Number($('#counter-message').text())
            var new_count = count + 1
            $('#counter-message').text(new_count)

            var html = data['html']
            if (event_choice == window.location.pathname) {

                    var wrapper = '#wrapper-dialog' + locate
                    if ($(wrapper).length) {
                        $(wrapper).html(html)
                     }
                    else {
                    var new_html = '<div id="' + wrapper + '">' + html + '</div>'
                        $('#All-dialogs').append(new_html)
                    }
            }
            else  {
                $('#show-message').html(html)
                $('#wrapper-show-message').show(100)
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





