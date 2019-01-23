
var type = ''
var user = ''

$('[data-action="modal-image-change"]').on('click', function(){
    $('[data-action="change-img-errors"]').text('')
    type = $(this).data('type')
    user = $(this).data('id')
    $('#container-change-photo').html('<img id="change-photo-img-src" class="img-fluid" >')
    $('[for="change-photo"]').show()
})

$('#modal-photo-img').on('hide.bs.modal', function(){
    $('[data-action="change-photo-button"]').hide()
    $('#container-change-photo').html('')

})

$('input[data-action="change-profile-image"]').on('change', function(){
        $('[data-action="change-photo-button"]').unbind('click')
        var input = $(this)
        var field = type
        if (input[0].files && input[0].files[0]) {
            var reader = new FileReader();
            var cropper = ''
            reader.onload = function (e) {
                if (type == 'image') {
                ratio =  1/1
                minCropH =  250
                minCropW =  250
                }
                else {
                ratio =  34/9
                minCropH =  200
                minCropW =  1200
            }
            $('#change-photo-img-src').attr('src', e.target.result)
            image = document.getElementById('change-photo-img-src');
            cropper = new Cropper(image, {aspectRatio: ratio, viewMode: 1,
                minCropBoxHeight: minCropH,
                minCropBoxWidth: minCropW,
                fillColor: '#fff',
                imageSmoothingEnabled: false,
                imageSmoothingQuality: 'high',
                })
                cropper.crop()
            };
            reader.readAsDataURL(input[0].files[0]);
            $('[data-action="change-photo-button"]').show()
            $('[for="change-photo"]').hide()

            $('[data-action="change-photo-button"]').click(function(){
                $('[data-action="change-photo-button"]').hide()
                cropper.getCroppedCanvas().toBlob(image_loader, input[0].files[0].type, 1)

                function image_loader(blob) {
                    var file = new File([blob], input[0].files[0].name, {'type': input[0].files[0].type});
                    var formData = new FormData();
                    formData.append(field, file);
                    $.ajax({
                        url: '/p/' + user + '/change/' + type + '/',
                        method: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function(data){
                            location.reload()
                        },
                        error: function(data) {
                            if (data.status == 400) {
                                data = JSON.parse(data.responseText)
                                 $('[data-type="error-change-photo"]').text(data['image'] || '')
                                 $('[data-type="error-change-header"]').text(data['head'] || '')

                                    setTimeout(function () {
                                    $('#modal-photo-img').modal('hide')
                                    }, 1000)

                            }
                        },

                    })

                }
            })

        }

});




$('[data-action="edit-profile-show"]').click(function() {
    $('#my-profile-info').hide()
    $('[data-type="hide_form"]').show()
    $('#header_user').show()
    $('#profile-head-main').addClass('shadow_header border border-danger')
    $('#hide-change-header').show()
    $("html,body").scrollTop()
    $("#id_user_name").focus()
})



$('[data-action="profile-cancel"]').click(function(){
    $('[data-type="hide_form"]').hide()
    $('#header_user').hide()
    $('#my-profile-info').show()
    $('#profile-head-main').removeClass('shadow_header border border-danger')
    $('#hide-change-header').hide()
})





