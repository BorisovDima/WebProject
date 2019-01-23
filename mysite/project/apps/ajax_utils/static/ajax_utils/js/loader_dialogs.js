var since = ''
var type = ''
var inProgress = true


$('[data-action="load-modal-notifications"]').click(function(){
     type = $(this).data('type')
    $('#list-dialogs-notify-body').html('')
    $('#modal-notify-window').modal('show')
    if (type == 'notify'){
        $('#counter-notify').html('')
    }
    $.ajax({
        url: '/api/load/' + type + '/',
        method: 'GET',
        success: function(data) {
          $('#list-dialogs-notify-body').append(data.html)
          since = data.since
          if (data.button) {
                $('#button-dialogs-notify-action').show()
                inProgress = false
           }
        }
    })
})

$('#button-dialogs-notify-action').on('click', function(){
    if (!inProgress) {
        $.ajax({
            url: '/api/load/' + type + '/',
            method: 'GET',
            data: {'since': since},
            success: function(data) {
                   $('#list-dialogs-notify-body').append(data.html)
                    since = data.since
                    if (!data.button) {
                        $('#button-dialogs-notify-action').hide()
                     }
            }
        })
    }
})




