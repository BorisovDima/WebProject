
$(document).on("mouseenter", '[data-action="parent-color"]', function (event) {
     var location = '#comment-' + $(this).data('id')
     $(location).css({'background' : '#d3dcea'})

})


$(document).on("mouseleave", '[data-action="parent-color"]', function (event) {
     var location = '#comment-' + $(this).data('id')
     $(location).css({'background' : '#ffffff'})

})

$(document).on('click', '[data-action="answer"]', function(e) {
    var initial = $(this).data('initial')
    var parent = $(this).data('id')
    var name = $(this).data('name')
    html = '<div class="form-group mb-0"> <input type="hidden" value="' + parent + '"><textarea style="resize: none; font-size: 14px; overflow: hidden; overflow-wrap: break-word;" rows="1" class="form-control" maxlength="220" placeholder="Ответить ' + name + '"  colls="40" data-type="data-form" ></textarea> <input data-action="comment-send" type="button" class="btn btn-link btn-sm mb-0" value="Отправить"/></div>'
    $('#comment-answer-' + initial).html(html)
    autosize($('#comment-answer-' + initial).find('textarea[data-type="data-form"]'));
})


$(document).on('click', '[data-action="loader-child"]', function(e) {
    var initial = $(this).data('id')
    $.ajax({
        url: '/api/load-comment-child/' + initial + '/',
        method: 'GET',
        success: function(data) {
            $('#comment-new-' + initial).html(data.html)
        }
    })
})