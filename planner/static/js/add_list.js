$(document).ready(function () {
    $("#add-list-form").hide(); // start by hiding add-list input

    $("#add-list-btn").on("click", function () {
        // when add-list button is clicked, hide button and show input
        $("#add-list-form").show();
        $("#add-list-input").focus();
        $("#add-list-btn").hide();
    });

    $("#add-list-input").focusout(function() {
        // when add-list input is no longer focused (clicked outside), show button and hide input
        $("#add-list-form").hide();
        $("#add-list-btn").show();
    });
});