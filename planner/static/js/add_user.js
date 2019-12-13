$(document).ready(function () {
    $('.add-user-form').hide();
});
$(document).on('click', '.add-user-btn', function () {
    $('.add-user-form').show();
    $('.add-user-input').focus();
    $('.add-user-btn').hide();
});
$(document).on('focusout', '.add-user-form', function () {
    $('.add-user-form').hide();
    $('.add-user-btn').show();
});