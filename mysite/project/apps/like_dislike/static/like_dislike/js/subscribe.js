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


 $('[data-action="user-subscribe"]').click(function() {
   var subscribe = $(this)
   var type = subscribe.data('type')
   var id = subscribe.data('id')
    $.ajax({
        url: '/api/subscribe/' + type + '/' + id + '/',
        method: 'POST'
    }).success(function(data) {
          if (data.add == true) {
                subscribe.removeClass( "btn-danger" ).addClass( "btn-success" );
                subscribe.text('Unsubscribe')
                $('#count-followers').text(data.count)
          }
          else {
                subscribe.removeClass( "btn-success" ).addClass( "btn-danger" );
                subscribe.text('Subscribe')
                $('#count-followers').text(data.count)
          }
    })

});