

$(document).ready(function(){
    $('#btn-registr').click(function() {
    $('#btn-registr').hide()

    var login = $('#id_username').val()
    var pas1 = $('#id_password1').val()
    var pas2 = $('#id_password2').val()
    var mail = $('#id_email').val()
    var sgk = grecaptcha.getResponse()
    $.ajax({
        url: '/registration/',
        method: 'POST',
        data: {'username': login, 'password1': pas1, 'password2': pas2, 'email': mail, 'g-recaptcha-response': sgk},
        success: function(data){
            $('[data-type="info-error"]').text('')
            console.log(data)
            $('#registration-body-modal').html(data.html)
        },
        error: function(data){
            if (data.status == 400) {
                data = JSON.parse(data.responseText)
                $('#error-username').text(data['username'] || '')
                $('#error-password1').text(data['password1'] || '')
                $('#error-password2').text(data['password2'] || '')
                $('#error-email').text(data['email'] || '')
                $('#error-captcha').text(data['captcha'] || '')
                $('#btn-registr').show()
            }
        }

    })

})

    $('#forgot-pass-btn').on('click', function() {
        var data = $('#forgot-pass-input').val()
        if (data.length > 0) {
             $.ajax({
                url: '/login/password-reset/',
                method: 'POST',
                data: {'email': data},
                success: function(data){
                    $('#reset-password-body').html(data.html)
                }
             })
        }

    })

})



