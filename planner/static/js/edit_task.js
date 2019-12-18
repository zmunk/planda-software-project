function edit_task_clicked(task_id) {
    let form_id = "#edit-task-form-" + task_id;
    let input_id = "#edit-task-input-" + task_id;
    let task_block_id = "#task-block-" + task_id;
    let task_text_id = "#task-text-" + task_id;
    let task_text = $(task_text_id).text();
    // alert(task_text);
    $(form_id).show();
    $(input_id).val(task_text);
    $(input_id).select();

    // $(input_id).focus();
    // $(input_id).click(function() {$(this).select();});
    $(task_block_id).hide();
}

function edit_task_form_unfocused() {
    $(".edit-task-form").hide();
    $(".task-block").show();
}