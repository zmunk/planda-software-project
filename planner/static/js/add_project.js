$(document).ready(function () {
    $("#add-project-form").hide();
    $(document).on("click", function (event) {
        $("#add-project-form").hide();
        $("#add-project-btn").show();

    });
    $("#add-project-btn").on("click", function (event) {
        event.stopPropagation();
        $("#add-project-form").show();
        $("#add-project-btn").hide();
    });

    $("#add-project-form").on("click", function (event) {
        event.stopPropagation();
    })
});