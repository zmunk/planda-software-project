function edit_task_clicked(task_id) {
    let form_id = "#edit-task-form-" + task_id;
    let input_id = "#edit-task-input-" + task_id;
    let task_text_id = "#task-text-" + task_id;
    $(form_id).show();
    $(input_id).focus();
    $(task_text_id).hide();
}

function edit_task_form_unfocused() {
    $(".edit-task-form").hide();
    $(".task-text").show();
}