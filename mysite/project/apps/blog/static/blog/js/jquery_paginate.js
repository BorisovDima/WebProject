$(document).ready(function(){
    // жду когда загрузится DOM. потом сразу же собираю инфу из селекторов и отправляют ajax запрос
    // с текущим 'obj_id' (может быть категория, пост или None).

    var inProgress = true
    var obj_id = $('#obj_loader').val()
    var since = ''
    var location = $('#loader').attr('value')

    $.ajax({
        url: '/api/load/' + location + '/',
        method: 'GET',
        data: {'obj_id': obj_id} // 'obj_id' (может быть категория, пост или None).
    }).success(function(data) {
          $('#add-loader').append(data.html) // При 200 ОК append в div c id 'add-loader'.
          since = data.since      // c какого id делать выборку
          inProgress = false     //( для условия && !inProgress)
    })

    $(window).bind('scroll', function() {

        //  Жду пока scroll достигнет Button-200 и выполнится первый ajax запрос, чтобы поставить
        // inProgress в false

        if ((($(window).height() + $(window).scrollTop()) > ($(document).height() - 200)) && !inProgress){
                 $.ajax({
                    url: '/api/load/' + location + '/',
                    method: 'GET',
                    data: {'since': since, 'obj_id': obj_id}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
                    beforeSend: function() {
                        inProgress = true // что бы больше не один scroll не вызвал ajax до завершения этого
                    },
                    complete: function() {
                        inProgress = false // теперь может вызываться следующий ajax
                    }
                 }).success(function(data) {
                        if (data.status == 'ok') {           // при 'ok' продолжаю
                            $('#add-loader').append(data.html)
                            since = data.since
                        }
                        else {
                            $(window).unbind('scroll')       // любой другой статус - отвязываю обработник scroll
                        }

                 }).error(function(data) {
                        console.log('error')

                 })
        }
    })

})

