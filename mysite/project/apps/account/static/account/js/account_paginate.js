$(document).ready(function(){
    // жду когда загрузится DOM. потом сразу же собираю инфу из селекторов и отправляют ajax запрос
    // с текущим 'obj_id' (может быть категория, пост или None).

    var inProgress = true
    var since = ''
    var start_location = $('#location').val()
    start_loder()


    $('[data-action="profile-paginate"]').click(function(){
        inProgress = true
        since = ''
        var event = $(this)
        $('[data-action="profile-paginate"]').removeClass('active')
        event.addClass('active')
        var type = event.data('type')
        if (type) {
            path = start_location + '/' + type
           }
        else {
            path = start_location
        }
        $('#location').val(path)
        $('#add-loader').html('')
        start_loder()
    })



    function start_loder() {
        var location = $('#location').val()
        $.ajax({
            url: '/api/load/' + location + '/',
            method: 'GET'
        }).success(function(data) {
            $('#add-loader').append(data.html) // При 200 ОК append в div c id 'add-loader'.
            since = data.since      // c какого id делать выборку
            inProgress = false     //( для условия && !inProgress)
        })
    }

    $(window).bind('scroll', loader)
    function loader() {
        //  Жду пока scroll достигнет Button-200 и выполнится первый ajax запрос, чтобы поставить
        // inProgress в false

        if ((($(window).height() + $(window).scrollTop()) > ($(document).height() - 200)) && !inProgress){
                 var location = $('#location').val()
                 $.ajax({
                    url: '/api/load/' + location + '/',
                    method: 'GET',
                    data: {'since': since}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
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
    }


})
