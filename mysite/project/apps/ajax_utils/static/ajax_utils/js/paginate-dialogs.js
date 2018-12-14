var since = ''
var btn = '<button type="button" id="button-dialogs-action" class="btn btn-outline-danger align-self-center btn-sm py-0">Загрузить еще</button>'

$('#load-my-dialogs').click(function(){
    var user = $(this).data('id')
    $('#list-dialogs-body').html('')
    $.ajax({
        url: '/api/load/dialogs/' + user + '/',
        method: 'GET'
    }).success(function(data) {
          $('#list-dialogs-body').append(data.html) // При 200 ОК append в div c id 'add-loader'.
          since = data.since      // c какого id делать выборку
          if (data.button) {
                $('#button-dialogs-div').html(btn)
                $('#button-dialogs-div').bind('click', function(){
                                                test(user)
                                                                })
          }
    })
})

function test(user){
    console.log(since)
    console.log(user)
    $.ajax({
            url: '/api/load/dialogs/' + user + '/',
            method: 'GET',
            data: {'since': since}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
            }).success(function(data) {
                   $('#list-dialogs-body').append(data.html) // При 200 ОК append в div c id 'add-loader'.
                    since = data.since      // c какого id делать выборку
                    if (!data.button) {
                           $('#button-dialogs-div').html('')
                           $('#button-dialogs-div').unbind('click')
                     }
            }).error(function(data) {
                    console.log('error')

            })
}




