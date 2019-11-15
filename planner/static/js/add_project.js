$(document).ready(function () {
    $("#add-project-form").hide(); // start by hiding add-project input

    $("#add-project-btn").on("click", function () {
        // when add-project button is clicked, hide button and show input
        $("#add-project-form").show();
        $("#add-project-input").focus();
        $("#add-project-btn").hide();
    });

    $("#add-project-input").focusout(function() {
        // when add-project input is no longer focused (clicked outside), show button and hide input
        $("#add-project-form").hide();
        $("#add-project-btn").show();
    });
});