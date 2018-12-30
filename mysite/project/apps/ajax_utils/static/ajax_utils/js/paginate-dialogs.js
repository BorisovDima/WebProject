var since = ''
var btn = '<button type="button" id="button-dialogs-action" class="btn btn-outline-danger align-self-center btn-sm py-0">Загрузить еще</button>'
var body = ''
var div = ''
var type = ''

$('[data-action="load-modal-notifications"]').click(function(){
    type = $(this).data('type')
    console.log(type)
    if (type == 'notify'){
        $('#counter-notify').html('')
    }
    body = '#list-' + type + '-body'
    div = '#button-' + type + '-div'
    $(body).html('')
    $.ajax({
        url: '/api/load/' + type + '/',
        method: 'GET',
        success: function(data) {
          $(body).append(data.html) // При 200 ОК append в div c id 'add-loader'.
          since = data.since      // c какого id делать выборку
          if (data.button) {
                $(div).html(btn)
                $(div).bind('click', loader_dialogs)
           }
        }
    })
})

function loader_dialogs(){
    $.ajax({
            url: '/api/load/' + type + '/',
            method: 'GET',
            data: {'since': since}, //c какого id делать выборку и obj_id'(может быть категория, пост или None).
            success: function(data) {
                   $(body).append(data.html) // При 200 ОК append в div c id 'add-loader'.
                    since = data.since      // c какого id делать выборку
                    if (!data.button) {
                           $(div).html('')
                           $(div).unbind('click')
                     }
            }
    })
}




