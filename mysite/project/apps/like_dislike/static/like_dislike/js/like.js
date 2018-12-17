var ready = true

$(document).on('click', '[data-action="like-counter"]', function(e){
   var like = $(this)
   var type = like.data('type')
   var id = like.data('id')
   if (ready) {
    $.ajax({
        url: '/api/like/' + type + '/' + id + '/',
        method: 'POST',
        beforeSend: function() {
          ready = false // что бы больше не один scroll не вызвал ajax до завершения этого
        },
        complete: function() {
           ready = true // теперь может вызываться следующий ajax
        }
    }).success(function(data) {
          like.find('[data-count="like"]').text(data.count)
          if (data.add == true) {
                like.find('[data-target="like-image"]').attr('src', '/static/blog/img/icon-like-active.png')
          }
          else {
                like.find('[data-target="like-image"]').attr('src', '/static/blog/img/icon-like.png')
          }
    })
    }
});
