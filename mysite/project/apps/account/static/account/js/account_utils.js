$(function(){
    $("#change-photo").change(function(){
        $("#change-photo-form").submit();
        $("#change-photo-form").hide();

    });
});


$("#change-header").change(function(){
    $("#change-head-form").submit();
    $("#change-head-form").hide();

});



moment.locale('ru')
$(function() {
    $('[data-action="date-birthday"]').daterangepicker({
    singleDatePicker: true,
    showDropdowns: true,
    maxYear: 2016,
    minYear: 1941,
    locale: {
    format: 'DD.MM.YYYY',
    }
    });
});

$('[data-action="edit-profile-show"]').click(function() {
    $('#my-profile-info').hide()
    $('[data-type="hide_form"]').show()
    $('#header_user').show()
    $("html,body").scrollTop($('[data-type="hide_form"]').offset().top - 100)
    $("#id_user_name").focus()

})

$('[data-action="profile-cancel"]').click(function(){
    $('[data-type="hide_form"]').hide()
    $('#header_user').hide()
    $('#my-profile-info').show()

})