$(document).on('click', '.task-delete-btn', function () {
    return confirm('Are you sure you want to delete this task?');
});

$(document).on('click', '.category-delete-btn', function () {
    return confirm('Are you sure you want to delete this list?');
});