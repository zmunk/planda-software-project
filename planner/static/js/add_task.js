function add_task_clicked(category_id) {
    let form_id = "#task-form-" + category_id;
    let input_id = "#task-input-" + category_id;
    let btn_id = "#task-btn-" + category_id;
    $(form_id).show();
    $(input_id).focus();
    $(btn_id).hide();
}

function add_task_form_unfocused() {
    $(".add-task-form").hide();
    $(".add-task-btn").show();
}


// $(document).ready(function () {
//     // alert('ahasdf');
//     // $(".add-task-form").hide(); // start by hiding add-task inputs
// });

