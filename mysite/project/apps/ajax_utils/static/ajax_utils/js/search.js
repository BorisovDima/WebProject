$(document).ready(function(){
    // жду когда загрузится DOM. потом сразу же собираю инфу из селекторов и отправляют ajax запрос
    // с текущим 'obj_id' (может быть категория, пост или None).
    var inProgress = true
    var since = ''
    var location = $('#search-ajax').val() +'-search'
    var search = ''
        $("#search-form-ajax-btn").click(function() {
                search = $('#search-form-ajax').val()
                console.log('dadadadada')
                if (search.length > 0) {
                    $('#search-form-ajax').val('')
                     $("html, body").scrollTop(0, 0)
                    $(window).unbind('scroll')

                    $.ajax({
                        url: '/api/load/' + location + '/',
                        data: {'search': search},
                    }).success(function(data) {
                         if (data.status == 'ok') {
                            $('#add-loader').html(data.html)
                            since = data.since
                            inProgress = false
                            $(window).bind('scroll', serch_loader)
                        }
                        else {
                            $('#add-loader').html('<h1> Nothing </h1>')

                        }
    })          }
})


    function serch_loader()  {

        //  Жду пока scroll достигнет Button-200 и выполнится первый ajax запрос, чтобы поставить
        // inProgress в false
        if ((($(window).height() + $(window).scrollTop()) > ($(document).height() - 200)) && !inProgress){
                 $.ajax({
                    url: '/api/load/' + location  + '/',
                    method: 'GET',
                    data: {'since': since, 'search': search}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
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