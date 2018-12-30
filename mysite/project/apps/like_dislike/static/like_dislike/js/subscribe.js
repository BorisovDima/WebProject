var ready = true

$(document).on('click', '[data-action="user-subscribe"]', function() {
   var subscribe = $(this)
   var type = subscribe.data('type')
   var id = subscribe.data('id')
    if (ready) {
    $.ajax({
        url: '/api/subscribe/' + type + '/' + id + '/',
        method: 'POST',
        beforeSend: function() {
                ready = false // что бы больше не один scroll не вызвал ajax до завершения этого
        },
        complete: function() {
                ready = true // теперь может вызываться следующий ajax
        },
        success: function(data) {
                if (data.add == true) {
                    subscribe.removeClass( "btn-danger" ).addClass( "btn-success" );
                    subscribe.text('Unsubscribe')
                    $('#count-followers').text(data.count)
            }
            else {
                    subscribe.removeClass( "btn-success" ).addClass( "btn-danger" );
                    subscribe.text('Subscribe')
                    $('#count-followers').text(data.count)
             }
         },
    })
    }
});