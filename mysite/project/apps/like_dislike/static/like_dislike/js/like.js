

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$.ajaxSetup({
       headers: { "X-CSRFToken": getCookie("csrftoken") }
 });


$('[data-action="like-counter"]').click(function() {
   var like = $(this)
   var type = like.data('type')
   var id = like.data('id')
    $.ajax({
        url: '/api/like/' + type + '/' + id + '/',
        method: 'POST'
    }).success(function(data) {
          like.find('[data-count="like"]').text(data.count)
    })

});
