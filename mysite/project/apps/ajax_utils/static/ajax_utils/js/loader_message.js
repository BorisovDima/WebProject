var since = ''
var inProgress = true
var dialog = $("#message-list").data('id')


$(document).ready(function(){
    $.ajax({
        url: '/api/load/message/user-messages/',
        method: 'GET',
        data: {'f': dialog},
        success: function(data) {
          $('#message-list').prepend(data.html)
          $(window).scrollTop($(document).height())
          since = data.since
          inProgress = false
        }
    })


$('#button-dialogs-loader').on('click', function(){
        if (!inProgress) {
                 $.ajax({
                    url: '/api/load/message/user-messages/',
                    method: 'GET',
                    data: {'f': dialog, 'since': since}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
                    beforeSend: function() {
                        inProgress = true // что бы больше не один scroll не вызвал ajax до завершения этого
                    },
                   success: function(data) {
                        console.log(data.status)
                        if (data.status == 'ok') {           // при 'ok' продолжаю
                            $('#message-list').prepend(data.html)
                            since = data.since
                            inProgress = false
                        }
                        else {
                            $('#button-dialogs-loader').hide()
                            inProgress = true
                        }
                    }

                 })
         }

    })
 })

