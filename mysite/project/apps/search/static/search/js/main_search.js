$(document).ready(function(){
    var search_data = $('#search-q').val()
    var inProgress = true
    var since = ''
    var location =  $('#location').val()
    start_loader()

   $("#search-q").on('keypress', function(e) {
        inProgress = true
        if(e.which == 13) {
            var value = $(this).val()
            if (value) {
                search_data = value
                window.history.pushState("", "", window.location.pathname + '?q=' + search_data);
                start_loader()
            }
        }
    })


    $('[data-action="ajax-paginate-btn"]').click(function(){
        inProgress = true
        var event = $(this)
        $('[data-action="ajax-paginate-btn"]').removeClass('my_active')
        event.addClass('my_active')
        var type = event.data('type')
        $('#location').val(type)
        location = type
        start_loader()
    })


    function start_loader() {
        $.ajax({
            url: '/api/load/' + location + '/',
            method: 'GET',
            data: {'search': search_data},
            success: function(data) {
            if (data.status == 'ok') {
                $('#add-loader').html(data.html) // При 200 ОК append в div c id 'add-loader'.
                since = data.since      // c какого id делать выборку
                inProgress = false
            }
            else {
                $('#add-loader').html('<h1>Ничего не найдено</h1>')
            }
           }
        })
    }

    //////////////////////////////////////////////////////////

    $(window).bind('scroll', loader)
    function loader() {

        if ((($(window).height() + $(window).scrollTop()) > ($(document).height() - 200)) && !inProgress){
                 $.ajax({
                    url: '/api/load/' + location + '/',
                    method: 'GET',
                    data: {'since': since, 'search': search_data}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
                    beforeSend: function() {
                        inProgress = true // что бы больше не один scroll не вызвал ajax до завершения этого
                    },
                   success: function(data) {
                        if (data.status == 'ok') {           // при 'ok' продолжаю
                            $('#add-loader').append(data.html)
                            since = data.since
                            inProgress = false
                        }
                        else {
                            inProgress = true
                        }
                    }

                 })
        }
    }
})

