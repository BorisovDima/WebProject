$(document).ready(function(){
    var search_data = ''
    var inProgress = true
    var since = ''
    var start_location = $('#location').data('id')
    var location =  $('#location').val()
    start_loader()

    //////////////////////////////////////////////////////////
    $("#search-form-ajax").on('keypress', function(e) {
        if(e.which == 13) {
            search_data = $('#search-form-ajax').val()
            $('#search-cur-value').text(search_data)
            inProgress = true
            location = $('#location').val()
            location = location + '/' + $('[data-action="choice-sort"]').val()
            $('#add-loader').html('')
            start_loader()
        }
    })
    //////////////////////////////////////////////////////////

    $('[data-action="choice-sort"]').on('change', function(e){
           inProgress = true
           location = $('#location').val() + '/' + $(this).val()
           $('#add-loader').html('')
           start_loader()
    })



    ///////////////////////////////////////////////////////////
    $('[data-action="ajax-paginate-btn"]').click(function(){
        inProgress = true
        search_data = ''
        $("#search-form-ajax").val('')
        $('#search-cur-value').text('')
        var event = $(this)
        $('[data-action="ajax-paginate-btn"]').removeClass('my_active')
        event.addClass('my_active')
        var type = event.data('type')
        if (type) {
            path = start_location + '/' + type
           }
        else {
            path = start_location
        }
        $('#location').val(path)
        $('#add-loader').html('')
        location = path
        window.history.pushState("", "", '/' + start_location + '/' + type);
        start_loader()
    })

    //////////////////////////////////////////////////////////

    function start_loader() {
        if ($('#location').val()  == 'm/people' || $('#location').val()   ==  'm/communities') {
            $('#search-main').show()
        }
        else {
            $('#search-main').hide()
        }
        $.ajax({
            url: '/api/load/' + location + '/',
            method: 'GET',
            data: {'search': search_data},
            success: function(data) {
            if (data.status == 'ok') {
                $('#add-loader').append(data.html) // При 200 ОК append в div c id 'add-loader'.
                since = data.since      // c какого id делать выборку
                inProgress = false     //( для условия && !inProgress)
            }
            else {
                $('#add-loader').append('<h1>Ничего не найдено</h1>')
            }
           }
        })
    }

    //////////////////////////////////////////////////////////

    $(window).bind('scroll', loader)
    function loader() {
        //  Жду пока scroll достигнет Button-200 и выполнится первый ajax запрос, чтобы поставить
        // inProgress в false

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
