$('[data-action="show-more-recommend"]').on('click', function(){

    $.ajax({
        url: '/api/home/recommends/',
        method: 'GET',
        success: function(data) {
           $('#recommend-body').html(data.html)
           $('#modal-recommend').modal('show')
        }
    })


})