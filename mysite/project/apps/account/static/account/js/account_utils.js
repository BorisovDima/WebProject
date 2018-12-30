

var type = ''
var user = ''

$('[data-action="modal-image-change"]').on('click', function(){
    $('[data-action="change-photo-button"]').hide()
    type = $(this).data('type')
    user = $(this).data('id')
    console.log(type, user)
    html = '<img id="' + type + '-user" class="img-fluid" >'
    $('#container-' +  type).html(html)
    $('[for="' + type + '"]').show()
})



$('input[data-action="change-profile-image"]').on('change', function(){
        $('[data-action="change-photo-button"]').unbind('click')
        var input = $(this)
        var field = input.attr('name')
        if (input[0].files && input[0].files[0]) {
            var reader = new FileReader();
            var cropper = ''
            reader.onload = function (e) {
                if (type == 'change-photo') {
                ratio =  1/1
                minCropH =  250
                minCropW =  250
                }
                else {
                ratio =  30/9
                minCropH =  200
                minCropW =  1200
            }
            $('#' + type + '-user').attr('src', e.target.result)
            image = document.getElementById(type + '-user');
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
            $('[for="' + type + '"]').hide()

            $('[data-action="change-photo-button"]').click(function(){
                $('[data-action="change-photo-button"]').hide()
                cropper.getCroppedCanvas().toBlob(image_loader, input[0].files[0].type, 1)

                function image_loader(blob) {
                    var file = new File([blob], input[0].files[0].name, {'type': input[0].files[0].type});
                    var formData = new FormData();
                    formData.append(field, file);
                    $.ajax({
                        url: '/profile/' + user + '/' + type + '/',
                        method: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function(data){
                            location.reload()
                        },
                        fail: function(data) {
                            html = '<h5 class="text-danger" data-type="error-image"></h5>'
                            $('#container-' +  type).html(html)
                            data = JSON.parse(data.responseText)
                            if (data['image']) {
                                $('[data-type="error-image"]').text(data['image'])
                            }
                            else {
                                $('[data-type="error-image"]').text(data['head'])
                            }
                        }
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





