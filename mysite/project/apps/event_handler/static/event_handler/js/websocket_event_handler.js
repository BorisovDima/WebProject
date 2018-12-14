

function close_modal() {
    $('#wrapper-show-message').hide(100)
}




var Socket = new WebSocket('ws://' + window.location.host + '/ws/event-handler/');
//alert($('#wrapper-dialog').length)

Socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var event = data['event']
    var locate = data['dialog']
    var html = data['html']
    if (event == 'message') {
        if (Number(locate) != Number($('#message-dispatch').val())) {
            var count = Number($('#counter-message').text())
            var new_count = count + 1
            $('#counter-message').text(new_count)

            $('#show-message').html(html)
            $('#wrapper-show-message').show(100)
         }
            var wrapper = '#wrapper-dialog' + locate
            if ($(wrapper).length) {
                $(wrapper).html(html)
                }
            else if ($('#All-dialogs').length) {
                var new_html = '<div id="' + wrapper + '">' + html + '</div>'
                $('#All-dialogs').prepend(new_html)
                }

    }
}


Socket.onclose = function(event) {
    console.error('WebSocket close');
}

Socket.onerror = function(error) {
    console.error(error)

}





