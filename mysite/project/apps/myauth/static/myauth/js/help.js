
$('#send-activate').on('click', function(){
    var email = $('#id_email').val()
    var sgk = grecaptcha.getResponse()
    console.log(sgk)
    $.ajax({
        url: '/login/help/',
        method: 'POST',
        data: {'email': email, 'g-recaptcha-response': sgk},
        success: function(data){
            console.log(data.email)
            $('[data-type="error"]').text('')
            $('#body-activate-email').hide()
            text = 'Письмо с ссылкой на активацию было успешно отправленно на вашу почту ' + data.email
            $('#info-success').text(text)
        },
        fail: function(data){
            data = JSON.parse(data.responseText)
            $("#error-captcha").text(data['captcha'] || '')
            $("#error-email").text(data['email'] || '')
        }
    })

})