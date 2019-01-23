$(document).ready(function(){
    var search_data = ''
    var inProgress = true
    var since = ''
    var model = $('#location').data('type')
    var location =  $('#location').val()
    var start_location = $('#location').data('start')
    var id_location = $('#location').data('detail') || ''
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
        model = event.data('type')
        location = event.data('sort')
        $('#location').val(location)
        $('#add-loader').html('')
        if (event.data('add')=='False'){
            path = start_location
        }
        else {
            path = start_location + '/' + location
        }
        window.history.pushState("", "", '/' + path + '/');
        start_loader()
    })

    //////////////////////////////////////////////////////////

    function start_loader() {
        console.log(model)
        if (model  == 'user') {
            $('#search-main').show()
        }
        else {
            $('#search-main').hide()
        }
        console.log('/api/load/' + model + '/' + location + '/')
        $.ajax({
            url:'/api/load/' + model + '/' + location + '/',
            method: 'GET',
            data: {'q': search_data, 'f': id_location},
            success: function(data) {
            if (data.status == 'ok') {
                $('#add-loader').append(data.html)
                since = data.since
                inProgress = false
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

        if ((($(window).height() + $(window).scrollTop()) > ($(document).height() - 200)) && !inProgress){
                 $.ajax({
                    url: '/api/load/' + model + '/' + location + '/',
                    method: 'GET',
                    data: {'since': since, 'q': search_data, 'f': id_location}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
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
