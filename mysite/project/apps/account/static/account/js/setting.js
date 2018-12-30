$('[data-action="change-settings"]').on('click', function() {
    var old = $('[name="old_password"]').val()
    var new1 = $('[name="new_password1"]').val()
    var new2 = $('[name="new_password2"]').val()
    var email = $('[name="email"]').val()
    var event = $(this).data('event')
    var type = $(this).data('type')
    $(this).hide()
    $.ajax({
        url: '/profile/' + type + '/',
        method: 'POST',
        data: {"old_password": old, "new_password1": new1, "new_password2": new2, 'email': email},
        success: function(data){
            if (data.type == 'password') {
                $('#form-pass').hide()
                $('#pass-success').text(data.text)
            }
            if (data.type == 'email') {
                $('#form-email').hide()
                $('#email-success').text(data.text)
                $('#cur_email').text(email)

            }
        },
        fail: function(data) {
            data = JSON.parse(data.responseText)
            $('#old_password-error').text(data['old_password'] || '')
            $('#new_password1-error').text(data['new_password1'] || '')
            $('#new_password2-error').text(data['new_password2'] || '')
            $('#email-error').text(data['email'] || '')
            $(this).show()
            $('[data-action="change-settings"]').show()
        }
    })
})