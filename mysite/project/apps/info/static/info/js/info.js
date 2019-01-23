$(document).ready(function(){

var url = $('#body-info').data('id')
var language = $('#body-info').data('language')
get_template(url)

function get_template(url) {
    $.ajax({
        url: '/' + language + '/info/load_template/' + url + '/',
        method: 'GET',
        success: function(data) {
            $("#body-info").html(data.html)
        }
    })
}


$('[data-action="info-page"]').on('click', function() {

    var new_url = $(this).data('type')
    $('[data-action="info-page"]').removeClass('my_active')
    $(this).addClass('my_active')
    window.history.pushState("", "", '/' + language + '/info/' + new_url + '/');
    get_template(new_url)
})


$('#info-container').on('hide.bs.modal', function(){
    $('#info-email-captcha').hide()
})





$(document).on('click', '[data-action="support-message"]', function(){
    var type = $(this).data('type')
    if (type == 'email') {
        $('#info-email-captcha').show()
    }
    console.log(type)
    $.ajax({
        url: '/' + language + '/info/send/' + type + '/',
        method: 'GET',
        success: function(data) {
            $('#modal-info').html(data.html)
            $('#info-container').modal('show')
            autosize($('[data-type="info-form"]'));
         },

    })
})


$(document).on('click', '[data-action="send-question"]', function(){
       var type = $(this).data('type')
       var sgk = grecaptcha.getResponse()
       var body = $('#id_body').val()
       var title = $('#id_title').val()
       var email = $('#id_email').val()
        $.ajax({
            url: '/' + language + '/info/send/' + type + '/',
            method: 'POST',
            data: {'g-recaptcha-response': sgk, 'body': body, 'title': title, 'email': email},
            success: function(data) {
                $('#info-email-captcha').hide()
                $('#modal-info').html(data.html)


                },
            error: function(data){
                if (data.status = 400) {
                    data = JSON.parse(data.responseText)
                     $('[data-id="body-error"]').text(data['body'] || '')
                     $('[data-id="title-error"]').text(data['title'] || '')
                     $('[data-id="captcha-error"]').text(data['captcha'] || '')
                    setTimeout(function () {
                          $('[data-id="body-error"]').text('')
                          $('[data-id="title-error"]').text('')
                          $('[data-id="captcha-error"]').text('')
                    }, 1500)
                }

            }

        })

})


})